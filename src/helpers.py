def is_valid_article_id(string):
    return len(string) >= 4 and len(string) <= 7 and string.isdigit()
