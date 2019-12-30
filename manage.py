
# manage our application
# but also create database
# migrations.Indeed, each time you make
# changes, you will need to migrate your
# database. So let's learn to do the thingimport os
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()