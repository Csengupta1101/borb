import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from borb.pdf.canvas.geometry.rectangle import Rectangle

from borb.pdf.canvas.font.simple_font.font_type_1 import StandardType1Font

from borb.pdf.canvas.color.color import HexColor
from borb.pdf.canvas.layout.layout_element import Alignment
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import (
    FixedColumnWidthTable as Table,
)
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.document import Document
from borb.pdf.page.page import Page, TextAnnotationIconType
from borb.pdf.pdf import PDF
from borb.toolkit.text.regular_expression_text_extraction import (
    RegularExpressionTextExtraction,
)
from tests.test_util import compare_visually_to_ground_truth

unittest.TestLoader.sortTestMethodsUsing = None


class TestAddFreeTextAnnotation(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        # find output dir
        p: Path = Path(__file__).parent
        while "output" not in [x.stem for x in p.iterdir() if x.is_dir()]:
            p = p.parent
        p = p / "output"
        self.output_dir = Path(p, Path(__file__).stem.replace(".py", ""))
        if not self.output_dir.exists():
            self.output_dir.mkdir()

    def test_write_document(self):

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # add test information
        layout = SingleColumnLayout(page)
        layout.add(
            Table(number_of_columns=2, number_of_rows=3)
            .add(Paragraph("Date", font="Helvetica-Bold"))
            .add(Paragraph(datetime.now().strftime("%d/%m/%Y, %H:%M:%S")))
            .add(Paragraph("Test", font="Helvetica-Bold"))
            .add(Paragraph(Path(__file__).stem))
            .add(Paragraph("Description", font="Helvetica-Bold"))
            .add(
                Paragraph(
                    "This test creates a PDF with an empty Page, and a Paragraph of text. A subsequent test will add a free text annotation."
                )
            )
            .set_padding_on_all_cells(Decimal(2), Decimal(2), Decimal(2), Decimal(2))
        )

        layout.add(
            Paragraph(
                """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            """,
                font_size=Decimal(10),
                vertical_alignment=Alignment.TOP,
                horizontal_alignment=Alignment.LEFT,
                padding_top=Decimal(5),
                padding_right=Decimal(5),
                padding_bottom=Decimal(5),
                padding_left=Decimal(5),
            )
        )

        # attempt to store PDF
        with open(self.output_dir / "output_001.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, pdf)

    def test_add_text_annotation(self):

        # attempt to read PDF
        doc = None
        l = RegularExpressionTextExtraction("ad minim veniam")
        with open(self.output_dir / "output_001.pdf", "rb") as in_file_handle:
            doc = PDF.loads(in_file_handle, [l])

        bb = l.get_matches_for_page(0)[0].get_bounding_boxes()[0]
        doc.get_page(0).append_free_text_annotation(
            rectangle=Rectangle(Decimal(59), Decimal(500), Decimal(200), Decimal(100)),
            font=StandardType1Font("Helvetica"),
            font_size=Decimal(12),
            text="""Lorem Ipsum""",
            font_color=HexColor("F1CD2E"),
        )

        # attempt to store PDF
        with open(self.output_dir / "output_002.pdf", "wb") as out_file_handle:
            PDF.dumps(out_file_handle, doc)

        # compare visually
        compare_visually_to_ground_truth(self.output_dir / "output_002.pdf")
