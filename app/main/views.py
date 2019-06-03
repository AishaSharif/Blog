from flask import render_template, request, redirect, url_for, abort
from . import main
from .forms import ArticleForm, CommentForm, UpdateProfile
from ..models import Article, User, PhotoProfile, Comment
from flask_login import login_required, current_user
from .. import db, photos


@main.route('/')
def index():
    post = Article.query.order_by(Article.posted.desc())
    # post = Article.get_article(id)
    title = f'Posts'
    return render_template('index.html', title=title, post=post)


@main.route('/post', methods=['GET', 'POST'])
@login_required
def post_form():
    form = ArticleForm()

    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data

        new_post = Article(title=title, post=post, user=current_user)

        new_post.save_article()

        # mail_message("New Post",
        #              "email/new_article", user.email, post=new_post)

        return redirect(url_for('main.index'))

    title = f'New Post'
    return render_template('new_post.html', title=title, form=form)


@main.route('/post/<int:id>')
def post(id):
    post = Article.get_article(id)
    comments = Comment.get_comment(id)
    title = f'Article'
    return render_template('post.html', title=title, post=post, comments=comments)


@main.route('/post/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def deletepost(id):
    post = Article.delete_article(id)
    title = 'Delete Post'
    return redirect(url_for('main.index'))


@main.route('/post/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    post = Article.get_article(id)

    if comment_form.validate_on_submit():
        new_comment = Comment(username=comment_form.username.data,
                              comment=comment_form.comment.data, post_id=id, user=current_user)
        new_comment.save_comment()
        return redirect(url_for('main.post', id=id))
        # return redirect(url_for('main.index'))

    title = f'Post Comment'
    comments = Comment.get_comment(id)
    return render_template('comment.html', title=title, comment_form=comment_form, post=post, comments=comments)


@main.route('/post/comments/<int:id>')
def post_comments(id):
    post = Article.get_article(id)
    comments = Comment.get_comment(id)
    title = f'Comments'
    render_template('post.html', comments=comments)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)
    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))
