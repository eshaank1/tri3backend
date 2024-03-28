from sqlalchemy import Column, Integer, String
from __init__ import db

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)

    def __init__(self, title, author, link):
        self.title = title
        self.author = author
        self.link = link

    @staticmethod
    def create(title, author, link):
        try:
            article = Article(title=title, author=author, link=link)
            db.session.add(article)
            db.session.commit()
            return article
        except Exception as e:
            db.session.rollback()
            print(f"Error creating article: {e}")
            return None

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "link": self.link
        }

# Builds working data for testing


def init_articles():
    articles_data = [
        {'title': '12 Strategies to Writing the Perfect College Essay',
         'author': 'Pamela Reynolds',
         'link': 'https://shorturl.at/rszH7'},
        {'title': 'How to Write a College Essay: The Ultimate Guide',
         'author': 'College Essay Guy',
         'link': 'https://shorturl.at/doIQ2'},
        {'title': 'How to Write a Successful Common App Activites List',
         'author': 'College Essay Guy',
         'link': 'https://shorturl.at/asyLT'},
    ]
    for data in articles_data:
        Article.create(**data)


if __name__ == "__main__":
    # Create the database tables based on the defined models
    db.create_all()
    # Initialize articles
    init_articles()
