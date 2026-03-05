---
name: mac-mini-server
description: Set up OpenClaw on Mac Mini as always-on AI server — hardware recommendations, macOS config, Docker Desktop, launchd auto-start, Tailscale remote access, and cost comparison vs VPS. Use when deploying OpenClaw on Mac Mini for 24/7 personal AI.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: macOS, Homebrew
metadata: {"openclaw": {"emoji": "\ud83d\udda5\ufe0f", "homepage": "https://www.agxntsix.ai"}}
---

# 🖥️ Mac Mini 服务器

本指南详细介绍了如何在 Mac Mini 上运行 OpenClaw，将其作为始终在线的 AI 服务器使用，涵盖从硬件选择到监控的整个过程。

---

## 1. 硬件推荐

### Mac Mini M4（2024 年款）—— 基本配置：$499

| 规格 | 基本配置 | 升级配置 |
|------|------|---------|
| CPU | 10 核 | 10 核 |
| GPU | 10 核 | 10 核 |
| 内存 | 16GB | 32GB（额外费用 $200） |
| 存储 | 256GB | 512GB（额外费用 $200） |

**最适合：** 个人助手、小型团队或仅使用云 API 的场景。
**建议：** 升级至 32GB 内存（总费用 $699）—— 这对于运行 Docker 及未来的本地模型非常有用。

### Mac Mini M4 Pro — 基本配置：$1,399

| 规格 | 基本配置 | 升级配置 |
|------|------|---------|
| CPU | 12 核 | 14 核 |
| GPU | 16 核 | 20 核 |
| 内存 | 24GB | 48GB（额外费用 $200）/ 64GB（额外费用 $400） |
| 存储 | 512GB | 1TB（额外费用 $200） |

**最适合：** 本地模型推理（如 Ollama）、多客户端或高负载场景。
**建议：** 配备 48GB 内存（总费用 $1,599），以便在本地运行 70 亿到 130 亿参数的模型。

### 应该如何选择？

| 使用场景 | 推荐配置 | 原因 |
|----------|------|-----|
| 仅使用云 API（如 Claude、GPT） | M4 32GB | 性能足够，性价比高 |
| 本地与云混合使用 | M4 Pro 48GB | 可同时运行 Ollama 和 OpenClaw |
| 多客户端服务器 | M4 Pro 64GB | 有足够的资源支持多个代理 |
| 预算有限 | M4 16GB | 单用户使用也足够 |

---

## 2. macOS 初始设置

### 禁用睡眠和节能设置

```bash
# Prevent sleep entirely
sudo pmset -a sleep 0
sudo pmset -a disksleep 0
sudo pmset -a displaysleep 0

# Restart after power failure
sudo pmset -a autorestart 1

# Disable hibernation
sudo pmset -a hibernatemode 0

# Verify settings
pmset -g
```

**系统设置路径：** 系统设置 → 能源设置 → 将所有选项设置为“从不”。

### 启用自动登录

1. 系统设置 → 用户与组 → 自动登录 → 选择你的用户
2. 系统设置 → 锁屏 → 禁用“需要密码”

> ⚠️ 请仅在物理安全的环境中执行此操作。Mac Mini 应放置在安全的位置。

### 禁用自动更新重启

```bash
# Prevent auto-restart for updates
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticallyInstallMacOSUpdates -bool false
```

建议根据需要手动安排更新。

### 启用远程访问

```bash
# Enable SSH
sudo systemsetup -setremotelogin on

# Enable Screen Sharing (optional)
sudo defaults write /var/db/launchd.db/com.apple.launchd/overrides.plist com.apple.screensharing -dict Disabled -bool false
sudo launchctl load -w /System/Library/LaunchDaemons/com.apple.screensharing.plist
```

---

## 3. 安装 Homebrew 和 Docker Desktop

### 安装 Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 安装 Docker Desktop

```bash
brew install --cask docker

# Launch Docker Desktop
open -a Docker

# Wait for Docker to start, then verify
docker --version
docker compose version
```

**Docker Desktop 设置：**
- 资源 → CPU：为 macOS 留出 2 个核心，其余分配给 Docker
- 资源 → 内存：为 macOS 留出 4GB，其余分配给 Docker
- 通用 → 登录时启动 Docker Desktop：✅

### 安装必备工具

```bash
brew install git node pnpm tailscale jq htop
```

---

## 4. OpenClaw 和 Docker Compose 的配置

### 克隆并构建项目

```bash
cd ~
git clone https://github.com/openclaw/openclaw.git
cd openclaw

# Install dependencies and build
pnpm install
pnpm build

# Build Docker image
docker build -t openclaw:latest .
```

### 配置 OpenClaw

```bash
mkdir -p ~/.openclaw
cp openclaw.example.json ~/.openclaw/openclaw.json
nano ~/.openclaw/openclaw.json
```

### docker-compose.yml 文件配置

```yaml
version: "3.8"
services:
  openclaw-gateway:
    image: openclaw:latest
    container_name: openclaw-gateway
    restart: unless-stopped
    volumes:
      - ~/.openclaw:/home/node/.openclaw
      - ./:/host/openclaw:rw
      - /var/run/docker.sock:/var/run/docker.sock
      - ~/.ssh:/home/node/.ssh:ro
    ports:
      - "127.0.0.1:3000:3000"
    environment:
      - NODE_ENV=production
```

> ⚠️ **务必** 在端口前加上 `127.0.0.1:` 前缀。切勿将端口暴露到 `0.0.0.0`。

### 启动服务

```bash
docker compose up -d
docker compose logs -f  # verify startup
```

---

## 5. 设置 launchd 服务（开机自启动）

创建 `~/Library/LaunchAgents/com.openclaw.gateway.plist` 文件：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.gateway</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/docker</string>
        <string>compose</string>
        <string>-f</string>
        <string>/Users/YOUR_USER/openclaw/docker-compose.yml</string>
        <string>up</string>
        <string>-d</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>StandardOutPath</key>
    <string>/tmp/openclaw-launchd.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/openclaw-launchd-err.log</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
```

```bash
# Replace YOUR_USER with actual username
sed -i '' "s/YOUR_USER/$(whoami)/g" ~/Library/LaunchAgents/com.openclaw.gateway.plist

# Load the service
launchctl load ~/Library/LaunchAgents/com.openclaw.gateway.plist

# Verify
launchctl list | grep openclaw
```

---

## 6. 使用 Tailscale 实现远程访问

### 从任何地方访问
- SSH：`ssh user@100.x.x.x`
- OpenClaw：`https://mac-mini.tail-xxxxx.ts.net`
- 无需端口转发
- 数据传输全程加密

### Tailscale 的访问控制（推荐）
在 Tailscale 管理控制台中限制访问权限：

```json
{
  "acls": [
    {"action": "accept", "src": ["your-devices"], "dst": ["mac-mini:*"]}
  ]
}
```

---

## 7. 配置 Telegram 机器人

```bash
# 1. Create bot via @BotFather on Telegram
# 2. Get your user ID via @userinfobot
# 3. Edit config
nano ~/.openclaw/openclaw.json
```

将相关配置添加到文件中：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "dmPolicy": "allowlist",
      "dmAllowlist": ["YOUR_USER_ID"]
    }
  }
}
```

```bash
# Restart to apply
docker compose restart
```

---

## 8. 端口转发方案（Tailscale 无法使用时）

| 方法 | 优点 | 缺点 |
|--------|------|------|
| **Tailscale**（推荐） | 无需额外配置，加密安全，免费 | 需要在每台设备上安装客户端 |
| **Cloudflare Tunnel** | 免费，无需开放端口 | 有轻微延迟，依赖 Cloudflare |
| **ngrok** | 设置简单 | 免费 tier 限制较多，生产环境需付费 |
| **路由器端口转发** | 直接访问 | 存在安全风险，IP 地址可能动态变化 |
| **WireGuard** | 效率较高，可自托管 | 需手动配置和维护 |

### Cloudflare Tunnel（Tailscale 的替代方案）

```bash
brew install cloudflared
cloudflared tunnel login
cloudflared tunnel create openclaw
cloudflared tunnel route dns openclaw agent.yourdomain.com

# Create config: ~/.cloudflared/config.yml
cat > ~/.cloudflared/config.yml << EOF
tunnel: YOUR_TUNNEL_ID
credentials-file: /Users/$USER/.cloudflared/YOUR_TUNNEL_ID.json
ingress:
  - hostname: agent.yourdomain.com
    service: http://localhost:3000
  - service: http_status:404
EOF

cloudflared tunnel run openclaw
```

---

## 9. 电源保护器（UPS）推荐

电源保护器可以在停电时防止数据丢失，并提供足够的关闭时间。

| 型号 | 容量 | 续航时间 | 价格 | 最适合 |
|-------|----------|---------|-------|----------|
| APC BE425M | 425VA | 约 15 分钟 | $55 | 适合预算有限的用户，仅适用于 Mac Mini |
| CyberPower CP685AVRG | 685VA | 约 20 分钟 | $80 | 适用于 Mac Mini 和路由器 |
| APC BR700G | 700VA | 约 25 分钟 | $120 | 适用于 Mac Mini、显示器和路由器 |
| CyberPower CP1500PFCLCD | 1500VA | 约 45 分钟 | 配置较为复杂，但性能更优 |

**推荐：** CyberPower CP685AVRG — 性价比高，适合 Mac Mini 和路由器的组合使用。

### 配置停电自动关机功能

```bash
# macOS reads UPS status via USB automatically
# Configure in System Settings → Energy → UPS
# Set: "Shut down after using UPS battery for: 10 minutes"
```

---

## 10. 监控与警报

### 基本健康检查脚本

将脚本保存为 `~/{baseDir}/scripts/health_check.sh`：

```bash
#!/bin/bash
# Check if OpenClaw container is running
if ! docker ps | grep -q openclaw-gateway; then
    echo "$(date): OpenClaw container not running! Restarting..." >> /tmp/openclaw-monitor.log
    cd ~/openclaw && docker compose up -d
    # Send alert via Telegram (if bot is available on host)
    curl -s "https://api.telegram.org/botYOUR_TOKEN/sendMessage" \
      -d "chat_id=YOUR_ID&text=⚠️ OpenClaw was down. Auto-restarted."
fi
```

### 基于 Cron 任务的定期检查

```bash
crontab -e
# Check every 5 minutes
*/5 * * * * bash ~/{baseDir}/scripts/health_check.sh
```

### 系统指标监控

```bash
# Install monitoring tools
brew install htop btop

# Check resources
htop                          # Interactive process viewer
docker stats                  # Container resource usage
df -h                         # Disk space
```

### 外部监控服务

可以考虑使用免费的外部监控工具：
- [UptimeRobot](https://uptimerobot.com) — 监控 Tailscale 服务器的运行状态
- [Healthchecks.io](https://healthchecks.io) — 通过 Cron 任务进行检查（成功时发送通知）

---

## 11. 成本比较

### Mac Mini M4 32GB（一次性购买费用 $699）

| 项目 | 每月费用 |
|------|-------------|
| 电费（平均约 15 瓦） | 约 $2 |
| 互联网费用 | $0 |
| Tailscale 使用费用 | 免费 |
| AI API 使用费用 | $50-500 |
| **总计** | **每月 $52-502** |
| **第一年（含硬件成本）** | **$1,323-6,723** |
| **第二年及以后** | **$624-6,024** |

### VPS（Hetzner CX32 — 4 个 CPU 核心，8GB 内存）

| 项目 | 每月费用 |
|------|-------------|
| 服务器费用 | $15 |
| AI API 使用费用 | $50-500 |
| **总计** | **每月 $65-515** |
| **第一年** | **$780-6,180** |

### 云服务器（AWS t3.large）

| 项目 | 每月费用 |
|------|-------------|
| EC2 服务器 | $60 |
| 存储费用 | $10 |
| 带宽费用 | $5-20 |
| AI API 使用费用 | $50-500 |
| **总计** | **每月 $125-590** |
| **第一年** | **$1,500-7,080** |

### 综合比较

| 项目 | Mac Mini | VPS | 云服务器 |
|--------|----------|-----|-------|
| 初始投资 | $699 | $0 | $0 |
| 每月费用 | 最低 | 中等 | 最高 |
| 性能 | 最佳（M4 芯片） | 良好 | 良好 |
| 延迟 | 受网络影响 | 稳定 | 稳定 |
| 维护成本 | 自己负责 | 由服务商管理 | 由服务商管理 |
| 支持本地模型 | 可 | 不支持 | 不支持 |
| 经济性（约 4 年后） | 更具优势 | 不具优势 |

**总结：** 如果你需要本地模型功能或计划长期使用，Mac Mini 是更好的选择；如果追求简单性和无初始投资成本，VPS 更适合；对于有合规性要求的企业，云服务器是更好的选择。

---

## 快速启动 checklist

- [ ] 购买 Mac Mini（推荐配置：M4 32GB）
- [ ] 完成 macOS 设置（禁用睡眠功能、启用自动登录、配置 SSH）
- [ ] 安装 Homebrew 和 Docker 及相关工具
- [ ] 克隆并构建 OpenClaw 项目
- [ ] 配置 `openclaw.json` 文件
- [ ] 运行 `docker-compose up -d` 命令启动服务
- [ ] 设置 launchd 服务以实现开机自启动
- [ ] 安装并配置 Tailscale 服务
- [ ] 配置 Telegram 机器人
- [ ] 连接电源保护器
- [ ] 设置健康检查机制
- [ ] 测试系统的重启恢复能力

## 致谢
本指南由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 制作。
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
本指南属于 **AgxntSix Skill Suite** 系列，专为 OpenClaw 代理设计。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)