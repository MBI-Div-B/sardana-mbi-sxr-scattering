from sardana.macroserver.macro import Macro, macro, Type
import time


@macro()
def where_is_gap(self):
    self.output(self.execmacro("wu gap02"))


@macro()
def test_counter_value(self):
    pilc = self.getController("PiLCTimerCtrl")
    pilc.write_attribute("triggermode", 1)
    self.output(pilc.read_attribute("triggermode").value)
