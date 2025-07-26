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

### É necessário:
- Converter colunas de data para o tipo datetime.
- Analisar a distribuição das variáveis numéricas e categóricas.
- Identificar tendências e padrões nos dados.
