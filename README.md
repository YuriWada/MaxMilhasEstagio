# Programa de Estágio da MaxMilhas

## Dependências

Para rodar as análises, é necessário instalar as seguintes bibliotecas Python:

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

## Resumo da Análise Exploratória de Dados

### Visão Geral do Dataset
O dataset contém 2000 entradas e 12 colunas.

### Colunas e Tipos de Dados:
A descrição de cada coluna e tipos de dados está em
"Dicionário de dados + DER" do arquivo principal.

### Valores Ausentes:
- Apenas a coluna `data_volta` possui valores ausentes (1144), e é consistente com o `tipo_viagem` 'Somente ida'.

### Estatísticas Descritivas:
- `valor_passagem`: Varia de 100.0 a 10000.0, com média de 1000.0 e desvio padrão de 999.99.
- `milhas_usadas`: Varia de 0 a 100000, com média de 10000.0 e desvio padrão de 9999.99.
- `adultos`: Varia de 1 a 7, com média de 1.4.
- `criancas`: Varia de 0 a 3, com média de 0.072.

### Valores Únicos em Colunas Categóricas:
- `from_iata`: 10 aeroportos de origem únicos, com GIG sendo o mais frequente (1186 ocorrências).
- `to_iata`: 14 aeroportos de destino únicos, com GIG (601) e LIS (378) sendo os mais frequentes.
- `tipo_viagem`: 'Somente ida' (1143) e 'Ida e volta' (857).

### É necessário:
- Converter colunas de data para o tipo datetime.
- Investigar o significado dos `status_id`.
- Analisar a distribuição das variáveis numéricas e categóricas.
- Identificar tendências e padrões nos dados.
