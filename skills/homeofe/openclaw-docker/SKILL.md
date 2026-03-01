---
name: openclaw-docker
description: "通过 OpenClaw 工具管理 Docker 容器和 Compose 项目"
---
# @elvatis_com/openclaw-docker

OpenClaw 是一个用于 Docker 容器操作和 Docker Compose 项目管理的插件。

## 主要功能

- 通过 Unix 套接字或 TCP 连接 Docker 守护进程
- 支持远程访问 Docker 守护进程时的 TLS 加密（可选）
- 提供读取和写入容器信息的功能
- 通过 `docker compose` CLI 集成 Docker Compose 命令
- 具有 `readOnly` 和 `allowedOperations` 等安全控制机制
- 命令执行超时时间可配置

## 前提条件

- 主机上已安装并运行 Docker Engine
- 环境变量 PATH 中包含 Docker CLI（执行 Docker Compose 命令时需要）
- 具有访问 Docker 套接字（`/var/run/docker.sock`）的权限，或能够通过 TCP 远程连接到 Docker 守护进程

## 安装

```bash
npm install @elvatis_com/openclaw-docker
```

## 安全注意事项

- 如果仅需要查看容器信息（如列表、日志、检查容器状态），请设置 `readOnly: true`。这样可以降低安全风险。
- 使用 TLS 时，请妥善保管相关的 PEM 证书文件，并仅配置受信任的证书路径。
- 该插件会在您指定的 `composeProjects` 目录中执行 `docker compose` 命令；请仅配置受信任的项目路径。
- 尽可能在一个具有最小权限的环境中运行该插件。

## 配置选项

### 使用本地 Unix 套接字（默认设置）

```json
{
  "plugins": {
    "openclaw-docker": {
      "socketPath": "/var/run/docker.sock",
      "readOnly": false,
      "allowedOperations": ["ps", "logs", "inspect", "start", "stop", "restart", "compose_up", "compose_down", "compose_ps"],
      "composeProjects": [
        { "name": "aegis", "path": "/opt/aegis" }
      ],
      "timeoutMs": 15000
    }
  }
}
```

### 远程 Docker 守护进程（支持 TLS）

```json
{
  "plugins": {
    "openclaw-docker": {
      "host": "10.0.0.20",
      "port": 2376,
      "tls": {
        "caPath": "/etc/openclaw/docker/ca.pem",
        "certPath": "/etc/openclaw/docker/cert.pem",
        "keyPath": "/etc/openclaw/docker/key.pem",
        "rejectUnauthorized": true
      },
      "readOnly": true,
      "composeProjects": []
    }
  }
}
```

## 提供的工具

- `docker_ps`：列出所有正在运行的容器
- `docker_logs`：查看容器日志
- `docker_inspect`：检查容器详细信息
- `docker_start`：启动容器
- `docker_stop`：停止容器
- `docker_restart`：重启容器
- `docker_compose_up`：启动 Docker Compose 项目
- `docker_compose_down`：停止 Docker Compose 项目
- `docker_compose_ps`：列出 Docker Compose 项目的运行状态

## 使用示例

- “列出所有正在运行的容器”
- “显示 api-gateway 容器的最后 200 行日志”
- “检查 redis 容器的状态”
- “重启 identity-service 服务”
- “启动 aegis-compose 项目”
- “显示 aegis-compose 项目的运行状态”

## 安全性与权限控制

- 设置 `readOnly: true` 时，仅允许执行 `ps`、`logs`、`inspect` 和 `compose_ps` 命令
- `allowedOperations` 可用于限制可执行的工具
- Docker Compose 操作仅限于 `composeProjects` 中定义的项目
- 命令执行时会受到超时保护（通过 `timeoutMs` 参数设置）

## 开发信息

```bash
npm install
npm run build
npm test
```

## 许可证

MIT 许可证