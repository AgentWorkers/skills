---
name: uptime-kuma
description: 与 Uptime Kuma 监控服务器进行交互。可用于查看监控状态、添加/删除监控项、暂停/恢复检查、查看心跳历史记录。当提到 Uptime Kuma、服务器监控、运行时间检查或服务健康监控时，该功能会自动触发。
---

# Uptime Kuma 技能

通过基于 Socket.IO API 的 CLI 包装器来管理 Uptime Kuma 监控器。

## 设置

需要 `uptime-kuma-api` Python 包：
```bash
pip install uptime-kuma-api
```

环境变量（在 shell 或 Clawdbot 配置中设置）：
- `UPTIME_KUMA_URL` - 服务器地址（例如：`http://localhost:3001`）
- `UPTIME_KUMA_USERNAME` - 登录用户名
- `UPTIME_KUMA_PASSWORD` - 登录密码

## 使用方法

脚本位置：`scripts/kuma.py`

### 命令

```bash
# Overall status summary
python scripts/kuma.py status

# List all monitors
python scripts/kuma.py list
python scripts/kuma.py list --json

# Get monitor details
python scripts/kuma.py get <id>

# Add monitors
python scripts/kuma.py add --name "My Site" --type http --url https://example.com
python scripts/kuma.py add --name "Server Ping" --type ping --hostname 192.168.1.1
python scripts/kuma.py add --name "SSH Port" --type port --hostname server.local --port 22

# Pause/resume monitors
python scripts/kuma.py pause <id>
python scripts/kuma.py resume <id>

# Delete monitor
python scripts/kuma.py delete <id>

# View heartbeat history
python scripts/kuma.py heartbeats <id> --hours 24

# List notification channels
python scripts/kuma.py notifications
```

### 监控类型

- `http` - HTTP/HTTPS 端点
- `ping` - ICMP ping 检测
- `port` - TCP 端口检查
- `keyword` - 基于 HTTP 和关键词的搜索
- `dns` - DNS 解析
- `docker` - Docker 容器监控
- `push` - 基于推送的被动监控
- `mysql`, `postgres`, `mongodb`, `redis` - 数据库检查
- `mqtt` - MQTT 代理监控
- `group` - 监控组

### 常见工作流程

**检查哪些服务处于关闭状态：**
```bash
python scripts/kuma.py status
python scripts/kuma.py list  # Look for 🔴
```

**添加一个每 30 秒执行一次的 HTTP 监控：**
```bash
python scripts/kuma.py add --name "API Health" --type http --url https://api.example.com/health --interval 30
```

**维护模式（暂停所有监控）：**
```bash
for id in $(python scripts/kuma.py list --json | jq -r '.[].id'); do
  python scripts/kuma.py pause $id
done
```