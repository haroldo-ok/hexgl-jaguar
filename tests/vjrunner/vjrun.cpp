//
// vjrun - headless Virtual Jaguar runner used by the HexGL Jaguar port
//         end-to-end test suite.
//
// This program embeds the Virtual Jaguar emulation core (TOM/JERRY/M68000/
// GPU/DSP/OP/blitter - the very same sources that the Virtual Jaguar GUI uses)
// and drives it exactly like the GUI's main loop does:
//
//     JaguarInit() -> SelectBIOS() -> load cart ROM -> JaguarSetScreenBuffer()
//     -> JaguarReset() -> [ JaguarExecuteNew() per video field ]
//
// The de-facto output of TOM (the object processor output as RGBA pixels) is
// read back every field, analysed for "is the picture alive?" metrics and can
// be dumped as PNG files.  It is *not* a replacement emulator front end: it is
// the test harness of the port.
//
// Exit code 0 = all checks passed, 1 = a check failed, 2 = usage/setup error.
//

#include <SDL.h>

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <map>
#include <algorithm>

#include <zlib.h>

#include "jaguar.h"
#include "tom.h"
#include "memory.h"
#include "settings.h"
#include "modelsBIOS.h"
#include "gpu.h"
#include "dsp.h"
#include "dac.h"
#include "eeprom.h"
#include "joystick.h"
#include "version.h"
#include "m68000/m68kinterface.h"

// ---------------------------------------------------------------------------
// screen buffer (what the Qt GUI hands to TOM through JaguarSetScreenBuffer)
// ---------------------------------------------------------------------------

#define FB_PITCH  1024
#define FB_HEIGHT 512

static uint32_t framebuffer[FB_PITCH * FB_HEIGHT];

// ---------------------------------------------------------------------------
// tiny PNG writer (RGBA 8-bit)
// ---------------------------------------------------------------------------

static void put32be(std::vector<uint8_t> &v, uint32_t x)
{
    v.push_back((x >> 24) & 0xFF);
    v.push_back((x >> 16) & 0xFF);
    v.push_back((x >> 8) & 0xFF);
    v.push_back(x & 0xFF);
}

static void putChunk(std::vector<uint8_t> &out, const char *tag,
                     const std::vector<uint8_t> &data)
{
    put32be(out, (uint32_t)data.size());
    for (int i = 0; i < 4; i++) out.push_back((uint8_t)tag[i]);
    out.insert(out.end(), data.begin(), data.end());
    uint32_t crc = (uint32_t)crc32(0, (const Bytef *)tag, 4);
    crc = (uint32_t)crc32(crc, (const Bytef *)data.data(), (uInt)data.size());
    put32be(out, crc);
}

static bool writePNG(const char *path, const uint8_t *rgbx, int w, int h)
{
    // rgbx: w*h*4 bytes, R,G,B,A order
    std::vector<uint8_t> raw;
    raw.reserve((size_t)h * (1 + (size_t)w * 3));
    for (int y = 0; y < h; y++) {
        raw.push_back(0); // filter: none
        const uint8_t *src = rgbx + (size_t)y * w * 4;
        for (int x = 0; x < w; x++) {
            raw.push_back(src[x * 4 + 0]);
            raw.push_back(src[x * 4 + 1]);
            raw.push_back(src[x * 4 + 2]);
        }
    }
    uLongf clen = compressBound((uLong)raw.size());
    std::vector<uint8_t> comp(clen);
    if (compress2(comp.data(), &clen, raw.data(), (uLong)raw.size(), 6) != Z_OK)
        return false;
    comp.resize(clen);

    std::vector<uint8_t> png;
    const uint8_t sig[8] = { 0x89, 'P', 'N', 'G', '\r', '\n', 0x1A, '\n' };
    png.insert(png.end(), sig, sig + 8);

    std::vector<uint8_t> ihdr;
    put32be(ihdr, (uint32_t)w);
    put32be(ihdr, (uint32_t)h);
    ihdr.push_back(8);  // bit depth
    ihdr.push_back(2);  // colour type: truecolour
    ihdr.push_back(0);
    ihdr.push_back(0);
    ihdr.push_back(0);
    putChunk(png, "IHDR", ihdr);
    putChunk(png, "IDAT", comp);
    putChunk(png, "IEND", std::vector<uint8_t>());

    FILE *fp = fopen(path, "wb");
    if (!fp) return false;
    fwrite(png.data(), 1, png.size(), fp);
    fclose(fp);
    return true;
}

// ---------------------------------------------------------------------------
// frame analysis
// ---------------------------------------------------------------------------

struct FrameStats
{
    int      frame       = 0;
    int      width       = 0;
    int      height      = 0;
    long     pixels      = 0;
    long     nonzero     = 0;   // pixels that are not pure black
    int      avgLuma     = 0;   // 0..255
    int      maxLuma     = 0;
    uint64_t hash        = 0;   // FNV-1a over the visible picture
    long     changed     = -1;  // pixels differing from previous field
    uint32_t gpuPC       = 0;
    uint32_t game[20] = {};
    uint32_t audioSamples = 0;
    long worldChanged = 0, worldLit = 0;
    long audioNonzero = 0;
    uint32_t dacWrites   = 0;
};

static long g_prevPictureHashCount = 0;
static std::vector<uint32_t> g_prevPicture;

static FrameStats analyseFrame(int frame)
{
    FrameStats st;
    st.frame = frame;

    int w = (int)TOMGetVideoModeWidth();
    if (w <= 0 || w > FB_PITCH) w = FB_PITCH;
    // PAL: 256 visible halflines, NTSC: 240
    int h = vjs.hardwareTypeNTSC ? 240 : 256;

    st.width = w;
    st.height = h;

    uint64_t hash = 1469598103934665603ULL;
    long nonzero = 0;
    uint64_t lumaSum = 0;
    int maxLuma = 0;
    std::vector<uint32_t> picture;
    picture.resize((size_t)w * h);

    for (int y = 0; y < h; y++) {
        const uint32_t *row = &framebuffer[(size_t)y * FB_PITCH];
        for (int x = 0; x < w; x++) {
            uint32_t px = row[x];
            picture[(size_t)y * w + x] = px;
            uint8_t r = px >> 24, g = (px >> 16) & 0xFF, b = (px >> 8) & 0xFF;
            int luma = (r * 30 + g * 59 + b * 11) / 100;
            lumaSum += luma;
            if (luma > maxLuma) maxLuma = luma;
            if (px & 0xFFFFFF00) nonzero++;
            if(x>w/4 && x<3*w/4 && y>110 && y<195){
                if(luma>5)st.worldLit++;
                if(g_prevPicture.size()==picture.size() && px!=g_prevPicture[(size_t)y*w+x]) st.worldChanged++;
            }
            hash ^= (px & 0xFFFFFFFF);
            hash *= 1099511628211ULL;
        }
    }

    st.pixels  = (long)w * h;
    st.nonzero = nonzero;
    st.avgLuma = (int)(lumaSum / (uint64_t)st.pixels);
    st.maxLuma = maxLuma;
    st.hash    = hash;

    if (g_prevPicture.size() == picture.size()) {
        long changed = 0;
        for (size_t i = 0; i < picture.size(); i++)
            if (picture[i] != g_prevPicture[i]) changed++;
        st.changed = changed;
    }
    g_prevPicture.swap(picture);
    (void)g_prevPictureHashCount;

    st.gpuPC     = GPUGetPC();
    st.dacWrites = dacWriteCount;
    for(int i=0;i<20;i++) st.game[i]=GET32(jaguarMainRAM,0x1000+4*i);
    st.audioSamples=GET32(jaguarMainRAM,0x1084);

    return st;
}

static void dumpPNG(const std::string &path, int w, int h)
{
    std::vector<uint8_t> rgbx((size_t)w * h * 4);
    for (int y = 0; y < h; y++) {
        const uint32_t *row = &framebuffer[(size_t)y * FB_PITCH];
        for (int x = 0; x < w; x++) {
            uint32_t px = row[x];
            rgbx[((size_t)y * w + x) * 4 + 0] = (px >> 24) & 0xFF;
            rgbx[((size_t)y * w + x) * 4 + 1] = (px >> 16) & 0xFF;
            rgbx[((size_t)y * w + x) * 4 + 2] = (px >> 8) & 0xFF;
            rgbx[((size_t)y * w + x) * 4 + 3] = 0xFF;
        }
    }
    if (!writePNG(path.c_str(), rgbx.data(), w, h))
        fprintf(stderr, "vjrun: could not write '%s'\n", path.c_str());
    else
        printf("vjrun: wrote %s\n", path.c_str());
}

// ---------------------------------------------------------------------------
// input scripting:  "frame=field:buttons" e.g. 60:A,90:A+RIGHT,150:none
// ---------------------------------------------------------------------------

struct InputEvent { int frame; std::vector<int> buttons; std::string text; };

static int buttonFromName(const std::string &n)
{
    if (n == "up")     return BUTTON_U;
    if (n == "down")   return BUTTON_D;
    if (n == "left")   return BUTTON_L;
    if (n == "right")  return BUTTON_R;
    if (n == "a")      return BUTTON_A;
    if (n == "b")      return BUTTON_B;
    if (n == "c")      return BUTTON_C;
    if (n == "start")  return BUTTON_s;
    if (n == "option") return BUTTON_OPTION;
    if (n == "pause")  return BUTTON_PAUSE;
    return -1;
}

static std::vector<InputEvent> parseScript(const std::string &spec)
{
    std::vector<InputEvent> evs;
    size_t pos = 0;
    while (pos < spec.size()) {
        size_t comma = spec.find(',', pos);
        std::string item = spec.substr(pos, comma == std::string::npos ? std::string::npos : comma - pos);
        pos = (comma == std::string::npos) ? spec.size() : comma + 1;
        if (item.empty()) continue;
        size_t colon = item.find(':');
        if (colon == std::string::npos) continue;
        InputEvent ev;
        ev.frame = atoi(item.substr(0, colon).c_str());
        std::string btns = item.substr(colon + 1);
        ev.text = btns;
        size_t bpos = 0;
        while (bpos < btns.size()) {
            size_t plus = btns.find('+', bpos);
            std::string one = btns.substr(bpos, plus == std::string::npos ? std::string::npos : plus - bpos);
            bpos = (plus == std::string::npos) ? btns.size() : plus + 1;
            int b = buttonFromName(one);
            if (b >= 0) ev.buttons.push_back(b);
        }
        evs.push_back(ev);
    }
    std::sort(evs.begin(), evs.end(), [](const InputEvent &a, const InputEvent &b) { return a.frame < b.frame; });
    return evs;
}

static void applyInput(const std::vector<InputEvent> &evs, int frame)
{
    // newest event at or before 'frame' wins
    int idx = -1;
    for (size_t i = 0; i < evs.size(); i++)
        if (evs[i].frame <= frame) idx = (int)i;
    for (int b = 0; b <= BUTTON_LAST; b++) joypad0Buttons[b] = 0;
    if (idx >= 0)
        for (int b : evs[idx].buttons) joypad0Buttons[b] = 1;
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

static void usage(const char *argv0)
{
    printf(
        "usage: %s [options] rom.j64\n"
        "  --frames N          number of video fields to emulate (default 600)\n"
        "  --pal | --ntsc      video standard for the emulated console (default ntsc)\n"
        "  --out DIR           directory for PNG dumps and the report\n"
        "  --dump-at N[,N..]   dump a PNG at these field numbers\n"
        "  --dump-every N      dump a PNG every N fields (0 = never)\n"
        "  --dump-max N        maximum number of PNG dumps (default 12)\n"
        "  --input SPEC        input script, eg. '30:start,120:a,200:a+left'\n"
        "  --require-live      fail if the picture is black for > N fields (default 45)\n"
        "  --title STR         name used in the report\n"
        "  --quiet             do not print per-field lines\n"
        "  --no-bios           boot from cartridge 68000 entry, like default GUI\n"
        "  --seed N            randomized power-on RAM seed\n"
        "  --blank-video-at N  negative control: black video, CPU/GPU still running\n"
        "  --freeze-video-at N negative control: frozen picture, game still running\n"
        "  --stop-on-finish    end after native phase 3 (HexGL finish)\n",
        argv0);
}

int main(int argc, char **argv)
{
    const char *romPath = nullptr;
    int frames = 600;
    std::string outDir = ".";
    std::string inputSpec;
    std::vector<int> dumpAt;
    int dumpEvery = 0;
    int dumpMax = 12;
    int liveLimit = 45;
    std::string title = "rom";
    bool quiet = false;
    bool stopFinish = false;
    int haltGpuAt = -1, blankVideoAt = -1, freezeVideoAt = -1;
    bool useBIOS = true;
    unsigned seed = 1;

    for (int i = 1; i < argc; i++) {
        std::string a = argv[i];
        if (a == "--frames" && i + 1 < argc)          frames = atoi(argv[++i]);
        else if (a == "--pal")                        vjs.hardwareTypeNTSC = false;
        else if (a == "--ntsc")                       vjs.hardwareTypeNTSC = true;
        else if (a == "--out" && i + 1 < argc)        outDir = argv[++i];
        else if (a == "--dump-at" && i + 1 < argc) {
            std::string s = argv[++i];
            size_t pos = 0;
            while (pos < s.size()) {
                size_t c = s.find(',', pos);
                dumpAt.push_back(atoi(s.substr(pos, c == std::string::npos ? std::string::npos : c - pos).c_str()));
                pos = (c == std::string::npos) ? s.size() : c + 1;
            }
        }
        else if (a == "--dump-every" && i + 1 < argc) dumpEvery = atoi(argv[++i]);
        else if (a == "--dump-max" && i + 1 < argc)   dumpMax = atoi(argv[++i]);
        else if (a == "--input" && i + 1 < argc)      inputSpec = argv[++i];
        else if (a == "--require-live" && i + 1 < argc) liveLimit = atoi(argv[++i]);
        else if (a == "--title" && i + 1 < argc)      title = argv[++i];
        else if (a == "--halt-gpu-at" && i+1<argc) haltGpuAt=atoi(argv[++i]);
        else if (a == "--no-bios") useBIOS = false;
        else if (a == "--seed" && i+1<argc) seed = (unsigned)atoi(argv[++i]);
        else if (a == "--blank-video-at" && i+1<argc) blankVideoAt=atoi(argv[++i]);
        else if (a == "--freeze-video-at" && i+1<argc) freezeVideoAt=atoi(argv[++i]);
        else if (a == "--stop-on-finish") stopFinish = true;
        else if (a == "--quiet")                      quiet = true;
        else if (a == "-h" || a == "--help") { usage(argv[0]); return 0; }
        else if (a.size() && a[0] == '-') { fprintf(stderr, "vjrun: unknown option '%s'\n", a.c_str()); return 2; }
        else romPath = argv[i];
    }

    if (!romPath) { usage(argv[0]); return 2; }

    // ---- settings (the same defaults the GUI uses) -------------------------
    memset(&vjs, 0, sizeof(vjs));
    vjs.hardwareTypeNTSC     = true;
    vjs.useJaguarBIOS        = useBIOS;
    vjs.useRetailBIOS        = true;
    vjs.GPUEnabled           = true;
    vjs.DSPEnabled           = true;
    vjs.usePipelinedDSP      = false;
    vjs.audioEnabled         = false;
    vjs.useJoystick          = false;
    vjs.renderType           = RT_NORMAL;
    vjs.biosType             = BT_NULL;      // resolved from jaguarModel -> K series
    vjs.jaguarModel          = JAG_K_SERIES;
    vjs.DRAM_size            = 0x200000;
    vjs.useFastBlitter       = false;
    vjs.allowM68KExceptionCatch = false;
    vjs.allowWritesToROM     = false;
    vjs.nbrdisasmlines       = 0;
    vjs.nbrmemory1browserwindow = 0;
    snprintf(vjs.EEPROMPath, MAX_PATH, "%s/eeprom.bin", outDir.c_str());
    snprintf(vjs.screenshotPath, MAX_PATH, "%s", outDir.c_str());

    // parse -pal again (it was parsed before memset above)
    for (int i = 1; i < argc; i++) {
        std::string s = argv[i];
        if (s == "--pal")  vjs.hardwareTypeNTSC = false;
        if (s == "--ntsc") vjs.hardwareTypeNTSC = true;
    }

    SDL_Init(SDL_INIT_TIMER);
    setenv("SDL_AUDIODRIVER", "dummy", 1);

    printf("vjrun: Virtual Jaguar core %s (built %s %s)\n", VJ_RELEASE_VERSION, __DATE__, __TIME__);
    printf("vjrun: rom='%s' fields=%d video=%s\n", romPath, frames, vjs.hardwareTypeNTSC ? "NTSC" : "PAL");

    // ---- read the ROM ------------------------------------------------------
    FILE *fp = fopen(romPath, "rb");
    if (!fp) { fprintf(stderr, "vjrun: cannot open '%s'\n", romPath); return 2; }
    fseek(fp, 0, SEEK_END);
    long romSize = ftell(fp);
    fseek(fp, 0, SEEK_SET);
    if (romSize <= 0 || romSize > 0x600000) { fprintf(stderr, "vjrun: bad rom size %ld\n", romSize); fclose(fp); return 2; }
    std::vector<uint8_t> rom((size_t)romSize);
    if (fread(rom.data(), 1, (size_t)romSize, fp) != (size_t)romSize) { fprintf(stderr, "vjrun: short read\n"); fclose(fp); return 2; }
    fclose(fp);
    printf("vjrun: rom size = %ld bytes\n", romSize);

    // ---- boot the virtual console -----------------------------------------
    vjs.DSPEnabled = false; // no nondeterministic host audio thread
    srand(seed);
    JaguarInit();
    vjs.DSPEnabled = true;
    if (!SelectBIOS(vjs.biosType)) { fprintf(stderr, "vjrun: no BIOS available!\n"); return 2; }

    JaguarSetScreenBuffer(framebuffer);
    JaguarSetScreenPitch(FB_PITCH);
    memset(framebuffer, 0, sizeof(framebuffer));

    jaguarROMSize      = (uint32_t)romSize;
    jaguarCartInserted = true;
    memcpy(jagMemSpace + 0x800000, rom.data(), (size_t)romSize);

    jaguarRunAddress = GET32(jagMemSpace, 0x800404);
    JaguarReset();
    SET32(jaguarMainRAM, 0, vjs.DRAM_size);
    m68k_pulse_reset();

    std::vector<InputEvent> script = parseScript(inputSpec);

    // ---- run ---------------------------------------------------------------
    std::vector<FrameStats> stats;
    stats.reserve((size_t)frames);

    int dumps = 0;
    int liveStreak = 0;       // consecutive fields whose picture is (nearly) black
    int worstLiveStreak = 0;
    int firstLiveFrame = -1;
    int lastLiveFrame = -1;
    long changingFields = 0;
    long staticStreak = 0, worstStaticStreak = 0;

    int w = (int)TOMGetVideoModeWidth();
    if (w <= 0 || w > FB_PITCH) w = FB_PITCH;
    int h = vjs.hardwareTypeNTSC ? 240 : 256;

    std::vector<uint32_t> frozenVideo;
    for (int f = 0; f < frames; f++) {
        if(f==haltGpuAt)vjs.GPUEnabled=false; // negative control, never a ROM feature
        applyInput(script, f);
        JaguarExecuteNew();
        extern void SDLSoundCallback(void*, Uint8*, int);
        Uint8 pcm[3840];
        SDLSoundCallback(nullptr,pcm,vjs.hardwareTypeNTSC ? 3200 : 3840);
        // Fault injection affects observed video only, not native state.
        if(f == freezeVideoAt) frozenVideo.assign(framebuffer, framebuffer+FB_PITCH*FB_HEIGHT);
        if(!frozenVideo.empty()) std::copy(frozenVideo.begin(),frozenVideo.end(),framebuffer);
        if(blankVideoAt >= 0 && f >= blankVideoAt) memset(framebuffer,0,sizeof(framebuffer));
        FrameStats st = analyseFrame(f);
        for(int i=0;i<(vjs.hardwareTypeNTSC?3200:3840);i++)if(pcm[i])st.audioNonzero++;
        stats.push_back(st);

        // "live" = there is something visible: either a decent number of lit
        // pixels or a decent average luma.  A black screen / crashed GPU has
        // neither.
        bool live = (st.nonzero > 200) || (st.avgLuma > 4);
        if (live) {
            if (firstLiveFrame < 0) firstLiveFrame = f;
            lastLiveFrame = f;
            liveStreak = 0;
        } else {
            liveStreak++;
            if (liveStreak > worstLiveStreak) worstLiveStreak = liveStreak;
        }

        if (st.changed > 0) { changingFields++; staticStreak = 0; }
        else { staticStreak++; if (staticStreak > worstStaticStreak) worstStaticStreak = staticStreak; }

        bool wantDump = false;
        if (std::find(dumpAt.begin(), dumpAt.end(), f) != dumpAt.end()) wantDump = true;
        if (dumpEvery > 0 && (f % dumpEvery) == 0) wantDump = true;
        if (wantDump && dumps < dumpMax) {
            char path[512];
            snprintf(path, sizeof(path), "%s/frame_%05d.png", outDir.c_str(), f);
            dumpPNG(path, st.width, st.height);
            dumps++;
        }

        if (!quiet && (f < 8 || f % 50 == 0 || liveStreak > 20))
            printf("vjrun: field %5d  nonzero=%6ld/%ld  avgLuma=%3d  changed=%8ld  gpuPC=%08X%s\n",
                   f, st.nonzero, st.pixels, st.avgLuma, st.changed, st.gpuPC,
                   live ? "" : "   <-- BLACK");
        if(stopFinish && st.game[0]==0x48455847 && st.game[2]==3){ frames=f+1; break; }
    }

    w=(int)TOMGetVideoModeWidth();
    dumpPNG(outDir+"/final.png",w,h);
    // ---- report ------------------------------------------------------------
    char path[512];
    snprintf(path, sizeof(path), "%s/%s_report.json", outDir.c_str(), title.c_str());
    FILE *rf = fopen(path, "w");
    if (rf) {
        fprintf(rf, "{\n");
        fprintf(rf, "  \"title\": \"%s\",\n", title.c_str());
        fprintf(rf, "  \"rom\": \"%s\",\n", romPath);
        fprintf(rf, "  \"video\": \"%s\",\n", vjs.hardwareTypeNTSC ? "NTSC" : "PAL");
        fprintf(rf, "  \"field_count\": %d,\n", frames);
        fprintf(rf, "  \"video_mode_width\": %d,\n", w);
        fprintf(rf, "  \"video_mode_height\": %d,\n", h);
        fprintf(rf, "  \"first_live_field\": %d,\n", firstLiveFrame);
        fprintf(rf, "  \"last_live_field\": %d,\n", lastLiveFrame);
        fprintf(rf, "  \"worst_black_streak\": %d,\n", worstLiveStreak);
        fprintf(rf, "  \"fields_with_changes\": %ld,\n", changingFields);
        fprintf(rf, "  \"worst_static_streak\": %ld,\n", worstStaticStreak);
        fprintf(rf, "  \"final_gpu_pc\": \"%08X\",\n", GPUGetPC());
        fprintf(rf, "  \"dac_writes\": %u,\n", (unsigned)dacWriteCount);
        fprintf(rf, "  \"cpu_pc\": \"%06X\",\n", m68k_get_reg(NULL, M68K_REG_PC));
        fprintf(rf, "  \"fields\": [\n");
        for (size_t i = 0; i < stats.size(); i++) {
            const FrameStats &s = stats[i];
            fprintf(rf, "    {\"f\":%d,\"nz\":%ld,\"luma\":%d,\"chg\":%ld,\"hash\":\"%016llX\",\"gpupc\":\"%08X\",\"world_changed\":%ld,\"world_lit\":%ld,\"audio_samples\":%u,\"audio_nonzero\":%ld,\"game\":[",
                    s.frame,s.nonzero,s.avgLuma,s.changed,(unsigned long long)s.hash,s.gpuPC,s.worldChanged,s.worldLit,s.audioSamples,s.audioNonzero);
            for(int j=0;j<20;j++)fprintf(rf,"%d%s",(int32_t)s.game[j],j==19?"":",");
            fprintf(rf,"]}%s\n",i+1<stats.size()?",":"");
        }
        fprintf(rf, "  ]\n}\n");
        fclose(rf);
        printf("vjrun: report = %s\n", path);
    }

    // ---- verdict -----------------------------------------------------------
    int rc = 0;
    bool nativeSeen = false;
    int badWorld = 0, stalled = 0;
    uint32_t lastUpdate = 0;
    for(const auto &s : stats) {
        if(s.frame < 120) { if(s.game[0]==0x48455847) nativeSeen=true; continue; }
        if(s.game[0] != 0x48455847) { rc=1; continue; }
        badWorld = s.worldLit < 1500 ? badWorld+1 : 0;
        stalled = s.game[1] == lastUpdate ? stalled+1 : 0;
        lastUpdate = s.game[1];
        if(badWorld > 45 || stalled > 90) rc=1;
    }
    if(!nativeSeen) rc=1;
    if(rc) printf("vjrun: FAIL - native-entry/world/heartbeat watchdog\n");
    if (firstLiveFrame < 0) {
        printf("vjrun: FAIL - the emulated console never showed a picture (black screen)\n");
        rc = 1;
    } else {
        if (worstLiveStreak > liveLimit) {
            printf("vjrun: FAIL - picture went black for %d fields in a row (limit %d)\n", worstLiveStreak, liveLimit);
            rc = 1;
        }
        if (changingFields < frames / 10) {
            printf("vjrun: FAIL - picture is static: only %ld/%d fields changed\n", changingFields, frames);
            rc = 1;
        }
        if (rc == 0)
            printf("vjrun: PASS - first live field %d, %ld/%d fields animated, worst black streak %d\n",
                   firstLiveFrame, changingFields, frames, worstLiveStreak);
    }

    FILE *ram = fopen((outDir + "/ram.bin").c_str(), "wb");
    if(ram){fwrite(jaguarMainRAM,1,0x200000,ram);fclose(ram);}
    JaguarDone();
    return rc;
}
