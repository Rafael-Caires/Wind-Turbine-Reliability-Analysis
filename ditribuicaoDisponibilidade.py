import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Leitura dos arquivos CSV com separador ";"
df1 = pd.read_csv('confiabilidade_por_asset_FarmA.csv', sep=';')
df2 = pd.read_csv('confiabilidade_por_asset_FarmB.csv', sep=';')
df3 = pd.read_csv('confiabilidade_por_asset_FarmC.csv', sep=';')

# Adiciona coluna de identificação da origem dos dados
df1['Parque'] = 'Parque A'
df2['Parque'] = 'Parque B'
df3['Parque'] = 'Parque C'

# Concatena os dados
df_total = pd.concat([df1, df2, df3], ignore_index=True)

# Configurações de estilo
sns.set_theme(style="whitegrid")

# Cria o boxplot
plt.figure(figsize=(8, 6))
ax = sns.boxplot(data=df_total, x='Parque', y='Disponibilidade', palette='pastel')

# Calcula média e mediana
estatisticas = df_total.groupby('Parque')['Disponibilidade'].agg(['mean', 'median']).reset_index()

# Adiciona textos da média e mediana
for i, row in estatisticas.iterrows():
    plt.text(i, row['median'] - 0.005, f"Mediana: {row['median']:.4f}", 
             ha='center', va='top', fontsize=9, color='black')

# Título e eixos
plt.title('Distribuição da Disponibilidade por Parque')
plt.xlabel('Parque Eólico')
plt.ylabel('Disponibilidade')
plt.legend()

# Exibe
plt.tight_layout()
plt.show()