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
    if proxy.speed > 100:
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
    self.output("Running target_on...")
    self.execMacro('umv target_rot 200')


@macro()
def target_off(self):
    """Macro target_off"""
    self.output("Running target_off...")
    self.execMacro('umv target_rot 0')


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

