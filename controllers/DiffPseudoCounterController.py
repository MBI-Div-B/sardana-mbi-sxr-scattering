##############################################################################
##
# This file is part of Sardana
##
# http://www.sardana-controls.org/
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Sardana is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Sardana is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""This module contains the definition of a I1-I2 pseudo counter controller
for the Sardana Device Pool"""

__all__ = ["Diff"]

__docformat__ = 'restructuredtext'

from sardana.pool.controller import PseudoCounterController


class DiffPseudoCounterController(PseudoCounterController):
    """ A simple pseudo counter which receives two counter values (I1 and I2)
        and returns I1-I2"""

    counter_roles = "I1", "I2"
    pseudo_counter_roles = "diff",

    def Calc(self, axis, counter_values):
        i1, i2 = counter_values
        return i1 - i2
