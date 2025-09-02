from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


def main():
    # text_node = TextNode(
    #     "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    # )

    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    split_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(split_nodes)

    # print(text_node.__repr__())


main()
