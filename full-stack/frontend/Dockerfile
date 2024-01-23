FROM node:alpine3.19 AS build
WORKDIR /app

COPY package*.json ./
COPY tsconfig*.json ./
COPY vite.config.ts .


# We don't use the --production flag because @vitejs/plugin-react is needed when running npm run build and @vitejs/plugin-react
# is listed under devDependencies. It's needed to build the app for production inside the Docker container.
# The final built application that runs in production will not include these development dependencies. 
RUN npm ci  

COPY src ./src
COPY public ./public
COPY index.html .

ARG VITE_DJANGO_HOST
ENV VITE_DJANGO_HOST=$VITE_DJANGO_HOST

ARG VITE_DJANGO_PORT
ENV VITE_DJANGO_PORT=$VITE_DJANGO_PORT

RUN npm run build