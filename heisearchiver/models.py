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
