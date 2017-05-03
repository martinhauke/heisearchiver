# Database models for the archive
from sqlalchemy.ext.declarative import declarative_base
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
article_image = Table('article_image', Base.metadata,
                      Column('article_id', ForeignKey('article.id'),
                             primary_key=True),
                      Column('image_id', ForeignKey('image.id'),
                             primary_key=True),
                      Column('alt', String, nullable=True),
                      Column('caption', String, nullable=True))

# association table
article_link = Table('article_link', Base.metadata,
                     Column('article_id', ForeignKey('article.id'),
                            primary_key=True),
                     Column('link_id', ForeignKey('link.id'),
                            primary_key=True),
                     Column('rel', String, nullable=True),
                     Column('text', String),
                     Column('target', String))

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


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)

    name = Column(String(255))
    abbreviation = Column(String(10))


class Topic(Base):
    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)

    name = Column(String(64))


class Keyword(Base):
    __tablename__ = 'keyword'

    id = Column(Integer, primary_key=True)

    name = Column(String(64))


class Source(Base):
    __tablename__ = 'source'

    id = Column(Integer, primary_key=True)

    name = Column(String(64))


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)

    src = Column(String)


class Link(Base):
    __tablename__ = 'link'

    id = Column(Integer, primary_key=True)

    url = Column(String)


class Subheading(Base):
    __tablename__ = 'subheading'

    id = Column(Integer, primary_key=True)

    article_id = Column(ForeignKey('article.id'))
    text = Column(String)


class Paragraph(Base):
    __tablename__ = 'paragraph'

    id = Column(Integer, primary_key=True)

    article_id = Column(ForeignKey('article.id'))
    text_html = Column(String)
    text_plain = Column(String)
