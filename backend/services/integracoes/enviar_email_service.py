"""Integração SMTP; credenciais e domínio vêm somente da configuração do servidor."""

import smtplib
import ssl
from email.message import EmailMessage
from urllib.parse import urlsplit

from application.erros import IntegracaoIndisponivel


class EnviarEmailService:
    def __init__(self, config):
        self.config = config

    def verificar_configuracao(self):
        origem = self.config.get("PUBLIC_BASE_URL", "").rstrip("/")
        url = urlsplit(origem)
        local = url.hostname in {"localhost", "127.0.0.1", "::1"}
        if (
            not self.config.get("SMTP_HOST")
            or not self.config.get("SMTP_FROM")
            or not url.hostname
            or url.username
            or url.password
            or url[3]
            or url[4]
            or url.path
            or (url.scheme != "https" and not (local and url.scheme == "http"))
        ):
            raise IntegracaoIndisponivel(
                "A recuperação por e-mail ainda não foi configurada pelo responsável do Momentus."
            )
        return origem

    def executar(self, destinatario, link):
        self.verificar_configuracao()
        mensagem = EmailMessage()
        mensagem["Subject"] = "Redefinir sua senha — Momentus"
        mensagem["From"] = self.config["SMTP_FROM"]
        mensagem["To"] = destinatario
        mensagem.set_content(
            f"Recebemos um pedido para redefinir sua senha no Momentus.\n\n{link}\n\nO link expira em 30 minutos e só pode ser usado uma vez. Se não foi você, ignore esta mensagem."
        )
        contexto = ssl.create_default_context()
        try:
            usar_ssl = self.config.get("SMTP_SSL", False)
            classe = smtplib.SMTP_SSL if usar_ssl else smtplib.SMTP
            kwargs = {"context": contexto} if usar_ssl else {}
            with classe(
                self.config["SMTP_HOST"],
                int(self.config.get("SMTP_PORT", 587)),
                timeout=15,
                **kwargs,
            ) as conexao:
                if not usar_ssl:
                    conexao.starttls(context=contexto)
                if self.config.get("SMTP_USERNAME"):
                    conexao.login(
                        self.config["SMTP_USERNAME"],
                        self.config.get("SMTP_PASSWORD", ""),
                    )
                conexao.send_message(mensagem)
        except (OSError, smtplib.SMTPException, ValueError):
            raise IntegracaoIndisponivel(
                "Não foi possível enviar o e-mail agora. Tente novamente mais tarde."
            ) from None
