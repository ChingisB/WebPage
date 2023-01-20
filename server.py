from flask import Flask, render_template, redirect
from flask_login import LoginManager, current_user
from flask_login import login_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError
from forms.login_form import LoginForm
from forms.create_post_form import CreatePostForm
from forms.register_form import RegisterForm
from forms.comment_form import CommentForm
from database import create_user, get_num_pages, get_user_by_id, create_post, create_comment
from database import get_post_by_id, get_posts, verify, get_post_comments
from session import sess


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = verify(form.username.data, form.password.data)
        if user:
            user.is_authenticated = True
            login_user(user, force=True)
            return redirect('/main/1')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_confirm.data:
            return render_template('register.html', title="Создать новый аккаунт",
                                    form=form, register_error="Пароли не совпадают")
        try:
            create_user(form.username.data, form.password.data)
            return render_template('success.html')
        except IntegrityError:
            return render_template('register.html', title="Создать новый аккаунт",
                                    form=form, register_error="Такой пользователь уже есть")
    return render_template('register.html', title="Создать новый аккаунт",
                            form=form, register_error=None)


@app.route('/')
def check():
    return redirect('/login')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/main/<int:page>', methods=['GET'])
@login_required
def main_page(page):
    return render_template('index.html', posts=get_posts(page),
                            title='main', num_pages=get_num_pages())


@app.route('/write_post', methods=["GET", "POST"])
@login_required
def write_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        create_post(form.title.data, form.desc.data, form.content.data, current_user)
        return redirect('/main/1')
    return render_template('create_post.html', title="Создать пост", form=form)


@app.route('/post/<int:post_id>', methods=["GET", "POST"])
@login_required
def show_post(post_id: int):
    form = CommentForm()
    post = get_post_by_id(post_id)
    if form.validate_on_submit():
        create_comment(form.content.data, current_user, post)
        return render_template('post_view.html', title="Post",
                                post=post, form=form, comments=get_post_comments(post_id))
    return render_template('post_view.html',
                            title="Post", post=post, form=form, comments=get_post_comments(post_id))

def main():
    app.run()
    sess.commit()
    sess.close()


if __name__ == "__main__":
    main()
