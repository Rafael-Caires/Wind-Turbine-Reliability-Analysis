import pandas as pd
import os
from collections import defaultdict

# Caminhos
data_folder = "../WIND FARM C/datasets"
event_info_path = "../WIND FARM C/event_info.csv"

# Lê o arquivo de eventos
event_info = pd.read_csv(event_info_path, sep=';', parse_dates=['event_start', 'event_end'], dayfirst=True)

# --------- PARTE 1: Tempo de operação por asset (com merge de intervalos) ---------

# Coleta intervalos de tempo de cada dataset
asset_intervals = defaultdict(list)
for _, row in event_info.iterrows():
    asset_id = row['asset_id']
    event_id = row['event_id']
    filename = f"{asset_id}_{event_id}.csv"
    filepath = os.path.join(data_folder, filename)
    if not os.path.isfile(filepath):
        continue
    df = pd.read_csv(filepath, sep=';', usecols=[0])
    if df.empty:
        continue
    start = pd.to_datetime(df.iloc[0, 0])
    end = pd.to_datetime(df.iloc[-1, 0])
    asset_intervals[asset_id].append((start, end))

# Função para unir intervalos sobrepostos
def merge_intervals(intervals):
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    for current in sorted_intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            merged[-1] = (last[0], max(last[1], current[1]))
        else:
            merged.append(current)
    return merged

# Tempo total de operação por asset
operating_summary = []
for asset_id, intervals in asset_intervals.items():
    merged = merge_intervals(intervals)
    total_hours = sum([(end - start).total_seconds() / 3600 for start, end in merged])
    operating_summary.append({'asset_id': asset_id, 'total_operating_hours': round(total_hours, 2)})

df_operating = pd.DataFrame(operating_summary)

# --------- PARTE 2: Tempo de falha e contagem de falhas por asset ---------

all_assets = event_info['asset_id'].unique()
df_anomalies = event_info[event_info['event_label'] == 'anomaly'].copy()
df_anomalies['downtime'] = (df_anomalies['event_end'] - df_anomalies['event_start']).dt.total_seconds() / 3600

# Agrega falhas e downtime
failure_summary = df_anomalies.groupby('asset_id').agg(
    total_anomalies=('event_id', 'count'),
    total_downtime_hours=('downtime', 'sum')
).reset_index()

# Garante todos os assets no resumo
df_failure = pd.DataFrame({'asset_id': all_assets})
df_failure = df_failure.merge(failure_summary, on='asset_id', how='left').fillna(0)
df_failure['total_anomalies'] = df_failure['total_anomalies'].astype(int)
df_failure['total_downtime_hours'] = df_failure['total_downtime_hours'].round(2)

# --------- PARTE 3: Unificação e cálculo de métricas ---------

# Junta tempo de operação com falhas
df_result = df_operating.merge(df_failure, on='asset_id', how='outer').fillna(0)

# Cálculo das métricas
df_result['MTBF'] = df_result.apply(
    lambda row: row['total_operating_hours'] / row['total_anomalies'] if row['total_anomalies'] > 0 else 0, axis=1
)
df_result['MTTR'] = df_result.apply(
    lambda row: row['total_downtime_hours'] / row['total_anomalies'] if row['total_anomalies'] > 0 else 0, axis=1
)
df_result['Disponibilidade'] = df_result.apply(
    lambda row: row['total_operating_hours'] / (row['total_operating_hours'] + row['total_downtime_hours']) 
    if (row['total_operating_hours'] + row['total_downtime_hours']) > 0 else 0, axis=1
)

# Arredonda as métricas
df_result['MTBF'] = df_result['MTBF'].round(2)
df_result['MTTR'] = df_result['MTTR'].round(2)
df_result['Disponibilidade'] = df_result['Disponibilidade'].round(4)

# Salva resultado final
output_path = "confiabilidade_por_asset_FarmC.csv"
df_result.to_csv(output_path, sep=';', index=False)

output_path
