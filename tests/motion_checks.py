"""Independent numerical checks of native camera/bank state and renderer inputs.
All end-to-end inputs enter through the normal controller; RAM is read-only.
"""
import math


def smooth(old,target,alpha):
    step=((target-old)*alpha+128)//256
    if step==0 and target!=old:step=1 if target>old else -1
    return old+step


def committed(result):
    last=None
    for f in result['fields'][150:]:
        seq=f['motion'][16]
        if 'view' in f and f['view'][12]!=seq:continue
        if seq and seq!=last:
            yield f
            last=seq


def verify_motion(result):
    previous=None;updates=0;height_filtered=0;left=False;right=False
    for f in committed(result):
        g,m,p=f['game'],f['motion'],f['pose']
        assert abs(m[0])<=332*256,'Unbounded ship bank'
        assert 0<=m[1]<=40*256,'Unbounded camera pullback'
        assert m[11]==160+(m[1]>>8),'Camera distance ignores filtered speed offset'
        assert p[0]==p[3]==((f.get('physics',[0]*32)[6]>>8)&2044),'Ship/booster ignored native terrain pitch'
        assert p[1]==p[4]==(-g[7])&2044,'Object yaw does not follow native heading'
        bank=f.get('handling',[0]*32)[16] if 'handling' in f else m[0]
        angle=(bank>>8)&2044
        assert p[2]==p[5]==angle,'Ship/booster renderer roll differs from filter state'
        assert (m[15]>>16)&0xffff==angle and m[15]&0xffff==angle
        assert p[6:9]==m[12:15] and p[9]==f.get('view',[0]*4+[g[7]])[4],'Renderer camera differs from computed pose'
        view=f.get('view',[0]*32)
        if g[2]!=5:
            heading=p[9]*2*math.pi/2048
            distance=view[14] if view[1] else m[11]
            assert abs(m[12]-((g[4]>>8)+math.sin(heading)*distance))<=2,'Camera X offset is wrong'
            assert abs(m[14]-((g[6]>>8)-math.cos(heading)*distance))<=2,'Camera Z offset is wrong'
            expected_y=(g[5]>>8)+(80 if view[1]==1 else 48) if view[1] else m[2]>>8
            assert m[13]==expected_y,'Renderer ignored smoothed/view height'
        if g[2] in (0,4):
            assert m[0]==m[1]==0,'Bank/camera drift during ready/countdown'
        if previous and m[16]==previous['motion'][16]+1:
            pm=previous['motion']
            if g[2]==1 and not g[13]:
                dt=m[7];h=g[20]
                coefficients=[round(256*(1-(1-rate)**(dt*60/h))) for rate in (.08,.30,.15)]
                assert m[8:11]==coefficients,'Wrong PAL/NTSC response coefficients'
                assert m[0]==smooth(pm[0],m[4],m[8]),('Bank filter mismatch',f['f'],pm,m)
                assert m[1]==smooth(pm[1],m[5],m[9]),'Speed-sensitive camera filter mismatch'
                expected=max(g[5]+24*256,min(g[5]+80*256,smooth(pm[2],m[6],m[10])))
                assert m[2]==expected,('Height filter/clamp mismatch',f['f'])
                assert m[5]==g[8]*40*256//28,'Pullback target is not proportional to speed'
                assert m[6]==g[5]+64*256,'Height target is wrong'
                assert g[5]+24*256<=m[2]<=g[5]+80*256,'Camera crossed height safety envelope'
                if m[2]!=m[6]:height_filtered+=1
                left|=m[0]<-1024;right|=m[0]>1024
                updates+=1
            else:
                assert m[:11]==pm[:11],'Motion filters advanced while paused/inactive'
        previous=f
    assert updates>0,'No active motion updates observed'
    return {'verified_updates':updates,'height_filtered_updates':height_filtered,'left_bank_seen':left,'right_bank_seen':right}


def bank_script(h):
    t=100+8*h
    events=[(100,'a'),(120,'none'),(t,'left'),(t+h,'none'),(t+2*h,'right'),(t+3*h,'none'),(t+4*h,'left+b'),(t+5*h,'none'),(t+6*h,'right+b'),(t+7*h,'pause'),(t+7*h+10,'none'),(t+8*h,'pause'),(t+8*h+10,'none'),(t+9*h,'option'),(t+9*h+10,'none')]
    return ','.join(f'{f}:{keys}' for f,keys in events),t+10*h,t


def bank_case(result,t,h):
    evidence=verify_motion(result);s=result['fields']
    def roll_at(n):return s[n]['motion'][0]
    assert roll_at(t+h-8)<-190*256,'Left bank did not reach its target'
    assert roll_at(t+3*h-8)>190*256,'Right bank did not reach its target'
    assert roll_at(t+5*h-8)<-325*256,'Left airbrake did not increase bank'
    assert roll_at(t+7*h-8)>325*256,'Right airbrake did not increase bank'
    for n in [t+2*h-8,t+4*h-8,t+6*h-8]:assert abs(roll_at(n))<2048,'Ship did not return to within 1.5 degrees of level'
    w=s[t+7*h+20:t+8*h-10]
    assert w and all(f['game'][13]==1 for f in w)
    assert len({tuple(f['motion'][:16]) for f in w})==1,'Bank or camera drifted during pause'
    assert len({tuple(f['pose']) for f in w})==1,'Rendered pose changed during pause'
    reset=s[t+9*h+20]
    assert reset['game'][2]==0 and reset['motion'][:2]==[0,0],'Restart retained motion state'
    assert reset['motion'][2]==reset['game'][5]+64*256,'Restart left camera at previous height'
    live=s[t:t+7*h]
    assert all(f['game'][8]==0 and f['game'][9]==100 for f in live),'Steering-only test unexpectedly moved/crashed'
    assert evidence['left_bank_seen'] and evidence['right_bank_seen']
    evidence['half_second_left_roll_q8']=roll_at(t+h//2)
    evidence['checks']=['left/right bank','airbrake bank','return to level','pause freezes renderer pose','restart clears filters','actual ship and booster angles','fixed-point recurrence','PAL/NTSC coefficients']
    evidence['fields']=len(s)
    return evidence


def speed_script(h):
    go=100+7*h
    return f'100:a,120:none,{go+h}:a,{go+2*h}:b,{go+3*h}:none',go+5*h,go


def speed_case(result,go,h):
    evidence=verify_motion(result);s=result['fields']
    acceleration=s[go+h:go+2*h]
    assert max(f['motion'][11] for f in acceleration)>=198,'Chase camera did not pull back at speed'
    # Test the actual Q8 filter, not integer rounding of its displayed distance.
    assert len({f['motion'][1] for f in acceleration})>10,'Pullback snapped instead of filtering'
    assert max(f['game'][8] for f in acceleration)==28,'Speed target was not exercised'
    assert s[-1]['game'][8]==0 and s[-1]['motion'][11]==160,'Camera failed to return after braking'
    assert sum(f['world_changed']>100 for f in acceleration)>8,'Speed-camera test has no visible world animation'
    evidence['checks']=['speed-dependent pullback','smooth camera distance','return after braking','rendered camera position','fixed-point recurrence']
    evidence['fields']=len(s)
    return evidence
