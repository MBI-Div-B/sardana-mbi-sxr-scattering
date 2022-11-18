from tango import DeviceProxy
from sardana import State
from sardana.pool.controller import TwoDController, Type, Description, DefaultValue, FGet, FSet
import time
import numpy

class HamamatsuTangoTwoDController(TwoDController):
    """The most basic controller intended from demonstration purposes only.
    This is the absolute minimum you have to implement to set a proper counter
    controller able to get a counter value, get a counter state and do an
    acquisition.
    This example is so basic that it is not even directly described in the
    documentation"""



    def __init__(self, inst, props, *args, **kwargs):
        """Constructor"""
        TwoDController.__init__(self,inst,props, *args, **kwargs)
        print('Hamamatsu Tango Initialization ...')
        #self.proxy = DeviceProxy('faraday/HamamatsuTango/1')
        print('SUCCESS')
        self.startTime = 0
        self.expTime = 0
        self._axes = {}


    def AddDevice(self, axis):
        self._axes[axis] = {}

    def DeleteDevice(self, axis):
        self._axes.pop(axis)

        
    def ReadOne(self, axis):
        """Get the specified counter value"""  
        #self.proxy.getImage()
        #return self.proxy.image
        return numpy.ones((2048,2048))*30000 
    
    def SetAxisPar(self, axis, parameter, value):
        pass

    def StateOne(self, axis):
        if abs(self.startTime-time.time()) < self.expTime:
            return State.Moving, 'Moving'
        else:
            return State.On, 'No Moving'
        """Get the specified counter state"""
        #if self.proxy.recording:
        #    return State.Moving, 'Moving'
        #else:
        #    return State.On, 'No Moving'
        pass

    def PrepareOne(self, axis, value, repetitions, latency, nb_starts):
        #print(float(value * 1000))
        #self.proxy.exposure_time = float(value * 1000)
        self.expTime = value
        pass
    
    def LoadOne(self, axis, value, repetitions, latency_time):
        pass

    def StartOne(self, axis, value=None):
        """acquire the specified counter"""
        #self.proxy.stopAcquisition()
        #self.proxy.startAcquisition()
        #return
        self.startTime = time.time()
        pass

    def StopOne(self, axis):
        """Stop the specified counter"""
        #self.proxy.stopAcquisition()
        pass    

    def AbortOne(self, axis):
        """Abort the specified counter"""
        #self.proxy.stopAcquisition()
        pass
