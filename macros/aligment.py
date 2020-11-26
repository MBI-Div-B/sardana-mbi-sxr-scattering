from sardana.macroserver.macro import Macro, macro, Type

@macro()
def slit_out(self):
    """Macro slit_out"""
    self.output("Moving slit out horizontally towards door...")
    self.execMacro('umv', 'slit_hor', '41')

@macro()
def slit_in(self):
    """Macro slit_out"""
    self.output("Moving slit in horizontally towards window...")
    self.execMacro('umv', 'slit_hor', '8')



@macro()
def go_to_pinhole(self):
    """Macro go_to_pinhole"""
    self.output("You are here:")
    self.execMacro('wa',)
    self.output("Going to pinhole...")
    self.execMacro('umv', 'zs', '-10')
    self.execMacro('umv', 'th', '90')



