import tempfile
import unittest
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches

from build_slides import add_support, read_slides


class SupportingMaterialTests(unittest.TestCase):
    def parse(self, material):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "slides.md"
            path.write_text(
                "# Title\n- Takeaway\n\n## Example\n"
                + material
                + "\n\n<!-- notes: Keep these notes exactly. -->",
                encoding="utf-8",
            )
            return read_slides(path)[0]

    def test_code_indentation_and_notes_are_preserved(self):
        code = "steps:\n  - run: npm test"
        slide = self.parse(f"```yaml\n{code}\n```")
        self.assertEqual(slide["support"]["value"], code)
        self.assertEqual(slide["notes"], "Keep these notes exactly.")
        self.assertEqual(slide["bullets"], ["Takeaway"])

    def test_table_removes_separator_and_display_markup(self):
        slide = self.parse("| Input | Result |\n| --- | --- |\n| `unknown` | Block |")
        self.assertEqual(slide["support"]["value"], [["Input", "Result"], ["unknown", "Block"]])

    def test_inconsistent_table_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "inconsistent table"):
            self.parse("| Input | Result |\n| --- | --- |\n| missing |")

    def test_unsupported_fence_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unsupported supporting material"):
            self.parse("```unknown\npayload\n```")

    def test_flow_creates_editable_cards(self):
        slide = self.parse("```flow\nBuild | Produce reviewed bytes.\nVerify | Check the digest.\n```")
        prs = Presentation()
        page = prs.slides.add_slide(prs.slide_layouts[6])
        add_support(page, slide["support"], Inches(2), Path(r"C:\Windows\Fonts\arial.ttf"))
        texts = [shape.text for shape in page.shapes if shape.has_text_frame]
        self.assertIn("Build", texts)
        self.assertIn("Check the digest.", texts)

    def test_oversized_code_is_rejected(self):
        slide = self.parse("```text\n" + "W" * 200 + "\n```")
        prs = Presentation()
        page = prs.slides.add_slide(prs.slide_layouts[6])
        with self.assertRaisesRegex(ValueError, "too wide"):
            add_support(page, slide["support"], Inches(2), Path(r"C:\Windows\Fonts\arial.ttf"))

    def test_qr_slots_are_editable_explicit_placeholders(self):
        slide = self.parse("```qr\nFeedback | Insert the class link.\nCompletion | Insert the module link.\n```")
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        page = prs.slides.add_slide(prs.slide_layouts[6])
        add_support(page, slide["support"], Inches(2), Path(r"C:\Windows\Fonts\arial.ttf"))
        texts = [shape.text for shape in page.shapes if shape.has_text_frame]
        self.assertEqual(texts.count("ADD QR\nHERE"), 2)
        self.assertIn("Insert the class link.", texts)
        self.assertIn("Insert the module link.", texts)
        self.assertFalse(any(shape.shape_type == 13 for shape in page.shapes))

    def test_qr_slots_reject_invalid_card_count_or_format(self):
        for value in ("No separator", "A | One\nB | Two\nC | Three"):
            slide = self.parse(f"```qr\n{value}\n```")
            prs = Presentation()
            page = prs.slides.add_slide(prs.slide_layouts[6])
            with self.assertRaisesRegex(ValueError, "QR placeholders require"):
                add_support(page, slide["support"], Inches(2), Path(r"C:\Windows\Fonts\arial.ttf"))

    def test_opening_and_closing_decks_cover_delivery_needs(self):
        root = Path(__file__).resolve().parents[1] / "slides"
        opening = read_slides(root / "00-introduction.md")
        closing = read_slides(root / "99-conclusion.md")
        self.assertEqual(len(opening), 4)
        self.assertEqual(len(closing), 6)
        self.assertIn("Meet your trainer", [item["title"] for item in opening])
        self.assertIn("Our agenda", [item["title"] for item in opening])
        self.assertTrue(any("cleanup" in item["notes"] for item in closing))
        qr_slides = [item for item in closing if item["support"] and item["support"]["kind"] == "qr"]
        self.assertEqual(len(qr_slides), 2)
        self.assertIn("MTM", qr_slides[0]["support"]["value"])
        self.assertIn("Microsoft Learn", qr_slides[1]["title"])

    def test_background_constructs_have_visible_yaml_examples(self):
        source = Path(__file__).resolve().parents[1] / "slides" / "02-execution.md"
        slides = read_slides(source)
        examples = {
            "wait: finish a named step before continuing": "- wait: build",
            "wait-all: finish every active background step": "- wait-all:",
            "cancel: stop a background process by its ID": "- cancel: heartbeat",
        }
        for title, construct in examples.items():
            with self.subTest(title=title):
                slide = next(item for item in slides if item["title"] == title)
                self.assertEqual(slide["support"]["kind"], "yaml")
                code = slide["support"]["value"]
                self.assertIn("background: true", code)
                self.assertIn(construct, code)
                self.assertNotIn("if:", code)
                self.assertIn("Timing", slide["notes"])


if __name__ == "__main__":
    unittest.main()
