---
name: setup-agent
description: 设置或登录Karma。当用户请求“设置代理”、“配置API密钥”、“连接到Karma”、“登录Karma”或首次使用任何Karma功能时，请执行此操作。
version: 0.2.0
tags: [agent, setup, authentication, login]
metadata:
  author: Karma
  category: authentication
---
# 设置 Karma 代理

配置您的环境以使用 Karma 代理功能。在使用任何操作技能之前，请先运行此步骤。

有关基础 URL 和错误处理的详细信息，请参阅 [代理 API 参考文档](../references/agent-api.md)。

## 流程

检查 `KARMA_API_KEY` 是否已设置：

- **如果已设置** → 转到 [验证配置](#3-verify-configuration)
- **如果未设置** → 使用 `AskUserQuestion` 工具，并选择以下选项：
  - 问题：“您需要一个 Karma API 密钥才能继续。您希望如何设置它？”
  - 选项：["快速开始 — 立即生成（无需账户")", "通过电子邮件登录 — 链接到现有的 Karma 账户", "我已经有密钥"]

  - **快速开始** → 转到 [快速开始 — 无需账户](#quick-start--no-account-needed)
  - **通过电子邮件登录** → 转到 [通过电子邮件创建 API 密钥](#create-api-key-via-email)
  - **我已经有密钥** → 询问用户密钥，然后转至 [保存您的 API 密钥](#1-save-your-api-key)

## 快速开始 — 无需账户

这是最快捷的入门方式。无需电子邮件、登录或现有账户。

```bash
BASE_URL="${KARMA_API_URL:-https://gapapi.karmahq.xyz}"
INVOCATION_ID=$(uuidgen)

curl -s -X POST "${BASE_URL}/v2/agent/register" \
  -H "Content-Type: application/json" \
  -H "X-Source: skill:setup-agent" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: 0.2.0" \
  -d '{}'
```

**预期响应：**
```json
{ "key": "karma_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" }
```

密钥仅显示一次。立即继续执行 [设置您的 API 密钥](#1-set-your-api-key)。

> **注意**：使用此方法创建的项目将拥有自己的钱包。这些项目不会与现有的 Karma 账户关联，因此目前无法通过网站进行管理（将在未来的更新中添加此功能）。

## 通过电子邮件创建 API 密钥

### 第 1 步：询问用户电子邮件地址

询问用户的电子邮件地址。

### 第 2 步：发送验证代码

```bash
BASE_URL="${KARMA_API_URL:-https://gapapi.karmahq.xyz}"
INVOCATION_ID=$(uuidgen)

curl -s -X POST "${BASE_URL}/v2/api-keys/auth/init" \
  -H "Content-Type: application/json" \
  -H "X-Source: skill:setup-agent" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: 0.2.0" \
  -d '{ "email": "user@example.com" }'
```

**预期响应：**
```json
{ "message": "Verification code sent to user@example.com" }
```

告知用户：“请查看您的电子邮件以获取来自 Karma 的验证代码。”

### 第 3 步：验证代码

询问用户收到的验证代码，然后：

```bash
curl -s -X POST "${BASE_URL}/v2/api-keys/auth/verify" \
  -H "Content-Type: application/json" \
  -H "X-Source: skill:setup-agent" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: 0.2.0" \
  -d '{
    "email": "user@example.com",
    "code": "123456",
    "name": "claude-agent"
  }'
```

**预期响应：**
```json
{ "key": "karma_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" }
```

**重要提示：** 密钥仅显示一次。立即继续设置密钥。

### 第 4 步：处理错误

| 错误 | 含义 | 处理方式 |
|-------|---------|--------|
| `400 无效或过期的代码` | 代码错误或已过期 | 请用户检查代码或请求新的代码 |
| `409 已存在有效的密钥` | 用户已有密钥 | 告知用户使用现有的密钥或从网站撤销该密钥 |
| `429 请求次数过多` | 被限制了请求次数 | 等待片刻后重试 |

## 1. 保存您的 API 密钥

获取密钥后，**请求用户允许** 将其永久保存：

> 您希望我将您的 API 密钥保存到您的 shell 配置文件中，这样您就无需每次都手动输入它了吗？

如果用户同意，检测用户的 shell 并添加以下代码：

```bash
# Detect shell config file
if [ -f "$HOME/.zshrc" ]; then
  SHELL_RC="$HOME/.zshrc"
elif [ -f "$HOME/.bashrc" ]; then
  SHELL_RC="$HOME/.bashrc"
fi

# Append only if not already present
grep -q 'KARMA_API_KEY' "$SHELL_RC" || echo '\n# Karma API Key\nexport KARMA_API_KEY="karma_..."' >> "$SHELL_RC"

# Also export for current session
export KARMA_API_KEY="karma_..."
```

如果文件中已经存在该密钥，请替换旧值，而不是添加重复项。

如果用户拒绝保存，只需为当前会话设置密钥即可：

```bash
export KARMA_API_KEY="karma_your_key_here"
```

## 2. 设置 API URL（可选）

默认设置为生产环境地址。对于本地开发环境：

```bash
export KARMA_API_URL="http://localhost:3002"
```

## 3. 验证配置

```bash
curl -s "${KARMA_API_URL:-https://gapapi.karmahq.xyz}/v2/agent/info" \
  -H "x-api-key: ${KARMA_API_KEY}" \
  -H "X-Source: skill:setup-agent" -H "X-Invocation-Id: $INVOCATION_ID" -H "X-Skill-Version: 0.2.0" \
  | python3 -m json.tool
```

**预期响应：**
```json
{
  "walletAddress": "0x...",
  "smartAccountAddress": "0x...",
  "supportedChainIds": [10, 137, 1135, ...],
  "supportedActions": ["createProject", "createMilestone", ...]
}
```

## 4. 确认成功

如果响应中包含 `walletAddress` 和 `supportedActions`，则告知用户他们的 API 密钥已设置完成：

> 您的 Karma 代理已设置完成！
>
> **API 密钥**：`karma_...`（步骤 1 或通过电子邮件获取的密钥）
>
> 现在您可以使用以下技能：
> - `project-manager` — 创建和管理项目、拨款、里程碑和更新
> - `find-funding-opportunities` — 搜索拨款机会、黑客马拉松、悬赏任务等

请不要向用户显示钱包地址、智能账户地址或链 ID。他们只需要 API 密钥即可。

## 故障排除

| 问题 | 解决方法 |
|-------|-----|
| `401 无效或被撤销的 API 密钥` | 密钥错误或已过期 — 通过电子邮件流程或 karmahq.xyz 重新生成密钥 |
| `walletAddress: null` | 密钥是在服务器钱包创建之前的 — 重新生成密钥 |
| `连接被拒绝` | `KARMA_API_URL` 错误 — 检查 URL 是否可访问 |
| `KARMA_API_KEY 未设置` | 在终端中运行 `export KARMA_API_KEY="karma_..."` 命令 |