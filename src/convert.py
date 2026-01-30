from blocktype import BlockType
from htmlnode import LeafNode, ParentNode
from parse import block_to_block_type, markdown_to_blocks, text_to_textnodes
from textnode import TextNode, TextType


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def heading_block_to_html(block):
    level = block.count("#", 0, block.index(" "))
    text = block[level + 1 :].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_block_to_html(block):
    lines = block.split("\n")
    code_lines = lines[1:-1]
    if code_lines:
        stripped_lines = [line.lstrip() for line in code_lines]
        code_content = "\n".join(stripped_lines) + "\n"
    else:
        code_content = ""
    code_leaf = LeafNode("code", code_content)
    return ParentNode("pre", [code_leaf])


def quote_block_to_html(block):
    lines = block.split("\n")
    cleaned_lines = [line.lstrip().lstrip(">").lstrip() for line in lines]
    text = "\n".join(cleaned_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)


def unordered_list_block_to_html(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("- "):
            text = stripped[2:]
        elif stripped.startswith("* "):
            text = stripped[2:]
        else:
            text = stripped
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)


def ordered_list_block_to_html(block):
    lines = block.split("\n")
    list_items = []
    for line in lines:
        stripped = line.lstrip()
        # Find where the number ends and ". " begins
        if ". " in stripped:
            text = stripped[stripped.index(". ") + 2 :]
        else:
            text = stripped
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)


def paragraph_block_to_html(block):
    lines = block.split("\n")
    stripped_lines = [line.strip() for line in lines]
    text = " ".join(stripped_lines)
    children = text_to_children(text)
    return ParentNode("p", children)


def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise Exception(f"Provided value {text_node} is not a TextNode")
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            block_node = heading_block_to_html(block)
        elif block_type == BlockType.CODE:
            block_node = code_block_to_html(block)
        elif block_type == BlockType.QUOTE:
            block_node = quote_block_to_html(block)
        elif block_type == BlockType.UNORDERED_LIST:
            block_node = unordered_list_block_to_html(block)
        elif block_type == BlockType.ORDERED_LIST:
            block_node = ordered_list_block_to_html(block)
        else:  # PARAGRAPH
            block_node = paragraph_block_to_html(block)

        block_nodes.append(block_node)

    return ParentNode("div", block_nodes)
