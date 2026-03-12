---
name: Docker
slug: docker
version: 1.0.4
homepage: https://clawic.com/skills/docker
description: "Docker容器、镜像、Compose编排堆栈、网络配置、卷管理、调试工具以及用于维护真实环境稳定性的相关命令。这些工具适用于以下场景：  
1. 当任务涉及Docker、Dockerfile、镜像、容器或Compose时；  
2. 当构建系统的可靠性、运行时行为、日志记录、端口配置、卷管理或安全性需要重点关注时；  
3. 当代理程序需要Docker的指导，并且应默认采用Docker的相关配置时。"
changelog: Simplified the skill name and kept the stateless activation guidance
metadata: {"clawdbot":{"emoji":"🐳","requires":{"bins":["docker"]},"os":["linux","darwin","win32"]}}
---
## 使用场景

当任务涉及 Docker、Dockerfile、容器构建、Compose、镜像发布、网络配置、卷管理、日志记录、调试或生产环境中的容器操作时，请使用本技能。该技能具有“无状态”特性，应在任何与 Docker 相关的工作场景中直接应用。

## 快速参考

| 主题 | 文件 |
|-------|------|
| 基本命令 | `commands.md` |
| Dockerfile 模板 | `images.md` |
| Compose 配置 | `compose.md` |
| 网络与卷管理 | `infrastructure.md` |
| 安全加固 | `security.md` |

## 核心规则

### 1. 固定镜像版本
- 应使用特定版本（例如 `python:3.11.5-slim`），而非 `python:latest`；因为最新版本可能与后续版本不兼容，导致构建失败。

### 2. 合并 `RUN` 命令
- 将多个 `apt-get update` 和 `apt-get install` 命令合并到一个 `RUN` 命令中执行，以避免缓存问题。

### 3. 默认以非 root 用户身份运行容器
- 在 Dockerfile 中添加 `USER nonroot` 语句；以 root 用户身份运行会干扰安全扫描和平台策略。

### 4. 设置资源限制
- 为每个容器设置内存限制（例如 `-m 512m`），否则容器可能会因内存不足而崩溃。

### 5. 配置日志轮换
- 默认的 JSON 文件日志格式没有大小限制，可能导致日志文件占用过多磁盘空间。

## 常见问题与注意事项

### 镜像相关问题
- 多阶段构建时，如果忘记使用 `--from=builder` 选项，可能会从错误的构建阶段复制文件。
- 在执行 `COPY` 操作前应先执行 `RUN` 命令，以确保缓存被清除。
- 使用 `ADD` 命令可以自动解压文件包；除非确实需要解压，否则应使用 `COPY` 命令。
- 构建参数会显示在镜像历史记录中，切勿将其用于存储敏感信息。

### 运行时相关问题
- 容器内的 `localhost` 实际上是指容器自身的 IP 地址（`0.0.0.0`），需要将其绑定到外部地址。
- 如果端口已被其他容器占用，需要等待该容器停止或强制删除它。
- 输出代码 137 表示容器因内存不足（OOM）而终止，代码 139 表示发生段错误（segfault）——可以使用 `docker inspect --format='{{.State.ExitCode}}` 进行检查。
- 无 shell 的镜像无法直接访问文件，可以使用 `docker cp` 或调试工具来传输文件。

### 网络相关问题
- 容器的 DNS 只在自定义网络中有效；默认的桥接网络无法解析域名。
- 发布的端口应绑定到 `0.0.0.0:5432`，以便在本地访问。
- 已终止的容器可能仍然保持连接状态，需要设置健康检查机制并配置重启策略。

### Compose 相关问题
- `depends_on` 会等待容器启动完成，而非服务准备好；应使用 `condition: service_healthy` 来确保服务已启动。
- `.env` 文件如果位于错误的位置可能会被忽略；它必须位于 `docker-compose.yml` 的同一目录下。
- 卷挂载可能会覆盖容器内的文件；请确保主机目录为空，以避免数据丢失。
- YAML 中的锚点（anchors）在不同文件间可能无法正确传递；建议使用多个 `docker-compose.yml` 文件来管理配置。

### 卷管理相关问题
- 未命名的卷会默默地累积数据；建议使用命名卷。
- 绑定挂载时需要确保容器用户与主机用户具有相同的权限。
- `docker system prune` 命令无法删除命名卷；需要使用 `--volumes` 参数来指定要删除的卷。
- 已终止的容器的数据会一直保留，直到容器被删除。

### 资源泄漏问题
- 未使用的镜像会持续占用存储空间；应定期使用 `docker image prune` 删除不必要的镜像。
- 构建缓存可能会无限增长；可以使用 `docker builder prune` 来清理缓存。
- 停止的容器会占用磁盘空间；可以使用 `docker container prune` 或 `--rm` 命令删除容器。
- 多个 Compose 项目可能会创建大量网络；可以使用 `docker network prune` 来清理网络资源。

### 秘密信息与安全相关问题
- 使用 `ENV` 或 `COPY` 命令会将敏感信息永久保存在镜像历史记录中；建议使用专门的秘密管理工具或运行时环境变量来存储敏感信息。
- 使用 `--privileged` 选项会关闭所有安全限制；这种做法几乎不被推荐，应寻找更安全的解决方案。
- 来自未知注册表的镜像可能存在安全风险；请验证镜像来源。
- 构建参数会显示在镜像历史记录中，切勿将其用于存储敏感信息。

### 调试相关问题
- 输出代码 137 表示容器因内存不足（OOM）而终止，代码 139 表示发生段错误（segfault）——可以使用 `docker inspect --format='{{.State.ExitCode}}` 进行检查。
- 如果容器无法启动，请查看日志（即使容器已经失败）：`docker logs <container>`。
- 无 shell 的镜像无法直接访问文件；可以使用 `docker cp` 或调试工具来传输文件。
- 可以使用 `docker cp deadcontainer:/path ./local` 来查看已终止容器的文件系统内容。

## 相关技能
- 如果用户需要，可以使用 `clawhub install <slug>` 安装以下工具：
  - `devops`：部署管道
  - `linux`：主机系统管理
  - `server`：服务器管理

## 反馈建议
- 如果本文档对您有帮助，请给它打星（`clawhub star docker`）。
- 为了保持信息更新，请使用 `clawhub sync` 命令同步最新内容。