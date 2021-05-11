from sardana import State
from sardana.pool.controller import CounterTimerController
from sardana.pool.controller import Type, Description, DefaultValue, Access, DataAccess, Memorized, Memorize

import time
import numpy as np
import pyvisa as visa

class RigolMSOCounterTimerController(CounterTimerController):
    """RigolMSOCounterTimerController

    Use Rigol MSO 5000 Scope

    """
    ctrl_properties = {'resource': {Type: str,
                                     Description: 'visa resource of the MSO',
                                     DefaultValue: 'TCPIP::192.168.1.110::INSTR'},
                       }


    MaxDevice = 1

    def __init__(self, inst, props, *args, **kwargs):
        """Constructor"""
        CounterTimerController.__init__(self, inst, props, *args, **kwargs)
        self._log.info('Rigol MSO Initialization on {:s} ...'.format(self.resource))
        rm = visa.ResourceManager()
        self.mso = rm.open_resource('TCPIP::192.168.1.110::INSTR')
        self._log.info('SUCCESS')
        self.__start_time = time.time()
        self.__integ_time = 0

    def AddDevice(self, axis):
        self._log.debug('AddDevice(%d): entering...' % axis)

    def ReadOne(self, axis):
        self._log.info('ReadOne(%d): entering...' % axis)
        return time.time()-self.__start_time

    def StateOne(self, axis):
        """Get the dummy trigger/gate state"""
        if time.time() > (self.__integ_time + self.__start_time):
            sta = State.On
            status = "Stopped"
        else:
            sta = State.Moving
            status = "Moving"

        return sta, status

    def PrepareOne(self, axis, value, repetitions, latency_time, nb_starts):
        self._log.info('PrepareOne(%d): entering...' % axis)
        pass

    def LoadOne(self, axis, value, repetitions, latency_time):
        self._log.info('LoadOne(%d): entering...' % axis)
        self.mso.write(':SING')
        time.sleep(0.1)

    def PreStartOne(self, axis, value):
        self._log.info('PreStartOne(%d): entering...' % axis)
        return True

    def StartOne(self, axis, value):
        self._log.info('StartOne(%d): entering...' % axis)
        self.__integ_time = value
        self.__start_time = time.time()

    def StopOne(self, axis):
        self._log.debug('AbortOne(%d): entering...' % axis)
        pass

    def AbortOne(self, axis):
        pass
