---
name: pref0
description: 从用户的对话中了解他们的偏好，并自动个性化响应内容。用户的偏好会随着时间的推移而发生变化——例如，用户要求使用 TypeScript 而不是 JavaScript 的需求会被记录下来，并应用到未来的会话中。
version: 1.0.0
user-invocable: true
metadata: {"openclaw":{"requires":{"env":["PREF0_API_KEY"]},"primaryEnv":"PREF0_API_KEY"}}
---

# pref0 — 用于AI代理的偏好学习功能

您可以使用pref0 API。该API能够从用户对话中学习用户的偏好，并在推理时将这些偏好信息提供给系统。您跟踪的对话越多，其学习效果就越好。

## 何时使用此功能

### 对话结束后 → 追踪对话内容

在对话结束后（或遇到自然的分界点时），将对话内容发送给pref0，以便它能够提取用户的偏好信息。当用户对您的回答进行纠正（例如：“使用pnpm，而不是npm”）或明确表达偏好（例如：“始终使用公制单位”）时，这一点尤其重要。

### 在回复用户之前 → 获取用户的偏好信息

在生成回复之前，先获取用户已学习的偏好信息，并据此进行回复。这样可以避免用户在多次会话中重复表达相同的内容。

## API参考

**基础URL：** `https://api.pref0.com`  
**认证方式：** `Authorization: Bearer $PREF0_API_KEY`

### 追踪对话内容（POST /v1/track）

发送对话内容，以便pref0从中学习用户的偏好。该API会自动提取用户的纠正信息、明确表达的偏好以及行为模式。

**响应示例：**
```bash
curl -X POST https://api.pref0.com/v1/track \
  -H "Authorization: Bearer $PREF0_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "userId": "<user-id>",
    "messages": [
      { "role": "user", "content": "Help me set up a new project" },
      { "role": "assistant", "content": "Here is a project using npm and JavaScript..." },
      { "role": "user", "content": "Use pnpm, not npm. And TypeScript." },
      { "role": "assistant", "content": "Updated to pnpm and TypeScript..." }
    ]
  }'
```

响应会告诉您处理了多少条消息（`messagesAnalyzed`），以及哪些偏好信息发生了变化：`created`（新学习到的偏好）、`reinforced`（现有偏好再次出现，置信度提高）、`decreased`（用户撤回了偏好，置信度降低）、`removed`（偏好被完全撤回并删除）。

### 获取用户的学习偏好信息（GET /v1/profiles/:userId）

检索用户的偏好信息。可以使用`?minConfidence=0.5`来仅获取那些置信度较高的偏好信息，以便直接用于系统提示中。

**响应示例：**
```bash
curl https://api.pref0.com/v1/profiles/<user-id>?minConfidence=0.5 \
  -H "Authorization: Bearer $PREF0_API_KEY"
```

每个偏好信息都包含`evidence`（触发偏好提取的原始语句）、`firstSeen`（首次学习的时间）和`lastSeen`（最后一次确认的时间）。`prompt`字段是一个可以直接添加到系统提示中的字符串。

### 删除用户偏好信息（DELETE /v1/profiles/:userId）

重置用户的偏好设置。适用于需要重置偏好或删除数据的情况。

**响应示例：**
```bash
curl -X DELETE https://api.pref0.com/v1/profiles/<user-id> \
  -H "Authorization: Bearer $PREF0_API_KEY"
```

响应代码返回`204 No Content`。

## 如何将此功能集成到您的工作流程中

1. **识别用户**：使用一个稳定的用户标识符（如电子邮件、账户ID或电话号码）。
2. **在会话开始时**，获取用户的偏好信息：
   - 调用`GET /v1/profiles/{userId}?minConfidence=0.5`
   - 直接使用`prompt`字段将偏好信息添加到系统提示中，或使用结构化的`preferences`数组进行更精细的控制。
3. **在会话结束时**，跟踪对话内容：
   - 调用`POST /v1/track`并传入完整的对话记录
   - pref0会自动处理偏好信息的提取和置信度评估。
4. **偏好信息会随时间累积**：用户的纠正行为会提升置信度（从0.70开始），隐含的偏好会从0.40开始累积；每次重复表达相同偏好会增加0.15的置信度，最高上限为1.0。

## 置信度判断标准

| 信号类型                | 初始置信度            | 例子                          |
|-------------------|-------------------|-----------------------------------|
| 明确的纠正            | 0.70               | “使用Tailwind框架，而不是Bootstrap”             |
| 隐含的偏好            | 0.40               | “将代码部署到Vercel服务器”                 |
| 行为模式              | 0.30               | 用户始终希望收到简短的回复                |
| 每次重复表达          | +0.15              | 在不同会话中保持相同的偏好设置               |

## 设置步骤

1. 在[pref0.com](https://pref0.com/signup)注册账号。
2. 在控制面板中创建API密钥。
3. 设置`PREF0_API_KEY`环境变量。
4. 每月前100次请求免费，之后每1000次请求收取5美元费用。