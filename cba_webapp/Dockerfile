FROM node:14
MAINTAINER Florian Schneider "florian.schneider.1992@gmx.de"

WORKDIR /usr/src/app

COPY package.json ./
RUN npm install

ENV CBA_DEPLOY="docker"
ENV CBA_API_HOST="cba_api"
ENV CBA_API_PORT="80"
ENV CBA_CONTEXT_PATH="/cba-app/"

COPY . .
EXPOSE 3000

RUN npm run build

CMD [ "npm", "run", "start" ]
