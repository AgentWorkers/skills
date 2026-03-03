---
name: vps-bootstrap
description: 从零开始将一个新的虚拟专用服务器（VPS）配置为可正常运行的 OpenClaw 环境，包括备份/恢复功能以及恢复后的验证流程。适用于在新 VPS 上安装 OpenClaw、从故障服务器中恢复数据、在不同机器之间迁移系统，或实现灾难恢复自动化。内容涵盖系统依赖关系、Node.js 的配置、OpenClaw 的安装过程、安全加固措施、数据备份至 Google Drive 的方法、从备份中恢复数据的功能，以及全面的系统验证流程。
---
# VPS 自动部署与灾难恢复框架（适用于 Ubuntu VPS 上的 OpenClaw）

## 概述

整个部署和灾难恢复流程由三个脚本完成：

1. **`bootstrap.sh`** — 从新创建的 VPS 部署到完全可用的 OpenClaw 环境（耗时约 15-20 分钟）
2. **`restore.sh`** — 从备份中恢复工作区文件、配置信息、加密密钥以及定时任务（Cron 作业）
3. **`verify.sh`** — 部署后的验证（所有检查通过表示环境已准备就绪）

## 快速入门

### 新 VPS 的设置

```bash
# On fresh Ubuntu 24.04 VPS
bash scripts/bootstrap.sh
```

### 从备份中恢复数据

```bash
bash scripts/restore.sh ~/openclaw-backup-*.tar.gz
```

### 验证所有功能是否正常

```bash
bash scripts/verify.sh
```

## `bootstrap.sh` 的功能

该脚本执行顺序化的安装过程，并在每个步骤中处理可能出现的错误：

1. **系统软件包**：安装 `build-essential`、`curl`、`git`、`jq`、`unzip` 等工具。
2. **Node.js**：通过 NodeSource 安装最新版本的 LTS 版本。
3. **Google Chrome**：安装稳定版本的浏览器，并配置无头模式以供浏览器工具使用。
4. **OpenClaw**：全局安装 Node.js 包并通过 npm 配置 OpenClaw 服务。
5. **安全基础设置**：配置 UFW 防火墙、`fail2ban` 规则以及仅使用 SSH 密钥的认证方式。
6. **服务配置**：创建一个 systemd 用户服务，并设置自动重启功能。

每个步骤都是可重复执行的（idempotent），即使过程中中断也可以重新运行。

## `restore.sh` 的功能

该脚本从备份文件中恢复以下内容：

- 工作区文件（`SOUL.md`、`MEMORY.md`、`AGENTS.md`、`memory/` 目录及其中的脚本文件）
- OpenClaw 的配置文件（`openclaw.json`、`.env`）
- 定时任务数据库
- GPG 密钥及密码存储（以加密形式保存）
- OAuth 认证信息（如 GOG、rclone 的配置）
- 系统配置的快照

## `verify.sh` 的功能

该脚本执行多项检查并报告结果：

- OpenClaw 服务是否正常运行
- 是否成功连接到 Telegram/Discord 通信服务
- 浏览器工具是否可用
- 备份系统是否正常工作
- 定时任务是否已加载并执行
- SSH 安全设置是否正确
- 磁盘空间和内存使用情况是否满足要求

## 备份脚本（可选）

有关自动每日备份的详细信息，请参阅 `references/backup-guide.md`。

## 自定义设置

您可以在 `scripts/bootstrap.sh` 文件的顶部修改相关配置变量：

```bash
OPENCLAW_PORT=18789        # Gateway port
ENABLE_FIREWALL=true       # UFW setup
ENABLE_FAIL2BAN=true       # SSH protection
INSTALL_CHROME=true        # Browser tools support
```

## 系统要求

- Ubuntu 22.04 或更高版本，或 Debian 12 及更高版本
- 拥有 root 权限或 sudo 权限
- 建议配备 2GB 以上的内存
- SSH 密钥配置已完成

## 安全注意事项

- 脚本不会将任何敏感信息以明文形式存储在脚本文件中。
- GPG 密钥会进行加密备份。
- SSH 认证方式设置为仅使用密钥。
- OpenClaw 服务默认绑定到本地主机（localhost）。