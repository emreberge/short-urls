from flaskext.script import Manager
from web import db, app

manager = Manager(app)

@manager.command
def create_all():
    db.create_all()
    
@manager.command
def drop_all():
    db.drop_all()

if __name__ == "__main__":
    manager.run()
