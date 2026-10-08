#!/usr/bin/env python3
"""Génère la lettre de motivation ciblée pour TAT Productions."""

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
OUTPUT = ASSETS / "Lettre_Motivation_TAT_Productions.pdf"
QR_PATH = ASSETS / "qrcode_portfolio.png"
PORTFOLIO_URL = "https://martindidier.github.io/portfolio-leina/"

NAVY = colors.HexColor("#102A43")
TEAL = colors.HexColor("#2A939B")
INK = colors.HexColor("#182531")
MUTED = colors.HexColor("#5F6F7D")
PAPER = colors.HexColor("#F3F6F8")
LINE = colors.HexColor("#D7E0E7")


class PortfolioCard(Flowable):
    """QR Code et lien cliquable, sans encadré décoratif."""

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
    canvas.drawString(22 * mm, 10.5 * mm, "LEÏNA MARTIN - CANDIDATURE TAT PRODUCTIONS")
    canvas.drawRightString(width - 22 * mm, 10.5 * mm, "STAGES 2027")
    canvas.restoreState()


def build_letter() -> None:
    if not QR_PATH.is_file():
        raise FileNotFoundError(f"QR Code introuvable : {QR_PATH}")

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=22 * mm,
        leftMargin=22 * mm,
        topMargin=18 * mm,
        bottomMargin=20 * mm,
        title="Lettre de motivation - TAT Productions - Leïna Martin",
        author="Leïna Martin",
        subject="Candidature pour deux périodes de stage en 2027",
    )
    styles = getSampleStyleSheet()
    identity = ParagraphStyle(
        "Identity",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14.5,
        leading=17,
        textColor=NAVY,
        spaceAfter=1,
    )
    contact = ParagraphStyle(
        "Contact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.6,
        leading=11,
        textColor=MUTED,
    )
    recipient = ParagraphStyle(
        "Recipient",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.9,
        leading=11.5,
        textColor=INK,
        leftIndent=76 * mm,
        spaceBefore=5 * mm,
        spaceAfter=4 * mm,
    )
    subject = ParagraphStyle(
        "Subject",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.25,
        leading=11.5,
        textColor=NAVY,
        spaceAfter=3.8 * mm,
    )
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.75,
        leading=11.45,
        textColor=INK,
        alignment=TA_LEFT,
        spaceAfter=2.35 * mm,
    )
    recommendation = ParagraphStyle(
        "Recommendation",
        parent=body,
        fontName="Helvetica-Bold",
        textColor=NAVY,
        leftIndent=4 * mm,
        borderColor=TEAL,
        borderWidth=0,
        borderPadding=(0, 0, 0, 3 * mm),
        spaceAfter=2.8 * mm,
    )
    bullets = ParagraphStyle(
        "Bullets",
        parent=body,
        leftIndent=5 * mm,
        firstLineIndent=-3.5 * mm,
        spaceAfter=0.7 * mm,
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
        Paragraph("Élève en 1ère Bac Pro RPIP – Lycée Stéphane Hessel", contact),
        Paragraph(
            "À l'attention du Service Recrutement / Communication<br/><b>TAT Productions — Toulouse</b>",
            recipient,
        ),
        Paragraph(
            "Objet : Candidature – Stage en graphisme / PAO (Janvier-Février 2027 ou Juin-Juillet 2027)",
            subject,
        ),
        Paragraph("Madame, Monsieur,", body),
        Paragraph(
            "Actuellement élève en Première Bac Pro RPIP (Réalisation de Produits Imprimés et Plurimédia) option Graphisme au lycée Stéphane Hessel de Toulouse, c'est avec un grand enthousiasme que je sollicite un stage au sein de votre service communication.",
            body,
        ),
        Paragraph(
            "Dans le cadre de ma formation, je dois effectuer deux périodes de stage en entreprise :",
            body,
        ),
        Paragraph("- Du 11 janvier au 5 février 2027 (4 semaines)", bullets),
        Paragraph("- Du 7 juin au 2 juillet 2027 (4 semaines)", bullets),
        Spacer(1, 0.8 * mm),
        Paragraph(
            "Je souhaite poser ma candidature pour la première session de janvier, mais je reste pleinement disponible pour la session de juin si le planning de votre studio s'y prête davantage.",
            body,
        ),
        Paragraph(
            "Après un premier parcours au lycée en communication visuelle plurimédia, j'ai choisi de m'orienter vers la filière RPIP pour me spécialiser dans le travail sur informatique et la chaîne graphique (logiciels PAO, traitement d'image, préparation des fichiers pour impression). Passionnée par l'univers visuel de TAT Productions, je serais ravie de mettre ma sensibilité créative et mes compétences au service de vos projets.",
            body,
        ),
        Paragraph(
            "Vous trouverez ci-joint mon portfolio présentant deux travaux réalisés sur Illustrator et InDesign (un packaging et une mise en page éditoriale).",
            body,
        ),
        Paragraph(
            "Internée à Toulouse durant mes semaines de cours et de stage, je bénéficie d'une totale autonomie et disponibilité logistique au quotidien.",
            body,
        ),
        Paragraph(
            "Sur les conseils de M. Damien Martin, membre de votre studio, je vous adresse ma candidature et me tiens à votre entière disposition pour un entretien.",
            body,
        ),
        Paragraph(
            "Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.",
            body,
        ),
        Paragraph("Leïna Martin", signature),
        Spacer(1, 3.5 * mm),
        PortfolioCard(document.width),
    ]
    document.build(story, onFirstPage=draw_page, onLaterPages=draw_page)


if __name__ == "__main__":
    build_letter()
