import os
import shutil

from blocks import markdown_to_html_node, extract_title

def copy_files(source, target):

    if os.path.exists(target):
        shutil.rmtree(target)
    os.mkdir(target)

    source_dir = os.listdir(source)

    for file in source_dir:
        file_path = os.path.join(source, file)
        is_file = os.path.isfile(file_path)
        if is_file:
            shutil.copy(file_path, target)
        else:
            new_target = os.path.join(target, file)
            copy_files(file_path, new_target)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path)
    template_file = open(template_path)
    markdown = markdown_file.read()
    template = template_file.read()
    markdown_file.close()
    template_file.close()

    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)

    new_file = open(dest_path, "w")
    new_file.write(template)
    new_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    source_dir = os.listdir(dir_path_content)

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    
    for file in source_dir:
        file_path = os.path.join(dir_path_content, file)
        is_file = os.path.isfile(file_path)
        dest_path = os.path.join(dest_dir_path, file)
        if is_file:
            generate_page(file_path, template_path, f"{dest_dir_path}/index.html")
        else:
            generate_pages_recursive(file_path, template_path, dest_path)

def main():
    copy_files("./static", "./public")
    # generate_page("./content/index.md", "./template.html", "./public/index.html")
    generate_pages_recursive("./content", "./template.html", "./public")
    return

main()