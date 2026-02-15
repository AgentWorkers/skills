---
name: bitwarden
description: 使用 rbw CLI 安全地访问和管理 Bitwarden/Vaultwarden 的密码。
metadata: {"clawdbot":{"emoji":"🔒","os":["linux","macos"],"requires":{"bins":["rbw"]}}}
---

# Bitwarden 技能

使用 `rbw` CLI 与 Bitwarden 或 Vaultwarden 保管库进行交互。

## 使用方法与配置

### 1. 设置（首次运行）
```bash
rbw config set email <your_email>
rbw config set baseurl <vault_url> # Optional, defaults to bitwarden.com
rbw login
```
*注意：登录需要主密码，可能还需要 2FA（电子邮件/OTP）验证。*

### 2. 解锁
```bash
rbw unlock
```
*注意：`rbw` 会将会话密钥缓存到代理程序中。如果需要交互式输入（如密码输入），请考虑使用 `pinentry-curses`（基于 CLI 的密码输入工具）作为密码输入方式。*

### 3. 管理
- **列出项目：`rbw list`
- **获取项目信息：`rbw get "名称"`
- **获取项目详情（JSON 格式）：`rbw get --full "名称"`
- **搜索：`rbw search "查询条件"`
- **添加项目：`rbw add ...`
- **同步数据：`rbw sync`（刷新保管库数据）*
*注意：在获取项目详情之前，请务必先执行同步操作以确保数据准确性。*

## 工具

代理程序使用 `exec` 命令来执行 `rbw` 命令。
- 如果 `rbw` 通过 `pinentry-curses` 要求输入密码，请使用 `tmux` 来提供交互式密码输入界面。
- 在添加项目时，`rbw add` 命令可能需要配置 `EDITOR` 或使用 `tmux` 来辅助操作。