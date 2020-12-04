#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 18:31:12 2020

@author: orestis
"""

from traces import Transversal
from plots import plot_obj_vtk


transversal = Transversal(45, 135, 1, 10000, "data.yaml")

# Export obj and vtk for the first angle pair of the transversal direction and get paths
obj_path, vtk_path = transversal.export_obj_vtk(0, nrays=100)
plot_obj_vtk(obj_path, vtk_path)
