from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'dillybar'

class Blog(db.Model):
    '''User text input is taken in to create new blog posts'''

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(12000))

    def __init__(self, title, body):
        self.title = title
        self.body = body



@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        new_post = Blog(blog_title, blog_body)
        db.session.add(new_post)
        db.session.commit()

    return render_template('index.html', title='Blog Home Page')


@app.route('/newpost')
def add_post():
    return render_template('newpost.html')

@app.route('/blog')
def blog_listings():

    posts = Blog.query.all()

    return render_template('blog.html', posts=posts)


if __name__ == '__main__':
    app.run()