from sardana.macroserver.macro import macro, Type

@macro()
def alton(self):
    """Macro alton"""
    acqConf = self.getEnv('acqConf')
    acqConf['altOn'] = True
    self.setEnv('acqConf', acqConf)
    self.info('switching alternate ON')
    
    # # enable minus field counters
    # mnt_grp = self.getObj(self.getEnv('ActiveMntGrp'), type_class=Type.MeasurementGroup)
    # mnt_grp.setEnabled(True, "epochM", "ADC0M", "ADC1M", "pm_pumpM", "pressure_readM") #"specM", "spec1M", "spec2M", "spec3M", "spec4M","refM", "ref1M", "ref2M", "ref3M", "ref4M", )



@macro()    
def altoff(self):
    """Macro altoff"""
    acqConf = self.getEnv('acqConf')
    acqConf['altOn'] = False
    self.setEnv('acqConf', acqConf)
    self.info('switching alternate OFF')
    
    # # disable minus field counters
    # mnt_grp = self.getObj(self.getEnv('ActiveMntGrp'), type_class=Type.MeasurementGroup)
    # mnt_grp.setEnabled(False, "epochM", "ADC0M", "ADC1M", "pm_pumpM", "pressure_readM", "specM", "spec1M", "spec2M", "spec3M", "spec4M","refM", "ref1M", "ref2M", "ref3M", "ref4M")
    
