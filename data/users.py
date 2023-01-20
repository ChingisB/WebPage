import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_authenticated = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    is_anonymous = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return self.login
