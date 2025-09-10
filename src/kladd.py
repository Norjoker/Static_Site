
import re
from textnode import TextNode, TextType
from extract_markdown import *
from splitnodes import *
import os
from blocks import BlockType

#text = "This is **text** with an _italic_ word and a `code block` and an ![](https://i.imgur.com/fJRm4Vk.jpeg) and a [](https://boot.dev)"
def get_props(text):
        image_tuples = extract_markdown_images(text)
        link_tuples = extract_markdown_links(text)
        return link_tuples

source = os.getcwd() + "/static/"
target = os.getcwd() + "/public/"

md ="""```
This is text that _should_ remain
the **same** even with inline stuff
```"""

directory_content = os.listdir(source)
for content in directory_content:
        full_path = os.path.join(source, content)
        print(full_path)
        print(os.path.exists(full_path))
        if os.path.isfile(full_path):
                print(f"{content} is a file")
        else:
                print(f"{content} is a directory")

#print(os.listdir(source))
        
