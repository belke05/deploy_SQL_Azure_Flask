import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)
# so you can do python manage.py db init upgrade or migrate 

if __name__ == '__main__':
    manager.run()