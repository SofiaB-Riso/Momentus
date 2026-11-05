"""Proteções HTTP e configuração da instalação; sem regras do domínio."""

import hmac
import os
from hashlib import sha256
from hmac import compare_digest
from pathlib import Path
from secrets import token_urlsafe
from tempfile import NamedTemporaryFile
from threading import Lock
from time import monotonic
from urllib.parse import urlsplit

from flask import current_app, jsonify, request, session


def token_csrf(criar=False):
    identidade = session.get("usuario_identidade")
    if not identidade:
        if criar:
            session.setdefault("csrf_nonce", token_urlsafe(32))
        identidade = session.get("csrf_nonce")
    if not identidade:
        return ""
    dados = f"csrf:{session.get('usuario_id', 'anonimo')}:{identidade}"
    return hmac.new(
        current_app.secret_key.encode(), dados.encode(), "sha256"
    ).hexdigest()


def segredo_instalacao(pasta):
    """Mantém sessões entre reinícios locais sem distribuir um segredo no ZIP."""
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = pasta / ".session-secret"
    if not arquivo.exists():
        with NamedTemporaryFile(
            mode="w", dir=pasta, prefix=".session-", delete=False
        ) as stream:
            temporario = Path(stream.name)
            stream.write(token_urlsafe(48))
            stream.flush()
            os.fsync(stream.fileno())
        try:
            try:
                os.link(temporario, arquivo)
            except FileExistsError:
                pass
        finally:
            temporario.unlink(missing_ok=True)
    segredo = arquivo.read_text().strip()
    if len(segredo) < 32:
        raise RuntimeError(
            "O segredo local está incompleto. Restaure o arquivo .session-secret a partir do backup."
        )
    return segredo


class LimitesHTTP:
    """Contadores limitados e seguros entre threads de um processo Waitress."""

    def __init__(self):
        self.contadores = {}
        self.trava = Lock()

    def permitir(self, chave, limite, segundos):
        agora = monotonic()
        with self.trava:
            if len(self.contadores) >= 10000:
                self.contadores = {
                    k: v for k, v in self.contadores.items() if v[1] > agora
                }
                if len(self.contadores) >= 10000:
                    return False, segundos
            qtd, fim = self.contadores.get(chave, (0, agora + segundos))
            if fim <= agora:
                qtd, fim = 0, agora + segundos
            self.contadores[chave] = (qtd + 1, fim)
            return qtd < limite, max(1, int(fim - agora))


def registrar_seguranca(app):
    limites = LimitesHTTP()
    app.extensions["limites_http"] = limites

    @app.before_request
    def proteger_requisicao():
        if app.config["CSRF_ENABLED"] and request.method not in {
            "GET",
            "HEAD",
            "OPTIONS",
        }:
            origem = request.headers.get("Origin")
            if origem and origem != request.host_url.rstrip("/"):
                return jsonify(
                    erro="Origem da requisição não autorizada.", codigo="CSRF_INVALID"
                ), 403
            enviado = request.headers.get("X-CSRF-Token", "")
            esperado = token_csrf()
            if (
                not esperado
                or not enviado
                or not compare_digest(enviado.encode(), esperado.encode())
            ):
                return jsonify(
                    erro="Atualize a página e tente novamente.", codigo="CSRF_INVALID"
                ), 403
        if not app.config["RATE_LIMIT_ENABLED"]:
            return None
        ip = request.remote_addr or "local"
        regras = []
        if request.path == "/auth/login" and request.method == "POST":
            dados = request.get_json(silent=True)
            email = (
                str(dados.get("email", ""))[:180].strip().lower()
                if isinstance(dados, dict)
                else ""
            )
            regras = [
                (f"login-ip:{ip}", 40, 60),
                ("login-conta:" + sha256(email.encode()).hexdigest(), 10, 900),
            ]
        elif request.path == "/auth/cadastro" and request.method == "POST":
            regras = [(f"cadastro:{ip}", 15, 3600)]
        elif request.path in {
            "/auth/recuperacao",
            "/auth/redefinir-senha",
            "/autorizacoes/consultar",
            "/autorizacoes/responder",
        }:
            regras = [(f"conta:{request.path}:{ip}", 20, 300)]
        elif request.path == "/catalogo/perto" or request.path.endswith(
            "/recomendacoes"
        ):
            regras = [(f"catalogo:{ip}", 30, 60)]
        for chave, qtd, segundos in regras:
            permitido, espera = limites.permitir(chave, qtd, segundos)
            if not permitido:
                resposta = jsonify(
                    erro="Muitas tentativas. Aguarde antes de tentar novamente.",
                    codigo="RATE_LIMIT",
                )
                resposta.headers["Retry-After"] = str(espera)
                return resposta, 429
        return None

    @app.after_request
    def cabecalhos(resposta):
        resposta.headers["X-Content-Type-Options"] = "nosniff"
        resposta.headers["X-Frame-Options"] = "DENY"
        resposta.headers["Referrer-Policy"] = "strict-origin"
        resposta.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(self)"
        )
        resposta.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: blob:; "
            "connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'"
        )
        if app.config["SESSION_COOKIE_SECURE"]:
            resposta.headers["Strict-Transport-Security"] = "max-age=31536000"
        if request.path.startswith(
            (
                "/auth/",
                "/privacidade/",
                "/autorizacoes/",
                "/eventos",
                "/notificacoes",
                "/favoritos",
                "/rsvp/",
                "/colaboracoes/",
            )
        ):
            resposta.headers["Cache-Control"] = "private, no-store"
        return resposta


def validar_producao(config):
    if config["APP_ENV"] not in {"development", "production"}:
        raise RuntimeError("APP_ENV deve ser development ou production.")
    if config["APP_ENV"] != "production":
        return
    chave = config.get("SECRET_KEY") or ""
    url = urlsplit(config.get("PUBLIC_BASE_URL", ""))
    if len(chave) < 32 or chave.startswith(("troque", "dev-")):
        raise RuntimeError(
            "Em produção, configure SECRET_KEY com pelo menos 32 caracteres aleatórios."
        )
    if url.scheme != "https" or not url.hostname:
        raise RuntimeError(
            "Em produção, configure PUBLIC_BASE_URL com o endereço HTTPS do site."
        )
    if config.get("PRIVACY_DEMO") or not all(
        config.get(c)
        for c in (
            "PRIVACY_CONTROLLER",
            "PRIVACY_OFFICER",
            "PRIVACY_EMAIL",
            "PRIVACY_PHONE",
        )
    ):
        raise RuntimeError(
            "Em produção, configure os contatos reais de privacidade e PRIVACY_DEMO=false."
        )
    config["TRUSTED_HOSTS"] = [url.hostname]
    config["SESSION_COOKIE_SECURE"] = True
