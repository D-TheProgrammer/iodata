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
"""Test iodata.inputs module."""


import os
import numpy as np

from typing import List

from ..iodata import IOData
from ..utils import angstrom
from ..api import load_one, write_input

try:
    from importlib_resources import path
except ImportError:
    from importlib.resources import path


def check_load_input_and_compare(fname: str, expected_lines: List[str]):
    """Load saved input file and compare to expected input lines.

    Parameters
    ----------
    fname : str
        Input file name to load.
    expected_lines : sequence of str
        Expected lines in the input file.

    """
    with open(fname, 'r') as ifn:
        content = "".join(ifn.readlines())
    expected = "\n".join(expected_lines)
    assert content == expected


def test_input_gaussian_from_xyz(tmpdir):
    # load geometry from xyz file & add level of theory & basis set
    with path('iodata.test.data', 'water_number.xyz') as fn:
        mol = load_one(fn)
    mol.nelec = 10
    mol.spinpol = 0
    mol.lot = 'ub3lyp'
    mol.obasis_name = '6-31g*'
    # write input in a temporary folder using an input template
    fname = os.path.join(tmpdir, 'input_from_xyz.com')
    with path('iodata.test.data', 'template_gaussian.com') as tname:
        write_input(mol, fname, fmt='gaussian', template=tname)
    # load input & compare
    lines = ["%chk=gaussian.chk", "%mem=3500MB", "%nprocs=4",
             "#p ub3lyp/6-31g* opt scf(tight,xqc,fermi) integral(grid=ultrafine) nosymmetry",
             "", "Water ub3lyp/6-31g* opt-force", "", "0 1", ""
             "H     0.783837  -0.492236  -0.000000",
             "O    -0.000000   0.062020  -0.000000",
             "H    -0.783837  -0.492236  -0.000000",
             "", "--Link1--", "%chk=gaussian.chk", "%mem=3500MB", "%nprocs=4",
             "#p ub3lyp/6-31g* force guess=read geom=allcheck integral(grid=ultrafine) output=wfn",
             "", "gaussian.wfn", "", "", "", ""]
    check_load_input_and_compare(fname, lines)


def test_input_gaussian_from_iodata(tmpdir):

    # make an instance of IOData for HCl anion
    data = {"atcoords": np.array([[0.0, 0.0, 0.0], [angstrom, 0.0, 0.0]]),
            "atnums": np.array([1, 17]), "nelec": 19, "run_type": 'opt',
            "title": " hydrogen chloride anion", "spinpol": 1}
    mol = IOData(**data)
    # write input in a temporary file
    fname = os.path.join(tmpdir, 'input_from_iodata.com')
    write_input(mol, fname, fmt='gaussian')
    # load input & compare
    expected_lines = ["#n hf/sto-3g opt", "", " hydrogen chloride anion", "", "-1 2",
                      "H     0.000000   0.000000   0.000000",
                      "Cl    1.000000   0.000000   0.000000",
                      "", "", ""]
    check_load_input_and_compare(fname, expected_lines)


def test_input_gaussian_from_fchk(tmpdir):
    # load fchk
    with path('iodata.test.data', 'water_hfs_321g.fchk') as fn:
        mol = load_one(fn)
    # write input in a temporary file
    fname = os.path.join(tmpdir, 'input_from_fchk.in')
    write_input(mol, fname, fmt='gaussian')
    # compare saved input to expected
    expected_lines = ["#n rhfs/3-21g sp", "", "water", "", "0 1",
                      "H     0.000000   0.783837  -0.443405",
                      "O     0.000000   0.000000   0.110851",
                      "H    -0.000000  -0.783837  -0.443405",
                      "", "", ""]
    check_load_input_and_compare(fname, expected_lines)
