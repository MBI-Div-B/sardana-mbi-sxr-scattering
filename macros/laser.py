from sardana.macroserver.macro import Macro, macro, Type
from tango import DeviceProxy

@macro()
def laser_on(self):
    """Macro laser_on"""
    proxy = DeviceProxy('laser/ThorlabsShutter/0')
    proxy.Open()
    self.output("Laser shutter open!")


@macro()
def laser_off(self):
    """Macro laser_off"""
    proxy = DeviceProxy('laser/ThorlabsShutter/0')
    proxy.Close()
    self.output("Laser shutter closed!")

