microservices App

# Microservices with Docker, Flask, React
[![Build Status](https://travis-ci.org/atomek88/microservices.svg?branch=master)](https://travis-ci.org/atomek88/microservices

USING
SQLAlchemy (postgresql), Blueprints (routing), coverage, CI (travis CI via github), flake8 (linter for semantics)
Flask Debug Toolbar (debug toolbar)
TDD (Flask-Testing)

BUILD HELP
Deployed on EC2 instance (req)
Prod and Dev environments set up
use docker-compose to build container locally or on ec2 (recreate_db, seed_db, test available for exec commands)
docker-compose -f docker-compose-prod.yml up -d --build (?nginx)  # use non prod for localhost

# use this // need aws access_id and secret pass
docker-machine create --driver amazonec2 appName

# active host and
docker-machine env appName
eval $(docker-machine env appName) #point to aws
eval $(docker-machine env -u) #point to localhost

docker-compose up -d --build # update containers
# auto reload see changes on server
docker-compose logs -f

# add ports on AWS to accept from new instance

# run cli commands from manage.py
docker-compose -f docker-compose-prod.yml exec users python/3 manage.py CMD

# run unit & integration tests
docker-compose exec users python3 manage.py {cov, test}
docker-compose exec users flake8 project (linter)
npm test - runs react-scripts
react-scripts test --coverage
