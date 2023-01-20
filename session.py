from data import db_session

db_session.global_init('db/blogs.db')
sess = db_session.create_session()