import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click me", props={"href": "https://example.com", "target": "_blank"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://example.com" target="_blank">Click me</a>')  
        
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_value_none_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_leaf_to_html_not_equal_wrong_props(self):
        node = LeafNode("a", "Click me", props={"href": "https://example.com"})
        # The output should NOT match if the href is wrong
        self.assertNotEqual(
            node.to_html(),
            '<a href="https://wrong.com">Click me</a>')

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>")


if __name__ == "__main__":
    unittest.main()