import os
import re
import shutil

from htmlnode import HTMLNode, LeafNode, ParentNode
from parse import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


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


def main():
    static_dir = "static"
    public_dir = "public"

    clean_directory(public_dir)
    copy_directory_recursive(static_dir, public_dir)
    print("Copy complete!")


if __name__ == "__main__":
    main()
