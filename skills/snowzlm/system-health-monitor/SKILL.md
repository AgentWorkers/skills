---
name: system-health-monitor
description: "系统健康与安全监控技能，采用8层监控体系。提供实时的系统健康状况评估、安全事件报告以及性能分析功能。适用于以下场景：检查系统状态、监控安全事件或生成系统健康报告。"
homepage: https://github.com/openclaw/openclaw
author: "ZLMbot 🦞"
license: MIT
metadata: { "openclaw": { "emoji": "🏥", "requires": { "bins": ["systemctl", "jq"], "os": "linux" }, "tags": ["monitoring", "security", "health", "system"] } }
---
# 系统健康监控

这是一个用于系统健康和安全性监控的技能，采用了8层监控架构。

## 描述

该技能通过与8层监控基础设施集成，提供系统性能和安全的实时状态报告、警报以及历史数据分析功能。

## 使用场景

✅ **适用场景：**
- 检查系统的整体健康状况
- 监控安全事件和威胁
- 分析系统性能趋势
- 生成健康报告
- 调查监控警报
- 查看fail2ban的运行情况

❌ **不适用场景：**
- 修改系统配置 → 使用系统管理工具
- 安装软件包 → 使用apt/yum
- 管理用户账户 → 使用useradd/usermod

## 使用方法

### 快速健康检查
```bash
/health status
```

### 详细系统报告
```bash
/health report
```

### 检查特定监控层（1-8）
```bash
/health layer 3      # Check heartbeat monitoring
/health layer 6      # Check package integrity monitoring
```

### 安全概览
```bash
/health security
```

## 配置

配置文件位于 `config/health-monitor.json`（可选）：
```json
{
  "alert_threshold": 80,
  "report_frequency": "hourly",
  "notify_on_critical": true,
  "telegram_channel_id": "",
  "monitored_services": [
    "ssh-login-monitor",
    "heartbeat-monitor",
    "package-integrity-monitor"
  ]
}
```

## 监控层（8层监控系统）

| 监控层 | 服务 | 集成方式 |
|-------|---------|-------------|
| 1     | SSH登录监控 | 实时登录跟踪 |
| 2     | 心跳监控 | 高级健康检查 |
| 3     | 出站流量监控 | 网络安全 |
| 4     | UFW防火墙 | 网络层防护 |
| 5     | 软件包完整性监控 | 软件安全 |
| 6     | 报告监控 | 自动化报告生成 |
| 7     | 系统维护监控 | 系统维护任务 |
| 8     | 内部安全监控 | 网络威胁检测 |

## 特点

- **实时健康评分**：根据各监控层的状态给出0-100分的评分
- **警报系统**：通过Telegram发送关键问题警报
- **历史分析**：跟踪系统性能趋势
- **安全仪表板**：统一显示安全状态
- **自动化报告**：生成每日/每周的健康报告

## 命令

### 获取当前状态
```bash
bash scripts/health-check.sh status
```

### 生成报告
```bash
bash scripts/health-check.sh report
```

## 系统要求

- **操作系统**：基于systemd的Linux发行版
- 必须运行OpenClaw Gateway
- 必须启用systemd监控服务
- 所需依赖包：`systemctl`, `jq`
- 可选依赖包：`fail2ban`, `ufw`（用于安全功能）

## 技能开发详情

- **版本**：1.1.1
- **作者**：ZLMbot 🦞
- **创建时间**：2026-02-28
- **更新时间**：2026-03-01（修复了安全扫描相关问题）
- **许可证**：MIT许可证

---
**状态**：🟢 正在运行  
**监控系统**：✅ 8层监控系统  
**最后更新时间**：2026-03-01