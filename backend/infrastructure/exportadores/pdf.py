import io
from html import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class ExportadorPDF:
    def exportar(self, dados):
        buffer = io.BytesIO()
        estilos = getSampleStyleSheet()
        corpo = estilos["BodyText"]
        corpo.fontSize = 8
        corpo.leading = 10
        documento = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            title="Relatório - " + dados["nome"],
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36,
        )
        elementos = [
            Paragraph("Momentus - Relatório do Evento", estilos["Title"]),
            Spacer(1, 12),
        ]
        largura = A4[0] - 72
        for titulo, linhas in dados.items():
            if titulo == "nome":
                continue
            elementos += [Paragraph(escape(titulo), estilos["Heading2"]), Spacer(1, 6)]
            if len(linhas) == 1 and titulo != "Resumo":
                elementos.append(Paragraph("Nenhum registro cadastrado.", corpo))
                continue
            celulas = [
                [
                    Paragraph(escape(str(v if v is not None else "")), corpo)
                    for v in linha
                ]
                for linha in linhas
            ]
            tabela = Table(
                celulas,
                colWidths=[largura / len(linhas[0])] * len(linhas[0]),
                repeatRows=0 if titulo == "Resumo" else 1,
                hAlign="LEFT",
            )
            tabela.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e7e2f5")),
                        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#ddd6ee")),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ]
                )
            )
            elementos += [tabela, Spacer(1, 12)]
        documento.build(elementos)
        return buffer.getvalue()
