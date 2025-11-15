from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import os

def _register_cn_font():
    candidates = [
        r"C:\\Windows\\Fonts\\simhei.ttf",
        r"C:\\Windows\\Fonts\\msyh.ttf",
        r"/usr/share/fonts/truetype/arphic/uming.ttc",
        r"/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(TTFont("CNFont", path))
                return "CNFont"
            except Exception:
                continue
    return "Helvetica"

def _build_styles(base_font):
    styles = getSampleStyleSheet()
    for name in ["Normal", "Heading1", "Heading2", "Heading3"]:
        styles[name].fontName = base_font
    styles.add(ParagraphStyle(name="List", fontName=base_font, leading=16, fontSize=11, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name="Body", fontName=base_font, leading=18, fontSize=11, alignment=TA_LEFT))
    styles["Heading1"].fontSize = 18
    styles["Heading2"].fontSize = 16
    styles["Heading3"].fontSize = 14
    return styles

def markdown_to_pdf(markdown_text: str, output_pdf_path: str, images: list = None):
    base_font = _register_cn_font()
    styles = _build_styles(base_font)
    doc = SimpleDocTemplate(output_pdf_path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    flow = []

    # 预处理：移除HTML换行与代码围栏
    cleaned = (
        markdown_text.replace('<br/>', ' ').replace('<br />', ' ').replace('<br>', ' ')
        .replace('```json', '```').replace('```', '')
        .replace('`', '')
    )
    lines = cleaned.splitlines()
    list_buffer = []

    def flush_list():
        nonlocal list_buffer
        if list_buffer:
            items = [ListItem(Paragraph(item, styles["Body"])) for item in list_buffer]
            flow.append(ListFlowable(items, bulletType='bullet'))
            list_buffer = []

    for raw in lines:
        line = raw.strip()
        if not line:
            flush_list()
            flow.append(Spacer(1, 8))
            continue
        if line.startswith("### "):
            flush_list()
            flow.append(Paragraph(line[4:], styles["Heading3"]))
            flow.append(Spacer(1, 6))
        elif line.startswith("## "):
            flush_list()
            flow.append(Paragraph(line[3:], styles["Heading2"]))
            flow.append(Spacer(1, 8))
        elif line.startswith("# "):
            flush_list()
            flow.append(Paragraph(line[2:], styles["Heading1"]))
            flow.append(Spacer(1, 10))
        elif line.startswith(('- ', '* ')):
            list_buffer.append(line[2:])
        else:
            # 简单处理表格行：去除竖线并以逗号分隔
            if line.startswith('|') and line.endswith('|'):
                cells = [c.strip() for c in line.strip('|').split('|')]
                line = ', '.join([c for c in cells if c])
            flush_list()
            flow.append(Paragraph(line, styles["Body"]))
            flow.append(Spacer(1, 4))

    flush_list()

    if images:
        flow.append(PageBreak())
        flow.append(Paragraph("图表附录", styles["Heading2"]))
        flow.append(Spacer(1, 10))
        for img in images:
            if os.path.exists(img):
                try:
                    flow.append(Image(img, width=16*cm, height=10*cm))
                    flow.append(Spacer(1, 8))
                except Exception:
                    continue

    doc.build(flow)
