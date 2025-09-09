from textnode import TextType, TextNode
from extract_markdown import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if (node.text == "") or (node.text.count(delimiter) % 2 != 0):
            #print(f"Node Text: {node.text}")
            raise Exception("invalid markdown syntax")
        elif node.text_type != TextType.TEXT or (node.text.count(delimiter) == 0):
            new_list.append(node)
        else:
            split_list = node.text.split(delimiter)
            for i in range(len(split_list)):
                if i%2 != 0:
                    new_list.append(TextNode(split_list[i] , text_type))
                elif split_list[i]:
                    new_list.append(TextNode(split_list[i] , TextType.TEXT))
            
    return new_list


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        tuples_images = extract_markdown_images(node.text)
        if not tuples_images:
            new_nodes.append(node)
        else:
            node_text = node.text
            i = 1
            for image_alt, image_url in tuples_images:
                split = node_text.split(f"![{image_alt}]({image_url})", 1)
                if split[0] != "":
                    new_nodes.append(TextNode(split[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
                if i == len(tuples_images) and split[1] != "":
                    new_nodes.append(TextNode(split[1], TextType.TEXT))
                node_text = split[1] if len(split) > 1 else ""
                i += 1

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        tuples_links = extract_markdown_links(node.text)
        if not tuples_links:
            new_nodes.append(node)
        else:
            node_text = node.text
            i = 1
            for link_alt, link_url in tuples_links:
                split = node_text.split(f"[{link_alt}]({link_url})", 1)
                if split[0] != "":
                    new_nodes.append(TextNode(split[0], TextType.TEXT))
                new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
                if i == len(tuples_links) and split[1] != "":
                    new_nodes.append(TextNode(split[1], TextType.TEXT))
                node_text = split[1] if len(split) > 1 else ""
                i += 1

    return new_nodes

def text_to_textnodes(text):
    old_nodes = [TextNode(text, TextType.TEXT,)]
    new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    
    return new_nodes