import base64
import json

from app import app

cliente = app.test_client()


def test_pagina_inicial():
    assert cliente.get("/").status_code == 200


def test_busca_escapa_html():
    r = cliente.get("/busca?q=<script>alert(1)</script>")
    assert b"<script>" not in r.data


def test_saudacao_sem_injecao_de_template():
    r = cliente.get("/saudacao?nome={{7*7}}")
    assert b"49" not in r.data


def test_redirect_so_interno():
    r = cliente.get("/ir?url=https://site-malicioso.com")
    assert "site-malicioso" not in r.headers.get("Location", "")


def test_arquivo_sem_path_traversal():
    r = cliente.get("/arquivo?nome=../app.py")
    assert b"Flask" not in r.data


def b64(d):
    return base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")


def test_painel_recusa_token_sem_assinatura():
    falso = b64({"alg": "none"}) + "." + b64({"sub": "x", "papel": "admin"}) + "."
    r = cliente.get("/admin/painel", headers={"Authorization": "Bearer " + falso})
    assert b"admin" not in r.data
