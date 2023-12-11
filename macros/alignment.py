from sardana.macroserver.macro import Macro, macro, Type


@macro()
def slit_out_completely(self):
    """Macro slit_out"""
    self.output("Moving slit out horizontally towards door...")
    self.execMacro("umv", "slit_y", "41.3")


@macro()
def slit_out(self):
    """Macro slit_out"""
    self.output("Moving slit out horizontally towards door...")
    self.execMacro("umv", "slit_y", "26")


@macro()
def slit_in(self):
    """Macro slit_out"""
    self.output("Moving slit in horizontally towards window...")
    self.execMacro("umv", "slit_y", "6")


@macro()
def go_to_pump_diode(self):
    """Macro to move to pump diode"""
    self.output("You are here:")
    self.execMacro(
        "wa",
    )
    self.output("Going tth to -44 and ccd height down ")
    self.execMacro("umv", "tth", "-44")
    self.execMacro("umv", "ccd_height", "-25.3")


@macro()
def go_to_pinhole(self):
    """Macro go_to_pinhole"""
    self.output("You are here:")
    self.execMacro(
        "wa",
    )
    self.output("Going to pinhole...")
    self.execMacro("umv", "zs", "-10")
    self.execMacro("umv", "th", "90")
