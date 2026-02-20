---
name: vps-openclaw-security-hardening
description: 适用于运行 OpenClaw AI 代理的虚拟专用服务器（VPS）的生产级安全加固方案。该方案包括 SSH 安全加固（自定义端口设置）、防火墙配置、审计日志记录、凭证管理以及智能警报功能。遵循 BSI IT-Grundschutz 和 NIST 的安全指南，同时实现最小的资源消耗。
version: 1.0.6
author: OpenClaw Community
homepage: https://github.com/MarcusGraetsch/vps-openclaw-security-hardening
metadata:
  openclaw:
    emoji: 🛡️
    requires:
      bins: ["ssh", "ufw", "auditd", "systemctl", "apt-get"]
      optional: ["fail2ban"]
      os: ["ubuntu", "debian"]
    tags: ["security", "hardening", "vps", "audit", "monitoring", "firewall", "ssh", "fail2ban"]
    install: "SSH_PORT=4848 ./scripts/install.sh"
    verify: "./scripts/verify.sh"
    warning: "DO NOT use on machines with sensitive personal data. Use dedicated VPS only. Test in VM first."
---
# OpenClaw的VPS安全加固方案

专为在VPS上部署AI代理而设计的、具备生产环境级别的安全加固方案。

## ⚠️ 重要警告

**切勿在存储敏感个人数据的服务器/机器上运行OpenClaw**。请使用专用的机器（VPS、裸机或专为OpenClaw设计的本地服务器）。

**支持的操作系统：** Ubuntu 20.04+、Debian 11+。不支持Windows（请使用WSL2）或macOS。

## ⚠️ 首先选择SSH端口

**在安装之前，必须选择一个自定义的SSH端口（1024-65535）**。这有助于您明确自己的安全决策。

```bash
# Choose your port (example: 4848)
export SSH_PORT=4848

# Install
cd ~/.openclaw/skills/vps-openclaw-security-hardening
sudo ./scripts/install.sh

# Verify
./scripts/verify.sh

# Test SSH (new terminal)
ssh -p ${SSH_PORT} root@your-vps-ip
```

## 功能介绍

| 层级 | 保护措施 | 实现方式 |
|-------|------------|----------------|
| **网络** | 防火墙、SSH安全加固 | UFW防火墙、自定义端口（由您选择）、仅使用密钥认证 |
| **系统** | 自动更新、监控 | 无人值守升级、auditd日志记录 |
| **密码管理** | 集中式密码管理（.env文件存储） |
| **监控** | 审计日志记录、警报机制 | 内核级审计功能、多渠道警报系统 |

## 系统要求

- **操作系统：** Ubuntu 20.04+ 或 Debian 11+（仅限Linux系统）  
- **不支持的系统：** Windows（请使用WSL2）或macOS  
- 需要具有root权限  
- 需要现有的SSH密钥认证机制  
- **警报渠道（可选）：** Telegram、Discord、Slack、电子邮件或Webhook  
- **自定义SSH端口（1024-65535）**

## 安全改进措施

### SSH设置
- **端口：** 从22更改为${SSH_PORT}（您选择的端口，范围为1024-65535）  
- **认证方式：** 仅使用密钥认证（禁止使用密码）  
- **root登录：** 被禁用  
- **最大重试次数：** 3次  
- **暴力破解防护：** 启用Fail2ban机制  

### 防火墙设置
- **默认策略：** 拒绝所有入站连接  
- **允许的连接：** 仅允许您选择的SSH端口  

### 服务配置
- **CUPS（打印服务）：** 已停止并禁用  
- **入侵检测：** 启用Fail2ban机制  
- **自动更新：** 安全补丁会自动应用  

### 监控机制
- **密码文件访问记录：** 记录所有对密码文件的访问操作  
- **SSH配置变更检测：** 异常更改会立即触发警报  
- **权限升级警报：** 发生权限升级时会立即通知  
- **每日安全报告：** 提供每日安全状况汇总  

## 资源消耗

| 组件 | 内存占用（MB） | 磁盘空间（MB） |
|-----------|-----|------|
| auditd | 约2 MB | 最大40 MB |
| UFW防火墙 | 约1 MB | 可忽略不计 |
| 脚本文件 | 约5 MB | 可忽略不计 |
| **总计：** **<10 MB** | **<50 MB** |

## 相关文件

- `scripts/install.sh`：主要安装脚本  
- `scripts/verify.sh`：安装完成后进行验证  
- `scripts/rollback-ssh.sh`：用于紧急情况下的SSH配置回滚  
- `scripts/critical-alert.sh`：发送Telegram警报的脚本  
- `scripts/daily-briefing.sh`：生成每日安全报告的脚本  
- `rules/audit.rules`：审计规则配置文件  

## 文档说明

详细文档请参阅[README.md]。  

## 许可证

本项目采用MIT许可证。具体许可信息请参阅[LICENSE文件]。