import unittest

from textnode import TextNode, TextType
from splitnodes import *


class TestSplitNode(unittest.TestCase):
    def test_normal(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_multiple_delimiters(self):
        node = TextNode("Here is `one` and `two` codes", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("Here is ", TextType.TEXT),
            TextNode("one", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.CODE),
            TextNode(" codes", TextType.TEXT),
        ])

    def test_no_delimiters(self):
        node = TextNode("No special formatting here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("No special formatting here", TextType.TEXT),
        ])

    def test_unmatched_delimiter(self):
        node = TextNode("This has an `unmatched delimiter", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "invalid markdown syntax")

    def test_multiple_nodes(self):
        nodes = [
            TextNode("First `code` part", TextType.TEXT),
            TextNode("Second `more code` here", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" part", TextType.TEXT),
            TextNode("Second ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ])

    def test_empty_string_node(self):
        node = TextNode("", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "invalid markdown syntax")

    def test_non_text_type_node(self):
        node = TextNode("This is `already code` text", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        # Since it's not TextType.TEXT, it should not be split
        self.assertEqual(new_nodes, [
            TextNode("This is `already code` text", TextType.CODE),
        ])

    def test_multi_node_multi_delimiters(self):
    # Multiple nodes, mix of single- and multi-character delimiters
        nodes = [
            TextNode("Start **bold** and `code`.", TextType.TEXT),
            TextNode("Then _italics_ and **second bold**.", TextType.TEXT),
        ]

        # Apply splitting in stages per delimiter
        nodes_after_code = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes_after_bold = split_nodes_delimiter(nodes_after_code, "**", TextType.BOLD)
        final_nodes = split_nodes_delimiter(nodes_after_bold, "_", TextType.ITALIC)

        self.assertEqual(final_nodes, [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
            TextNode("Then ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("second bold", TextType.BOLD),
            TextNode(".", TextType.TEXT),
        ])

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and another ", TextType.TEXT),
                    TextNode(
                        "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                    ),
                ],
                new_nodes,
            )

    def test_image_single_middle(self):
        node = TextNode(
            "A pic: ![alt text](https://example.com/x.png) cool!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("A pic: ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://example.com/x.png"),
                TextNode(" cool!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode(
            "![logo](https://cdn.example.org/logo.svg) is our mark",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("logo", TextType.IMAGE, "https://cdn.example.org/logo.svg"),
                TextNode(" is our mark", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode(
            "end with pic ![cap](https://img.example.com/last.jpg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("end with pic ", TextType.TEXT),
                TextNode("cap", TextType.IMAGE, "https://img.example.com/last.jpg"),
            ],
            new_nodes,
        )

    def test_two_images_back_to_back(self):
        node = TextNode(
            "imgs: ![one](https://ex.com/1.png)![two](https://ex.com/2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("imgs: ", TextType.TEXT),
                TextNode("one", TextType.IMAGE, "https://ex.com/1.png"),
                TextNode("two", TextType.IMAGE, "https://ex.com/2.png"),
            ],
            new_nodes,
        )

    def test_preserves_non_text_nodes(self):
        # Pre-existing IMAGE node should remain unchanged; only TEXT is split
        existing_image = TextNode("already", TextType.IMAGE, "https://a.b/already.png")
        text_node = TextNode(
            "and new ![fresh](https://a.b/fresh.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([existing_image, text_node])
        self.assertListEqual(
            [
                TextNode("already", TextType.IMAGE, "https://a.b/already.png"),
                TextNode("and new ", TextType.TEXT),
                TextNode("fresh", TextType.IMAGE, "https://a.b/fresh.png"),
            ],
            new_nodes,
        )

    def test_text_with_no_images_is_unchanged(self):
        node = TextNode("just plain text here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("just plain text here", TextType.TEXT)], new_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_multiple_links_in_text(self):
        node = TextNode(
            "see [site](https://ex.com) and also [docs](https://ex.com/docs)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("see ", TextType.TEXT),
                TextNode("site", TextType.LINK, "https://ex.com"),
                TextNode(" and also ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "https://ex.com/docs"),
            ],
            new_nodes,
        )

    def test_link_at_start(self):
        node = TextNode(
            "[home](https://ex.org) is the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("home", TextType.LINK, "https://ex.org"),
                TextNode(" is the start", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode(
            "go to the [end](https://end.example)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("go to the ", TextType.TEXT),
                TextNode("end", TextType.LINK, "https://end.example"),
            ],
            new_nodes,
        )

    def test_two_links_back_to_back(self):
        node = TextNode(
            "pair: [one](https://1.test)[two](https://2.test)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("pair: ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://1.test"),
                TextNode("two", TextType.LINK, "https://2.test"),
            ],
            new_nodes,
        )

    def test_preserves_non_text_nodes(self):
        existing_link = TextNode("existing", TextType.LINK, "https://keep.me")
        text_node = TextNode(
            " and new [fresh](https://fresh.me)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([existing_link, text_node])
        self.assertListEqual(
            [
                TextNode("existing", TextType.LINK, "https://keep.me"),
                TextNode(" and new ", TextType.TEXT),
                TextNode("fresh", TextType.LINK, "https://fresh.me"),
            ],
            new_nodes,
        )

    def test_text_with_no_links_is_unchanged(self):
        node = TextNode("no links here!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("no links here!", TextType.TEXT)], new_nodes)


class TestTextToTextNodes(unittest.TestCase):
    # --- Helpers -------------------------------------------------------------
    def as_tuples(self, nodes):
        """Convert a list of TextNode objects into (text, type, url) tuples."""
        out = []
        for n in nodes:
            url = getattr(n, "url", None)
            out.append((n.text, n.text_type, url))
        return out

    def T(self, text, ttype, url=None):
        return (text, ttype, url)

    # --- Tests ---------------------------------------------------------------

    def test_plain_text_returns_single_text_node(self):
        s = "Just plain text."
        result = text_to_textnodes(s)
        self.assertEqual(self.as_tuples(result), [self.T("Just plain text.", TextType.TEXT, None)])

    def test_example_from_prompt(self):
        s = (
            "This is **text** with an _italic_ word and a `code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a "
            "[link](https://boot.dev)"
        )
        result = text_to_textnodes(s)
        expected = [
            self.T("This is ", TextType.TEXT, None),
            self.T("text", TextType.BOLD, None),
            self.T(" with an ", TextType.TEXT, None),
            self.T("italic", TextType.ITALIC, None),
            self.T(" word and a ", TextType.TEXT, None),
            self.T("code block", TextType.CODE, None),
            self.T(" and an ", TextType.TEXT, None),
            self.T("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            self.T(" and a ", TextType.TEXT, None),
            self.T("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(self.as_tuples(result), expected)

    def test_adjacent_formatting_segments(self):
        s = "**bold**_italic_`code`"
        result = text_to_textnodes(s)
        self.assertEqual(
            self.as_tuples(result),
            [
                self.T("bold", TextType.BOLD, None),
                self.T("italic", TextType.ITALIC, None),
                self.T("code", TextType.CODE, None),
            ],
        )

    def test_multiple_links_same_url_and_trailing_text(self):
        s = "A [x](https://u) B [y](https://u) C"
        result = text_to_textnodes(s)
        self.assertEqual(
            self.as_tuples(result),
            [
                self.T("A ", TextType.TEXT, None),
                self.T("x", TextType.LINK, "https://u"),
                self.T(" B ", TextType.TEXT, None),
                self.T("y", TextType.LINK, "https://u"),
                self.T(" C", TextType.TEXT, None),
            ],
        )

    def test_image_and_link_back_to_back(self):
        s = "![alt](https://img) [name](https://site)"
        result = text_to_textnodes(s)
        self.assertEqual(
            self.as_tuples(result),
            [
                self.T("alt", TextType.IMAGE, "https://img"),
                self.T(" ", TextType.TEXT, None),
                self.T("name", TextType.LINK, "https://site"),
            ],
        )

    def test_unclosed_markup_is_text(self):
        s = "This is **not closed and _also not_ closed"
        with self.assertRaises(Exception) as context:
            text_to_textnodes(s)
        self.assertEqual(str(context.exception), "invalid markdown syntax")

    def test_empty_alt_image(self):
        s = "![](https://img.png)"
        result = text_to_textnodes(s)
        self.assertEqual(self.as_tuples(result), [self.T("", TextType.IMAGE, "https://img.png")])

    def test_no_links_or_images_or_markup(self):
        s = "No markdown here"
        result = text_to_textnodes(s)
        self.assertEqual(self.as_tuples(result), [self.T("No markdown here", TextType.TEXT, None)])

    def test_empty_string_returns_exception(self):
        s = ""
        with self.assertRaises(Exception) as context:
            text_to_textnodes(s)
        self.assertEqual(str(context.exception), "invalid markdown syntax")

if __name__ == "__main__":
    unittest.main()