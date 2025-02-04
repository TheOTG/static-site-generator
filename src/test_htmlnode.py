import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):
        node = HTMLNode("p", "this is a paragraph")
        node2 = HTMLNode("a", "this is a link", None, {"href": "www.google.com"})
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(node2.props_to_html(), ' href="www.google.com"')

    def test_leafnode(self):
        node = LeafNode("p", "this is a paragraph")
        node2 = LeafNode("a", "this is a link", {"href": "www.google.com"})
        node3 = LeafNode("", "this is a raw text")
        node4 = LeafNode("", None)
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(node2.props_to_html(), ' href="www.google.com"')
        self.assertEqual(node.to_html(), "<p>this is a paragraph</p>")
        self.assertEqual(node2.to_html(), '<a href="www.google.com">this is a link</a>')
        self.assertEqual(node3.props_to_html(), "")
        self.assertEqual(node3.to_html(), "this is a raw text")
        self.assertRaises(ValueError, lambda: node4.to_html())

    def test_parentnode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node3 = ParentNode(
            "a",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"href": "www.google.com"}
        )

        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        self.assertEqual(
            node2.to_html(),
            "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        self.assertEqual(node3.to_html(), '<a href="www.google.com"><b>Bold text</b>Normal text<i>italic text</i>Normal text</a>')

    def test_text_node_to_html_node(self):
        node = text_node_to_html_node(TextNode("normal text", TextType.TEXT))
        node2 = text_node_to_html_node(TextNode("bold text", TextType.BOLD))
        node3 = text_node_to_html_node(TextNode("italic text", TextType.ITALIC))
        node4 = text_node_to_html_node(TextNode("code text", TextType.CODE))
        node5 = text_node_to_html_node(TextNode("this is a link", TextType.LINK, "www.google.com"))
        node6 = text_node_to_html_node(TextNode("alt image text", TextType.IMAGE, "wow.jpg"))

        self.assertEqual(node.to_html(), "normal text")
        self.assertEqual(node2.to_html(), "<b>bold text</b>")
        self.assertEqual(node3.to_html(), "<i>italic text</i>")
        self.assertEqual(node4.to_html(), "<code>code text</code>")
        self.assertEqual(node5.to_html(), '<a href="www.google.com">this is a link</a>')
        self.assertEqual(node6.to_html(), '<img src="wow.jpg" alt="alt image text"></img>')

if __name__ == "__main__":
    unittest.main()