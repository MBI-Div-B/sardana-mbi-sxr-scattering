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


@imacro()
def target_check(self):
    """Macro target_check"""
    proxy = DeviceProxy('xpl/faulhaberdcmotor/rsxs')
    if proxy.speed > 50:
        # all fine
        pass
    else:
        # target is not rotating
        self.output('Target is NOT rotating!')
        answer = ''
        while answer not in ['y', 'n']:
            answer = self.input("Start target (y)?")

        if answer == 'n':
            self.output('ct without rotating target!')
        else:
            self.execMacro('target_on')
            sleep(0.5)
            self.output("Target is ON!")


@macro()
def target_on(self):
    """Macro target_on"""
    proxy = DeviceProxy('xpl/target/rotation')
    proxy.jog_plus()
    self.output("Running target_on...")


@macro()
def target_off(self):
    """Macro target_off"""
    proxy = DeviceProxy('xpl/target/rotation')
    proxy.stop()
    self.output("Running target_off...")


@macro()
def watchdog_on(self):
    """Macro watchdog_on"""
    self.output("Running watchdog_on...")
    proxy = DeviceProxy('rsxs/watchdog/1')
    proxy.run()


@macro()
def watchdog_off(self):
    """Macro watchdog_off"""
    self.output("Running watchdog_off...")
    proxy = DeviceProxy('rsxs/watchdog/1')
    proxy.stop()


@macro()
def new_line(self):
    """Macro to translate the target to a new line."""
    self.execMacro('umvr','target_trans','0.1')

