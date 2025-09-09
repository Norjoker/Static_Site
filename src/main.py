from textnode import TextNode, TextType
import os
import shutil

def main():
    source = os.getcwd() + "/static/"
    target = os.getcwd() + "/public/"
    #copy_content(source, target)
    print(os.path.exists(source))
    print(os.path.exists(source))

def copy_content(source, target):
    shutil.rmtree(target)
    os.makedirs(target)


if __name__ == "__main__":
    main()