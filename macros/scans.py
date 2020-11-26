from sardana.macroserver.macro import Macro, macro, Type


@macro([["integ_time", Type.Float, 1, "integration time in [s]"]])
def acquire(self, integ_time):
    """Macro acquire"""
    self.execMacro('timescan', '0', '{:0.3f}'.format(integ_time), '10', '0.2')


@macro([
    ['motor', Type.Moveable, None, 'Moveable to move'],
    ['start_pos', Type.Float, None, 'Scan start position'],
    ['final_pos', Type.Float, None, 'Scan final position'],
    ['nr_interv', Type.Integer, None, 'Number of scan intervals'],
    ['integ_time', Type.Float, None, 'Integration time']
])
def lup(self, motor, start_pos, final_pos, nr_interv, integ_time):
    """motor scan relative to the starting position.
    lup scans one motor, as specified by motor. If motor motor is at a
    position X before the scan begins, it will be scanned from X+start_pos
    to X+final_pos. The step size is (start_pos-final_pos)/nr_interv.
    The number of data points collected will be nr_interv+1. Count time is
    given by time which if positive, specifies seconds and if negative,
    specifies monitor counts. """
    self.execMacro(['dscan', motor, start_pos, final_pos, nr_interv, integ_time])


