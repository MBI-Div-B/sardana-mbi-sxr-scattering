from sardana.macroserver.macro import Macro, macro, imacro, Type
import tango
from time import sleep
import subprocess


@macro()
def fix(self):
    self.execMacro("tape_off")
    self.execMacro("target_off")
    self.execMacro("laser_ready_mode")



@macro()
def pressure_check(self):
    try:
        pressure_scattering = tango.DeviceProxy("rsxs/TPG261/scattering").pressure
    except:
        pressure_scattering = 9999.0
    try:
        pressure_rzp = tango.DeviceProxy("rsxs/TPG261/rzp").pressure
    except:
        pressure_rzp = 9999.0
    try:
        pressure_xpl = tango.DeviceProxy("sxr/TPG261/pxs").pressure
    except:
        pressure_xpl = 9999.0

    p_tar = 2.0e-5  # ideally 2e-5
    p_rzp = 9.0e-6  # ideally 9e-6
    p_sca = 4.0e-6  # ideally 4e-6

    self.output("Target <%0.1e?" % p_tar)
    self.output(pressure_xpl)
    self.output(pressure_xpl < p_tar)
    self.output("==========")

    self.output("RZP <%0.1e?" % p_rzp)
    self.output(pressure_rzp)
    self.output(pressure_rzp < p_rzp)
    self.output("==========")

    self.output("Scattering <%0.1e?" % p_sca)
    self.output(pressure_scattering)
    self.output(pressure_scattering < p_sca)

    if pressure_xpl < p_tar and pressure_xpl < p_tar and pressure_rzp < p_rzp:
        return True
    else:
        return False


@imacro()  # choose detector at the beginning!
def start_of_the_day(self):
    self.output("Running start_of_the_day in 5s:")
    for i in range(5):
        self.output((i + 1) * ".")
        sleep(1)

    self.execMacro("laser_sleep_mode")

    pressures_low_enough = self.execMacro("pressure_check").getResult()
    # how it is done in switch to moench_laser, activvating the probe shutter
    # self.execMacro("acqconf", 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0)
    # was previously, not activating the last probe shutter
    # self.execMacro("acqconf", 1, 1, 1, 1, 1, 1, 1, 1, 0)
    self.execMacro("acqconf", 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0)
    if pressures_low_enough:
        self.output("The pressures are low enough. Are all valves open? [y / n]")
        answer = ""
        while answer not in ["y", "n"]:
            answer = self.input("Cool the camera to -50°C ? [y / n]")
        if answer == "n":
            self.output("Not cooling camera.")
        else:
            answer = ""
            while answer not in ["y", "n"]:
                answer = self.input("Is the camera software running? [y / n]")
            if answer == "n":
                self.output("Not cooling camera.")
            else:
                self.output("Cooling camera.")
                self.execMacro("ccd_temp_set", -50)
    else:
        self.output(
            "The pressures are NOT low enough! Fix them and then you can cool the camera automatically!"
        )

    answer = ""
    while answer not in ["y", "n"]:
        answer = self.input("Setting laser to ready mode? [y / n]")
    if answer == "n":
        self.output("Open the valves.")
    else:
        self.execMacro("laser_ready_mode")


#    self.execMacro('magnet_off')
#    self.execMacro('umv', 'cryo_temp', 300)

@macro()
def sync(self):
    scanDir = self.getEnv("ScanDir")
    self.output("synchronize data to NAS")
    result = subprocess.run(
    f'rsync -r -t -g -v --progress -s {scanDir} data_ampere@nasbsxr.sxr.lab:/share/Data/henry.sxr.lab/RSXS/data',shell = True, stdout=subprocess.PIPE,)
    self.output(result.stdout.decode("utf-8"))

@macro()
def end_of_the_day(self):
    self.output("Running end_of_the_day in 5s:")

    for i in range(5):
        self.output((i + 1) * ".")
        sleep(1)

    self.execMacro("umv", "thindisk_wp", "0")
    self.output('look at the infoscreen and note the laser power now!')
    self.output('resuming in 5s')
    sleep(5)


    self.execMacro("laser_sleep_mode")
    self.execMacro("shutter_disable")
    self.execMacro("shutter_manual")

    self.execMacro("laser_off")
    self.execMacro("tape_off")
    self.execMacro("target_off")

    self.output("UMV OF WAVEPLATE TO 0 POSITION IS DISABLED!!!!!!!")
    self.output("CAUTION! PUMP BEAM MAY BE NOT BLOCKED!!!!!!!")
    self.output("MAKE SURE THAT TANGO DEVICE laser/AgilisAGP/pump POSITION IS 0")
    # self.execMacro("umv","wp","0")

    try:
        self.execMacro("ccd_temp_set", 19)
    except:
        self.warning("Could not contact CCD to heat to 19 degrees C")

    #    self.output(pressure_xpl)
    #    self.output(pressure_rzp)
    #    self.output(pressure_scattering)
    try:
        #        self.execMacro('magnet_off')
        self.execMacro("umv", "mag_curr", "0")
    except:
        self.output("Magnet can not be turned off. CaenFastPS off?")
    try:
        self.execMacro("sync")
    except:
        self.warning("Sync data")
    
    try:
        self.execMacro("start_puzzing_all")
    except:
        self.warning("Could not contact Puzzi properly.")


#    self.execMacro('umv', 'cryo_temp', 300)


def turbo_on(self, name):
    ds = self.getEnv("TangoDevices")
    self.warning('Switching %s turbo on!'%name)
    turbo = tango.DeviceProxy(ds['turbo_%s'%name])
    turbo.turn_on()

def turbo_off(self, name):
    ds = self.getEnv("TangoDevices")
    self.warning('Switching %s turbo off!'%name)
    turbo = tango.DeviceProxy(ds['turbo_%s'%name])
    turbo.turn_off()

@macro()
def turbo_optic_on(self):
    turbo_on(self, 'optic')

@macro()
def turbo_ccd_on(self):
    turbo_on(self, 'ccd')


@macro()
def turbo_optic_off(self):
    turbo_off(self, 'optic')

@macro()
def turbo_ccd_off(self):
    turbo_off(self, 'ccd')
    



@macro()
def switch_to_mte(self):
    self.output("switching to mte ccd detector...")
    # self.output("driving ccd in")
    # self.execMacro("ccd_in")
    self.output("switching measurement group to pilc_mte")
    self.execMacro("set_meas", "pilcmte")
    self.output("switching PiLCTimerCtrl.TriggerMode to 2 (scattering)")
    pilc = self.getController("PiLCTimerCtrl")
    pilc.write_attribute("triggermode", 2)
    self.output(f"triggermode = %d" % pilc.read_attribute("triggermode").value)

    self.output("exporting acqconf to check mte CamTemp")
    # args are boolean: checkTape, checkTarget, checkMTETemp, checkCCDTemp, startTape, stopTape, startTarget, stopTarget, autoModeLaser, darkModeLaser, autoShutterPump, waittime
    self.execMacro("pressure_check")
    self.execMacro("acqconf", 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0)
    self.execMacro("ccd_temp_set", -40)
    self.output("don't forget to switch\nLaVue Tango Events -> Attributes to rsxs mte")


@macro()
def switch_to_lotte(self):
    self.output("switching to greateyes lotte detector...")
    self.output("switching measurement group to lotte_mgmt")
    self.execMacro("set_meas", "lotte_mgmt")
    self.output("switching PiLCTimerCtrl.TriggerMode to 2 (scattering)")
    pilc = self.getController("PiLCTimerCtrl")
    pilc.write_attribute("triggermode", 2)
    self.output(f"triggermode = %d" % pilc.read_attribute("triggermode").value)
    self.output("exporting acqconf to check CamTemp")
    # args are boolean: checkTape, checkTarget, checkMTETemp, checkCCDTemp, startTape, stopTape, startTarget, stopTarget, autoModeLaser, darkModeLaser, autoShutterPump, waittime
    self.execMacro("pressure_check")
    self.execMacro("acqconf", 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0)
    # self.execMacro("ccd_temp_set", -35)
    self.output(
        "don't forget to switch\nLaVue Tango Attribute 'sxr/greateyesccd/lotte/images' "
    )


@macro()
def switch_to_moench_laser(self):
    self.output("switching to moench hybrid detector...")
    self.output("using laser direct as a trigger")
    # self.output("driving ccd out")
    # self.execMacro("ccd_out")
    self.output("switching measurement group to moench_zmq_mgmt")
    self.execMacro("set_meas", "moenchzmq_only")
    # self.execMacro("set_meas", "moench_zmq_mgmt")
    self.output("switching PiLCTimerCtrl.TriggerMode to 1")
    pilc = self.getController("PiLCTimerCtrl")
    pilc.write_attribute("triggermode", 1)
    self.output(f"triggermode = %d" % pilc.read_attribute("triggermode").value)
    # pilc.read_attribute("triggermode").value
    self.output("exporting acqconf to ignore mte CamTemp")
    # args are boolean: checkTape, checkTarget, checkCamTemp, startTape, stopTape, startTarget, stopTarget, autoModeLaser, darkModeLaser, autoShutterPump
    self.execMacro("acqconf", 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0)
    self.output(
        "don't forget to switch\nLaVue Tango Events -> Attributes to rsxs moench"
    )


@macro()
def switch_to_moench_chopper(self):
    self.output("GET TO THE CHOPPER")
    self.output("switching to moench hybrid detector...")
    self.output("using chopper as a trigger")
    # self.output("driving ccd out")
    # self.execMacro("ccd_out")
    self.output("switching measurement group to moench_zmq_mgmt")
    self.execMacro("set_meas", "moench_zmq_mgmt")
    self.output("switching PiLCTimerCtrl.TriggerMode to 4")
    pilc = self.getController("PiLCTimerCtrl")
    pilc.write_attribute("triggermode", 4)
    self.output(f"triggermode = %d" % pilc.read_attribute("triggermode").value)
    # pilc.read_attribute("triggermode").value
    self.output("exporting acqconf to ignore mte CamTemp")
    # args are boolean: checkTape, checkTarget, checkCamTemp, startTape, stopTape, startTarget, stopTarget, autoModeLaser, darkModeLaser, autoShutterPump
    self.execMacro("acqconf", 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0)
    self.output(
        "don't forget to switch\nLaVue Tango Events -> Attributes to rsxs moench"
    )
    self.output("DO NOT FORGET TO SWITCH ON THE CHOPPER")


@macro()
def switch_to_top_diode(self):
    self.output('switching measurement group to "sic diode top only"')
    self.execMacro("set_meas", "sic_diode_top_only")
    self.output("switching PiLCTimerCtrl.TriggerMode to 1")
    pilc = self.getController("PiLCTimerCtrl")
    pilc.write_attribute("triggermode", 1)
    self.output(f"triggermode = %d" % pilc.read_attribute("triggermode").value)
    self.output("exporting acqconf to ignore mte CamTemp")
    # args are boolean: checkTape, checkTarget, checkCamTemp, startTape, stopTape, startTarget, stopTarget, autoModeLaser, darkModeLaser, autoShutterPump
    self.execMacro("acqconf", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    # self.output(
    #   "don't forget to switch\nLaVue Tango Events -> Attributes to rsxs moench"
    # )


@macro()
def switch_to_bottom_diode(self):
    self.output('switching measurement group to "sic diode bottom only"')
    self.execMacro("set_meas", "sic_diode_bottom_only")
    self.output("switching PiLCTimerCtrl.TriggerMode to 1")
    pilc = self.getController("PiLCTimerCtrl")
    pilc.write_attribute("triggermode", 1)
    self.output(f"triggermode = %d" % pilc.read_attribute("triggermode").value)
    self.output("exporting acqconf to ignore mte CamTemp")
    # args are boolean: checkTape, checkTarget, checkCamTemp, startTape, stopTape, startTarget, stopTarget, autoModeLaser, darkModeLaser, autoShutterPump
    self.execMacro("acqconf", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    # self.output(
    #   "don't forget to switch\nLaVue Tango Events -> Attributes to rsxs moench"
    # )


@macro()
def switch_to_IR_diode(self):
    self.output("switching to keithley voltmeter...")
    # self.output("driving ccd out")
    # self.execMacro("ccd_out")
    self.output("switching measurement group to laser_diode_mgmt")
    self.execMacro("set_meas", "laser_diode_mgmt")
    self.output("switching PiLCTimerCtrl.TriggerMode to 1")
    pilc = self.getController("PiLCTimerCtrl")
    pilc.write_attribute("triggermode", 1)
    self.output(f"triggermode = %d" % pilc.read_attribute("triggermode").value)
    self.output("exporting acqconf to ignore mte CamTemp")
    # args are boolean: checkTape, checkTarget, checkCamTemp, startTape, stopTape, startTarget, stopTarget, autoModeLaser, darkModeLaser, autoShutterPump
    self.execMacro("acqconf", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    # self.output(
    #   "don't forget to switch\nLaVue Tango Events -> Attributes to rsxs moench"
    # )


@macro()
def get_moench_file_index(self):
    file_index_number = tango.DeviceProxy("rsxs/moenchControl/bchip286").fileindex
    self.output("The next number will be #%d" % file_index_number)
