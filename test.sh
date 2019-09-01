#!/bin/bash

fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

#run unit and integration tests
docker-compose up -d --build
docker-compose exec users python manage.py test
inspect $? users
docker-compose exec users flake8 project
inspect $? users-lint
docker-compose exec client npm test -- --coverage
# add command {q} to pass into react tests since doesnt quit on its own
inspect $? client
docker-compose down

# return code
if [ -n "${fails}" ]; then
  echo "Tests fails: ${fails}"
  exit 1
else
  echo "Tests passed"
  exit 0
fi
