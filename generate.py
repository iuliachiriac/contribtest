#!/usr/bin/python
import os
import logging
import logging.config
import jinja2
import json
import argparse
import re

log = logging.getLogger(__name__)
logging.config.fileConfig('etc/log.conf', disable_existing_loggers=False)


def beautify(text):
    """
    (str) -> str
    Replaces 3 or more consecutive newlines with 2 newlines.
    Removes multiple newlines at the end of the string.
    """
    text = re.sub('\n{3,}', '\n\n', text)
    text = re.sub('\n+$', '\n', text)
    return text


def list_files(folder_path):
    """
    (str) -> str
    Generator function, yields all .rst files' names from the given path.
    """
    try:
        for name in os.listdir(folder_path):
            base, ext = os.path.splitext(name)
            if ext != '.rst':
                continue
            yield os.path.join(folder_path, name)
    except OSError as ex:
        log.error('Exception occured in list_files: {0}'.format(ex))


def read_file(file_path):
    """
    (str) -> dict, str
    Reads file at given path, interprets its content, returning a metadata
    dictionary, that will be used at template render, and text content.
    """
    raw_metadata = ""
    content = ""
    try:
        with open(file_path, 'rb') as f:
            for line in f:
                if line.strip() == '---':
                    break
                raw_metadata += line
            for line in f:
                content += line
    except IOError as ex:
        log.error('Open file failed: {0}'.format(ex))
    try:
        metadata = json.loads(raw_metadata)
    except ValueError:
        log.error('No JSON object found in file {0}'.format(file_path))
        metadata = {}
    return metadata, content


def write_output(directory, name, html):
    """
    (str, str, str) -> None
    Writes output .html file using the path, filename and content received.
    Creates output directory if it does not exist.
    """
    if not os.path.isdir(directory):
        os.mkdir(directory)
    with open(os.path.join(directory, '.'.join((name, 'html'))), 'w') as f:
        f.write(beautify(html))


def generate_site(folder_path, output_path):
    """
    (str, str) -> None
    Initializes jinja environment, creates desired output from the files found
    in folder_path.
    """
    log.info("Generating site from {0}".format(folder_path))
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        os.path.join(folder_path, 'layout')))
    for file_path in list_files(folder_path):
        metadata, content = read_file(file_path)
        try:
            template_name = metadata['layout']
        except KeyError:
            log.error('Incorrect .rst file at: {0}'.format(file_path))
            continue
        try:
            template = jinja_env.get_template(template_name)
        except jinja2.exceptions.TemplateNotFound:
            log.error('Jinja template not found: {0}. Check {1} file.'.format(
                template_name, file_path))
            continue
        data = dict(metadata, content=content)
        html = template.render(**data)
        name = os.path.splitext(os.path.basename(file_path))[0]
        write_output(output_path, name, html)
        log.info("Writing {0} with template {1}".format(name, template_name))


def main():
    """
    () -> None
    Configures argument parser, generates site files.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("layout_path", help="relative path to the directory "
                        "containing .rst files with site content and jinja "
                        "templates that define the site structure")
    parser.add_argument("output_path", help="relative path to the output "
                        "directory")
    arguments = parser.parse_args()

    generate_site(arguments.layout_path, arguments.output_path)


if __name__ == '__main__':
    main()
