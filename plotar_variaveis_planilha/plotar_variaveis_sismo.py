#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 11:16:07 2023

@author: taty
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Lê o arquivo XLSX usando o pandas
nome_arquivo = '/home/taty/Downloads/santa_cruz.xlsx'
dados = pd.read_excel(nome_arquivo)

# Converte a coluna de Data/Horário para o tipo datetime
dados['Data/Horário'] = pd.to_datetime(dados['Data/Horário'])

# Define o formato da data e hora com o "Z" no final
date_format = mdates.DateFormatter('%d/%m %HZ')

# Definir variáveis para cada coluna
temperatura = dados[['Data/Horário', 'Temperatura do Ar']]
umidade = dados[['Data/Horário', 'Umidade Relativa']]
direcao_vento = dados[['Data/Horário', 'Direção do Vento']]
intensidade_vento = dados[['Data/Horário', 'Intensidade do Vento']]
rajada_vento = dados[['Data/Horário', 'Rajada de Vento']]
visibilidade = dados[['Data/Horário', 'Visibilidade']]

# Plota um gráfico para uma variável em relação ao tempo
def plotar_grafico(data, variable, title, unit):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Data/Horário'], data[variable])
    plt.title(title)
    plt.xlabel('Data/Horário')
    plt.ylabel(f'{variable} ({unit})')
    plt.gca().xaxis.set_major_formatter(date_format)
#    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.grid(False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'/home/taty/Imagens/santa_cruz_visibilidade.png', bbox_inches='tight',
                    pad_inches=0.2, dpi=300)
    plt.show()


# Exibe um menu para escolher qual variável visualizar
print("Escolha uma variável para visualizar:")
print("1. Temperatura do Ar (°C)")
print("2. Umidade Relativa (%)")
print("3. Direção do Vento (°)")
print("4. Intensidade do Vento (KT)")
print("5. Rajada de Vento (KT)")
print("6. Visibilidade (MN)")

escolha = int(input("Digite o número da opção desejada: "))

if escolha == 1:
    plotar_grafico(dados, 'Temperatura do Ar', 'Variação da Temperatura do Ar', '°C')
elif escolha == 2:
    plotar_grafico(dados, 'Umidade Relativa', 'Variação da Umidade Relativa', '%')
elif escolha == 3:
    plotar_grafico(dados, 'Direção do Vento', 'Variação da Direção do Vento', 'graus')
elif escolha == 4:
    plotar_grafico(dados, 'Intensidade do Vento', 'Variação da Intensidade do Vento', 'KT')
elif escolha == 5:
    plotar_grafico(dados, 'Rajada de Vento', 'Variação da Rajada de Vento', 'KT')
elif escolha == 6:
    plotar_grafico(dados, 'Visibilidade', 'Variação da Visibilidade', 'MN')
else:
    print("Escolha inválida.")