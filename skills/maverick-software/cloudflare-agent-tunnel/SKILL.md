---
name: cloudflare-agent-tunnel
description: 使用 Cloudflare Tunnel（cloudflared）为每个 OpenClaw 代理分配一个独立的、安全的 HTTPS URL。无需管理 SSL 证书，也无需公开暴露任何端口。该方法适用于在 VPS 上为 OpenClaw 代理设置安全云访问、为每个代理分配子域名（例如 koda.yourdomain.com）、在不使用 nginx 或 Let's Encrypt 的情况下启用 HTTPS，或将自定义域名连接到代理。涵盖了快速隧道（无需注册账户，立即获取 URL）、命名隧道（永久 URL，使用免费 Cloudflare 账户）、在单个 VPS 上配置多个代理以及自定义域名设置等功能。
---
# Cloudflare 代理隧道

通过 Cloudflare Tunnel 为每个 OpenClaw 代理分配一个永久且安全的 HTTPS 地址——无需 SSL 证书、无需使用 nginx，也无需开放任何端口。

## 工作原理

```
User → https://koda.yourdomain.com
         ↓ (Cloudflare edge — TLS termination here)
       Cloudflare Tunnel (encrypted)
         ↓
       cloudflared process on VPS
         ↓
       http://localhost:18789  (OpenClaw gateway)
```

- Cloudflare 负责处理 TLS 加密通信，服务器端无需管理 SSL 证书；
- 本地端口无需直接暴露给互联网；
- 每个代理都会运行自己的 `cloudflared` 进程，并通过 systemd 服务进行管理。

---

## 选项 1 — 快速隧道（无需账号，立即生效）

适用于测试或临时访问。分配的 URL 是随机生成的，并在重启后自动重置。

```bash
# Install cloudflared
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared any main" \
  | tee /etc/apt/sources.list.d/cloudflared.list
apt-get update -qq && apt-get install -y cloudflared

# Start quick tunnel — prints a random https://*.trycloudflare.com URL
cloudflared tunnel --url http://localhost:18789 --no-autoupdate
```

使用自动化脚本：
```bash
./scripts/tunnel-setup.sh --agent koda --port 18789 --quick
```

---

## 选项 2 — 命名隧道（永久使用，需免费 Cloudflare 账号）

可获取永久性的 HTTPS 地址。需要一个免费的 Cloudflare 账号和一个域名。

### 第 1 步：身份验证

```bash
cloudflared login
# Opens a browser URL — authorize your domain
# Saves /root/.cloudflared/cert.pem
```

### 第 2 步：创建隧道

```bash
cloudflared tunnel create openclaw-koda
# Outputs UUID — save it
```

### 第 3 步：配置代理设置

在 `/etc/cloudflared/openclaw-koda.yml` 文件中进行配置：
```yaml
tunnel: <UUID>
credentials-file: /root/.cloudflared/<UUID>.json

ingress:
  - hostname: koda.yourdomain.com
    service: http://localhost:18789
  - service: http_status:404
```

### 第 4 步：配置 DNS 路由

```bash
cloudflared tunnel route dns openclaw-koda koda.yourdomain.com
# Creates CNAME: koda.yourdomain.com → <UUID>.cfargotunnel.com
```

### 第 5 步：将代理设置为 systemd 服务

```bash
cat > /etc/systemd/system/cloudflared-koda.service << 'EOF'
[Unit]
Description=Cloudflare Tunnel — koda
After=network.target

[Service]
Type=simple
User=root
ExecStart=/usr/bin/cloudflared tunnel --no-autoupdate --config /etc/cloudflared/openclaw-koda.yml run
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable cloudflared-koda
systemctl start cloudflared-koda
```

或者使用自动化脚本：
```bash
./scripts/tunnel-setup.sh --agent koda --port 18789 --domain koda.yourdomain.com
```

---

## 多代理设置（一个 VPS 上部署多个代理）

每个代理对应一个 OpenClaw 网关和一个 Cloudflare 隧道，两者都作为独立的 systemd 服务运行。

```
Port 18789 → openclaw-koda.service   + cloudflared-koda.service   → koda.yourdomain.com
Port 18790 → openclaw-alex.service   + cloudflared-alex.service   → alex.yourdomain.com
Port 18791 → openclaw-jordan.service + cloudflared-jordan.service → jordan.yourdomain.com
```

**重要提示：** 不要使用 `cloudflared service install` 命令来为多个代理设置隧道——该命令仅支持创建一个隧道，并会覆盖系统中的默认服务配置。务必为每个代理手动创建独立的 systemd 服务配置文件（如上所示）。

```bash
# Add each agent sequentially
./scripts/tunnel-setup.sh --agent alex   --port 18790 --domain alex.yourdomain.com
./scripts/tunnel-setup.sh --agent jordan --port 18791 --domain jordan.yourdomain.com
```

---

## 更新 OpenClaw 的允许访问源地址

设置好隧道后，需将 HTTPS 地址添加到代理的 `openclaw.json` 配置文件中，否则代理的 UI 界面会阻止连接。

```json
"gateway": {
  "controlUi": {
    "allowedOrigins": [
      "http://localhost:18789",
      "https://koda.yourdomain.com"
    ]
  }
}
```

然后重启代理服务：`systemctl restart openclaw-koda`

---

## 自定义域名

关于如何添加域名、配置 Cloudflare 名称服务器、为每个代理设置子域名以及管理 DNS 记录的详细步骤，请参阅 `references/custom-domains.md`。

**关键注意事项：**
- 域名必须使用 Cloudflare 提供的名称服务器（免费）；
- Cloudflare 会自动处理 TLS 证书的更新；
- 通过 `cloudflared tunnel route dns` 命令会自动生成 CNAME 记录；
- 免费 Cloudflare 计划支持无限数量的隧道和无限带宽。

---

## 管理隧道

```bash
# Status of all tunnels
systemctl list-units "cloudflared-*" --no-pager

# Logs
journalctl -u cloudflared-koda -f

# List all named tunnels (requires cloudflared login)
cloudflared tunnel list

# Delete a tunnel
cloudflared tunnel delete openclaw-koda
systemctl disable cloudflared-koda && rm /etc/systemd/system/cloudflared-koda.service
```