
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


# Produtos e preços fictícios dos concorrentes
produtos = {
    "CONC-001": {
        "produto": "Mouse Logitech M170",
        "preco": 74.90,
        "moeda": "BRL"
    },
    "CONC-002": {
        "produto": "Teclado Logitech K120",
        "preco": 105.90,
        "moeda": "BRL"
    },
    "CONC-003": {
        "produto": "SSD Kingston 480GB",
        "preco": 219.90,
        "moeda": "BRL"
    },
    "CONC-004": {
        "produto": "Webcam Logitech C270",
        "preco": 109.90,
        "moeda": "BRL"
    },
    "CONC-005": {
        "produto": "Headset Havit H2002D",
        "preco": 169.90,
        "moeda": "BRL"
    },
    "CONC-006": {
        "produto": "Monitor LG 24 polegadas",
        "preco": 649.90,
        "moeda": "BRL"
    }
}


# Classe responsável por responder às consultas
class APIProdutos(BaseHTTPRequestHandler):

    def do_GET(self):

        if not self.path.startswith("/precos/"):
            self.enviar_resposta(
                {"erro": "Rota não encontrada"},
                404
            )
            return

        id_produto = self.path.split("/precos/")[1].split("?")[0]

        produto = produtos.get(id_produto)

        if produto is None:
            self.enviar_resposta(
                {"erro": "Produto não encontrado"},
                404
            )
            return

        self.enviar_resposta(
            {"id": id_produto, **produto},
            200
        )

    # Envia os dados no formato JSON
    def enviar_resposta(self, dados, status):

        resposta = json.dumps(dados).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header("Content-Length", str(len(resposta)))
        self.end_headers()

        self.wfile.write(resposta)


# Inicializa a API local
servidor = HTTPServer(("127.0.0.1", 8000), APIProdutos)

print("API fictícia iniciada!")
print("Endereço: http://127.0.0.1:8000")
print("Produtos disponíveis: 6")
print("Pressione Ctrl + C para encerrar.")

servidor.serve_forever()
