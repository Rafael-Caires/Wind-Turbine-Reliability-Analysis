import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Carregar os resultados da análise de confiabilidade
with open("resultados_confiabilidade.txt", "r", encoding="cp1252") as arquivo:
    conteudo = arquivo.read()

# Dividir o conteúdo em blocos para cada Parque Eólico
blocos = conteudo.split("\n\n")

dados_confiabilidade = []

for bloco in blocos:
    if "--- Métricas de Confiabilidade Parque Eólico A ---" in bloco:
        nome_parque = "A"
    elif "--- Métricas de Confiabilidade Parque Eólico B ---" in bloco:
        nome_parque = "B"
    elif "--- Métricas de Confiabilidade Parque Eólico C ---" in bloco:
        nome_parque = "C"
    else:
        continue

    linhas_dados = bloco.strip().split("\n")[1:]  # Pula cabeçalho
    if linhas_dados and not linhas_dados[0].startswith("Empty DataFrame"):
        df = pd.read_csv(io.StringIO("\n".join(linhas_dados)), sep=r"\s+")
        df.columns = [col.strip() for col in df.columns]  # Remove espaços
        df["Parque_Eolico"] = nome_parque
        dados_confiabilidade.append(df)

# Concatenar todos os dados
df_confiabilidade = pd.concat(dados_confiabilidade, ignore_index=True)

# Verificar as colunas para debug
print("Colunas disponíveis:", df_confiabilidade.columns.tolist())

# Gráfico de barras para MTBF
plt.figure(figsize=(10, 6))
sns.barplot(x="Parque_Eolico", y="MTBF", data=df_confiabilidade)
plt.title("Tempo Médio Entre Falhas (MTBF) por Parque Eólico")
plt.ylabel("MTBF (horas)")
plt.xlabel("Parque Eólico")
plt.savefig("mtbf_barplot.png")
plt.close()

# Gráfico de barras para MTTR
plt.figure(figsize=(10, 6))
sns.barplot(x="Parque_Eolico", y="MTTR", data=df_confiabilidade)
plt.title("Tempo Médio Para Reparo (MTTR) por Parque Eólico")
plt.ylabel("MTTR (horas)")
plt.xlabel("Parque Eólico")
plt.savefig("mttr_barplot.png")
plt.close()

# Gráfico de barras para Disponibilidade
plt.figure(figsize=(10, 6))
sns.barplot(x="Parque_Eolico", y="Disponibilidade", data=df_confiabilidade)
plt.title("Disponibilidade por Parque Eólico")
plt.ylabel("Disponibilidade")
plt.xlabel("Parque Eólico")
plt.savefig("availability_barplot.png")
plt.close()

print("Visualizações geradas: mtbf_barplot.png, mttr_barplot.png, availability_barplot.png")

# Gráficos de séries temporais (mantém seu código original abaixo)

# Parque Eólico A - id_ativo 0
caminho_a = 'WIND FARM A/0.csv'
df_a = pd.read_csv(caminho_a, sep=';')
df_a["time_stamp"] = pd.to_datetime(df_a["time_stamp"])
df_a_ativo0 = df_a[df_a["asset_id"] == 0].copy()

plt.figure(figsize=(15, 7))
sns.lineplot(x="time_stamp", y="sensor_0_avg", data=df_a_ativo0)
plt.title("Média do Sensor 0 para o Ativo 0 (Parque Eólico A)")
plt.xlabel("Data e Hora")
plt.ylabel("Média do Sensor 0")
plt.savefig("wf_a_ativo0_sensor0_avg.png")
plt.close()

print("Gráfico de série temporal gerado: wf_a_ativo0_sensor0_avg.png")

# Parque Eólico B - id_ativo 13
caminho_b = 'WIND FARM B/2.csv'
df_b = pd.read_csv(caminho_b, sep=';')
df_b["time_stamp"] = pd.to_datetime(df_b["time_stamp"])
df_b_ativo13 = df_b[df_b["asset_id"] == 13].copy()

plt.figure(figsize=(15, 7))
sns.lineplot(x="time_stamp", y="sensor_0_avg", data=df_b_ativo13)
plt.title("Média do Sensor 0 para o Ativo 13 (Parque Eólico B)")
plt.xlabel("Data e Hora")
plt.ylabel("Média do Sensor 0")
plt.savefig("wf_b_ativo13_sensor0_avg.png")
plt.close()

print("Gráfico de série temporal gerado: wf_b_ativo13_sensor0_avg.png")
