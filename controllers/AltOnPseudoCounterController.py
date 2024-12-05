from sardana.pool.controller import PseudoCounterController
from PyTango import DeviceProxy

class AltOnPseudoCounterController(PseudoCounterController):
    """ A  pseudo counter which remebers the input for negative magnetic
    fields and returns it at positive fields"""

    counter_roles        = ('I',)
    pseudo_counter_roles = ('O',)
    value = 0
    field = 0
    
    def __init__(self, inst, props):  
        PseudoCounterController.__init__(self, inst, props)
        self.magnet = DeviceProxy("tango://ampere.sxr.lab:10000/rsxs/caenfastps/magnet")
    
    def Calc(self, axis, counters):
        counter = counters[0]
        try:
            #self.field = self.magnetState.magnet
            self.field = self.magnet.current
            
            if self.field < 0:
                self.value = counter
        except:
            pass
    
        return self.value
