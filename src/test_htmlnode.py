import unittest

from htmlnode import HTMLNODE


class TestHtmlNode(unittest.TestCase):
    def test_htmlnode_params(self):
        tag = "h1"
        value = "words"
        children = ["p", "tb"]
        props = "bunch of text"
        node = HTMLNODE(tag, value, children, props)

        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)


    def test_htmlnode_paramchange(self):
        tag = "h1"
        value = "words"
        children = ["p", "tb"]
        props = "bunch of text"
        node = HTMLNODE(tag, value, children, props)

        node.value = "new stuff"
        self.assertNotEqual(node.value, value)
        self.assertEqual(node.value, "new stuff")

    def test_htmlnode_create(self):
        node = HTMLNODE()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_htmlnode_propstohtml(self):
        node = HTMLNODE(tag="p", value="a block of text", children=None, props={"href": "https://www.google.com"})
        self.assertEqual(' href="https://www.google.com"', node.props_to_html())


if __name__=="__main__":
    unittest.main()
