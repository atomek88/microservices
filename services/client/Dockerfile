# base image
FROM node:11.12.0-alpine

# wdir
WORKDIR /usr/src/app

# add usr/src/app/node_modules/.bin' to path
ENV PATH /usr/src/app/node_modules/.bin:$PATH

# install cache app dependencies
COPY package.json /usr/src/app/package.json
COPY package-lock.json /usr/src/app/package-lock.json
RUN npm ci
RUN npm install react-scripts@2.1.8 -g --silent

# start
CMD ["npm" , "start"]
