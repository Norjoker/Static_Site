

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag #A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value #A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children #A list of HTMLNode objects representing the children of this node
        self.props = props #A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props = self.props.copy()
        string = ""
        for key in props:
            string += f" {key}="
            string += f'"{props[key]}"'

        return string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return str(self.value)
        if not self.props is None:
            props = self.props.copy()
            string = f"<{self.tag}"
            for key in props:
                string += f" {key}="
                string += f'"{props[key]}"'
            string += f">{self.value}</{self.tag}>"
            return string
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode nees a tag value")
        if self.children is None:
            raise ValueError("ParentNode needs children")
        string = f"<{self.tag}>"
        for child in self.children:
            string += child.to_html()
        string += f"</{self.tag}>"
        return string