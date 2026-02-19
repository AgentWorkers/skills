---
name: telnyx-network
description: 通过 Telnyx 和 WireGuard 基础设施实现私有网络连接以及公网 IP 的暴露。可以安全地连接节点，或将服务暴露到互联网上。
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["wg"],"env":["TELNYX_API_KEY"]},"primaryEnv":"TELNYX_API_KEY"}}
---

# Telnyx 网络

通过 Telnyx WireGuard 基础设施实现私有网络连接及公共 IP 的暴露。

## 必需条件

- **Telnyx API 密钥** — [免费获取](https://portal.telnyx.com/#/app/api-keys)
- 你的机器上已安装了 WireGuard

## 代理使用（OpenClaw）

WireGuard 需要提升权限才能创建网络接口。为了让 OpenClaw 自动管理你的网络，请运行以下命令 **一次**：

```bash
sudo ./setup-sudoers.sh
```

这会添加一条 `sudoers` 规则，允许在无需输入密码的情况下执行 WireGuard 命令。设置完成后，你的代理可以：

```bash
# Agent can now do all of this without password prompts:
./setup.sh --region ashburn-va
./join.sh --name "my-node" --apply
./register.sh --name "my-node"
./teardown.sh
```

**功能说明：**
- 在 `/etc/sudoers.d/wireguard-<username>` 文件中添加相应的条目
- 仅允许执行 `wg` 和 `wg-quick` 命令（而非全面的 sudo 权限）
- 可以随时通过 `sudo rm /etc/sudoers.d/wireguard-*` 删除该规则

**如果不进行此设置**，代理仍然可以创建网络并生成配置文件，但你需要手动运行 `sudo wg-quick up <config>` 来建立连接。

## 两种模式

### 网络模式（私有）
将多台机器连接到一个私有网络中。类似于 Tailscale，但基于 Telnyx 的基础设施。

```bash
./setup.sh --region ashburn-va
./join.sh --name "laptop"
./join.sh --name "server"  # run on server
# Now laptop and server can talk via 172.27.0.x
```

**费用：$10/月**（WireGuard 网关）

### 公开模式
获取一个公共 IP 并将服务暴露到互联网上。

```bash
./setup.sh --region ashburn-va
./join.sh --name "server" --apply
./add-public-ip.sh
./expose.sh 443
# Now https://64.16.x.x:443 reaches your server
```

**费用：$60/月**（WireGuard 网关 + 互联网网关）

## 命令

| 命令 | 说明 |
|---------|-------------|
| `sudo ./setup-sudoers.sh` | 为 WireGuard 启用免密码 sudo 访问（仅限代理使用，一次性设置） |
| `./setup.sh --region <code>` | 创建网络并配置 WireGuard 网关 |
| `./join.sh --name <name>` | 将该机器添加到网络中 |
| `./peers.sh` | 列出所有已连接的节点 |
| `./add-public-ip.sh` | 添加互联网网关（公共 IP） |
| `./expose.sh <port>` | 打开指定端口 |
| `./unexpose.sh <port>` | 关闭指定端口 |
| `./status.sh` | 显示完整状态 |
| `./teardown.sh` | 删除所有配置 |
| `./register.sh --name <name>` | 在网络注册表中注册节点 |
| `./discover.sh` | 发现网络中的其他节点 |
| `./unregister.sh --name <name>` | 从注册表中删除节点 |

## 节点发现

网络中的节点可以通过存储在 Telnyx 存储系统中的注册表来找到彼此。这使得 OpenClaw 实例能够自动发现并相互通信。

### 注册节点

加入网络后，请注册你的节点，以便其他节点能够找到你：

```bash
./register.sh --name "home-server"
```

### 发现其他节点

列出网络中所有已注册的节点：

```bash
./discover.sh

# Output:
# NAME            IP              HOSTNAME             REGISTERED
# home-server     172.27.0.1      macbook.local        2026-01-31 ✅
# work-laptop     172.27.0.2      thinkpad             2026-01-31 ✅

# JSON output for scripts
./discover.sh --json
```

### 从注册表中删除节点

从注册表中删除某个节点：

```bash
./unregister.sh --name "old-server"
```

### 使用场景：多 OpenClaw 之间的通信

```bash
# On OpenClaw A
./join.sh --name "openclaw-a" --apply
./register.sh --name "openclaw-a"

# On OpenClaw B
./join.sh --name "openclaw-b" --apply
./register.sh --name "openclaw-b"

# Either can now discover the other
./discover.sh
# → Shows both openclaw-a and openclaw-b with their mesh IPs

# Direct communication works via mesh IPs
curl http://172.27.0.2:18789/health  # OpenClaw B's gateway
```

以上内容涵盖了“主机与本地节点之间的会话”以及“OpenClaw 实例之间的直接通信”等使用场景。

## 地区设置

| 地区 | 代码 | 所在地 |
|--------|------|----------|
| 美国东部 | `ashburn-va` | 弗吉尼亚州阿什伯恩 |
| 美国中部 | `chicago-il` | 伊利诺伊州芝加哥 |
| 欧洲 | `frankfurt-de` | 德国法兰克福 |
| 欧洲 | `amsterdam-nl` | 荷兰阿姆斯特丹 |

查看完整地区列表：
```bash
./setup.sh --region help
```

## 安全性

### 被阻止的端口（需使用 `--force` 参数）
- 22（SSH）
- 23（Telnet）
- 3306（MySQL）
- 5432（PostgreSQL）
- 6379（Redis）
- 27017（MongoDB）

### 防火墙
只有明确暴露的端口才会允许通过 WireGuard 接口接收流量。其他端口默认被阻断。

## 配置

所有配置信息存储在 `config.json` 文件中：

```json
{
  "network_id": "...",
  "region": "ashburn-va",
  "wireguard_gateway": {
    "id": "...",
    "endpoint": "64.16.x.x:5107",
    "subnet": "172.27.0.1/24"
  },
  "internet_gateway": {
    "id": "...",
    "public_ip": "64.16.x.x"
  },
  "peers": [...],
  "exposed_ports": [443, 80]
}
```

## 使用场景

### 1. 连接 OpenClaw 实例
```bash
# On main server
./setup.sh --region ashburn-va
./join.sh --name "openclaw-main" --apply

# On secondary server
./join.sh --name "openclaw-backup" --apply

# Now they can communicate securely
```

### 2. 暴露 Webhook 端点
```bash
./add-public-ip.sh
./expose.sh 443
# Configure your webhook URL as https://64.16.x.x/webhook
```

### 3. 多地区网络
```bash
./setup.sh --region ashburn-va
./join.sh --name "us-east-server"

# Same network, different region gateway
./setup.sh --region frankfurt-de --name same-network
./join.sh --name "eu-server"
```

## 价格

| 组件 | 每月费用 |
|-----------|--------------|
| WireGuard 网关 | $10 |
| 互联网网关 | $50 |
| 节点连接 | 免费 |
| 流量传输 | 免费（测试阶段） |

## 故障排除

### “网关尚未配置完成”
设置完成后请等待 5-10 分钟，网关才会准备好。

### “连接被拒绝”
- 检查 WireGuard 是否正在运行：`sudo wg show`
- 检查端口是否已暴露：`./status.sh`
- 检查防火墙设置：`sudo iptables -L -n`

### “权限被拒绝”
WireGuard 需要 root 权限。请使用 `sudo` 运行相关命令，或使用 `--apply` 标志。

## 许可证

MIT 许可证