import re

from blocktype import BlockType
from textnode import TextNode, TextType


def markdown_to_blocks(markdown):
    blocks = list(filter(None, map(str.strip, markdown.split("\n\n"))))
    return blocks


def block_to_block_type(block):
    lines = block.split("\n")

    # Heading
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    # Code
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE

    # Quote
    if all(line.lstrip().startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered List
    if all(
        line.lstrip().startswith("- ") or line.lstrip().startswith("* ")
        for line in lines
    ):
        return BlockType.UNORDERED_LIST

    # Ordered List
    is_ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.lstrip().startswith(f"{i}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    if blocks[0].startswith("# "):
        return blocks[0][2:].strip()
    else:
        raise Exception("Could not extract Title, no h1 (#) found.")


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise Exception(
                f"No closing delimiter {delimiter} found, invalid markdown."
            )
        parts = node.text.split(delimiter)
        for i in range(len(parts)):
            if i % 2 != 0:
                new_nodes.append(TextNode(parts[i], text_type))
            else:
                if parts[i] == "":
                    continue
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(extract_markdown_images(node.text)) == 0:
            new_nodes.append(node)
            continue
        parts = re.split(r"(!\[.*?\]\(.*?\))", node.text)
        for part in parts:
            image = extract_markdown_images(part)
            if part is None or part == "":
                continue
            elif len(image) == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(
                    TextNode(f"{image[0][0]}", TextType.IMAGE, f"{image[0][1]}")
                )
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if len(extract_markdown_links(node.text)) == 0:
            new_nodes.append(node)
            continue
        parts = re.split(r"(?<!\!)(\[.*?\]\(.*?\))", node.text)
        for part in parts:
            link = extract_markdown_links(part)
            if part is None or part == "":
                continue
            elif len(link) == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(
                    TextNode(f"{link[0][0]}", TextType.LINK, f"{link[0][1]}")
                )
    return new_nodes


def text_to_textnodes(text):
    nodes_start = [TextNode(text, TextType.TEXT)]

    nodes_image = split_nodes_image(nodes_start)
    nodes_link = split_nodes_link(nodes_image)
    nodes_bold = split_nodes_delimiter(nodes_link, "**", TextType.BOLD)
    nodes_italic = split_nodes_delimiter(nodes_bold, "_", TextType.ITALIC)
    nodes_code = split_nodes_delimiter(nodes_italic, "`", TextType.CODE)

    return nodes_code
