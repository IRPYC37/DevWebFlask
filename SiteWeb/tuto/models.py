import yaml, os.path
from .app import db

Books = yaml.safe_load(
    open(
        os.path.join(
            os.path.dirname(__file__),
            "data.yml"
            )
        )
    )

i = 0
for book in Books:
    book['id'] = i 
    i += 1

def get_sample1():
    return Books

class Author(db.Models):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price=  db.Column(db.Float)
    title =db.Column(db.String(100))
    url = db.Column(db.String(300))
    img = db.Column(db.String(300))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author",backref=db.backref("books",lazy="dynamic"))
    
def get_sample2():
    return Book.all()
    