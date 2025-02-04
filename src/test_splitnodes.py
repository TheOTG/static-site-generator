import unittest

from textnode import TextNode, TextType
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link

class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block`, *italic*, and **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a `code block`, *italic*, and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

        new_nodes2 = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)

        self.assertEqual(
            new_nodes2,
            [
                TextNode("This is text with a `code block`, ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

        new_nodes3 = split_nodes_delimiter(new_nodes2, "`", TextType.CODE)

        self.assertEqual(
            new_nodes3,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(", ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(", and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

        self.assertRaises(Exception, split_nodes_delimiter(new_nodes3, "*", TextType.ITALIC))

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ]
        )

        node2 = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and ![test img](img.jpg) and [link](www.google.com)",
            TextType.TEXT
        )
        new_nodes2 = split_nodes_image([node2])
        self.assertEqual(
            new_nodes2,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("test img", TextType.IMAGE, "img.jpg"),
                TextNode(" and [link](www.google.com)", TextType.TEXT),
            ]
        )

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ]
        )

    def test_split_nodes_image_link(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and ![test img](img.jpg) and [link](www.google.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("test img", TextType.IMAGE, "img.jpg"),
                TextNode(" and [link](www.google.com)", TextType.TEXT),
            ]
        )

        new_nodes2 = split_nodes_link(new_nodes)
        self.assertEqual(
            new_nodes2,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("test img", TextType.IMAGE, "img.jpg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.google.com"),
            ]
        )

    def test_split_nodes_link_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and ![test img](img.jpg) and [link](www.google.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and ![test img](img.jpg) and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.google.com"),
            ]
        )

        new_nodes2 = split_nodes_image(new_nodes)
        self.assertEqual(
            new_nodes2,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("test img", TextType.IMAGE, "img.jpg"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "www.google.com"),
            ]
        )

if __name__ == "__main__":
    unittest.main()