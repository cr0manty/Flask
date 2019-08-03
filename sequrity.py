from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from flask_admin import AdminIndexView
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from models import User


class Registration(FlaskForm):
    first_name = StringField('Имя')
    last_name = StringField('Фамилия')
    name = StringField('Логин', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторить пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегестрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пользователь с данным логином уже зарегестрирован.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пользователь с данным email уже зарегестрирован.')


class Login(FlaskForm):
    login = StringField('Логин')
    password = PasswordField('Пароль')
    submit = SubmitField('Войти')


class AdminPanel:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index', next=request.url))


class BaseView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseView, self).on_model_change(form, model, is_created)


class AdminView(AdminPanel, ModelView):
    pass


class HomeAdminView(AdminPanel, AdminIndexView):
    pass


class PostAdminView(AdminPanel, BaseView):
    form_columns = ['title', 'body', 'tags']


class TagAdminView(AdminPanel, BaseView):
    form_columns = ['name', 'posts']


class UsersAdminView(AdminPanel, BaseView):
    form_columns = ['email', 'name', 'password', 'roles']
