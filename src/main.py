from markdown_blocks import markdown_to_html_node


def main():
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

    test = markdown_to_html_node(md)

    print(test)


main()
