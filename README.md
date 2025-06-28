# Análise de Confiabilidade de Sistemas de Parques Eólicos

Este projeto realiza a análise de confiabilidade, manutenibilidade e disponibilidade (Reliability, Maintainability, and Availability - RMA) de componentes de três parques eólicos (Parque A, B e C). Os scripts em Python processam dados históricos de operação e falha para calcular métricas essenciais como Tempo Médio Até a Falha (MTTF), Tempo Médio Para Reparo (MTTR) e Disponibilidade Operacional.

## 📂 Estrutura do Projeto

O repositório está organizado da seguinte forma:

```
.
├── WIND FARM A/
│   └── (Arquivos de dados do Parque A)
├── WIND FARM B/
│   └── (Arquivos de dados do Parque B)
├── WIND FARM C/
│   └── (Arquivos de dados do Parque C)
│
├── analise_confiabilidade.py   # Script principal que realiza os cálculos
├── carregar_dados.py           # Script para carregar e pré-processar os dados
├── gerar_visualizacoes.py      # Script que cria os gráficos e plots
│
├── resultados_confiabilidade.txt # Saída com os resultados numéricos da análise
├── saida_inspecao_dados.txt    # Arquivo de log ou inspeção inicial dos dados
│
├── availability_barplot.png    # Gráfico com a disponibilidade por parque
├── mttf_barplot.png            # Gráfico com o MTTF por parque
└── mttr_barplot.png            # Gráfico com o MTTR por parque
```

## ❗ Dados do Projeto

**Importante:** Os arquivos de dados brutos (em formato Excel), necessários para a execução da análise, são muito grandes e não foram incluídos neste repositório do GitHub.

Para executar os scripts, você precisa fazer o download dos dados separadamente através do link abaixo e colocar os arquivos nas suas respectivas pastas (`WIND FARM A`, `WIND FARM B`, `WIND FARM C`).

➡️ **Faça o download dos dados aqui:https://drive.google.com/drive/folders/1U3_ulgmNl2MxuH0QgOcmdNNVRODkbgeN?usp=sharing

## 🚀 Como Executar

1.  **Clone o repositório:**

2.  **Baixe e organize os dados:**
    * Faça o download dos arquivos de dados a partir do link do Google Drive fornecido acima.
    * Descompacte e mova os arquivos para as pastas correspondentes (`WIND FARM A/`, `WIND FARM B/`, `WIND FARM C/`).

3.  **Instale as dependências:**

4.  **Execute a análise:**
    Execute os scripts na ordem apropriada para carregar os dados, processá-los e gerar as visualizações.
    ```bash
    python carregar_dados.py
    python analise_confiabilidade.py
    python gerar_visualizacoes.py
    ```

## 📊 Resultados

Os resultados numéricos da análise de confiabilidade são salvos no arquivo `resultados_confiabilidade.txt`.

As visualizações, como os gráficos de barras para Disponibilidade, MTTF e MTTR, são salvas como arquivos `.png` no diretório principal do projeto.
