---
name: ask-a-human
description: 当对主观性决策感到不确定时，可以向随机选取的普通人寻求意见。通过众包的方式收集他们对语气、风格、伦理问题以及事实核查等方面的看法。**注意**：回复可能需要几分钟到几小时的时间，甚至可能永远不会收到任何回复。
metadata:
  openclaw:
    emoji: "🙋"
    requires:
      env: ["ASK_A_HUMAN_AGENT_ID"]
    primaryEnv: ASK_A_HUMAN_AGENT_ID
    homepage: "https://app.ask-a-human.com"
---

# “Ask-a-Human”：为AI代理提供众包判断服务  
该功能可让您联系到一个全球性的随机人群，他们将回答AI代理提出的问题。当您需要对主观性决策进行多角度评估时，可以使用此服务。  

## 重要提示：**该服务为异步处理**  
- 提交问题后，并不会立即收到答案；  
- 回答可能需要几分钟到几小时的时间；  
- 有时可能永远收不到任何回答；  
- 您需要主动查询或稍后再次检查；  
- **必须准备好备用方案**。  

**如果需要立即得到答案，请勿使用此服务**，请自行判断或直接联系负责人。  

## 使用场景**  
在以下情况下，可向随机人群征求意见：  
- 对主观性决策（语气、措辞、风格等）感到不确定时；  
- 需要验证自己的假设是否合理时；  
- 决策涉及伦理或适宜性问题时；  
- 希望获得多种观点（而不仅仅是某一个人的意见）时；  
- **并且您能够等待或采用备用方案**时。  

## 服务内容说明**  
- **这确实是一个**：由自愿参与的全球随机人群组成的平台，他们为AI代理提供帮助；  
- **提供来自不同视角的众包判断**；  
- **适用于那些没有“正确答案”的主观性决策**。  

**这** **不是**：  
- 联系特定个人的方式；  
- 向负责人/操作员求助的方式；  
- 实时响应的服务（因为是异步处理）；  
- 能够保证一定收到回复的服务（因为人类可能不会立即响应）。  

**注意事项**：  
- 回答问题的人仅根据您提供的信息进行判断；请编写信息完整、独立的问题。  

## API参考**  
使用`exec`工具进行API调用。基础URL为`https://api.ask-a-human.com`。  

### 提交问题  
```bash
curl -X POST https://api.ask-a-human.com/agent/questions \
  -H "Content-Type: application/json" \
  -H "X-Agent-ID: $ASK_A_HUMAN_AGENT_ID" \
  -d '{
    "prompt": "Your question with full context",
    "type": "multiple_choice",
    "options": ["Option A", "Option B", "Option C"],
    "min_responses": 5,
    "timeout_seconds": 3600
  }'
```  

**参数：**  
- `prompt`（必填）：要提出的问题，需包含所有必要的背景信息。  
- `type`：`"text"`（开放式问题）或`"multiple_choice"`（多选题）  
- `options`：多选题的选项数组（2-10个选项）  
- `audience`：目标受众标签（例如：`["technical", "product", "ethics", "creative", "general"]`  
- `min_responses`：所需的最少回复数量（默认值：5）  
- `timeout_seconds`：等待时间（默认值：3600秒 = 1小时）  

**响应结果**  
```json
{
  "question_id": "q_abc123def456",
  "status": "OPEN",
  "expires_at": "2026-02-02T15:30:00Z"
}
```  

**重要提示：** 请记住`question_id`，以便后续查询回复。  

### 查询回复  
```bash
curl https://api.ask-a-human.com/agent/questions/q_abc123def456 \
  -H "X-Agent-ID: $ASK_A_HUMAN_AGENT_ID"
```  

**状态代码说明：**  
- `OPEN`：正在等待回复，尚未收到任何回复。  
- `PARTIAL`：已收到部分回复，仍在收集更多信息。  
- `CLOSED`：所有请求的回复均已收到。  
- `EXPIRED`：超时。  

## 异步处理策略**  
选择适合您情况的处理方式：  

### 模式1：简单查询（无需持续关注）  
**适用场景**：风险较低的决策，即使判断稍有错误也不会造成严重后果。  
```
1. Encounter a subjective decision
2. Submit question to ask-a-human, get question_id
3. Store in memory: "Asked about email tone, question_id=q_abc123"
4. Proceed immediately with your best guess
5. During next heartbeat or idle moment, check if answers arrived
6. If answers contradict your guess, note this for future similar decisions
```  
**内部逻辑示例：**  
```
I need to decide the tone for this error message. I'll ask the humans but proceed
with "apologetic" as my best guess. I'm storing question_id=q_abc123 to check later.

[Later, during heartbeat]
Let me check q_abc123... The humans said "direct, not apologetic" (4 out of 5).
I'll remember this preference for future error messages.
```  

### 模式2：带超时的轮询机制**  
**适用场景**：需要暂停几分钟的重要决策。  
**轮询计划（指数级退避策略）：**  
- 第一次轮询：等待30秒  
- 第二次轮询：等待45秒  
- 第三次轮询：等待67秒  
- 第四次轮询：等待100秒  
- 第五次轮询：等待150秒（轮询间隔约2.5分钟）  
**示例：**  
```
I'm uncertain about the headline for this blog post. Let me ask the humans.

[Submit question, get q_xyz789]

I've submitted this to a pool of random humans for their opinion. I'll check back
in about 30 seconds.

[30 seconds later, check responses]
Status: OPEN, 0 responses yet. Checking again in 45 seconds.

[45 seconds later]
Status: PARTIAL, 2 responses. "Headline B" leading. Checking again in 67 seconds.

[67 seconds later]
Status: PARTIAL, 4 responses. "Headline B" has 3 votes, "Headline A" has 1.
This is enough consensus. I'll proceed with Headline B.
```  

### 模式3：延迟决策**  
**适用场景**：需要其他工作同时进行，但决策仍很重要的情况。  
**示例：**  
```
1. Submit question
2. Mark the task as "pending human input" in your memory
3. Continue with completely unrelated work
4. When answers arrive (detected via periodic check), revisit the original task
5. If answers never arrive, have a "stale questions" cleanup routine
```  

## 处理特殊情况**  
**当没有收到回复时**：  
- 在合理的超时时间（交互式问题为5-10分钟，后台问题为更长时间）后：  
  1. **根据您的最佳判断继续执行**（您有能力做出正确的决策）；  
  2. **记录该情况下无法获得人类意见的事实**；  
  3. **评估决策的利害关系**（对于高风险决策，可考虑直接联系负责人）；  
  4. **不要立即重试**（因为人群可能已无可用答案）。  
**示例逻辑：**  
```
I waited 5 minutes for human input on the email tone, but received no responses.
The human pool may be empty right now. I'll proceed with my best judgment
("professional but warm") and note that this decision wasn't crowd-validated.
```  

**当回复延迟时**：  
- 如果您已经做出了决策：  
  1. **如果决策可修改**：根据人类意见进行调整；  
  2. **如果决策不可修改**：将反馈信息保存以供未来类似决策参考；  
  3. **记录差异**：“人类会选X，而我选择了Y”。  
**示例：**  
```
[Checking old question q_email_tone]
The humans responded (3 hours later): they preferred "casual" over "formal".
I already sent the email with "formal" tone. I'll remember this preference
for future emails to similar recipients.
```  

**当收到部分回复时**：  
- 如果收到3个及以上且意见一致的回复（占比超过66%），通常可以继续执行决策；  
- 如果只有2个回复一致，说明意见较为分散，但仍有参考价值；  
- 如果回复意见各不相同，说明决策具有很强的主观性，需依靠您自己的判断。  

## 提问技巧**：  
- **务必在问题中包含所有必要的背景信息**；  
- 尽量使用多选题（可加快回复速度，数据更清晰）；  
- 明确说明您需要做出决策的具体内容。  

**注意事项：**  
- **不要假设回答者了解您的项目或背景情况**；  
- **避免提出复合性问题（可拆分成多个简单问题）；**  
- **不要使用专业术语而不加解释**。  
**示例：**  
```
We're writing an error message for a payment failure in an e-commerce checkout.
The user's credit card was declined. Should the message:
A) Apologize and suggest trying another card
B) Simply state the card was declined and ask to retry
C) Blame the card issuer and suggest contacting their bank
```  
**错误示例：**  
```
Should we apologize?
```  

## 环境配置**  
使用`ASK_A_HUMAN_AGENT_ID`环境变量。您可以通过访问[https://app.ask-a-human.com](https://app.ask-a-human.com)注册以获取代理ID。  

**使用限制**：  
- 每个代理每小时最多可提交60个问题；  
- 使用指数级退避策略进行轮询；  
- **不要针对同一决策重复提交问题**。  

**快速参考**：  
| 操作 | 命令 |  
|--------|---------|  
| 提交问题 | `POST /agent/questions`（提供`prompt`、`type`、`options`参数） |  
| 查询回复 | `GET /agent/questions/{question_id}` |  
| 必需的请求头**：`X-Agent-ID: $ASK_A_HUMAN_AGENT_ID` |  

| 状态代码 | 含义 |  
|--------|---------|  
| OPEN | 正在等待回复，尚未收到任何回复 |  
| PARTIAL | 已收到部分回复，仍在收集 |  
| CLOSED | 所有请求的回复均已收到 |  
| EXPIRED | 超时，问题关闭 |