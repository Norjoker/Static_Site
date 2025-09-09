from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if (node.text == "") or (node.text.count(delimiter) % 2 != 0):
            raise Exception("invalid markdown syntax")
        elif node.text_type != TextType.TEXT or (node.text.count(delimiter) == 0):
            new_list.append(node)
        else:
            split_list = node.text.split(delimiter)
            for i in range(len(split_list)):
                if i%2 != 0:
                    new_list.append(TextNode(split_list[i] , text_type))
                else:
                    new_list.append(TextNode(split_list[i] , TextType.TEXT))
            
    return new_list