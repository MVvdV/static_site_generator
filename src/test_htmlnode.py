import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node0 = HTMLNode("a", "Awesome")
        node1 = HTMLNode("h1", "Awesome Blog Heading 1", node0)
        node2 = HTMLNode("h1", "Awesome Blog Heading 1", node0)
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = HTMLNode("h1", "Awesome Blog Heading 1")
        node2 = HTMLNode("h2", "Awesome Blog Heading 2")
        self.assertNotEqual(node1, node2)
        node3 = HTMLNode("h1", "Awesome Blog Heading 1")
        node4 = HTMLNode("p", "Awesome Blog Pargraph", props={"width": "100%"})
        self.assertNotEqual(node3, node4)

    def test_props(self):
        node1 = HTMLNode(
            "a",
            "click here",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertIsInstance(node1.props, dict)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!", {"width": "100%"})
        self.assertEqual(node.to_html(), "<p width='100%'>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(
            "a",
            "Hello, world!",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.to_html(),
            "<a href='https://www.google.com' target='_blank'>Hello, world!</a>",
        )


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children_and_grandchildren(self):
        grandchild_node1 = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode(
            "a", "grandchild_a", {"href": "https://www.google.com", "target": "_blank"}
        )
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        child_node2 = ParentNode("span", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><a href='https://www.google.com' target='_blank'>grandchild_a</a></span><span><b>grandchild</b><a href='https://www.google.com' target='_blank'>grandchild_a</a></span></div>",
        )

    def test_to_html_with_multiple_parents(self):
        grandchild_node1 = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode(
            "a", "grandchild_a", {"href": "https://www.google.com", "target": "_blank"}
        )
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        child_node2 = ParentNode("span", [grandchild_node1, grandchild_node2])
        parent_node1 = ParentNode("div", [child_node1])
        parent_node2 = ParentNode("div", [child_node1])
        parent_node3 = ParentNode(
            "div", [parent_node1, child_node1, child_node2, parent_node2]
        )
        self.assertEqual(
            parent_node3.to_html(),
            "<div><div><span><b>grandchild</b><a href='https://www.google.com' target='_blank'>grandchild_a</a></span></div><span><b>grandchild</b><a href='https://www.google.com' target='_blank'>grandchild_a</a></span><span><b>grandchild</b><a href='https://www.google.com' target='_blank'>grandchild_a</a></span><div><span><b>grandchild</b><a href='https://www.google.com' target='_blank'>grandchild_a</a></span></div></div>",
        )


if __name__ == "__main__":
    unittest.main()
