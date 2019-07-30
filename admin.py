from flask import redirect, url_for, request
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from flask_admin import AdminIndexView


class AdminPanel:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))


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
