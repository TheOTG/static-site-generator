from textnode import TextNode, TextType
from extractmarkdownimages import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
        else:
            split_text = old_node.text.split(delimiter)
            if len(split_text)%2 == 0:
                raise Exception("invalid markdown syntax")
            for i in range(len(split_text)):
                result.append(TextNode(split_text[i], old_node.text_type if i%2 == 0 else text_type))

    return result

def split_nodes_image(old_nodes):
    result = []

    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if not images:
            result.append(old_node)
        else:
            split_text = old_node.text.split(f"![{images[0][0]}]({images[0][1]})", 1)
            extract_first_split = extract_markdown_images(split_text[0])
            if not extract_first_split and split_text[0] != "":
                result.append(TextNode(split_text[0], TextType.TEXT))

            result.append(TextNode(images[0][0], TextType.IMAGE, images[0][1]))

            if split_text[1]:
                result.extend(split_nodes_image([TextNode(split_text[1], TextType.TEXT)]))

    return result

def split_nodes_link(old_nodes):
    result = []

    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if not links:
            result.append(old_node)
        else:
            split_text = old_node.text.split(f"[{links[0][0]}]({links[0][1]})", 1)
            extract_first_split = extract_markdown_links(split_text[0])
            if not extract_first_split and split_text[0] != "":
                result.append(TextNode(split_text[0], TextType.TEXT))

            result.append(TextNode(links[0][0], TextType.LINK, links[0][1]))

            if split_text[1]:
                result.extend(split_nodes_link([TextNode(split_text[1], TextType.TEXT)]))

    return result