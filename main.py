from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/get-it/done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'dillybar'



@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@app.route('/add-post')
def add_post():
    return render_template('add-post.html')

@app.route('/blog-listings')
def blog_listings():
    return render_template('blog-listings.html')


if __name__ == '__main__':
    app.run()