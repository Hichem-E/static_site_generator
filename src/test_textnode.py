import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_textnode_eq(self):
        # Same nodes
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        # same nodes with a url
        node3 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node4 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node3, node4)


    def test_textnode_noteq(self):
        # Different text
        node = TextNode("This is a text node maybe?", TextType.BOLD)
        node1 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node1)

        # Different text type
        node2 = TextNode("This is a text node", TextType.CODE)
        node3 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node2, node3)

        # Same text and textype, different link
        node4 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node5 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertNotEqual(node4, node5)

        # Different everything
        node6 = TextNode("This is a text", TextType.BOLD, "https://www.boot.dev")
        node7 = TextNode("Welcome home", TextType.IMAGE, "https://www.google.dev")
        self.assertNotEqual(node6, node7)

    def test_textnode_create(self):
        node = TextNode("This is a text node maybe?", TextType.BOLD, "https://www.google.dev")
        self.assertEqual(type(node.text_type), type(TextType.ITALIC))
        self.assertEqual(type("H"), type(node.text))
        self.assertEqual(type("H"), type(node.url))

if __name__=="__main__":
    unittest.main()
