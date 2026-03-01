---
name: Google Services (gog CLI)
description: 通过 gog CLI 管理 Google API 的 OAuth 令牌刷新。
slug: google-gog
tags: [google, gmail, drive, oauth, gog, credentials]
---
# Google Services (gog CLI)

## 配置

- **账户：** `xtyherry@gmail.com`
- **凭据：** `~/.openclaw/credentials/client_secret.json`
- **令牌存储：** 操作系统密钥环（自动加密）

## 令牌更新机制

令牌会在每次 API 调用时自动更新，无需用户手动操作。

**如果令牌无效：**
```bash
gog auth add xtyherry@gmail.com --services gmail,drive,calendar --manual --force-consent
```

**用于自动化任务（如 cron 或无头脚本）：**
```bash
export GOG_KEYRING_BACKEND=file
export GOG_KEYRING_PASSWORD=<password>
gog auth list --check  # Check token validity and expiration
```

## 快速命令

```bash
# Gmail: send, search
gog gmail send user@example.com --subject "Hi" --body "Message"
gog gmail search "newer_than:7d"

# Drive: list, upload, download
gog drive ls /
gog drive upload file.txt /
gog drive download /file.txt ./output.txt

# Check token health
gog auth list --check
```