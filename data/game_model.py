import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )
    total_rounds = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=10)
    trends = sqlalchemy.Column(sqlalchemy.PickleType, nullable=False, default={})
    points_gave = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user = orm.relationship('User')
