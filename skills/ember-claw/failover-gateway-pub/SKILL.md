---
name: failover-gateway
version: 1.0.0
description: 为 OpenClaw 设置一个主动-被动故障转移网关：部署一个备用节点，当主节点发生故障时该备用节点会自动接管服务，主节点恢复后备用节点会自动降级回备用状态。该方案包括健康检查脚本、systemd 服务配置、通道分割策略以及详细的部署指南。适用于需要高可用性、灾难恢复或冗余功能的 OpenClaw 实例场景。
---
# OpenClaw 的故障转移网关

部署一个备用 OpenClaw 网关，当主节点发生故障时，该备用网关会自动接管服务。采用主动-被动设计模式，支持自动升级和降级功能。

## 功能特点

- **30 秒内完成故障转移**：健康监测器检测到主节点故障后，立即升级备用节点。
- **自动恢复**：当主节点恢复正常后，备用节点会自动降级。
- **避免“脑裂”现象**：主节点和备用节点使用不同的通信渠道，确保消息不会重复传输。
- **工作区同步**：备用节点在升级时会拉取最新的工作区数据。
- **每月成本：12 美元**：运行在配置简单的虚拟专用服务器（VPS）上。

## 架构示意图

```
PRIMARY (your main VPS)          STANDBY (failover VPS)
├─ Full stack (all channels)     ├─ Single channel only (e.g., Discord DM)
├─ All cron jobs                 ├─ No crons (recovery mode)
├─ Gateway active ✅              ├─ Gateway stopped 💤
└─ Pushes workspace to git       └─ Health monitor watches primary
                                      │
                                      ├─ Primary healthy → sleep
                                      ├─ Primary down 30s → PROMOTE
                                      └─ Primary back → DEMOTE
```

**关键原则**：**将通信渠道分配给主节点和备用节点**。不要让它们共享相同的渠道或凭据，确保每个节点独占自己的通信渠道。这样可以完全避免“脑裂”现象（即两个节点同时接收相同的数据）。

### 通信渠道配置示例

| 配置方式 | 主节点 | 备用节点 |
|---------|---------|
| RC + Discord | RocketChat（全功能） | 仅使用 Discord 私信 |
| Discord + Telegram | Discord（全功能） | 仅使用 Telegram 私信 |
| Slack + Discord | Slack（全功能） | 仅使用 Discord 私信 |

主节点负责处理所有业务逻辑，备用节点仅保持可访问状态，以备紧急情况下使用。

## 先决条件

- 一个运行在 VPS 上的主 OpenClaw 实例。
- 一个用于部署备用节点的 VPS（每月费用 6–12 美元，支持任意云服务提供商）。
- [Tailscale](https://tailscale.com) 网络服务（或类似的 VPN/私有网络）。
- 用于同步工作区数据的 Git 仓库（如 GitHub、GitLab 等）。
- 一个与主节点不同的通信渠道（用于备用节点）。

## 部署步骤

### 第 1 阶段：准备备用 VPS

任何配置简单的 VPS 都可以。推荐配置：2GB 内存，Ubuntu 24.04 操作系统。

```bash
# Harden the box
ufw allow 22/tcp
ufw enable
apt install -y fail2ban unattended-upgrades

# Create openclaw user
adduser openclaw --disabled-password
usermod -aG sudo openclaw
# Copy your SSH key to openclaw user

# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up --hostname=your-failover-name
```

### 第 2 阶段：安装 OpenClaw

```bash
# As openclaw user
curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
source ~/.bashrc
nvm install --lts
npm install -g openclaw

# Clone workspace
git clone <your-workspace-repo> ~/.openclaw/workspace
```

### 第 3 阶段：配置故障转移

在备用节点上创建一个最小化的 OpenClaw 配置文件，仅启用备用节点所需的通信渠道：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-opus-4-6",
        "fallbacks": ["anthropic/claude-sonnet-4-5"]
      },
      "workspace": "/home/openclaw/.openclaw/workspace"
    },
    "list": [{ "id": "main", "default": true }]
  },
  "channels": {
    "discord": {
      "enabled": true,
      "token": "<YOUR_DISCORD_BOT_TOKEN>",
      "dm": {
        "policy": "allowlist",
        "allowFrom": ["<YOUR_DISCORD_USER_ID>"]
      }
    }
  },
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "tailnet"
  }
}
```

**注意**：在主节点上禁用该通信渠道，以避免冲突。

测试其是否正常工作：运行 `openclaw gateway run` 命令，确认机器人能够正常连接并响应，然后停止该服务。

### 第 4 阶段：部署健康监测器

将 `scripts/health-monitor.sh` 脚本复制到备用节点：

```bash
sudo cp health-monitor.sh /usr/local/bin/openclaw-health-monitor.sh
sudo chmod +x /usr/local/bin/openclaw-health-monitor.sh
```

修改脚本中的配置变量：
- `PRIMARY_IP`：主节点的 Tailscale IP 地址。
- `PRIMARY_PORT`：主节点的网关端口（默认值：18789）。
- `SECRETS_HOST`（可选）：用于在备用节点升级时同步机密信息的服务器地址。

创建 systemd 服务文件：
- `/etc/systemd/system/openclaw-health-monitor.service`
```ini
[Unit]
Description=OpenClaw Failover Health Monitor
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/openclaw-health-monitor.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

- `/etc/systemd/system/openclaw.service`
```ini
[Unit]
Description=OpenClaw Gateway (Failover)
After=network-online.target tailscaled.service
Wants=network-online.target

[Service]
Type=simple
User=openclaw
Group=openclaw
WorkingDirectory=/home/openclaw/.openclaw/workspace
ExecStart=/usr/bin/openclaw gateway run
Restart=on-failure
RestartSec=5
Environment=HOME=/home/openclaw
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

启用健康监测器服务（但不要启用网关服务，因为网关服务会在主节点升级时自动启动）：

```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw-health-monitor
sudo systemctl start openclaw-health-monitor
# Do NOT enable openclaw.service — the monitor controls it
```

### 第 5 阶段：在主节点上禁用备用节点的通信渠道

这是非常重要的步骤：从主节点的配置文件中删除或禁用备用节点的通信渠道。

### 第 6 阶段：进行测试

```bash
# On primary — simulate failure
sudo systemctl stop openclaw-gateway  # or kill the process

# Watch the standby logs
journalctl -u openclaw-health-monitor -f

# Expected: 3 failed checks → PROMOTE → gateway starts → standby channel live

# On primary — recover
sudo systemctl start openclaw-gateway

# Expected: standby detects primary → DEMOTE → gateway stops
```

## 故障转移流程

| 时间 | 事件 |
|------|-------|
| 0 秒 | 主节点故障 |
| 10 秒 | 第一次健康检查失败 |
| 20 秒 | 第二次检查失败 |
| 30 秒 | 第三次检查失败 → 备用节点升级 |
| 35 秒 | 备用节点拉取最新工作区数据并同步机密信息 |
| 40 秒 | 备用节点的网关服务启动 |
| 45 秒 | 备用节点的通信渠道开始生效 |
| 约 60 秒 | 服务恢复正常可用 |

## 边缘情况处理

- **主节点故障**：备用节点会在 30–60 秒内接管服务。
- **主节点和备用节点同时故障**：此时系统将处于离线状态（可以考虑添加第三个节点）。
- **网络中断**：备用节点可能在主节点仍在运行时尝试升级，但由于使用不同的通信渠道，不会出现冲突。
- **备用节点重启**：健康监测器会自动重启并继续执行监控任务。
- **主节点状态不稳定**：健康监测器会自动处理升级/降级操作，建议适当调整故障检测阈值（FAIL_THRESHOLD）。

## 故障恢复

系统具备自动恢复能力：
- 当主节点恢复正常后，健康监测器会检测到主节点的状态。
- 备用节点的网关服务会停止运行。
- 主节点会重新接管所有通信渠道。
- 备用节点会恢复监控任务。

无需人工干预。

## 成本估算

| 组件 | 成本 |
|---------|------|
| VPS（2GB 内存） | 每月 6–12 美元 |
| Tailscale | 免费（个人用户） |
| Git 仓库 | 免费 |
| **总计**：每月 6–12 美元 |

## 使用建议

- **每月进行一次测试**：故意关闭主节点，确认故障转移功能是否正常。
- **保持备用节点的配置简单**：避免使用不必要的 cron 任务或额外通信渠道，因为备用节点仅用于恢复。
- **频繁推送代码**：确保备用节点的工作区数据始终是最新的。
- **使用 Tailscale**：它简化了跨 VPS 的网络连接，无需配置防火墙规则或端口转发。
- **为不同节点配置不同的机器人令牌**：如果在主节点和备用节点上都使用 Discord，需要为每个节点创建独立的机器人账户；使用相同的令牌可能导致连接优先级问题。
- **定期检查监控器**：定期运行 `journalctl -u openclaw-health-monitor` 命令，确保监控器正常运行。