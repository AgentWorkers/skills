---
name: arc-shield
version: 1.0.0
category: security
tags: [security, sanitization, secrets, output-filter, privacy]
requires: [bash, python3]
author: OpenClaw
description: **代理响应的输出清理功能**——防止意外泄露机密信息
---

# arc-shield

**用于清理代理响应中的敏感信息。** 在所有出站消息离开代理之前，会扫描其中是否包含泄露的秘密信息、令牌、密钥、密码和个人身份信息（PII）。

⚠️ **这不是一个输入扫描工具** — `clawdefender` 已经负责处理输入数据的扫描工作。`arc-shield` 的作用是作为 **输出过滤器**，用于捕获代理在响应中可能无意中包含的敏感内容。

## 为什么需要它

代理可以访问敏感数据，例如：1Password 密码库、环境变量、配置文件以及钱包密钥。在以下情况下，代理可能会不小心将这些敏感信息包含在响应中：
- 调试并显示完整的命令输出时
- 复制包含敏感信息的文件内容时
- 生成包含真实凭据的代码示例时
- 总结包含令牌的日志时

`arc-shield` 会在这些敏感信息到达 Discord、Signal、X 或任何外部渠道之前将其拦截。

## 它能检测到什么

### 🔴 **严重级别（在 `--strict` 模式下会阻止这些内容）**
- **API 密钥和令牌**：1Password（`ops_*`）、GitHub（`ghp_*`）、OpenAI（`sk_*`）、Stripe、AWS、Bearer 令牌
- **密码**：如 `password=...` 或 `passwd: ...` 这样的赋值语句
- **私钥**：以太坊密钥（0x 开头的 64 位十六进制字符串）、SSH 密钥、PGP 密钥
- **钱包助记词**：12/24 个单词的恢复短语
- **个人身份信息（PII）**：社会安全号码、信用卡号码
- **平台令牌**：Slack、Telegram、Discord 的令牌

### 🟠 **警告级别（会发出强烈警告）**
- **高熵字符串**：长度大于 16 个字符的字符串，其香农熵值大于 4.5（用于检测新型的敏感信息模式）
- **信用卡号码**：16 位数的信用卡号码
- **Base64 编码的凭据**：看起来像令牌的长 Base64 字符串

### 🟡 **信息提示级别**
- **敏感文件路径**：`~/.secrets/*` 文件夹中的文件路径，或包含 “password”、“token”、“key” 等关键词的路径
- **环境变量**：以 `ENV_VAR=secret_value` 形式导出的变量
- **数据库 URL**：包含凭据的连接字符串

## 安装

```bash
cd ~/.openclaw/workspace/skills
git clone <arc-shield-repo> arc-shield
chmod +x arc-shield/scripts/*.sh arc-shield/scripts/*.py
```

或者，您可以将其作为技能包下载。

## 使用方法

### 命令行使用

```bash
# Scan agent output before sending
agent-response.txt | arc-shield.sh

# Block if critical secrets found (use before external messaging)
echo "Message text" | arc-shield.sh --strict || echo "BLOCKED"

# Redact secrets and return sanitized text
cat response.txt | arc-shield.sh --redact

# Full report
arc-shield.sh --report < conversation.log

# Python version with entropy detection
cat message.txt | output-guard.py --strict
```

### 与 OpenClaw 代理集成

#### **预发送钩子（推荐使用）**

将其添加到您的消息处理技能或包装器中：

```bash
#!/bin/bash
# send-message.sh wrapper

MESSAGE="$1"
CHANNEL="$2"

# Sanitize output
SANITIZED=$(echo "$MESSAGE" | arc-shield.sh --strict --redact)
EXIT_CODE=$?

if [[ $EXIT_CODE -eq 1 ]]; then
    echo "ERROR: Message contains critical secrets and was blocked." >&2
    exit 1
fi

# Send sanitized message
openclaw message send --channel "$CHANNEL" "$SANITIZED"
```

#### 手动管道处理

在任何外部消息发送之前，使用以下命令：

```bash
# Generate response
RESPONSE=$(agent-generate-response)

# Sanitize
CLEAN=$(echo "$RESPONSE" | arc-shield.sh --redact)

# Send
signal send "$CLEAN"
```

### 测试

提供了以下测试用例：
- 真实的泄露信息（如 1Password 令牌、Instagram 密码、钱包助记词）
- 防止误报（正常 URL、电子邮件地址、文件路径）
- 检查信息隐藏的准确性
- 检查严格模式下的阻止效果

## 配置

敏感信息模式定义在 `config/patterns.conf` 文件中：

```conf
CRITICAL|GitHub PAT|ghp_[a-zA-Z0-9]{36,}
CRITICAL|OpenAI Key|sk-[a-zA-Z0-9]{20,}
WARN|Secret Path|~\/\.secrets\/[^\s]*
```

您可以编辑该文件以添加自定义模式或调整警告级别。

## 模式选项

| 模式 | 行为 | 结束代码 | 使用场景 |
|------|----------|-----------|----------|
| 默认 | 直接传递消息并将在 stderr 中显示警告 | 0 | 开发阶段、日志记录 |
| `--strict` | 遇到严重违规时阻止消息发送 | 结束代码为 1 | 用于生产环境的出站消息 |
| `--redact` | 用 “[REDACTED:TYPE]” 替换敏感信息 | 0 | 适用于安全日志记录和审计 |
| `--report` | 仅进行分析，不传递原始消息 | 0 | 用于审计对话记录 |

## 熵值检测

Python 版本（`output-guard.py`）使用香农熵值分析来检测不符合正则表达式的敏感信息：

```python
# Detects high-entropy strings like:
kJ8nM2pQ5rT9vWxY3zA6bC4dE7fG1hI0  # Novel API key format
Zm9vOmJhcg==                      # Base64 credentials
```

默认阈值：**4.5 比特**（可通过 `--entropy-threshold` 参数进行调整）

## 性能

- **Bash 版本**：处理典型消息（小于 1KB）的速度约为 10 毫秒
- **Python 版本**：包含熵值分析时速度约为 50 毫秒
- **无外部依赖**：仅使用 bash 和 Python 标准库

该工具运行速度足够快，可以实时处理所有出站消息，而不会造成明显延迟。

## 实际应用案例

从我们自己的代理会话中捕获的敏感信息示例：

```bash
# 1Password token
"ops_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Instagram password in debug output
"instagram login: user@example.com / MyInsT@Gr4mP4ss!"

# Wallet mnemonic in file listing
"cat ~/.secrets/wallet-recovery-phrase.txt
abandon ability able about above absent absorb abstract..."

# GitHub PAT in git config
"[remote "origin"]
url = https://ghp_abc123:@github.com/user/repo"
```

所有这些敏感信息在到达外部渠道之前都被 `arc-shield` 拦截了。

## 最佳实践

1. **对于外部消息（如 Discord、Signal、X、电子邮件），始终使用 `--strict` 模式**  
2. **对于需要日后查看的日志，使用 `--redact` 模式**  
3. **在添加自定义模式后运行测试，以确保没有误报**  
4. **同时使用 bash 和 Python 版本，以实现最大程度的覆盖**  
5. **不要仅依赖此工具** — 应教育代理避免在响应中包含敏感信息（请参考 AGENTS.md 中关于输出清理的指导原则）

## 限制

- **缺乏上下文理解**：无法区分 “这是我的密码：X”（错误）和 “将密码设置为 X”（指令）  
- **无法理解语句的语义**：无法检测到 “我的令牌在之前的消息中”  
- **基于模式检测**：新的敏感信息格式需要更新相应的检测规则  

建议将 `arc-shield` 与代理指令和精心设计的提示语句结合使用。

## 集成示例

完整的 OpenClaw 代理集成示例：

```bash
# In your agent's message wrapper
send_external_message() {
    local message="$1"
    local channel="$2"
    
    # Pre-flight sanitization
    if ! echo "$message" | arc-shield.sh --strict > /dev/null 2>&1; then
        echo "ERROR: Message blocked by arc-shield (contains secrets)" >&2
        return 1
    fi
    
    # Double-check with entropy detection
    if ! echo "$message" | output-guard.py --strict > /dev/null 2>&1; then
        echo "ERROR: High-entropy secret detected" >&2
        return 1
    fi
    
    # Safe to send
    openclaw message send --channel "$channel" "$message"
}
```

## 故障排除

**正常文本中出现误报的情况：**
- 调整熵值阈值：`output-guard.py --entropy-threshold 5.0`
- 编辑 `config/patterns.conf` 以优化正则表达式模式  
- 在模式文件中添加例外情况  

**敏感信息未被检测到的情况：**
- 检查模式文件的覆盖范围  
- 使用 `--report` 参数运行工具，查看实际检测的内容  
- 使用 `tests/run-tests.sh` 进行测试  
- 考虑降低熵值阈值（但要注意避免误报）  

**性能问题：**
- 仅使用 Bash 版本（可跳过熵值检测）  
- 通过 `head -c 10000` 限制输入消息的长度  
- 在后台运行 `arc-shield.sh --report &`  

## 贡献方式

您可以根据以下格式向 `config/patterns.conf` 文件中添加新的检测模式：

```
SEVERITY|Category Name|regex_pattern
```

部署前请使用 `tests/run-tests.sh` 进行测试。

## 许可证

MIT 许可证 — 可自由使用，但请保护好您的敏感信息。

---

**请记住**：`arc-shield` 是您的安全保障措施，而非解决问题的唯一方案。应训练代理避免在响应中包含任何敏感信息。该工具用于捕捉错误行为，而非恶意行为。