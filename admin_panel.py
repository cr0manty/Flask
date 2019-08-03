from app import app, db
from models import *
from sequrity import *
from flask_admin import Admin,  expose


admin = Admin(app, 'Cr0manty', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session, url='/admin/post'))
admin.add_view(TagAdminView(Tag, db.session, url='/admin/tags'))
admin.add_view(UsersAdminView(User, db.session, url='/admin/users'))


@expose('/')
def index(self):
    return self.render('admin/index.html')