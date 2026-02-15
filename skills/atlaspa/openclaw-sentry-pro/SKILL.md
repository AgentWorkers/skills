---
name: openclaw-sentry-pro
description: "**完整的安全扫描套件：**  
能够检测泄露的 API 密钥、令牌和凭据，自动屏蔽（redact）这些敏感信息，隔离受影响的文件，并强制执行 `.gitignore` 规则。这套功能包含在 openclaw-sentry（免费版本）中，同时还提供了自动化应对措施。"
user-invocable: true
metadata: {"openclaw":{"emoji":"🔑","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Sentry Pro

[openclaw-sentry](https://github.com/AtlasPA/openclaw-sentry) 的所有功能（免费版本）再加上自动化对策。

**免费版本可检测秘密信息；Pro 版本可彻底清除这些秘密信息。**

## 检测命令（免费版本也提供）

### 全面扫描

扫描工作区中的所有文件，查找秘密信息和高风险文件。

```bash
python3 {baseDir}/scripts/sentry.py scan --workspace /path/to/workspace
```

### 检查单个文件

检查特定文件中是否存在秘密信息。

```bash
python3 {baseDir}/scripts/sentry.py check MEMORY.md --workspace /path/to/workspace
```

### 快速状态

提供关于秘密信息泄露风险、文件隔离状态以及政策配置的简短总结。

```bash
python3 {baseDir}/scripts/sentry.py status --workspace /path/to/workspace
```

## Pro 版本的对策

### 遮盖秘密信息

在文件中找到秘密信息后，将其替换为掩码版本（例如，`sk-ant-abc...xyz` 会被替换为 `sk-ant-***REDACTED***`）。修改前会创建备份文件（`.bak`）。如果没有指定文件，则会覆盖工作区中的所有文件。

```bash
# Redact a single file
python3 {baseDir}/scripts/sentry.py redact config.json --workspace /path/to/workspace

# Redact all files in workspace
python3 {baseDir}/scripts/sentry.py redact --workspace /path/to/workspace
```

### 将文件隔离

将包含秘密信息的文件移动到 `.quarantine/sentry/` 目录，并附带元数据 JSON 文件，记录发现的内容、时间以及原始位置。

```bash
python3 {baseDir}/scripts/sentry.py quarantine .env --workspace /path/to/workspace
```

### 解除文件隔离

将被隔离的文件恢复到原始位置。

```bash
python3 {baseDir}/scripts/sentry.py unquarantine .env --workspace /path/to/workspace
```

### 防护措施

自动生成并更新 `.gitignore` 文件，以屏蔽常见的秘密信息模式（如 `.env`、`.pem`、`.key`、`credentials.json` 等文件），并创建 `.sentry-policy.json` 文件来指定需要执行的防护规则。

```bash
python3 {baseDir}/scripts/sentry.py defend --workspace /path/to/workspace
```

### 自动保护（全面扫描）

进行全面自动化扫描：扫描所有文件，自动屏蔽非关键文件中的秘密信息，将含有高密度秘密信息的文件隔离，并更新 `.gitignore` 文件。**这是启动会话时推荐的命令。**

```bash
python3 {baseDir}/scripts/sentry.py protect --workspace /path/to/workspace
```

## 推荐的集成方式

### 会话启动钩子（Claude Code）

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 scripts/sentry.py protect",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 心跳检测（OpenClaw）

将相关代码添加到 HEARTBEAT.md 文件中，以实现定期保护：

```
- Run secret scanning protection (python3 {skill:openclaw-sentry-pro}/scripts/sentry.py protect)
```

### 添加新配置或新秘密信息后

运行 `protect` 命令，自动屏蔽并隔离新暴露的秘密信息。

## 可检测的秘密信息类型

| 提供商 | 秘密信息模式 |
|----------|----------|
| **AWS** | 访问密钥（AKIA...）、秘密密钥 |
| **GitHub** | PAT（ghp_、gho_、ghs_、ghr_、github_pat_） |
| **Slack** | 机器人/用户令牌（xox...）、Webhook |
| **Stripe** | 秘密密钥（sk_live_）、可公开密钥 |
| **OpenAI** | API 密钥（sk-...） |
| **Anthropic** | API 密钥（sk-ant-...） |
| **Google** | API 密钥（AIza...）、OAuth 密钥 |
| **Azure** | 存储账户密钥 |
| **通用** | API 密钥、密码、bearer 令牌、连接字符串 |
| **加密** | PEM 私钥、.key/.pem/.p12 文件 |
| **数据库** | 包含凭据的 PostgreSQL/MySQL/MongoDB/Redis URL |
| **JWT** | JSON Web 令牌 |
| **环境变量** | .env 文件中的变量 |

## 对策总结

| 命令 | 功能 |
|---------|--------|
| `protect` | 全面扫描 + 自动屏蔽秘密信息 + 自动隔离 + 更新 `.gitignore` |
| `redact [file]` | 将秘密信息替换为掩码版本，并备份原始文件 |
| `quarantine <file>` | 将文件移至隔离目录，并附带元数据 |
| `unquarantine <file>` | 恢复被隔离的文件 |
| `defend` | 更新 `.gitignore` 文件并创建防护策略 |

## 无需外部依赖

仅依赖 Python 标准库，无需安装任何第三方库（如 pip），也不进行网络请求。所有操作均在本地执行。

## 跨平台兼容性

支持与 OpenClaw、Claude Code、Cursor 以及任何遵循 Agent Skills 规范的工具配合使用。