from flask import Flask
from web.config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore

app = Flask(__name__)
app.config.from_object(Configuration)
login = LoginManager(app)
login.login_view = 'login'

db = SQLAlchemy(app)

from .models import User, Role
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
