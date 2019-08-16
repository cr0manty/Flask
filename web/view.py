from web.app import app, db
from flask import render_template, redirect, url_for, request
from flask_security import login_required, current_user, logout_user, login_user
from web.sequrity import Registration, User
from web.sequrity import Login
from flask.testing import url_parse
from web.location import make_map


@app.route('/')
def index():
    make_map()
    return render_template('index.html',
                           username=(current_user.name if current_user.is_authenticated
                                     else None))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/links')
def links():
    return render_template('links.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return url_for(next_page)
    return render_template('security/login.html', form=form)


@app.route('/reg', methods=['GET', 'POST'])
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

    return render_template('security/registration.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def show_user(username):
    user = User.query.filter(User.name == username).first()
    return render_template('user.html', user=user)
