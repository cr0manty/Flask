from app import app, db, current_user_info
from flask import render_template, redirect, url_for
from flask_security import login_required, current_user, logout_user
from sequrity import Registration, User


@app.route('/')
def index():
    return render_template('index.html', user=current_user)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/links')
def links():
    return render_template('links.html')

@app.route('/login')
def login():
    pass

@app.route('/register', methods=['GET', 'POST'])
def user_reg():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = Registration()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data,
                    first_name=form.first_name.data, last_name=form.last_name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<slug>')
@login_required
def show_user(slug):
    user = User.query.filter(User.slug == slug)
    return render_template('user.html', slug=current_user_info)
