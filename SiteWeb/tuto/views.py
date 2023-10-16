from .app import app
from flask import render_template
from .models import get_sample2


@app.route("/")
def home():
    return render_template(
        "booksBS.html", 
        title="My Books !",
        books=get_sample2())


@app.route("/detail/<id>")
def detail(id):
    books = get_sample2()
    book = books[int(id)]
    return render_template(
        "detail.html",
        book=book)