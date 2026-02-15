---
name: komodo
description: 管理 Komodo 的基础设施，包括服务器、Docker 部署、开发环境配置（stacks）以及构建流程（builds）。当用户询问服务器状态、容器管理、部署详情或任何与 Komodo 相关的基础设施问题时，可使用此功能。
---

# Komodo Skill

通过 Komodo Core API 管理服务器、Docker 容器、开发环境（stacks）、构建过程（builds）以及相关操作。

## 前提条件

设置环境变量：
- `KOMODO_ADDRESS` - Komodo Core 的 URL（例如：`https://komodo.example.com`）
- `KOMODO_API_KEY` - API 密钥（以 `K-` 开头）
- `KOMODO_API_SECRET` - API 密码（以 `S-` 开头）

## 快速参考

```bash
# Set env (or source from credentials file)
export KOMODO_ADDRESS="https://komodo.weird.cyou"
export KOMODO_API_KEY="K-..."
export KOMODO_API_SECRET="S-..."

# List resources
python scripts/komodo.py servers
python scripts/komodo.py deployments
python scripts/komodo.py stacks
python scripts/komodo.py builds
python scripts/komodo.py procedures
python scripts/komodo.py repos

# Server operations
python scripts/komodo.py server <name>
python scripts/komodo.py server-stats <name>

# Deployment operations
python scripts/komodo.py deployment <name>
python scripts/komodo.py deploy <name>
python scripts/komodo.py start <name>
python scripts/komodo.py stop <name>
python scripts/komodo.py restart <name>
python scripts/komodo.py logs <name> [lines]

# Stack operations
python scripts/komodo.py stack <name>
python scripts/komodo.py deploy-stack <name>
python scripts/komodo.py start-stack <name>
python scripts/komodo.py stop-stack <name>
python scripts/komodo.py restart-stack <name>
python scripts/komodo.py create-stack <name> <server> <compose.yml> [env_file]
python scripts/komodo.py delete-stack <name>
python scripts/komodo.py stack-logs <name> [service]

# Build operations
python scripts/komodo.py build <name>
python scripts/komodo.py run-build <name>

# Procedure operations
python scripts/komodo.py procedure <name>
python scripts/komodo.py run-procedure <name>
```

## 状态指示器

- 🟢 运行中/正常
- 🔴 停止
- ⚪ 未部署
- 🟡 不健康
- 🔄 重新启动中
- 🔨 正在构建
- ⏳ 待处理

## 直接 API 调用

对于 CLI 未支持的操作，可以使用 curl 进行调用：

```bash
# Read operation
curl -X POST "$KOMODO_ADDRESS/read/ListServers" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $KOMODO_API_KEY" \
  -H "X-Api-Secret: $KOMODO_API_SECRET" \
  -d '{}'

# Execute operation
curl -X POST "$KOMODO_ADDRESS/execute/Deploy" \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: $KOMODO_API_KEY" \
  -H "X-Api-Secret: $KOMODO_API_SECRET" \
  -d '{"deployment": "my-deployment"}'
```

## API 参考

可读取的 API 端点：
- `ListServers`、`ListDeployments`、`ListStacks`、`ListBuilds`、`ListProcedures`、`ListRepos`、`GetSystemStats`、`GetLog`

可执行的 API 端点：
- `Deploy`、`StartDeployment`、`StopDeployment`、`RestartDeployment`、`DeployStack`、`StartStack`、`StopStack`、`RestartStack`、`RunBuild`、`RunProcedure`

完整的 API 文档：https://komo.do/docs