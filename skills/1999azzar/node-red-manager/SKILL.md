---
name: node-red-manager
description: 通过 Admin API 或 CLI 管理 Node-RED 实例。实现流程的自动化部署、节点的安装以及问题的排查与解决。适用于用户需要“构建自动化流程”、“连接设备”或“修复 Node-RED 问题”的场景。
---

# Node-RED Manager

## 设置
1. 将 `.env.example` 文件复制到 `.env` 文件中。
2. 在 `.env` 文件中设置 `NODE_RED_URL`、`NODE_RED_USERNAME` 和 `NODE_RED_PASSWORD`。
3. 脚本在首次运行时会自动处理依赖项的下载和安装。

## 基础设施
- **部署位置**：`deployments/node-red`
- **数据卷**：`deployments/node-red/data`
- **Docker 服务**：`mema-node-red`
- **URL**：`https://flow.glassgallery.my.id`

## 使用方法

### 流管理

```bash
# List all flows
scripts/nr list-flows

# Get specific flow by ID
scripts/nr get-flow <flow-id>

# Deploy flows from file
scripts/nr deploy --file assets/flows/watchdog.json

# Update specific flow
scripts/nr update-flow <flow-id> --file updated-flow.json

# Delete flow
scripts/nr delete-flow <flow-id>

# Get flow runtime state
scripts/nr get-flow-state

# Set flow runtime state
scripts/nr set-flow-state --file state.json
```

### 备份与恢复

```bash
# Backup all flows to file
scripts/nr backup
scripts/nr backup --output my-backup.json

# Restore flows from backup
scripts/nr restore node-red-backup-20260210_120000.json
```

### 节点管理

```bash
# List installed nodes
scripts/nr list-nodes

# Install node module
scripts/nr install-node node-red-contrib-http-request

# Get node information
scripts/nr get-node node-red-contrib-http-request

# Enable/disable node
scripts/nr enable-node node-red-contrib-http-request
scripts/nr disable-node node-red-contrib-http-request

# Remove node
scripts/nr remove-node node-red-contrib-http-request
```

### 运行时信息

```bash
# Get runtime settings
scripts/nr get-settings

# Get runtime diagnostics
scripts/nr get-diagnostics
```

### 上下文管理

```bash
# Get context value
scripts/nr get-context flow my-key
scripts/nr get-context global shared-data

# Set context value
scripts/nr set-context flow my-key '"value"'
scripts/nr set-context global counter '42'
scripts/nr set-context global config '{"key": "value"}'
```

## Docker 操作

```bash
# Restart Node-RED
cd deployments/node-red && docker compose restart

# View logs
docker logs mema-node-red --tail 100

# Follow logs
docker logs -f mema-node-red
```

## 环境变量
- `NODE_RED_URL`：Node-RED API 端点（默认值：`http://localhost:1880`）
- `NODE_RED_USERNAME`：管理员用户名
- `NODE_RED_PASSWORD`：管理员密码

为了向后兼容，仍然支持旧的变量名称（`NR_URL`、`NR_USER`、`NR_PASS`）。

## API 参考
有关完整的管理员 API 端点文档，请参阅 `references/admin-api.md`。