"""Servidor WSGI para Windows/Linux; configure HTTPS no proxy da hospedagem."""

import os

from app import app
from waitress import serve

if __name__ == "__main__":
    serve(
        app,
        host=os.getenv("BIND_HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        threads=int(os.getenv("WSGI_THREADS", "32")),
    )
