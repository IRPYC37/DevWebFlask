import yaml, os.path
from .app import db, login_manager
from flask_login import UserMixin

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

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    def __repr__(self):
        return "<Author (%d) %s>" % (self.id,self.name)
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price=  db.Column(db.Float)
    title =db.Column(db.String(100))
    url = db.Column(db.String(300))
    img = db.Column(db.String(300))
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author",backref=db.backref("books",lazy="dynamic"))
    
    def __repr__(self):
        return "<Book (%d) %s>" % (self.id, self.title)
def get_sample2():
    return Book.query.all()

def get_author(id):
    return Author.query.get(id)

def get_books_by_author(id):
    ida=id
    return Author.query.filter(Author.id==id).one().books.all()
    
class User(db.Model,UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    
    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)