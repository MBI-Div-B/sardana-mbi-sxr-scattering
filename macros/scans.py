from sardana.macroserver.macro import Macro, macro, Type


@macro([["integ_time", Type.Float, 1, "integration time in [s]"]])
def acquire(self, integ_time):
    """Macro acquire"""
    self.execMacro('timescan', '0', '{:0.3f}'.format(integ_time), '10', '0.2')



