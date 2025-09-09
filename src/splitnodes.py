from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
        elif (node.text == "") or (node.text.count(delimiter) % 2 != 0):
            #print(f"{delimiter} | {node.text} | {node.text.count(delimiter)} | {delimiter not in node.text}")
            raise Exception("invalid markdown syntax")
        else:
            delimiter_indices = [j for j, x in enumerate(node.text) if x == delimiter]
            if delimiter_indices == []:
                new_list.append(node)
            else:
                new_nodes = []
                for i in range(len(delimiter_indices)):
                    if i == 0:
                        new_nodes.append(TextNode(node.text[:delimiter_indices[i]],TextType.TEXT))
                    elif i % 2 == 0:
                        new_nodes.append(TextNode(node.text[delimiter_indices[i-1] + 1:delimiter_indices[i]],TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(node.text[delimiter_indices[i-1] + 1:delimiter_indices[i]],text_type))
                new_nodes.append(TextNode(node.text[delimiter_indices[-1] + 1:],TextType.TEXT))
                new_list.extend(new_nodes)
        
    return new_list