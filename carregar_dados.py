import pandas as pd

# Caminhos dos arquivos
caminho_a = './WIND FARM A/0.csv'
caminho_b = './WIND FARM B/2.csv'
caminho_c = './WIND FARM C/1.csv'

caminho_evento_a = './WIND FARM A/event_info.csv'
caminho_evento_b = './WIND FARM B/event_info.csv'
caminho_evento_c = './WIND FARM C/event_info.csv'

# Carregar os datasets de exemplo
dataframe_a = pd.read_csv(caminho_a, sep=';')
dataframe_b = pd.read_csv(caminho_b, sep=';')
dataframe_c = pd.read_csv(caminho_c, sep=';')

# Carregar os arquivos de informações de eventos
dataframe_evento_a = pd.read_csv(caminho_evento_a, sep=';')
dataframe_evento_b = pd.read_csv(caminho_evento_b, sep=';')
dataframe_evento_c = pd.read_csv(caminho_evento_c, sep=';')

print('--- Parque Eólico A (0.csv) ---')
print(dataframe_a.head())
print(dataframe_a.info())
print('\n--- Parque Eólico B (2.csv) ---')
print(dataframe_b.head())
print(dataframe_b.info())
print('\n--- Parque Eólico C (1.csv) ---')
print(dataframe_c.head())
print(dataframe_c.info())

print('\n--- Informações de Eventos Parque Eólico A ---')
print(dataframe_evento_a.head())
print(dataframe_evento_a.info())
print('\n--- Informações de Eventos Parque Eólico B ---')
print(dataframe_evento_b.head())
print(dataframe_evento_b.info())
print('\n--- Informações de Eventos Parque Eólico C ---')
print(dataframe_evento_c.head())
print(dataframe_evento_c.info())

# Salvar informações para análise posterior
with open('saida_inspecao_dados.txt', 'w') as arquivo:
    arquivo.write('--- Parque Eólico A (0.csv) ---\n')
    arquivo.write(dataframe_a.head().to_string() + '\n')
    arquivo.write(str(dataframe_a.info()) + '\n')
    arquivo.write('\n--- Parque Eólico B (2.csv) ---\n')
    arquivo.write(dataframe_b.head().to_string() + '\n')
    arquivo.write(str(dataframe_b.info()) + '\n')
    arquivo.write('\n--- Parque Eólico C (1.csv) ---\n')
    arquivo.write(dataframe_c.head().to_string() + '\n')
    arquivo.write(str(dataframe_c.info()) + '\n')
    arquivo.write('\n--- Informações de Eventos Parque Eólico A ---\n')
    arquivo.write(dataframe_evento_a.head().to_string() + '\n')
    arquivo.write(str(dataframe_evento_a.info()) + '\n')
    arquivo.write('\n--- Informações de Eventos Parque Eólico B ---\n')
    arquivo.write(dataframe_evento_b.head().to_string() + '\n')
    arquivo.write(str(dataframe_evento_b.info()) + '\n')
    arquivo.write('\n--- Informações de Eventos Parque Eólico C ---\n')
    arquivo.write(dataframe_evento_c.head().to_string() + '\n')
    arquivo.write(str(dataframe_evento_c.info()) + '\n')


