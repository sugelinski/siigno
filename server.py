"""Servidor local do "Descubra seu signo" — usa apenas a biblioteca padrão do Python.

Uso:  python server.py   ->   http://localhost:8000
"""
import json
import sqlite3
from datetime import datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

BASE = Path(__file__).parent
DB_PATH = BASE / "database" / "signos.db"
PORT = 8000


def registrar_consulta(con, data_iso: str, signo_id: int, ip: str):
    """Grava no banco a data de nascimento informada, o signo e o momento da consulta."""
    con.execute(
        """CREATE TABLE IF NOT EXISTS consultas (
               id              INTEGER PRIMARY KEY AUTOINCREMENT,
               data_nascimento TEXT NOT NULL,
               signo_id        INTEGER NOT NULL REFERENCES signos(id),
               consultado_em   TEXT NOT NULL DEFAULT (datetime('now','localtime')),
               ip              TEXT
           )"""
    )
    con.execute(
        "INSERT INTO consultas (data_nascimento, signo_id, ip) VALUES (?,?,?)",
        (data_iso, signo_id, ip),
    )
    con.commit()


def buscar_signo(data_iso: str, ip: str = ""):
    """Recebe 'AAAA-MM-DD' e devolve o signo correspondente (dict) ou None."""
    d = datetime.strptime(data_iso, "%Y-%m-%d")
    md = d.month * 100 + d.day
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    # Capricórnio atravessa o ano (inicio_md > fim_md), por isso o segundo ramo.
    row = con.execute(
        """SELECT * FROM signos
           WHERE (inicio_md <= fim_md AND ? BETWEEN inicio_md AND fim_md)
              OR (inicio_md >  fim_md AND (? >= inicio_md OR ? <= fim_md))""",
        (md, md, md),
    ).fetchone()
    if row:
        try:
            registrar_consulta(con, data_iso, row["id"], ip)
        except sqlite3.Error:
            pass  # falha ao registrar não deve impedir a resposta
    con.close()
    return dict(row) if row else None


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE), **kwargs)

    def _json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/signo":
            data = parse_qs(url.query).get("data", [""])[0]
            try:
                signo = buscar_signo(data, self.client_address[0])
            except ValueError:
                return self._json(400, {"erro": "Data inválida. Use o formato AAAA-MM-DD."})
            if not signo:
                return self._json(404, {"erro": "Signo não encontrado."})
            return self._json(200, signo)
        # Não expõe o arquivo do banco nem o código do servidor
        if url.path.startswith("/database") or url.path.endswith(".py"):
            return self.send_error(404)
        return super().do_GET()


if __name__ == "__main__":
    if not DB_PATH.exists():
        raise SystemExit("Banco não encontrado. Rode antes: python database/init_db.py")
    print(f"Servidor rodando em http://localhost:{PORT}  (Ctrl+C para parar)")
    ThreadingHTTPServer(("", PORT), Handler).serve_forever()
