
import sqlite3
import pandas as pd

from pathlib import Path


# Define os caminhos dos arquivos
PASTA = Path(__file__).parent
BANCO = PASTA / "historico_precos.db"
RELATORIO = PASTA / "relatorio_monitoramento.xlsx"


# Função responsável por gerar o relatório Excel
def gerar_relatorio():

    # Verifica se o banco de dados existe
    if not BANCO.exists():
        print("Erro: Banco de dados não encontrado!")
        return

    try:
        # Conecta ao banco SQLite
        with sqlite3.connect(BANCO) as conexao:

            # Consulta todos os registros do histórico
            historico = pd.read_sql_query("""
                SELECT
                    id,
                    sku AS "SKU",
                    produto AS "Produto",
                    id_concorrente AS "ID Concorrente",
                    preco_proprio AS "Preço Próprio",
                    preco_concorrente AS "Preço Concorrente",
                    diferenca AS "Diferença (%)",
                    situacao AS "Situação",
                    data_consulta AS "Data da Consulta"
                FROM historico
                ORDER BY id
            """, conexao)

        # Verifica se existem registros no banco
        if historico.empty:
            print("Nenhuma consulta encontrada no histórico.")
            return

        # Obtém o registro mais recente de cada produto
        ultimas_consultas = historico.drop_duplicates(
            subset="SKU",
            keep="last"
        ).sort_values("SKU")

        # Calcula um resumo das últimas consultas
        total = len(ultimas_consultas)

        alertas = (
            ultimas_consultas["Situação"] == "ALERTA"
        ).sum()

        resumo = pd.DataFrame({
            "Indicador": [
                "Produtos monitorados",
                "Produtos em alerta",
                "Produtos sem alerta"
            ],
            "Quantidade": [
                total,
                int(alertas),
                int(total - alertas)
            ]
        })

        # Cria o arquivo Excel com três abas
        with pd.ExcelWriter(RELATORIO, engine="openpyxl") as excel:

            ultimas_consultas.drop(
                columns="id"
            ).to_excel(
                excel,
                sheet_name="Ultimas Consultas",
                index=False
            )

            historico.drop(
                columns="id"
            ).to_excel(
                excel,
                sheet_name="Historico",
                index=False
            )

            resumo.to_excel(
                excel,
                sheet_name="Resumo",
                index=False
            )

            # Ajusta a largura das colunas
            for aba in excel.sheets.values():

                aba.freeze_panes = "A2"
                aba.auto_filter.ref = aba.dimensions

                for coluna in aba.columns:

                    tamanho = max(
                        len(str(celula.value or ""))
                        for celula in coluna
                    )

                    aba.column_dimensions[
                        coluna[0].column_letter
                    ].width = min(tamanho + 3, 45)

        print("Relatório Excel gerado com sucesso!")
        print(f"Arquivo: {RELATORIO.name}")

    except Exception as erro:
        print(f"Erro ao gerar relatório: {erro}")


# Executa a geração do relatório
if __name__ == "__main__":
    gerar_relatorio()
