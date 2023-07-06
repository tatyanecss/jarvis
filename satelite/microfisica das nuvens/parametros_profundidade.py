#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 20:53:14 2023

@author: tatyane
"""

#-----------------------------------------------------------------------------------------------------------
# INPE / CPTEC - Training: Python and GOES-R Imagery: Script 14 - Reprojection with GDAL
#-----------------------------------------------------------------------------------------------------------
# Required modules
from netCDF4 import Dataset                     # Read / Write NetCDF4 files
import matplotlib.pyplot as plt                 # Plotting library
from datetime import datetime                   # Basic Dates and time types
import cartopy, cartopy.crs as ccrs             # Plot maps
import os                                       # Miscellaneous operating system interfaces
from osgeo import osr                           # Python bindings for GDAL
from osgeo import gdal                          # Python bindings for GDAL
import numpy as np                              # Scientific computing with Python
from utilities import download_CMI              # Our function for download
from utilities import loadCPT                   # Import the CPT convert function
import cartopy.io.shapereader as shpreader      # Import shapefiles
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib import cm
#-----------------------------------------------------------------------------------------------------------
# Input and output directories
input = "Samples"; os.makedirs(input, exist_ok=True)
output = "Output"; os.makedirs(output, exist_ok=True)

# Desired extent
extent = [-52., -23., -39.0, -14.0] # Min lon, Max lon, Min lat, Max lat

# Datetime to process
yyyymmddhhmn = '202210031530'
band = '08'
band2 = '15'

# Download the file
file_name = download_CMI(yyyymmddhhmn, band, input)
file_name2 = download_CMI(yyyymmddhhmn, band2, input)

#-----------------------------------------------------------------------------------------------------------
# Variable
var = 'CMI'

# Open the file
img = gdal.Open(f'NETCDF:{input}/{file_name}.nc:' + var)

# Read the header metadata
metadata = img.GetMetadata()
scale = float(metadata.get(var + '#scale_factor'))
offset = float(metadata.get(var + '#add_offset'))
undef = float(metadata.get(var + '#_FillValue'))
dtime = metadata.get('NC_GLOBAL#time_coverage_start')

# Load the data
ds = img.ReadAsArray(0, 0, img.RasterXSize, img.RasterYSize).astype(float)

# Apply the scale, offset and convert to celsius
ds = (ds * scale + offset) - 273.15

# Read the original file projection and configure the output projection
source_prj = osr.SpatialReference()
source_prj.ImportFromProj4(img.GetProjectionRef())

target_prj = osr.SpatialReference()
target_prj.ImportFromProj4("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")

# Reproject the data
GeoT = img.GetGeoTransform()
driver = gdal.GetDriverByName('MEM')
raw = driver.Create('raw', ds.shape[0], ds.shape[1], 1, gdal.GDT_Float32)
raw.SetGeoTransform(GeoT)
raw.GetRasterBand(1).WriteArray(ds)

# Define the parameters of the output file  
options = gdal.WarpOptions(format = 'netCDF', 
          srcSRS = source_prj, 
          dstSRS = target_prj,
          outputBounds = (extent[0], extent[3], extent[2], extent[1]), 
          outputBoundsSRS = target_prj, 
          outputType = gdal.GDT_Float32, 
          srcNodata = undef, 
          dstNodata = 'nan', 
          xRes = 0.02, 
          yRes = 0.02, 
          resampleAlg = gdal.GRA_NearestNeighbour)

print(options)

# Write the reprojected file on disk
gdal.Warp(f'{output}/{file_name}_ret.nc', raw, options=options)
#-----------------------------------------------------------------------------------------------------------
# Open the reprojected GOES-R image
file = Dataset(f'{output}/{file_name}_ret.nc')

# Get the pixel values
data = file.variables['Band1'][:]

#-----------------------------------------------------------------------------------------------------------
# Variable2
var2 = 'CMI'

# Open the file
img2 = gdal.Open(f'NETCDF:{input}/{file_name2}.nc:' + var2)

# Read the header metadata
metadata2 = img2.GetMetadata()
scale2 = float(metadata2.get(var2 + '#scale_factor'))
offset2 = float(metadata2.get(var2 + '#add_offset'))
undef2 = float(metadata2.get(var2 + '#_FillValue'))
dtime2 = metadata2.get('NC_GLOBAL#time_coverage_start')

# Load the data
ds2 = img2.ReadAsArray(0, 0, img2.RasterXSize, img2.RasterYSize).astype(float)

# Apply the scale, offset and convert to celsius
ds2 = (ds2 * scale2 + offset2) - 273.15

# Read the original file projection and configure the output projection
source_prj2 = osr.SpatialReference()
source_prj2.ImportFromProj4(img2.GetProjectionRef())

target_prj2 = osr.SpatialReference()
target_prj2.ImportFromProj4("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")

# Reproject the data
GeoT2 = img2.GetGeoTransform()
driver2 = gdal.GetDriverByName('MEM')
raw2 = driver2.Create('raw', ds2.shape[0], ds2.shape[1], 1, gdal.GDT_Float32)
raw2.SetGeoTransform(GeoT2)
raw2.GetRasterBand(1).WriteArray(ds2)

# Define the parameters of the output file  
options2 = gdal.WarpOptions(format = 'netCDF', 
          srcSRS = source_prj2, 
          dstSRS = target_prj2,
          outputBounds = (extent[0], extent[3], extent[2], extent[1]), 
          outputBoundsSRS = target_prj2, 
          outputType = gdal.GDT_Float32, 
          srcNodata = undef, 
          dstNodata = 'nan', 
          xRes = 0.02, 
          yRes = 0.02, 
          resampleAlg = gdal.GRA_NearestNeighbour)

print(options)

# Write the reprojected file on disk
gdal.Warp(f'{output}/{file_name2}_ret.nc', raw2, options=options2)
#-----------------------------------------------------------------------------------------------------------
# Open the reprojected GOES-R image
file2 = Dataset(f'{output}/{file_name2}_ret.nc')

# Get the pixel values
data2 = file2.variables['Band1'][:]

#Contas
datafinal = data-data2

#-----------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
plt.figure(figsize=(10,10))

# Use the Geostationary projection in cartopy
ax = plt.axes(projection=ccrs.PlateCarree())

# Define the image extent
img_extent = [extent[0], extent[2], extent[1], extent[3]]

# Define the color scale based on the channel
colormap = "YlGnBu_r"
cpt = loadCPT('/IR4AVHRR6.cpt')                   # Load the CPT file   
my_cmap = cm.colors.LinearSegmentedColormap('cpt', cpt)          # Create a custom linear colormap
vmin = -103.0                                                    # Min. value
vmax = 84.0                                                      # Max. value
    
# Plot the image
img3 = ax.imshow(datafinal, origin='upper', extent=img_extent, cmap=colormap)

# Add a shapefile
shapefile = list(shpreader.Reader('/MG_Microrregioes_2021.shp').geometries())
ax.add_geometries(shapefile, ccrs.PlateCarree(), edgecolor='black',facecolor='none', linewidth=1)

# Add coastlines, borders and gridlines
ax.coastlines(resolution='10m', color='white', linewidth=0.8)
ax.add_feature(cartopy.feature.BORDERS, edgecolor='white', linewidth=0.5)
gl = ax.gridlines(crs=ccrs.PlateCarree(), color='gray', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
gl.top_labels = False
gl.right_labels = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlocator  =  mticker.FixedLocator(np.arange(-52,-39,2)) #intervalo x
gl.ylocator  =  mticker.FixedLocator(np.arange(-23,-14,2)) #intervalo y

# Add a colorbar
plt.colorbar(img3, label='Temperatura (°C)', extend='both', orientation='horizontal', pad=0.05, fraction=0.05)

# Extract date
date = (datetime.strptime(dtime, '%Y-%m-%dT%H:%M:%S.%fZ'))

# Add a title
plt.title('Profundidade da nuvem ' + date.strftime('%Y-%m-%d %H:%M') + ' UTC', fontweight='bold', fontsize=10, loc='left')
plt.title('Reg.: ' + str(extent) , fontsize=10, loc='right')
#-----------------------------------------------------------------------------------------------------------
# Save the image
plt.savefig(f'{output}/profundidade_1530.png', bbox_inches='tight', pad_inches=0.2, dpi=300)

# Show the image
plt.show()
