from textnode import TextNode, TextType

def main():
    obj = TextNode("This is some anchor text", TextType.LINKS, "https://www.boot.dev")
    print(obj)


if __name__ == "__main__":
    main()