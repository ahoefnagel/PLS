import json
class Book:
    def __init__(self, author: str, country, image_link, language, link, pages, title, year):
        self.author = author
        self.country = country
        self.image_link = image_link
        self.language = language
        self.link = link
        self.pages = pages
        self.title = title
        self.year = year

    def __str__(self):
        return self.title

    def to_dict(self):
        return json.dumps(self.__dict__, indent=2) + ','

    def to_csv(self):
        return ','.join([str(f) for f in self.__dict__.values()]) + '\n'
