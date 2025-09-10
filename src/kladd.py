
import re
from textnode import TextNode, TextType
from extract_markdown import *
from splitnodes import *
import os
from blocks import BlockType

#text = "This is **text** with an _italic_ word and a `code block` and an ![](https://i.imgur.com/fJRm4Vk.jpeg) and a [](https://boot.dev)"


md = """1. first
2. second
3. third
"""
lines = md.splitlines()
html = ""
i = 1
for line in lines:
    line = line.replace(f"{i}. ", "<li>")
    html += line + "</li>"
    i += 1

"""
text = text.strip()
text = text.replace("\n", "")"""

print(html)
        
