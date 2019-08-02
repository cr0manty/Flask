from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_security import SQLAlchemyUserDatastore, Security

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from models import *
from admin_panel import *

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)