# Docker Tutorial

![banner](https://i.imgur.com/rQVSCn6.png)

Learning Docker with NodeJS from [Docker Tutorial for Beginners](https://youtu.be/3c-iBn73dDE). Forked from Nanuchi's [Docker demo](https://gitlab.com/nanuchi/techworld-js-docker-demo-app).

## Content

Deploying a NodeJS web app with MongoDB onto Docker with persistence.

---

### Basic Commands

**Docker Pull**

    docker pull <image>

Pulls an image from a registry.

**Docker Images**

    docker images

List all images.

**Docker Run**

    docker run <image> [OPTIONS]

Runs a new container from an image.

- Options:
  - `-d`: Detached mode (ie. run in background).
  - `--name`: Name of the container.
  - `-e`: Set environment variables.
  - `-p <host_port>:<container_port>`: Port binding. Binds host port to container port.
    - This allows to run multiple instances of the same container port.
- Shortcut:
  - `docker run <image>:<tag>` = `docker pull <image>:<tag> && docker run <image>:<tag>`

**Docker Process Status**

    docker ps

Lists all running containers.

- Options:
  - `-a`: Show all containers.

**Docker Start / Stop**

    docker start <container_ID>
    docker stop <container_ID>

#### Debugging

**Docker Logs**

    docker logs <container_ID>

Fetches the logs of a container.

**Docker Container Terminal**

    docker exec -it <container_ID> /bin/bash

Launch a interactive terminal in the container. Specify shell type with `/bin/bash`.

### Practical: Basic Deployment of NodeJS Web App w/ Containers

#### Step 1: Pull the Image

    docker pull mongo
    docker pull mongo-express

**Docker Network**

![](https://i.imgur.com/v4WqyAp.png)

Containers in the same network can communicate with each other automatically. With a network, configuring IP addresses / port number for each container is not necessary. External applications can connect to it using the IP address of the exposed container(s).

**Docker Create Network**

    docker network create <network_name>

**Docker List Network**

    docker network ls

#### Step:2 Run MongoDB Containers

**Run Mongo**

    docker run ^
      -d ^
      -p 27017:27017 ^
      -e MONGO_INITDB_ROOT_USERNAME=admin ^
      -e MONGO_INITDB_ROOT_PASSWORD=password ^
      --name mongodb ^
      --net mongo-network ^
      mongo

Docker will run the container in detached mode on port 27017 with respective environment variables. The container will be named `mongodb`. The container will be connected to the network `mongo-network`. Environment variable names are found in [MongoDB Docker docs](https://hub.docker.com/_/mongo).

**Run MongoExpress UI**

    docker run ^
      -d ^
      -p 8081:8081 ^
      -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin ^
      -e ME_CONFIG_MONGODB_ADMINPASSWORD=password ^
      -e ME_CONFIG_MONGODB_SERVER=mongodb ^
      --net mongo-network ^
      --name mongo-express ^
      mongo-express

#### Step 4: Docker Compose

**Syntax**

```yaml
version: "3" # optional
services:
  mongodb: # container name
    image: mongo # image name. version can also be specified.
    ports:
      - 27017:27017
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password
    volumes:
      - mongo-data:/data/db
  mongo-express:
    image: mongo-express
    restart: always # fixes MongoNetworkError when mongodb is not ready when mongo-express starts
    ports:
      - 8080:8081
    environment:
      - ME_CONFIG_MONGODB_ADMINUSERNAME=admin
      - ME_CONFIG_MONGODB_ADMINPASSWORD=password
      - ME_CONFIG_MONGODB_SERVER=mongodb
volumes:
  mongo-data:
    driver: local
```

Docker Compose takes care of creating a common network. Hence there is no need to specify the network name.

**Running Docker Compose**

    docker-compose <up | down>

- Options:
  -  `-f`: Specify docker-compose.yaml file path.
  -  `-d`: Detached mode.

Alternative for Docker run commands. Starts or stops containers.

### Building Docker Image w/ Dockerfile

```dockerfile
FROM node:13-alpine

ENV MONGO_DB_USERNAME=admin \
    MONGO_DB_PWD=password

RUN mkdir -p /home/app

COPY ./app /home/app

WORKDIR /home/app

RUN npm install

CMD ["node", "server.js"]
```

- `FROM node:13-alpine` installs node & `13-alpine` version to use node command.
- `ENV MONGO_DB_USERNAME=admin MONGO_DB_PWD=password` configures env vars.
- `RUN mkdir -p /home/app` executes any Linux command
- `COPY ./app /home/app` copies everything from Host `/app` dir into Container `/home/app` dir.
- `WORKDIR /home/app`
- `RUN npm install`
- `CMD ["node", "server.js"]` default command that overrides other commands when container runs.
- _whenever Dockerfile is modified, image must be rebuilt._

```
docker build -t <image_name>:<tag> <Dockerfile_directory>
```

- eg `docker build -t my-app:1.0 .`
  - tells Docker to build my-app with tag 1.0 with Dockerfile located in current dir.
- `t` is an optional parameter to add a tag to the image.

```
docker run my-app:1.0
```

---

### Dependencies

- [Docker](https://www.docker.com/products/docker-desktop)

### Execution

1. Start MongoDB & Mongo-Express.
   - `docker-compose -f docker-compose.yaml up`
2. Navigate to `localhost:8080`.
3. Create new database `my-db`.
4. Create new collection `users`.
5. Start Node server in `/app`.
   - `npm install`\
     `node server.js`
6. Access NodeJS web app in `localhost:3000`.
7. Build Docker image.
   - `docker build -t my-app:1.0 .`

### Tips

Sauce: [Docker Best Practices](https://youtu.be/8vXoMqWgbQQ)

1. Use official Docker images as base image.
   - Instead of:
     ```dockerfile
     FROM ubuntu
     RUN apt-get update && apt-get install -y \
         node \
         && rm -rf /var/lib/apt/lists/*
     ```
   - Use this:
     ```dockerfile
     FROM node
     ```
2. Use specific image versions.
   - Using latest versions cause unpredictability.
   - Instead of:
     ```dockerfile
     FROM node
     ```
   - Use this:
     ```dockerfile
     FROM node:17.0.1
     ```
3. Use small-sized official images.
   - Using leaner distros reduce attack surface, increasing security.
   - Instead of:
     ```dockerfile
     FROM node:17.0.1
     ```
   - Use this:
     ```dockerfile
     FROM node:17.0.1-alpine
     ```
4. Optimize caching Image Layers
   - TLDR: <mark>Order Dockerfile commands from least changed to most changed</mark>.
   - **Image Layer**: Each Docker command in a Dockerfile creates a layer. The layers are built <mark>upwards</mark>.
   - **Caching an Image Layer**: Only the layers that are changed are rebuilt (ie downloaded). However, <mark>all subsequent layer would also be rebuilt from the changed layer</mark>.
   - To optimize caching, it is best to cache as many image layers as possible (ie run as many unchanged commands).
   - Instead of:
     ```dockerfile
     FROM node:17.0.1-alpine
     WORKDIR /app
     COPY myapp /app
     RUN npm install --production
     CMD ["node", "src/index.js"]
     ```
   - Use this:
     ```dockerfile
     FROM node:17.0.1-alpine
     WORKDIR /app
     COPY package.json package-lock.json .
     RUN npm install --production
     COPY myapp /app
     CMD ["node", "src/index.js"]
     ```
   - For example, in the 1st example, if we modify the source code, Docker will rebuild layers `COPY` to `CMD`. In the 2nd example, Docker will only rebuild layers `COPY` to `CMD`. Note that running `npm install` takes a long time.
5. Use `.dockerignore` to ignore autogenerated files / others.
   - Exclude `venv`, README, etc.
6. Use multi-stage builds.

   - There are some files that are needed for building the image, but not for running the app at the final stage (eg requirements.txt, package.json).
   - You can separate them with multiple `FROM` commands. Each `FROM` command starts a new build stage. But only the last `FROM` command creates the final Image Layer.
   - Use this:

     ```dockerfile
     # build stage
     FROM maven as build
     ...

     # run stage
     FROM tomcat
     ...
     ```

7. Use the least privileged user.
   - By default Docker runs on root.
   - Fix this by creating a new user & group with only required permissions.
   - Use this:
     ```dockerfile
     # create group & user
     RUN groupadd -r tom && useradd -g tom tom
     # set ownership & permissions
     RUN chown -R tom:tom /app
     # switch to user
     USER tom
     CMD node index.js
     ```
   - _Note: Some base images have a generic user bundled in, so you can use it._
     - For example, `USER node` in node image.
8. Docker scan for vulnerabilities.
   - Run this following command:
     ```
     docker scan <app_name>:<tag_number>
     ```
   - Can be <mark>integrated in CI/CD</mark>.

## Credits

- [Techworld with Nana](https://twitter.com/Njuchi_)
- prod by blvnk.
