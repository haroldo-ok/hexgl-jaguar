SHELL := /bin/bash
ROOT := $(CURDIR)
BJL_ROOT := $(ROOT)/vendor/new_bjl
LYXASS := $(ROOT)/vendor/lyxass/lyxass
VJ := $(ROOT)/vendor/virtualjaguar
PYTHON ?= python3
export BJL_ROOT
.PHONY: all rom assets toolchain emulator test test-core test-gui test-unit test-quick test-clean release verify clean
all: rom

toolchain:
	$(MAKE) -C vendor/lyxass

# Every asset comes from the pinned original repositories, no generated substitute meshes.
assets:
	$(PYTHON) tools/sky.py
	$(PYTHON) tools/audio.py
	$(PYTHON) tools/route.py
	$(PYTHON) tools/replay.py

rom: toolchain
	@test -f assets/models.inc || { echo 'Run make assets first'; exit 1; }
	$(PYTHON) tools/frontend.py
	$(PYTHON) tools/hud.py
	$(PYTHON) tools/motion.py
	$(PYTHON) tools/dynamics.py
	$(PYTHON) tools/effects.py
	$(PYTHON) tools/prepare_engine.py
	cd src && $(LYXASS) -d -o audio.bin audio.js
	cd src && $(LYXASS) -sh hexgl.js
	m68k-linux-gnu-as -m68000 src/cart_boot.S -o src/cart_boot.o
	m68k-linux-gnu-ld -Ttext=0x900000 --oformat=binary src/cart_boot.o -o src/cart_boot.bin
	$(PYTHON) tools/package_rom.py
	$(PYTHON) tools/verify.py

emulator:
	$(PYTHON) tests/vjrunner/instrument_vj.py "$(VJ)"
	$(MAKE) -C "$(VJ)" -f jaguarcore.mak SDL_CFLAGS="$$(pkg-config --cflags sdl2)" QT_CFLAGS="-fPIC $$(pkg-config --cflags Qt5Widgets)" CXXFLAGS="-O2 -w -std=c++11"
	$(MAKE) -C "$(VJ)/src/m68000" CROSS= CFLAGS="-O2 -std=gnu89 -w -fomit-frame-pointer" INCS="-I. -I./obj"
	$(MAKE) -C tests/vjrunner VJ="$(VJ)"

# Release gate: compile current source, test assertions, real core, and stock GUI.
test: rom emulator test-unit
	$(PYTHON) tests/e2e.py
	$(PYTHON) tests/hud_e2e.py
	$(PYTHON) tests/dynamics_e2e.py
	$(PYTHON) tests/frontend_e2e.py
	$(PYTHON) tools/check_recorded_dynamics.py
	xvfb-run -a -s '-screen 0 1024x768x24' $(PYTHON) tests/gui_e2e.py

test-core: rom emulator
	$(PYTHON) tests/e2e.py
	$(PYTHON) tests/hud_e2e.py
	$(PYTHON) tests/dynamics_e2e.py
	$(PYTHON) tests/frontend_e2e.py
	$(PYTHON) tools/check_recorded_dynamics.py

test-gui: rom
	xvfb-run -a -s '-screen 0 1024x768x24' $(PYTHON) tests/gui_e2e.py

test-unit:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py' -v

test-clean: rom
	$(PYTHON) tools/clean_rebuild.py

release: test test-clean
	$(PYTHON) tools/black_screen_report.py
	$(PYTHON) tools/bundle.py

test-quick: rom emulator test-unit
	$(PYTHON) tests/e2e.py --quick

verify:
	$(PYTHON) tools/verify.py

clean:
	rm -f src/hexgl.o src/hexgl.equ src/audio.bin rom/hexgl.j64
