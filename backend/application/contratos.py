"""Contratos pequenos para as dependências que podem ser substituídas."""

from dataclasses import dataclass
from typing import Protocol


class Transacao(Protocol):
    def sincronizar(self): ...
    def confirmar(self): ...
    def reverter(self): ...
    def encerrar(self): ...


class ProvedorFornecedores(Protocol):
    def buscar(self, categoria, **filtros) -> list[dict]: ...


class ProvedorCatalogoPaginado(Protocol):
    def buscar_pagina(self, categoria, **filtros) -> dict: ...


class ProvedorFotos(Protocol):
    def foto(self, token: str) -> tuple[bytes, str]: ...


class ExportadorRelatorio(Protocol):
    def exportar(self, dados: dict) -> bytes: ...


class ArmazenamentoArquivos(Protocol):
    def salvar(self, arquivo, prefixo: str, extensoes: set[str]) -> str: ...
    def remover(self, nome: str): ...


class EstrategiaRateio(Protocol):
    def calcular(self, total, pessoas: int, valor_fixo) -> list: ...


class BuscaEventosPorTipo(Protocol):
    def buscar_por_tipo_evento(self, tipo_evento: str, usuario_id: int) -> list: ...


@dataclass(frozen=True)
class Criado:
    dados: object


@dataclass(frozen=True)
class ArquivoGerado:
    conteudo: bytes
    nome: str
    tipo: str
