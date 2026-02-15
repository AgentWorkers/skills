---
name: openclaw-server-secure-skill
description: **OpenClaw（原名Clawdbot/Moltbot）全面安全加固与安装指南**  
当用户需要保护服务器、安装OpenClaw代理，或配置Tailscale/Firewall以支持该代理时，请参考本指南。
---

# OpenClaw 服务器安全与安装指南

## 概述
本指南将指导您如何设置一个安全、自托管的 OpenClaw 实例。内容包括 SSH 安全加固、防火墙配置、Tailscale VPN 的搭建以及 OpenClaw 本身的安装过程。

## 工作流程

### 第一阶段：系统安全加固

1. **SSH 安全设置**
    - 目标：仅允许使用 SSH 密钥登录，禁止使用密码，同时禁止 root 用户登录。
    - 操作：修改 `/etc/ssh/sshd_config` 文件。
    - 命令：
      ```bash
      # Backup config
      sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
      # Disable Password Auth
      sudo sed -i 's/^#*PasswordAuthentication .*/PasswordAuthentication no/' /etc/ssh/sshd_config
      # Disable Root Login
      sudo sed -i 's/^#*PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config
      # Reload SSH
      sudo sshd -t && sudo systemctl reload ssh
      ```

2. **默认拒绝策略防火墙（Default-Deny Firewall）**
    - 目标：默认拒绝所有传入的连接请求。
    - 操作：安装并启用 UFW 防火墙。
    - 命令：
      ```bash
      sudo apt update && sudo apt install ufw -y
      sudo ufw default deny incoming
      sudo ufw default allow outgoing
      sudo ufw enable
      ```
    *注意：在启用 UFW 之前，请确保您能够访问控制台，或者准备好备用登录方式（以防 SSH 无法在其他接口上使用）。接下来我们将配置 Tailscale。*

3. **暴力登录防护**
    - 目标：在登录尝试失败后自动封禁相关 IP 地址。
    - 操作：安装 Fail2ban 工具。
    - 命令：
      ```bash
      sudo apt install fail2ban -y
      sudo systemctl enable --now fail2ban
      ```

### 第二阶段：网络隐私保护（使用 Tailscale）

4. **安装 Tailscale**
    - 目标：创建一个私有的 VPN 网络。
    - 命令：
      ```bash
      curl -fsSL https://tailscale.com/install.sh | sh
      sudo tailscale up
      ```
    *等待用户完成 Tailscale 的身份验证。*

5. **通过 Tailscale 配置 SSH 和 Web 访问**
    - 目标：仅允许来自 Tailscale 子网（100.64.0.0/10）的流量通过，并禁止公共访问。
    - 命令：
      ```bash
      # Allow SSH over Tailscale
      sudo ufw allow from 100.64.0.0/10 to any port 22 proto tcp
      # Remove public SSH access (Adjust rule name/number as needed)
      sudo ufw delete allow OpenSSH || sudo ufw delete allow 22/tcp
      # Allow Web ports over Tailscale
      sudo ufw allow from 100.64.0.0/10 to any port 443 proto tcp
      sudo ufw allow from 100.64.0.0/10 to any port 80 proto tcp
      ```

6. **禁用 IPv6（可选）**
    - 目标：减少攻击面。
    - 命令：
      ```bash
      sudo sed -i 's/IPV6=yes/IPV6=no/' /etc/default/ufw
      if ! grep -q "net.ipv6.conf.all.disable_ipv6 = 1" /etc/sysctl.conf; then
        echo "net.ipv6.conf.all.disable_ipv6 = 1" | sudo tee -a /etc/sysctl.conf
      fi
      sudo sysctl -p && sudo ufw reload
      ```

### 第三阶段：OpenClaw 安装

7. **安装 OpenClaw**
    - 命令：
      ```bash
      npm install -g openclaw && openclaw doctor
      ```

8. **配置用户访问权限**
    - **必填信息**：要求用户提供他们的 Telegram ID。
    - 操作：更新配置文件，仅允许该用户登录。
    - JSON 配置文件示例（使用 `openclaw doctor` 工具验证配置）：
      ```json
      { 
        "dmPolicy": "allowlist", 
        "allowFrom": ["YOUR_TELEGRAM_ID"], 
        "groupPolicy": "allowlist" 
      }
      ```

9. **保护用户凭证**
    - 目标：限制文件的访问权限。
    - 命令：
      ```bash
      chmod 700 ~/.openclaw/credentials 2>/dev/null || true
      chmod 600 .env 2>/dev/null || true
      ```

10. **最终安全审计**
    - 操作：运行内置的安全审计工具。
    - 命令：
      ```bash
      openclaw security audit --deep
      ```

## 验证状态
运行以下命令以确认配置是否正确：
```bash
sudo ufw status verbose
ss -tulnp
tailscale status
openclaw doctor
```