#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 10 23:32:35 2019

@author: jacopo
"""

import Fringes_dataset_manager as fdm
import initialization

for l in ['p', 'a', 'g']:
    output_mc(create_measures(*get_names(l, names)))
