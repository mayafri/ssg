import os

from conf import ALLOW_INDEX, AUTHOR, BASE_URL, DATA_DIRNAME, DESCRIPTION, LANG, OUTPUT_DIRNAME, POSTS_DIRNAME, TITLE
from post import Post
from utils import copy_dir, create_file, get_html_from_md, read_file, rm_dir

def generate_website():
    rm_dir(OUTPUT_DIRNAME)
    copy_dir(DATA_DIRNAME, OUTPUT_DIRNAME)
    posts = get_posts()
    create_file(generate_index_page(posts), OUTPUT_DIRNAME, "index.html")
    create_file(generate_atom_page(posts), OUTPUT_DIRNAME, "atom.xml")
    for post in posts:
        create_file(generate_post_page(post), OUTPUT_DIRNAME, post.link)
    www_local_path = os.getcwd() + "/" + OUTPUT_DIRNAME + "/index.html"
    print(f"file://{www_local_path}")

def get_posts() -> list[Post]:
    filenames = os.listdir(POSTS_DIRNAME)
    filenames.sort(reverse=True)
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
    html = "<table>"
    html += "<tr><th>Date</th><th>Post</th></tr>"
    for post in posts:
        html += "<tr>"
        html += f"<td>{post.date_str}</td>"
        html += f"<td><a href='{post.link}'>{post.title}</a></td>"
        html += "</tr>"
    html += "</table>"
    return html

def generate_post_page(post: Post) -> str:
    html = generate_header()
    html += post.html_content
    html += f"<p>{post.date_str}</p><nav><p><a href='index.html'>Retour</a></p></nav>"
    return html

def generate_header() -> str:
    noindex_tag = '<meta name="robots" content="noindex">' if not ALLOW_INDEX else ''

    return f"""
    <!DOCTYPE html lang="{LANG}">
    <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width,initial-scale=1">
            <link rel="stylesheet" media="screen" href="screen.css">
            <link rel="alternate" type="application/atom+xml" href="{BASE_URL}/atom.xml">
            {noindex_tag}
            <title>""" + TITLE + """</title>
        </head>
        <body>
    """

def generate_atom_page(posts: list[Post]) -> str:
    items = []
    for post in posts:
        items.append(
            f"""
            <entry xml:lang="{LANG}">
                <id>{post.url}</id>
                <link href="{post.url}" />
                <title type="html"><![CDATA[{post.title}]]></title>
                <updated>{post.date_str}T00:00:00+00:00</updated>
                <content type="html"><![CDATA[
                    {post.html_content}
                ]]></content>
            </entry>
            """
        )
        
    return f"""<?xml version="1.0" encoding="utf-8" standalone="yes" ?>
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="fr">
    <id>{BASE_URL}</id>
    <title><![CDATA[{TITLE}]]></title>
    <subtitle><![CDATA[{DESCRIPTION}]]></subtitle>
    <link href="{BASE_URL}/atom.xml" rel="self" />
    <link href="{BASE_URL}" />
    <updated>{posts[0].date_str}T00:00:00+00:00</updated>
    <author>
        <name><![CDATA[{AUTHOR}]]></name>
    </author>
    {"".join(items)}
</feed>
    """

generate_website()
