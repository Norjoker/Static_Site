import unittest

from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter


class TestSplitNode(unittest.TestCase):
    def test_normal(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        print(new_nodes)
        '''self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        )'''