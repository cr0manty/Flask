from app import app, db
from flask import render_template, redirect, url_for, request
from flask_security import login_required, current_user, login_user, logout_user
from sequrity import Registration, User, Login
from werkzeug.urls import url_parse

current_user_info = None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return url_for(next_page)
    return render_template('login_user.html', form=form)


@app.route('/')
def index():
    return render_template('index.html', user=current_user_info)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/links')
def links():
    return render_template('links.html')


@app.route('/register', methods=['GET', 'POST'])
def user_reg():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Registration()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data,
                    first_name=form.first_name.data, last_name=form.last_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def show_user(username):
    return render_template('user.html', user=current_user_info)
