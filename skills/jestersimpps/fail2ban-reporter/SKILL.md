---
name: fail2ban-reporter
description: "**自动将 fail2ban 禁止的 IP 地址报告到 AbuseIPDB，并通过 Telegram 通知**  
适用于监控服务器安全、举报攻击者或检查被禁止的 IP 地址的场景。该功能会实时监控 fail2ban 的禁用操作，将新生成的禁用记录报告至 AbuseIPDB，并发送警报通知。"
---

# fail2ban Reporter

该工具用于监控 fail2ban 的封禁记录，并自动将攻击者信息报告给 AbuseIPDB。

## 设置

1. 在 https://www.abuseipdb.com/account/api 获取免费的 AbuseIPDB API 密钥。
2. 将密钥保存到配置文件中：`pass insert abuseipdb/api-key`
3. 安装监控脚本：`bash {baseDir}/scripts/install.sh`

## 手动使用

### 报告所有当前被封禁的 IP 地址

```bash
bash {baseDir}/scripts/report-banned.sh
```

### 检查特定的 IP 地址

```bash
bash {baseDir}/scripts/check-ip.sh <ip>
```

### 显示封禁统计信息

```bash
bash {baseDir}/scripts/stats.sh
```

## 自动报告

安装脚本会配置一个自动触发机制，用于在发生新的封禁事件时自动向 AbuseIPDB 报告。

```bash
bash {baseDir}/scripts/install.sh    # install auto-reporting
bash {baseDir}/scripts/uninstall.sh  # remove auto-reporting
```

## 与 Heartbeat 服务集成

将相关配置添加到 HEARTBEAT.md 文件中，以实现定期检查新的封禁记录：

```markdown
- [ ] Check fail2ban stats and report any unreported IPs to AbuseIPDB
```

## 工作流程

1. 当 fail2ban 封禁某个 IP 地址时，会触发 `report-single.sh` 脚本。
2. 脚本会以“SSH 暴力攻击”类别将封禁信息报告给 AbuseIPDB。
3. （如果已配置）会通过 Telegram 发送通知。
4. 报告日志会被保存到 `/var/log/abuseipdb-reports.log` 文件中。

## API 参考

请参阅 [references/abuseipdb-api.md](references/abuseipdb-api.md) 以获取完整的 API 文档。