import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Configurações do matplotlib e seaborn
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.titlesize'] = 20

file_path = 'Case de Dados - Maxmilhas.xlsx'
df = pd.read_excel(file_path)

# Primeiro é importante converter as colunas de data para o tipo datetime
# isso para nao dar nenhum erro ao manipular datas
df['data_compra'] = pd.to_datetime(df['data_compra'])
df['data_ida'] = pd.to_datetime(df['data_ida'])
df['data_volta'] = pd.to_datetime(df['data_volta'], errors='coerce')

df['mes_compra'] = df['data_compra'].dt.strftime('%Y-%m')
df['dia_semana_compra'] = df['data_compra'].dt.day_name()
df['usa_milhas'] = df['milhas_usadas'] > 0
df['passageiros_total'] = df['adultos'] + df['criancas']

# E aqui mapeamos os status para facilitar a leitura
# Lembrando que os status_id estão representados na aba BaseStatus
status_df = pd.read_excel(file_path, sheet_name='BaseStatus')
status_map = dict(zip(status_df['status_id'], status_df['status']))

df['status'] = df['status_id'].map(status_map)

# Agora mapeamos todos os voos para identificar se são do Mercosul ou não
# A lógica funciona assim: primeiro pegamos os aeroportos de origem e destino
# da tabela BaseAeroporto, depois concatenamos os códigos IATA
# e por fim verificamos se o par de aeroportos está na lista do Mercosul
aeroportos_df = pd.read_excel(file_path, sheet_name='BaseAeroporto')
aeroportos_df['iata'] = aeroportos_df['from_iata'] + aeroportos_df['to_iata']
mercosul_map = dict(zip(aeroportos_df['iata'], aeroportos_df['is_mercosul']))

df['iata'] = df['from_iata'] + df['to_iata']
df['is_mercosul'] = df['iata'].map(mercosul_map)

# Agrupando os dados por mês para análise de vendas
vendas_por_mes = df.groupby('mes_compra').agg({
    'id_itens': 'count',
    'valor_passagem': 'sum',
    'milhas_usadas': 'sum'
}).reset_index()
vendas_por_mes.columns = ['Mês', 'Quantidade de Vendas', 'Valor Total (R$)', 'Milhas Totais']

# Análise das vendas por mes
plt.figure(figsize=(14, 8))
ax = sns.barplot(x='Mês', y='Quantidade de Vendas', data=vendas_por_mes)
plt.title('Quantidade de Vendas por Mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade de Vendas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('vendas_por_mes.png', dpi=300)
plt.close()

# Analise do valor total de vendas por mês
plt.figure(figsize=(14, 8))
ax = sns.barplot(x='Mês', y='Valor Total (R$)', data=vendas_por_mes)
plt.title('Valor Total de Vendas por Mês (R$)')
plt.xlabel('Mês')
plt.ylabel('Valor Total (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('valor_por_mes.png', dpi=300)
plt.close()

# Analise de status das compras
status_counts = df['status'].value_counts()
plt.figure(figsize=(12, 8))
ax = sns.barplot(x=status_counts.index, y=status_counts.values)
plt.title('Distribuição de Status das Compras')
plt.xlabel('Status')
plt.ylabel('Quantidade')
plt.xticks(rotation=45, ha='right') 
plt.tight_layout()
plt.savefig('status_compras.png', dpi=300)
plt.close()

# rotas mais populares
top_routes = df.groupby(['from_iata', 'to_iata']).size().reset_index(name='count')
top_routes = top_routes.sort_values('count', ascending=False).head(10)
top_routes['rota'] = top_routes['from_iata'] + ' → ' + top_routes['to_iata']

plt.figure(figsize=(14, 8))
ax = sns.barplot(x='rota', y='count', data=top_routes)
plt.title('Top 10 Rotas Mais Populares')
plt.xlabel('Rota')
plt.ylabel('Quantidade de Vendas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('top_rotas.png', dpi=300)
plt.close()

# Análise de Uso de Milhas
milhas_usage = df['usa_milhas'].value_counts()
plt.figure(figsize=(10, 8))
plt.pie(milhas_usage, labels=['Sem Milhas', 'Com Milhas'], autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
plt.title('Proporção de Compras com e sem Uso de Milhas')
plt.axis('equal')
plt.tight_layout()
plt.savefig('uso_milhas.png', dpi=300)
plt.close()

# Análise de Receita Média por Compra (Métrica 1)
receita_media_mes = df.groupby('mes_compra')['valor_passagem'].mean().reset_index()
receita_media_mes.columns = ['Mês', 'Receita Média por Compra (R$)']

plt.figure(figsize=(14, 8))
ax = sns.lineplot(x='Mês', y='Receita Média por Compra (R$)', data=receita_media_mes, marker='o', linewidth=2)
plt.title('Receita Média por Compra ao Longo do Tempo')
plt.xlabel('Mês')
plt.ylabel('Receita Média (R$)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('receita_media.png', dpi=300)
plt.close()

# Análise de Milhas Médias Utilizadas por Compra
# Filtrar apenas compras com milhas
df_com_milhas = df[df['milhas_usadas'] > 0]
milhas_media_mes = df_com_milhas.groupby('mes_compra')['milhas_usadas'].mean().reset_index()
milhas_media_mes.columns = ['Mês', 'Milhas Médias por Compra']

plt.figure(figsize=(14, 8))
ax = sns.lineplot(x='Mês', y='Milhas Médias por Compra', data=milhas_media_mes, marker='o', linewidth=2)
plt.title('Milhas Médias Utilizadas por Compra ao Longo do Tempo')
plt.xlabel('Mês')
plt.ylabel('Milhas Médias')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('milhas_media.png', dpi=300)
plt.close()

#Análise de Tipo de Viagem
tipo_viagem_counts = df['tipo_viagem'].value_counts()
plt.figure(figsize=(10, 8))
plt.pie(tipo_viagem_counts, labels=tipo_viagem_counts.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
plt.title('Distribuição de Tipos de Viagem')
plt.axis('equal')
plt.tight_layout()
plt.savefig('tipo_viagem.png', dpi=300)
plt.close()

# Análise de Mercosul vs nao-mercosul
mercosul_counts = df['is_mercosul'].value_counts()
plt.figure(figsize=(10, 8))
plt.pie(mercosul_counts, labels=['Não-Mercosul', 'Mercosul'], autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff'])
plt.title('Proporção de Voos Mercosul vs Não-Mercosul')
plt.axis('equal')
plt.tight_layout()
plt.savefig('mercosul.png', dpi=300)
plt.close()

# Análise de Correlação entre Variáveis Numéricas
numeric_cols = ['valor_passagem', 'milhas_usadas', 'adultos', 'criancas', 'passageiros_total']
corr = df[numeric_cols].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Matriz de Correlação entre Variáveis Numéricas')
plt.tight_layout()
plt.savefig('correlacao.png', dpi=300)
plt.close()

# Salvar dados processados para caso precise usar depois
df.to_csv('dados_processados.csv', index=False)

# Gera as estatísticas
receita_media_geral = df['valor_passagem'].mean()
receita_media_por_status = df.groupby('status')['valor_passagem'].mean()
receita_media_por_tipo = df.groupby('tipo_viagem')['valor_passagem'].mean()

milhas_media_geral = df_com_milhas['milhas_usadas'].mean() if len(df_com_milhas) > 0 else 0
milhas_media_por_status = df_com_milhas.groupby('status')['milhas_usadas'].mean() if len(df_com_milhas) > 0 else pd.Series()
milhas_media_por_tipo = df_com_milhas.groupby('tipo_viagem')['milhas_usadas'].mean() if len(df_com_milhas) > 0 else pd.Series()

# escreve as estatísticas em um arquivo de texto
with open('estatisticas_metricas.txt', 'w') as f:
    f.write("ESTATÍSTICAS DAS MÉTRICAS PROPOSTAS\n\n")
    
    f.write("1. RECEITA MÉDIA POR COMPRA\n")
    f.write(f"Receita Média Geral: R$ {receita_media_geral:.2f}\n\n")
    
    f.write("Receita Média por Status:\n")
    for status, valor in receita_media_por_status.items():
        f.write(f"- {status}: R$ {valor:.2f}\n")
    f.write("\n")
    
    f.write("Receita Média por Tipo de Viagem:\n")
    for tipo, valor in receita_media_por_tipo.items():
        f.write(f"- {tipo}: R$ {valor:.2f}\n")
    f.write("\n")
    
    f.write("2. MILHAS MÉDIAS UTILIZADAS POR COMPRA\n")
    f.write(f"Milhas Médias Geral: {milhas_media_geral:.2f}\n\n")
    
    f.write("Milhas Médias por Status:\n")
    for status, valor in milhas_media_por_status.items():
        f.write(f"- {status}: {valor:.2f}\n")
    f.write("\n")
    
    f.write("Milhas Médias por Tipo de Viagem:\n")
    for tipo, valor in milhas_media_por_tipo.items():
        f.write(f"- {tipo}: {valor:.2f}\n")