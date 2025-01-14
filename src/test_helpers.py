import unittest

from helpers import (
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    markdown_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType


class Testtxttohtmlfn(unittest.TestCase):
    tnode_t = TextNode(
        text="This is a string!", text_type=TextType.TEXT, url="https://www.google.com"
    )
    tnode_b = TextNode(
        text="This is a string!", text_type=TextType.BOLD, url="https://www.google.com"
    )
    tnode_i = TextNode(
        text="This is a string!",
        text_type=TextType.ITALIC,
        url="https://www.google.com",
    )
    tnode_c = TextNode(
        text="This is a string!", text_type=TextType.CODE, url="https://www.google.com"
    )
    tnode_l = TextNode(
        text="This is a string!", text_type=TextType.LINK, url="https://www.google.com"
    )
    tnode_img = TextNode(
        text="This is a string!", text_type=TextType.IMAGE, url="https://www.google.com"
    )

    def test_txttohtml_text(self):
        lnode_t = text_node_to_html_node(self.tnode_t)
        self.assertIsNotNone(lnode_t.value)
        self.assertIsNone(lnode_t.tag)
        self.assertIsNone(lnode_t.props)

    def test_txttohtml_bold(self):
        lnode_b = text_node_to_html_node(self.tnode_b)
        self.assertIsNotNone(lnode_b.value)
        self.assertEqual(lnode_b.tag, "b")
        self.assertIsNone(lnode_b.props)

    def test_txttohtml_italic(self):
        lnode_i = text_node_to_html_node(self.tnode_i)
        self.assertIsNotNone(lnode_i.value)
        self.assertEqual(lnode_i.tag, "i")
        self.assertIsNone(lnode_i.props)

    def test_txttohtml_code(self):
        lnode_c = text_node_to_html_node(self.tnode_c)
        self.assertIsNotNone(lnode_c.value)
        self.assertEqual(lnode_c.tag, "code")
        self.assertIsNone(lnode_c.props)

    def test_txttohtml_link(self):
        lnode_l = text_node_to_html_node(self.tnode_l)
        self.assertIsNotNone(lnode_l.value)
        self.assertEqual(lnode_l.tag, "a")
        self.assertIsNotNone(lnode_l.props)
        self.assertIn("href", lnode_l.props)

    def test_txttohtml_image(self):
        lnode_img = text_node_to_html_node(self.tnode_img)
        self.assertIsNone(lnode_img.value)
        self.assertEqual(lnode_img.tag, "img")
        self.assertIsNotNone(lnode_img.props)
        self.assertIsInstance(lnode_img.props, dict)
        self.assertIn("src", lnode_img.props)
        self.assertIn("alt", lnode_img.props)


class Testsplitnodesfn(unittest.TestCase):
    tnode_t = TextNode(text="This is a string!", text_type=TextType.TEXT)
    tnode_b = TextNode(text="This is a **string!**", text_type=TextType.TEXT)
    tnode_i = TextNode(text="This is a *string!*", text_type=TextType.TEXT)
    tnode_c = TextNode(text="This is a `string!`", text_type=TextType.TEXT)
    tnode_b2 = TextNode(text="This **is** a **string!**", text_type=TextType.TEXT)
    tnode_crazy = TextNode(
        text="First we **bold** then we `code` then we *italicize* and then we're done",
        text_type=TextType.TEXT,
    )

    def test_splitnode_none(self):
        split_nodes = split_nodes_delimiter(
            [self.tnode_t], delimiter="*", text_type=TextType.ITALIC
        )
        self.assertEqual(
            split_nodes, [TextNode("This is a string!", TextType.TEXT, None)]
        )

    def test_splitnode_bold(self):
        split_nodes = split_nodes_delimiter(
            [self.tnode_b], delimiter="**", text_type=TextType.BOLD
        )
        self.assertEqual(
            split_nodes,
            [
                TextNode("This is a ", TextType.TEXT, None),
                TextNode("string!", TextType.BOLD, None),
            ],
        )

    def test_splitnode_italic(self):
        split_nodes = split_nodes_delimiter(
            [self.tnode_i], delimiter="*", text_type=TextType.ITALIC
        )
        self.assertEqual(
            split_nodes,
            [
                TextNode("This is a ", TextType.TEXT, None),
                TextNode("string!", TextType.ITALIC, None),
            ],
        )

    def test_splitnode_code(self):
        split_nodes = split_nodes_delimiter(
            [self.tnode_c], delimiter="`", text_type=TextType.CODE
        )
        self.assertEqual(
            split_nodes,
            [
                TextNode("This is a ", TextType.TEXT, None),
                TextNode("string!", TextType.CODE, None),
            ],
        )

    def test_splitnode_double(self):
        split_nodes = split_nodes_delimiter(
            [self.tnode_b2], delimiter="**", text_type=TextType.BOLD
        )
        self.assertEqual(
            split_nodes,
            [
                TextNode("This ", TextType.TEXT, None),
                TextNode("is", TextType.BOLD, None),
                TextNode(" a ", TextType.TEXT, None),
                TextNode("string!", TextType.BOLD, None),
            ],
        )

    def test_splitnode_multiple(self):
        split_nodes = split_nodes_delimiter(
            [self.tnode_crazy], delimiter="**", text_type=TextType.BOLD
        )
        split_nodes = split_nodes_delimiter(
            split_nodes, delimiter="*", text_type=TextType.ITALIC
        )
        split_nodes = split_nodes_delimiter(
            split_nodes, delimiter="`", text_type=TextType.CODE
        )
        self.assertEqual(
            split_nodes,
            [
                TextNode("First we ", TextType.TEXT, None),
                TextNode("bold", TextType.BOLD, None),
                TextNode(" then we ", TextType.TEXT, None),
                TextNode("code", TextType.CODE, None),
                TextNode(" then we ", TextType.TEXT, None),
                TextNode("italicize", TextType.ITALIC, None),
                TextNode(" and then we're done", TextType.TEXT, None),
            ],
        )


class Testmarkdownextraction(unittest.TestCase):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    text2 = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    text3 = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg). This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"

    def test_extract_markdown_images(self):
        extracted = extract_markdown_images(self.text)
        self.assertEqual(
            extracted,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_markdown_links(self):
        extracted = extract_markdown_links(self.text2)
        self.assertEqual(
            extracted,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extract_markdown_linksandimages(self):
        extracted = extract_markdown_images(self.text3)
        extracted.extend(extract_markdown_links(self.text3))
        self.assertEqual(
            extracted,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
                ("to boot dev", "https://www.boot.dev"),
            ],
        )


class Testsplitnodeimage(unittest.TestCase):
    text_i = TextNode(
        text="This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        text_type=TextType.TEXT,
    )
    text_l = TextNode(
        text="This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        text_type=TextType.TEXT,
    )
    text_mix = TextNode(
        text="This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        text_type=TextType.TEXT,
    )
    text_mix2 = TextNode(
        text="This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        text_type=TextType.TEXT,
    )

    edgecase1 = TextNode(
        text="[to boot dev](https://www.boot.dev) ![to youtube](https://www.youtube.com/@bootdotdev)",
        text_type=TextType.TEXT,
    )
    edgecase2 = TextNode(
        text="[to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
        text_type=TextType.TEXT,
    )
    edgecase3 = TextNode(
        text="[to boot dev](https://www.boot.dev) ![to youtube](https://www.youtube.com/@bootdotdev) hiya!",
        text_type=TextType.TEXT,
    )

    def test_split_nodes_image(self):
        extracted = split_nodes_image([self.text_i])
        self.assertEqual(
            extracted,
            [
                TextNode("This is text with a link ", TextType.TEXT, None),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT, None),
                TextNode(
                    "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_split_nodes_link(self):
        extracted = split_nodes_link([self.text_l])
        self.assertEqual(
            extracted,
            [
                TextNode("This is text with a link ", TextType.TEXT, None),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT, None),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_split_nodes_both(self):
        extracted_i = split_nodes_image([self.text_mix])
        self.assertEqual(
            extracted_i,
            [
                TextNode(
                    "This is text with a link [to boot dev](https://www.boot.dev) and ",
                    TextType.TEXT,
                    None,
                ),
                TextNode(
                    "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )
        extracted_l = split_nodes_link([self.text_mix2])
        self.assertEqual(
            extracted_l,
            [
                TextNode("This is text with a link ", TextType.TEXT, None),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    " and ![to youtube](https://www.youtube.com/@bootdotdev)",
                    TextType.TEXT,
                    None,
                ),
            ],
        )

        combo = split_nodes_link(extracted_i)
        self.assertEqual(
            combo,
            [
                TextNode("This is text with a link ", TextType.TEXT, None),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT, None),
                TextNode(
                    "to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_splitnode_edgecases(self):
        extracted_i_e1 = split_nodes_image([self.edgecase1])
        extracted_l_e1 = split_nodes_link([self.edgecase1])
        combo_e1_ItoL = split_nodes_link(extracted_i_e1)
        combo_e1_LtoI = split_nodes_image(extracted_l_e1)
        self.assertEqual(combo_e1_ItoL, combo_e1_LtoI)

        extracted_i_e1 = split_nodes_image([self.edgecase2])
        extracted_l_e1 = split_nodes_link([self.edgecase2])
        combo_e1_ItoL = split_nodes_link(extracted_i_e1)
        combo_e1_LtoI = split_nodes_image(extracted_l_e1)
        self.assertEqual(combo_e1_ItoL, combo_e1_LtoI)

        extracted_i_e1 = split_nodes_image([self.edgecase3])
        extracted_l_e1 = split_nodes_link([self.edgecase3])
        combo_e1_ItoL = split_nodes_link(extracted_i_e1)
        combo_e1_LtoI = split_nodes_image(extracted_l_e1)
        self.assertEqual(combo_e1_ItoL, combo_e1_LtoI)


class Testtexttonode(unittest.TestCase):
    def test_texttonode_sim(self):
        txt = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        ans = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(txt, ans)


class Testmarkdowntoblocks(unittest.TestCase):
    tester = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
    """

    def test_simple_markd2block(self):
        res = markdown_to_blocks(self.tester)
        ans = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]

        self.assertEqual(res, ans)


class Testblocktoblock(unittest.TestCase):
    def test_headers(self):
        head1 = "# ayo"
        head2 = "### yea"
        head3 = "###### yea"
        nohead1 = " # yea"
        nohead2 = "  yea"
        nohead3 = "####### yea"

        self.assertEqual(block_to_block_type(head1), "heading")
        self.assertEqual(block_to_block_type(head2), "heading")
        self.assertEqual(block_to_block_type(head3), "heading")
        self.assertEqual(block_to_block_type(nohead1), "paragraph")
        self.assertEqual(block_to_block_type(nohead2), "paragraph")
        self.assertEqual(block_to_block_type(nohead3), "paragraph")

    def test_code(self):
        code1 = "``` this is code ```"
        code2 = "```alsocode```"
        code3 = "````dis code too````"
        nocode1 = " ``` not code ```"
        nocode2 = "``` not code ``` "
        nocode3 = "`` not code```"
        nocode4 = "``` not code``"

        self.assertEqual(block_to_block_type(code1), "code")
        self.assertEqual(block_to_block_type(code2), "code")
        self.assertEqual(block_to_block_type(code3), "code")
        self.assertEqual(block_to_block_type(nocode1), "paragraph")
        self.assertEqual(block_to_block_type(nocode2), "paragraph")
        self.assertEqual(block_to_block_type(nocode3), "paragraph")
        self.assertEqual(block_to_block_type(nocode4), "paragraph")

    def test_quote(self):
        quote1 = ">quote\n>and quote"
        quote2 = ">quote too"
        quote3 = "> also a \n>quote ya\n>feel?"
        noquote1 = " >not a quote"
        noquote2 = ">totall\nnot a quote"
        noquote3 = "no quote > here"

        self.assertEqual(block_to_block_type(quote1), "quote")
        self.assertEqual(block_to_block_type(quote2), "quote")
        self.assertEqual(block_to_block_type(quote3), "quote")
        self.assertEqual(block_to_block_type(noquote1), "paragraph")
        self.assertEqual(block_to_block_type(noquote2), "paragraph")
        self.assertEqual(block_to_block_type(noquote3), "paragraph")

    def test_unorlist(self):
        unor_list = "* this\n* is\n* a list"
        unor_list2 = "- this\n- is\n- a list"
        unor_list_mix = "- this\n* is a list"
        no_unor_list = "*thisisnt a list"
        no_unor_list2 = "* this isnt\n*alist"
        no_unor_list3 = "* this is not\n^ a list"

        self.assertEqual(block_to_block_type(unor_list), "unordered_list")
        self.assertEqual(block_to_block_type(unor_list2), "unordered_list")
        self.assertEqual(block_to_block_type(unor_list_mix), "unordered_list")
        self.assertEqual(block_to_block_type(no_unor_list), "paragraph")
        self.assertEqual(block_to_block_type(no_unor_list2), "paragraph")
        self.assertEqual(block_to_block_type(no_unor_list3), "paragraph")

    def test_ordlist(self):
        or_list = "1. this is numbered list"
        or_list2 = "1. this is also\n2. a good ord list"
        or_list3 = "1. testing\n2. a long one\n3. ya\n4. dig?"
        or_list4 = "1. a\n2. a\n3. a\n4. a\n5. a\n6. a\n7. a\n8. a\n9. a\n10. a"
        not_or_list1 = "1.not ord list"
        not_or_list2 = "1. not an ord\n3. listing"
        not_or_list3 = "1. this is\n 2. wrong"
        not_or_list4 = "1. this is not\n$. a list too"
        not_or_list5 = "0. this is not\n1. a list too"

        self.assertEqual(block_to_block_type(or_list), "ordered_list")
        self.assertEqual(block_to_block_type(or_list2), "ordered_list")
        self.assertEqual(block_to_block_type(or_list3), "ordered_list")
        self.assertEqual(block_to_block_type(or_list4), "ordered_list")
        self.assertEqual(block_to_block_type(not_or_list1), "paragraph")
        self.assertEqual(block_to_block_type(not_or_list2), "paragraph")
        self.assertEqual(block_to_block_type(not_or_list3), "paragraph")
        self.assertEqual(block_to_block_type(not_or_list4), "paragraph")
        self.assertEqual(block_to_block_type(not_or_list5), "paragraph")

    def test_par(self):
        par = "regular string!"
        par1 = "#some changes but nothing big ```"

        self.assertEqual(block_to_block_type(par), "paragraph")
        self.assertEqual(block_to_block_type(par1), "paragraph")


class Testmarkdown_to_html_node(unittest.TestCase):
    def test_headers(self):
        tester = "# Title"
        res = markdown_to_html_node(tester)
        ans = ParentNode(
            tag="div",
            children=[ParentNode(tag="h1", children=[LeafNode(value="Title")])],
        )
        self.assertEqual(res.tag, ans.tag)

    def test_code(self):
        tester = "```coding```"
        res = markdown_to_html_node(tester)
        ans = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="pre",
                    children=[
                        ParentNode(tag="code", children=[LeafNode(value="coding")])
                    ],
                )
            ],
        )
        self.assertEqual(res.children[0].tag, ans.children[0].tag)

    def test_quote(self):
        tester = ">blocks\n>of quotes"
        res = markdown_to_html_node(tester)
        ans = ParentNode(
            tag="div",
            children=[ParentNode(tag="blockquote", children=[LeafNode(value="Title")])],
        )
        self.assertEqual(res.children[0].tag, ans.children[0].tag)

    def test_unord_list(self):
        tester = "* this is\n* a list"
        res = markdown_to_html_node(tester)
        ans = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="ul",
                    children=[
                        ParentNode(tag="li", children=[LeafNode(value="this is")]),
                        ParentNode(tag="li", children=[LeafNode(value="a list")]),
                    ],
                )
            ],
        )
        self.assertEqual(res.children[0].tag, ans.children[0].tag)

    def test_ord_list(self):
        tester = "1. first\n2. second"
        res = markdown_to_html_node(tester)
        ans = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="ol",
                    children=[
                        ParentNode(tag="li", children=[LeafNode(value="first")]),
                        ParentNode(tag="li", children=[LeafNode(value="second")]),
                    ],
                )
            ],
        )
        self.assertEqual(res.children[0].tag, ans.children[0].tag)


if __name__ == "__main__":
    unittest.main()
