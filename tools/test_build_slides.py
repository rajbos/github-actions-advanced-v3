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


if __name__ == "__main__":
    unittest.main()
