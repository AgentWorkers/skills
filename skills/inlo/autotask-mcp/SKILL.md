---
name: autotask-mcp
description: **使用说明：**  
当您需要通过 MCP 服务器与 Datto/Kaseya Autotask PSA 进行交互时（包括处理工单、公司信息、联系人信息、项目信息、时间记录、备注、附件以及执行查询等操作），请使用本指南。本指南提供了 Docker Compose 及辅助脚本，用于在本地部署并运行 Autotask MCP 服务器，并配置所需的环境变量。
---

# Autotask MCP (Kaseya Autotask PSA)

该技能包包含了一个用于上游MCP服务器的本地Docker Compose配置：
- 仓库地址：https://github.com/asachs01/autotask-mcp
- 镜像：`ghcr.io/asachs01/autotask-mcp:latest`

## 快速启动

1) 创建环境文件（填写凭据）：

```bash
cd /Users/stephan/.openclaw/workspace/skills/autotask-mcp
cp .env.example .env
$EDITOR .env
```

2) 拉取并运行镜像：

```bash
./scripts/mcp_pull.sh
./scripts/mcp_up.sh
```

3) 验证配置是否正确：

```bash
curl -sS http://localhost:8080/health
```

客户端连接地址：
- `http://localhost:8080/mcp`

4) 查看日志/停止服务：

```bash
./scripts/mcp_logs.sh
./scripts/mcp_down.sh
```

## 必需的环境变量

来自上游项目的最低要求环境变量：
- `AUTOTASK_INTEGRATION_CODE`
- `AUTOTASK_USERNAME`
- `AUTOTASK_SECRET`

（详情请参见`.env.example`文件。）