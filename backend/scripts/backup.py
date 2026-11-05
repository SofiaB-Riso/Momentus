"""Backup SQLite + uploads. Restauração somente em diretório novo e vazio."""

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import stat
import tempfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, BadZipFile, ZipFile

BACKEND = Path(__file__).resolve().parents[1]


def hash_arquivo(caminho):
    with Path(caminho).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def criar_backup(banco, uploads, destino):
    banco, uploads, destino = map(Path, (banco, uploads, destino))
    if not banco.is_file() or banco.is_symlink():
        raise ValueError("Informe um arquivo SQLite existente, sem link simbólico.")
    if uploads.is_symlink():
        raise ValueError("A pasta de uploads não pode ser um link simbólico.")
    destino.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="momentus-backup-") as pasta:
        copia = Path(pasta) / "banco.db"
        with (
            sqlite3.connect(banco.resolve().as_uri() + "?mode=ro", uri=True) as origem,
            sqlite3.connect(copia) as db,
        ):
            origem.backup(db)
            if db.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                raise ValueError("O banco não passou na verificação de integridade.")
        arquivos = {"banco.db": copia}
        for arquivo in uploads.rglob("*") if uploads.exists() else []:
            if arquivo.is_symlink():
                raise ValueError("Remova links simbólicos dos uploads antes do backup.")
            if arquivo.is_file():
                arquivos["uploads/" + arquivo.relative_to(uploads).as_posix()] = arquivo
        segredo = banco.parent / ".session-secret"
        if segredo.is_file() and not segredo.is_symlink():
            arquivos["segredo-sessao"] = segredo
        manifesto = {
            "versao": 1,
            "criado_em": datetime.now(timezone.utc).isoformat(),
            "arquivos": {nome: hash_arquivo(p) for nome, p in arquivos.items()},
        }
        descritor = os.open(destino, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        try:
            with (
                os.fdopen(descritor, "wb") as stream,
                ZipFile(stream, "w", ZIP_DEFLATED) as zipado,
            ):
                for nome, arquivo in arquivos.items():
                    zipado.write(arquivo, nome)
                zipado.writestr(
                    "manifesto.json",
                    json.dumps(manifesto, ensure_ascii=False, indent=2),
                )
        except Exception:
            destino.unlink(missing_ok=True)
            raise
    return destino


def restaurar_backup(arquivo, destino):
    destino = Path(destino)
    if destino.is_symlink() or (
        destino.exists() and (not destino.is_dir() or any(destino.iterdir()))
    ):
        raise ValueError("Restaure em uma pasta nova ou completamente vazia.")
    destino.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(arquivo) as zipado:
        infos = zipado.infolist()
        if sum(i.file_size for i in infos) > 2 * 1024**3:
            raise ValueError("O backup excede o limite de 2 GB desta ferramenta.")
        if len({i.filename for i in infos}) != len(infos) or any(
            stat.S_ISLNK(i.external_attr >> 16) for i in infos
        ):
            raise ValueError("Backup com entradas duplicadas ou links simbólicos.")
        if zipado.getinfo("manifesto.json").file_size > 1024**2:
            raise ValueError("Manifesto inválido.")
        manifesto = json.loads(zipado.read("manifesto.json"))
        if manifesto.get("versao") != 1 or not isinstance(
            manifesto.get("arquivos"), dict
        ):
            raise ValueError("Versão do backup não reconhecida.")
        arquivos = manifesto["arquivos"]
        if (
            set(zipado.namelist()) != set(arquivos) | {"manifesto.json"}
            or "banco.db" not in arquivos
        ):
            raise ValueError("Conteúdo do backup não corresponde ao manifesto.")
        with tempfile.TemporaryDirectory(
            dir=destino.parent, prefix=".momentus-restauracao-"
        ) as pasta:
            raiz = Path(pasta) / "restaurado"
            for nome, esperado in arquivos.items():
                partes = PurePosixPath(nome)
                if (
                    partes.is_absolute()
                    or ".." in partes.parts
                    or "\\" in nome
                    or partes.as_posix() != nome
                ):
                    raise ValueError("Caminho inválido no backup.")
                if nome == "banco.db":
                    alvo = raiz / "backend/instance/momentus.db"
                elif nome == "segredo-sessao":
                    alvo = raiz / "backend/instance/.session-secret"
                elif nome.startswith("uploads/") and len(partes.parts) > 1:
                    alvo = raiz / "backend" / partes
                else:
                    raise ValueError("Arquivo inesperado no backup.")
                alvo.parent.mkdir(parents=True, exist_ok=True)
                with zipado.open(nome) as origem, alvo.open("wb") as saida:
                    shutil.copyfileobj(origem, saida)
                os.chmod(alvo, 0o600)
                if hash_arquivo(alvo) != esperado:
                    raise ValueError("O backup está corrompido ou foi alterado.")
            with sqlite3.connect(raiz / "backend/instance/momentus.db") as db:
                if db.execute("PRAGMA quick_check").fetchone()[0] != "ok":
                    raise ValueError("Banco restaurado inválido.")
            if destino.exists():
                destino.rmdir()
            raiz.replace(destino)
    return destino


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    acoes = parser.add_subparsers(dest="acao", required=True)
    criar = acoes.add_parser("criar")
    criar.add_argument("--banco", type=Path, default=BACKEND / "instance/momentus.db")
    criar.add_argument("--uploads", type=Path, default=BACKEND / "uploads")
    criar.add_argument("--saida", type=Path, required=True)
    restaurar = acoes.add_parser("restaurar")
    restaurar.add_argument("--arquivo", type=Path, required=True)
    restaurar.add_argument("--destino", type=Path, required=True)
    args = parser.parse_args()
    try:
        resultado = (
            criar_backup(args.banco, args.uploads, args.saida)
            if args.acao == "criar"
            else restaurar_backup(args.arquivo, args.destino)
        )
    except (ValueError, OSError, KeyError, BadZipFile) as erro:
        parser.exit(1, str(erro) + "\n")
    print(resultado.resolve())


if __name__ == "__main__":
    main()
