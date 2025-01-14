import re
from functools import reduce

from htmlnode import HTMLNODE
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(value=text_node.text, tag="b")
        case TextType.ITALIC:
            return LeafNode(value=text_node.text, tag="i")
        case TextType.CODE:
            return LeafNode(value=text_node.text, tag="code")
        case TextType.LINK:
            return LeafNode(
                value=text_node.text, tag="a", props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                value=None,
                tag="img",
                props={"src": text_node.url, "alt": text_node.text},
            )


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []

    for node in old_nodes:
        split_line = node.text.split(delimiter)
        if len(split_line) == 1:
            res.append(node)
            continue

        new_type = False
        for i in range(len(split_line)):
            if not split_line[i] and i == 0:
                new_type = True
                continue
            if i == len(split_line) - 1 and split_line[i] == "":
                continue

            if new_type:
                res.append(TextNode(text=split_line[i], text_type=text_type))
            else:
                res.append(TextNode(text=split_line[i], text_type=node.text_type))
            new_type = not new_type
    return res


def split_nodes_image(old_nodes):
    res = []

    for node in old_nodes:
        extracted_images = extract_markdown_images(node.text)
        if not extracted_images:
            res.append(node)
            continue

        working_list = node.text

        for image in extracted_images:
            working_list = working_list.split(f"![{image[0]}]({image[1]})", 1)
            if not working_list[0]:
                res.append(
                    TextNode(text=image[0], text_type=TextType.IMAGE, url=image[1])
                )

            else:
                res.append(TextNode(text=working_list[0], text_type=node.text_type))
                res.append(
                    TextNode(text=image[0], text_type=TextType.IMAGE, url=image[1])
                )
            working_list = working_list[1]

        if working_list:
            res.append(TextNode(text=working_list, text_type=node.text_type))
    return res


def split_nodes_link(old_nodes):
    res = []

    for node in old_nodes:
        extracted_links = extract_markdown_links(node.text)
        if not extracted_links:
            res.append(node)
            continue

        working_list = node.text

        for link in extracted_links:
            working_list = working_list.split(f"[{link[0]}]({link[1]})", 1)
            if not working_list[0]:
                res.append(TextNode(text=link[0], text_type=TextType.LINK, url=link[1]))

            else:
                res.append(TextNode(text=working_list[0], text_type=node.text_type))
                res.append(TextNode(text=link[0], text_type=TextType.LINK, url=link[1]))
            working_list = working_list[1]

        if working_list:
            res.append(TextNode(text=working_list, text_type=node.text_type))
    return res


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def text_to_textnodes(text):
    res = [TextNode(text=text, text_type=TextType.TEXT)]
    delimiters = [
        ("`", TextType.CODE),
        ("**", TextType.BOLD),
        ("*", TextType.ITALIC),
    ]

    for delimiter, text_type in delimiters:
        res = split_nodes_delimiter(res, delimiter, text_type)

    res = split_nodes_image(res)
    res = split_nodes_link(res)
    return res


def markdown_to_blocks(markdown):
    return list(
        filter(lambda x: x, list(map(lambda x: x.strip(), markdown.split("\n\n"))))
    )


def block_to_block_type(markdown):
    if re.search(r"^\#{1,6}\ ", markdown):
        return "heading"
    if re.search(r"^\`{3}.*`{3}$", markdown):
        # if markdown[0:3] == "```" and markdown[-3:] == "```":
        return "code"

    line_arr = markdown.split("\n")
    num_lines = len(line_arr)
    quote_check = len(list(filter(lambda x: x[0] == ">", line_arr)))
    if quote_check == num_lines:
        return "quote"

    check_str_sizes = len(list(filter(lambda x: len(x) > 2, line_arr)))
    if check_str_sizes != num_lines:
        return "paragraph"

    unord_list = len(list(filter(lambda x: x[0:2] == "* " or x[0:2] == "- ", line_arr)))
    if unord_list == num_lines:
        return "unordered_list"

    ord_list = list(filter(lambda x: re.search(r"^\d+. {1}", x), line_arr))
    if len(ord_list) == num_lines:
        res = []
        for text in ord_list:
            i = 0
            while text[i] != ".":
                i += 1
            res.append(int(text[:i]))

        ordered = True
        for i in range(len(res)):
            if i + 1 == res[i]:
                continue
            else:
                return "paragraph"
        if ordered:
            return "ordered_list"

    return "paragraph"


def markdown_to_html_node(markdown):
    blocked_md = markdown_to_blocks(markdown)
    # print(blocked_md)
    res = []
    for block in blocked_md:
        res.append(block_to_html(block))

    return ParentNode(tag="div", children=res)


def block_to_html(block):
    block_type = block_to_block_type(block)

    if block_type == "paragraph":
        arr_text_nodes = block_text_TN_HTMLN(block)
        new_parent = ParentNode(tag="p", children=arr_text_nodes)

    if block_type == "heading":
        idx_cut = 0
        while block[idx_cut] == "#":
            idx_cut += 1
        idx_cut += 1
        arr_text_nodes = block_text_TN_HTMLN(block, idx_cut)
        new_parent = ParentNode(tag=f"h{idx_cut - 1}", children=arr_text_nodes)

    if block_type == "code":
        arr_text_nodes = block_text_TN_HTMLN(block[3:-3])
        pre_parent = ParentNode(tag="code", children=arr_text_nodes)
        new_parent = ParentNode(tag="pre", children=[pre_parent])

    if block_type == "quote":
        idx_cut = 1
        arr_text_nodes = block_text_TN_HTMLN(block, idx_cut)
        new_parent = ParentNode(tag="blockquote", children=arr_text_nodes)

    if block_type == "unordered_list":
        idx_cut = 2
        arr_text_nodes = block_text_TN_HTMLN(block, idx_cut)

        li_parents = []
        for node in arr_text_nodes:
            li_parents.append(ParentNode(tag="li", children=node))
        # li_parent = ParentNode(tag="li", children = arr_text_nodes)
        new_parent = ParentNode(tag="ul", children=li_parents)

    if block_type == "ordered_list":
        arr_text_nodes = block_text_TN_HTMLN(block, ord_list=True)

        li_parents = []
        for node in arr_text_nodes:
            li_parents.append(ParentNode(tag="li", children=node))
        # li_parent = ParentNode(tag="li", children = arr_text_nodes)
        new_parent = ParentNode(tag="ol", children=li_parents)

    return new_parent


def block_text_TN_HTMLN(block, idx_cut=0, ord_list=False):
    if ord_list is True:
        block = find_first_space(block)
        arr_text_nodes = list(map(text_to_textnodes, block))

    else:
        arr_text_nodes = list(
            map(text_to_textnodes, list(map(lambda x: x[idx_cut:], block.split("\n"))))
        )

    for i in range(len(arr_text_nodes)):
        for j in range(len(arr_text_nodes[i])):
            arr_text_nodes[i][j] = text_node_to_html_node(arr_text_nodes[i][j])

    arr_text_nodes = reduce(lambda x, y: x + y, arr_text_nodes, [])
    # arr_text_nodes = arr_text_nodes[0]

    return arr_text_nodes


def find_first_space(texts):
    arr_of_texts = texts.split("\n")
    res = []
    for arr in arr_of_texts:
        i = 0
        while arr[i] != " ":
            i += 1

        res.append(arr[i + 1 :])
    return res


# tester = "# **first *real* header**\n\n```this is some crazy code```\n\n1. l1\n2. l2\n\n para"
# tester = "# Title\n\nParagraph"
# htmlcode = markdown_to_html_node(tester)
# print(htmlcode.tag, htmlcode.children)


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        btype = block_to_block_type(block)
        if btype == "heading":
            if block[0:2] == "# ":
                return block[2:].strip()

    raise Exception("No title")
