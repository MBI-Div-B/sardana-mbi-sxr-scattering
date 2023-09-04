import numpy as np

from sardana.pool.controller import PseudoMotorController
from sardana.pool.controller import (
    Type,
    Description,
    DefaultValue,
    Access,
    FGet,
    FSet,
    DataAccess,
    Memorize,
    Memorized,
)


class MagnetPseudoMotorController(PseudoMotorController):
    """A Slit pseudo motor controller for handling gap and offset pseudo
    motors. The system uses to real motors sl2t (top slit) and sl2b (bottom
    slit)."""

    axis_attributes = {
        "factor": {
            Type: float,
            Description: "mTperA",
            DefaultValue: 1,
            Memorized: Memorize,
        },
    }

    pseudo_motor_roles = ("OutputMotor",)
    motor_roles = ("InputMotor",)

    def __init__(self, inst, props):
        PseudoMotorController.__init__(self, inst, props)

    def CalcPhysical(self, axis, pseudo_pos, curr_physical_pos):
        field = pseudo_pos[axis - 1]
        return field / self.factor

    def CalcPseudo(self, axis, physical_pos, curr_pseudo_pos):
        mag_curr = physical_pos[axis - 1]
        return mag_curr * self.factor

    def GetAxisExtraPar(self, axis, name):
        """Get Smaract axis particular parameters.
        @param axis to get the parameter
        @param name of the parameter to retrive
        @return the value of the parameter
        """
        name = name.lower()

        if name == "factor":
            result = self.factor
        else:
            raise ValueError("There is not %s attribute" % name)
        return result

    def SetAxisExtraPar(self, axis, name, value):
        """Set Smaract axis particular parameters.
        @param axis to set the parameter
        @param name of the parameter
        @param value to be set
        """
        name = name.lower()
        if name == "factor":
            self.factor = value
        else:
            raise ValueError("There is not %s attribute" % name)
