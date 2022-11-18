from sardana.macroserver.macro import Macro, macro, Type

macro()
def where_is_gap(self):
    self.output(self.execmacro('wu gap02'))