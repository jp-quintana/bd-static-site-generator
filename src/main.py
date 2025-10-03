import os
from markdown_blocks import extract_title
from copystatic import generate_page

dir_path_static = "static"
dir_path_public = "public"
dir_path_content = "content"


def main():
    markdown_file_path = os.path.join(dir_path_content, "index.md")
    index_file_path = os.path.join(dir_path_public, "index.html")
    template_file_path = os.path.join("template.html")

    generate_page(markdown_file_path, template_file_path, index_file_path)

    try:
        with open(markdown_file_path, "r", encoding="utf-8") as f:
            markdown_content = f.read()

        print(extract_title(markdown_content))

    except FileNotFoundError:
        print(f"Error: The file {markdown_file_path} was not found.")
        print(
            "Please make sure you have a 'content' directory with an 'index.md' file inside it."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


main()
