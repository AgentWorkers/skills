---
name: ssl-checker
description: "错误：必须使用 `--domain` 参数。当您需要 SSL 检查功能时，请使用该参数。该参数适用于以下选项：`ssl checker`、`domain`、`port`、`warn-days`、`format` 和 `output`。"
---
# ssl-checker

这是一个用于检查 SSL/TLS 证书的工具，能够验证证书的过期日期、颁发机构信息、主题信息、证书链的有效性、协议支持以及支持的加密算法。该工具会提供距离证书到期的剩余天数，并支持配置警告阈值，以便进行主动的证书管理。它使用 `openssl s_client` 和 Python3 进行验证，无需任何外部依赖。非常适合用于 DevOps 监控、安全审计和证书生命周期管理。

## 命令

| 命令 | 描述 |
|---------|-------------|

## 选项

- `--port <port>` — 连接的端口（默认值：443）
- `--format table|json|csv|text` — 输出格式（默认值：表格）
- `--output <file>` — 将输出结果保存到文件
- `--warn-days <days>` — 证书过期前的警告阈值（默认值：30 天）
- `--crit-days <days>` — 证书过期前的严重警告阈值（默认值：7 天）
- `--timeout <seconds>` — 连接超时时间（默认值：10 秒）
- `--sni <hostname>` — 替换 SNI 主机名
- `--verbose` — 显示完整的证书详细信息
- `--quiet` — 仅输出警告或错误信息

## 示例

```bash
# Full SSL check
bash scripts/main.sh check example.com

# Check expiry with custom thresholds
bash scripts/main.sh expiry example.com --warn-days 60 --crit-days 14

# Show certificate chain
bash scripts/main.sh chain example.com --format json

# Monitor multiple domains
bash scripts/main.sh monitor domains.txt --format json --output ssl-report.json

# Check non-standard port
bash scripts/main.sh check mail.example.com --port 993

# Verify chain trust
bash scripts/main.sh verify example.com --verbose
```

## 错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 成功 — 证书有效，且过期时间晚于警告阈值 |
| 1 | 警告 — 证书将在警告阈值内过期 |
| 2 | 严重警告 — 证书将在严重警告阈值内过期或已经过期 |
| 3 | 错误 — 连接失败或证书存在问题 |
---
💬 意见反馈与功能请求：https://bytesagain.com/feedback
由 BytesAgain 提供支持 | bytesagain.com