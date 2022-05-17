from . import blueprints
from flask import render_template

from bs4 import BeautifulSoup
from pathlib import Path
import markdown

base_path = Path(__file__).parent

@blueprints["posts"].route("/posts/")
def posts():
    dir =  (base_path / "../_posts").resolve()
    files = [x for x in dir.glob("**/*") if x.is_file()]
    posts = []

    for file in files:
        with open(file) as f:
            content = f.read()
            md_converter = markdown.Markdown(extensions=["meta"])
            md_converter.convert(content)

            post = {
                "filename": file.stem,
                "metadata": md_converter.Meta
            }

            posts.append(post)

    return render_template("posts/index.html", posts=posts)

@blueprints["posts"].route("/posts/<slug>/")
def post(slug):
    file_path = (base_path / f"../_posts/{slug}.md").resolve()

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
