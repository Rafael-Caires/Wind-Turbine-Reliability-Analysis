import pandas as pd

# Caminhos dos arquivos
caminho_a = 'WIND FARM A/0.csv'
caminho_b = 'WIND FARM B/2.csv'
caminho_c = 'WIND FARM C/1.csv'

caminho_evento_a = 'WIND FARM A/event_info.csv'
caminho_evento_b = 'WIND FARM B/event_info.csv'
caminho_evento_c = 'WIND FARM C/event_info.csv'

# Carregar os arquivos de informações de eventos
df_evento_a = pd.read_csv(caminho_evento_a, sep=';')
df_evento_b = pd.read_csv(caminho_evento_b, sep=';')
df_evento_c = pd.read_csv(caminho_evento_c, sep=';')

# Função para pré-processar os dados de eventos
def pre_processar_dados_evento(df_evento):
    df_evento['event_start'] = pd.to_datetime(df_evento['event_start'], format='%d.%m.%Y %H:%M')
    df_evento['event_end'] = pd.to_datetime(df_evento['event_end'], format='%d.%m.%Y %H:%M')

    # Renomear diferentes possibilidades para 'id_ativo'
    if 'asset' in df_evento.columns:
        df_evento = df_evento.rename(columns={'asset': 'id_ativo'})
    elif 'asset_id' in df_evento.columns:
        df_evento = df_evento.rename(columns={'asset_id': 'id_ativo'})
    elif 'id' in df_evento.columns:
        df_evento = df_evento.rename(columns={'id': 'id_ativo'})

    if 'id_ativo' not in df_evento.columns:
        raise ValueError("Coluna de identificação do ativo não encontrada em event_info.csv")

    return df_evento

df_evento_a_processado = pre_processar_dados_evento(df_evento_a.copy())
df_evento_b_processado = pre_processar_dados_evento(df_evento_b.copy())
df_evento_c_processado = pre_processar_dados_evento(df_evento_c.copy())

# Função para calcular MTBF, MTTR e Disponibilidade para um id_ativo processado
def calcular_metricas_confiabilidade_para_ativo(df_ativo_processado):
    tempos_operacao = []
    tempos_parada = []
    num_falhas = 0

    tempo_operacao_atual = 0
    tempo_parada_atual = 0

    for i, linha in df_ativo_processado.iterrows():
        if linha['e_falha'] == False:
            tempo_operacao_atual += linha['diferenca_tempo']
            if tempo_parada_atual > 0:
                tempos_parada.append(tempo_parada_atual)
                tempo_parada_atual = 0
        else:
            tempo_parada_atual += linha['diferenca_tempo']
            if tempo_operacao_atual > 0:
                tempos_operacao.append(tempo_operacao_atual)
                num_falhas += 1
                tempo_operacao_atual = 0

    if tempo_operacao_atual > 0:
        tempos_operacao.append(tempo_operacao_atual)
    if tempo_parada_atual > 0:
        tempos_parada.append(tempo_parada_atual)

    mtbf = sum(tempos_operacao) / num_falhas if num_falhas > 0 else float('inf')
    mttr = sum(tempos_parada) / num_falhas if num_falhas > 0 else 0
    disponibilidade = mtbf / (mtbf + mttr) if (mtbf + mttr) > 0 else 0

    return {
        'id_ativo': df_ativo_processado['id_ativo'].iloc[0],
        'MTBF': mtbf,
        'MTTR': mttr,
        'Disponibilidade': disponibilidade,
        'Num_Falhas': num_falhas
    }

# Processar e calcular métricas para cada Parque Eólico
def processar_parque_eolico_otimizado(caminho_dados, df_evento_processado):
    todos_dados_confiabilidade = []

    df_completo = pd.read_csv(caminho_dados, sep=';')

    # Padronizar coluna de identificação do ativo
    if 'asset_id' in df_completo.columns:
        df_completo = df_completo.rename(columns={'asset_id': 'id_ativo'})
    elif 'id' in df_completo.columns:
        df_completo = df_completo.rename(columns={'id': 'id_ativo'})

    if 'id_ativo' not in df_completo.columns:
        raise ValueError("Coluna 'id_ativo' não encontrada no arquivo: " + caminho_dados)

    ids_ativos_unicos = df_evento_processado['id_ativo'].unique() if 'WIND FARM C' in caminho_dados else df_completo['id_ativo'].unique()

    for id_ativo in ids_ativos_unicos:
        dados_ativo = df_completo[df_completo['id_ativo'] == id_ativo].copy()

        if not dados_ativo.empty:
            dados_ativo['time_stamp'] = pd.to_datetime(dados_ativo['time_stamp'])
            dados_ativo = dados_ativo.sort_values(by='time_stamp')

            dados_ativo['e_falha'] = False
            eventos_ativo = df_evento_processado[df_evento_processado['id_ativo'] == id_ativo]

            for _, linha in eventos_ativo.iterrows():
                if linha['event_label'] == 'anomaly':
                    tempo_inicio = linha['event_start']
                    tempo_fim = linha['event_end']
                    dados_ativo.loc[
                        (dados_ativo['time_stamp'] >= tempo_inicio) &
                        (dados_ativo['time_stamp'] <= tempo_fim),
                        'e_falha'
                    ] = True

            dados_ativo['diferenca_tempo'] = dados_ativo['time_stamp'].diff().dt.total_seconds() / 3600
            dados_ativo['diferenca_tempo'] = dados_ativo['diferenca_tempo'].fillna(0)

            metricas_confiabilidade = calcular_metricas_confiabilidade_para_ativo(dados_ativo)
            todos_dados_confiabilidade.append(metricas_confiabilidade)

    return pd.DataFrame(todos_dados_confiabilidade)

# Executar para cada Parque Eólico
confiabilidade_a = processar_parque_eolico_otimizado(caminho_a, df_evento_a_processado)
confiabilidade_b = processar_parque_eolico_otimizado(caminho_b, df_evento_b_processado)
confiabilidade_c = processar_parque_eolico_otimizado(caminho_c, df_evento_c_processado)

# Salvar resultados
with open('resultados_confiabilidade.txt', 'w') as arquivo:
    arquivo.write('--- Métricas de Confiabilidade Parque Eólico A ---\n')
    arquivo.write(confiabilidade_a.to_string(index=False) + '\n\n')
    arquivo.write('--- Métricas de Confiabilidade Parque Eólico B ---\n')
    arquivo.write(confiabilidade_b.to_string(index=False) + '\n\n')
    arquivo.write('--- Métricas de Confiabilidade Parque Eólico C ---\n')
    arquivo.write(confiabilidade_c.to_string(index=False) + '\n\n')

print('Análise de confiabilidade concluída. Verifique resultados_confiabilidade.txt para detalhes.')
