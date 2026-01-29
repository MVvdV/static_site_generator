import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)
        node3 = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("", TextType.BOLD)
        self.assertNotEqual(node3, node4)
        node5 = TextNode("This is a text node", TextType.BOLD)
        node6 = TextNode("www.apple.com", TextType.LINK, "www.apple.com")
        self.assertNotEqual(node5, node6)

    def test_text_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        self.assertIsInstance(node1.text_type, TextType)

    def test_url(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node1.url)


if __name__ == "__main__":
    unittest.main()
