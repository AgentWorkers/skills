---
name: otter
description: Otter.ai 转录命令行工具（CLI）：支持列出、搜索、下载会议记录，并将记录同步到客户关系管理（CRM）系统中。
version: 1.0.0
author: dbhurley
homepage: https://otter.ai
metadata:
  clawdis:
    emoji: "🦦"
    requires:
      bins: ["python3", "uv"]
      env:
        - OTTER_EMAIL
        - OTTER_PASSWORD
    optionalEnv:
      - TWENTY_API_URL
      - TWENTY_API_TOKEN
    primaryEnv: OTTER_EMAIL
---

# Otter.ai 文本转录 CLI

通过 Otter.ai CLI 可以管理会议记录，包括列出、搜索、下载、上传、生成摘要以及同步到 CRM 系统。

## 🔑 必需的凭据

| 变量 | 说明 | 获取方式 |
|----------|-------------|------------|
| `OTTER_EMAIL` | 你的 Otter.ai 账户邮箱 | 登录时使用的邮箱 |
| `OTTER_PASSWORD` | 你的 Otter.ai 密码 | 在 Otter 账户设置中配置 |

## 🔐 可选的凭据（用于同步到 CRM）

| 变量 | 说明 | 获取方式 |
|----------|-------------|------------|
| `TWENTY_API_URL` | Twenty CRM 的 API 端点地址 | 在 Twenty 系统的设置 → 开发者 → API 密钥中获取 |
| `TWENTY_API_TOKEN` | Twenty CRM 的 API 密钥 | 在 Twenty 系统的设置 → 开发者 → API 密钥中获取 |

## ⚙️ 设置

在 `~/.clawdis/clawdis.json` 文件中进行配置：
```json
{
  "skills": {
    "otter": {
      "env": {
        "OTTER_EMAIL": "you@company.com",
        "OTTER_PASSWORD": "your-password",
        "TWENTY_API_URL": "https://api.your-twenty.com",
        "TWENTY_API_TOKEN": "your-token"
      }
    }
  }
}
```

## 📋 命令

### 列出最近的转录记录
```bash
uv run {baseDir}/scripts/otter.py list [--limit 10]
```

### 获取完整转录内容
```bash
uv run {baseDir}/scripts/otter.py get <speech_id>
```

### 搜索转录记录
```bash
uv run {baseDir}/scripts/otter.py search "quarterly review"
```

### 下载转录文件
```bash
uv run {baseDir}/scripts/otter.py download <speech_id> [--format txt|pdf|docx|srt]
```

### 上传音频以生成转录内容
```bash
uv run {baseDir}/scripts/otter.py upload /path/to/audio.mp3
```

### 获取 AI 生成的摘要
```bash
uv run {baseDir}/scripts/otter.py summary <speech_id>
```

### 同步到 Twenty CRM
```bash
uv run {baseDir}/scripts/otter.py sync-twenty <speech_id>
uv run {baseDir}/scripts/otter.py sync-twenty <speech_id> --company "Client Name"
```

## 📤 输出格式

所有命令都支持使用 `--json` 选项以机器可读的格式输出结果：
```bash
uv run {baseDir}/scripts/otter.py list --json
```

## 🔗 与 Twenty CRM 的集成

同步到 Twenty CRM 时，会创建以下内容：
- 包含转录记录的标题、日期、时长和完整文本的 **笔记**；
- 如果使用了 `--company` 参数，还会自动添加与会议相关的 **链接**。

## ⚠️ 注意事项

- 需要 Otter.ai 账户（建议使用企业账户以访问 API）；
- 本工具使用了 Otter.ai 的非官方 API；
- 使用 SSO（单点登录）的用户需要在 Otter 账户设置中创建密码；
- 可能存在速率限制。

## 📦 安装

```bash
clawdhub install otter
```