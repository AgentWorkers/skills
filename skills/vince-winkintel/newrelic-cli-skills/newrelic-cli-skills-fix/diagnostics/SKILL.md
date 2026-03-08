# 代理诊断

验证 New Relic 代理的配置、连接性以及报告状态。

---

## 运行全面诊断

```bash
newrelic diagnose run
```

检查内容：API 密钥的有效性、账户连接性、代理配置文件、日志路径、代理设置。

---

## 验证配置文件

```bash
# For .NET agent on Windows
newrelic diagnose validate \
  --config "C:\ProgramData\New Relic\.NET Agent\newrelic.config"

# For Linux
newrelic diagnose validate --config /etc/newrelic/newrelic.yml
```

---

## 检查代理是否正在报告数据

```bash
# Verify an app is actively sending data
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID --query "
  SELECT count(*)
  FROM Transaction
  WHERE appName = 'my-app'
  SINCE 10 minutes ago
"
# count = 0 means agent is not reporting

# Check entity reporting status
newrelic entity search --name "my-app" --type APPLICATION --domain APM | \
  jq '.[] | {name, reporting}'
```

---

## 检查代理版本

```bash
newrelic entity search --name "my-app" --type APPLICATION --domain APM | \
  jq '.[] | {name, tags: (.tags[] | select(.key == "agentVersion"))}'
```

---

## 连接性测试

```bash
# Test API key and account access
newrelic profile list
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID \
  --query "SELECT count(*) FROM NrIntegrationError SINCE 1 hour ago"
```

如果 `NrIntegrationError` 的数量大于 0，则表示数据导入存在问题。

---

## 常见问题

| 症状 | 可能原因 | 解决方案 |
|---|---|---|
| 应用程序显示“reporting: false” | 代理已停止运行或配置文件缺失 | 重启应用程序池/检查代理日志 |
| 事务数量为 0 | IIS 应用程序池在代理未初始化的情况下被回收 | 确保代理在启动时自动进行数据采集 |
| `NrIntegrationError` 数量过高 | 数据过大或格式不正确 | 检查代理日志中的序列化错误 |
| `alertSeverity: NOT_CONFIGURED` | 实体上没有设置警报条件 | 添加 NRQL 或 APM 指标条件 |

---

## .NET 代理（Windows/IIS）专属

```bash
# Check which apps are instrumented on a host
newrelic entity search --name "my-host" --type HOST | \
  jq '.[] | .tags[] | select(.key == "apmApplicationNames")'

# Agent logs location (Windows)
# C:\ProgramData\New Relic\.NET Agent\Logs\
```

---

## 配置文件管理

```bash
# List all profiles
newrelic profile list

# Switch profile
newrelic profile default --profile production

# Add a new profile
newrelic profile add \
  --profile staging \
  --apiKey $NEW_RELIC_API_KEY \
  --accountId $NEW_RELIC_ACCOUNT_ID \
  --region US
```