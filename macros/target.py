from sardana.macroserver.macro import Macro, macro, imacro, Type
from tango import DeviceProxy, DevState
from time import sleep

@macro()
def tape_on(self):
    """Macro tape_on"""
    self.output("Running tape_on...")
    proxy = DeviceProxy('xpl/debristape/rsxs')
    proxy.start_all()
    sleep(0.5)
    self.output("Tape is ON!")


@macro()
def tape_off(self):
    """Macro tape_off"""
    self.output("Running tape_off...")
    proxy = DeviceProxy('xpl/debristape/rsxs')
    proxy.stop_all()
    self.output("Tape is OFF!")


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



@imacro()
def tape_check(self):
    """Macro tape_check"""
    proxy = DeviceProxy('xpl/debristape/rsxs')
    if proxy.State() == DevState.MOVING:
        # all fine
        pass
    else:
        # debris tape is not moving
        self.output('Debris tape is NOT moving!')
        answer = ''
        while answer not in ['y', 'n']:
            answer = self.input("Start debris tape (y)?")

        if answer == 'n':
            self.output('ct without running tape!')
        else:
            proxy.start_all()
            sleep(0.5)
            self.output("Tape is ON!")

