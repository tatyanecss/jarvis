#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 14:44:05 2023

@author: taty
"""

import geopandas as gpd
import matplotlib.pyplot as plt

# Carregar o shapefile dos municípios de Pernambuco
pernambuco_shapefile = "/PE_Municipios_2022.shp"
municipios = gpd.read_file(pernambuco_shapefile)

# Filtrar os municípios da região metropolitana de Recife
regiao_metropolitana = ['Jaboatão dos Guararapes', 'Olinda', 'Paulista',
                  'Igarassu', 'Abreu e Lima', 'Camaragibe',
                  'Cabo de Santo Agostinho', 'São Lourenço da Mata',
                  'Araçoiaba', 'Ilha de Itamaracá', 'Ipojuca', 'Moreno',
                  'Itapissuma', 'Recife']
regiao_metropolitana2 = ['Cabo de Santo Agostinho']
municipios_regiao_metropolitana = municipios[municipios["NM_MUN"].isin(regiao_metropolitana)]
municipios_regiao_metropolitana2 = municipios[municipios["NM_MUN"].isin(regiao_metropolitana2)]

# Calcular o centro do mapa
centro_x = (municipios.total_bounds[0] + municipios.total_bounds[2]) / 2
centro_y = (municipios.total_bounds[1] + municipios.total_bounds[3]) / 2

# Criar uma nova figura do Matplotlib
fig, ax = plt.subplots(figsize=(10, 10))

# Plotar todos os municípios de Pernambuco em branco
municipios.plot(ax=ax, color="whitesmoke", edgecolor="lightgrey")

# Plotar os municípios da região metropolitana de Recife com uma cor única
municipios_regiao_metropolitana.plot(ax=ax, color="red", edgecolor="black")

# Plotar um município da região metropolitana de Recife com uma cor única
municipios_regiao_metropolitana2.plot(ax=ax, color="blue", edgecolor="black")

# Configurar os limites do gráfico
ax.set_xlim(centro_x - 5, centro_x + 3.)
ax.set_ylim(centro_y - 3.5, centro_y + 0.5)

# Configurar os marcadores dos eixos x e y
ax.set_xticks([centro_x - 5., centro_x - 1., centro_x + 3.])
ax.set_xticklabels(['{:.1f}'.format(centro_x - 0.5), '{:.1f}'.format(centro_x), '{:.1f}'.format(centro_x + 0.5)])
ax.set_yticks([centro_y - 3.5, centro_y -1.5, centro_y + 0.5])
ax.set_yticklabels(['{:.1f}'.format(centro_y - 0.5), '{:.1f}'.format(centro_y), '{:.1f}'.format(centro_y + 0.5)])

# Configurar os eixos com as coordenadas
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Adicionar título
plt.title('Região Metropolitana do Recife', fontweight='bold', fontsize=25, loc='center')

# Salvar
plt.savefig('/RMR2.png', bbox_inches='tight', pad_inches=0.1, dpi=300)

# Exibir o gráfico
plt.show()