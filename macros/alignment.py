from sardana.macroserver.macro import Macro, macro, Type

@macro()
def slit_out_completely(self):
    """Macro slit_out"""
    self.output("Moving slit out horizontally towards door...")
    self.execMacro('umv', 'slit_hor', '41.3')

@macro()
def slit_out(self):
    """Macro slit_out"""
    self.output("Moving slit out horizontally towards door...")
    self.execMacro('umv', 'slit_hor', '26')

@macro()
def slit_in(self):
    """Macro slit_out"""
    self.output("Moving slit in horizontally towards window...")
    self.execMacro('umv', 'slit_hor', '6')


@macro()
def ccd_out(self):
    """Macro ccd_out"""
    self.output("Moving ccd out horizontally towards door and down...")
    self.execMacro('umv', 'ccd_height', '-25', 'tth', '-25')
    #

@macro()
def ccd_in(self):
    """Macro ccd_out"""
    self.output("Moving ccd in horizontally towards window and up...")
    self.execMacro('umv', 'ccd_height', '0', 'tth', '-0')
    
    #device = self.getDevice("controller/pilccountertimercontroller/pilctimerctrl")
    #print(device.getTriggerMode())


@macro()
def pol_out(self):
    """Macro pol_out"""
    self.output("Moving polariser out horizontally towards door...")
    self.execMacro('umv', 'slit_hor', '25')

@macro()
def pol_in(self):
    """Macro pol_out"""
    self.output("Moving polariser in horizontally towards window...")
    self.execMacro('umv', 'slit_hor', '6.15')




@macro()
def go_to_pump_diode(self):
    """Macro to move to pump diode"""
    self.output("You are here:")
    self.execMacro('wa',)
    self.output("Going tth to -44 and ccd height down ")
    self.execMacro('umv', 'tth', '-44')
    self.execMacro('umv', 'ccd_height', '-25.3')



@macro()
def go_to_pinhole(self):
    """Macro go_to_pinhole"""
    self.output("You are here:")
    self.execMacro('wa',)
    self.output("Going to pinhole...")
    self.execMacro('umv', 'zs', '-10')
    self.execMacro('umv', 'th', '90')




