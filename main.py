from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import re
from datetime import datetime

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
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date



@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['body']

        if not blog_body or not blog_title:
            if not blog_title:
                flash('Please enter a title', 'error')
            if not blog_body:
                flash('Please enter content for your post', 'error')
            return render_template('newpost.html', title="New Blog Post")


        new_post = Blog(blog_title, blog_body)
        db.session.add(new_post)
        db.session.commit()
        return render_template('blogpage.html', post=new_post)


    return render_template('index.html', title='Blog Home Page')


@app.route('/newpost')
def add_post():
    return render_template('newpost.html')

@app.route('/blog')
def blog_listings():

    posts = Blog.query.order_by(Blog.pub_date.desc()).all()

    if request.args.get('id'):
        post_id = request.args.get('id')
        post = Blog.query.filter_by(id=post_id).first()
        return render_template('blogpage.html', post=post)

    return render_template('blog.html', posts=posts)


if __name__ == '__main__':
    app.run()