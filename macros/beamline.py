from sardana.macroserver.macro import Macro, macro, imacro, Type

from time import sleep

@imacro()
def start_of_the_day(self):
    self.output("Running start_of_the_day in 5s:")
    for i in range(5):
        self.output((i+1)*'.')
        sleep(1)

    self.execMacro('laser_sleep_mode')
#    self.execMacro('umv', 'laser_power', 2)

    self.execMacro('target_on')

    answer = ''
    while answer not in ['y', 'n']:
        answer = self.input("Is the pressure in the scattering chamber below 1e-4 mbar?")
    if answer == 'n':
        self.output('Not cooling camera.')
    else:
        answer = ''
        while answer not in ['y', 'n']:
            answer = self.input("Is the camera controller on?")
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




#    self.output(pressure_xpl)
#    self.output(pressure_rzp)
#    self.output(pressure_scattering)

#    self.execMacro('magnet_off')
#    self.execMacro('umv', 'cryo_temp', 300)



@macro()
def end_of_the_day(self):
    self.output("Running end_of_the_day in 5s:")

    for i in range(5):
        self.output((i+1)*'.')
        sleep(1)

    self.execMacro('laser_sleep_mode')        
    self.execMacro('shutter_disable')
    self.execMacro('shutter_manual')
    self.execMacro('shutter_disable')
#    self.execMacro('umv', 'laser_power', 2)


    self.execMacro('laser_off')
    self.execMacro('pump_off')

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

