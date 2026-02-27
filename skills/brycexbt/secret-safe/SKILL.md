---
name: secret-safe
description: >
  **代理技能的安全API密钥和机密管理**  
  每当任务需要与外部服务进行身份验证、读取或写入API密钥、令牌、密码或任何形式的凭证时，都应使用此技能。此外，在审计其他技能是否存在凭证泄露风险时、用户询问如何安全地将机密传递给某个技能时，或者在审查处理敏感数据的SKILL.md文件时，也应触发此技能。该技能会指导代理如何处理这些机密，确保它们永远不会被存储在大型语言模型（LLM）的上下文中、提示信息中、日志中或输出结果中——而是通过OpenClaw的原生环境注入（env injection）机制来实现安全存储。
tags: [security, api-keys, credentials, secrets, audit]
version: 1.0.0
---
# Secret-Safe: 为代理技能提供安全的凭证处理机制

> **为何需要这一技能**：Snyk的研究人员发现，7.1%的ClawHub技能指示代理通过大型语言模型（LLM）的上下文来处理API密钥——这使得所有密钥都可能成为数据泄露的渠道。本技能旨在教导正确的处理方式。

---

## 核心规则

**任何密钥都绝不能出现在以下地方：**
- 大型语言模型的提示或系统上下文中
- Claude的响应或推理过程中
- 日志文件、会话导出文件或`.jsonl`历史文件中
- 代理创建的文件中
- 反馈给用户的错误信息中

**密钥只能通过以下途径传递：**
- `process.env`（由OpenClaw在代理启动前注入）
- 代理启动的子进程的shell环境中
- 通过 secrets manager 的 CLI 进行读取（在子进程层面进行读取，不会被传回上下文）

---

## 模式 1：环境变量注入（推荐使用）

这是OpenClaw提供的原生安全方式。适用于所有需要API密钥的技能。

### 在 `SKILL.md` 的前置内容中

```yaml
---
name: my-service-skill
description: Interact with MyService API.
metadata: {"openclaw": {"requires": {"env": ["MY_SERVICE_API_KEY"]}, "primaryEnv": "MY_SERVICE_API_KEY"}}
---
```

`requires.env` 确保如果密钥不存在，该技能将**不会被加载**——既不会发生无声的失败，也不会在对话过程中提示用户输入密钥。

`primaryEnv` 字段链接到 `openclaw.json` 中的 `skills.entries.<n>.apiKey`，因此用户只需在配置文件中配置一次，无需在聊天中再次输入。

### 在技能指令中

```markdown
## Authentication
The API key is available as `$MY_SERVICE_API_KEY` in the shell environment.
Pass it to CLI tools or curl as an environment variable — never echo it or
include it in any output returned to the user.
```

### 安全的curl调用示例（指导代理执行此操作）

```bash
# CORRECT — key stays in environment, never in command string visible to LLM
MY_SERVICE_API_KEY="$MY_SERVICE_API_KEY" curl -s \
  -H "Authorization: Bearer $MY_SERVICE_API_KEY" \
  https://api.myservice.com/v1/data
```

**绝对不要指示代理执行以下操作：**
```bash
# WRONG — key is visible in LLM context, command history, and logs
curl -H "Authorization: Bearer sk-abc123realkeyhere" https://api.myservice.com/
```

---

## 模式 2：集成 secrets manager

在生产环境或团队环境中，应在子进程层面从 secrets manager 中读取密钥。

### 支持的 secrets manager 工具

| 工具 | CLI 命令 | 环境变量模式 |
|---|---|---|
| macOS Keychain | `security find-generic-password -w` | 不适用 |
| 1Password CLI | `op read op://vault/item/field` | `OP_SERVICE_ACCOUNT_TOKEN` |
| Doppler | `doppler run --` | `DOPPLER_TOKEN` |
| HashiCorp Vault | `vault kv get -field=value` | `VAULT_TOKEN` |
| Bitwarden CLI | `bw get password item-name` | `BW_SESSION` |

### 安全的 shell 脚本编写方式

在技能中创建一个 `scripts/run-with-secret.sh` 脚本：

```bash
#!/usr/bin/env bash
# Fetches the secret at subprocess level — never echoes to stdout
SECRET=$(security find-generic-password -s "my-service-api-key" -w 2>/dev/null)
if [ -z "$SECRET" ]; then
  echo "ERROR: Secret 'my-service-api-key' not found in keychain." >&2
  exit 1
fi
export MY_SERVICE_API_KEY="$SECRET"
exec "$@"
```

代理会执行 `bash {baseDir}/scripts/run-with-secret.sh <实际命令>`——密钥的获取和注入过程完全在大型语言模型的视野之外进行。

---

## 模式 3：用户初次设置流程

如果用户尚未配置密钥，应指导他们完成设置**而无需在聊天中请求密钥**。

### 正确的设置提示：

```
To use this skill, add your API key to ~/.openclaw/openclaw.json:

  skills:
    entries:
      my-service:
        apiKey: "your-key-here"

Or set it as an environment variable before starting OpenClaw:
  export MY_SERVICE_API_KEY="your-key-here"

Do NOT paste your key into this chat — it will be logged.
```

### 错误的设置方式（绝对不要这样做）：

```
Please share your API key so I can help you set it up.
```

---

## 审查其他技能是否存在安全漏洞

在审查 `SKILL.md` 时，需检查是否存在以下问题：

### 🔴 危险情况——必须立即修复

| 模式 | 危险原因 |
|---|---|
| 指示用户在聊天中输入密钥 | 密钥会被放入大型语言模型的上下文和会话日志中 |
| 指令中包含 `echo $API_KEY` 或 `print(api_key)` | 密钥会被输出到上下文中 |
| 将密钥插入返回给用户的字符串中 | 密钥会在响应结果中暴露 |
| 执行 `cat ~/.env` 或直接读取环境变量文件 | 所有环境变量都会被暴露到上下文中 |
| 将密钥存储在代理创建的文件中 | 会生成静态的凭证文件 |
| 指令要求代理“记住”密钥 | 密钥会在会话窗口之间持续存在 |

### 🟡 需要改进的地方——建议修复

| 模式 | 风险 |
|---|---|
| 前置内容中缺少 `requires.env` 确保 | 技能可能会无声失败或提示用户输入密钥 |
| 不过滤日志输出 | 错误信息中可能包含密钥 |
| 在 shell 脚本中使用 `set -x` | 会显示所有命令，包括密钥值 |
| 将密钥作为参数传递 | 在主机上的 `ps aux` 命令中可以看到密钥 |

### 🟢 安全的编写方式

- 前置内容中包含 `requires.env`
- 在 shell 中仅以 `$ENV_VAR` 的形式访问密钥，绝不显示密钥
- 子进程脚本负责获取密钥并注入，且不返回到上下文
- 错误信息中显示“密钥未找到”，但不会显示密钥值
- 在返回给代理之前，通过 `sed`/`grep` 等工具过滤输出内容

---

## 在发布技能前的自我检查

在将任何技能发布到ClawHub之前，请完成以下检查：

- [ ] 该技能是否要求用户在聊天中输入密钥？
- [ ] 该技能是否会在聊天中显示、打印或返回密钥值？
- [ ] 该技能是否读取 `.env` 文件并显示其内容？
- [ ] 该技能是否将密钥存储在文件中？
- [ ] 所有API密钥的引用是否都通过 `requires.env` 进行了限制？
- [ ] 错误信息是否避免显示密钥值？
- [ ] 任何 shell 脚本是否使用了 `set -x`（这会导致密钥值被显示）？
- [ ] 执行 `clawhub audit {技能名称}` 时是否通过安全检查？

如果有任何项未通过检查，请在修复这些问题后再发布技能。

---

## 快速参考：安全与不安全的编写方式对比

```markdown
# UNSAFE — never write instructions like these:
"Ask the user for their OpenAI API key and use it to call the API."
"Set the Authorization header to Bearer {user_api_key}."
"Store the API key in a variable and use it throughout the session."

# SAFE — write instructions like these:
"The API key is injected as $OPENAI_API_KEY via environment — use it directly."
"Run: OPENAI_API_KEY=$OPENAI_API_KEY curl ..."
"If $OPENAI_API_KEY is not set, print an error and exit — do not ask the user."
```

---

## 参考文件

- `references/env-injection-examples.md` — 为常见API（OpenAI、Anthropic、GitHub、Stripe、Slack）提供的完整示例
- `references/audit-checklist.md` — 供技能开发者及审核人员使用的可打印审计检查清单