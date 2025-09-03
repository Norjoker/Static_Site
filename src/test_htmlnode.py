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
    
    def test_to_html_raises_when_tag_none(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_raises_when_children_none(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_empty_children_list(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_nested_parent_multiple_children_order_preserved(self):
        children = [
            LeafNode("span", "first"),
            LeafNode("b", "second"),
            ParentNode("i", [LeafNode(None, "third")]),  # <i>third</i>
        ]
        parent_node = ParentNode("div", children)
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>first</span><b>second</b><i>third</i></div>"
        )

    def test_deep_nesting_three_levels_mixed(self):
        deep = ParentNode("ul", [
            ParentNode("li", [LeafNode(None, "one")]),
            ParentNode("li", [LeafNode("b", "two")]),
            ParentNode("li", [ParentNode("span", [LeafNode(None, "three")])]),
        ])
        wrapper = ParentNode("div", [deep])
        self.assertEqual(
            wrapper.to_html(),
            "<div><ul><li>one</li><li><b>two</b></li><li><span>three</span></li></ul></div>"
        )

    def test_child_error_propagates_from_leaf(self):
        # LeafNode with value=None should raise; ensure ParentNode doesn't swallow it
        bad_child = LeafNode("p", None)
        parent_node = ParentNode("div", [bad_child])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_props_are_ignored_in_output_and_not_equal_with_attrs(self):
        # Current ParentNode.to_html() ignores props when rendering
        parent_node = ParentNode("div", [LeafNode("span", "x")], props={"class": "box"})
        self.assertEqual(parent_node.to_html(), "<div><span>x</span></div>")
        # And ensure it's NOT equal to a string that includes attributes
        self.assertNotEqual(parent_node.to_html(), '<div class="box"><span>x</span></div>')


if __name__ == "__main__":
    unittest.main()