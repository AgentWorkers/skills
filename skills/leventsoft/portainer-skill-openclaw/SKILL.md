---
name: portainer
description: **Portainer CE环境及堆栈的全面管理工具**  
该工具支持列出所有环境、管理Docker Compose/Swarm堆栈，并通过代理执行原始Docker命令。适用于用户需要部署应用程序、检查容器状态或管理Portainer内部网络的情况。使用该工具前，必须在OpenClaw中配置Portainer API密钥。
---

# Portainer Manager 技能

通过 Portainer CE 的 HTTP API 管理您的 Docker 基础设施。

## 设置

将您的 Portainer API 密钥添加到 OpenClaw 的配置文件中：

```bash
openclaw config set portainer.apiKey "your_token_here"
```

## 功能

*   `list_environments()`: 获取所有 Portainer 环境（端点）。
*   `list_stacks(environment_id)`: 列出所有堆栈。可选：按环境 ID 过滤。
*   `inspect_stack(stack_id)`: 返回特定堆栈的完整 JSON 详细信息。
*   `deploy_stack(stack_name, compose_content, environment_id)`: 根据提供的 Compose 配置文件创建一个新的 Docker 堆栈。
*   `remove_stack(stack_id)`: 通过 ID 删除堆栈。
*   `execute_docker_command(environment_id, path, method, payload)`: 高级功能。通过 Portainer 代理原始的 Docker API 请求（例如 `/containers/json`）。