import re

def extract_markdown_images(text):
    alt_text_list = re.findall(r"\!\[(.*?)\]", text)
    url_list = re.findall(r"\((.*?)\)", text)
    return list(zip(alt_text_list, url_list))

def extract_markdown_links(text): # (?<!!)\[(.*?)\]\((.*?)\)
    link_list = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return link_list