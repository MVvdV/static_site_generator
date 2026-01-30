import unittest
from blocktype import BlockType


class TestBlockType(unittest.TestCase):
    def test_values(self):
        self.assertEqual(BlockType.PARAGRAPH.value, "paragraph")
        self.assertEqual(BlockType.HEADING.value, "heading")
        self.assertEqual(BlockType.CODE.value, "code")
        self.assertEqual(BlockType.QUOTE.value, "quote")
        self.assertEqual(BlockType.UNORDERED_LIST.value, "unordered_list")
        self.assertEqual(BlockType.ORDERED_LIST.value, "ordered_list")


if __name__ == "__main__":
    unittest.main()
