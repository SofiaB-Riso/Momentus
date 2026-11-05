import os

os.environ["DATABASE_URL"] = "sqlite://"
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from threading import Barrier

from app import create_app
from models import EntradaEspera, db


class QuatroRecursosTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.app = create_app(
            {
                "TESTING": True,
                "SECRET_KEY": "teste-quatro-recursos",
                "SQLALCHEMY_DATABASE_URI": "sqlite:///" + self.tmp.name + "/test.db",
                "UPLOAD_FOLDER": self.tmp.name + "/uploads",
                "LIVE_INTERVAL": 0,
                "LIVE_ITERATIONS": 1,
            }
        )
        self.c = self.app.test_client()
        self.cadastrar(self.c, "dono@teste.example")
        self.ev = self.criar()
        self.base = f"/eventos/{self.ev['id']}"

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.engine.dispose()
        self.tmp.cleanup()

    def cadastrar(self, c, email):
        r = c.post(
            "/auth/cadastro",
            json={
                "nome": "Pessoa Teste",
                "email": email,
                "senha": "senha-teste",
                "aceite_termos": True,
                "versao_termos": "2026-10-30",
                "faixa_etaria": "adulto",
                "declaracao_idade": True,
            },
        )
        self.assertEqual(r.status_code, 201, r.json)

    def criar(self, cliente=None, **dados):
        r = (cliente or self.c).post(
            "/eventos",
            json={
                "nome_evento": "Evento de teste",
                "tipo_evento": "aniversario",
                "data_evento": "2027-06-10",
                "hora_evento": "18:00",
                "endereco_evento": "Rua A, 100",
                "cidade_evento": "Belo Horizonte",
                **dados,
            },
        )
        self.assertEqual(r.status_code, 201, r.json)
        return r.json

    def proposta(self, **dados):
        r = self.c.post(
            self.base + "/propostas",
            json={
                "fornecedor": "Fornecedor Teste",
                "categoria": "buffet",
                "valor": 100,
                "servicos": ["equipe", "montagem"],
                **dados,
            },
        )
        self.assertEqual(r.status_code, 201, r.json)
        return r.json

    def convidado(self, nome="Convidado"):
        r = self.c.post(self.base + "/convidados", json={"nome": nome})
        self.assertEqual(r.status_code, 201, r.json)
        return r.json

    def responder(self, c, status="confirmado"):
        r = self.app.test_client().post(
            "/rsvp/" + c["token_rsvp"], json={"status": status}
        )
        self.assertEqual(r.status_code, 200, r.json)
        return r.json["convidado"]

    def limite(self, n):
        r = self.c.put(self.base + "/lista-espera", json={"limite_vagas": n})
        self.assertEqual(r.status_code, 200, r.json)
        return r.json

    def test_comparacao_total_taxas_desconto_parcelas(self):
        a = self.proposta(valor=200, desconto=20, taxas=10, parcelas=3)
        b = self.proposta(fornecedor="Mais barato", valor=175)
        r = self.c.get(self.base + "/propostas/comparacao").json
        self.assertEqual(r["propostas"][0]["id"], b["id"])
        self.assertTrue(r["propostas"][0]["destaque"])
        self.assertEqual(a["total"], 190)
        self.assertEqual(a["primeira_parcela"], 63.34)
        self.assertEqual(r["economia_possivel"], 15)

    def test_comparacao_prioriza_servicos_e_teto(self):
        barato = self.proposta(valor=50, servicos=[])
        completo = self.proposta(valor=100, servicos=["equipe"])
        self.proposta(valor=300, servicos=["equipe"])
        r = self.c.get(
            self.base + "/propostas/comparacao?necessarios=equipe&teto=150"
        ).json
        self.assertEqual(r["propostas"][0]["id"], completo["id"])
        self.assertTrue(r["propostas"][0]["destaque"])
        self.assertEqual(
            next(p for p in r["propostas"] if p["id"] == barato["id"])["faltantes"],
            ["equipe"],
        )

    def test_comparacao_nao_mistura_categorias(self):
        self.proposta()
        self.proposta(categoria="musica", valor=1)
        self.assertEqual(
            len(self.c.get(self.base + "/propostas/comparacao").json["propostas"]), 1
        )

    def test_comparacao_sem_opcao_adequada_nao_recomenda(self):
        self.proposta()
        r = self.c.get(self.base + "/propostas/comparacao?teto=0").json
        self.assertFalse(any(p["destaque"] for p in r["propostas"]))

    def test_proposta_edita_remove_e_valida_campos(self):
        p = self.proposta()
        for campo, valor in [
            ("valor", -1),
            ("desconto", 200),
            ("taxas", {}),
            ("parcelas", 0),
            ("servicos", ["invalido"]),
            ("categoria", "invalida"),
            ("fornecedor", "X"),
        ]:
            with self.subTest(campo=campo):
                self.assertEqual(
                    self.c.post(
                        self.base + "/propostas",
                        json={
                            "fornecedor": "Fornecedor",
                            "categoria": "buffet",
                            "valor": 100,
                            campo: valor,
                        },
                    ).status_code,
                    400,
                )
        self.assertEqual(
            self.c.put(
                self.base + "/propostas/" + str(p["id"]),
                json={"fornecedor": "Alterado", "categoria": "buffet", "valor": 80},
            ).status_code,
            200,
        )
        self.assertEqual(
            self.c.delete(self.base + "/propostas/" + str(p["id"])).status_code, 204
        )
        self.assertEqual(self.c.get(self.base + "/propostas").json["propostas"], [])

    def test_propostas_isoladas_por_evento_e_usuario(self):
        p = self.proposta()
        outro = self.app.test_client()
        self.cadastrar(outro, "outro@teste.example")
        ev = self.criar(outro)
        self.assertEqual(
            outro.get(self.base + "/propostas/comparacao").status_code, 403
        )
        self.assertEqual(
            self.c.delete(f"/eventos/{ev['id']}/propostas/{p['id']}").status_code, 403
        )

    def test_agenda_detecta_sobreposicao_e_mesmo_endereco(self):
        r = self.c.post(
            "/eventos/conflitos",
            json={
                "data_evento": "2027-06-10",
                "hora_evento": "19:00",
                "duracao_minutos": 60,
                "endereco_evento": "Rua A, 100",
                "cidade_evento": "Belo Horizonte",
            },
        ).json
        self.assertEqual(len(r["conflitos"]), 1)
        self.assertTrue(r["conflitos"][0]["mesmo_local"])

    def test_agenda_bordas_adjacentes_nao_conflitam(self):
        r = self.c.post(
            "/eventos/conflitos",
            json={
                "data_evento": "2027-06-10",
                "hora_evento": "21:00",
                "duracao_minutos": 60,
            },
        ).json
        self.assertEqual(r["conflitos"], [])

    def test_agenda_cruza_meia_noite(self):
        self.criar(hora_evento="23:00", duracao_minutos=180)
        r = self.c.post(
            "/eventos/conflitos",
            json={
                "data_evento": "2027-06-11",
                "hora_evento": "00:30",
                "duracao_minutos": 60,
            },
        ).json
        self.assertEqual(len(r["conflitos"]), 1)

    def test_agenda_ignora_proprio_rascunho_e_cancelado(self):
        self.criar(status="rascunho")
        self.criar(status="cancelado")
        r = self.c.post(
            "/eventos/conflitos",
            json={
                "evento_id": self.ev["id"],
                "data_evento": "2027-06-10",
                "hora_evento": "18:00",
            },
        ).json
        self.assertEqual(r["conflitos"], [])

    def test_agenda_nao_expoe_evento_privado_de_outro(self):
        c = self.app.test_client()
        self.cadastrar(c, "privado@teste.example")
        self.criar(c)
        r = c.post(
            "/eventos/conflitos",
            json={"data_evento": "2027-06-10", "hora_evento": "18:00"},
        ).json
        self.assertEqual(len(r["conflitos"]), 1)
        self.assertNotEqual(r["conflitos"][0]["id"], self.ev["id"])

    def test_agenda_sem_horario_e_duracao_invalida(self):
        for dados in [
            {"data_evento": "2027-06-10"},
            {"data_evento": "x", "hora_evento": "18:00"},
            {
                "data_evento": "2027-06-10",
                "hora_evento": "18:00",
                "duracao_minutos": True,
            },
        ]:
            self.assertEqual(
                self.c.post("/eventos/conflitos", json=dados).status_code, 400
            )
        self.assertEqual(
            self.c.put(self.base, json={"duracao_minutos": 0}).status_code, 400
        )

    def test_duracao_persiste_na_criacao_e_edicao(self):
        self.assertEqual(
            self.c.get(self.base).json["planejamento"]["duracao_minutos"], 180
        )
        self.assertEqual(
            self.c.put(self.base, json={"duracao_minutos": 90}).json["planejamento"][
                "duracao_minutos"
            ],
            90,
        )

    def test_cronograma_reaproveita_checklist_sem_duplicar(self):
        self.assertEqual(len(self.c.get(self.base).json["tarefas"]), 4)
        self.assertEqual(self.c.post(self.base + "/cronograma").status_code, 200)
        tarefas = self.c.get(self.base).json["tarefas"]
        self.assertEqual(len(tarefas), 6)
        self.assertTrue(all(t["prazo"] for t in tarefas))
        self.c.post(self.base + "/cronograma")
        self.assertEqual(len(self.c.get(self.base).json["tarefas"]), 6)

    def test_cronograma_recalcula_pendentes_preserva_concluidas_e_manuais(self):
        self.c.post(self.base + "/cronograma")
        tarefas = self.c.get(self.base).json["tarefas"]
        primeira = tarefas[0]
        self.c.put(self.base + "/tarefas/" + primeira["id"], json={"feita": True})
        manual = self.c.post(
            self.base + "/tarefas",
            json={"titulo": "Manual", "prazo": "2027-05-01T12:00"},
        ).json
        self.c.put(self.base, json={"data_evento": "2027-06-20"})
        depois = {t["id"]: t for t in self.c.get(self.base).json["tarefas"]}
        self.assertEqual(depois[primeira["id"]]["prazo"], primeira["prazo"])
        for t in tarefas[1:]:
            self.assertEqual(
                datetime.fromisoformat(depois[t["id"]]["prazo"])
                - datetime.fromisoformat(t["prazo"]),
                timedelta(days=10),
            )
        self.assertEqual(depois[manual["id"]]["prazo"], "2027-05-01T12:00:00")

    def test_cronograma_muda_antecedencia_por_tipo(self):
        self.c.post(self.base + "/cronograma")
        antes = self.c.get(self.base).json["tarefas"]
        self.c.put(self.base, json={"tipo_evento": "casamento"})
        depois = self.c.get(self.base).json["tarefas"]
        a = next(t for t in antes if t["chave"] == "checklistLocal")
        d = next(t for t in depois if t["chave"] == "checklistLocal")
        self.assertEqual(
            datetime.fromisoformat(a["prazo"]) - datetime.fromisoformat(d["prazo"]),
            timedelta(days=150),
        )

    def test_fila_fifo_reenvio_e_promocao_automatica(self):
        self.limite(1)
        a, b, c = [self.convidado(n) for n in ["A", "B", "C"]]
        self.assertEqual(self.responder(a)["status"], "confirmado")
        self.assertEqual(self.responder(b)["status"], "espera")
        self.responder(c)
        self.responder(b)
        fila = self.c.get(self.base + "/lista-espera").json["fila"]
        self.assertEqual([f["nome"] for f in fila], ["B", "C"])
        self.responder(a, "recusado")
        fila = self.c.get(self.base + "/lista-espera").json
        self.assertEqual(fila["confirmados"], 1)
        self.assertEqual([f["nome"] for f in fila["fila"]], ["C"])
        dados = self.app.test_client().get("/rsvp/" + b["token_rsvp"]).json
        self.assertEqual(dados["convidado"]["status"], "confirmado")
        self.assertTrue(any("vaga" in a["titulo"].lower() for a in dados["avisos"]))

    def test_fila_sem_limite_preserva_comportamento(self):
        for _ in range(3):
            self.assertEqual(self.responder(self.convidado())["status"], "confirmado")

    def test_fila_cancelamento_reentrada_vai_ao_final(self):
        self.limite(1)
        a, b, c = [self.convidado(n) for n in ["A", "B", "C"]]
        self.responder(a)
        self.responder(b)
        self.responder(c)
        self.responder(b, "pendente")
        self.responder(b)
        self.assertEqual(
            [x["nome"] for x in self.c.get(self.base + "/lista-espera").json["fila"]],
            ["C", "B"],
        )

    def test_remover_confirmado_promove_proximo(self):
        self.limite(1)
        a, b = self.convidado("A"), self.convidado("B")
        self.responder(a)
        self.responder(b)
        self.c.delete(self.base + "/convidados/" + a["id"])
        self.assertEqual(
            self.app.test_client()
            .get("/rsvp/" + b["token_rsvp"])
            .json["convidado"]["status"],
            "confirmado",
        )

    def test_ampliar_e_desativar_limite_promove_fila(self):
        self.limite(1)
        for n in ["A", "B", "C"]:
            self.responder(self.convidado(n))
        self.assertEqual(self.limite(2)["confirmados"], 2)
        self.assertEqual(self.limite(None)["confirmados"], 3)
        self.assertEqual(self.c.get(self.base + "/lista-espera").json["fila"], [])

    def test_limite_menor_que_confirmados_rejeitado(self):
        self.responder(self.convidado())
        self.responder(self.convidado())
        self.assertEqual(
            self.c.put(
                self.base + "/lista-espera", json={"limite_vagas": 1}
            ).status_code,
            400,
        )
        self.assertIsNone(self.c.get(self.base + "/lista-espera").json["limite_vagas"])

    def test_painel_organizador_respeita_limite(self):
        self.limite(1)
        a, b = self.convidado("A"), self.convidado("B")
        self.responder(a)
        r = self.c.put(
            self.base + "/convidados/" + b["id"], json={"status": "confirmado"}
        )
        self.assertEqual(r.json["status"], "espera")

    def test_rsvp_expoe_so_a_propria_posicao(self):
        self.limite(1)
        a, b, c = [self.convidado(n) for n in ["A", "Nome B secreto", "Nome C secreto"]]
        for con in (a, b, c):
            self.responder(con)
        r = self.app.test_client().get("/rsvp/" + b["token_rsvp"])
        self.assertEqual(r.json["lista_espera"]["posicao"], 1)
        self.assertNotIn("Nome C secreto", r.get_data(as_text=True))

    def test_confirmacoes_concorrentes_nao_ultrapassam_limite(self):
        self.limite(1)
        a, b = self.convidado("A"), self.convidado("B")
        barreira = Barrier(2)

        def confirmar(con):
            cliente = self.app.test_client()
            barreira.wait(timeout=10)
            r = cliente.post(
                "/rsvp/" + con["token_rsvp"], json={"status": "confirmado"}
            )
            return r.status_code, r.json

        with ThreadPoolExecutor(max_workers=2) as ex:
            res = list(ex.map(confirmar, [a, b]))
        self.assertEqual([r[0] for r in res], [200, 200], res)
        self.assertEqual(
            sorted(r[1]["convidado"]["status"] for r in res), ["confirmado", "espera"]
        )
        self.assertEqual(self.c.get(self.base + "/lista-espera").json["confirmados"], 1)

    def test_leitor_nao_pode_mutar_novos_recursos(self):
        c = self.app.test_client()
        self.cadastrar(c, "leitor@teste.example")
        convite = self.c.post(
            self.base + "/colaboradores",
            json={
                "nome": "Leitor",
                "email": "leitor@teste.example",
                "pode_editar": False,
            },
        ).json
        c.post(
            "/colaboracoes/" + convite["token"] + "/responder", json={"status": "ativo"}
        )
        self.assertEqual(c.get(self.base + "/propostas/comparacao").status_code, 200)
        for metodo, rota, dados in [
            ("post", "/cronograma", {}),
            ("put", "/lista-espera", {"limite_vagas": 1}),
            (
                "post",
                "/propostas",
                {"fornecedor": "Teste", "categoria": "buffet", "valor": 50},
            ),
        ]:
            self.assertEqual(
                getattr(c, metodo)(self.base + rota, json=dados).status_code, 403
            )

    def test_espera_libera_item_reservado_antes_da_confirmacao(self):
        self.limite(1)
        a, b = self.convidado("A"), self.convidado("B")
        self.responder(a)
        item = self.c.post(
            self.base + "/itens-compartilhados",
            json={"nome": "Bebida", "quantidade": 1},
        ).json
        r = self.app.test_client().post(
            "/rsvp/" + b["token_rsvp"] + "/itens/" + str(item["id"]) + "/assumir"
        )
        self.assertEqual(r.status_code, 200, r.json)
        self.assertEqual(self.responder(b)["status"], "espera")
        atual = self.c.get(self.base).json["itens_compartilhados"][0]
        self.assertFalse(atual["responsavelNome"])

    def test_gerar_link_responsavel_libera_vaga_e_promove_fila(self):
        self.limite(1)
        a, b = self.convidado("A"), self.convidado("B")
        self.responder(a)
        self.responder(b)
        r = self.app.test_client().post("/rsvp/" + a["token_rsvp"] + "/responsavel")
        self.assertEqual(r.status_code, 200, r.json)
        dados = self.app.test_client().get("/rsvp/" + b["token_rsvp"]).json
        self.assertEqual(dados["convidado"]["status"], "confirmado")
        r = self.app.test_client().post(
            "/rsvp/" + a["token_rsvp"], json={"status": "confirmado"}
        )
        self.assertEqual(r.status_code, 400, r.json)

    def test_excluir_evento_remove_novos_dados_dependentes(self):
        self.proposta()
        self.limite(1)
        for nome in ["A", "B"]:
            self.responder(self.convidado(nome))
        self.c.post(self.base + "/cronograma")
        self.assertEqual(self.c.delete(self.base).status_code, 204)
        from models import PlanejamentoEvento, PropostaFornecedor

        with self.app.app_context():
            for model in [PlanejamentoEvento, PropostaFornecedor, EntradaEspera]:
                self.assertEqual(model.listar_todos(), [])

    def test_agenda_mesmo_horario_em_dias_diferentes_nao_conflita(self):
        for data in ["2027-06-09", "2027-06-11", "2028-06-10"]:
            with self.subTest(data=data):
                r = self.c.post(
                    "/eventos/conflitos",
                    json={
                        "data_evento": data,
                        "hora_evento": "18:00",
                        "duracao_minutos": 180,
                    },
                )
                self.assertEqual(r.status_code, 200, r.json)
                self.assertEqual(r.json["conflitos"], [])
                self.assertTrue(r.json["inicio"].startswith(data))

    def test_agenda_so_sobrepoe_na_virada_do_dia_correto(self):
        self.c.put(self.base, json={"hora_evento": "23:00", "duracao_minutos": 180})
        for data, quantidade in [
            ("2027-06-11", 1),
            ("2027-06-12", 0),
            ("2027-06-10", 0),
        ]:
            r = self.c.post(
                "/eventos/conflitos",
                json={
                    "data_evento": data,
                    "hora_evento": "00:30",
                    "duracao_minutos": 60,
                },
            )
            self.assertEqual(len(r.json["conflitos"]), quantidade)

    def gerar_com_relogio(self, agora):
        from unittest.mock import patch

        with patch(
            "services.cronograma.sincronizar_cronograma_service.agora_local",
            return_value=agora,
        ):
            return self.c.post(self.base + "/cronograma")

    def test_cronograma_casamento_em_duas_semanas_distribui_datas_futuras(self):
        agora = datetime(2026, 11, 3, 12, 30)
        self.c.put(
            self.base, json={"data_evento": "2026-11-17", "tipo_evento": "casamento"}
        )
        r = self.gerar_com_relogio(agora)
        self.assertEqual(r.status_code, 200, r.json)
        prazos = [datetime.fromisoformat(t["prazo"]) for t in r.json["tarefas"]]
        self.assertTrue(
            all(agora <= prazo <= datetime(2026, 11, 17, 18) for prazo in prazos)
        )
        self.assertGreaterEqual(len({p.date() for p in prazos}), 4)
        self.assertEqual(min(prazos).date(), agora.date())
        self.assertEqual(max(prazos).date().isoformat(), "2026-11-16")

    def test_cronograma_todos_os_tipos_cabem_no_periodo_disponivel(self):
        agora = datetime(2026, 11, 3, 17)
        for tipo in [
            "casamento",
            "formatura",
            "corporativo",
            "aniversario",
            "churrasco",
            "Festa junina",
        ]:
            with self.subTest(tipo=tipo):
                self.c.put(
                    self.base, json={"data_evento": "2026-11-17", "tipo_evento": tipo}
                )
                r = self.gerar_com_relogio(agora)
                self.assertEqual(r.status_code, 200, r.json)
                self.assertTrue(
                    all(
                        agora
                        <= datetime.fromisoformat(t["prazo"])
                        <= datetime(2026, 11, 17, 18)
                        for t in r.json["tarefas"]
                    )
                )

    def test_cronograma_amanha_nao_sugere_prazo_antes_de_agora(self):
        agora = datetime(2026, 11, 3, 22, 45)
        self.c.put(
            self.base, json={"data_evento": "2026-11-04", "tipo_evento": "casamento"}
        )
        r = self.gerar_com_relogio(agora)
        self.assertEqual(r.status_code, 200, r.json)
        self.assertTrue(
            all(
                agora <= datetime.fromisoformat(t["prazo"]) <= datetime(2026, 11, 4, 18)
                for t in r.json["tarefas"]
            )
        )

    def test_cronograma_no_mesmo_dia_distribui_no_intervalo_restante(self):
        agora = datetime(2026, 11, 3, 12)
        self.c.put(
            self.base, json={"data_evento": "2026-11-03", "hora_evento": "18:00"}
        )
        r = self.gerar_com_relogio(agora)
        self.assertEqual(r.status_code, 200, r.json)
        prazos = [datetime.fromisoformat(t["prazo"]) for t in r.json["tarefas"]]
        self.assertTrue(all(agora <= p <= datetime(2026, 11, 3, 18) for p in prazos))
        self.assertGreaterEqual(len(set(prazos)), 4)

    def test_cronograma_evento_passado_recusa_sem_alterar_checklist(self):
        self.c.put(self.base, json={"data_evento": "2026-11-02"})
        r = self.gerar_com_relogio(datetime(2026, 11, 3, 12))
        self.assertEqual(r.status_code, 400, r.json)
        evento = self.c.get(self.base).json
        self.assertEqual(len(evento["tarefas"]), 4)
        self.assertFalse(evento["planejamento"]["cronograma_ativo"])

    def test_cronograma_encurtar_data_preserva_concluidas_e_manuais(self):
        from unittest.mock import patch

        agora = datetime(2026, 11, 3, 12)
        self.gerar_com_relogio(agora)
        t = self.c.get(self.base).json["tarefas"][0]
        self.c.put(self.base + "/tarefas/" + t["id"], json={"feita": True})
        manual = self.c.post(
            self.base + "/tarefas",
            json={"titulo": "Tarefa manual", "prazo": "2026-11-01T10:00"},
        ).json
        with patch(
            "services.cronograma.sincronizar_cronograma_service.agora_local",
            return_value=agora,
        ):
            r = self.c.put(
                self.base,
                json={"data_evento": "2026-11-17", "tipo_evento": "casamento"},
            )
        self.assertEqual(r.status_code, 200, r.json)
        for tarefa in r.json["tarefas"]:
            if tarefa["id"] == t["id"]:
                self.assertEqual(tarefa["prazo"], t["prazo"])
            elif tarefa["id"] == manual["id"]:
                self.assertEqual(tarefa["prazo"], "2026-11-01T10:00:00")
            else:
                self.assertGreaterEqual(datetime.fromisoformat(tarefa["prazo"]), agora)

    def test_cronograma_no_mesmo_dia_recalcula_ao_mudar_so_horario(self):
        from unittest.mock import patch

        agora = datetime(2026, 11, 3, 12)
        self.c.put(
            self.base, json={"data_evento": "2026-11-03", "hora_evento": "18:00"}
        )
        self.gerar_com_relogio(agora)
        with patch(
            "services.cronograma.sincronizar_cronograma_service.agora_local",
            return_value=agora,
        ):
            r = self.c.put(self.base, json={"hora_evento": "16:00"})
        self.assertEqual(r.status_code, 200, r.json)
        prazos = [datetime.fromisoformat(t["prazo"]) for t in r.json["tarefas"]]
        self.assertTrue(all(agora <= p <= datetime(2026, 11, 3, 16) for p in prazos))

    def test_cronograma_no_mesmo_dia_sem_horario_usa_fim_do_dia(self):
        agora = datetime(2026, 11, 3, 20)
        self.c.put(self.base, json={"data_evento": "2026-11-03", "hora_evento": ""})
        r = self.gerar_com_relogio(agora)
        self.assertEqual(r.status_code, 200, r.json)
        prazos = [datetime.fromisoformat(t["prazo"]) for t in r.json["tarefas"]]
        self.assertTrue(
            all(agora <= p <= datetime(2026, 11, 3, 23, 59, 59) for p in prazos)
        )
