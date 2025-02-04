import unittest

from blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        blocks = markdown_to_blocks(
"""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        )
        # print(blocks, "===")
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                """* This is the first list item in a list block
* This is a list item
* This is another list item"""
            ]
        )

    def test_block_to_block_type(self):
        block = "# This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "heading")

        block = "## This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "heading")

        block = "### This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "heading")

        block = "#### This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "heading")

        block = "##### This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "heading")

        block = "###### This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "heading")

        block = "####### This is a normal paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = " # This is a normal paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = " ## This is a normal paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = "```This is a code block```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "code")

        block = " ```This is a normal paragraph```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = "```This is a normal paragraph``` "
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = ">This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "quote")

        block = "> This is a quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "quote")

        block = " >This is a normal paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = """* This is the first list item in a unordered list block
* This is a list item
* This is another list item"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "unordered_list")

        block = """* This is the first list item in a unordered list block
- This is a still a list item
* This is another list item"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "unordered_list")

        block = """* This is the first list item in a unordered list block
*oops no space, this is a normal paragraph now
* This is another list item"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = """* This is the first list item in a list block
 * just kidding its a paragraph
* xdd"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = """1. This is the first list item in a ordered list block
2. This is a list item
3. This is another list item"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "ordered_list")

        block = """1. This is the first list item in a ordered list block
3. jk
3. This is a paragraph now"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_markdown_to_html_node(self):
        node = markdown_to_html_node(
"""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        )

        self.assertEqual(
            node.to_html(),
            "<div><h1>This is a heading</h1><p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p><ul><li>This is the first list item in a list block</li><li>This is a list item</li><li>This is another list item</li></ul></div>"
        )

    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title(" # Hello"), "Hello")
        self.assertRaises(Exception, extract_title, "## Hello")
        self.assertRaises(Exception, extract_title, "#Hello")

        markdown = """# Hello

# Another heading"""
        self.assertEqual(extract_title(markdown), "Hello")

if __name__ == "__main__":
    unittest.main()