import os

from conf import DATA_DIRNAME, OUTPUT_DIRNAME, POSTS_DIRNAME, SUBTITLE, TITLE
from post import Post
from utils import copy_dir, create_file, get_html_from_md, read_file, rm_dir

def generate_website():
    rm_dir(OUTPUT_DIRNAME)
    copy_dir(DATA_DIRNAME, OUTPUT_DIRNAME)
    posts = get_posts()
    create_file(generate_index_page(posts), OUTPUT_DIRNAME, "index.html")
    for post in posts:
        create_file(generate_post_page(post), OUTPUT_DIRNAME, post.link)
    www_local_path = os.getcwd() + "/" + OUTPUT_DIRNAME + "/index.html"
    print(f"file://{www_local_path}")

def get_posts() -> list[Post]:
    filenames = os.listdir(POSTS_DIRNAME)
    posts = []
    for filename in filenames:
        if filename == "index.md":
            continue
        if filename[0] in (".", "_"):
            print(f"[Info]\tIgnored {filename}")
            continue
        try:
            posts.append(Post(filename))
        except Exception as e:
            print(f"[Error]\t{filename}\t{e}")
    return posts

def generate_index_page(posts: list[Post]) -> str:
    html = generate_header()
    html += f"<h1>{TITLE}</h1>"
    html += f"<h2>{SUBTITLE}</h2>"
    html += get_index_post()
    html += generate_posts_table(posts)
    return html

def get_index_post() -> str:
    try:
        return get_html_from_md(read_file(POSTS_DIRNAME, "index.md"))
    except FileNotFoundError:
        print("[Info]\tCreate posts/index.md add content on the index page.")
        return ""

def generate_posts_table(posts: list[Post]) -> str:
    html = "<nav>"
    for post in posts:
        html += f"<p><span>{post.date_str}</span><a href='{post.link}'>{post.title}</a></p>"
    html += "</nav>"
    return html

def generate_post_page(post: Post) -> str:
    html = generate_header()
    html += "<nav><a href='index.html'>Retour</a></nav><hr>"
    html += post.html_content
    html += f"<p>{post.date_str}</p><hr><nav><a href='index.html'>Retour</a></nav>"
    return html

def generate_header() -> str:
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <link rel="stylesheet" media="screen" href="screen.css">
            <title>""" + TITLE + """</title>
        </head>
        <body>
    """

generate_website()
