from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps import create_app
from apps.models.new import *
from apps.models.user import *


app = create_app()
manager = Manager(app=app)

migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)










if __name__ == '__main__':
    manager.run()
