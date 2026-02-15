---
name: docker-essentials
description: 用于容器管理、镜像操作和调试的基本 Docker 命令和工作流程。
homepage: https://docs.docker.com/
metadata: {"clawdbot":{"emoji":"🐳","requires":{"bins":["docker"]}}}
---

# Docker基础

Docker的核心命令，用于容器和镜像的管理。

## 容器生命周期

### 运行容器
```bash
# Run container from image
docker run nginx

# Run in background (detached)
docker run -d nginx

# Run with name
docker run --name my-nginx -d nginx

# Run with port mapping
docker run -p 8080:80 -d nginx

# Run with environment variables
docker run -e MY_VAR=value -d app

# Run with volume mount
docker run -v /host/path:/container/path -d app

# Run with auto-remove on exit
docker run --rm alpine echo "Hello"

# Interactive terminal
docker run -it ubuntu bash
```

### 管理容器
```bash
# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Stop container
docker stop container_name

# Start stopped container
docker start container_name

# Restart container
docker restart container_name

# Remove container
docker rm container_name

# Force remove running container
docker rm -f container_name

# Remove all stopped containers
docker container prune
```

## 容器检查与调试

### 查看日志
```bash
# Show logs
docker logs container_name

# Follow logs (like tail -f)
docker logs -f container_name

# Last 100 lines
docker logs --tail 100 container_name

# Logs with timestamps
docker logs -t container_name
```

### 执行命令
```bash
# Execute command in running container
docker exec container_name ls -la

# Interactive shell
docker exec -it container_name bash

# Execute as specific user
docker exec -u root -it container_name bash

# Execute with environment variable
docker exec -e VAR=value container_name env
```

### 容器检查
```bash
# Inspect container details
docker inspect container_name

# Get specific field (JSON path)
docker inspect -f '{{.NetworkSettings.IPAddress}}' container_name

# View container stats
docker stats

# View specific container stats
docker stats container_name

# View processes in container
docker top container_name
```

## 镜像管理

### 构建镜像
```bash
# Build from Dockerfile
docker build -t myapp:1.0 .

# Build with custom Dockerfile
docker build -f Dockerfile.dev -t myapp:dev .

# Build with build args
docker build --build-arg VERSION=1.0 -t myapp .

# Build without cache
docker build --no-cache -t myapp .
```

### 管理镜像
```bash
# List images
docker images

# Pull image from registry
docker pull nginx:latest

# Tag image
docker tag myapp:1.0 myapp:latest

# Push to registry
docker push myrepo/myapp:1.0

# Remove image
docker rmi image_name

# Remove unused images
docker image prune

# Remove all unused images
docker image prune -a
```

## Docker Compose

### 基本操作
```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs

# Follow logs for specific service
docker-compose logs -f web

# Scale service
docker-compose up -d --scale web=3
```

### 服务管理
```bash
# List services
docker-compose ps

# Execute command in service
docker-compose exec web bash

# Restart service
docker-compose restart web

# Rebuild service
docker-compose build web

# Rebuild and restart
docker-compose up -d --build
```

## 网络配置
```bash
# List networks
docker network ls

# Create network
docker network create mynetwork

# Connect container to network
docker network connect mynetwork container_name

# Disconnect from network
docker network disconnect mynetwork container_name

# Inspect network
docker network inspect mynetwork

# Remove network
docker network rm mynetwork
```

## 卷（Volume）管理
```bash
# List volumes
docker volume ls

# Create volume
docker volume create myvolume

# Inspect volume
docker volume inspect myvolume

# Remove volume
docker volume rm myvolume

# Remove unused volumes
docker volume prune

# Run with volume
docker run -v myvolume:/data -d app
```

## 系统管理
```bash
# View disk usage
docker system df

# Clean up everything unused
docker system prune

# Clean up including unused images
docker system prune -a

# Clean up including volumes
docker system prune --volumes

# Show Docker info
docker info

# Show Docker version
docker version
```

## 常见工作流程

**开发容器：**
```bash
docker run -it --rm \
  -v $(pwd):/app \
  -w /app \
  -p 3000:3000 \
  node:18 \
  npm run dev
```

**数据库容器：**
```bash
docker run -d \
  --name postgres \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=mydb \
  -v postgres-data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15
```

**快速调试：**
```bash
# Shell into running container
docker exec -it container_name sh

# Copy file from container
docker cp container_name:/path/to/file ./local/path

# Copy file to container
docker cp ./local/file container_name:/path/in/container
```

**多阶段构建：**
```dockerfile
# Dockerfile
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

## 有用的标志（Flags）

**`docker run` 的标志：**
- `-d`：分离模式（在后台运行）
- `-it`：交互式终端
- `-p`：端口映射（主机到容器）
- `-v`：挂载卷
- `-e`：环境变量
- `--name`：容器名称
- `--rm`：容器退出后自动删除
- `--network`：连接到网络

**`docker exec` 的标志：**
- `-it`：交互式终端
- `-u`：指定用户
- `-w`：工作目录

## 提示：

- 使用 `.dockerignore` 文件排除构建过程中的文件
- 在 Dockerfile 中组合 `RUN` 命令以减少镜像层数
- 使用多阶段构建来减小镜像大小
- 为镜像添加版本标签
- 对于一次性使用的容器，使用 `--rm` 命令
- 使用 `docker-compose` 管理多容器应用
- 定期使用 `docker system prune` 清理系统资源

## 文档参考

官方文档：https://docs.docker.com/
Dockerfile 参考：https://docs.docker.com/engine/reference/builder/
Compose 文件参考：https://docs.docker.com/compose/compose-file/