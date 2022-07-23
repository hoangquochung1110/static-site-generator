import pathlib
from typing import Iterator, Sequence

import markdown
import markdown.extensions.fenced_code
import pymdownx.magiclink
import frontmatter
import jinja2



# Jinja will look up templates in `templates` folder
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates")
)

markdown_ = markdown.Markdown(
    extensions=[
        "toc",
        "admonition",
        "tables",
        "abbr",
        "attr_list",
        "footnotes",
        "pymdownx.smartsymbols",
        markdown.extensions.fenced_code.FencedCodeExtension(lang_prefix="language-"),
        pymdownx.magiclink.MagiclinkExtension(hide_protocol=False,),
    ]
)

def get_sources() -> Iterator[pathlib.Path]:
    """Get all markdown files."""
    return pathlib.Path('.').glob('srcs/*.md')

def parse_source(source: pathlib.Path) -> frontmatter.Post:
    """Can get content of the file by post.content"""
    post = frontmatter.load(str(source))
    breakpoint()
    return post

def render_markdown(content: str) -> str:
    """Turn markdown content into html-formatted string."""
    markdown_.reset()
    content = markdown_.convert(content)
    return content

def write_post(post: frontmatter.Post, content: str):
    if post.get("legacy_url"):
        path = pathlib.Path("./docs/{}/index.html".format(post["stem"]))
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        path = pathlib.Path("./docs/{}.html".format(post["stem"]))
    
    template = jinja_env.get_template("post.html")
    rendered = template.render(post=post, content=content)
    path.write_text(rendered)

def write_posts() -> Sequence[frontmatter.Post]:
    posts = []
    sources = get_sources()

    for source in sources:
        post = parse_source(source)
        content = render_markdown(post.content)
        post["stem"] = source.stem
        write_post(post, content)

        posts.append(post)

    return posts

def write_index(post: Sequence[frontmatter.Post]):
    """Render the index page."""
    posts = sorted(posts, key=lambda post: post["date"], reverse=True)
    path = pathlib.Path("./docs/index.html")
    template = jinja_env.get_template("index.html")
    rendered = template.render(posts=posts)
    path.write_text(rendered)

def write_rss(posts: Sequence[frontmatter.Post]):
    posts = sorted(posts, key=lambda post: post["date"], reverse=True)
    path = pathlib.Path("./docs/feed.xml")
    template = jinja_env.get_template("rss.xml")
    rendered = template.render(posts=posts, root="")
    path.write_text(rendered)

def main():
    posts = write_posts()
    write_index(posts)
    write_rss(posts)

if __name__ == '__main__':
    main()
