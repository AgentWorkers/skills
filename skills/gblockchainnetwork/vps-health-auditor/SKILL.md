---
summary: "VPS Health Auditor: Automated healthchecks for VPS/servers with Ollama-powered reports and recommendations."
description: "Runs comprehensive diagnostics (CPU, RAM, disk, network, services, uptime) via SSH/local exec, analyzes with Ollama LLM for actionable insights."
triggers:
  - "audit my VPS"
  - "check VPS health"
  - "server health report"
  - "VPS auditor"
read_when:
  - "VPS health" in message
  - "server check" in message
---

# VPS健康审计器 v1.0.0

## 🎯 目的
提前检测Linux虚拟私有服务器（VPS）/服务器上的问题。检查内容包括：
- 系统资源（CPU、内存、磁盘使用情况）
- 网络延迟/带宽
- 关键服务（SSH、Web服务器、数据库）
- 运行时间及日志记录
通过Ollama生成PDF/HTML格式的报告。

## 🚀 快速入门
```
!vps-health-auditor --host example.com --user root --key ~/.ssh/id_rsa
```

## 文件结构
- `scripts/healthcheck.sh`：跨平台审计脚本（适用于Ubuntu/CentOS/Debian系统）
- `reports/template.md`：用于生成报告的Ollama模板

## 自定义功能
您可以通过编辑`scripts/healthcheck.sh`来添加自定义的检查项，并将相应的Ollama模型添加到脚本的触发条件中以实现自定义审计功能。