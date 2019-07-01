# microservices App using Flask, Python, TDD, Docker
# tom_micro

Deployed on EC2 instance (req)
Prod and Dev environments set up
use docker-compose to build container locally or on ec2 (recreate_db, seed_db, test available for exec commands)
docker-compose -f docker-compose-prod.yml up -d

# use this // need aws access_id and secret pass
docker-machine create --driver amazonec2 appName

# active host and
docker-machine env appName
eval $(docker-machine env appName)

docker-compose -f docker-compose-prod.yml up -d --build

# add ports on AWS to accept from new instance
