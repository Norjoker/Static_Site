import re

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((https:\/\/.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((https:\/\/.*?)\)", text)

def extract_title(markdown):
    if not markdown.startswith("# "):
        raise Exception("invalid markdown syntax")
    else:
        stripped_markdown = markdown.replace("# ", "", 1).strip()
        return stripped_markdown