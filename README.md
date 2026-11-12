
# PriceWatch RPA

Projeto acadêmico de automação de processos desenvolvido em Python para monitorar e comparar preços de produtos.

## Sobre o projeto

O PriceWatch RPA simula uma solução para a empresa fictícia TechVarejo, que precisa acompanhar os preços praticados por concorrentes.

O robô automatiza a leitura de produtos, consulta de preços, identificação de alertas e geração de relatórios.

**Os produtos e preços utilizados na demonstração são fictícios.**

## Tecnologias utilizadas

- Python
- Pandas e OpenPyXL
- API REST simulada com HTTP e JSON
- Requests
- BeautifulSoup
- Expressões regulares (Regex)
- SQLite
- Logging

## Funcionalidades

- Leitura de produtos cadastrados no Excel
- Validação de informações e identificadores
- Consulta de preços por API local
- Extração de preços de um catálogo HTML com BeautifulSoup
- Comparação de preços e geração de alertas
- Armazenamento do histórico em SQLite
- Registro de logs de execução
- Geração automática de relatórios Excel
- Tratamento de falhas de conexão e dados inválidos

## Como executar

### 1. Instalar as dependências

```bash
python -m pip install -r requirements.txt
```

### 2. Iniciar a API simulada

Em um terminal:

```bash
python api_simulada.py
```

### 3. Executar o monitoramento

Em outro terminal:

```bash
python planilha.py
```

O robô consultará os produtos da planilha `produtos_monitoramento.xlsx`, comparará os preços e registrará os resultados.

## Arquivos gerados

Após a execução, o projeto poderá gerar:

- `historico_precos.db`: histórico das consultas
- `pricewatch.log`: registros de execução
- `relatorio_monitoramento.xlsx`: relatório Excel com resultados

Esses arquivos não são versionados no Git.

## Observações

O projeto utiliza uma API e um catálogo HTML simulados para fins educacionais. Não realiza coleta de preços de lojas reais nem modifica anúncios comerciais.

## Contexto

Projeto desenvolvido para a disciplina de Automação Robótica de Processos (RPA).
