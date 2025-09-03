from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.extend(node)
        if delimiter not in node.text:
            raise Exception("invalid markdown syntax")
        delimiter_indices = [i for i, x in enumerate(node.text) if x == delimiter]
        new_nodes = []
        for i in range(len(delimiter_indices)):
            if i == 0:
                new_nodes.append(TextNode(node.text[:delimiter_indices[i]],TextType.TEXT))
            elif i % 2 == 0:
                new_nodes.append(TextNode(node.text[delimiter_indices[i-1] + 1:delimiter_indices[i]],TextType.TEXT))
            else:
                new_nodes.append(TextNode(node.text[delimiter_indices[i-1] + 1:delimiter_indices[i]],text_type))
        new_nodes.append(TextNode(node.text[delimiter_indices[-1]:],TextType.TEXT))
        
    new_list.append(new_nodes)
    return new_list