import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Lê o arquivo CSV
df = pd.read_csv('confiabilidade_por_asset_FarmA.csv', sep=';')

# Filtra valores não nulos e diferentes de zero
df_mtbf = df[df['MTBF'] > 0]
df_mttr = df[df['MTTR'] > 0]

# Estilo
sns.set_theme(style="whitegrid")

# Cria a figura com dois subplots lado a lado
plt.figure(figsize=(5, 8))

# Histograma MTBF
plt.subplot(2, 1, 1)
sns.histplot(df_mtbf['MTBF'], bins=5, kde=True, color='skyblue')
plt.title('Histograma do MTBF Parque A (ativos com falha)')
plt.xlabel('MTBF (horas)')
plt.ylabel('Frequência')

# Histograma MTTR
plt.subplot(2, 1, 2)
sns.histplot(df_mttr['MTTR'], bins=5, kde=True, color='salmon')
plt.title('Histograma do MTTR Parque A (ativos com falha)')
plt.xlabel('MTTR (horas)')
plt.ylabel('Frequência')

# Layout final
plt.tight_layout()
plt.show()
