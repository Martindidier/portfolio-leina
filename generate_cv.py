#!/usr/bin/env python3
"""Génère le CV A4 de Leïna Martin avec ReportLab."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
OUTPUT = ASSETS / "CV_Leina_Martin.pdf"
QR_PATH = ASSETS / "qrcode_portfolio.png"
PORTFOLIO_URL = "https://martindidier.github.io/portfolio-leina/"

PAGE_W, PAGE_H = A4
NAVY = colors.HexColor("#102A43")
NAVY_DARK = colors.HexColor("#091C2D")
TEAL = colors.HexColor("#2A939B")
TEAL_LIGHT = colors.HexColor("#57C3C9")
INK = colors.HexColor("#182531")
MUTED = colors.HexColor("#5F6F7D")
PAPER = colors.HexColor("#F3F6F8")
LINE = colors.HexColor("#D7E0E7")
WHITE = colors.white


def paragraph_style(
    name: str,
    *,
    font: str = "Helvetica",
    size: float = 8.4,
    leading: float = 11.2,
    color=INK,
    left_indent: float = 0,
    first_indent: float = 0,
) -> ParagraphStyle:
    return ParagraphStyle(
        name,
        fontName=font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=TA_LEFT,
        leftIndent=left_indent,
        firstLineIndent=first_indent,
    )


def draw_paragraph(pdf, html, style, x, top_y, width):
    paragraph = Paragraph(html, style)
    _, height = paragraph.wrap(width, PAGE_H)
    paragraph.drawOn(pdf, x, top_y - height)
    return top_y - height


def draw_section_title(pdf, title, x, y, width, *, light=False):
    color = TEAL_LIGHT if light else TEAL
    pdf.setFillColor(color)
    pdf.setFont("Helvetica-Bold", 9.3)
    pdf.drawString(x, y, title.upper())
    pdf.setStrokeColor(color)
    pdf.setLineWidth(1.2)
    pdf.line(x, y - 2.5 * mm, x + width, y - 2.5 * mm)
    return y - 7 * mm


def draw_portfolio_block(pdf, x, top_y, width):
    top_y = draw_section_title(pdf, "Portfolio web", x, top_y, width, light=True)
    qr_size = 20 * mm
    qr_x = x + (width - qr_size) / 2
    qr_y = top_y - qr_size
    pdf.drawImage(
        str(QR_PATH),
        qr_x,
        qr_y,
        qr_size,
        qr_size,
        preserveAspectRatio=True,
        mask="auto",
    )

    label_y = qr_y - 5 * mm
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 7.8)
    pdf.drawCentredString(x + width / 2, label_y, "Voir le Portfolio en ligne")

    pdf.linkURL(
        PORTFOLIO_URL,
        (qr_x, qr_y, qr_x + qr_size, qr_y + qr_size),
        relative=0,
        thickness=0,
    )
    pdf.linkURL(
        PORTFOLIO_URL,
        (x, label_y - 2 * mm, x + width, label_y + 3 * mm),
        relative=0,
        thickness=0,
    )
    return label_y - 8 * mm


def build_cv() -> None:
    if not QR_PATH.is_file():
        raise FileNotFoundError(f"QR Code introuvable : {QR_PATH}")

    pdf = canvas.Canvas(str(OUTPUT), pagesize=A4)
    pdf.setTitle("CV - Leïna Martin")
    pdf.setAuthor("Leïna Martin")
    pdf.setSubject("CV - Graphisme, PAO et chaîne graphique")

    sidebar_w = 68 * mm
    margin = 13 * mm
    right_x = sidebar_w + 13 * mm
    right_w = PAGE_W - right_x - margin

    pdf.setFillColor(PAPER)
    pdf.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    pdf.setFillColor(NAVY_DARK)
    pdf.rect(0, 0, sidebar_w, PAGE_H, stroke=0, fill=1)
    pdf.setFillColor(TEAL)
    pdf.rect(sidebar_w, PAGE_H - 6 * mm, PAGE_W - sidebar_w, 6 * mm, stroke=0, fill=1)

    # En-tête.
    header_y = PAGE_H - 24 * mm
    pdf.setFillColor(NAVY)
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawString(right_x, header_y, "LEÏNA MARTIN")
    pdf.setFillColor(TEAL)
    pdf.setFont("Helvetica-Bold", 10.5)
    pdf.drawString(right_x, header_y - 8 * mm, "ÉLÈVE EN 1ÈRE BAC PRO RPIP")
    pdf.setFillColor(MUTED)
    pdf.setFont("Helvetica", 9.5)
    pdf.drawString(right_x, header_y - 14 * mm, "Option Graphisme & PAO")
    pdf.setStrokeColor(LINE)
    pdf.line(right_x, header_y - 20 * mm, PAGE_W - margin, header_y - 20 * mm)

    body = paragraph_style("Body")
    body_small = paragraph_style("BodySmall", size=8.0, leading=10.5)
    skill = paragraph_style("Skill", size=8.15, leading=10.7)
    sidebar_body = paragraph_style(
        "SidebarBody", size=8.15, leading=10.5, color=colors.HexColor("#D8E4EA")
    )
    sidebar_link = paragraph_style("SidebarLink", size=8.0, leading=10.5, color=WHITE)
    sidebar_bullet = paragraph_style(
        "SidebarBullet",
        size=8.0,
        leading=10.4,
        color=colors.HexColor("#D8E4EA"),
        left_indent=3.6 * mm,
        first_indent=-3.6 * mm,
    )

    # Colonne gauche : informations essentielles uniquement.
    left_x = 11 * mm
    left_w = sidebar_w - 22 * mm
    left_y = PAGE_H - 20 * mm
    pdf.setFillColor(WHITE)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(left_x, left_y, "PROFIL")
    pdf.setFillColor(TEAL_LIGHT)
    pdf.rect(left_x, left_y - 5 * mm, 18 * mm, 1.2 * mm, stroke=0, fill=1)
    left_y -= 13 * mm

    left_y = draw_section_title(pdf, "Contact", left_x, left_y, left_w, light=True)
    left_y = draw_paragraph(
        pdf,
        '<link href="tel:0744732981" color="#FFFFFF"><b>07 44 73 29 81</b></link>',
        sidebar_link,
        left_x,
        left_y,
        left_w,
    ) - 2 * mm
    left_y = draw_paragraph(
        pdf,
        '<link href="mailto:leina.m31410@gmail.com" color="#FFFFFF"><b>leina.m31410@gmail.com</b></link>',
        sidebar_link,
        left_x,
        left_y,
        left_w,
    ) - 2 * mm
    left_y = draw_paragraph(
        pdf,
        "4 Grande rue du prieure<br/>31410 Longages",
        sidebar_body,
        left_x,
        left_y,
        left_w,
    ) - 7 * mm

    left_y = draw_portfolio_block(pdf, left_x, left_y, left_w)

    left_y = draw_section_title(pdf, "Stages 2027", left_x, left_y, left_w, light=True)
    left_y = draw_paragraph(
        pdf,
        "<b>Période 1</b><br/>11 janv. - 5 fév. 2027<br/>(4 semaines)",
        sidebar_body,
        left_x,
        left_y,
        left_w,
    ) - 3 * mm
    left_y = draw_paragraph(
        pdf,
        "<b>Période 2</b><br/>7 juin - 2 juil. 2027<br/>(4 semaines)",
        sidebar_body,
        left_x,
        left_y,
        left_w,
    ) - 8 * mm

    left_y = draw_section_title(pdf, "Langues", left_x, left_y, left_w, light=True)
    for item in ("- Français", "- Anglais", "- Espagnol"):
        left_y = draw_paragraph(pdf, item, sidebar_bullet, left_x, left_y, left_w) - 0.6 * mm
    left_y -= 7 * mm

    left_y = draw_section_title(pdf, "Loisirs", left_x, left_y, left_w, light=True)
    draw_paragraph(
        pdf,
        "Photographie<br/>Mode<br/>Boxe Thaïlandaise<br/>Football",
        sidebar_body,
        left_x,
        left_y,
        left_w,
    )

    # Colonne principale.
    right_y = header_y - 29 * mm
    right_y = draw_section_title(pdf, "Compétences techniques & PAO", right_x, right_y, right_w)
    skills = (
        "<b>Adobe Illustrator</b> - Vectorisation et packaging : Boîte de chocolat.",
        "<b>Adobe InDesign</b> - Mise en page éditoriale et grille magazine.",
        "<b>Adobe Photoshop</b> - Retouche et préparation d'images.",
        "<b>Chaîne graphique</b> - Préparation de fichiers pour l'impression : CMJN, fonds perdus, traits de coupe et typographie.",
    )
    for item in skills:
        right_y = draw_paragraph(pdf, item, skill, right_x, right_y, right_w) - 2.2 * mm
    right_y -= 5 * mm

    right_y = draw_section_title(pdf, "Expériences & stages", right_x, right_y, right_w)
    experiences = (
        ("Aerrotec & Concept", "Blagnac", "Stage de communication"),
        ("Les Nuances de Céline", "Longages", "Stage clientèle"),
        ("Roady Garage", "Muret", "Stage clientèle & vente"),
        ("Hôtel de l'Arche", "Noé", "Stage clientèle & restauration"),
    )
    for company, city, description in experiences:
        right_y = draw_paragraph(
            pdf,
            f'<b>{company}</b> <font color="#5F6F7D">- {city}</font><br/><font color="#5F6F7D">{description}</font>',
            body_small,
            right_x,
            right_y,
            right_w,
        ) - 2.2 * mm
    right_y -= 5 * mm

    right_y = draw_section_title(pdf, "Formation & diplômes", right_x, right_y, right_w)
    right_y = draw_paragraph(
        pdf,
        '<b>2026-2027</b> - 1ère Bac Pro RPIP, option Graphisme<br/><font color="#5F6F7D">Lycée Stéphane Hessel, Toulouse</font>',
        body,
        right_x,
        right_y,
        right_w,
    ) - 3 * mm
    right_y = draw_paragraph(
        pdf,
        '<b>2025-2026</b> - 2de Pro Communication Visuelle Plurimédia<br/><font color="#5F6F7D">Lycée Stéphane Hessel, Toulouse</font>',
        body,
        right_x,
        right_y,
        right_w,
    ) - 3 * mm
    draw_paragraph(
        pdf,
        "<b>Diplômes et certifications</b><br/>Brevet des collèges - Lycée Charles de Gaulle, Muret<br/>PSC1 (Secourisme) - ASSR1 & ASSR2",
        body,
        right_x,
        right_y,
        right_w,
    )

    pdf.save()


if __name__ == "__main__":
    build_cv()
