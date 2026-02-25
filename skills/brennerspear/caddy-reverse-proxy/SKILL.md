---
name: caddy
description: 通过通配符子域名，添加、管理并排查 Caddy 反向代理路由的问题，以支持本地应用程序。
compatibility: macOS (LaunchDaemon) or Linux (systemd). Requires Caddy, Tailscale, Vercel DNS account.
---
# Caddy — 用于本地应用的通配符反向代理

Caddy 通过反向代理将 `*.YOUR_DOMAIN` 这些子域名通过 HTTPS 链接到本地服务，并自动生成 Let’s Encrypt 证书。此功能专为仅通过 Tailscale 访问的场景设计（不对外公开）。

> **DNS 提供商：** 本功能使用 **Vercel DNS** 来处理 DNS-01 ACME 挑战。如果您使用其他 DNS 提供商，请将 `caddy-dns/vercel` 插件和 TLS 配置替换为您所使用提供商的相应插件和配置（详情请参见 [caddy-dns](https://github.com/caddy-dns)）。

## 添加新应用

1. **创建一个后台服务**（macOS 上使用 LaunchAgent，Linux 上使用 systemd）——模板请参见 `reference.md`。
2. **在 Caddyfile（`~/.config/caddy/Caddyfile`）中添加相关配置**：
   ```caddy
   appname.YOUR_DOMAIN {
       import vercel_tls
       reverse_proxy localhost:31XX
   }
   ```
   同时在顶部的仪表板 HTML 块中添加一个 `<li>` 条目以显示新应用的名称。
3. **重新加载 Caddy**：
   ```bash
   ~/.local/bin/caddy reload --config ~/.config/caddy/Caddyfile --address localhost:2019
   ```
   TLS 证书的生成需要 30–60 秒（完成 DNS-01 挑战）。
4. **如果应用需要连接到 OpenClaw Gateway**——请参阅该文件夹中的 `OPENCLAW.md` 以获取特定的网关配置。

## 快速开发服务器

配套技能：[dev-serve](https://clawhub.com/skills/dev-serve)——通过一个命令即可启动开发服务器并配置 Caddy 路由。

```bash
dev-serve up ~/projects/myapp        # → https://myapp.YOUR_DOMAIN
dev-serve down myapp
dev-serve ls
```

## 重新加载/重启 Caddy

```bash
# Reload config (no restart, no sudo)
~/.local/bin/caddy reload --config ~/.config/caddy/Caddyfile --address localhost:2019

# Full restart
# macOS:
sudo launchctl unload /Library/LaunchDaemons/com.caddyserver.caddy.plist
sudo launchctl load /Library/LaunchDaemons/com.caddyserver.caddy.plist
# Linux:
systemctl --user restart caddy
```

## 故障排除

- **证书生成失败**：`tail -50 /var/log/caddy-error.log | grep -i error` — 可能是 Vercel API 令牌过期导致的。
- **DNS 解析失败**：`dig +short appname.YOUR_DOMAIN` — 应该能返回您的 Tailscale IP 地址。
- **TLS 错误（curl 命令返回 35 状态码）**：证书尚未生成，请等待 30–60 秒。

如需完整参考信息（包括示例应用、关键文件和构建说明），请参阅 `reference.md`。
有关 OpenClaw 网关的集成方式，请参阅 `OPENCLAW.md`。