import unittest

from extract_markdown import *

class TestSplitNode(unittest.TestCase):
    # --- Images ---
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_markdown_images_multiple(self):
        md = (
            "![first](https://example.com/1.png) and more text "
            "then ![second image](https://example.com/path/2.jpg)"
        )
        matches = extract_markdown_images(md)
        self.assertListEqual(
            [
                ("first", "https://example.com/1.png"),
                ("second image", "https://example.com/path/2.jpg"),
            ],
            matches
        )

    def test_extract_markdown_images_query_and_fragment(self):
        md = "![chart](https://example.com/c.png?ver=2#section)"
        matches = extract_markdown_images(md)
        self.assertListEqual(
            [("chart", "https://example.com/c.png?ver=2#section")],
            matches
        )

    def test_extract_markdown_images_mixed_with_links(self):
        md = (
            "See ![icon](https://ex.com/i.png) and also "
            "[our site](https://ex.com) for details."
        )
        matches = extract_markdown_images(md)
        self.assertListEqual(
            [("icon", "https://ex.com/i.png")],
            matches
        )

    def test_extract_markdown_images_newlines_and_spacing(self):
        md = (
            "Intro text\n\n"
            "![alt text](https://assets.example.org/img.png)\n"
            "More text\n"
        )
        matches = extract_markdown_images(md)
        self.assertListEqual(
            [("alt text", "https://assets.example.org/img.png")],
            matches
        )

    def test_extract_markdown_images_no_matches(self):
        md = "This has no images, only text and a [link](https://example.com)."
        matches = extract_markdown_images(md)
        self.assertListEqual([], matches)

    # --- Links ---

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev")],
            matches
        )

    def test_extract_markdown_links_multiple(self):
        md = (
            "Links: [Docs](https://docs.example.com) and "
            "[YouTube](https://www.youtube.com/@bootdotdev)"
        )
        matches = extract_markdown_links(md)
        self.assertListEqual(
            [
                ("Docs", "https://docs.example.com"),
                ("YouTube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches
        )

    def test_extract_markdown_links_query_and_fragment(self):
        md = "[search](https://example.com?q=markdown+link#results)"
        matches = extract_markdown_links(md)
        self.assertListEqual(
            [("search", "https://example.com?q=markdown+link#results")],
            matches
        )

    def test_extract_markdown_links_mixed_with_images(self):
        md = (
            "![thumb](https://cdn.ex/t.png) "
            "and a link [read more](https://ex.com/articles/1)"
        )
        matches = extract_markdown_links(md)
        self.assertListEqual(
            [("read more", "https://ex.com/articles/1")],
            matches
        )

    def test_extract_markdown_links_newlines_and_spacing(self):
        md = "Intro\n\n[About us](https://example.org/about)\nEnd."
        matches = extract_markdown_links(md)
        self.assertListEqual(
            [("About us", "https://example.org/about")],
            matches
        )

    def test_extract_markdown_links_no_matches(self):
        md = "No links here, only an image ![pic](https://ex.com/p.png)."
        matches = extract_markdown_links(md)
        self.assertListEqual([], matches)

    # --- Combined / ordering / punctuation ---

    def test_order_is_preserved(self):
        md = (
            "Start [one](https://a.example) text "
            "![img](https://i.example/x.png) more "
            "[two](https://b.example)"
        )
        # Ensure each extractor only pulls its type, and the relative order
        self.assertListEqual(
            [("one", "https://a.example"), ("two", "https://b.example")],
            extract_markdown_links(md)
        )
        self.assertListEqual(
            [("img", "https://i.example/x.png")],
            extract_markdown_images(md)
        )

    def test_trailing_punctuation_after_link_or_image(self):
        md = (
            "Check [this](https://ex.com), and this image "
            "![that](https://ex.com/that.png). Wow!"
        )
        self.assertListEqual(
            [("this", "https://ex.com")],
            extract_markdown_links(md)
        )
        self.assertListEqual(
            [("that", "https://ex.com/that.png")],
            extract_markdown_images(md)
        )


if __name__ == "__main__":
    unittest.main()