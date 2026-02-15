---
name: phoenix-shield
description: 自愈型备份与更新系统，具备智能回滚功能。该系统通过更新后自动监控系统健康状况，并在需要时从备份中恢复数据，从而有效防止更新失败带来的风险。其主要特性包括：金丝雀部署测试（canary deployment testing）、健康基线监控（health baselines）、智能回滚机制（smart rollback），以及全天候自动化监控（24/7 automated monitoring）。适用于执行关键系统更新、管理生产环境中的部署任务，或确保服务的高可用性（high availability）。通过预先检查（pre-flight checks）、数据完整性验证（integrity verification）及自动恢复流程（automatic recovery workflows），有效防止系统停机（downtime）。
---

# PhoenixShield 🔥🛡️

> “就像凤凰一样，您的系统能够从自身的备份中重生。”

这是一个具备自我修复功能的备份与更新系统，同时支持智能回滚机制。

## 为什么选择PhoenixShield？

**问题：**系统更新可能会出现故障，导致服务中断并引发停机时间。

**解决方案：**PhoenixShield提供了全面的安全保障机制，在出现问题时能够自动回滚到之前的状态。

**优势：**
- 🔄 **自动恢复**：更新失败时系统能够自动自我修复
- 🧪 **金丝雀测试**：在生产环境之前先测试更新内容
- 📊 **健康监控**：更新后进行24小时持续监控
- ⚡ **智能回滚**：仅恢复发生变更的组件
- 🛡️ **零停机时间**：在可能的情况下实现平滑降级

---

## 快速入门

### 1. 初始化PhoenixShield

```bash
phoenix-shield init --project myapp --backup-dir /var/backups
```

### 2. 创建更新前的系统快照

```bash
phoenix-shield snapshot --name "pre-update-$(date +%Y%m%d)"
```

### 3. 安全更新并实现自动恢复

```bash
phoenix-shield update \
  --command "npm update" \
  --health-check "curl -f http://localhost/health" \
  --auto-rollback
```

### 4. 更新后进行监控

```bash
phoenix-shield monitor --duration 24h --interval 5m
```

---

## 核心功能

### 1. 更新前检查

在开始任何更新之前，PhoenixShield会进行以下检查：

```bash
phoenix-shield preflight
```

**检查内容：**
- ✅ 确保有足够的磁盘空间
- ✅ 没有正在运行的关键进程
- ✅ 备份存储可用
- ✅ 网络连接正常
- ✅ 服务运行状态正常

### 2. 智能备份

备份内容包括：
- 配置文件
- 数据库备份
- 系统状态信息
- 进程列表
- 网络连接信息
- 服务健康指标

### 3. 金丝雀部署

首先在隔离环境中测试更新内容：

```bash
phoenix-shield canary \
  --command "apt upgrade" \
  --test-duration 5m \
  --test-command "systemctl status nginx"
```

### 4. 生产环境更新

在安全机制的保护下执行更新：

```bash
phoenix-shield deploy \
  --command "npm install -g openclaw@latest" \
  --health-checks "openclaw --version" \
  --health-checks "openclaw health" \
  --rollback-on-failure
```

### 5. 更新后监控

**自动监控阶段：**
| 时间段 | 监控内容 |
|-----------|--------|
| 0-5分钟 | 关键服务是否正常运行 |
| 5-30分钟 | 所有服务是否响应正常 |
| 30-120分钟 | 集成测试 |
| 24小时 | 系统稳定性监控 |

```bash
phoenix-shield monitor --start
```

### 6. 智能回滚

当更新失败时，PhoenixShield会：
1. **尝试软恢复**：重启相关服务
2. **配置回滚**：恢复配置文件
3. **软件包回滚**：降级受影响的软件包
4. **完全恢复**：彻底恢复系统状态
5. **进入紧急模式**：仅保留最基本的服务，并通知管理员

---

## 工作流程示例

### 安全地更新OpenClaw

```bash
#!/bin/bash
# Update OpenClaw with PhoenixShield protection

phoenix-shield preflight || exit 1

phoenix-shield snapshot --name "openclaw-$(date +%Y%m%d)"

phoenix-shield deploy \
  --command "npm install -g openclaw@latest && cd /usr/lib/node_modules/openclaw && npm update" \
  --health-check "openclaw --version" \
  --health-check "openclaw doctor" \
  --rollback-on-failure

phoenix-shield monitor --duration 2h
```

### 更新Ubuntu服务器

```bash
phoenix-shield deploy \
  --command "apt update && apt upgrade -y" \
  --health-check "systemctl status nginx" \
  --health-check "systemctl status mysql" \
  --pre-hook "/root/notify-start.sh" \
  --post-hook "/root/notify-complete.sh" \
  --auto-rollback
```

### 多服务器更新

```bash
# Update multiple servers with PhoenixShield
SERVERS="server1 server2 server3"

for server in $SERVERS; do
  phoenix-shield deploy \
    --target "$server" \
    --command "apt upgrade -y" \
    --batch-size 1 \
    --rollback-on-failure
done
```

---

## 配置

创建 `phoenix-shield.yaml` 配置文件：

```yaml
project: my-production-app
backup:
  directory: /var/backups/phoenix
  retention: 10  # Keep last 10 backups
  compression: gzip

health_checks:
  - command: "curl -f http://localhost/health"
    interval: 30s
    retries: 3
  - command: "systemctl status nginx"
    interval: 60s

monitoring:
  enabled: true
  duration: 24h
  intervals:
    critical: 1m    # 0-5 min
    normal: 5m      # 5-30 min
    extended: 30m   # 30-120 min
    stability: 2h   # 2-24h

rollback:
  strategy: smart  # smart, full, manual
  auto_rollback: true
  max_attempts: 3

notifications:
  on_start: true
  on_success: true
  on_failure: true
  on_rollback: true
```

---

## 命令参考

| 命令 | 描述 |
|---------|-------------|
| `init` | 为项目初始化PhoenixShield |
| `snapshot` | 创建系统快照 |
| `backup` | 创建完整或增量备份 |
| `preflight` | 执行更新前的检查 |
| `canary` | 在隔离环境中测试更新 |
| `deploy` | 在保护机制下执行更新 |
| `monitor` | 启动更新后的监控 |
| `rollback` | 回滚到之前的系统状态 |
| `status` | 显示当前系统状态 |
| `history` | 查看更新历史记录 |
| `verify` | 验证备份文件的完整性 |

---

## 与CI/CD集成

```yaml
# GitHub Actions example
- name: Safe Deployment
  run: |
    phoenix-shield preflight
    phoenix-shield snapshot --name "deploy-$GITHUB_SHA"
    phoenix-shield deploy \
      --command "./deploy.sh" \
      --health-check "curl -f http://localhost/ready" \
      --auto-rollback
```

---

## 最佳实践

### 1. 必须执行更新前检查
```bash
# Bad
phoenix-shield deploy --command "apt upgrade"

# Good
phoenix-shield preflight && \
phoenix-shield deploy --command "apt upgrade"
```

### 2. 在生产环境前先测试回滚机制
```bash
phoenix-shield snapshot --name test
phoenix-shield deploy --command "echo test"
phoenix-shield rollback --dry-run  # See what would happen
```

### 3. 特别关注关键系统的更新
```bash
phoenix-shield deploy --command "major-update.sh"
phoenix-shield monitor --duration 48h  # Extended monitoring
```

### 4. 保持备份的完整性

```bash
# Regular cleanup
phoenix-shield cleanup --keep-last 10 --older-than 30d

# Verify backups
phoenix-shield verify --all
```

---

## 故障排除

### “更新前检查失败”
- 检查磁盘空间：`df -h`
- 确认备份位置存在
- 确保没有关键进程正在运行

### “回滚失败”
- 验证备份文件的完整性：`phoenix-shield verify`
- 从备份路径 `/var/backups/phoenix/` 手动恢复系统
- 如需紧急恢复，请联系管理员

### “健康检查失败”
- 延长监控时间：`phoenix-shield monitor --duration 48h`
- 查看服务日志：`journalctl -u myservice`
- 考虑仅回滚部分配置：`phoenix-shield rollback --config-only`

---

## 架构概述

```
┌─────────────────────────────────────┐
│        PhoenixShield Core           │
├─────────────────────────────────────┤
│ PreFlight │ Deploy │ Monitor │ Roll │
├─────────────────────────────────────┤
│   Backup Engine  │  Health Engine   │
├─────────────────────────────────────┤
│      Snapshots   │   Recovery       │
├─────────────────────────────────────┤
│   Config │ State │ Logs │ Metrics   │
└─────────────────────────────────────┘
```

---

## 安全性措施

- 备份数据在存储过程中会被加密
- 使用校验和来验证备份文件的完整性
- 对所有操作进行安全处理
- 提供详细的操作审计记录

---

## 许可证

采用MIT许可证，适用于个人和商业用途。

---

## 🔗 相关链接

- **ClawHub：** https://clawhub.com/skills/phoenix-shield
- **GitHub仓库：** https://github.com/mig6671/phoenix-shield
- **官方文档：** 本文件
- **作者：** @mig6671（OpenClaw团队成员）

---

**就像凤凰一样，您的系统能够从备份中重生 🔥🛡️**

---

## 致谢

该工具由OpenClaw团队成员@mig6671开发  
灵感来源于对系统更新过程的高可靠性需求。