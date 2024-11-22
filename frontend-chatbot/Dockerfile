FROM node:16.14.2 AS build

# RUN apt-get update && apt-get install -y curl && apt-get clean

WORKDIR /web-app

COPY package.json package-lock.json ./

RUN npm install

COPY . .
RUN npm run build

RUN npm install -g serve

CMD ["serve", "-s", "build"]



