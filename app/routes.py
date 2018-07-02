from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',title='Home')

@app.route('/contact')
def contact():
    return render_template('contact.html',title='Contact')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid login credentials')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title='Login',form=login_form)

@app.route('/news')
def news():
    return render_template('news.html',title='News')

@app.route('/profile')
def profile():
    if current_user.is_anonymous:
        return redirect(url_for('index'))
    user=current_user
    return render_template('profile.html',title='Profile',user=user)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = User(username=register_form.username.data, \
            email=register_form.email.data)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))

    return render_template('register.html',title='Register',form=register_form)

@app.route('/what')
def what():
    return render_template('what.html',title='What')

@app.route('/where')
def where():
    return render_template('where.html',title='Where')

@app.route('/who')
def who():
    return render_template('who.html',title='Who')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
