import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    username = sqlalchemy.Column(
        sqlalchemy.String(32),
        unique=True,
        nullable=False
    )
    stars = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    points = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    points_spent = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    exchange_history = sqlalchemy.Column(sqlalchemy.JSON, nullable=False, default={})
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    games = orm.relationship('Game', back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
