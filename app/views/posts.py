from . import blueprints
from .. import posts as _posts
from flask import render_template

from bs4 import BeautifulSoup, Comment
import re

@blueprints["posts"].route("/posts/")
def posts():
    return render_template("posts/index.html", posts=_posts)

@blueprints["posts"].route("/posts/<slug>/")
def post(slug):
    post = _posts.get_or_404(slug)

    soup = BeautifulSoup(post.html, "html.parser")

    # TODO: messy code, needs refacoring
    # generate & append heading tag
    for heading_tag in soup.find_all(re.compile('^h[1-6]$')):
        # replace all non-alphanumeric characters
        heading_tag_id = re.sub(r'[\W]+', '-', heading_tag.string).lower()

        while heading_tag_id[-1] == "-":
                heading_tag_id = heading_tag_id[0:len(heading_tag_id) - 1]

        heading_tag['id'] = heading_tag_id

    # TODO: match only the "table of content string", thus we don't need to check if c.lower == "table.."
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        # too dumb
        if (str(c).strip().lower() == "table of content" or str(c).strip().lower() == "table of contents"):
            # toc stands for table of content
            toc_tag = soup.new_tag("h2")
            toc_tag.string = str(c).strip()

            ul_tag = soup.new_tag("ul")

            for heading_tag in soup.find_all(re.compile('^h[1-6]$')):
                li_tag = soup.new_tag("li")

                a_tag = soup.new_tag("a")
                a_tag.string = heading_tag.string
                a_tag["href"] = "#" + heading_tag["id"]

                li_tag.append(a_tag)
                ul_tag.append(li_tag)

            c.insert_before(toc_tag)
            c.insert_before(ul_tag)

            # delete the comment
            c.extract()

    post.html = str(soup)
    return render_template("posts/slug.html", post=post)
