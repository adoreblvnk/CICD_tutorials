# Docker Tutorial

![banner](https://i.imgur.com/rQVSCn6.png)

Learning Docker with NodeJS from [Docker Tutorial for Beginners](https://youtu.be/3c-iBn73dDE). Forked from Nanuchi's [Docker demo](https://gitlab.com/nanuchi/techworld-js-docker-demo-app).

## About

Deploying a NodeJS web app with MongoDB onto Docker with persistence.

---

### Basic Commands

```
docker pull <image>
```

- default version is latest.

```
docker images
```

```
docker run <image> [<-d> <--name <name>> <-e <environment_variables>>]
```

- create & run a new container from an image.
- `-d` runs container in detached mode (ie run in background).
- `--name` gives a custom name to container.
- `-e` sets env vars.

```
docker ps <-a>
```

- lists running containers.
- `-a` shows all containers.

```
docker stop <container_ID>
```

```
docker start <container_ID>
```

#### Port Binding

```
docker run -p <Host_Port>:<Container_Port>
```

- binds host port to container port.
  - to run multiple instances of the same port.

#### Troubleshooting

```
docker logs <container_ID>
```

```
docker exec -it <container_ID> <shell_path>
```

- launches an interactive terminal in a container. Specify shell type (eg `/bin/sh`, `/bin/bash`).
  - navigate the directories of the container here.
  - check env var with `env` command.

### Basic Deployment of NodeJS Web App w/ Containers

```
docker pull mongo
docker pull mongo-express
```

- pull MongoDB images.

#### Docker Network

![docker network](https://i.imgur.com/v4WqyAp.png)

Docker Network where containers are in. When 2 containers are deployed in the same network, they can communicate with each other without configuring localhost port number, etc.

Applications that run outside of the network will connect to it just by using localhost & port number.

```
docker network create <network_name>
```

```
docker network ls
```

#### Run MongoDB Containers

```
docker run ^
  -d ^
  -p 27017:27017 ^
  -e MONGO_INITDB_ROOT_USERNAME=admin ^
  -e MONGO_INITDB_ROOT_PASSWORD=password ^
  --name mongodb ^
  --net mongo-network ^
  mongo
```

- docker run in detached mode on host port 27017 with respective env vars with name mongodb. This will run in the network mongo-network defined earlier.
- env var names are in [MongoDB Docker docs](https://hub.docker.com/_/mongo).

```
docker run ^
  -d ^
  -p 8081:8081 ^
  -e ME_CONFIG_MONGODB_ADMINUSERNAME=admin ^
  -e ME_CONFIG_MONGODB_ADMINPASSWORD=password ^
  --net mongo-network ^
  --name mongo-express ^
  -e ME_CONFIG_MONGODB_SERVER=mongodb ^
  mongo-express
```

- runs mongo-express.

### Docker Compose

```
docker-compose -f <filename> <up | down> [<-d>]
```

- run configurations across multiple containers quickly.
  - _docker-compose is an efficient alternative to running multiple Docker commands._
- `up` builds & starts containers.
- `down` stops containers.

### Building Docker Image w/ Dockerfile

```
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

## Credits

- [Techworld with Nana](https://twitter.com/Njuchi_)
- blvnk
