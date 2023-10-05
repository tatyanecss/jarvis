#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 23:00:09 2023

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
municipios_regiao_metropolitana = municipios[municipios["NM_MUN"].isin(regiao_metropolitana)]

# Calcular o centro do mapa
centro_x = (municipios.total_bounds[0] + municipios.total_bounds[2]) / 2
centro_y = (municipios.total_bounds[1] + municipios.total_bounds[3]) / 2

# Criar uma nova figura do Matplotlib
fig, ax = plt.subplots(figsize=(10, 10))

# Plotar todos os municípios de Pernambuco em branco
municipios.plot(ax=ax, color="whitesmoke", edgecolor="lightgrey")

# Plotar os municípios da região metropolitana de Recife com uma cor única
municipios_regiao_metropolitana.plot(ax=ax, color="whitesmoke", edgecolor="black")

# Configurar os eixos com as coordenadas
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Adicionar título
plt.title('Região Metropolitana do Recife', fontweight='bold', fontsize=25, loc='center')

# Salvar
plt.savefig('/Imagens/rmr_foco.png', bbox_inches='tight', pad_inches=0.2, dpi=300)

# Exibir o gráfico
plt.show()
