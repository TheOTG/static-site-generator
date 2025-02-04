import re
from htmlnode import ParentNode, text_node_to_html_node
from text_to_textnode import text_to_textnodes

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading" and block.startswith("# "):
            return get_block_text(block, block_type)
    raise Exception("No title")

def markdown_to_blocks(markdown):
    return list(map(lambda x: x.strip(), markdown.split("\n\n")))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match (block_type):
            case ("heading"):
                block_text = get_block_text(block, block_type)
                header_count = len(block.split(" ", 1)[0])
                block_nodes.append(ParentNode(f"h{header_count}", text_to_children(block_text)))
            case ("code"):
                block_text = get_block_text(block, block_type)
                if block_text.startswith("\n"):
                    block_text = block_text[1:]
                block_nodes.append(ParentNode("pre", [ParentNode("code", text_to_children(block_text))]))
            case ("quote"):
                block_text = get_block_text(block, block_type)
                block_nodes.append(ParentNode("blockquote", text_to_children(block_text)))
            case ("unordered_list"):
                split_block = block.split("\n")
                text_list = map(lambda x: get_block_text(x, block_type), split_block)
                li_list = map(lambda x: ParentNode("li", text_to_children(x)), text_list)
                block_nodes.append(ParentNode("ul", list(li_list)))
            case ("ordered_list"):
                split_block = block.split("\n")
                text_list = map(lambda x: get_block_text(x, block_type), split_block)
                li_list = map(lambda x: ParentNode("li", text_to_children(x)), text_list)
                block_nodes.append(ParentNode("ol", list(li_list)))
            case _:
                block_nodes.append(ParentNode("p", text_to_children(block)))
                pass

    return ParentNode("div", children=block_nodes)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children_nodes = list(map(lambda x: text_node_to_html_node(x), text_nodes))
    return children_nodes

def get_block_text(block, block_type):
    match (block_type):
        case ("heading"):
            split_block = block.split(" ", 1)
            return split_block[1]
        case ("code"):
            return block[3:-3]
        case ("quote"):
            return block[1:].lstrip()
        case ("unordered_list"):
            return block[2:]
        case ("ordered_list"):
            return block[3:]
        case _:
            return block

def block_to_block_type(block):
    is_heading = re.findall(r"(?<!.)\#{1,6} (?=.)", block)
    is_code = block.startswith("```") and block.endswith("```")
    is_quote = True
    is_unordered_list = True
    is_ordered_list = True

    block_lines = block.split("\n")
    for i, line in enumerate(block_lines):
        if line[0] != ">":
            is_quote = False
        if line[:2] != "* " and line[:2] != "- ":
            is_unordered_list = False
        if line[:3] != f"{i+1}. ":
            is_ordered_list = False

    if is_heading:
        return "heading"
    if is_code:
        return "code"
    if is_quote:
        return "quote"
    if is_unordered_list:
        return "unordered_list"
    if is_ordered_list:
        return "ordered_list"
    return "paragraph"