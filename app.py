from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_security import SQLAlchemyUserDatastore, Security
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from models import *
from admin import *

admin = Admin(app, 'Cr0manty', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)