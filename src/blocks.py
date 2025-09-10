from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from splitnodes import text_to_textnodes
from extract_markdown import *
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code text"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    blocks_list = []
    for block in markdown.split("\n\n"):
        if block.strip():
            blocks_list.append(block.strip())
            
    return blocks_list

def block_to_block_type(markdown_block):
    markdown_lines = markdown_block.splitlines()
    if markdown_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif markdown_block.startswith("```") and markdown_block.endswith("```"):
        return BlockType.CODE
    all_quote = True
    all_unordered = True
    all_ordered = True
    i = 1
    for line in markdown_lines:
        all_quote &= line.startswith(">")
        all_unordered &= line.startswith("- ")
        all_ordered &= line.startswith(f"{i}. ")
        i += 1
    if all_quote:
        return BlockType.QUOTE
    if all_unordered:
        return BlockType.UNORDERED_LIST
    if all_ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    # ---- Helper Functions-----------------------------------------------------------
    def get_html_tag(type):
        match type:
            case BlockType.PARAGRAPH:
               tag = "p"
            case BlockType.HEADING:
               tag = "h1"
            case BlockType.CODE:
               tag = "code"
            case BlockType.UNORDERED_LIST:
               tag = "ul" 
            case BlockType.ORDERED_LIST:
               tag = "ol" 
            case BlockType.QUOTE:
               tag = "blockquote"
        return tag

    def format_list(list_text):
        lines = list_text.splitlines()
        html = ""
        i = 1
        for line in lines:
            if line.startswith("- "):
                line = line.replace("- ", "<li>")
                html += line + "</li>"
            else:
                line = line.replace(f"{i}. ", "<li>")
                html += line + "</li>"
                i += 1
        return html

    def text_to_children(text):
        text_nodes = text_to_textnodes(text)
        nodes = []
        for node in text_nodes:
            nodes.append(text_node_to_html_node(node))
        return nodes
     # ---- Main Function------------------------------------------------------------   

    children = []
    for block in markdown_to_blocks(markdown):
        type = block_to_block_type(block)
        tag = get_html_tag(type)
        if tag == "h1":
            c = block.count("#")
            htag = f"h{c}"
            text = block.replace("\n", " ")
            text = text.strip("# ")
            text = text.strip("#")
            html_node = ParentNode(htag, text_to_children(text), None)
        elif tag == "code":
            html_node = ParentNode("pre",[text_node_to_html_node(TextNode(block.strip("`"),TextType.CODE))])        
        elif tag == "ol" or tag == "ul":
            html_node = ParentNode(tag, text_to_children(format_list(block)), None)
        else:
            if tag == "blockquote":
                block = block.replace("> ", "")
                block = block.replace(">", "")
            text = block.replace("\n", " ")
            html_node = ParentNode(tag, text_to_children(text), None)
        children.append(html_node)
    
    parent_node = ParentNode("div", children)
    return parent_node