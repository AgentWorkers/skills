---
name: phoenix-shield
description: 具有智能回滚功能的自修复备份与更新系统。通过更新后自动监控系统健康状况，并在需要时从备份中恢复数据，从而防止更新失败。该系统支持“金丝雀部署”测试（canary deployment testing）、健康基线（health baselines）、智能回滚（smart rollback）以及24/7全天候自动化监控。适用于执行关键系统更新、管理生产环境中的部署，或确保服务的高可用性。通过预更新检查（pre-update checks）、数据完整性验证（integrity verification）以及自动恢复工作流程（automatic recovery workflows），有效防止系统停机。
---

# PhoenixShield 🔥🛡️

> “就像凤凰一样，您的系统可以从自身的备份中重生。”

这是一个具备自我修复功能的备份与更新系统，同时支持智能回滚机制。

## 为什么选择 PhoenixShield？

**问题：** 系统更新可能会出现故障，导致服务中断和停机。

**解决方案：** PhoenixShield 提供了一套完整的安全保障机制，在出现问题时能够自动回滚到系统之前的状态。

**优势：**
- 🔄 **自动恢复**：当更新失败时，系统能够自动自我修复。
- 🧪 **金丝雀测试**：在正式部署前先在隔离环境中测试更新。
- 📊 **健康监控**：更新后进行24小时持续监控。
- ⚡ **智能回滚**：仅恢复发生变更的组件。
- 🛡️ **零停机时间**：在可能的情况下实现平滑的降级处理。

---

## 快速入门

### 1. 初始化 PhoenixShield

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

### 1. 更新前的检查

在开始任何更新之前，PhoenixShield 会执行以下检查：

```bash
phoenix-shield preflight
```

**检查内容：**
- ✅ 确保有足够的磁盘空间。
- ✅ 没有关键进程正在运行。
- ✅ 备份存储路径可访问。
- ✅ 网络连接正常。
- ✅ 系统服务处于健康状态。

### 2. 智能备份

备份内容包括：
- 配置文件
- 数据库备份
- 系统状态
- 进程列表
- 网络连接信息
- 系统健康指标的基线数据

### 3. 金丝雀部署

首先在隔离环境中测试更新：

```bash
phoenix-shield canary \
  --command "apt upgrade" \
  --test-duration 5m \
  --test-command "systemctl status nginx"
```

### 4. 正式更新

在安全保障机制的保护下执行更新：

```bash
phoenix-shield deploy \
  --command "npm install -g openclaw@latest" \
  --health-checks "openclaw --version" \
  --health-checks "openclaw health" \
  --rollback-on-failure
```

### 5. 更新后的监控

**自动监控阶段：**
| 时间段 | 监控内容 |
|---------|--------|
| 0-5分钟 | 关键服务是否正常运行 |
| 5-30分钟 | 所有服务是否响应正常 |
| 30-120分钟 | 进行集成测试 |
| 24小时内 | 监控系统稳定性 |

```bash
phoenix-shield monitor --start
```

### 6. 智能回滚

如果更新失败，PhoenixShield 会：
1. **尝试软恢复**：重启相关服务。
2. **配置回滚**：将配置恢复到更新前的状态。
3. **软件包回滚**：降级受影响的软件包。
4. **完全恢复**：彻底恢复系统到更新前的状态。
5. **进入紧急模式**：仅保留最低限度的服务，并通知管理员。

---

## 工作流程示例

### 安全地更新 OpenClaw

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

### 更新 Ubuntu 服务器

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
| `init` | 为项目初始化 PhoenixShield |
| `snapshot` | 创建系统快照 |
| `backup` | 创建完整或增量备份 |
| `preflight` | 运行更新前的检查 |
| `canary` | 在隔离环境中测试更新 |
| `deploy` | 在保护机制下执行更新 |
| `monitor` | 启动更新后的监控 |
| `rollback` | 回滚到之前的系统状态 |
| `status` | 显示当前系统状态 |
| `history` | 查看更新历史记录 |
| `verify` | 验证备份文件的完整性 |

---

## 与持续集成/持续部署（CI/CD）的集成

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

### 1. 必须始终执行更新前的检查
```bash
# Bad
phoenix-shield deploy --command "apt upgrade"

# Good
phoenix-shield preflight && \
phoenix-shield deploy --command "apt upgrade"
```

### 2. 在正式部署前测试回滚机制
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

### 4. 保持备份的整洁性
```bash
# Regular cleanup
phoenix-shield cleanup --keep-last 10 --older-than 30d

# Verify backups
phoenix-shield verify --all
```

---

## 故障排除

### “更新前的检查失败”
- 检查磁盘空间：`df -h`
- 确认备份路径存在。
- 确保没有关键进程正在运行。

### “回滚失败”
- 验证备份文件的完整性：`phoenix-shield verify`
- 从 `/var/backups/phoenix/` 目录手动恢复系统。
- 如需紧急恢复，请联系管理员。

### “健康检查失败”
- 延长监控时间：`phoenix-shield monitor --duration 48h`
- 查看相关服务的日志：`journalctl -u myservice`
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

- 备份数据在存储时会被加密。
- 使用校验和来验证备份文件的完整性。
- 对所有操作进行安全处理。
- 提供详细的操作审计记录。

---

## 许可证

采用 MIT 许可证，个人和商业用途均免费。

---

## 致谢

由 OpenClaw Agent (@mig6671) 开发。  
该工具的灵感来源于对系统更新过程的高安全性需求。