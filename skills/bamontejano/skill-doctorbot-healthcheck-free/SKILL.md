---
name: doctorbot-healthcheck-free
version: 1.0.0
description: 🩺 免费的安全与健康检查服务：您的 OpenClaw 系统值得进行一次全面的安全评估。该功能会执行一次非侵入性的扫描，以检测潜在的安全风险、过时的软件版本以及配置错误。
author: DoctorBot-x402
tags: [security, audit, health, devops, free]
icon: 🛡️
homepage: https://github.com/bamontejano/skill-doctorbot-healthcheck
---

# DoctorBot: 健康检查（免费版）🛡️

> **您的 OpenClaw 主机安全吗？让我们来了解一下。**

该技能会对运行 OpenClaw 的机器进行 **只读** 的安全性和健康状况审计。该过程完全不会对您的系统造成任何影响。

## 🚀 免费功能

- **OpenClaw 安全审计：** 运行 `openclaw security audit --deep` 命令，以检测 OpenClaw 设置中的安全漏洞。
- **更新状态检查：** 通过 `openclaw update status` 命令检查 OpenClaw 是否已过时。
- **防火墙与端口扫描：** 扫描主机的防火墙状态（`ufw`、`firewalld`），并列出开放的端口。
- **系统基本信息：** 检查操作系统版本和正在运行的服务。

## 🛠️ 使用方法

只需告诉您的代理：“运行健康检查。”

该技能会引导您完成整个过程，并提供一份包含 **“系统健康评分”** 的简单报告。

## 升级到专业版（Upgrade to Pro）

### 🩺 升级到 DoctorBot: HealthCheck Pro

免费扫描发现了关键问题吗？**专业版** 可以自动修复这些问题。

**专业版功能：**
- **自动修复：** 根据安全最佳实践自动强化您的系统。
- **防火墙管理：** 关闭不必要的端口。
- **SSH 安全设置：** 禁用密码登录，强制使用密钥登录。
- **定期审计：** 每日或每周自动进行检查，并在新风险出现时提醒您。

**如需升级，请在 ClawHub 上查找 `DoctorBot: HealthCheck Pro`。**

---
*由 DoctorBot-x402 维护。为了维护一个健康的代理生态系统，请使用该工具。*