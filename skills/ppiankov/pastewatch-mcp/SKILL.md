---
name: pastewatch-mcp
description: OpenClaw代理的专用秘密数据保护服务器。该服务器可防止API密钥、数据库凭据、SSH密钥、电子邮件地址、IP地址、JWT令牌以及其他29种类型的敏感信息泄露给大型语言模型（LLM）提供商。系统包含用于阻止泄露敏感数据的Shell命令的防护机制、用于检测异常行为的“金丝雀令牌”（canary tokens）、加密存储库功能，以及用于扫描Git历史记录的审计工具。适用于在处理可能包含敏感信息的文件时、配置代理安全设置时，或进行凭据泄露审计时使用。
metadata: {"openclaw":{"requires":{"bins":["pastewatch-cli","mcporter"]}}}
---
# Pastewatch MCP — 秘密数据保护工具

该工具可防止敏感数据泄露到大型语言模型（LLM）提供商处。它通过使用占位符来处理敏感信息，确保这些数据仅存储在本地。

**来源：** https://github.com/ppiankov/pastewatch

## 安装

```bash
# macOS
brew install ppiankov/tap/pastewatch

# Linux (binary + checksum)
curl -fsSL https://github.com/ppiankov/pastewatch/releases/latest/download/pastewatch-cli-linux-amd64 \
  -o /usr/local/bin/pastewatch-cli
curl -fsSL https://github.com/ppiankov/pastewatch/releases/latest/download/pastewatch-cli-linux-amd64.sha256 \
  -o /tmp/pastewatch-cli.sha256
cd /usr/local/bin && sha256sum -c /tmp/pastewatch-cli.sha256
chmod +x /usr/local/bin/pastewatch-cli
```

验证安装版本：`pastewatch-cli version`（版本号应大于或等于 0.18.0）

## MCP 服务器配置

```bash
mcporter config add pastewatch --command "pastewatch-cli mcp --audit-log /var/log/pastewatch-audit.log"
mcporter list pastewatch --schema  # 6 tools
```

## 代理集成（一键配置）

```bash
pastewatch-cli setup claude-code    # hooks + MCP config
pastewatch-cli setup cline          # MCP + hook instructions
pastewatch-cli setup cursor         # MCP + advisory
```

`--severity` 参数用于设置钩子拦截的敏感数据级别和 MCP 数据保护阈值；`--project` 参数用于配置项目级设置。

## MCP 工具列表

| 工具 | 功能 |
|------|---------|
| `pastewatch_read_file` | 读取文件，将其中的敏感信息替换为 `__PW{TYPE_N}__` 占位符 |
| `pastewatch_write_file` | 写入文件，将占位符替换为实际的敏感数据 |
| `pastewatch_check_output` | 在返回结果前检查文本中是否包含原始的敏感信息 |
| `pastewatch_scan` | 扫描文本中是否存在敏感数据 |
| `pastewatch_scan_file` | 扫描单个文件 |
| `pastewatch_scan_dir` | 递归扫描目录中的文件 |

## Guard — 阻止敏感数据泄露的命令

该工具与 Chainwatch 配合使用：Chainwatch 可拦截具有破坏性的命令，而 Guard 则能拦截可能导致敏感数据泄露的命令。

```bash
pastewatch-cli guard "cat .env"              # BLOCKED if .env has secrets
pastewatch-cli guard "psql -f migrate.sql"   # scans SQL file
pastewatch-cli guard "docker-compose up"     # scans referenced env_files
```

Guard 可识别以下类型的命令：
- Shell 内置命令：`cat`, `echo`, `env`, `printenv`, `source`, `curl`, `wget`
- 数据库命令行工具：`psql`, `mysql`, `mongosh`, `redis-cli`, `sqlite3`（包括连接字符串和 `-f` 参数、密码）
- 基础设施管理工具：`ansible`, `terraform`, `docker`, `kubectl`, `helm`（包括环境变量文件和配置文件）
- 脚本语言：`python`, `ruby`, `node`, `perl`, `php`（包括脚本文件参数）
- 文件传输工具：`scp`, `rsync`, `ssh`, `ssh-keygen`
- 管道链（`|`）和命令组合（`&&`, `||`, `;`）——每个部分都会被扫描
- 子shell 代码：`$(cat .env)` 和反引号表达式
- 重定向操作符：`>`, `>>`, `<`, `2>` — 用于扫描源文件

## Canary Tokens（测试用令牌）

生成格式正确但无实际功能的令牌，用于检测数据泄露情况：

```bash
pastewatch-cli canary generate --prefix myagent    # creates canaries for 7 secret types
pastewatch-cli canary verify                        # confirms detection rules catch them
pastewatch-cli canary check --log /var/log/app.log  # search logs for leaked canaries
```

## 加密存储

将敏感数据加密后存储在本地，而不是以明文形式保存在 `.env` 文件中：

```bash
pastewatch-cli --init-key                    # generate 256-bit key (.pastewatch-key, mode 0600)
pastewatch-cli fix --encrypt                 # secrets → ChaCha20-Poly1305 vault
pastewatch-cli vault list                    # show entries without decrypting
pastewatch-cli vault decrypt                 # export to .env for deployment
pastewatch-cli vault export                  # print export VAR=VALUE for shell
pastewatch-cli vault rotate-key              # re-encrypt with new key
```

## Git 历史记录扫描

通过指纹识别重复的敏感数据：相同的敏感数据在多个提交中只会被记录一次。

## 会话报告

```bash
pastewatch-cli report --audit-log /var/log/pastewatch-audit.log
pastewatch-cli report --format json --since 2026-03-01T00:00:00Z
```

## 支持的敏感数据类型

支持超过 29 种类型的敏感数据：
- AWS, Anthropic/OpenAI/HuggingFace/Groq 的密钥
- 数据库连接信息
- SSH 密钥
- JSON Web Tokens (JWTs)
- 电子邮件地址
- IP 地址
- 信用卡信息（Luhn 码）
- Slack/Discord 的 Webhook 令牌
- Azure 和 GCP 服务账户信息
- npm/PyPI/RubyGems/GitLab 的访问令牌
- Telegram 机器人的访问令牌

采用确定性正则表达式进行检测，不依赖机器学习或 API 调用。每次扫描耗时仅几微秒。

## 限制

- 该工具仅能防止敏感数据泄露到 LLM 提供商处，无法保护提示内容或代码结构的安全性。
- 如需实现完全的隐私保护，请使用本地模型。

---

**Pastewatch MCP v1.1**
作者：ppiankov
版权所有 © 2026 ppiankov
官方仓库：https://github.com/ppiankov/pastewatch
许可证：MIT

如果本文档出现在其他地方，请以上述仓库中的版本为准。