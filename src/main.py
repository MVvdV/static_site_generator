import os

# import re
import shutil

from convert import markdown_to_html_node

# from htmlnode import HTMLNode, LeafNode, ParentNode
from parse import extract_title


def clean_directory(directory):
    """Delete all contents of the directory if it exists."""
    if os.path.exists(directory):
        print(f"Cleaning directory: {directory}")
        shutil.rmtree(directory)
    os.mkdir(directory)
    print(f"Created clean directory: {directory}")


def copy_directory_recursive(source_dir, dest_dir):
    """Recursively copy all contents from source_dir to dest_dir."""
    if not os.path.exists(source_dir):
        raise ValueError(f"Source directory does not exist: {source_dir}")

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} -> {dest_path}")
        else:
            os.mkdir(dest_path)
            print(f"Created directory: {dest_path}")
            copy_directory_recursive(source_path, dest_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html_content = html_node.to_html()

    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)

    print(f"Page generated successfully: {dest_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """Recursively generate HTML pages from all markdown files in content directory."""
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)

        if os.path.isdir(content_path):
            # Recursively process subdirectories
            dest_subdir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(content_path, template_path, dest_subdir)
        elif item.endswith(".md"):
            # Calculate the destination path with .html extension
            dest_filename = item.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, dest_filename)

            # Generate the page
            generate_page(content_path, template_path, dest_path)


def main():
    static_dir = "static"
    public_dir = "public"

    clean_directory(public_dir)
    copy_directory_recursive(static_dir, public_dir)
    print("Copy complete!")

    generate_pages_recursive("content", "template.html", "public")
    print("Site generation complete!")


if __name__ == "__main__":
    main()
