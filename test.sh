#!/bin/bash

fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

#run unit and integration tests
server() {
  echo 'running server unittests'
  docker-compose up -d --build
  docker-compose exec users python manage.py test
  inspect $? users
  docker-compose exec users flake8 project
  inspect $? users-lint
  docker-compose down
}

# run e2e tests
client() {
  echo 'running client'
  docker-compose up -d --build
  docker-compose exec client npm test -- --coverage
  # add command {q} to pass into react tests since doesnt quit on its own
  inspect $? client
  docker-compose down
}
e2e() {
  echo 'running e2e'
  docker-compose -f docker-compose-prod.yml up -d --build
  docker-compose -f docker-compose-prod.yml exec users python manage.py recreate_db
  ./node_modules/.bin/cypress run --config baseUrl=http://localhost
  inspect $? e2e
  docker-compose -f docker-compose-prod.yml down
}
all() {
  echo "running all tests"
  server
  client
  e2e
}
$1 $2 $3 $4

# run appropriate tests
<<COMMENT
if [[ "${type}" == "server" ]]; then
  echo "\n"
  echo "Running server-side tests!\n"
  server
elif [[ "${type}" == "client" ]]; then
  echo "\n"
  echo "Running client-side tests!\n"
  client
elif [[ "${type}" == "e2e" ]]; then
  echo "\n"
  echo "Running e2e tests!\n"
  e2e
else
  echo "\n"
  echo "Running all tests!\n"
  all
fi
COMMENT


# return code
if [ -n "${fails}" ]; then
  echo "Tests fails: ${fails}"
  exit 1
else
  echo "Tests passed"
  exit 0
fi
