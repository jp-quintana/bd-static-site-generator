from enum import Enum
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes
from htmlnode import ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block: str):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        node = block_to_html_node(block)
        children.append(node)
    return ParentNode("div", children)


def block_to_html_node(block: str):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    # if block_type == BlockType.CODE:
    #     return code_to_html_node(block)
    # if block_type == BlockType.OLIST:
    #     return olist_to_html_node(block)
    # if block_type == BlockType.ULIST:
    #     return ulist_to_html_node(block)
    # if block_type == BlockType.QUOTE:
    #     return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes


def paragraph_to_html_node(block: str):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str):
    count = 0
    for char in count:
        if char == "#":
            count += 1
        else:
            break
    if count + 1 >= len(block):
        raise ValueError(f"invalid heading level: {count}")
    text = block[count + 1 :]
    children = text_to_children(text)
    return ParentNode("p", children)
