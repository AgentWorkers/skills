---
name: Docker (Essentials + Advanced)
slug: docker
version: 1.0.3
homepage: https://clawic.com/skills/docker
description: 使用图像优化、网络配置以及适用于生产环境的最佳实践来构建、保护并部署 Docker 容器。
changelog: Added essential commands reference and production patterns
metadata: {"clawdbot":{"emoji":"🐳","requires":{"bins":["docker"]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以了解用户偏好指南。

## 使用场景

需要具备 Docker 相关知识。该工具负责管理容器、镜像、Compose 配置、网络设置、卷以及生产环境的部署。

## 架构

内存存储在 `~/docker/` 目录下。具体结构请参阅 `memory-template.md`。

```
~/docker/
└── memory.md    # Preferences and context
```

## 快速参考

| 主题 | 文件 |
|-------|------|
| 基本命令 | `commands.md` |
| Dockerfile 模板 | `images.md` |
| Compose 配置 | `compose.md` |
| 网络与卷管理 | `infrastructure.md` |
| 安全性加固 | `security.md` |
| 设置指南 | `setup.md` |
| 内存管理 | `memory-template.md` |

## 核心规则

### 1. 固定镜像版本
- 应使用 `python:3.11.5-slim` 而不是 `python:latest`，因为后者可能在不同时间点发生变化，导致构建结果不稳定。

### 2. 合并 `RUN` 命令
- 将 `apt-get update && apt-get install -y pkg` 命令合并到一个 `RUN` 命令中，以避免构建过程中的缓存问题。

### 3. 默认以非 root 用户身份运行
- 在 Dockerfile 中指定 `USER nonroot`，以确保安全扫描和平台策略的合规性。

### 4. 设置资源限制
- 为每个容器设置内存限制（例如：`-m 512m`），否则系统可能会因内存不足而触发 OOM（Out of Memory）错误。

### 5. 配置日志轮换
- 默认的日志文件格式（json）没有大小限制，可能会导致磁盘空间被占用。建议使用其他格式或配置日志轮换策略。

## 常见问题与解决方法

### 镜像相关问题
- 多阶段构建时，如果忘记使用 `--from=builder` 参数，可能会导致从错误阶段复制文件。
- 在执行 `COPY` 操作前，应先执行 `RUN` 命令以确保缓存被清除；先安装依赖项，再复制代码。
- 使用 `ADD` 命令可以自动解压文件包，但除非确实需要解压，否则应使用 `COPY` 命令。
- 构建参数会显示在镜像历史记录中，切勿将其用于存储敏感信息。

### 运行时相关问题
- 容器内的 `localhost` 实际上是容器自身的 IP 地址（`127.0.0.1`），需要将其绑定到 `0.0.0.0`。
- 如果端口已被其他容器占用，需要等待该容器停止或强制删除它。
- 出错代码 137 表示容器因 OOM 而终止，139 表示发生段错误（Segment Fault）——可以使用 `docker inspect --format='{{.State.ExitCode}}` 进行检查。
- 无 shell 的镜像无法直接访问文件，可以使用 `docker cp` 命令或调试工具进行数据传输。

### 网络相关问题
- 容器的 DNS 只在自定义网络中有效，默认的桥接网络无法解析域名。
- 公开发布的端口应绑定到 `127.0.0.1:5432`，以确保仅在本机范围内可用。
- 已终止的容器可能仍保持连接状态，需要设置健康检查机制并配置重启策略。

### Compose 相关问题
- `depends_on` 会等待容器启动完成，而非服务准备好；建议使用 `condition: service_healthy` 来确保依赖关系正确建立。
- `.env` 文件如果位于错误的位置可能会被忽略，应将其放在 `docker-compose.yml` 文件旁边。
- 卷挂载可能会覆盖容器内的文件；请确保主机目录和容器目录为空。
- YAML 中的锚点（anchors）在不同文件间可能无法正确传递数据，建议使用多个 `compose.yml` 文件来管理配置。

### 卷相关问题
- 匿名卷会不断累积数据；建议使用命名卷来避免数据丢失。
- 绑定挂载可能存在权限问题，确保容器用户与主机用户具有相同的权限。
- `docker system prune` 命令无法删除命名卷；需要使用 `--volumes` 参数来指定要删除的卷。
- 已终止的容器的数据会一直保留，需要使用 `docker container prune` 或 `--rm` 命令来清理。

### 资源泄漏问题
- 未使用的镜像会持续占用存储空间；定期使用 `docker image prune` 来清理这些镜像。
- 构建缓存可能会无限增长；使用 `docker builder prune` 来释放空间。
- 停止的容器会占用磁盘空间；可以使用 `docker container prune` 或 `--rm` 命令来释放资源。
- 多个 Compose 项目可能导致网络资源堆积；使用 `docker network prune` 来清理网络。

### 保密性与安全性
- 环境变量（ENV）和 `COPY` 操作会将敏感信息永久保存在镜像历史记录中；建议使用专门的保密机制（如 secrets mount 或运行时环境变量）。
- 使用 `--privileged` 参数会禁用所有安全限制；通常不需要这样做，应根据实际需求选择合适的权限设置。
- 来自未知注册表的镜像可能包含恶意代码；请验证镜像来源。
- 构建参数会显示在镜像历史记录中，切勿将其用于存储敏感信息。

## 调试技巧
- 出错代码 137 表示容器因 OOM 而终止，139 表示发生段错误——使用 `docker inspect --format='{{.State.ExitCode}}` 进行检查。
- 如果容器无法启动，请查看日志（即使容器已失败）：`docker logs <container>`。
- 无 shell 的镜像无法直接访问文件，可以使用 `docker cp` 命令或调试工具进行数据传输。
- 可以通过 `docker cp deadcontainer:/path ./local` 命令来查看已终止容器的文件系统内容。

## 相关技能
如果用户需要，可以使用 `clawhub install <slug>` 安装相关工具：
- `devops`：部署管道管理
- `linux`：主机系统管理
- `server`：服务器运维

## 反馈
- 如果本文档对您有帮助，请给 `clawhub` 评分（例如：使用星号）。
- 为了保持信息更新，请使用 `clawhub sync` 命令。