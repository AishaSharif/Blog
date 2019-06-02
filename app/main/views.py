from flask import render_template, request, redirect, url_for, abort
from . import main
from .forms import ArticleForm
from ..models import Article, User, PhotoProfile
from flask_login import login_required, current_user
from .. import db, photos


@main.route('/post', methods=['GET', 'POST'])@login_required
def post(id):
    form = ArticleForm()
    article = get_article(id)

    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data

        new_post = Article(title=title, post=post, user=current_user)

        new_post.save_article()

        return redirect(url_for('.post', id=post.id))
    title = f'New Post'
    return render_template('new_post.html', title=title, form=form, post=post)
