from wtforms import Form, StringField, TextAreaField


class PostForm(Form):
    title = StringField('Заголовок')
    body = TextAreaField('Текст')
