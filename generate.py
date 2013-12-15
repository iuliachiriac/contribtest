#!/usr/bin/python
import os
import logging
import jinja2
import json
import argparse

log = logging.getLogger(__name__)


def list_files(folder_path):
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name)


def read_file(file_path):
    with open(file_path, 'rb') as f:
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line
        content = ""
        for line in f:
            content += line
    return json.loads(raw_metadata), content


def write_output(directory, name, html):
    if not os.path.isdir(directory):
        os.mkdir(directory)
    with open(os.path.join(directory, name + '.html'), 'w') as f:
        f.write(html)


def generate_site(folder_path, output_path):
    log.info("Generating site from %r", folder_path)
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        os.path.join(folder_path, 'layout')))
    for file_path in list_files(folder_path):
        metadata, content = read_file(file_path)
        template_name = metadata['layout']
        template = jinja_env.get_template(template_name)
        data = dict(metadata, content=content)
        html = template.render(**data)
        name = os.path.splitext(os.path.basename(file_path))[0]
        write_output(output_path, name, html)
        log.info("Writing %r with template %r", name, template_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("layout_path", help="relative path to the directory "
                        "containing .rst files with site content and jinja "
                        "templates that define the site structure")
    parser.add_argument("output_path", help="relative path to the output "
                        "directory")
    arguments = parser.parse_args()

    generate_site(arguments.layout_path, arguments.output_path)


if __name__ == '__main__':
    logging.basicConfig()
    main()
