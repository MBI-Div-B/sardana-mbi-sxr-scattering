from sardana.macroserver.macro import Macro, macro, Type


@macro(
    [
        ["tth_pos", Type.Float, None, "two_theta position"],
        ["th_pos", Type.Float, None, "theta position"],
    ]
)
def an(self, tth_pos, th_pos):
    """moving tth and th at the same time"""
    self.execMacro(["mv", [["tth", tth_pos], ["th", th_pos]]])


@macro(
    [
        ["tth_pos", Type.Float, None, "two_theta position"],
        ["th_pos", Type.Float, None, "theta position"],
    ]
)
def uan(self, tth_pos, th_pos):
    """update moving tth and th at the same time"""
    self.execMacro(["umv", [["tth", tth_pos], ["th", th_pos]]])
