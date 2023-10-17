from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import get_sample2, get_author, Author, get_books_by_author
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms.validators import DataRequired


@app.route("/")
def home():
    return render_template(
        "booksBS.html", 
        title="My Books !",
        books=get_sample2())

@app.route("/one-author/<id>")
def one_author(id):
    a = get_author(id)
    book_author = get_books_by_author(id)
    return render_template(
        "one-author.html",author=a,books=book_author)

@app.route("/detail/<id>")
def detail(id):
    books = get_sample2()
    book = books[int(id)-1]
    return render_template(
        "detail.html",
        book=book)
    
class AuthorForm(FlaskForm):
    id=HiddenField('id')
    name=StringField('Nom', validators=[DataRequired()])
    
@app.route("/edit/author/<int:id>")
def edit_author(id):
    a = get_author(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template("edit-author.html",author=a, form=f)

@app.route("/save/author/", methods =("POST",))
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        ida = int(f.id.data)
        a = get_author(ida)
        a.name = f.name.data
        db.session.commit()
        return redirect( url_for("one_author", id=ida))
    a = get_author(int(f.ida.data))
    return render_template(
    "edit-author.html",
    author =a, form=f)