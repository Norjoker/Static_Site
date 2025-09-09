
import re
from textnode import TextNode, TextType
from extract_markdown import *
from splitnodes import *
from blocks import BlockType

#text = "This is **text** with an _italic_ word and a `code block` and an ![](https://i.imgur.com/fJRm4Vk.jpeg) and a [](https://boot.dev)"
def get_props(text):
        image_tuples = extract_markdown_images(text)
        link_tuples = extract_markdown_links(text)
        return link_tuples



md ="""```
This is text that _should_ remain
the **same** even with inline stuff
```"""

print(md.strip("`"))
        
