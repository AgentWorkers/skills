# KKClaw 服务器

这是一个针对 Ubuntu/Raspbian 系统优化的 OpenClaw 客户端，可作为远程服务器使用。

## 概述

KKClaw 服务器是专为 Ubuntu 和 Raspbian 服务器设计的无图形界面版本。它无需图形界面即可运行，非常适合用于 Raspberry Pi 或云服务器环境。

## 特点

### 1. 心跳机制
- 心跳间隔可配置（默认：30 秒）
- 向网关报告状态信息
- 监控内存使用情况和运行时间
- 自动检测连接状态

### 2. 自动重连
- 采用指数级退避策略进行重连
- 可配置最大重试次数
- 持续监控连接状态
- 支持优雅的故障降级机制

### 3. 自动恢复
- 自动恢复会话状态
- 断开连接后恢复消息队列
- 故障时自动切换到之前的模型
- 设定最大重启尝试次数

### 4. 消息队列管理
- 断开连接时将消息放入队列
- 支持带退避机制的自动重试
- 设置队列大小限制
- 采用 FIFO 处理方式

### 5. 模型切换
- 不需要重启即可切换模型
- 支持备用模型
- 故障时自动切换到备用模型
- 提供超时保护机制

## 快速入门

```bash
# Initialize config
kkclaw-server init

# Start server
kkclaw-server start

# Check status
kkclaw-server status

# Switch model
kkclaw-server model minimax-portal/MiniMax-M2.5
```

## 配置

编辑 `~/.kkclaw/config.json` 文件：

```json
{
  "gateway": {
    "url": "http://your-gateway:18789",
    "apiKey": "your-api-key"
  },
  "heartbeat": {
    "enabled": true,
    "interval": 30000
  },
  "reconnect": {
    "enabled": true,
    "maxRetries": 10,
    "baseDelay": 1000
  },
  "recovery": {
    "enabled": true,
    "maxRestarts": 5
  },
  "queue": {
    "maxSize": 100,
    "maxRetries": 3
  },
  "models": {
    "default": "claude-opus-4-6",
    "fallback": "minimax-portal/MiniMax-M2.5"
  }
}
```

## 使用 systemd 服务（Raspbian/Ubuntu）

创建 `/etc/systemd/system/kkclaw.service` 文件：

```ini
[Unit]
Description=KKClaw Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/kkclaw
ExecStart=/usr/bin/node /home/pi/kkclaw/main.js start
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

然后执行以下命令以启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable kkclaw
sudo systemctl start kkclaw
```

## 特点详细说明

### 心跳机制
- 定期向网关发送心跳信号
- 报告状态、当前使用的模型、队列长度、内存使用情况和运行时间
- 可及时检测到连接问题

### 自动重连
- 采用指数级退避策略（1 秒、2 秒、4 秒、8 秒……最多 60 秒）
- 默认最多重试 10 次
- 支持手动重新连接

### 自动恢复
- 清除失败的会话状态
- 恢复队列中的消息
- 故障时自动切换到之前的模型

### 消息队列管理
- 断开连接时将消息放入队列
- 支持带退避机制的自动重试
- 超过最大重试次数后删除失败的消息

### 模型切换
- 不需要重启即可切换模型
- 支持超时保护（默认超时时间为 30 秒）
- 故障时自动切换到默认模型

## 命令行接口（CLI）命令

| 命令 | 描述 |
|---------|-------------|
| `init` | 创建默认配置 |
| `start` | 启动服务器 |
| `status` | 显示当前状态 |
| `connect` | 手动连接 |
| `model <name>` | 切换模型 |
| `queue` | 显示队列信息 |

## 开发者

Glitch（OpenClaw 项目的开发者）