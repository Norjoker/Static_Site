import unittest
from blocks import *


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_paragraph_returns_single_block(self):
        md = "Just a single paragraph with **bold** and _italic_."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single paragraph with **bold** and _italic_."])

    def test_heading_paragraph_list_three_blocks(self):
        md = "# Heading\n\nThis is a para.\nStill same para line.\n\n- a\n- b"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a para.\nStill same para line.",
                "- a\n- b",
            ],
        )

    def test_multiple_blank_lines_are_collapsed(self):
        md = "First paragraph\n\n\n\nSecond paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph", "Second paragraph"])

    def test_trailing_and_leading_whitespace_is_stripped_per_block(self):
        md = "   Leading spaces in this block   \n\n\tSecond block with tab prefix\t"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Leading spaces in this block", "Second block with tab prefix"],
        )

    def test_preserves_single_newlines_within_a_block(self):
        md = "Line one of the paragraph\nLine two of the same paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Line one of the paragraph\nLine two of the same paragraph"],
        )

    def test_trailing_double_newline_does_not_create_empty_block(self):
        md = "Block A\n\nBlock B\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block A", "Block B"])

    def test_leading_double_newline_does_not_create_empty_block(self):
        md = "\n\nBlock only"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block only"])

    def test_excessive_newlines_yield_no_empty_blocks(self):
        md = "\n\n\n\n"  # document that is only blank lines
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_whitespace_only_document_returns_empty_list(self):
        md = "   \n\t\n  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])


class TestBlockToBlockType(unittest.TestCase):
    # --- Headings ------------------------------------------------------------

    def test_heading_levels_1_through_6(self):
        for level in range(1, 7):
            hashes = "#" * level
            self.assertEqual(
                block_to_block_type(f"{hashes} Heading"),
                BlockType.HEADING,
                msg=f"Failed for level {level}",
            )

    def test_heading_requires_space_after_hashes(self):
        # No space after hashes → not a heading per spec
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)

    def test_seven_hashes_is_not_a_valid_heading(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    # --- Code blocks ---------------------------------------------------------

    def test_code_block_multiline_fenced(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_same_line_fences(self):
        block = "```print('inline')```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_unclosed_code_block_is_paragraph(self):
        block = "```\nprint('missing fence')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Quote blocks --------------------------------------------------------

    def test_quote_block_every_line_prefixed_with_gt(self):
        block = "> quote line one\n> quote line two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_mixed_prefix_is_paragraph(self):
        block = "> good line\nnot quoted"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Unordered lists -----------------------------------------------------

    def test_unordered_list_all_lines_dash_space(self):
        block = "- item one\n- item two\n- item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space_after_dash_is_paragraph(self):
        block = "-item one\n- item two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Ordered lists -------------------------------------------------------

    def test_ordered_list_proper_sequence(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start_number_is_paragraph(self):
        block = "0. nope\n1. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_increment_is_paragraph(self):
        block = "1. first\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_missing_space_after_dot_is_paragraph(self):
        block = "1.first\n2. second"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # --- Fallback ------------------------------------------------------------

    def test_fallback_is_paragraph(self):
        block = "Just a normal paragraph with **inline** markup."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraphs(self):
        md = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        #print(repr(html))
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """```This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()