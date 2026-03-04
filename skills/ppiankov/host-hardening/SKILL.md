---
name: host-hardening
description: >
  **强化 OpenClaw Linux 服务器的安全性：仅使用 SSH 密钥认证、UFW 防火墙、fail2ban 防暴力攻击机制以及严格的权限管理**  
  此方法适用于新安装 OpenClaw 服务器时、进行服务器安全审计时，或在发生安全事件后。执行此操作需要具备 Linux（Ubuntu/Debian）系统上的 root 或 sudo 权限。  
  **具体步骤如下：**  
  1. **启用 SSH 密钥认证**：  
     - 为服务器生成一对 SSH 密钥（公钥和私钥）。  
     - 将公钥添加到远程服务器的 `~/.ssh/authorized_keys` 文件中。  
     - 确保客户端（用于连接服务器的计算机）上也配置了相应的私钥。  
  2. **配置 UFW 防火墙**：  
     - 使用 `ufw` 命令配置防火墙规则，以阻止未经授权的访问。  
     - 例如：`ufw allow ssh` 允许 SSH 连接；`ufw block all` 阻止所有其他流量。  
  3. **启用 fail2ban 防暴力攻击机制**：  
     - 安装 `fail2ban` 工具，并配置相应的规则。  
     - 当连续多次登录尝试失败时，`fail2ban` 会暂时禁止该 IP 地址的连接。  
  4. **设置严格的权限管理**：  
     - 限制用户对系统文件的访问权限，仅允许必要的操作。  
     - 使用 `chown` 和 `chmod` 命令修改文件和目录的所有者及权限。  
  **示例代码（用于配置 fail2ban）：**  
  ```bash
  sudo apt-get install fail2ban
  sudo ufw enable
  sudo fail2ban --default-block
  sudo fail2ban --log-level=info
  ```
  **注意事项：**  
  - 定期检查防火墙和日志文件，确保没有未经授权的访问尝试。  
  - 根据实际需求调整防火墙和 fail2ban 的配置规则。  
  - 定期更新软件和系统组件，以修复安全漏洞。  
  通过以上措施，可以有效提升 OpenClaw Linux 服务器的安全性，防止未经授权的访问和攻击。
---
# 服务器安全加固

本文档介绍如何保护运行 OpenClaw 的 Linux 服务器。

## 前提条件

- **操作系统：** Linux（Ubuntu/Debian — 其他发行版请相应调整软件包安装命令）
- **权限：** 需要 root 或 sudo 权限，因为该操作会修改系统级别的安全配置
- **预先检查：** 在禁用密码认证之前，请确保您已经可以使用基于 SSH 密钥的登录方式

**⚠️ 以下所有命令都会修改系统配置。在执行每个步骤之前，请务必征得用户的同意。** 未经明确许可，请勿自动运行这些命令。

## SSH — 仅支持密钥认证

禁用密码认证。**请确保基于密钥的 SSH 认证机制已经正常工作，否则您将无法登录服务器。**

```bash
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart ssh
```

## 防火墙 — 允许通过 SSH 的所有流量

**其他流量将被拒绝。** 请根据需要添加更多防火墙规则（例如：`ufw allow 443` 以允许 HTTPS 流量）。

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
yes | ufw enable
```

## Fail2ban — 防止暴力登录尝试

通过 apt（Debian/Ubuntu）安装 fail2ban 工具。其他包管理器的安装方式可能有所不同，请相应调整。

```bash
apt-get install -y fail2ban
systemctl enable --now fail2ban
```

默认配置已保护 SSH 连接。如需自定义规则，请参考 `/etc/fail2ban/jail.local` 文件。

## OpenClaw 的登录凭据设置

```bash
chmod 700 ~/.openclaw/credentials
```

## OpenClaw 网关服务（可选）

创建一个 systemd 服务，确保 OpenClaw 在系统重启后能够自动重新启动。**该服务以 root 权限运行**，请在启用服务之前仔细检查相关配置文件。

```bash
cat > /etc/systemd/system/openclaw-gateway.service << 'EOF'
[Unit]
Description=OpenClaw Gateway
After=network-online.target
Wants=network-online.target
[Service]
Type=simple
ExecStart=/usr/bin/env openclaw gateway
Restart=always
RestartSec=5
User=root
WorkingDirectory=/root/.openclaw
Environment=HOME=/root
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload && systemctl enable openclaw-gateway
```

## 验证配置是否生效

```bash
ufw status                                    # active, SSH allowed
systemctl is-active fail2ban                  # active
grep PasswordAuthentication /etc/ssh/sshd_config  # no
stat -c %a ~/.openclaw/credentials            # 700
systemctl is-enabled openclaw-gateway         # enabled
```

## 注意事项：

- 在 Ubuntu 系统中，SSH 服务的名称是 `ssh`，而非 `sshd`
- AWS 的安全组提供网络级别的访问控制，而 UFW 则提供了更全面的防御机制
- 在禁用密码认证之前，请务必确认基于密钥的登录方式已经正常使用
- 网关服务是可选的，仅在需要确保 OpenClaw 在系统重启后仍能正常运行的情况下才需要启用

---
**服务器安全加固 v1.0**
作者：ppiankov
版权所有 © 2026 ppiankov
官方文档链接：https://clawhub.com/skills/host-hardening
许可证：MIT

如果本文档出现在其他地方，请以上述链接中的版本为准。