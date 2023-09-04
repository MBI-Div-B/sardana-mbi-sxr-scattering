from PyTango import DeviceProxy
import time
from sardana import State, DataAccess
from sardana.pool.controller import Type, Access, Description
from sardana.pool.controller import CounterTimerController


class KeithleyDMM7510CounterTimerController(CounterTimerController):
    """The most basic controller intended from demonstration purposes only.
    This is the absolute minimum you have to implement to set a proper counter
    controller able to get a counter value, get a counter state and do an
    acquisition.

    This example is so basic that it is not even directly described in the
    documentation"""

    MaxDevice = 99

    axis_attributes = {
        "Tango_Device": {
            Type: str,
            Description: "The Tango Device" " (e.g. domain/family/member)",
            Access: DataAccess.ReadWrite,
        },
    }

    def __init__(self, inst, props, *args, **kwargs):
        """Constructor"""
        CounterTimerController.__init__(self, inst, props, *args, **kwargs)
        self._log.info("Initialized")
        self.axis_extra_pars = {}

    def AddDevice(self, axis):
        self._log.info("adding axis {:d}".format(axis))
        self.axis_extra_pars[axis] = {}
        self.axis_extra_pars[axis]["Proxy"] = None

    def DeleteDevice(self, axis):
        pass

    def ReadOne(self, axis):
        """Get the specified counter value"""
        return float(self.axis_extra_pars[axis]["Proxy"].stats_average)

    def StateOne(self, axis):
        status = self.axis_extra_pars[axis]["Proxy"].trigger_status
        if (status == "IDLE") or (status == "EMPTY") or (status == "BUILDING"):
            return State.On, "Counter is stopped"
        elif (status == "RUNNING") or (status == "WAITING"):
            return State.Moving, "Counter is running"
        else:
            return State.Fault, "Something is wrong"

    def StartOne(self, axis, value=None):
        """acquire the specified counter"""
        pass

    def PrepareOne(self, axis, value, repetitions, latency_time, nb_starts):
        self.axis_extra_pars[axis]["Proxy"].trigger_external(int(value * 100))

    def LoadOne(self, axis, value, repetitions, latency_time):
        self.axis_extra_pars[axis]["Proxy"].trigger_init()

    def StopOne(self, axis):
        """Stop the specified counter"""
        self.axis_extra_pars[axis]["Proxy"].trigger_abort()

    def AbortOne(self, axis):
        """Stop the specified counter"""
        self.axis_extra_pars[axis]["Proxy"].trigger_abort()

    def GetAxisExtraPar(self, axis, name):
        return self.axis_extra_pars[axis][name]

    def SetAxisExtraPar(self, axis, name, value):
        if name == "Tango_Device":
            self.axis_extra_pars[axis][name] = value
            try:
                self.axis_extra_pars[axis]["Proxy"] = DeviceProxy(value)
                self._log.info("axis {:d} DeviceProxy set to: {:s}".format(axis, value))
            except Exception as e:
                self.axis_extra_pars[axis]["Proxy"] = None
                raise e
