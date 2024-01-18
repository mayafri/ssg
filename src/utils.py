from datetime import datetime
import os
import re
import shutil

import markdown

def read_file(path: str, filename: str) -> str:
    content = ""
    with open(path + "/" + filename) as f:
        content = f.read()
    return content

def create_file(content: str, path: str, filename: str):
    with open(path + "/" + filename, "x") as f:
        f.write(content)

def rm_dir(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)

def copy_dir(src_path: str, dst_path: str):
    shutil.copytree(src_path, dst_path)

def extract_date_from_filename(filename: str) -> datetime:
    matches = re.search(r"^(\d\d\d\d)-(\d\d)-(\d\d)", filename)
    if not matches:
        raise Exception("Unable to extract YYYY-MM-DD date at the beginning of file name")
    year = int(matches.groups()[0])
    month = int(matches.groups()[1])
    day = int(matches.groups()[2])
    return datetime(year, month, day).date()

def extract_title(html_text: str) -> str:
    matches = re.search(r"<h1>(.+)<\/h1>", html_text, re.MULTILINE)
    if not matches:
        raise Exception("Unable to extract title")
    return matches.groups()[0]

def get_html_from_md(md_text: str) -> str:
    md = markdown.Markdown(extensions=['fenced_code', 'tables'])
    return md.convert(md_text)
