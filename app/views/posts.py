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

            # TODO: refactor nested toc, this is yet the worst code i've wrotten, some of it is hard coded
            heading_tags = soup.find_all(re.compile('^h[1-6]$'))
            root_ul = soup.new_tag("ul")
            root_li = soup.new_tag("li")

            a_tag = soup.new_tag("a")
            a_tag.string = heading_tags[0].string
            a_tag["href"] = "#" + heading_tags[0]["id"]

            root_li_name = int(heading_tags[0].name[1:len(heading_tags[0].name)])
            root_li["class"] = str(root_li_name)
            root_li.append(a_tag)

            root_ul.append(root_li)

            nested_ul = root_ul

            init_ul = False
            for i in range(1, len(heading_tags)):
                heading_tag_number_now = int(heading_tags[i].name[1:len(heading_tags[i].name)])
                heading_tag_number_before = int(heading_tags[i - 1].name[1:len(heading_tags[i - 1].name)])
                is_root = heading_tag_number_now == root_li_name

                temp_a_tag = soup.new_tag("a")
                temp_a_tag.string = heading_tags[i].string
                temp_a_tag["href"] = "#" + heading_tags[i]["id"]

                temp_li_tag = soup.new_tag("li")
                temp_li_tag["class"] = str(heading_tag_number_now)
                temp_li_tag.append(temp_a_tag)

                temp_ul_tag = soup.new_tag("ul")

                if is_root:
                    root_li = temp_li_tag
                    root_ul.append(temp_li_tag)

                # nest to h1 or h2
                # lol 
                if not is_root:
                    li_to_be_nested = root_ul.find_all(class_=str(heading_tag_number_now - 1))

                    if heading_tag_number_before == root_li_name:
                        temp_ul_tag.append(temp_li_tag)
                        root_li.append(temp_ul_tag)
                        continue

                    if heading_tag_number_now != heading_tag_number_before:
                        init_ul = False

                    if not init_ul:
                        li_to_be_nested[-1].append(temp_ul_tag)
                        temp_ul_tag.append(temp_li_tag)
                        nested_ul = temp_ul_tag

                        init_ul = True
                    else:
                        nested_ul.append(temp_li_tag)

            # clean up temp classes
            for tag in root_ul.find_all():
                del tag["class"]

            c.insert_before(toc_tag)
            c.insert_before(root_ul)

            # delete the comment
            c.extract()

    post.html = str(soup)
    return render_template("posts/slug.html", post=post)
