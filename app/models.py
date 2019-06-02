from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())

    password_hash = db.Column(db.String(255))
    photos = db.relationship('PhotoProfile', backref='user', lazy="dynamic")

    article = db.relationship('Article', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'


class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer, primary_key=True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))


class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    post = db.Column(db.Text)
    posted = db.Column(db.Time, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def save_article(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_article(cls, id):
        atricle = Article.query.filter_by(id=id).all()
        return atricle
