from sardana.macroserver.macro import Macro, macro, Type
from tango import DeviceProxy
from time import sleep

@macro()
def tape_start(self):
    """Macro tape_start"""
    self.output("Running tape_start...")
    proxy = DeviceProxy('xpl/debristape/rsxs')
    proxy.start_all()
    sleep(0.5)
    self.output("Tape started!")


@macro()
def tape_stop(self):
    """Macro tape_stop"""
    self.output("Running tape_stop...")
    proxy = DeviceProxy('xpl/debristape/rsxs')
    proxy.stop_all()
    self.output("Tape stopped!")


@macro()
def tape_test(self):
    """Macro tape_test"""
    self.output("Running tape_test...")
    proxy = DeviceProxy('xpl/debristape/rsxs')
    proxy.start_all()
    self.output("Tape started!")
    sleep(3)
    proxy.stop_all()
    self.output("Tape stopped!")


