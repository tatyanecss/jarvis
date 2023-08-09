#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 9 11:16:07 2023

@author: taty
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Lê o arquivo XLSX usando o pandas
nome_arquivo = '/home/taty/Downloads/ilha_do_pai.xlsx'
dados = pd.read_excel(nome_arquivo)

# Converte a coluna de Data/Horário para o tipo datetime
dados['Data/Horário'] = pd.to_datetime(dados['Data/Horário'])

# Define o formato da data e hora com o "Z" no final
date_format = mdates.DateFormatter('%d/%m %HZ')

# Definir variáveis para cada coluna
variaveis = [
    ('Temperatura do Ar', '°C'),
    ('Umidade Relativa', '%'),
    ('Direção do Vento', 'graus'),
    ('Intensidade do Vento', 'KT'),
    ('Rajada de Vento', 'KT'),
    ('Visibilidade', 'MN')
]

# Plota um gráfico para uma variável em relação ao tempo
def plotar_grafico(data, variable, title, unit):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Data/Horário'], data[variable])
    plt.title(title)
    plt.xlabel('Data/Horário')
    plt.ylabel(f'{variable} ({unit})')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.grid(False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'/home/taty/Imagens/ilha_do_pai_{variable.lower()}.png', bbox_inches='tight',
                pad_inches=0.2, dpi=300)
    plt.close()

# Loop para plotar todos os gráficos
for var, unit in variaveis:
    plotar_grafico(dados, var, f'Variação da {var} - Ilha do Pai', unit)

print("Gráficos gerados com sucesso!")
