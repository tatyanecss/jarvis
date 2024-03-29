#!/usr/bin/env python3.9.5
# -*- Coding: UTF-8 -*-

import os
import utilities

# INPUT VARIABLES - Extent and Datetime
extent = [-60.0, -35.0, -45.0, -25.0] # [min. lon, min. lat, max. lon, max. lat]
yyyymmddhhmn = '202107071000'

# Check/create input and output directories
input = 'input'; os.makedirs(input, exist_ok=True)
output = 'output'; os.makedirs(output, exist_ok=True)

# Download/read file and get variable var
var = 'CMI'
for band in [13, 7]:
    # Download file
    file_name = utilities.download_CMI(yyyymmddhhmn, band, input)
    # Read file - 13 and 7 have same projection (img and undef)
    dtime, img, undef, ds = utilities.get_ds(input, file_name, var, 0)
    # Save band 13 datasheet
    if band == 13:
        ds_13 = ds

# Calculate difference - BTD
ds = ds_13 - ds

# Reprojection of BTD image and write to a NC file
file_name = f"{output}/{file_name.replace('C07', 'BTD')}"
utilities.proj_ret(img, undef, ds, extent, file_name)

# Define properties to plot map
properties = {
    'colormap': 'gray',
    'label': 'Night Fog Difference',
    'band': 'BTD',
    'vmin': -5,
    'vmax': 5
}
utilities.plot_map(dtime, file_name, extent, properties)