from extract_markdown import extract_title
from blocks import markdown_to_html_node
import os

def generate_page(from_path, template_path, dest_path, basepath = "/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath = "/"):
    directory_content = os.listdir(dir_path_content)
    if not directory_content:
         return False
    for content in directory_content:
        full_content_path = os.path.join(dir_path_content, content)
        if content.endswith(".md"):
            html_content = content.replace(".md",".html")
            full_dest_path = os.path.join(dest_dir_path, html_content)
        else:
            full_dest_path = os.path.join(dest_dir_path, content)
        if os.path.isfile(full_content_path):
                generate_page(full_content_path, template_path, full_dest_path, basepath)
        elif os.path.isdir(full_content_path):
                print(f"{full_content_path} is a directory, inception time!")
                new_target = os.path.join(dest_dir_path, content)
                os.mkdir(new_target)
                generate_pages_recursive(full_content_path, template_path, new_target, basepath)
        else:
             raise Exception("Unsupported filetype detected")