from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link

def text_to_textnodes(text):
    base_text = TextNode(text, TextType.TEXT)

    split_bold = split_nodes_delimiter([base_text], "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "*", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    split_image = split_nodes_image(split_code)
    split_link = split_nodes_link(split_image)

    return split_link