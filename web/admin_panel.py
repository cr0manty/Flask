from web.app import app
from web.models import *
from web.sequrity import *
from flask_admin import Admin,  expose


admin = Admin(app, 'Cr0manty', url='/', index_view=Admin(name='Home'))
admin.add_view(Admin(Post, db.session, url='/admin/post'))
admin.add_view(Admin(Tag, db.session, url='/admin/tags'))
admin.add_view(Admin(User, db.session, url='/admin/users'))


@expose('/')
def index(self):
    return self.render('admin/index.html')