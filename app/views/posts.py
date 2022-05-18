from . import blueprints
from flask import render_template, abort

from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path
import markdown

post_dir = Path(__file__).parent.parent / "_posts"

@blueprints["posts"].route("/posts/")
def posts():
    markdown_files = [i for i in post_dir.glob("**/*") if i.is_file() and i.suffix == ".md"]
    posts = []

    for file in markdown_files:
        with open(file) as f:
            content = f.read()
            md_converter = markdown.Markdown(extensions=["meta"])
            md_converter.convert(content)

            post = {
                "filename": file.stem,
                "metadata": md_converter.Meta
            }

            posts.append(post)
            posts.sort(key=lambda post: datetime.strptime(post["metadata"]["date"][0], "%d %b %Y"), reverse=True)

    return render_template("posts/index.html", posts=posts)

@blueprints["posts"].route("/posts/<slug>/")
def post(slug):
    file_path = post_dir / f"{slug}.md"

    try:
        with open(file_path) as f:
            content = f.read()
            md_converter = markdown.Markdown(extensions=["toc", "codehilite", "meta"])
            html = md_converter.convert(content)
            
            html_parser = BeautifulSoup(html, "html.parser")
            toc_tag = html_parser.find("div", class_="toc")

            # if there is "Table of contents"
            if toc_tag != None:
                # append "Table of contents" heading tag, remove div.toc wrapper
                h2 = html_parser.new_tag("h2")
                h2.string = "Table of contents"
                toc_tag.insert_before(h2)
                toc_tag.unwrap()

            html = str(html_parser)

        post = {
            "html": html,
            "metadata": md_converter.Meta
        }

        return render_template("posts/slug.html", post=post)
    except IOError:
        abort(404)
