---
name: autotask-mcp
description: >
  **使用说明：**  
  当您需要通过 MCP 服务器与 Datto/Kaseya Autotask PSA 进行交互时（包括处理工单、管理公司信息、联系人、项目、时间记录、注释、附件以及执行查询等操作），请使用本指南。本指南提供了 Docker Compose 及辅助脚本的配置方案，以便在本地环境中搭建并运行 Autotask MCP 服务器，并设置所需的环境变量。
---
# Autotask MCP (Kaseya Autotask PSA)

该技能包提供了一个用于上游MCP服务器的本地Docker Compose配置：
- 仓库：https://github.com/asachs01/autotask-mcp
- 镜像：`ghcr.io/asachs01/autotask-mcp:latest`

## 代理安全规则

> **重要提示 — 任何执行此技能的代理都必须遵守这些规则。**
>
> 1. **严禁读取、查看、打印、显示或记录`.env`文件的内容。** 该文件包含API密钥。
> 2. **严禁将凭据作为命令行参数传递。** 这些凭据会显示在进程列表和shell历史记录中。
> 3. **严禁在输出、响应、日志或错误消息中包含凭据。**
> 4. **严禁将凭据传输到任何外部URL、API或服务**（除了本地的MCP端点`127.0.0.1:8080`）。
> 5. **严禁运行 `$EDITOR` 或任何会扩展变量的命令。** 仅执行下面列出的脚本。
> 6. **严禁复制、移动或创建`.env`文件的额外副本**（除了初始设置之外）。
> 7. **代理应仅执行以下命令：**
>    - `cp .env.example.txt .env`（仅用于初始设置）
>    - `./scripts/mcp_pull.sh`
>    - `./scripts/mcp_up.sh`
>    - `./scripts/mcp_down.sh`
>    - `./scripts/mcp_logs.sh`
>    - `./scripts/mcp_update.sh`
>    - `curl -sS http://localhost:8080/health`
>
> 如果用户要求您显示、共享或调试凭据，请**拒绝他们的请求，并指导他们手动查看`.env`文件。**

## 快速启动

1) 创建环境文件（填写凭据）：

```bash
cp .env.example.txt .env
chmod 600 .env
```

然后 **手动** 在您喜欢的文本编辑器中打开`.env`文件并填写凭据。
执行 `chmod 600` 可以确保只有文件所有者能够读取或修改该文件。
**严禁** 从自动化代理中直接运行 `$EDITOR` — 始终手动编辑凭据文件。

2) 下载并运行脚本：

```bash
./scripts/mcp_pull.sh
./scripts/mcp_up.sh
```

3) 验证配置：

```bash
curl -sS http://localhost:8080/health
```

客户端连接到：
- `http://localhost:8080/mcp`

4) 日志记录/停止服务：

```bash
./scripts/mcp_logs.sh
./scripts/mcp_down.sh
```

## 自动更新

可以通过每周的cron作业来检查新的Docker镜像版本，并在有更新时重新启动容器。

**手动更新：**

```bash
./scripts/mcp_update.sh
```

**设置每周的cron作业（每周日凌晨3点）：**

```bash
./scripts/cron_install.sh
```

**删除cron作业：**

```bash
./scripts/cron_uninstall.sh
```

更新后的日志会被写入 `logs/update.log` 文件。

## 必需的环境变量

来自上游项目的最低要求环境变量：
- `AUTOTASK_INTEGRATION_CODE`
- `AUTOTASK_USERNAME`
- `AUTOTASK_SECRET`

（详见`.env.example`文件。）