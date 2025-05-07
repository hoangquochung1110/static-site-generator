import pathlib
from typing import Iterator, Sequence

import frontmatter
import jinja2
import markdown
import markdown.extensions.fenced_code
import pymdownx.magiclink

import highlighting
import settings
import witchhazel

ROOT_URL = "https://hoangquochung1110.github.io/static-site-generator"

# Jinja will look up templates in `templates` folder
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates")
)

markdown_ = markdown.Markdown(
    extensions=[
        "toc",
        "admonition",  # Bring your own styles
        "tables",
        "abbr",
        "attr_list",
        "footnotes",
        "pymdownx.smartsymbols",
        markdown.extensions.fenced_code.FencedCodeExtension(lang_prefix="language-"),
        pymdownx.magiclink.MagiclinkExtension(hide_protocol=False,),
    ]
)

def get_sources(path: str = "./srcs") -> Iterator[pathlib.Path]:
    """Get all markdown files."""
    srcs_path = pathlib.Path(path)
    return srcs_path.glob('*.md')

def parse_source(source: pathlib.Path) -> frontmatter.Post:
    """Can get content of the file by post.content"""
    post = frontmatter.load(str(source))
    return post

def fixup_styles(content: str) -> str:
    content = content.replace('<table>', '<table class="table">')
    return content

def render_markdown(content: str) -> str:
    """Turn markdown content into html-formatted string."""
    markdown_.reset()
    content = markdown_.convert(content)
    content = highlighting.highlight(content)
    content = fixup_styles(content)
    return content

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

def write_post(post: frontmatter.Post, content: str):
    if post.get("legacy_url"):
        path = pathlib.Path("./docs/{}/index.html".format(post["stem"]))
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
        if post.get("til", False):
            path = pathlib.Path("./docs/til/{}.html".format(post["stem"]))
        else:
            path = pathlib.Path("./docs/{}.html".format(post["stem"]))

    template = jinja_env.get_template("post.html")
    try:
        default_value = settings.TAGS_MAPPING["default"]
        background_map = [
            settings.TAGS_MAPPING.get(tag, default_value)
            for tag in post["tags"]
        ]
        post["background_color"] = background_map
    except KeyError:
        # some posts don't provide tags
        pass
    rendered = template.render(post=post, content=content)
    path.write_text(rendered)


def write_tils() -> Sequence[frontmatter.Post]:
    """Get TIL articles and convert md into html."""
    posts = []
    sources = get_sources("./srcs/til")

    for source in sources:
        post = parse_source(source)
        content = render_markdown(post.content)
        post["stem"] = source.stem
        write_til(post, content)
        posts.append(post)

    return posts

def write_til(post: frontmatter.Post, content: str):
    """Compose TIL articles as html."""
    if post.get("legacy_url"):
        path = pathlib.Path("./docs/{}/index.html".format(post["stem"]))
        path.parent.mkdir(parents=True, exist_ok=True)
    else:
            path = pathlib.Path("./docs/til/{}.html".format(post["stem"]))

    template = jinja_env.get_template("post.html")
    rendered = template.render(post=post, content=content)
    path.write_text(rendered)

def write_pygments_style_sheet():
    css = highlighting.get_style_css(witchhazel.WitchHazelStyle)
    pathlib.Path("./docs/static/pygments.css").write_text(css)
    pathlib.Path("./docs/til/static/pygments.css").write_text(css)

def write_index(posts: Sequence[frontmatter.Post]):
    """Render the index page."""
    posts = sorted([post for post in posts if "date" in post], key=lambda post: post["date"], reverse=True)
    path = pathlib.Path("./docs/index.html")
    template = jinja_env.get_template("index.html")
    rendered = template.render(posts=posts)
    path.write_text(rendered)

def write_til_index(posts: Sequence[frontmatter.Post]):
    """Render the til page."""
    posts = sorted([post for post in posts if "date" in post], key=lambda post: post["date"], reverse=True)
    path = pathlib.Path("./docs/til/index.html")
    template = jinja_env.get_template("til.html")
    rendered = template.render(posts=posts)
    path.write_text(rendered)

def write_rss(posts: Sequence[frontmatter.Post]):
    posts = sorted([post for post in posts if "date" in post], key=lambda post: post["date"], reverse=True)
    path = pathlib.Path("./docs/feed.xml")
    template = jinja_env.get_template("rss.xml")
    rendered = template.render(posts=posts, root=ROOT_URL)
    path.write_text(rendered)


def main():
    write_pygments_style_sheet()
    articles = write_posts()
    write_index(articles)
    tils = write_tils()
    write_til_index(tils)
    write_rss(articles)

if __name__ == '__main__':
    main()
