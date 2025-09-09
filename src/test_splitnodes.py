import unittest

from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter


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