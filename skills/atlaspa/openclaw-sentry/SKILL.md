---
name: openclaw-sentry
user-invocable: true
metadata: {"openclaw":{"emoji":"🔑","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Sentry

该工具会扫描代理工作空间中可能泄露的敏感信息，包括 API 密钥、令牌、密码、私钥等，这些信息绝不应该以明文形式存在。

## 问题所在

代理工作空间中会积累各种敏感信息：配置文件中存放 API 密钥，内存日志中保存令牌，环境文件中包含密码。哪怕仅有一个敏感信息泄露，也可能导致整个基础设施的安全受到威胁。现有的敏感信息扫描工具主要针对 Git 仓库进行检测，但并未监控代理工作空间本身。

## 命令选项

### 全面扫描

扫描工作空间中的所有文件，查找敏感信息和高风险文件。

```bash
python3 {baseDir}/scripts/sentry.py scan --workspace /path/to/workspace
```

### 检查单个文件

检查指定的文件是否存在敏感信息。

```bash
python3 {baseDir}/scripts/sentry.py check MEMORY.md --workspace /path/to/workspace
```

### 快速状态检查

提供关于敏感信息泄露风险的简短摘要。

```bash
python3 {baseDir}/scripts/sentry.py status --workspace /path/to/workspace
```

## 支持检测的来源

| 提供方 | 检测模式 |
|----------|----------|
| **AWS** | 访问密钥（AKIA...）、秘密密钥 |
| **GitHub** | PAT（ghp_, gho_, ghs_, ghr_, github_pat_） |
| **Slack** | 机器人/用户令牌（xox...）、Webhook |
| **Stripe** | 秘密密钥（sk_live_）、可公开使用的密钥 |
| **OpenAI** | API 密钥（sk-...） |
| **Anthropic** | API 密钥（sk-ant-...） |
| **Google** | API 密钥（AIza...）、OAuth 密钥 |
| **Azure** | 存储账户密钥 |
| **通用** | API 密钥、密码、 bearer 令牌、连接字符串 |
| **加密** | PEM 格式的私钥（.key/.pem/.p12 文件） |
| **数据库** | 包含敏感信息的 PostgreSQL/MySQL/MongoDB/Redis URL |
| **JWT** | JSON Web 令牌 |
| **环境变量** | .env 文件中的环境变量 |

## 返回码

- `0`：未发现敏感信息
- `1`：检测到高风险文件
- `2`：发现关键敏感信息

## 无需外部依赖

仅依赖 Python 标准库，无需安装任何第三方库（如 pip），也不进行网络请求。所有操作都在本地完成。

## 跨平台兼容性

支持与 OpenClaw、Claude Code、Cursor 以及任何遵循 Agent Skills 规范的工具配合使用。