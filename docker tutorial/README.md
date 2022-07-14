<div align="center">
    <img src="https://i.imgur.com/rQVSCn6.png" width=100> <!-- Logo -->
    <h1>Docker Tutorial</h1> <!-- Title -->
</div>

---

<details>
<summary>Table of Contents</summary>

- [Docker Command Cheat Sheet](#docker-command-cheat-sheet)
  - [Info & Stats](#info--stats)
  - [Run](#run)
  - [Images](#images)
  - [Containers](#containers)
  - [Debugging](#debugging)
  - [Cleanup](#cleanup)
- [Dockerfile Cheat Sheet](#dockerfile-cheat-sheet)
- [Tips](#tips)
</details>

## About <!-- omit in toc -->

Docker cheat sheets.

## Docker Command Cheat Sheet

Collection of common Docker commands.

### Info & Stats

**docker images**: Lists all local images.

    docker images

**docker ps**: Process status. List running containers.

    docker ps [-a]

- Options:
  - `-a`: Show all containers.

### Run

**docker run**: Run a new container from an image.

    docker run [OPTIONS] <image>

- Options:
  - `-d`: Detached mode. Run the container in background.
  - `-e <env_var>`: Set environment variables.
  - `--env-file <file_path>`: Load environment variables from a file.
  - `-it`: Launches an interactive terminal. Allows commands to be run inside of the container.
  - `--name <name>`: Assign a name to the container.
  - `--net <network_name>`: Connects the container to a network.
  - `-p <host_port>:<container_port>`: Publish port. Maps container port to host port & exposes host port externally.

### Images

**docker build**: Build an image from a Dockerfile. Refer to [Dockerfile Cheat Sheet](#dockerfile-cheat-sheet) for more.

    docker build [OPTIONS] <path>

- Required:
  - `path`: Path of Dockerfile. Use `.` if Dockerfile is named `Dockerfile` & is in executed directory.
- Options:
  - `-t`: Name & tag an image in the format of `<name>:<tag>`.

**docker rmi**: Removes image.

    docker rmi [OPTIONS] <image>

- Options:
  - `-f`: Force remove.

**docker pull**: Pulls an image from a registry.

    docker pull <image>[:<tag>]

- Parameters:
  - `image`: Image name. Defaults to Docker Hub as remote registry. Use `<remote_url>/<image>` for other remote registries.

**docker push**: Push an image to a registry.

    docker push <image>[:<tag>]

- Parameters:
  - `image`: Image name. See **docker pull** in [Image Transfer](#image-transfer) for more details.

### Containers

**docker start**: Start 1 or more stopped containers.

    docker start <container> [<container> . . .]

**docker stop**: Stop 1 or more running containers.

    docker stop <container> [<container> . . .]

**docker rm**: Removes 1 or more containers.

    docker rm [OPTIONS] <container> [<container> . . .]

- Options
  - `-f`: Force remove.

### Debugging

**docker logs**: Prints the logs of a container.

    docker logs [OPTIONS] <container>

- Options:
  - `-f`: Follow log output. Continues to print new output from container.
  - `-t`: Show timestamps.

**docker exec**: Run commands in a running container. Use `docker exec -it <container> /bin/bash` to enter the terminal of the running container.

    docker exec [OPTIONS] <container> <command>

- Required:
  - `command`: Command to be executed.
- Options:
  - `-it`: Launches an interactive terminal.

### Cleanup

**docker system prune**: Remove dangling images.

    docker system prune [OPTIONS]

- Options:
  - `-a`: Remove all unused images.
  - `-f`: Force remove.

## Dockerfile Cheat Sheet

**FROM**: Sets base image.

    FROM <image>:<tag> [AS <name>]

**RUN**: Runs shell command by default.

    RUN <command>

**COPY**: Copies from host path to container path

    COPY <host_path> <container_path>

**WORKDIR**: Sets working directory in the container for `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, & `ADD`.

    WORKDIR <path>

**CMD**: The default command to be executed for a container at the end. There can only be 1 `CMD` in a Dockerfile.

```dockerfile
# NOTE: the outer brackets are required.
CMD ["<executable>", ["<command>" . . .]]
```

## Tips

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

Sauce: [Docker Best Practices](https://youtu.be/8vXoMqWgbQQ)

## Credits <!-- omit in toc -->

- [Techworld with Nana](https://twitter.com/Njuchi_)
- blvnk
