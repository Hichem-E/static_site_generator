import unittest
from leafnode import LeafNode
from parentnode import ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_parentnode_singlelayer(self):
        node = ParentNode(
            tag="p", 
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_parentnode_twolayer(self):
        node = ParentNode(
                tag="p", 
                children=[
                    ParentNode(tag="c", children=[LeafNode("b", "Bold text"), LeafNode(None, "Normal text")]),
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                ]
            )
        self.assertEqual(node.to_html(), "<p><c><b>Bold text</b>Normal text</c><b>Bold text</b>Normal text</p>")

    def test_parentnode_leafwithprop(self):
        node = ParentNode(
                tag="p", 
                children=[
                    ParentNode(tag="c", children=[LeafNode("b", "Bold text"), LeafNode(None, "Normal text")]),
                    LeafNode("b", "Bold text", props={"href": "https://www.google.com"}),
                    LeafNode(None, "Normal text"),
                ],
            )
        self.assertEqual(node.to_html(), '<p><c><b>Bold text</b>Normal text</c><b href="https://www.google.com">Bold text</b>Normal text</p>')
        
    def test_parentnode_leafwithmultiprop(self):
        node = ParentNode(
                tag="p", 
                children=[
                    ParentNode(tag="c", children=[LeafNode("b", "Bold text"), LeafNode(None, "Normal text")]),
                    LeafNode("b", "Bold text", props={"href": "https://www.google.com", "target": "_blank"}),
                    LeafNode(None, "Normal text"),
                ],
            )
        self.assertEqual(node.to_html(), '<p><c><b>Bold text</b>Normal text</c><b href="https://www.google.com" target="_blank">Bold text</b>Normal text</p>')

    def test_parentnode_pwithprop(self):
        node = ParentNode(
                tag="p", 
                children=[
                    ParentNode(tag="c", children=[LeafNode("b", "Bold text"), LeafNode(None, "Normal text")]),
                    LeafNode("b", "Bold text", props={"href": "https://www.google.com", "target": "_blank"}),
                    LeafNode(None, "Normal text"),
                ],
                props={"target": "_blank"}
            )
        self.assertEqual(node.to_html(), '<p target="_blank"><c><b>Bold text</b>Normal text</c><b href="https://www.google.com" target="_blank">Bold text</b>Normal text</p>')

    def test_parentnode_nestedparentwprops(self):
        node = ParentNode(
                tag="p", 
                children=[
                    ParentNode(tag="c", children=[LeafNode("b", "Bold text"), LeafNode("i", "Italic text", props={"href": "https://www.google.com"})], props={"target": "_blank"}),
                    LeafNode("b", "Bold text"),
                    LeafNode(None, "Normal text"),
                ],
            )
        self.assertEqual(node.to_html(), '<p><c target="_blank"><b>Bold text</b><i href="https://www.google.com">Italic text</i></c><b>Bold text</b>Normal text</p>')




if __name__=="__main__":
    unittest.main()
