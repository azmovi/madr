FROM node:lts-alpine

RUN npm install -g http-server

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ /app/


RUN npm run dev

EXPOSE 8080

CMD [ "http-server", "dist" ]
