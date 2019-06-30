# manage.py services/users

from flask.cli import FlaskGroup
from project import app

cli = FlaskGroup(app)
# add cli interface to app to run and manage flask app from cl

if __name__ == '__main__':
    cli()
