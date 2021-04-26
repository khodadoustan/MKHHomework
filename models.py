from random import randint

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)
    created_on = db.Column(db.DateTime, index=False, unique=False, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class ShortLink(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=True,
    )
    user = db.relationship('User', backref='shortlink')
    main_url = db.Column(db.Text, nullable=False)
    otp_code = db.Column(db.Text, nullable=True)
    short_url = db.Column(db.String(20), nullable=False,
                          unique=True)  # 20 for user custom string. System generate 8 character string.
    expire = db.Column(db.Integer, default=5 * 60)
    private = db.Column(db.Boolean, default=False)
    redirection_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<Link %r>" % self.short_ur


class OTP(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        nullable=False,
    )
    user = db.relationship('User', backref='otp')
    token = db.Column(db.Integer, nullable=False, default=randint(1000, 9999), unique=True)
    used = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Link %r>" % self.otp
