"""Generate the course decks from Markdown using the supplied Xebia layouts."""

import argparse
from copy import deepcopy
import hashlib
import json
import re
from pathlib import Path

from PIL import ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.enum.shapes import PP_PLACEHOLDER
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Emu, Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
NOTES = re.compile(r"<!-- notes:\s*(.*?)\s*-->", re.DOTALL)
FONT_NAME = "Arial"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plain(text):
    return LINK.sub(r"\1", text).replace("`", "")


def read_slides(path):
    slides = []
    for index, chunk in enumerate(re.split(r"(?m)^---\s*$", path.read_text(encoding="utf-8")), 1):
        notes = NOTES.findall(chunk)
        if len(notes) != 1:
            raise ValueError(f"{path.name}, slide {index}: expected exactly one notes block")
        teaching, separator, material = NOTES.sub("", chunk).strip().partition("\n## ")
        lines = [line.strip() for line in teaching.splitlines() if line.strip()]
        if not lines or not lines[0].startswith("# ") or any(not line.startswith("- ") for line in lines[1:]):
            raise ValueError(f"{path.name}, slide {index}: unsupported Markdown structure")
        support = None
        if separator:
            caption, _, payload = material.partition("\n")
            payload = payload.strip()
            fenced = re.fullmatch(r"```(yaml|bash|text|flow|gates|scatter|qr)\n(.*?)\n```", payload, re.DOTALL)
            if fenced:
                kind, value = fenced.groups()
                support = {"caption": plain(caption), "kind": kind, "value": value}
            elif payload.startswith("|"):
                rows = [[plain(cell.strip()) for cell in line.strip("|").split("|")] for line in payload.splitlines()]
                if len(rows) < 3 or not all(re.fullmatch(r":?-+:?", cell) for cell in rows[1]):
                    raise ValueError(f"{path.name}, slide {index}: malformed table")
                rows.pop(1)
                if any(len(row) != len(rows[0]) for row in rows):
                    raise ValueError(f"{path.name}, slide {index}: inconsistent table columns")
                support = {"caption": plain(caption), "kind": "table", "value": rows}
            else:
                raise ValueError(f"{path.name}, slide {index}: unsupported supporting material")
        slides.append({
            "title": plain(lines[0][2:]),
            "bullets": [plain(line[2:]) for line in lines[1:]],
            "notes": notes[0].strip(),
            "support": support,
        })
    return slides


def wrap_lines(text, width_points, size, font_path):
    font = ImageFont.truetype(str(font_path), size * 4)
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if font.getlength(candidate) / 4 > width_points:
            if not current or font.getlength(word) / 4 > width_points:
                raise ValueError(f"Unbreakable text does not fit: {word}")
            lines.append(current)
            current = word
        else:
            current = candidate
    return [*lines, current]


def line_count(text, width_points, size, font_path):
    return len(wrap_lines(text, width_points, size, font_path))


def set_text(shape, lines, size, color, *, bold=False, bullets=False, font_name=FONT_NAME):
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.auto_size = MSO_AUTO_SIZE.NONE
    frame.margin_left = frame.margin_right = 0
    frame.margin_top = frame.margin_bottom = 0
    for index, text in enumerate(lines):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = text
        paragraph.line_spacing = 1.15
        paragraph.space_before = Pt(0)
        paragraph.space_after = Pt(14 if bullets else 0)
        paragraph.font.name = font_name
        paragraph.font.size = Pt(size)
        paragraph.font.bold = bold
        props = paragraph._p.get_or_add_pPr()
        for item in list(props):
            if item.tag.endswith(("}buNone", "}buChar", "}buAutoNum")):
                props.remove(item)
        bullet = OxmlElement("a:buChar" if bullets else "a:buNone")
        if bullets:
            bullet.set("char", "\u2022")
            props.set("marL", str(Inches(0.24)))
            props.set("indent", str(-Inches(0.24)))
        props.append(bullet)
        for run in paragraph.runs:
            run.font.name = font_name
            run.font.size = Pt(size)
            run.font.bold = bold
            run.font.color.rgb = RGBColor.from_string(color)
            run._r.get_or_add_rPr().set("lang", "en-US")

def add_support(slide, support, top, font_path):
    shapes = []

    def label(name, text, left, y, width, height, size, color, bold=False, font_name=FONT_NAME):
        shape = slide.shapes.add_textbox(Inches(left), y, Inches(width), height)
        shape.name = name
        set_text(shape, text.split("\n"), size, color, bold=bold, font_name=font_name)
        shapes.append(shape)
        return shape

    label("Example caption", support["caption"], 0.45, top, 12, Pt(28), 18, "611562", True)
    top += Pt(34)
    height = Emu(Inches(6.7) - top)
    kind, value = support["kind"], support["value"]
    if kind == "table":
        rows, columns = len(value), len(value[0])
        size = 18 if rows >= 5 else 20
        table_shape = slide.shapes.add_table(rows, columns, Inches(0.45), top, Inches(12), height)
        table_shape.name = "Example table"
        shapes.append(table_shape)
        for r, row in enumerate(value):
            lines = max(line_count(text, 12 * 72 / columns - 26, size, font_path) for text in row)
            table_shape.table.rows[r].height = Pt(lines * size * 1.4 + 8)
            for c, text in enumerate(row):
                cell = table_shape.table.cell(r, c)
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor.from_string("611562" if r == 0 else ("FBF7F7" if r % 2 else "EEE6F0"))
                cell.margin_left = cell.margin_right = Inches(0.12)
                cell.margin_top = cell.margin_bottom = Pt(3)
                wrapped = "\v".join(wrap_lines(text, 12 * 72 / columns - 26, size, font_path))
                set_text(cell, [wrapped], size, "FFFFFF" if r == 0 else "130025", bold=r == 0)
        if table_shape.height > height:
            raise ValueError(f"Example table is too tall: {support['caption']}")
    elif kind == "qr":
        cards = [line.split(" | ", 1) for line in value.splitlines()]
        if not 1 <= len(cards) <= 2 or any(len(card) != 2 for card in cards):
            raise ValueError("QR placeholders require one or two 'label | instruction' lines")
        for i, (heading, instruction) in enumerate(cards):
            left = 0.45 + i * 6.2
            label(f"QR heading {i}", heading, left, top, 5.8, Pt(32), 22, "611562", True)
            side = min(Inches(2.4), height - Pt(92))
            if side < Inches(1.5):
                raise ValueError("QR placeholder has insufficient space")
            panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), top + Pt(38), side, side)
            panel.name = f"QR placeholder {i}"
            panel.fill.solid()
            panel.fill.fore_color.rgb = RGBColor.from_string("FBF7F7")
            panel.line.color.rgb = RGBColor.from_string("611562")
            set_text(panel, ["ADD QR", "HERE"], 18, "611562", bold=True)
            shapes.append(panel)
            label(f"QR instruction {i}", instruction, left, top + Pt(44) + side, 5.8, Pt(44), 18, "130025")
    elif kind == "flow":
        cards = [line.split(" | ", 1) for line in value.splitlines()]
        width = (12 - (len(cards) - 1) * 0.45) / len(cards)
        for i, card in enumerate(cards):
            if len(card) != 2:
                raise ValueError("Flow cards require 'heading | explanation'")
            left = 0.45 + i * (width + 0.45)
            panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), top, Inches(width), height)
            panel.fill.solid()
            panel.fill.fore_color.rgb = RGBColor.from_string("FBF7F7")
            panel.line.color.rgb = RGBColor.from_string("611562")
            shapes.append(panel)
            heading = "\n".join(wrap_lines(card[0], (width - 0.35) * 72 - 12, 22, font_path))
            label(f"Flow heading {i}", heading, left + 0.17, top + Pt(16), width - 0.34, Pt(75), 22, "611562", True)
            detail = "\n".join(wrap_lines(card[1], (width - 0.35) * 72 - 12, 20, font_path))
            label(f"Flow detail {i}", detail, left + 0.17, top + Pt(85), width - 0.34, height - Pt(100), 20, "130025")
            if i < len(cards) - 1:
                arrow = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(left + width + 0.1), top + height // 2 - Pt(10), Inches(0.25), Pt(20))
                arrow.fill.solid()
                arrow.fill.fore_color.rgb = RGBColor.from_string("611562")
                arrow.line.fill.background()
                shapes.append(arrow)
    elif kind == "gates":
        cards = [line.split(" | ", 1) for line in value.splitlines()]
        if len(cards) != 4 or any(len(card) != 2 or not all(part.strip() for part in card) for card in cards):
            raise ValueError("Gate diagrams require three rules and one outcome")
        gap = 0.25
        width = (12 - 2 * gap) / 3
        card_height = Pt(100)
        join_top = top + card_height + Pt(10)
        outcome_top = top + card_height + Pt(30)
        outcome_height = height - Pt(130)
        if outcome_height < Pt(40):
            raise ValueError("Gate diagram has insufficient space")
        centers = []
        for i, (heading, detail) in enumerate(cards[:3]):
            left = 0.45 + i * (width + gap)
            centers.append(Inches(left + width / 2))
            panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), top, Inches(width), card_height)
            panel.name = f"Gate rule {i + 1}"
            panel.fill.solid()
            panel.fill.fore_color.rgb = RGBColor.from_string("FBF7F7")
            panel.line.color.rgb = RGBColor.from_string("611562")
            shapes.append(panel)
            heading = "\n".join(wrap_lines(heading, (width - 0.34) * 72 - 12, 18, font_path))
            detail = "\n".join(wrap_lines(detail, (width - 0.34) * 72 - 12, 17, font_path))
            label(f"Gate heading {i}", heading, left + 0.17, top + Pt(10), width - 0.34, Pt(24), 18, "611562", True)
            label(f"Gate detail {i}", detail, left + 0.17, top + Pt(35), width - 0.34, Pt(60), 17, "130025")
        for i, center in enumerate(centers):
            connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, center, top + card_height, center, join_top)
            connector.name = f"Gate input {i + 1}"
            connector.line.color.rgb = RGBColor.from_string("611562")
            connector.line.width = Pt(1.5)
            shapes.append(connector)
        for name, x1, y1, x2, y2 in (
            ("Gate join", centers[0], join_top, centers[2], join_top),
            ("Gate outcome connector", centers[1], join_top, centers[1], outcome_top),
        ):
            connector = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
            connector.name = name
            connector.line.color.rgb = RGBColor.from_string("611562")
            connector.line.width = Pt(1.5)
            shapes.append(connector)
        panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.45), outcome_top, Inches(12), outcome_height)
        panel.name = "Gate outcome"
        panel.fill.solid()
        panel.fill.fore_color.rgb = RGBColor.from_string("611562")
        panel.line.color.rgb = RGBColor.from_string("611562")
        shapes.append(panel)
        label("Gate heading 3", cards[3][0], 0.65, outcome_top + Pt(10), 1.6, outcome_height - Pt(16), 20, "FFFFFF", True)
        label("Gate detail 3", cards[3][1], 2.45, outcome_top + Pt(10), 9.7, outcome_height - Pt(16), 20, "FFFFFF")
    elif kind == "scatter":
        cards = [line.split(" | ", 1) for line in value.splitlines()]
        if len(cards) != 8 or any(len(card) != 2 for card in cards):
            raise ValueError("Scatter diagrams require six jobs, results, and gate cards")
        label("Scatter limit", "max-parallel: 3", 0.45, top, 12, Pt(24), 18, "611562", True)
        job_top = top + Pt(26)
        card_width, card_height = 3.65, Pt(48)
        group = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.35), job_top - Pt(5), Inches(12.2), Pt(116)
        )
        group.name = "Scatter job group"
        group.fill.background()
        group.line.color.rgb = RGBColor.from_string("B998B9")
        shapes.append(group)
        for index, (heading, detail) in enumerate(cards[:6]):
            row, column = divmod(index, 3)
            left = 0.45 + column * 4.15
            y = job_top + row * Pt(58)
            panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), y, Inches(card_width), card_height)
            panel.name = f"Scatter job {index + 1}"
            panel.fill.solid()
            panel.fill.fore_color.rgb = RGBColor.from_string("FBF7F7")
            panel.line.color.rgb = RGBColor.from_string("611562")
            shapes.append(panel)
            label(f"Scatter job heading {index + 1}", heading, left + 0.12, y + Pt(5), card_width - 0.24, Pt(19), 15, "611562", True)
            label(f"Scatter job detail {index + 1}", detail, left + 0.12, y + Pt(26), card_width - 0.24, Pt(16), 14, "130025")
        gather_top = job_top + Pt(126)
        gather_height = height - Pt(152)
        gather_arrow = slide.shapes.add_shape(
            MSO_SHAPE.DOWN_ARROW,
            Inches(0.45 + 5.55 / 2 - 0.09),
            job_top + Pt(111),
            Inches(0.18),
            Pt(14),
        )
        gather_arrow.name = "Scatter gather arrow"
        gather_arrow.fill.solid()
        gather_arrow.fill.fore_color.rgb = RGBColor.from_string("611562")
        gather_arrow.line.fill.background()
        shapes.append(gather_arrow)
        for index, (heading, detail) in enumerate(cards[6:]):
            width = 5.55
            left = 0.45 + index * 6.05
            panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), gather_top, Inches(width), gather_height)
            panel.name = "Scatter results" if index == 0 else "Scatter required gate"
            panel.fill.solid()
            panel.fill.fore_color.rgb = RGBColor.from_string("EEE6F0" if index == 0 else "611562")
            panel.line.color.rgb = RGBColor.from_string("611562")
            shapes.append(panel)
            color = "130025" if index == 0 else "FFFFFF"
            heading_color = "611562" if index == 0 else "FFFFFF"
            label(f"Scatter gather heading {index + 1}", heading, left + 0.15, gather_top + Pt(10), width - 0.3, Pt(24), 18, heading_color, True)
            label(f"Scatter gather detail {index + 1}", detail, left + 0.15, gather_top + Pt(38), width - 0.3, gather_height - Pt(46), 15, color)
            if index == 0:
                arrow = slide.shapes.add_shape(MSO_SHAPE.CHEVRON, Inches(left + width + 0.1), gather_top + Pt(27), Inches(0.25), Pt(20))
                arrow.fill.solid()
                arrow.fill.fore_color.rgb = RGBColor.from_string("611562")
                arrow.line.fill.background()
                shapes.append(arrow)
    else:
        panel = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.45), top, Inches(12), height)
        panel.fill.solid()
        panel.fill.fore_color.rgb = RGBColor.from_string("130025")
        panel.line.fill.background()
        shapes.append(panel)
        code = label("Example code", value, 0.65, top + Pt(12), 11.6, height - Pt(24), 18, "FFFFFF", font_name="Consolas")
        code.text_frame.word_wrap = False
        for paragraph in code.text_frame.paragraphs:
            paragraph.line_spacing = 1.05
        font = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 72)
        if max(font.getlength(line) / 4 for line in value.splitlines()) > 11.6 * 72:
            raise ValueError("Example code is too wide at 18 points")
        if len(value.splitlines()) * 18 * 1.05 > height.pt - 24:
            raise ValueError("Example code is too tall at 18 points")
    return shapes


def copy_geometry(shape, original):
    shape.left = original.left
    shape.top = original.top
    shape.width = original.width
    shape.height = original.height


def remove_sample_slides(prs):
    for slide_id in list(prs.slides._sldIdLst):
        prs.part.drop_rel(slide_id.rId)
        prs.slides._sldIdLst.remove(slide_id)
    # Guidance sections refer to the removed sample slide IDs.
    for extension in list(prs._element.xpath("./p:extLst/p:ext")):
        if any("sectionLst" in child.tag for child in extension.iter()):
            extension.getparent().remove(extension)
    custom_shows = prs._element.xpath("./p:custShowLst")
    for item in custom_shows:
        item.getparent().remove(item)
    if not any(
        shape.is_placeholder and shape.placeholder_format.type == PP_PLACEHOLDER.BODY
        for shape in prs.notes_master.shapes
    ):
        # This guidance deck has an empty notes master. Supply real notes
        # placeholders so PowerPoint exposes notes rather than a plain textbox.
        for shape in Presentation().notes_master.shapes:
            prs.notes_master.shapes._spTree.append(deepcopy(shape._element))


def add_slide(prs, content, module, index, total, font_path, bold_font_path):
    dark = index == 1 or content["title"].startswith(("Debrief:", "Capstone:", "Review:", "Final exercise:"))
    layout_name = "Title Content/Dark" if dark else "Title Content/White"
    layout = next(layout for layout in prs.slide_layouts if layout.name == layout_name)
    slide = prs.slides.add_slide(layout)
    for shape in slide.placeholders:
        original = next(
            ph for ph in layout.placeholders
            if ph.placeholder_format.idx == shape.placeholder_format.idx
        )
        copy_geometry(shape, original)
    title = slide.shapes.title
    body = slide.placeholders[110]
    header = slide.placeholders[106]
    color = "FFFFFF" if dark else "130025"
    title_color = "FFFFFF" if dark else "611562"
    title_size = 54 if index == 1 else 36
    title.width = Inches(12)
    title_text = wrap_lines(content["title"], 12 * 72 - 24, title_size, bold_font_path)
    title_lines = len(title_text)
    title.height = Pt(title_lines * title_size * 1.4 + 8)
    set_text(title, ["\v".join(title_text)], title_size, title_color, bold=True)
    title.name = "Slide title"
    body.top = title.top + title.height + Inches(0.35)
    body.height = Inches(6.75) - body.top
    body.width = Inches(11.5)
    body.name = "Teaching points"
    set_text(body, content["bullets"], 22, color, bullets=True)
    available_width = 11.5 * 72 - 18
    required_height = sum(
        line_count(text, available_width, 22, font_path) * 22 * 1.15 + 14
        for text in content["bullets"]
    )
    if required_height > body.height.pt:
        raise ValueError(f"{module}, slide {index}: body text exceeds its measured bounds")
    support_shapes = []
    if content["support"]:
        body.height = Pt(required_height + 5)
        support_shapes = add_support(slide, content["support"], body.top + body.height + Pt(8), font_path)
    section = {0: "INTRODUCTION", 99: "CONCLUSION"}.get(module, f"MODULE {module:02d}")
    set_text(header, [f"ACTIONS ADVANCED  |  {section}"], 11, color)
    header.height = Inches(0.24)
    header.name = "Module label"
    for placeholder_index, text in (
        (3, "Copyright \u00a9 2025 Xebia. All rights reserved"),
        (12, f"{index} / {total}"),
    ):
        original = next(
            ph for ph in layout.placeholders
            if ph.placeholder_format.idx == placeholder_index
        )
        slide.shapes.clone_placeholder(original)
        shape = slide.placeholders[placeholder_index]
        copy_geometry(shape, original)
        shape.top = Inches(7.03)
        shape.height = Inches(0.24)
        set_text(shape, [text], 11, color)
    # Keep the semantic reading order focused on the teaching content.
    tree = slide.shapes._spTree
    for shape in reversed([title, body, *support_shapes, header]):
        tree.remove(shape._element)
        tree.insert(2, shape._element)
    slide.notes_slide.notes_text_frame.text = content["notes"]
    return {"layout": layout_name, "title_lines": title_lines, "body_height_points": round(required_height, 2), "support": content["support"]["kind"] if content["support"] else None}


def verify_deck(path, source, template):
    prs = Presentation(str(path))
    expected = read_slides(source)
    if len(prs.slides) != len(expected):
        raise ValueError(f"{path.name}: slide count mismatch")
    if prs.slide_width != template.slide_width or prs.slide_height != template.slide_height:
        raise ValueError(f"{path.name}: template dimensions changed")
    if len(prs.slide_masters) != len(template.slide_masters):
        raise ValueError(f"{path.name}: template master count changed")
    for actual, original in zip(prs.slide_masters, template.slide_masters):
        if actual._element.xml != original._element.xml:
            raise ValueError(f"{path.name}: template master changed")
    if len(prs.slide_layouts) != len(template.slide_layouts):
        raise ValueError(f"{path.name}: template layout count changed")
    for actual, original in zip(prs.slide_layouts, template.slide_layouts):
        if actual._element.xml != original._element.xml:
            raise ValueError(f"{path.name}: template layout changed: {original.name}")
    for index, (slide, item) in enumerate(zip(prs.slides, expected), 1):
        layout_title = next(
            ph for ph in slide.slide_layout.placeholders
            if ph.placeholder_format.type == PP_PLACEHOLDER.TITLE
        )
        if slide.shapes.title.left != layout_title.left or slide.shapes.title.top != layout_title.top:
            raise ValueError(f"{path.name}, slide {index}: title lost its template margin")
        if " ".join(slide.shapes.title.text.split()) != item["title"]:
            raise ValueError(f"{path.name}, slide {index}: title mismatch")
        if [p.text for p in slide.placeholders[110].text_frame.paragraphs] != item["bullets"]:
            raise ValueError(f"{path.name}, slide {index}: bullet mismatch")
        if slide.notes_slide.notes_text_frame.text != item["notes"]:
            raise ValueError(f"{path.name}, slide {index}: notes mismatch")
        if item["support"]:
            support = item["support"]
            actual_caption = next(shape.text for shape in slide.shapes if shape.name == "Example caption")
            if actual_caption != support["caption"]:
                raise ValueError(f"{path.name}, slide {index}: example caption mismatch")
            if support["kind"] == "table":
                table = next(shape.table for shape in slide.shapes if shape.has_table)
                if [[" ".join(cell.text.split()) for cell in row.cells] for row in table.rows] != support["value"]:
                    raise ValueError(f"{path.name}, slide {index}: example table mismatch")
            elif support["kind"] == "qr":
                for i, line in enumerate(support["value"].splitlines()):
                    for part, text in zip(("heading", "instruction"), line.split(" | ", 1)):
                        actual = next(shape.text for shape in slide.shapes if shape.name == f"QR {part} {i}")
                        if actual != text:
                            raise ValueError(f"{path.name}, slide {index}: QR placeholder text mismatch")
                    next(shape for shape in slide.shapes if shape.name == f"QR placeholder {i}")
            elif support["kind"] == "gates":
                for i, line in enumerate(support["value"].splitlines()):
                    for part, text in zip(("heading", "detail"), line.split(" | ", 1)):
                        actual = next(shape.text for shape in slide.shapes if shape.name == f"Gate {part} {i}")
                        if " ".join(actual.split()) != text:
                            raise ValueError(f"{path.name}, slide {index}: gate text mismatch")
            elif support["kind"] == "scatter":
                for i, line in enumerate(support["value"].splitlines()[:6], 1):
                    heading, detail = line.split(" | ", 1)
                    actual_heading = next(shape.text for shape in slide.shapes if shape.name == f"Scatter job heading {i}")
                    actual_detail = next(shape.text for shape in slide.shapes if shape.name == f"Scatter job detail {i}")
                    if " ".join(actual_heading.split()) != heading or " ".join(actual_detail.split()) != detail:
                        raise ValueError(f"{path.name}, slide {index}: scatter job text mismatch")
                for i, line in enumerate(support["value"].splitlines()[6:], 1):
                    heading, detail = line.split(" | ", 1)
                    actual_heading = next(shape.text for shape in slide.shapes if shape.name == f"Scatter gather heading {i}")
                    actual_detail = next(shape.text for shape in slide.shapes if shape.name == f"Scatter gather detail {i}")
                    if " ".join(actual_heading.split()) != heading or " ".join(actual_detail.split()) != detail:
                        raise ValueError(f"{path.name}, slide {index}: scatter gather text mismatch")
            elif support["kind"] != "flow":
                code = next(shape.text for shape in slide.shapes if shape.name == "Example code")
                if code != support["value"]:
                    raise ValueError(f"{path.name}, slide {index}: example code mismatch")
            else:
                for i, line in enumerate(support["value"].splitlines()):
                    for part, text in zip(("heading", "detail"), line.split(" | ", 1)):
                        actual = next(shape.text for shape in slide.shapes if shape.name == f"Flow {part} {i}")
                        if " ".join(actual.split()) != text:
                            raise ValueError(f"{path.name}, slide {index}: flow text mismatch")
        for shape in slide.shapes:
            if shape.left < 0 or shape.top < 0 or shape.left + shape.width > prs.slide_width or shape.top + shape.height > prs.slide_height:
                raise ValueError(f"{path.name}, slide {index}: off-slide shape {shape.name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--font", type=Path, default=Path(r"C:\Windows\Fonts\arial.ttf"))
    parser.add_argument("--bold-font", type=Path, default=Path(r"C:\Windows\Fonts\arialbd.ttf"))
    parser.add_argument("--output", type=Path, default=ROOT / "slides" / "powerpoint")
    args = parser.parse_args()
    for font_path in (args.font, args.bold_font):
        if not font_path.is_file():
            raise FileNotFoundError(f"Arial font required for text-fit checks: {font_path}")
    template = Presentation(str(args.template))
    names = {layout.name for layout in template.slide_layouts}
    for name in ("Title Content/White", "Title Content/Dark"):
        if name not in names:
            raise ValueError(f"Supplied template lacks inspected layout: {name}")
    args.output.mkdir(parents=True, exist_ok=True)
    report = {
        "template": args.template.name,
        "template_sha256": digest(args.template),
        "masters": len(template.slide_masters),
        "layouts": len(template.slide_layouts),
        "decks": [],
    }
    for source in sorted((ROOT / "slides").glob("[0-9][0-9]-*.md")):
        items = read_slides(source)
        prs = Presentation(str(args.template))
        remove_sample_slides(prs)
        prs.core_properties.title = items[0]["title"]
        prs.core_properties.subject = "Actions Advanced: Faster Feedback, Trusted Delivery"
        prs.core_properties.author = "Xebia"
        prs.core_properties.keywords = "GitHub Actions, instructor-led training"
        prs.core_properties.comments = "Generated from the matching Markdown source. Do not edit the deck independently."
        module = int(source.name[:2])
        measurements = [
            add_slide(prs, item, module, index, len(items), args.font, args.bold_font)
            for index, item in enumerate(items, 1)
        ]
        output = args.output / f"{source.stem}.pptx"
        prs.save(str(output))
        verify_deck(output, source, template)
        report["decks"].append({
            "file": output.name,
            "sha256": digest(output),
            "source": source.relative_to(ROOT).as_posix(),
            "source_sha256": digest(source),
            "slide_count": len(items),
            "notes_count": len(items),
            "slides": measurements,
        })
        print(f"{output.name}: {len(items)} slides; matching titles, bullets and notes; template layouts preserved")
    (args.output / "manifest.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
