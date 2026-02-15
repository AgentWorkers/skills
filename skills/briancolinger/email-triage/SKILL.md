---
name: email-triage
description: 通过本工具，可以利用本地部署的 Ollama LLM（Large Language Model）进行 IMAP 邮件扫描和分类。该工具能够自动识别未读邮件，并将其分为“紧急”、“需要回复”、“信息性”或“垃圾邮件”等类别，同时将重要信息呈现给处理人员。该系统可独立运行，同时支持基于启发式的备用分类方式；虽然 Ollama 是可选组件，但强烈推荐使用。
---

# 邮件分类与优先级处理

该脚本会扫描您的 IMAP 收件箱，将邮件分类为不同的优先级类别，并筛选出需要关注的邮件。它使用本地的 LLM（Ollama）进行智能分类；当 Ollama 不可用时，会采用基于规则的启发式方法作为备用方案。

## 先决条件

- **Python 3.10 或更高版本**
- **可访问 IMAP 的电子邮件账户**（Gmail、Fastmail 或自托管邮箱等）
- **Ollama**（可选）——用于基于 AI 的邮件分类。如果没有 Ollama，脚本会使用基于关键词的启发式方法，这些方法对于常见邮件模式仍然非常有效。

## 邮件类别

| 图标 | 类别 | 说明 |
|------|----------|-------------|
| 🔴 | `紧急` | 系统故障、安全警报、法律相关事务、支付失败、时间敏感的邮件 |
| 🟡 | `需要回复` | 商务咨询、问题、需要处理的操作事项 |
| 🔵 | `信息类` | 收据、确认邮件、新闻通讯、自动通知 |
| ⚫ | `垃圾邮件` | 市场营销邮件、促销信息、未经请求的垃圾邮件 |

## 配置

所有配置都通过环境变量完成：

| 变量 | 是否必填 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `IMAP_HOST` | ✅ | — | IMAP 服务器主机名 |
| `IMAP_PORT` | — | `993` | IMAP 端口（SSL） |
| `IMAP_USER` | ✅ | — | IMAP 用户名/电子邮件地址 |
| `IMAP_PASS` | ✅ | — | IMAP 密码或应用程序专用的密码 |
| `EMAIL_TRIAGE_STATE` | — | `./data/email-triage.json` | JSON 状态文件的路径 |
| `OLLAMA_URL` | — | `http://127.0.0.1:11434` | Ollama API 的端点地址 |
| `OLLAMA_MODEL` | — | `qwen2.5:7b` | 用于分类的 Ollama 模型 |

## 命令

```bash
# Scan inbox and classify new unread emails
python3 scripts/email-triage.py scan

# Scan with verbose output (shows each classification)
python3 scripts/email-triage.py scan --verbose

# Dry run — scan and classify but don't save state
python3 scripts/email-triage.py scan --dry-run

# Show unsurfaced important emails (urgent + needs-response)
python3 scripts/email-triage.py report

# Same as report but JSON output (for programmatic use)
python3 scripts/email-triage.py report --json

# Mark reported emails as surfaced (so they don't appear again)
python3 scripts/email-triage.py mark-surfaced

# Show triage statistics
python3 scripts/email-triage.py stats
```

## 工作原理

1. 通过 SSL 连接到 IMAP 服务器，获取未读邮件（每次扫描最多获取 20 封邮件）。
2. 通过邮件 ID（或主题和发件人的哈希值）来消除邮件重复，确保邮件不会被重复分类。
3. 如果可用，使用 Ollama 对每封邮件进行分类；否则，采用基于关键词的启发式方法进行分类。
4. 将邮件分类结果存储在本地 JSON 文件中，记录邮件的类别、分类原因以及是否已被处理。
5. 仅筛选出未处理的紧急邮件和需要回复的邮件，并按优先级排序后显示结果。
6. 为已处理的邮件添加标记，防止它们再次出现在后续报告中。
7. 自动删除最旧的 200 条记录，以避免状态文件无限增长。

## 集成建议

- **定期执行任务**：定期运行 `scan` 命令，然后使用 `report --json` 命令查看需要处理的邮件。
- **工作流程**：`scan` → `report --json` → 根据结果采取行动 → `mark-surfaced`。
- **无 Ollama 时**：启发式分类器可以很好地处理常见类型的邮件（如自动通知、营销邮件、紧急邮件）；Ollama 可以为模糊或复杂的邮件提供更精确的分类。
- **应用程序密码**：如果您的邮件服务提供 2FA（双重身份验证），请为 IMAP 访问生成一个应用程序专用的密码。