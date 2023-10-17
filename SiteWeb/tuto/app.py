from flask import Flask
from flask_bootstrap import Bootstrap5
import os.path
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = "c08ccb64-82d0-4611-8db3-cae048269d91"
bootstrap = Bootstrap5(app)

def mkpath(p):
    return os.path.normpath(
        os.path.join(
        os.path.dirname(__file__),
        p))
    


app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'+mkpath('./myapp.db'))

db = SQLAlchemy(app)

