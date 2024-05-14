# IODATA is an input and output module for quantum chemistry.
# Copyright (C) 2011-2019 The IODATA Development Team
#
# This file is part of IODATA.
#
# IODATA is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# IODATA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
# --
"""Utilities for writing input files."""

import attr

import numpy as np

from ..iodata import IOData
from ..utils import angstrom

__all__ = ["populate_fields"]


def populate_fields(data: IOData) -> dict:
    """Generate a dictionary with fields to replace in the template."""
    # load IOData dict using attr.asdict because the IOData class uses __slots__
    fields = attr.asdict(data, recurse=False)
    # store atomic coordinates in angstrom
    fields["atcoords"] = data.atcoords / angstrom
    # set general defaults
    fields["title"] = data.title if data.title is not None else "Input Generated by IOData"
    fields["run_type"] = data.run_type if data.run_type is not None else "energy"
    # convert spin polarization to multiplicity
    fields["spinmult"] = int(abs(np.round(data.spinpol))) + 1 if data.spinpol is not None else 1
    fields["charge"] = int(data.charge) if data.charge is not None else 0
    return fields
