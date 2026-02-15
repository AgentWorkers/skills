---
name: openclaw-cloudflare-secure
description: 如何通过 Cloudflare Zero Trust Access 和 Cloudflare Tunnel 在 VPS 上安全地暴露 OpenClaw Gateway 的 WebUI？具体步骤包括：

1. **配置 DNS**：将自定义主机名指向 Cloudflare 的 DNS 服务器，以确保用户可以通过域名访问 OpenClaw Gateway。

2. **启用 Cloudflare Zero Trust Access**：配置 Cloudflare Zero Trust Access，允许用户在没有密码认证的情况下访问受保护的资源（如 OpenClaw Gateway）。

3. **使用 Cloudflare Tunnel**：创建一个隧道，将 VPS 上的 OpenClaw Gateway WebUI 的网络流量通过 Cloudflare Tunnel 转发到外部网络。这可以确保流量在传输过程中受到加密和保护。

4. **配置安全规则**：设置适当的访问规则，以控制谁可以访问 OpenClaw Gateway，并确保只有经过验证的用户才能访问该资源。

5. **（可选）清理 Tailscale Serve**：如果之前使用了 Tailscale Serve 来托管 OpenClaw Gateway，建议将其关闭或迁移至其他安全的环境中。

通过以上步骤，你可以实现通过 Cloudflare Zero Trust Access 和 Cloudflare Tunnel 在 VPS 上安全地暴露 OpenClaw Gateway WebUI 的目标。
---

# OpenClaw WebUI：使用 Cloudflare Access 和 Tunnel（VPS）

当您需要一个易于使用的公共 URL（例如 `openclaw.example.com`）时，可以使用此方法。该 URL **不会** 直接暴露在互联网上，而是通过 **Cloudflare Access 的允许列表** 进行保护，并通过 **Cloudflare Tunnel** 传输到本地服务（通常是 `http://127.0.0.1:18789`）。

## 前提条件

- OpenClaw WebUI 可以在 VPS 上通过 `http://127.0.0.1:18789`（或您选择的本地端口）访问。
- 您可以控制 Cloudflare 中该域名的 DNS 设置（例如 `example.com`）。
- 您的代理程序/VPS 拥有 Cloudflare API 令牌，令牌名为 `CLOUDFLARE_API_TOKEN`。
  - 推荐的令牌权限（最小权限）：**Zone:DNS:Edit** + **Zone:Zone:Read**，以允许代理程序管理该域名的 DNS 记录。
- 您可以通过 Cloudflare Zero Trust UI 创建以下内容：
  - 为该域名创建一个 **访问应用**。
  - 为特定电子邮件地址设置 **允许** 策略。
  - 为所有用户设置 **阻止** 策略。
  - 创建一个 **Tunnel** 及其对应的 **令牌**。

## 快速入门（复制/粘贴）

### 0）（可选）：禁用 Tailscale Serve

如果您之前使用了 Tailscale Serve 并希望将其移除，请执行以下操作：

```bash
sudo tailscale serve reset
```

### 1）安装并启动基于令牌的 cloudflared tunnel 服务

在 Cloudflare Zero Trust 中：
- 转到 **Networks** → **Connectors** → **Tunnels** → **Create Tunnel** → 选择 **Cloudflared**。
- 从命令 `cloudflared service install <TOKEN>` 中复制 API 令牌。

在 VPS 上：
```bash
./scripts/install_cloudflared.sh
sudo ./scripts/tunnel_service_install.sh '<TOKEN>'
```

验证配置是否正确：
```bash
sudo systemctl is-active cloudflared
sudo systemctl status cloudflared --no-pager -l | sed -n '1,80p'
```

### 2）DNS 配置：将域名指向 Tunnel

请使用自带的 DNS 辅助工具 `./scripts/cf_dns.py` 进行配置。该工具会：
- 查找并删除与该域名相关的所有现有 A/AAAA/CNAME 记录。
- 为该域名创建一个指向 `<TUNNEL_UUID>.cfargotunnel.com` 的代理 CNAME 记录。

**前置要求：** 
```bash
export CLOUDFLARE_API_TOKEN='...'
```

### 2b）（可选）创建/更新子域名/DNS 记录（适用于代理程序）

当您希望代理程序使用具有最小权限的 DNS 令牌来编程创建 DNS 记录时，请执行以下操作：

```bash
./scripts/dns_create_record.sh --zone example.com --type A --name openclaw --content 1.2.3.4 --proxied true
./scripts/dns_create_record.sh --zone example.com --type CNAME --name openclaw --content target.example.net --proxied true
```

```bash
./scripts/dns_point_hostname_to_tunnel.sh \
  --zone example.com \
  --hostname openclaw.example.com \
  --tunnel-uuid <TUNNEL_UUID>
```

### 3）在 Cloudflare Zero Trust UI 中：将域名绑定到 Tunnel 服务

在 Tunnel 配置中：
- 添加 **Public Hostname**：
  - Hostname：`openclaw.example.com`
  - Service：`http://127.0.0.1:18789`

### 4）配置 Cloudflare Access 策略

在 Cloudflare Zero Trust 中：
- 转到 **Access** → **Applications** → **Add** → 选择 **Self-hosted**。
  - 设置 **Public Hostname** 为 `openclaw.example.com`。
  - 配置 **Policies**：
    - **Allow**：允许特定的电子邮件地址访问。
    - **Block**：阻止所有用户访问。

## 注意事项

- 如果在配置 Tunnel 时出现 “记录已存在” 的错误，这通常是由于 DNS 冲突引起的。您可以：
  - 删除现有的 DNS 记录，然后让系统重新创建。
  - 保持现有 DNS 设置不变，但在 Tunnel 配置中指定正确的 **Public Hostname**。
- 请确保域名是通过代理访问的（显示为橙色图标）。

## 回滚操作

- 如果需要恢复原始配置：
  - 在 DNS 中将域名指向原始的 A 记录。
  - 在 VPS 上执行 `sudo systemctl disable --now cloudflared` 命令，以停止 cloudflared 服务。