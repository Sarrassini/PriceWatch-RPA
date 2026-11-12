
import sqlite3
from pathlib import Path
from datetime import datetime


# Define o caminho do banco de dados
BANCO = Path(__file__).with_name("historico_precos.db")


# Cria a tabela caso ela ainda não exista
def criar_tabela():

    conexao = sqlite3.connect(BANCO)

    try:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS historico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sku TEXT NOT NULL,
                produto TEXT NOT NULL,
                id_concorrente TEXT NOT NULL,
                preco_proprio REAL NOT NULL,
                preco_concorrente REAL NOT NULL,
                diferenca REAL NOT NULL,
                situacao TEXT NOT NULL,
                data_consulta TEXT NOT NULL
            )
        """)

        conexao.commit()

    finally:
        conexao.close()


# Registra uma consulta no banco de dados
def registrar_consulta(
    sku,
    produto,
    id_concorrente,
    preco_proprio,
    preco_concorrente,
    diferenca,
    situacao
):

    conexao = sqlite3.connect(BANCO)

    try:
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        conexao.execute("""
            INSERT INTO historico (
                sku,
                produto,
                id_concorrente,
                preco_proprio,
                preco_concorrente,
                diferenca,
                situacao,
                data_consulta
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sku,
            produto,
            id_concorrente,
            preco_proprio,
            preco_concorrente,
            diferenca,
            situacao,
            data
        ))

        conexao.commit()

    finally:
        conexao.close()


# Permite visualizar as consultas armazenadas
def consultar_historico():

    conexao = sqlite3.connect(BANCO)

    try:
        registros = conexao.execute("""
            SELECT sku, produto, diferenca, situacao, data_consulta
            FROM historico
            ORDER BY id DESC
        """).fetchall()

        for registro in registros:
            print(registro)

    finally:
        conexao.close()


# Executa a consulta quando este arquivo é iniciado
if __name__ == "__main__":
    if BANCO.exists():
        consultar_historico()
    else:
        print("O banco de dados ainda não foi criado.")
