
import pandas as pd
import re
import logging

from pathlib import Path
from decimal import Decimal

from consulta_preco import consultar_preco
from banco import criar_tabela, registrar_consulta
from relatorio import gerar_relatorio


# Define os caminhos dos arquivos
PASTA = Path(__file__).parent
ARQUIVO_EXCEL = PASTA / "produtos_monitoramento.xlsx"
ARQUIVO_LOG = PASTA / "pricewatch.log"


# Configura os logs do robô
logging.basicConfig(
    filename=ARQUIVO_LOG,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    encoding="utf-8"
)


# Valida as informações dos produtos
def validar_produto(produto):

    sku = str(produto["SKU"]).strip()
    id_concorrente = str(produto["ID Concorrente"]).strip().upper()
    preco = pd.to_numeric(produto["Preço Próprio"], errors="coerce")
    limite = pd.to_numeric(produto["Limite Alerta (%)"], errors="coerce")
    ativo = str(produto["Ativo"]).strip().upper()

    # Valida o SKU
    if not re.fullmatch(r"[A-Z]{3}-\d{3}", sku):
        print(f"{sku}: SKU inválido!")
        logging.error(f"{sku}: SKU inválido.")
        return False

    # Valida o ID do concorrente
    if not re.fullmatch(r"CONC-\d{3}", id_concorrente):
        print(f"{sku}: ID do concorrente inválido!")
        logging.error(f"{sku}: ID do concorrente inválido.")
        return False

    # Valida o preço próprio
    if pd.isna(preco) or preco <= 0:
        print(f"{sku}: Preço próprio inválido!")
        logging.error(f"{sku}: Preço próprio inválido.")
        return False

    # Valida o limite de alerta
    if pd.isna(limite) or limite <= 0 or limite > 100:
        print(f"{sku}: Limite de alerta inválido!")
        logging.error(f"{sku}: Limite de alerta inválido.")
        return False

    # Valida o campo Ativo
    if ativo not in ["SIM", "NÃO"]:
        print(f"{sku}: Campo Ativo inválido!")
        logging.error(f"{sku}: Campo Ativo inválido.")
        return False

    # Ignora produtos desativados
    if ativo == "NÃO":
        print(f"{sku}: Produto desativado.")
        logging.info(f"{sku}: Produto desativado.")
        return False

    logging.info(f"{sku}: Produto validado.")
    return True


# Consulta e compara os preços
def comparar_precos(produto):

    sku = str(produto["SKU"]).strip()
    nome = str(produto["Produto"]).strip()
    id_concorrente = str(produto["ID Concorrente"]).strip().upper()

    preco_proprio = Decimal(str(produto["Preço Próprio"]))
    limite = Decimal(str(produto["Limite Alerta (%)"]))

    # Consulta a API e o catálogo HTML
    logging.info(f"{sku}: Iniciando consulta ao concorrente.")

    preco_concorrente = consultar_preco(id_concorrente)

    if preco_concorrente is None:
        print(f"{sku}: Não foi possível comparar os preços.")
        logging.error(f"{sku}: Falha na consulta de preços.")
        return

    logging.info(f"{sku}: Consulta realizada com sucesso.")

    # Calcula a diferença percentual
    diferenca = (
        (preco_proprio - preco_concorrente)
        / preco_proprio
    ) * 100

    print(f"\nSKU: {sku}")
    print(f"Preço próprio: R$ {preco_proprio:.2f}".replace(".", ","))
    print(f"Preço concorrente: R$ {preco_concorrente:.2f}".replace(".", ","))
    print(f"Diferença: {diferenca:.2f}%")

    # Verifica se é necessário gerar alerta
    if diferenca >= limite:
        situacao = "ALERTA"
        print("ALERTA: Concorrente com preço significativamente menor!")
        logging.warning(f"{sku}: Alerta de preço identificado.")

    else:
        situacao = "OK"
        print("OK: Nenhum alerta necessário.")
        logging.info(f"{sku}: Preço dentro do limite estabelecido.")

    # Registra o resultado no SQLite
    registrar_consulta(
        sku=sku,
        produto=nome,
        id_concorrente=id_concorrente,
        preco_proprio=float(preco_proprio),
        preco_concorrente=float(preco_concorrente),
        diferenca=round(float(diferenca), 2),
        situacao=situacao
    )

    print("Consulta registrada no banco de dados!")
    logging.info(f"{sku}: Resultado registrado no SQLite.")


# Execução principal do robô
try:
    logging.info("Monitoramento iniciado.")

    # Prepara o banco SQLite
    criar_tabela()
    logging.info("Banco SQLite preparado.")

    # Lê a planilha Excel
    produtos = pd.read_excel(
        ARQUIVO_EXCEL,
        sheet_name="Produtos"
    )

    logging.info("Planilha Excel carregada com sucesso.")

    print("Iniciando monitoramento de preços...\n")

    # Percorre os produtos cadastrados
    for indice, produto in produtos.iterrows():

        try:
            if validar_produto(produto):
                comparar_precos(produto)

        except Exception:
            print(f"Erro ao processar a linha {indice + 2}.")
            logging.exception(
                f"Falha ao processar a linha {indice + 2}."
            )

        print("=" * 45)

    print("\nMonitoramento finalizado!")
    logging.info("Monitoramento finalizado.")

    # Gera automaticamente o relatório Excel
    print("\nGerando relatório Excel...")
    logging.info("Iniciando geração do relatório.")

    gerar_relatorio()

    logging.info("Rotina de geração do relatório encerrada.")

except Exception:
    print("Erro geral durante o monitoramento.")
    logging.exception("Falha geral durante o monitoramento.")
