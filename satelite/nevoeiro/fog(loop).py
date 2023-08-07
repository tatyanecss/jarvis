#!/usr/bin/env python3.9.5
# -*- Coding: UTF-8 -*-

import os
import utilities
from datetime import datetime, timedelta

# INPUT VARIABLES - Extent
extent = [-43.5, -23.1, -42.8, -22.6]  # [min. lon, min. lat, max. lon, max. lat]

# Define date and time interval
initial_datetime = datetime(2023, 8, 3, 8, 0)  # 2023-08-03 08:00
final_datetime = datetime(2023, 8, 3, 10, 0)  # 2023-08-03 10:00
time_interval = timedelta(minutes=10)

# Check/create input and output directories
input = 'input'; os.makedirs(input, exist_ok=True)
output = 'output'; os.makedirs(output, exist_ok=True)

# Loop through dates and times
current = initial_datetime
while current <= final_datetime:
    yyyymmddhhmn = current.strftime('%Y%m%d%H%M')
    
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
    output_file_name = f"{output}/{file_name.replace('C07', 'BTD')}"
    utilities.proj_ret(img, undef, ds, extent, output_file_name)
    
    # Define properties to plot map
    properties = {
        'colormap': 'gray',
        'label': 'Night Fog Difference',
        'band': 'BTD',
        'vmin': -5,
        'vmax': 5
    }
    utilities.plot_map(dtime, output_file_name, extent, properties)
    
    # Update to the next time interval
    current += time_interval
