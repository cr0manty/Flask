from flask import Blueprint, render_template, redirect, url_for, request
from models import Post, Tag
from .forms import PostForm
from app import db
from flask_security import login_required

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=['POST', 'GET'])
@login_required
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title:
            try:
                post = Post(title=title, body=body)
                db.session.add(post)
                db.session.commit()
            except:
                print('Smth went wrong')

        return redirect(url_for('posts.index'))

    form = PostForm()
    return render_template('posts/create_post.html', form=form)


@posts.route('/<slug>/delete', methods=['POST', 'GET'])
@login_required
def delete(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()

    if request.method == 'GET':
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('posts.index'))

    return redirect(url_for('posts.show_post', slug=post.slug))


@posts.route('/<slug>/edit', methods=['POST', 'GET'])
@login_required
def edit(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()

    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.show_post', slug=post.slug))

    form = PostForm(obj=post)
    return render_template('posts/edit.html', post=post, form=form)


@posts.route('/')
def index():
    p = request.args.get('p')

    page = request.args.get('page')
    page = int(page) if page and page.isdigit() else 1

    if p:
        all_posts = Post.query.filter(Post.title.contains(p) | Post.body.contains(p))
    else:
        all_posts = Post.query.order_by(Post.created.desc())

    pages = all_posts.paginate(page=page, per_page=5)
    return render_template('posts/index.html', posts=all_posts, pages=pages)


@posts.route('/<slug>')
def show_post(slug):
    my_post = Post.query.filter(Post.slug == slug).first_or_404()
    tags = my_post.tags
    return render_template('posts/show_post.html', post=my_post, tags=tags)


@posts.route('/tag/<slug>')
def tag_show(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    all_post = tag.posts.all()
    return render_template('posts/tag.html', tag=tag, posts=all_post)
