---
name: security-sentinel
description: 扫描工作区以检测安全漏洞、暴露的敏感信息以及配置错误。
tags: [security, scan, audit]
---

# Security Sentinel

这是一个用于 OpenClaw 工作区的安全扫描工具。

## 使用方法

```bash
node skills/security-sentinel/scan.js
```

## 功能特点
- 扫描文本文件中暴露的 API 密钥。
- 检查文件权限（基础功能）。
- 将扫描结果输出到标准输出（stdout）。

---

# Security Sentinel

这是一个专为 OpenClaw 工作区设计的安全扫描工具。

## 使用说明

```bash
node skills/security-sentinel/scan.js
```

## 主要功能
- 检查文本文件中是否存在泄露的 API 密钥。
- 基本权限检查功能。
- 将扫描结果以标准输出（stdout）的形式显示给用户。