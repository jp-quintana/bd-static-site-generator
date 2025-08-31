from textnode import TextNode, TextType


class HTMLNode:
    def __init__(
        self, tag=None, value=None, children: list["HTMLNode"] = None, props=None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        str = ""
        if self.props:
            for key in self.props.keys():
                str += f' {key}="{self.props[key]}"'
        return str


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All parent nodes must have children")

        child_content = ""
        for child in self.children:
            child_content += child.to_html()

        props = self.props_to_html()
        return f"<{self.tag}{props}>{child_content}</{self.tag}>"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value

        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"


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
