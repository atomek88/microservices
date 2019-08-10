# manage.py services/users
import sys
import unittest
import coverage
from flask.cli import FlaskGroup
from project import create_app, db
from project.api.models import User

# add coverage reports - import in requirements.txt
COV = coverage.coverage(branch=True,
    include='project/*',
    omit=['projects/tests/*',
        'projects/config.py',
        ]
    )
COV.start()

app = create_app()
cli = FlaskGroup(create_app=create_app)
# add cli interface to app to run and manage flask app from cl
# docker-compose exec users flask shell (manage app+db context direcly)
@cli.command('recreate_db')
def recreate_db():
    """ recreates db every time for data integrity and testing """
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """Runs the tests without code coverage"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)

@cli.command('seed_db')
def seed_db():
    """seed the db"""
    db.session.add(User(
        username='tom', email='tom@yahoo.com', password='password1'))
    db.session.add(User(
        username='jon', email='jon@yahoo.com', password='password2'))
    db.session.commit()

@cli.command()
def cov():
    """runs unit tests with coverage"""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    sys.exit(result)
if __name__ == '__main__':
    cli()
