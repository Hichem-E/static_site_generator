from helpers import extract_title, markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(f"Generating path from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        from_data = file.read()

    with open(template_path, "r") as file:
        temp_data = file.read()

    htmlnode = markdown_to_html_node(from_data)
    print(htmlnode)
    # html_str = htmlnode.to_html()
    # print(html_str)

    title = extract_title(from_data)

    titled_html = temp_data.replace("{{ Title }}", title)

    final_html = titled_html.replace(
        "{{ Content }}", "Boom shaka laka i messed up my algorithm kill me"
    )

    f = open(dest_path, "w")
    f.write(final_html)
    f.close()
