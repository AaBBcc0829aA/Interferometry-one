#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:34:36 2019

@author: jacopo
"""

import Fringes_dataset_manager as fdm
import initialization as init
from numpy.random import uniform
from numpy.random import normal
from numpy.random import triangular
import numpy as np

def theta_from_fringes_medium(N, index, gamma):
    """
    Inverse function of fringes_difference_medium, still for a generic medium
    """
    Nabs = np.abs(N)
    cos_arg = (index**2 - 1 - (gamma * Nabs + index - 1)**2)/(2*(gamma*Nabs+index-1))
    cos_arg = np.clip(cos_arg, -1, 1)
    theta = (np.sign(N) * np.arccos(cos_arg))
    return(theta)
    
def fringes_from_theta_medium(theta, index, gamma):
    '''
    Number of fringes observed between 0 and theta due to a "thickness" thick layer of medium 
    of refractive index "index"
    '''
    n = np.sign(theta) / gamma * ( 1 - index - np.cos(theta) 
                                       + np.sqrt(index**2 - np.sin(theta)**2))
    return(n)

def dirty_angles(angles, half_width_fraction=0.25):
    angle_diffs = np.gradient(angles)
    def da(a, ad):
        hw = ad * half_width_fraction
        triangular_sample = triangular(a-hw, a, a+hw)
        return(triangular_sample)
    new_angles = da(angles, angle_diffs)
    return(new_angles)
    
def dataset_sim(n_fringes, index, gamma, cfac):
    fringes = np.arange(-n_fringes, n_fringes)
    angles = theta_from_fringes_medium(fringes, index, gamma)
    angles = dirty_angles(angles)
    steps = angles / cfac
    data = fdm.dataset()
    data.step_array = steps
    data.fringes_array = fringes
    data.analyze_fine()
    return(data)

def measure_sim(fringes, index_b, gamma_b, index_l, gamma_l, cfac):
    """
    returns a measure.
    
    Inputs:
    Fringes is a number, the datasets go from -fringes to +fringes
    indices and gamma for _background and _liquid
    cfac is the conversion factor, also called alpha
    """
    
    bkg = dataset_sim(fringes, index_b, gamma_b, cfac)
    sig = dataset_sim(fringes, index_l, gamma_l, cfac)
    
    angles = sig.step_array * cfac
    bkg_fringes = fringes_from_theta_medium(angles, index_b, gamma_b)
    sig.fringes_array = sig.fringes_array + bkg_fringes
    
    mea = fdm.measure(bkg, sig)
    mea.subtract_background(use_data=True)
    return(mea)