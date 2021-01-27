from sardana.macroserver.macro import Macro, macro, Type
from time import sleep

@macro()
def user_pre_acq(self):
    """Macro user_pre_acq"""

    acqConf  = self.getEnv('acqConf')
    try:
        waittime = acqConf['waitTime']
    except:
        self.warning('env variable acqConf/waitTime not found!')
        waittime = 0

    try:
        check_tape = acqConf['checkTape']
    except:
        self.warning('env variable acqConf/checkTape not found!')
        check_tape = False

    try:
        check_target = acqConf['checkTarget']
    except:
        self.warning('env variable acqConf/checkTarget not found!')
        check_target = False

    try:
        check_cam_temp = acqConf['checkCamTemp']
    except:
        self.warning('env variable acqConf/checkCamTemp not found!')
        check_cam_temp = False

    if check_tape:
        self.execMacro('tape_check')
    
    if check_target:
        self.execMacro('target_check')

    if check_cam_temp:
        self.execMacro('mte_check')

    if waittime > 0:
        sleep(waittime)
        self.debug('waiting for %.2f s', waittime)


@macro()
def user_pre_scan(self):
    """Macro user_pre_scan"""
    acqConf  = self.getEnv('acqConf')    

    try:
        start_tape = acqConf['startTape']
    except:
        self.warning('env variable acqConf/startTape not found!')

    if start_tape:
        self.execMacro('tape_on')

    try:
        auto_mode_laser = acqConf['autoModeLaser']
    except:
        self.warning('env variable acqConf/autoModeLaser not found!')
        
    if auto_mode_laser:
        self.execMacro('laser_scan_mode')

    self.execMacro('acqrep')

@macro()
def dark_image_prep(self):
    """Macro to prepare for dark image"""

    self.execMacro('laser_sleep_mode')
    self.execMacro('shutter_disable')
    self.execMacro('shutter_external')
    self.execMacro('probe_off')
    self.execMacro('laser_on')
    sleep(0.4)
    self.execMacro('shutter_enable')
    self.execMacro('tape_on')


@macro()
def user_post_scan(self):
    """Macro user_pre_scan"""

    acqConf  = self.getEnv('acqConf')
    shutter_states  = self.getEnv('shutter_states')

    try:
        stop_tape = acqConf['stopTape']
    except:
        self.warning('env variable acqConf/stopTape not found!')
        stop_tape = False

    if stop_tape:
        self.execMacro('tape_off')

    try:
        auto_mode_laser = acqConf['autoModeLaser']
    except:
        self.warning('env variable acqConf/autoModeLaser not found!')
        
    if auto_mode_laser:
        self.execMacro('laser_ready_mode')



@macro()
def user_pre_move(self):
    """Macro user_pre_move"""

    acqConf  = self.getEnv('acqConf')

    try:
        auto_shutter_pump = acqConf['autoShutterPump']
    except:
        self.warning('env variable acqConf/autoShutterPump not found!')
        auto_shutter_pump = False

    if auto_shutter_pump:
        self.execMacro('pump_off')

    #parent = self.getParentMacro()
    #if parent:
    #    self.output(parent._name)


@macro()
def user_post_move(self):
    """Macro user_post_move"""

    #self.info('In user post move')

    acqConf  = self.getEnv('acqConf')

    try:
        auto_shutter_pump = acqConf['autoShutterPump']
    except:
        self.warning('env variable acqConf/autoShutterPump not found!')
        auto_shutter_pump = False

    if auto_shutter_pump:
        self.execMacro('pump_on')



