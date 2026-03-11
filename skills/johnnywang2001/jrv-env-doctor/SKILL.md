---
name: jrv-env-doctor
description: 验证 `.env` 文件以检测常见问题：检查是否存在泄露的敏感信息（如 AWS 密钥、GitHub 令牌、Stripe 密钥、JWT 等），查找重复的变量，标记空值，并将文件内容与 `.env.example` 模板进行比较，同时检测语法错误。适用于需要检查 `.env` 文件、审核环境变量、扫描敏感信息泄露情况、验证环境配置或对比 `.env` 文件与 `.env.example` 模板的场景。本工具无需任何外部依赖。
---
# Env Doctor

用于验证和审计 `.env` 文件中的敏感信息、重复项、语法错误以及缺失的变量。

## 快速入门

```bash
python3 scripts/env_doctor.py .env
python3 scripts/env_doctor.py .env --example .env.example
python3 scripts/env_doctor.py .env --strict --json
```

## 主要功能

- **敏感信息扫描** — 检测 AWS 密钥、GitHub 令牌、Stripe 令牌、Slack 令牌、Google API 令牌、JWT（JSON Web Tokens）、私钥等敏感数据。
- **重复项检测** — 标记被定义多次的变量。
- **示例文件对比** — 将 `.env` 文件与 `.env.example` 文件进行比较，以发现缺失或多余的变量。
- **语法验证** — 检查格式错误的行以及包含空格的未引用值。
- **占位符检测** — 警告使用诸如 “changeme” 或 “your-api-key-here” 这类占位符的变量。
- **退出代码**：0 表示文件正常；1 表示存在问题；2 表示有敏感信息泄露（适用于持续集成/持续部署流程）。
- **无依赖项** — 仅使用 Python 标准库。

## 参数选项

| 参数 | 说明 |
|------|-------------|
| `--example PATH` | 用于比较的 `.env.example` 文件路径 |
| `--json` | 以结构化 JSON 格式输出结果 |
| `--strict` | 将空值视为错误 |

## 可检测的敏感信息类型

AWS 访问/密钥、GitHub 令牌（ghp_、gho_、ghs_、ghu_、github_pat_）、Slack 令牌、Stripe 令牌、Google API 令牌、私钥、JWT、Twilio 令牌、SendGrid 令牌、Heroku API 令牌以及其他高熵度的敏感信息。