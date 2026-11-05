"""Contratos verificáveis do enunciado: classes, rotas, Models e documentação."""

import ast
import importlib
import inspect
import json
import os
import re
import unittest
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite://"
from app import create_app
from models import db
from models.crud import CrudModel
from scripts.gerar_diagrama import inventario

BACKEND = Path(__file__).resolve().parents[1]
ROOT = BACKEND.parent
DOCS = ROOT / "docs"


class ArquiteturaDisciplinaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.engine.dispose()

    def test_todas_as_rotas_proprias_apontam_para_controllers_em_classes(self):
        for rule in self.app.url_map.iter_rules():
            if rule.endpoint == "static":
                continue
            view = self.app.view_functions[rule.endpoint]
            with self.subTest(rota=rule.rule):
                self.assertTrue(inspect.ismethod(view))
                self.assertTrue(type(view.__self__).__name__.endswith("Controller"))
                self.assertTrue(view.__module__.startswith("controllers."))

    def test_rotas_e_metodos_da_versao_anterior_foram_preservados(self):
        expected = json.loads((BACKEND / "tests/fixtures/rotas_base.json").read_text())
        actual = sorted(
            [r.rule, sorted(r.methods)] for r in self.app.url_map.iter_rules()
        )
        for route in expected:
            self.assertIn(route, actual)

    def test_models_mantem_heranca_e_crud_exigidos(self):
        with self.app.app_context():
            for mapper in db.Model.registry.mappers:
                model = mapper.class_
                with self.subTest(model=model.__name__):
                    self.assertTrue(issubclass(model, (CrudModel, db.Model)))
                    self.assertTrue(issubclass(model, CrudModel))
                    self.assertTrue(issubclass(model, db.Model))
                    for operation in (
                        "salvar",
                        "atualizar",
                        "deletar",
                        "listar_todos",
                        "buscar_por_id",
                    ):
                        self.assertTrue(callable(getattr(model, operation)))
                    self.assertEqual(model.listar_todos(), [])

    def test_http_externo_fica_nos_services_de_integracao(self):
        for folder in ("controllers", "infrastructure", "services"):
            for path in (BACKEND / folder).rglob("*.py"):
                for node in ast.walk(ast.parse(path.read_text())):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name == "requests":
                                self.assertIn("integracoes", path.parts, str(path))
                    if isinstance(node, ast.ImportFrom) and node.module == "requests":
                        self.assertIn("integracoes", path.parts, str(path))

    def test_matriz_descreve_telas_rotas_classes_e_tabelas_reais(self):
        cases = json.loads((DOCS / "funcionalidades.json").read_text())
        self.assertEqual([c["id"] for c in cases], list(range(1, 41)))
        self.assertEqual(len({c["titulo"] for c in cases}), 40)
        frontend = "\n".join(
            p.read_text()
            for p in (ROOT / "frontend").rglob("*")
            if p.suffix in {".js", ".html"}
        )
        for case in cases:
            with self.subTest(caso=case["id"]):
                self.assertTrue((ROOT / "frontend" / case["interface"]).is_file())
                for marker in re.findall(r"[#.]([A-Za-z]\w*)", case["controle"]):
                    self.assertIn(marker, frontend)
                route = next(
                    r
                    for r in self.app.url_map.iter_rules()
                    if r.rule == case["rota"] and case["metodo_http"] in r.methods
                )
                view = self.app.view_functions[route.endpoint]
                self.assertEqual(type(view.__self__).__name__, case["controller"])
                self.assertEqual(view.__name__, case["acao"])
                if case["service"] == "ExportarRelatorioService":
                    self.assertIn(".relatorio(", inspect.getsource(view))
                    self.assertEqual(
                        type(
                            self.app.extensions["momentus"].relatorio("pdf", None)
                        ).__name__,
                        case["service"],
                    )
                else:
                    self.assertIn(case["service"], inspect.getsource(view))
                service = getattr(
                    importlib.import_module(case["service_module"]), case["service"]
                )
                self.assertTrue(inspect.isclass(service))
                self.assertTrue(callable(service.executar))
                mapper = next(
                    m
                    for m in db.Model.registry.mappers
                    if m.class_.__name__ == case["model"]
                )
                self.assertEqual(mapper.local_table.name, case["tabela"])

    def test_diagrama_corresponde_aos_metadados_das_models(self):
        expected = json.loads((DOCS / "modelos.json").read_text())
        self.assertEqual(inventario(), expected)
        shown = set()
        for source in (DOCS / "diagramas").glob("*.mmd"):
            text = source.read_text()
            for name, body in re.findall(r"class (\w+) \{([^}]+)\}", text):
                if name not in expected:
                    continue
                shown.add(name)
                for attribute in re.findall(r"\+\w+ (\w+)\n", body):
                    self.assertIn(attribute, expected[name]["atributos"])
            self.assertTrue(source.with_suffix(".svg").is_file())
        self.assertEqual(shown, set(expected))

    def test_readme_enumera_quarenta_casos_e_indica_diagrama(self):
        text = (ROOT / "README.md").read_text()
        section = text.split("## Funcionalidades Implementadas\n", 1)[1].split(
            "\n## ", 1
        )[0]
        cases = json.loads((DOCS / "funcionalidades.json").read_text())
        listed = re.findall(r"^(\d+)\. (.+)\.$", section, re.MULTILINE)
        self.assertEqual(listed, [(str(c["id"]), c["titulo"]) for c in cases])
        self.assertIn("docs/diagrama_classes.md", text)
        self.assertIn("docs/roteiro_video.md", text)
