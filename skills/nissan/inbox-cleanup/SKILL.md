---
version: 1.0.1
name: inbox-cleanup
description: "IMAP bulk email triage — pattern-based delete/archive with dry-run mode. Use when: cleaning up large email inboxes, bulk-deleting emails from specific senders or domains, archiving newsletter/digest emails, triaging email by sender domain or subject patterns. Supports IMAP STARTTLS (e.g. Proton Bridge), dry-run preview, YAML/JSON config for patterns, and processes UIDs (not sequence numbers) for reliable bulk ops."
metadata:
  {
      "openclaw": {
            "emoji": "\ud83d\udce7",
            "requires": {
                  "bins": [
                        "python3"
                  ],
                  "env": [
                        "OP_SERVICE_ACCOUNT_TOKEN"
                  ]
            },
            "primaryEnv": "OP_SERVICE_ACCOUNT_TOKEN",
            "network": {
                  "outbound": false,
                  "reason": "Connects to local Proton Bridge IMAP only (127.0.0.1)."
            }
      }
}
---

# 收件箱清理

批量处理 IMAP 邮件：根据发件人域名、主题关键词或自定义模式对邮件进行分类、删除或归档。

## 关键文件

- `scripts/inbox_cleanup.py` — 主清理脚本（默认为 dry-run 模式）
- `scripts/config_example.yaml` — 模式配置模板

## 快速入门

```bash
# Dry run (preview only — no changes)
python3 scripts/inbox_cleanup.py --config my_patterns.yaml --dry-run

# Live run
python3 scripts/inbox_cleanup.py --config my_patterns.yaml
```

## 必需的环境变量

```bash
IMAP_HOST=127.0.0.1          # IMAP server host
IMAP_PORT=1143               # IMAP port (use 993 for direct SSL, 1143 for Proton Bridge)
IMAP_USER=you@example.com    # IMAP username
IMAP_PASSWORD=yourpassword   # IMAP password
IMAP_STARTTLS=true           # true for STARTTLS (Proton Bridge), false for direct SSL
IMAP_SKIP_CERT_VERIFY=true   # true for self-signed certs (Proton Bridge)
ARCHIVE_FOLDER=Archive        # Folder name to archive to (must exist in mailbox)
```

或者使用 `--imap-*` 命令行参数。详情请参阅 `python3 scripts/inbox_cleanup.py --help`。

## 配置文件格式（YAML）

```yaml
delete_domains:
  - github.com
  - noreply.github.com
  - slack.com

archive_domains:
  - notion.so
  - coinbase.com

archive_keywords:
  - newsletter
  - digest
  - weekly roundup

delete_subject_patterns:
  - "^\\[GitHub\\]"

leave_domains:
  - important-bank.com
```

## 设计说明

- **UID 不是序列号**：脚本始终使用 `UID FETCH`/`UID STORE` 来避免在批量删除邮件时出现邮件编号重置的问题。
- **默认为 dry-run 模式**：执行操作前请务必预览结果。如需直接应用清理操作，请使用 `--no-dry-run` 参数。
- **批量获取邮件**：对于邮件量较大的收件箱，系统会以每批 50 封邮件的方式获取邮件头部信息。如需逐封获取邮件信息以进行可靠的 UID 跟踪，可以使用 `--one-at-a-time` 参数。
- **进度日志记录**：所有操作会记录在标准输出（stdout）中，包括每个域名的处理数量以及最终的处理结果（以 JSON 格式）。
- **STARTTLS 支持**：使用 Proton Bridge 时需要此功能（端口 1143，使用自签名证书）。

## 密码管理

凭据可以通过环境变量或 1Password 工具进行管理：

```bash
# Via env vars
export IMAP_PASSWORD="$(op read 'op://Vault/Email Account/password')"
python3 scripts/inbox_cleanup.py --config patterns.yaml
```