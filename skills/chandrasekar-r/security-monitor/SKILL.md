---
name: security-monitor
description: Clawdbot的实时安全监控功能：能够检测入侵行为、异常的API调用、不寻常的凭证使用模式，并在发生安全漏洞时发出警报。
---

# 安全监控技能

## 使用场景

运行持续的安全监控，以检测Clawdbot部署中的安全漏洞、入侵行为以及异常活动。

## 设置

无需外部依赖项。该工具以后台进程的形式运行。

## 使用方法

### 启动实时监控

```bash
node skills/security-monitor/scripts/monitor.cjs --interval 60
```

### 以守护进程模式（后台）运行

```bash
node skills/security-monitor/scripts/monitor.cjs --daemon --interval 60
```

### 监控特定威胁

```bash
node skills/security-monitor/scripts/monitor.cjs --threats=credentials,ports,api-calls
```

## 监控内容

| 威胁类型 | 检测方式 | 应对措施 |
|--------|-----------|----------|
| **暴力攻击** | 失败的登录尝试 | 发送警报并追踪IP地址 |
| **端口扫描** | 迅速的连接尝试 | 发送警报 |
| **进程异常** | 意外的进程启动 | 发送警报 |
| **文件更改** | 未经授权的文件修改 | 发送警报 |
| **容器健康状况** | Docker相关问题 | 发送警报 |

## 输出结果

- 控制台输出（stdout）
- 日志文件：`/root/clawd/clawdbot-security/logs/alerts.log`（格式为JSON）
- Telegram警报（可配置）

## 守护进程模式

使用systemd或PM2来保持监控功能的持续运行：

```bash
# With PM2
pm2 start monitor.cjs --name "clawdbot-security" -- --daemon --interval 60
```

## 与安全审计结合使用

先执行安全审计，然后开启持续监控：

```bash
# One-time audit
node skills/security-audit/scripts/audit.cjs --full

# Continuous monitoring
node skills/security-monitor/scripts/monitor.cjs --daemon
```

## 相关技能

- `security-audit`：一次性安全扫描工具（需单独安装）