
import re
import requests

from pathlib import Path
from decimal import Decimal
from bs4 import BeautifulSoup


# Endereço da API fictícia
URL_API = "http://127.0.0.1:8000"

# Caminho do catálogo HTML
ARQUIVO_HTML = Path(__file__).with_name("catalogo.html")


# Consulta os preços de um produto concorrente
def consultar_preco(id_concorrente):

    # Padroniza o identificador
    id_concorrente = str(id_concorrente).strip().upper()

    # Valida o formato com Regex
    if not re.fullmatch(r"CONC-\d{3}", id_concorrente):
        print(f"{id_concorrente}: ID inválido!")
        return None

    try:
        # Consulta o produto na API fictícia
        resposta = requests.get(
            f"{URL_API}/precos/{id_concorrente}",
            timeout=10
        )

        # Verifica se a consulta foi bem-sucedida
        if resposta.status_code != 200:
            print(f"Erro na API: HTTP {resposta.status_code}")
            return None

        dados_api = resposta.json()

        # Abre e interpreta o arquivo HTML
        with open(ARQUIVO_HTML, "r", encoding="utf-8") as arquivo:
            html = arquivo.read()

        soup = BeautifulSoup(html, "html.parser")

        # Localiza o produto pelo identificador
        produto = soup.select_one(
            f'div.produto[data-id="{id_concorrente}"]'
        )

        if produto is None:
            print(f"{id_concorrente}: Produto não encontrado no HTML!")
            return None

        # Extrai o preço com BeautifulSoup
        elemento_preco = produto.select_one("p.preco")

        if elemento_preco is None:
            print(f"{id_concorrente}: Preço não encontrado!")
            return None

        texto_preco = elemento_preco.get_text(strip=True)

        # Converte "R$ 74,90" em um valor numérico
        preco_html = Decimal(
            texto_preco.replace("R$", "")
            .strip()
            .replace(".", "")
            .replace(",", ".")
        )

        preco_api = Decimal(str(dados_api["preco"]))

        # Exibe o resultado das consultas
        print(f"Produto: {dados_api['produto']}")
        print(f"Preço API: R$ {preco_api:.2f}".replace(".", ","))
        print(f"Preço HTML: R$ {preco_html:.2f}".replace(".", ","))

        # Compara os valores obtidos
        if preco_api != preco_html:
            print("Alerta: Os preços da API e do HTML são diferentes!")
            return None

        print("Consulta realizada com sucesso!")

        return preco_html

    except (requests.RequestException, OSError, ValueError, KeyError) as erro:
        print(f"Erro durante a consulta: {erro}")
        return None


# Executa um teste com o primeiro produto
if __name__ == "__main__":
    consultar_preco("CONC-001")
