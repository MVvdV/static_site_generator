class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # A string, HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value  # A string, the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children  # A list of child HTMLNode objects
        self.props = props  # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None or len(self.props.items()) == 0:
            return ""
        return "".join(
            list(map(lambda item: f" {item[0]}='{item[1]}'", self.props.items()))
        )

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(self, other):
        if not isinstance(other, LeafNode):
            return False
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        )

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError(
                "Invalid HTML: not a ParentNode, no children, should be LeafNode"
            )
        children_html = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __eq__(self, other):
        if not isinstance(other, ParentNode):
            return False
        return (
            self.tag == other.tag
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
