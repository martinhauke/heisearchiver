from html.parser import HTMLParser


class HeiseParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag: ", tag)
