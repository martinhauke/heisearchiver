# Database models for the archive
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime

Base = declarative_base()

# association table article_author
article_author = Table('article_author', Base.metadata,
                       Column('article_id', ForeignKey('article.id'),
                              primary_key=True),
                       Column('author_id', ForeignKey('author.id'),
                              primary_key=True))

# association table
article_keyword = Table('article_keyword', Base.metadata,
                        Column('article_id', ForeignKey('article.id'),
                               primary_key=True),
                        Column('keyword_id', ForeignKey('keyword.id'),
                               primary_key=True))

# association table
article_topic = Table('article_topic', Base.metadata,
                      Column('article_id', ForeignKey('article.id'),
                             primary_key=True),
                      Column('topic_id', ForeignKey('topic.id'),
                             primary_key=True))

# association table
article_source = Table('article_source', Base.metadata,
                       Column('article_id', ForeignKey('article.id'),
                              primary_key=True),
                       Column('source_id', ForeignKey('source.id'),
                              primary_key=True))

# association table
image_source = Table('image_source', Base.metadata,
                     Column('image_id', ForeignKey('image.id'),
                            primary_key=True),
                     Column('source_id', ForeignKey('source.id'),
                            primary_key=True))


# association table
class Article_Image(Base):
    __tablename__ = 'article_image'
    article_id = Column(Integer, ForeignKey('article.id'), primary_key=True)
    image_id = Column(Integer, ForeignKey('image.id'), primary_key=True)
    alt = Column(String, nullable=True)
    caption = Column(String, nullable=True)

    article = relationship("Article",
                           backref=backref("article_image",
                                           cascade="all, delete-orphan"))
    image = relationship("Image",
                         backref=backref('article_image',
                                         cascade="all, delete-orphan"))

    def __init__(self, article=None, image=None, alt=None, caption=None):
        self.article = article
        self.image = image
        self.alt = alt
        self.caption = caption

    def __repr__(self):
        return '<Article_Image {}>'.format(self.article.id + " "
                                           + self.image.src)


# association table
class Article_Link(Base):
    __tablename__ = 'article_link'
    article_id = Column(Integer, ForeignKey('article.id'), primary_key=True)
    link_id = Column(Integer, ForeignKey('link.id'), primary_key=True)
    rel = Column(String, nullable=True),
    text = Column(String),
    target = Column(String)

    article = relationship("Article",
                           backref=backref("article_link",
                                           cascade="all, delete-orphan"))
    link = relationship("Link", backref=backref("article_link",
                                                cascade="all, delete-orphan"))

    def __init__(self, article=None, link=None, text=None, rel=None):
        self.article = article
        self.link = link
        self.text = text
        self.rel = rel

    def __repr__(self):
        return '<Article_Link {}>'.format(self.article.id + " "
                                          + self.link.href)


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)

    meta_date = Column(DateTime)
    meta_description = Column(String)
    meta_dc_description = Column(String)
    meta_fulltitle = Column(String)
    meta_dc_title = Column(String)
    og_title = Column(String)
    og_locale = Column(String(32))
    og_type = Column(String)
    og_url = Column(String)
    og_description = Column(String)
    article_heading = Column(String)
    article_date = Column(DateTime)
    article_content_html = Column(String)
    article_content_plain = Column(String)
    article_teaser = Column(String)
    number_of_comments = Column(Integer)

    authors = relationship("Author", secondary=article_author,
                           backref=backref('article',
                                           cascade="all, delete-orphans"))
    keywords = relationship("Keyword", secondary=article_keyword,
                            backref=backref('article',
                                            cascade="all, delete-orphans"))
    topics = relationship("Topic", secondary=article_topic,
                          backref=backref('article',
                                          cascade="all, delete-orphans"))
    sources = relationship("Source", secondary=article_source,
                           backref=backref('article',
                                           cascade="all, delete-orphans"))

    images = relationship("Article_Image", secondary='article_image',
                          viewonly=True)
    links = relationship("Article_Link", secondary='article_link',
                         viewonly=True)

    subheadings = relationship("Subheading", backref='article')
    paragraphs = relationship("Paragraph", backref='article')

    def __init__(self, article_id, meta_date=None, meta_description=None,
                 meta_fulltitle=None):
        self.id = article_id
        self.meta_date = meta_date
        self.meta_description = meta_description
        self.meta_fulltitle = meta_fulltitle

    def __repr__(self):
        return '<Article {}>'.format(self.id)


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    abbreviation = Column(String(10))

    def __init__(self, name, abbreviation=None):
        self.name = name
        self.abbreviation = abbreviation

    def __repr__(self):
        return '<Author {}>'.format(self.name + " (" + self.abbriviation
                                    + " )")


class Topic(Base):
    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)

    name = Column(String(64))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Topic {}>'.format(self.name)


class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, primary_key=True)

    name = Column(String(64))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Keyword {}>'.format(self.name)


class Source(Base):
    __tablename__ = 'source'

    id = Column(Integer, primary_key=True)

    name = Column(String(64))

    images = relationship("Image", secondary=image_source,
                          backref=backref('source',
                                          cascade="all, delete-orphan"))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Source {}>'.format(self.name)


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)

    src = Column(String)

    articles = relationship("Article", secondary='article_image',
                            viewonly=True)

    sources = relationship("Source", secondary=image_source,
                           backref=backref('image',
                                           cascade="all, delete-orphan"))

    def __init__(self, src):
        self.src = src

    def __repr__(self):
        return '<Image {}>'.format(self.src)


class Link(Base):
    __tablename__ = 'link'

    id = Column(Integer, primary_key=True)

    url = Column(String)

    articles = relationship("Article", secondary="article_link", viewonly=True)

    def __init__(self, url):
        self.url = url
        self.articles = []

    def __repr__(self):
        return '<Link {}>'.format(self.url)


class Subheading(Base):
    __tablename__ = 'subheading'

    id = Column(Integer, primary_key=True)

    article_id = Column(ForeignKey('article.id'))
    text = Column(String)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<Subheading {}>'.format(self.text)


class Paragraph(Base):
    __tablename__ = 'paragraph'

    id = Column(Integer, primary_key=True)

    article_id = Column(ForeignKey('article.id'))
    text_html = Column(String)
    text_plain = Column(String)

    def __init__(self, text_html, text_plain):
        self.text_html = text_html
        self.text_plain = text_plain

    def __repr__(self):
        return '<Paragraph {}>'.format(self.id)
