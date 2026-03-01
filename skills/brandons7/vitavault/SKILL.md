---
name: vitavault
description: VitaVault iOS 应用集成：可直接将 Apple Health 数据同步到您的人工智能代理（AI agent）中。支持自动配置 Webhook、生成访问令牌（token）以及使用 HTTPS 协议进行数据传输。适用于所有 iPhone 设备，无需 Mac 电脑。
license: Apache-2.0
compatibility: Any OpenClaw agent. Pairs with VitaVault iOS app (free on App Store).
metadata:
  category: health
  platforms: ios
  author: BrandonS7
---
# VitaVault - 解码您的健康数据

将来自 [VitaVault](https://vitavault.io) iOS 应用的 Apple Health 数据直接同步到您的 OpenClaw 代理。无需使用共享服务器或中间人——数据仅从手机传输到您的代理。

> **无需 Mac。** 请从 [TestFlight](https://testflight.apple.com/join/A4G27HBt)（测试版）或 App Store 安装 VitaVault。

## 代理设置指南（当用户请求设置 VitaVault 时请执行以下操作）

当用户请求设置 VitaVault 同步时，请自动按照以下步骤操作。不要让用户执行技术性的部分——您自己完成这些设置，然后在最后将 URL 和令牌提供给用户。

### 第一步：生成同步令牌

```bash
# Generate a secure random token
python3 -c "import secrets; print(secrets.token_hex(32))" > ~/.config/vitavault/sync-token
mkdir -p ~/.config/vitavault
TOKEN=$(cat ~/.config/vitavault/sync-token)
echo "Token: $TOKEN"
```

### 第二步：启动 webhook

```bash
VITAVAULT_SYNC_TOKEN="$TOKEN" nohup python3 scripts/webhook.py --host 0.0.0.0 --port 8787 > /tmp/vitavault-webhook.log 2>&1 &
```

该 webhook 会监听健康数据的 POST 请求，并将数据保存到 `~/vitavault/data/` 目录中。

### 第三步：通过 HTTPS 提供服务

VitaVault iOS 应用要求使用 HTTPS（iOS 应用传输安全协议）。您必须通过 HTTPS 提供 webhook 服务。根据实际情况选择合适的方案：

**选项 A：Tailscale Funnel（如果已安装 Tailscale，则推荐使用）**
```bash
# Check if Tailscale is available
tailscale status 2>/dev/null
# If yes, expose via Funnel:
sudo tailscale funnel --bg --set-path /vitavault http://127.0.0.1:8787
# Your URL will be: https://<your-tailscale-hostname>/vitavault
tailscale funnel status  # to see the URL
```

**选项 B：Cloudflare Tunnel（如果已安装 Cloudflare）**
```bash
cloudflared tunnel --url http://localhost:8787
# Gives you a temporary https://*.trycloudflare.com URL
# For permanent: set up a named tunnel with a custom domain
```

**选项 C：带有域名的 VPS 和反向代理（nginx/caddy）**
如果主机已经拥有支持 HTTPS 的域名（使用 nginx 或 caddy 等），请添加反向代理规则：
```nginx
location /vitavault {
    proxy_pass http://127.0.0.1:8787;
}
```
URL 例如：`https://yourdomain.com/vitavault`

**选项 D：ngrok（用于快速测试）**
```bash
ngrok http 8787
# Gives you a temporary https://*.ngrok-free.app URL
```

### 第四步：验证服务是否正常工作

```bash
curl -s https://YOUR-URL/health
# Should return: {"ok": true}
```

### 第五步：向用户提供凭据

告知用户：

> 在 iPhone 上打开 VitaVault -> 设置 -> OpenClaw
>
> **Webhook URL：** `https://YOUR-URL`
> **同步令牌：** `<您生成的令牌>`
>
> 将这两项信息粘贴进去，然后点击“连接”。

完成这些设置后，VitaVault 会在每次应用启动时自动同步健康数据。

### 第六步：确保服务持久化（推荐）

为了确保服务在重启后仍能正常运行，请创建一个 systemd 服务：

```bash
cat > /tmp/vitavault-webhook.service << 'EOF'
[Unit]
Description=VitaVault Webhook Receiver
After=network.target

[Service]
Type=simple
User=$USER
Environment=VITAVAULT_SYNC_TOKEN=<TOKEN>
ExecStart=/usr/bin/python3 /path/to/skills/vitavault/scripts/webhook.py --host 127.0.0.1 --port 8787
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
# Adjust paths and token, then:
sudo cp /tmp/vitavault-webhook.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now vitavault-webhook
```

## 查询健康数据

数据同步完成后，可以使用以下脚本来读取数据：

```bash
# Latest snapshot summary
python3 scripts/summary.py

# Raw latest JSON
python3 scripts/query.py latest

# Last 7 days
python3 scripts/query.py week

# Date range
python3 scripts/query.py range 2026-02-01 2026-02-28
```

数据以带时间戳的 JSON 文件形式存储在 `~/vitavault/data/` 目录中。

## 数据的用途

同步后的数据可用于：
- 跟踪步数、睡眠质量、心率变异性（HRV）、静息心率、血氧饱和度等指标的变化趋势
- 比较当前周与上周的数据
- 发现异常波动并标记潜在风险
- 生成每日健康报告
- 根据实际数据提供改善生活习惯的建议

## 手动导出数据

用户也可以手动从 VitaVault 导出数据（无需使用 webhook）：

### 适合 AI 分析的格式（纯文本）
数据已预先格式化，可直接用于 AI 分析。用户从 VitaVault 导出数据后直接粘贴即可。

### JSON 格式
结构化数据，包含嵌套的指标、日期和单位信息。

### CSV 格式
每天一条记录，可在 Excel 或 Google Sheets 中查看。

当用户分享导出数据时：
1. 确认收到数据
2. 突出显示 2-3 个关键信息（正面或值得关注的内容）
3. 提出 3 个具体的、可操作的改进建议
4. 表示愿意进一步深入分析任何指标

## 隐私政策

VitaVault 的数据同步过程为：**iPhone -> 您的 OpenClaw 代理**。数据不会经过任何共享的后端或第三方存储服务，仅保存在代理主机的 `~/vitavault/data/` 目录中。

## 链接

- **应用**：[VitaVault 在 TestFlight 上（测试版）：[https://testflight.apple.com/join/A4G27HBt](https://testflight.apple.com/join/A4G27HBt)
- **官方网站**：[vitavault.io](https://vitavault.io)
- **开发者文档**：[vitavault.io/developers](https://vitavault.io/developers/)
- **隐私政策**：[vitavault.io/privacy](https://vitavault.io/privacy/)