from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode"):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: "TextNode"):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text, tag=None)
        case TextType.BOLD:
            return LeafNode(value=text_node.text, tag="b")
        case TextType.ITALIC:
            return LeafNode(value=text_node.text, tag="i")
        case TextType.CODE:
            return LeafNode(value=text_node.text, tag="code")
        case TextType.LINK:
            if not text_node.url:
                raise ValueError("Url is missing")

            return LeafNode(
                value=text_node.text,
                props={
                    "href": text_node.url,
                },
                tag="a",
            )
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError("Image url is missing")

            return LeafNode(
                value="",
                props={"src": text_node.url, "alt": text_node.text},
                tag="img",
            )
        case _:
            raise ValueError("Invalid value")
