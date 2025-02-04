from textnode import TextNode, TextType

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        html = []
        for prop in self.props:
            html.append(f' {prop}="{self.props[prop]}"')
        return "".join(html)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is required")
        elif not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required")
        elif not self.children:
            raise ValueError("children is required")
        children_to_html = "".join(map(lambda x: x.to_html(), self.children))
        return f"<{self.tag}{self.props_to_html()}>{children_to_html}</{self.tag}>"
    
def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case (TextType.TEXT):
            return LeafNode(None, text_node.text)
        case (TextType.BOLD):
            return LeafNode("b", text_node.text)
        case (TextType.ITALIC):
            return LeafNode("i", text_node.text)
        case (TextType.CODE):
            return LeafNode("code", text_node.text)
        case (TextType.LINK):
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case (TextType.IMAGE):
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("invalid text node")
