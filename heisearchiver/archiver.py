import os
from heisearchiver.config import ARCHIVE_PATH
from heisearchiver.parser import Parser


def write_article_to_file(content, path):
    """Writes an article to local file"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(content.encode("utf-8"))
        print("article saved to ..." + f.name[-15:])


def save_article(article_id, content, path=None):
    """Saves an article locally"""
    # TODO add option for saving to database instead
    parser = Parser(content)
    if path is None:
        path = ARCHIVE_PATH
    path += str(parser.extract_year()) + '/' + article_id
    print(path)
    write_article_to_file(content=parser.prettify(), path=path)
