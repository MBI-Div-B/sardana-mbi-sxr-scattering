from sardana.macroserver.macro import Macro, macro, Type
import os
from dirsync import sync
import tango
import time


@macro([["integ_time", Type.Float, 0.05, "integration time in [s]"]])
def acquire(self, integ_time):
    """Macro acquire"""
    self.execMacro('timescan', '0', '{:0.3f}'.format(integ_time), '10', '0.2')


@macro([
    ['motor', Type.Moveable, None, 'Moveable to move'],
    ['start_pos', Type.Float, None, 'Scan start position'],
    ['final_pos', Type.Float, None, 'Scan final position'],
    ['nr_interv', Type.Integer, None, 'Number of scan intervals'],
    ['integ_time', Type.Float, None, 'Integration time']
])
def lup(self, motor, start_pos, final_pos, nr_interv, integ_time):
    """motor scan relative to the starting position.
    lup scans one motor, as specified by motor. If motor motor is at a
    position X before the scan begins, it will be scanned from X+start_pos
    to X+final_pos. The step size is (start_pos-final_pos)/nr_interv.
    The number of data points collected will be nr_interv+1. Count time is
    given by time which if positive, specifies seconds and if negative,
    specifies monitor counts. """
    self.execMacro(['dscan', motor, start_pos, final_pos, nr_interv, integ_time])



@macro()
def custom_snapshot(self):
    """add some custom comments to the snapshots.
    First hard code the data source and make it configurable later on."""
    self.output("Running custom_snapshot...")
    
    parent = self.getParentMacro()
    if parent and (parent._name != 'ct'):
        self.output("Its a scan")
        dh = parent._gScan._data_handler
        # at this point the entry name is not yet set, so we give it explicitly
        # (otherwise it would default to "entry")
        dh.addCustomData([1, 2, 4, 5], 'dummyChar1',
                         nxpath='/custom_entry:NXentry/customdata:NXcollection')
    else:
        self.output("Its not a scan")



@macro()
def sync_data(self):
    ScanDir = self.getEnv('ScanDir')
    RemoteScanDir = self.getEnv('RemoteScanDir')
        
    if os.path.exists(RemoteScanDir):
        self.info('Syncing data from %s to %s', ScanDir, RemoteScanDir)
        sync(ScanDir, RemoteScanDir, 'sync', create=True)        
    else:
        self.warning('RemoteScanDir %s does not exist - no folder syncing', RemoteScanDir)



@macro([["integ_time", Type.Float, 0.05, "integration time in [s]"]])
def snap(self, integ_time):
    """Macro snap (ct wrapper)"""
    self.execMacro('user_pre_scan')
    self.execMacro('user_pre_acq')
    self.execMacro('ct', '{:0.3f}'.format(integ_time))
    self.execMacro('user_post_scan')