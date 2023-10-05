#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Autor: Tatyane Sousa - Meteorologista - tatyanecss@gmail.com

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

# Crie uma figura
plt.figure(figsize=(8, 8))

# Configurar a projeção azimutal da Antártica
m = Basemap(projection='ortho', lat_0=-90, lon_0=0, resolution='l')

# Desenhar a terra e o oceano com cores diferentes
m.drawcoastlines(linewidth=0.5)
m.drawcountries(linewidth=0.5)
m.drawparallels(np.arange(-90., 91., 30.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(0, 360, 45), labels=[1, 1, 1, 1], fmt='%d')

m.drawmapboundary(fill_color='lightblue')  # Cor suave do oceano
m.fillcontinents(color='lightgray', lake_color='lightblue')  # Altere a cor da terra para 'lightgray'

# Coordenadas para a primeira linha de -45W/-60S para -90W/-60S
lon_line1 = [-90, -45]  # Longitude de -45°W a -90°W
lat_line1 = [-5, -5]  # Latitude de -60°S a -60°S

# Coordenadas para a segunda linha de -45W/-90W para -45W/-10S
lon_line2 = [-45, -45]  # Longitude de -45°W a -45°W
lat_line2 = [-90, -10]  # Latitude de -90°S a -10°S

# Coordenadas para a linha que liga o meridiano de 90W ao paralelo de 60S
lon_line3 = [-90, -90]  # Longitude constante de -90°W
lat_line3 = [-90, -10]  # Latitude de -60°S a -10°S

# Coordenadas para a linha curva entre os meridianos de 90W e 45W
lon_curve_line = np.linspace(-90, -45, 100)  # Criando uma série de longitudes curvas
lat_curve_line = [-5] * len(lon_curve_line)  # Latitude constante de -10°S

# Converter coordenadas para projeção
x_curve_line, y_curve_line = m(lon_curve_line, lat_curve_line)

# Desenhar a linha curva em vermelho
m.plot(x_curve_line, y_curve_line, 'r-', linewidth=2.5)

# Desenhar a segunda linha em vermelho
x_line2, y_line2 = m(lon_line2, lat_line2)
m.plot(x_line2, y_line2, 'r-', linewidth=2.5)

# Desenhar a terceira linha em vermelho
x_line3, y_line3 = m(lon_line3, lat_line3)
m.plot(x_line3, y_line3, 'r-', linewidth=2.5)

# Mostrar o gráfico
plt.show()
