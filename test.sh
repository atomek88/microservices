#!/bin/bash

fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

#run unit and integration tests
unittests() {
  docker-compose up -d --build
  docker-compose exec users python manage.py test
  inspect $? users
  docker-compose exec users flake8 project
  inspect $? users-lint
  docker-compose exec client npm test -- --coverage
  # add command {q} to pass into react tests since doesnt quit on its own
  inspect $? client
  docker-compose down
}

# run e2e tests
e2e() {
  docker-compose -f docker-compose.yml up -d --build
  docker-compose -f docker-compose.yml exec users python manage.py recreate_db
  ./node_modules/.bin/cypress run --config baseUrl=http://localhost
  inspect $? e2e
  docker-compose -f docker-compose.yml down
}
test() {
  echo "test success"
}

$1 $2 $3 $4

# return code
if [ -n "${fails}" ]; then
  echo "Tests fails: ${fails}"
  exit 1
else
  echo "Tests passed"
  exit 0
fi
