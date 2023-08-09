#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Autor: INPE / CPTEC
#Editado por: Tatyane Sousa - Meteorologista - tatyanecss@gmail.com

# Módulos necessários
from netCDF4 import Dataset                     # Ler/gravar arquivos NetCDF4
import matplotlib.pyplot as plt                 # Biblioteca de plotagem
from datetime import datetime, timedelta        # Tipos básicos de datas e horários
import cartopy, cartopy.crs as ccrs             # Plotagem de mapas
import os                                       # Interfaces diversas do sistema operacional
from osgeo import osr                           # Biblioteca Python para GDAL
from osgeo import gdal                          # Biblioteca Python para GDAL
import numpy as np                              # Computação científica com Python
from utilities import download_CMI              # Nossa função para download
from utilities import loadCPT                   # Importar função de conversão de CPT
import cartopy.io.shapereader as shpreader      # Importar shapefiles
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from matplotlib import cm
import geopandas as gpd
#-----------------------------------------------------------------------------------------------------------
# Input and output directories
input = "Samples"; os.makedirs(input, exist_ok=True)
output = "Output"; os.makedirs(output, exist_ok=True)

# Extensão desejada
extent = [-44., -23.5, -41.5, -21.5] # Min lon, Max lon, Min lat, Max lat

# Start datetime to process
start_time = datetime.strptime('202211081900', '%Y%m%d%H%M')
end_time = start_time + timedelta(hours=1.5)  # 4 hours interval from start_time

# Loop through time intervals of 30 minutes
while start_time < end_time:
    # Format current datetime
    yyyymmddhhmn = start_time.strftime('%Y%m%d%H%M')
    
    # Baixar o arquivo
    file_name = download_CMI(yyyymmddhhmn, '11', input)
    file_name2 = download_CMI(yyyymmddhhmn, '14', input)
    file_name3 = download_CMI(yyyymmddhhmn, '15', input)
    
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

#-----------------------------------------------------------------------------------------------------------
# Variable3
    var3 = 'CMI'

# Open the file
    img3 = gdal.Open(f'NETCDF:{input}/{file_name3}.nc:' + var3)

# Read the header metadata
    metadata3 = img3.GetMetadata()
    scale3 = float(metadata3.get(var3 + '#scale_factor'))
    offset3 = float(metadata3.get(var3 + '#add_offset'))
    undef3 = float(metadata3.get(var3 + '#_FillValue'))
    dtime3 = metadata3.get('NC_GLOBAL#time_coverage_start')

# Load the data
    ds3 = img3.ReadAsArray(0, 0, img3.RasterXSize, img3.RasterYSize).astype(float)

# Apply the scale, offset and convert to celsius
    ds3 = (ds3 * scale3 + offset3) - 273.15

# Read the original file projection and configure the output projection
    source_prj3 = osr.SpatialReference()
    source_prj3.ImportFromProj4(img3.GetProjectionRef())

    target_prj3 = osr.SpatialReference()
    target_prj3.ImportFromProj4("+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")

# Reproject the data
    GeoT3 = img3.GetGeoTransform()
    driver3 = gdal.GetDriverByName('MEM')
    raw3 = driver3.Create('raw', ds3.shape[0], ds3.shape[1], 1, gdal.GDT_Float32)
    raw3.SetGeoTransform(GeoT3)
    raw3.GetRasterBand(1).WriteArray(ds3)

# Define the parameters of the output file  
    options3 = gdal.WarpOptions(format = 'netCDF', 
          srcSRS = source_prj3, 
          dstSRS = target_prj3,
          outputBounds = (extent[0], extent[3], extent[2], extent[1]), 
          outputBoundsSRS = target_prj3, 
          outputType = gdal.GDT_Float32, 
          srcNodata = undef, 
          dstNodata = 'nan', 
          xRes = 0.02, 
          yRes = 0.02, 
          resampleAlg = gdal.GRA_NearestNeighbour)

    print(options)

# Write the reprojected file on disk
    gdal.Warp(f'{output}/{file_name3}_ret.nc', raw3, options=options3)
#-----------------------------------------------------------------------------------------------------------
# Open the reprojected GOES-R image
    file3 = Dataset(f'{output}/{file_name3}_ret.nc')

# Get the pixel values
    data3 = file3.variables['Band1'][:]

#-----------------------------------------------------------------------------------------------------------

#Contas
    datafinal = (data-data2)-(data2-data3)

#-----------------------------------------------------------------------------------------------------------
# Choose the plot size (width x height, in inches)
    plt.figure(figsize=(10,10))

# Use the Geostationary projection in cartopy
    ax = plt.axes(projection=ccrs.PlateCarree())

# Define the image extent
    img_extent = [extent[0], extent[2], extent[1], extent[3]]

# Define the color scale based on the channel
    colormap = "seismic_r" # White to black for IR channels
#    cpt = loadCPT('/home/taty/Downloads/isadora/baixar_e_plotar_imagens/IR4AVHRR6.cpt')                   # Load the CPT file   
#    my_cmap = cm.colors.LinearSegmentedColormap('cpt', cpt)          # Create a custom linear colormap
    norm=plt.Normalize(-1,1)
    cmap = cm.colors.LinearSegmentedColormap.from_list("", ["white","red", "white", "blue", "blue"])
    vmin = -3.0                                                    # Min. value
    vmax = 4.0                                                      # Max. value

# Plot the image
    img3 = ax.imshow(datafinal, origin='upper', extent=img_extent, cmap=cmap, norm=norm)

# Carregar o shapefile dos municípios de Pernambuco
    pernambuco_shapefile = "/home/taty/Downloads/isadora/RJ_Municipios_2022.shp"
    municipios = gpd.read_file(pernambuco_shapefile)

# Filtrar os municípios da região metropolitana de Recife
    nova_iguacu = ['Cordeiro', 'Rio de Janeiro', 'Duque de Caxias']
    municipios_nova_iguacu = municipios[municipios["NM_MUN"].isin(nova_iguacu)]

# Plotar os municípios da região metropolitana de Recife com uma cor única
    municipios_nova_iguacu.plot(ax=ax, color="none", edgecolor="black")
    
# Add coastlines, borders and gridlines
    ax.coastlines(resolution='10m', color='gray', linewidth=0.8)
    ax.add_feature(cartopy.feature.BORDERS, edgecolor='gray', linewidth=0.5)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), color='gray', alpha=1.0, linestyle='--', linewidth=0.25, xlocs=np.arange(-180, 180, 5), ylocs=np.arange(-90, 90, 5), draw_labels=True)
    gl.top_labels = False
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlocator = mticker.FixedLocator(np.arange(-44., -41.5, 0.5))  # intervalo x
    gl.ylocator = mticker.FixedLocator(np.arange(-23.5, -21.5, 0.5))  # intervalo y

# Add a colorbar
    plt.colorbar(img3, label='Temperatura (°C)', extend='both', orientation='horizontal', pad=0.05, fraction=0.05)

    # Extract date
    date = (datetime.strptime(dtime, '%Y-%m-%dT%H:%M:%S.%fZ'))

# Add a title
    plt.title('Glaciação no topo da nuvem ' + date.strftime('%Y-%m-%d %H:%M') + ' UTC', fontweight='bold', fontsize=10, loc='left')
#    plt.title('Reg.: ' + str(extent) , fontsize=10, loc='right')
    
    # Save the image with the current datetime as the filename
    filename = start_time.strftime('%H%M') + '_zoom.png'
    plt.savefig(f'{output}/glaciacao_zoom_{filename}', bbox_inches='tight', pad_inches=0.2, dpi=300)

    # Increment the time by 30 minutes for the next iteration
    start_time += timedelta(minutes=10)

    # Close all open files and clear the plot
    plt.close('all')

# Show the last image
plt.show()