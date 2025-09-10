import re

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_title(markdown):
    for line in markdown.splitlines():
        if not line.startswith("# "):
            pass
        else:
            stripped_Title = line.replace("# ", "", 1).strip()
            return stripped_Title
    raise Exception("invalid markdown syntax")