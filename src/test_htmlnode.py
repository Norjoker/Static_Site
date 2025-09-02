import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_prop(self):
        propsdict = {
                    "href": "https://www.google.com",
                    "target": "_blank",
                }
        node = HTMLNode(None, None, None, propsdict)
        node = node.props_to_html()
        node2 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node, node2)

    def test_prop(self):
        propsdict = {
                    "href": "https:\n//www.google.com",
                    "something": "_something",
                }
        node = HTMLNode(None, None, None, propsdict)
        node = node.props_to_html()
        node2 = ' href="https:\n//www.google.com" something="_something"'
        self.assertEqual(node, node2)

    def test_prop(self):
        propsdict = {
                    "image": "'Insert URL Here'",
                    "target": "_blank",
                }
        node = HTMLNode(None, None, None, propsdict)
        node = node.props_to_html()
        node2 = ' image="\'Insert URL Here\'" target="_blank"'
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()