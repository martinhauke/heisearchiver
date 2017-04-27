def is_valid_article_id(string):
    """Returns true, if the article id appears to be valid"""
    return len(string) >= 4 and len(string) <= 7 and string.isdigit()
