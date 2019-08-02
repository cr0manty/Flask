from app import app, db
from models import *
from admin import *
from flask_admin import Admin,  expose


admin = Admin(app, 'Cr0manty', url='/admin', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))

@expose('/')
def index(self):
    return self.render('admin/index.html')