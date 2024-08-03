from datetime import datetime
from email.utils import formatdate
from urllib.parse import quote
from conf import BASE_URL, POSTS_DIRNAME

from utils import extract_date_from_filename, extract_title, get_html_from_md, read_file


class Post:
    filename: str
    link: str
    md_content: str
    html_content: str
    title: str
    date: datetime

    def __init__(self, filename: str):
        self.filename = filename
        self.link = filename.removesuffix(".md") + ".html"
        self.md_content = read_file(POSTS_DIRNAME, filename)
        self.html_content = get_html_from_md(self.md_content)
        self.title = extract_title(self.html_content)
        self.date = extract_date_from_filename(self.filename)

    @property
    def date_str(self) -> str:
        return self.date.isoformat()[:10]
    
    @property
    def url(self) -> str:
        return BASE_URL + "/" + quote(self.link)

    def __repr__(self) -> str:
        return self.date_str + " - " + self.title