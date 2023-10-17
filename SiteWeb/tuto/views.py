from .app import app, db
from flask import render_template, url_for, redirect, request
from .models import get_sample2, get_author, Author, get_books_by_author, User
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, PasswordField
from wtforms.validators import DataRequired
from hashlib import sha256
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def home():
    return render_template(
        "booksBS.html", 
        title="Mes livres",
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
@login_required
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

class AddAuthorForm(FlaskForm):
    name=StringField('Nom', validators=[DataRequired()])
    
@app.route("/ajoute-author/")
@login_required
def ajoute_author():
    f=AddAuthorForm(name=None)
    return render_template("ajoute-author.html", form=f)

@app.route("/save/ajout-author", methods=("POST",))
def save_ajoute_auteur():
    a=None
    f=AddAuthorForm()
    if f.validate_on_submit():
        print("oui")
        name=f.name.data
        o = Author(name=name)
        ida= o.id
        db.session.add(o)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("ajoute-author.html",form=f)
    
class LoginForm(FlaskForm):
    username=StringField('Username')
    password=PasswordField("Password")
    next=HiddenField()
    
    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m=sha256()
        m.update(self.password.data.encode())
        passwd= m.hexdigest()
        return user if passwd == user.password else None

@app.route("/login/", methods=("GET","POST",))
def login():
    f =LoginForm()
    if not f.is_submitted():
        f.next.data = request.args.get("next")
    elif f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            next = f.next.data or url_for("home")
            return redirect(next)
    return render_template(
        "login.html",form=f
    )
    
@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("home"))