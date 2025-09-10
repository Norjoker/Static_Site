from textnode import TextNode, TextType
import os
import shutil
from page_gen import generate_page

def main():
    source = os.getcwd() + "/static/"
    target = os.getcwd() + "/public/"
    content = os.getcwd() + "/content/"
    source_ind = os.path.join(content, "index.md")
    public_ind = os.path.join(target, "index.css")
    template_path = os.path.join(os.getcwd(), "template.html")
    print(f"From:{source}\nTo:{target}")
    if os.path.exists(source) and os.path.exists(target):
        print("Paths are valid. Proceeding!")
        copy_content(source, target)
    else:
        raise Exception("Invalid source or target path")
    
    generate_page(source_ind, template_path, public_ind)

def copy_content(source, target, already_deleted = False):
    source = os.path.abspath(source)
    target = os.path.abspath(target)
    if source == target:
        raise ValueError("source and target must be different paths")
    if not already_deleted:
        if os.path.exists(target):
            shutil.rmtree(target)
        os.mkdir(target)
        already_deleted = True
    
    directory_content = os.listdir(source)
    if not directory_content:
         return True
    for content in directory_content:
        full_path = os.path.join(source, content)
        if os.path.isfile(full_path):
                print(f"{full_path} is a file and will be copied now")
                shutil.copy(full_path, target)
        elif os.path.isdir(full_path):
                print(f"{full_path} is a directory, let's go deeper!")
                new_target = os.path.join(target, content)
                os.mkdir(new_target)
                copy_content(full_path, new_target, already_deleted)
        else:
             raise Exception("Unsupported filetype detected")
    return True


if __name__ == "__main__":
    main()