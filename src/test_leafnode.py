import unittest

from leafnode import LeafNode


class TestHtmlNode(unittest.TestCase):
    def test_leafnode_valcheck(self):
        node = LeafNode(value=None)
        self.assertRaises(ValueError, node.to_html)

    def test_leafnode_childrenone(self):
        node = LeafNode(value=None)
        self.assertIsNone(node.children)

    def test_leafnode_tohtml(self):
        node = LeafNode(value="this is a val!", tag="a")
        self.assertEqual(node.to_html(), "<a>this is a val!</a>")

        node1 = LeafNode(
            value="this is a val!", tag="a", props={"href": "https://www.google.com"}
        )
        self.assertEqual(
            node1.to_html(), '<a href="https://www.google.com">this is a val!</a>'
        )


if __name__ == "__main__":
    unittest.main()
