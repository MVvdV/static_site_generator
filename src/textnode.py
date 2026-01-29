from enum import Enum


class TextType(Enum):
    TEXT = "text"  # text (plain)
    BOLD = "bold"  # **Bold text**
    ITALIC = "italic"  # _Italic text_
    CODE = "code"  # `Code text`
    LINK = "link"  # Links, in this format: [anchor text](url)
    IMAGE = "image"  # Images, in this format: ![alt text](url)


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text  # The text content of the node
        self.text_type = TextType(
            text_type
        )  # The type of text this node contains, which is a member of the TextType enum.
        self.url = url  # The URL of the link or image, if the text is a link. Default to None if nothing is passed in.

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
