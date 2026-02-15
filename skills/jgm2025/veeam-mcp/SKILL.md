---
name: veeam-mcp
description: "通过运行在 Docker 中的 MCP 服务器，可以查询 Veeam Backup & Replication 和 Veeam ONE 的状态。该服务器提供了智能的备份监控、作业分析、容量规划以及基础设施健康检查功能。"
---

# Veeam Intelligence MCP 技能

通过运行在 Docker 中的 MCP（Model Context Protocol）服务器，与 Veeam Backup & Replication (VBR) 和 Veeam ONE 进行交互。

## 自然语言命令

当用户提出以下问题时：
- **“昨晚哪些备份任务失败了？”**
- **“显示所有虚拟机的备份状态”**
- **“我的备份存储库容量是多少？”**
- **“哪些虚拟机最近没有进行备份？”**
- **“查看 Veeam ONE 的警报”**
- **“分析备份性能趋势”**

## 功能概述

该技能通过运行在 Docker 中的 Veeam Intelligence MCP 服务器，提供对以下功能的自然语言访问：

**Veeam Backup & Replication (VBR):**
- 备份任务的状态和历史记录
- 备份存储库的容量和健康状况
- 虚拟机的备份状态
- 任务配置详情
- 失败任务的分析

**Veeam ONE:**
- 基础设施监控
- 性能分析
- 警报管理
- 容量规划
- 趋势分析

## 先决条件

- 已安装并运行 Docker
- 拥有有效的 Veeam Backup & Replication 和/或 Veeam ONE 许可证（非社区版）
- 在 Veeam 服务器上启用了 Veeam Intelligence（高级模式所需）
- 具有 Veeam 服务器的管理员权限

## 安装

### 1. 获取 Veeam Intelligence MCP 服务器

Veeam Intelligence MCP 服务器目前处于 **测试阶段**（beta）。

**获取访问权限的方法：**
- 直接联系 Veeam 或您的 Veeam 客户服务代表
- 访问官方 Veeam 社区论坛
- 关注 Veeam 的官方渠道以获取测试计划公告

获取 MCP 服务器包后，构建 Docker 镜像：

```bash
cd /path/to/veeam-mcp-server
docker build -t veeam-intelligence-mcp-server .
```

### 2. 安装此技能

```bash
clawhub install veeam-mcp
```

## 配置

### 创建凭据文件

创建 `~/.veeam-mcp-creds.json` 文件：

```json
{
  "vbr": {
    "url": "https://veeam-server.yourdomain.com:443/",
    "username": ".\\administrator",
    "password": "your_secure_password"
  },
  "vone": {
    "url": "https://veeam-one.yourdomain.com:1239/",
    "username": ".\\administrator",
    "password": "your_secure_password"
  }
}
```

**重要提示：** 保护凭据文件的安全：
```bash
chmod 600 ~/.veeam-mcp-creds.json
```

### 用户名格式

- **本地账户**：使用 `".\\username"` 格式
- **域账户**：使用 `"DOMAIN\\username"` 或 `"username@domain.com"`
- **JSON 中的反斜杠转义**：使用 `".\\"` 而不是 `".\\\\"`

### 启用 Veeam Intelligence

为了进行实时数据查询（高级模式），需要在 Veeam 服务器上启用 Veeam Intelligence：

**Veeam Backup & Replication:**
1. 打开 Veeam B&R 控制台
2. 转到 **选项** → **Veeam Intelligence 设置**
3. 启用 AI 助手

**Veeam ONE:**
1. 打开 Veeam ONE 控制台
2. 查找 **Veeam Intelligence** 设置
3. 启用该功能

如果没有启用此功能，查询将仅返回文档信息（基本模式）。

## 使用方法

### 自然语言交互（使用 OpenClaw）

只需自然地提出问题即可：

```
"What Veeam backup jobs failed yesterday?"
"Show me backup repository capacity"
"Check Veeam ONE alerts"
"Which VMs haven't been backed up this week?"
```

### 命令行脚本

```bash
# Query VBR
./scripts/query-veeam.sh vbr "What backup jobs ran in the last 24 hours?"

# Query Veeam ONE
./scripts/query-veeam.sh vone "Show current alerts"

# Test connections
./scripts/test-connection.sh vbr
./scripts/test-connection.sh vone

# List available MCP tools
./scripts/list-tools.sh vbr
```

## 工作原理

1. **Docker 容器**：MCP 服务器在隔离的容器中运行
2. **标准输入/输出（STDIO）通信**：通过标准输入/输出进行数据交换
3. **凭据传递**：从凭据文件安全地传递环境变量
4. **自然语言处理**：Veeam Intelligence 使用人工智能处理查询请求

## 故障排除

### 连接失败

```bash
# Check credentials file
cat ~/.veeam-mcp-creds.json | jq .

# Test Docker image
docker run -i --rm veeam-intelligence-mcp-server

# Manual connection test
echo '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}},"id":1}' | \
  docker run -i --rm \
    -e PRODUCT_NAME=vbr \
    -e WEB_URL=https://your-server:443/ \
    -e ADMIN_USERNAME='.\administrator' \
    -e ADMIN_PASSWORD='yourpassword' \
    -e ACCEPT_SELF_SIGNED_CERT=true \
    veeam-intelligence-mcp-server
```

### 基本模式（仅提供文档信息）

如果响应显示“处于基本模式”，请在您的服务器上启用 Veeam Intelligence。

### 用户名格式问题

- 尝试使用 `.\\username`（本地账户）
- 尝试使用 `DOMAIN\\username`（域账户）
- 确保 JSON 中的反斜杠使用单斜杠 `\"`

## 安全注意事项

- 凭据存储在本地文件 `~/.veeam-mcp-creds.json` 中（权限设置为 600）
- Docker 容器以非 root 用户身份运行
- 使用自签名证书进行 HTTPS 连接
- 凭据不会被记录在日志或命令历史记录中
- MCP 服务器仅通过标准输入/输出（stdin/stdout）进行通信

## 参考资料

- Veeam Intelligence MCP 服务器：请联系 Veeam 以获取测试权限
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Veeam Intelligence 文档](https://helpcenter.veeam.com/)

## 许可证

此技能按“原样”提供。Veeam Intelligence MCP 服务器需要单独购买许可证。

---

**需要帮助？** 请在 GitHub 上提交问题或在 OpenClaw 的 Discord 频道中咨询。