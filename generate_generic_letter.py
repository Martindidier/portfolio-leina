#!/usr/bin/env python3
"""Génère la lettre de motivation générique de Leïna Martin."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Flowable, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUTPUT = ASSETS / "Lettre_Motivation_Leina_Martin.pdf"
QR_PATH = ASSETS / "qrcode_portfolio.png"
PORTFOLIO_URL = "https://martindidier.github.io/portfolio-leina/"

NAVY = colors.HexColor("#102A43")
TEAL = colors.HexColor("#2A939B")
INK = colors.HexColor("#182531")
MUTED = colors.HexColor("#5F6F7D")
LINE = colors.HexColor("#D7E0E7")


class PortfolioFooter(Flowable):
    """QR Code et lien cliquable, posés directement sans conteneur."""

    def __init__(self, width: float):
        super().__init__()
        self.width = width
        self.height = 25 * mm

    def draw(self) -> None:
        pdf = self.canv
        pdf.saveState()
        qr_size = 16 * mm
        qr_x = (self.width - qr_size) / 2
        qr_y = 7 * mm
        pdf.drawImage(
            str(QR_PATH),
            qr_x,
            qr_y,
            qr_size,
            qr_size,
            preserveAspectRatio=True,
            mask="auto",
        )

        label = "Voir le Portfolio en ligne"
        label_y = 1.5 * mm
        pdf.setFillColor(NAVY)
        pdf.setFont("Helvetica-Bold", 9.2)
        pdf.drawCentredString(self.width / 2, label_y, label)

        pdf.linkURL(
            PORTFOLIO_URL,
            (qr_x, qr_y, qr_x + qr_size, qr_y + qr_size),
            relative=1,
            thickness=0,
        )
        pdf.linkURL(
            PORTFOLIO_URL,
            (
                self.width / 2 - 35 * mm,
                label_y - 1.5 * mm,
                self.width / 2 + 35 * mm,
                label_y + 4 * mm,
            ),
            relative=1,
            thickness=0,
        )
        pdf.restoreState()


def draw_page(canvas: Canvas, document: SimpleDocTemplate) -> None:
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 9 * mm, width, 9 * mm, stroke=0, fill=1)
    canvas.setFillColor(TEAL)
    canvas.rect(0, height - 10.5 * mm, width, 1.5 * mm, stroke=0, fill=1)
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(22 * mm, 15 * mm, width - 22 * mm, 15 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(22 * mm, 10.5 * mm, "LEÏNA MARTIN - CANDIDATURE DE STAGE")
    canvas.drawRightString(width - 22 * mm, 10.5 * mm, "2027")
    canvas.restoreState()


def build_letter() -> None:
    if not QR_PATH.is_file():
        raise FileNotFoundError(f"QR Code introuvable : {QR_PATH}")

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=22 * mm,
        leftMargin=22 * mm,
        topMargin=19 * mm,
        bottomMargin=20 * mm,
        title="Lettre de motivation - Leïna Martin",
        author="Leïna Martin",
        subject="Candidature pour un stage en graphisme, PAO et chaîne graphique",
    )
    styles = getSampleStyleSheet()
    identity = ParagraphStyle(
        "Identity",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=NAVY,
        spaceAfter=2,
    )
    contact = ParagraphStyle(
        "Contact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=11.4,
        textColor=MUTED,
    )
    recipient = ParagraphStyle(
        "Recipient",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.2,
        leading=12,
        textColor=INK,
        leftIndent=78 * mm,
        spaceBefore=7 * mm,
        spaceAfter=6 * mm,
    )
    subject = ParagraphStyle(
        "Subject",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=NAVY,
        spaceAfter=5 * mm,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.05,
        leading=12.05,
        textColor=INK,
        alignment=TA_LEFT,
        spaceAfter=2.8 * mm,
    )
    bullets = ParagraphStyle(
        "Bullets",
        parent=body,
        leftIndent=5 * mm,
        firstLineIndent=-3.5 * mm,
        spaceAfter=0.8 * mm,
    )
    signature = ParagraphStyle(
        "Signature",
        parent=body,
        fontName="Helvetica-Bold",
        textColor=NAVY,
        spaceBefore=0.5 * mm,
        spaceAfter=0,
    )

    story = [
        Paragraph("Leïna Martin", identity),
        Paragraph("07 44 73 29 81 | leina.m31410@gmail.com", contact),
        Paragraph("Élève en 1ère Bac Pro RPIP - Lycée Stéphane Hessel", contact),
        Paragraph("À l'attention du Responsable du recrutement / Direction", recipient),
        Paragraph("Objet : Candidature - Stage en graphisme, PAO et chaîne graphique", subject),
        Paragraph("Madame, Monsieur,", body),
        Paragraph(
            "Actuellement élève en Première Bac Pro RPIP (Réalisation de Produits Imprimés et Plurimédia) option Graphisme au lycée Stéphane Hessel de Toulouse, je suis à la recherche d'un stage pratique au sein d'une structure professionnelle pour développer mes compétences sur le terrain.",
            body,
        ),
        Paragraph(
            "Dans le cadre de mon cursus, je dois valider deux périodes de stage en entreprise :",
            body,
        ),
        Paragraph("- Du 11 janvier au 5 février 2027 (4 semaines)", bullets),
        Paragraph("- Du 7 juin au 2 juillet 2027 (4 semaines)", bullets),
        Spacer(1, 1 * mm),
        Paragraph(
            "Je souhaite poser ma candidature pour l'une ou l'autre de ces périodes, selon vos disponibilités et votre charge de travail.",
            body,
        ),
        Paragraph(
            "Issue d'un premier parcours en communication visuelle plurimédia dans le même établissement, j'ai choisi la filière RPIP pour me spécialiser dans le travail sur informatique et la maîtrise de la chaîne graphique (logiciels de PAO, mise en page, création vectorielle et préparation de fichiers pour l'impression).",
            body,
        ),
        Paragraph(
            "Sérieuse, appliquée et dynamique, je serais ravie d'apporter ma contribution à votre équipe tout en découvrant vos méthodes de production. Vous trouverez ci-joint mon portfolio présentant plusieurs travaux informatiques réalisés au cours de ma formation (conception de packaging sous Illustrator et mise en page éditoriale sous InDesign).",
            body,
        ),
        Paragraph(
            "Internée à Toulouse durant mes semaines de cours et de stage, je bénéficie d'une totale autonomie logistique et d'une pleine disponibilité au quotidien.",
            body,
        ),
        Paragraph(
            "Je reste à votre entière disposition pour un entretien afin de vous présenter de vive voix ma motivation et mon projet professionnel.",
            body,
        ),
        Paragraph(
            "Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.",
            body,
        ),
        Paragraph("Leïna Martin", signature),
        Spacer(1, 4 * mm),
        PortfolioFooter(document.width),
    ]
    document.build(story, onFirstPage=draw_page, onLaterPages=draw_page)


if __name__ == "__main__":
    build_letter()
