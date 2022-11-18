from sardana.macroserver.macro import Macro, macro, Type


@macro()
def where_is_gap(self):
    self.output(self.execmacro("wu gap02"))


@macro()
def test_counter_value(self):
    self.output(
        "don't forget to switch\nLaVue Tango Events -> Attributes to rsxs moench"
    )