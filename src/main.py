import re

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from utils import extract_markdown_images, extract_markdown_links


def main():
    # node = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    # print(node)

    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(re.split(r"(?<!\!)(\[.*?\]\(.*?\))", text))


if __name__ == "__main__":
    main()
