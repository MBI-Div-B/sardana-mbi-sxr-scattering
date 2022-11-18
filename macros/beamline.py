from sardana.macroserver.macro import Macro, macro, imacro, Type
import tango
from time import sleep


@macro()
def fix(self):
    self.execMacro('laser_ready_mode')
    self.execMacro('tape_off')
    self.execMacro('target_off')

@macro()
def pressure_check(self):
    try:
        pressure_scattering = tango.DeviceProxy('rsxs/TPG26X/scattering').pressure
    except:
        pressure_scattering = 9999.0
    try:
        pressure_rzp = tango.DeviceProxy('rsxs/TPG26X/rzp').pressure
    except:
        pressure_rzp = 9999.0
    try:
        pressure_xpl = tango.DeviceProxy('xpl/TPG26X/target').pressure
    except:
        pressure_xpl = 9999.0

    p_tar = 2.0e-5  # ideally 2e-5
    p_rzp = 9.0e-5  # ideally 8e-6
    p_sca = 9.1e-6  # ideally 4e-6

    self.output('Target <%0.1e?'%p_tar)
    self.output(pressure_xpl)
    self.output(pressure_xpl<p_tar)
    self.output('==========')

    self.output('RZP <%0.1e?'%p_rzp)
    self.output(pressure_rzp)
    self.output(pressure_rzp<p_rzp)
    self.output('==========')

    self.output('Scattering <%0.1e?'%p_sca)
    self.output(pressure_scattering)
    self.output(pressure_scattering<p_sca)

    if pressure_xpl<p_tar and pressure_xpl<p_tar and pressure_rzp<p_rzp:
        return True
    else:
        return False

@imacro()
def start_of_the_day(self):
    self.output("Running start_of_the_day in 5s:")
    for i in range(5):
        self.output((i+1)*'.')
        sleep(1)

    self.execMacro('laser_sleep_mode')

    pressures_low_enough = self.execMacro('pressure_check').getResult()

    self.execMacro('acqconf',1,1,1,1,1,1,1,1,0)

    if pressures_low_enough:
        self.output('The pressures are low enough. Are all valves open?')
        answer = ''
        while answer not in ['y', 'n']:
            answer = self.input("Cool the camera to -40°C ?")
        if answer == 'n':
            self.output('Not cooling camera.')
        else:
            answer = ''
            while answer not in ['y', 'n']:
                answer = self.input("Is the camera software running?")
            if answer == 'n':
                self.output('Not cooling camera.')
            else:
                self.output('Cooling camera.')
                self.execMacro('mte_temp_set',-40)
    else:
        self.output('The pressures are NOT low enough! Fix them and then you can cool the camera automatically!')
        
    answer = ''
    while answer not in ['y', 'n']:
        answer = self.input("Setting laser to ready mode?")
    if answer == 'n':
        self.output('Open the valves.')
    else:
        self.execMacro('laser_ready_mode')



#    self.execMacro('magnet_off')
#    self.execMacro('umv', 'cryo_temp', 300)



@macro()
def end_of_the_day(self):
    self.output("Running end_of_the_day in 5s:")

    for i in range(5):
        self.output((i+1)*'.')
        sleep(1)
    self.execMacro('umv', 'mag_curr', '0')
    self.execMacro('laser_sleep_mode')        
    self.execMacro('shutter_disable')
    self.execMacro('shutter_manual')
    self.execMacro('shutter_disable')
#    self.execMacro('umv', 'laser_power', 2)


    self.execMacro('laser_off')

    self.execMacro('tape_off')
    self.execMacro('target_off')

    self.execMacro('mte_temp_set',19)
    self.output("Turn off the camera software please!")
    for i in range(5):
        self.output((i+1)*'.')
        sleep(1)

    self.output("You CAN turn off the controller now.")


#    self.output(pressure_xpl)
#    self.output(pressure_rzp)
#    self.output(pressure_scattering)

#    self.execMacro('magnet_off')
#    self.execMacro('umv', 'cryo_temp', 300)

