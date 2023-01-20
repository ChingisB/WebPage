import datetime
from sqlalchemy.exc import IntegrityError
from data.users import User
from data.post import Post
from data.comment import Comment
from session import sess


def get_user_by_id(user_id):
    user = sess.query(User).filter(User.id == user_id).first()
    if user:
        return user
    return None


def create_user(login: str, password: str) -> None:
    user = User()
    user.login = login
    user.hashed_password = get_hash(password)
    sess.add(user)
    try:
        sess.commit()
    except IntegrityError as i_e:
        sess.rollback()
        raise i_e


def create_post(title, desc, content, current_user):
    post = Post()
    post.title = title
    post.desc = desc
    post.content = content
    post.user = current_user
    sess.add(post)
    sess.commit()


def get_hash(password: str) -> int:
    num = 26
    modulo = 1e9 + 7
    hash_result = 0
    for letter in password:
        hash_result = (num * hash_result + ord(letter)) % modulo
    return hash_result


def verify(login: str, password: str) -> User:
    user = sess.query(User).filter(User.login == login,
                                   User.hashed_password == get_hash(password)).first()
    return user


def post_to_dict(post: Post) -> dict:
    new_post = {}
    new_post['id'] = post.id
    new_post['title'] = post.title
    new_post['desc'] = post.desc
    new_post['content'] = post.content
    new_post['created_date'] = datetime.datetime.strftime(post.created_date, "%d %B %Y %H:%M")
    new_post['user'] = post.user
    new_post['user_id'] = post.user_id
    return new_post


def get_posts(page: int):
    posts = sess.query(Post).order_by(Post.created_date.desc())
    posts = posts.limit(10)
    posts = posts.offset((page - 1) * 10)
    posts = posts.all()
    ans = []
    for post in posts:
        ans.append(post_to_dict(post))
    return ans


def get_post_by_id(post_id: int) -> Post:
    post = sess.query(Post).filter(Post.id == post_id).first()
    return post


def get_num_pages():
    num_posts = sess.query(Post).count()
    return num_posts // 10 + bool(num_posts % 10)


def comment_to_dict(comment: Comment) -> dict:
    new_comment = {}
    new_comment['id'] = comment.id
    new_comment['content'] = comment.content
    new_comment['created_date'] = datetime.datetime.strftime(comment.created_date, "%d %B %Y %H:%M")
    new_comment['user_id'] = comment.user_id
    new_comment['user'] = comment.user
    new_comment['post_id'] = comment.post_id
    new_comment['post'] = comment.post
    return new_comment


def get_post_comments(post_id):
    comments = sess.query(Comment).filter(Comment.post_id == post_id).all()
    ans = []
    for comment in comments:
        ans.append(comment_to_dict(comment))
    return ans

def create_comment(content, user, post):
    comment = Comment()
    comment.content = content
    comment.user = user
    comment.post = post
    sess.add(comment)
    sess.commit()
