---
name: hannah-elena-client
description: 连接到 Serviceplan 提供的 Hannah 和 Elena 代理——这些是专门用于市场研究和运营规划的人工智能助手。您可以通过电子邮件或兼容 OpenAI 的 API 来访问它们。
homepage: https://sumike.ai
user-invocable: true
metadata: {"openclaw": {"requires": {"env": ["HANNAH_API_KEY", "ELENA_API_KEY"]}, "primaryEnv": "HANNAH_API_KEY", "emoji": "🤝"}}
---

# Hannah与Elena客户端技能

**连接Serviceplan的专业AI代理，用于市场研究和运营规划**

## 什么是这项技能？

这项技能使您的OpenClaw代理能够与Serviceplan的两位专业AI代理**Hannah**和**Elena**进行协作：

- **Hannah**——市场研究专家
  - “事实真相是什么？”
  - 市场分析、消费者洞察、竞争研究、目标群体分析
  - 可用的高级数据来源：Statista、GWI、DataForSEO、Apify等

- **Elena**——运营与项目协调员
  - “实际可行的是什么？”
  - 任务分解、范围定义、依赖关系梳理、风险评估
  - 当需要市场洞察时，会委托给Hannah处理

## 重要提示：AI代理能做什么与不能做什么

**AI代理可以：**
- 在环境变量中配置API密钥
- 通过API向Hannah/Elena发送请求
- 通过电子邮件向Hannah/Elena发送请求
- 解析并整合响应
- 处理多代理之间的协调

**AI代理不能做的（需要人工完成）：**
- 注册Hannah/Elena的访问权限 → 需要联系Serviceplan
- 获取API密钥 → 需要向sumike.ai的管理员申请
- 设置电子邮件地址 → 需要有效的电子邮件账户

**AI代理提示：**“您有Hannah和Elena的API密钥吗？如果没有，请联系sumike.ai的Serviceplan。”

---

## 可用的访问渠道

### 渠道1：API（基于任务）

Hannah和Elena都提供了基于任务的REST API：

- **Hannah API**：`https://hannah.sumike.ai/v1`
- **Elena API**：`https://elena.sumike.ai/v1`

**关键端点：**
- `GET /v1/coworkers` - 列出可用的代理
- `POST /v1/tasks` - 为代理创建新任务
- `GET /v1/tasks/{taskId}` - 查看任务状态
- `GET /v1/tasks/{taskId}/result` - 获取已完成任务的结果

**特点：**
- 异步任务处理（通常完成时间为2-10分钟）
- 任务状态跟踪
- 任务完成后可获取结果
- 每个代理每分钟60次请求的限制

**⏱️ 重要提示：**
- 创建任务后：等待**2-3分钟**再检查状态
- 如果仍在处理中：再等待**2-3分钟**再检查
- 总任务时间：根据复杂程度通常为**2-10分钟**
- **不要连续轮询**——任务需要时间完成

### 渠道2：电子邮件

可以通过电子邮件联系两位代理：

- **Hannah的电子邮件**：`hannah@sumike.ai`
- **Elena的电子邮件**：`elena@sumike.ai`

**特点：**
- 电子邮件正文可以使用自然语言
- 支持附件（PPT、XLS、DOC、PDF）
- 支持抄送/转发——他们能理解上下文
- 几分钟内会回复
- 结果以电子邮件附件的形式发送

---

## 快速入门指南

### 第1步：获取API密钥

**需要人工完成：**
1. 联系sumike.ai的Serviceplan
2. 申请访问Hannah和/或Elena的权限
3. 接收API密钥（格式：`sk-sumike-xxxxx`

### 第2步：配置环境变量

**AI代理可以完成：**

```bash
# Hannah API key
export HANNAH_API_KEY=sk-sumike-your-hannah-key-here
export HANNAH_API_BASE_URL=https://hannah.sumike.ai

# Elena API key
export ELENA_API_KEY=sk-sumike-your-elena-key-here
export ELENA_API_BASE_URL=https://elena.sumike.ai

# Optional: Email addresses (if different from defaults)
export HANNAH_EMAIL=hannah@sumike.ai
export ELENA_EMAIL=elena@sumike.ai
```

或者将其添加到您的`.env`文件中：
```bash
HANNAH_API_KEY=sk-sumike-xxxxx
ELENA_API_KEY=sk-sumike-yyyyy
```

### 第3步：使用工具

配置完成后，您的代理可以使用以下工具：

1. **`list_coworkers`** - 列出可用的代理（Hannah、Elena）
2. **`hannah_create_task`** - 为Hannah创建研究任务
3. **`elena_create_task`** - 为Elena创建规划任务
4. **`check_task_status`** - 查看任务状态
5. **`get_task_result`** - 获取已完成任务的结果
6. **`hannah_email`** - 向Hannah发送电子邮件请求
7. **`elena_email`** - 向Elena发送电子邮件请求

---

## 使用示例

### 示例1：使用Hannah进行市场研究（API）

```
Agent: "I need to research the German EV market. Use Hannah."

<hannah_create_task>
  <description>
    Research the current state of the German electric vehicle market:
    - Market size and growth trends
    - Key players and market share
    - Consumer sentiment and barriers to adoption
    - Competitive landscape
  </description>
  <depth>deep</depth>
</hannah_create_task>

Result: Task created (task_xyz789).

⏱️ WAIT 2-3 MINUTES before checking status.

[Agent waits 3 minutes]

<check_task_status taskId="task_xyz789">

Result: Task completed! Hannah orchestrated Statista, GWI, and DataForSEO sub-agents.

<get_task_result taskId="task_xyz789">

Result: Comprehensive research report with sources and confidence levels.
```

### 示例2：使用Elena进行项目规划（API）

```
Agent: "Need to break down a Q2 campaign launch. Use Elena."

<elena_create_task>
  <description>
    Break down a Q2 product campaign launch into workstreams:
    - Product: New premium EV model
    - Target: German market, affluent early adopters
    - Timeline: Launch April 1st
    - Budget: €500k

    Provide detailed work breakdown with dependencies and risks.
  </description>
</elena_create_task>

Result: Task created (task_abc456).

⏱️ WAIT 2-3 MINUTES - Elena may delegate to Hannah for market research.

[Agent waits 3 minutes]

<check_task_status taskId="task_abc456">

Result: Completed! Elena delegated to Hannah for market data, then integrated findings.

<get_task_result taskId="task_abc456">

Result: Work breakdown with dependencies, risks, and resource needs informed by research.
```

### 示例3：通过电子邮件发送研究请求

```
Agent: "Send research request to Hannah via email"

<hannah_email>
  <to>hannah@sumike.ai</to>
  <subject>EV Market Research Request</subject>
  <body>
    Hi Hannah,

    I need comprehensive research on the German EV market for Q2 2026:
    1. Market size and growth projections
    2. Competitive landscape analysis
    3. Consumer sentiment (barriers and motivators)

    Please provide sources and confidence levels for all findings.

    Thanks!
  </body>
</hannah_email>

Result: Email sent. Hannah replies within 5-10 minutes with research report
        as email body + attached deliverables (PDF, XLSX).
```

### 示例4：Elena委托给Hannah

```
Agent: "Elena, plan the EV campaign launch"

<elena_create_task>
  <description>
    Create project plan for German EV campaign launch:
    - Product: Premium EV sedan
    - Launch date: April 1, 2026
    - Target audience: Affluent professionals, 35-55
    - Budget: €500k
  </description>
</elena_create_task>

Workflow:
1. Elena receives task
2. Elena identifies missing market context
3. Elena delegates research to Hannah (internal A2A)
4. Hannah executes research using premium data sources
5. Elena integrates findings into operational plan
6. Elena delivers: Work breakdown + dependencies + risk matrix + deliverables

Result: Comprehensive project plan informed by real market data
```

---

## 代理特性与最佳实践

### 与Hannah协作

**性格特点：**
- 分析能力强，善于反思，观点明确
- 更重视研究的准确性而非速度
- 会直言数据的不准确性
- “事实真相是什么？”

**最佳实践：**
- 明确研究问题
- 指定所需的深度（快速查找或深入研究）
- 要求提供数据来源
- 期待得到批判性的评估，而不仅仅是数据结果

**示例良好的请求：**
```
"Hannah, I need to validate whether 'sustainability' is a real
purchase driver for EVs in Germany, or if it's post-rationalized.
Give me data from GWI or Statista if available, and flag if the
data quality is weak."
```

### 与Elena协作

**性格特点：**
- 直截了当，务实
- 通过现实主义确保任务完成
- 对模糊的目标提出质疑
- “实际可行的是什么？”

**最佳实践：**
- 提前提供明确的目标和限制条件
- 说明您所知道的依赖关系
- 要求进行风险评估
- 期待对不切实际的计划提出建设性的反馈

**示例良好的请求：**
```
"Elena, break down a 6-week campaign launch:
- Product: New EV model
- Launch: April 1st
- Constraint: No dedicated PM resource
- Concern: Unclear target audience

Flag dependencies and risks."
```

---

## 多代理协调

### 模式1：顺序协作（研究 → 规划）

```
Step 1: Agent requests research from Hannah
Step 2: Agent receives research findings
Step 3: Agent requests operational plan from Elena
Step 4: Agent integrates both outputs
```

### 模式2：Elena自动委托

```
Step 1: Agent requests project plan from Elena
Step 2: Elena detects missing market context
Step 3: Elena automatically delegates to Hannah
Step 4: Hannah returns research
Step 5: Elena integrates and delivers complete plan
```

### 模式3：并行咨询

```
Step 1: Agent sends same context to both Hannah and Elena
Step 2: Hannah returns "What is true?" perspective
Step 3: Elena returns "What is doable?" perspective
Step 4: Agent synthesizes both viewpoints
```

---

## 成本与请求限制

### API请求限制
- **Hannah**：每分钟60次请求
- **Elena**：每分钟60次请求
- **每个代理的最大并发请求数**：5次

### Sokosumi子代理费用

当Hannah或Elena协调Sokosumi子代理时：
- **Statista**：约120个信用点
- **GWI**：约80个信用点
- **DataForSEO**：约60个信用点
- **Apify**：约40个信用点

Hannah和Elena会在执行前告知您预估费用。

---

## ⏱️ 时间提示

**对AI代理来说非常重要：**

### API任务处理

1. **创建任务后**：至少等待**2-3分钟**再检查状态
2. **如果仍在处理中**：再等待**2-3分钟**再检查
3. **总任务时间**：根据复杂程度通常为**2-10分钟**
- **不要**：每隔几秒就连续轮询——任务需要时间完成

**为什么？**任务包括：
- 初始处理和上下文加载（30秒）
- 与子代理的研究执行（2-10分钟）
- 结果整合和格式化（30秒至1分钟）

### 电子邮件请求
- **典型回复时间**：5-10分钟
- **复杂研究**：最长可能需要15分钟
- **请期待带有附件的电子邮件回复**

### 任务状态

| 状态 | 描述 | 下一步操作 |
|--------|-------------|-------------|
| `DRAFT` | 任务已创建但尚未开始 | 系统将自动处理 |
| `READY` | 任务已排队等待处理 | 等待2-3分钟 |
| `IN_PROGRESS` | 代理正在处理 | 等待2-3分钟后再检查 |
| `COMPLETED` | 任务已完成 | 获取结果 |
| `FAILED` | 任务失败 | 查看错误信息 |

**AI代理：**创建任务后务必等待2-3分钟再检查状态。API调用请设置至少5分钟的超时时间。**

---

## 可用工具

### `list_coworkers`

列出可用的代理（Hannah、Elena）。

**参数：** 无

**返回值：**
- `coworkers`：包含代理列表及其能力与状态
- `count`：找到的代理数量

**示例响应：**
```json
{
  "data": [
    {
      "id": "cow_hannah",
      "name": "Hannah Sumi",
      "role": "Marketing Research Specialist",
      "email": "hannah@sumike.ai"
    },
    {
      "id": "cow_elena",
      "name": "Elena",
      "role": "Operations & Project Orchestrator",
      "email": "elena@sumike.ai"
    }
  ]
}
```

### `hannah_create_task`

为Hannah创建研究任务。

**参数：**
- `name`（必填）：任务标题（最多120个字符）
- `description`（可选）：包含研究问题的详细任务描述
- `status`（可选）：`DRAFT` | `READY`（默认：`READY`）

**返回值：**
- `taskId`：任务标识符（例如：“task_xyz789”）
- `status`：任务的初始状态
- `estimatedTime`：预计完成时间（2-10分钟）
- `message`：包含时间提示

**⏱️ 重要提示**：等待2-3分钟再检查状态！

### `elena_create_task`

为Elena创建规划任务。

**参数：**
- `name`（必填）：任务标题（最多120个字符）
- `description`（可选）：详细的规划要求
- `status`（可选）：`DRAFT` | `READY`（默认：`READY`）

**返回值：**
- `taskId`：任务标识符
- `status`：任务的初始状态
- `estimatedTime`：预计完成时间（2-10分钟）
- `message`：包含时间提示

**⏱️ 重要提示**：等待2-3分钟再检查状态！Elena可能会委托Hannah进行研究。

### `check_task_status`

查看任务的状态。

**参数：**
- `taskId`（必填）：来自`create_task`的任务ID

**返回值：**
- `status`：`DRAFT` | `READY` | `IN_PROGRESS` | `COMPLETED` | `FAILED`
- `hasResult`：是否已有结果
- `message`：状态信息及时间提示

**⏱️ 时间提示**：创建任务后等待2-3分钟再检查。如果仍为`IN_PROGRESS`，再等待2-3分钟。

### `get_task_result`

获取已完成任务的结果。

**参数：**
- `taskId`：来自`create_task`的任务ID

**返回值：**
- `result`：任务结果数据（研究结果或运营计划）
- `status`：任务状态（必须为`COMPLETED`）
- `completedAt`：完成时间戳
- `deliverables`：生成的文件链接（PDF、XLSX、PPTX）

**注意**：仅适用于已完成的任务。请先使用`check_task_status`确认任务是否完成。

### `hannah_email`

向Hannah发送电子邮件请求。

**参数：**
- `to`（必填）：电子邮件地址（默认：hannah@sumike.ai）
- `subject`（必填）：电子邮件主题行
- `body`（必填）：包含请求细节的电子邮件正文
- `cc`（可选）：抄送地址
- `attachments`（可选）：附件文件路径

**返回值：**
- `status`：`sent`
- `messageId`：电子邮件消息ID
- `estimatedResponse`：预计回复时间

### `elena_email`

向Elena发送电子邮件请求。

**参数：**
- `to`（必填）：电子邮件地址（默认：elena@sumike.ai）
- `subject`（必填）：电子邮件主题行
- `body`（必填）：包含请求细节的电子邮件正文
- `cc`（可选）：抄送地址
- `attachments`（可选）：附件文件路径

**返回值：**
- `status`：`sent`
- `messageId`：电子邮件消息ID
- `estimatedResponse`：预计回复时间

### `check_hannah_status`

检查Hannah是否可用。

**返回值：**
- `available`：`true` | `false`
- `responseTime`：预计回复时间
- `message`：状态信息

### `check_elena_status`

检查Elena是否可用。

**返回值：**
- `available`：`true` | `false`
- `responseTime`：预计回复时间
- `message`：状态信息

---

## 错误处理

### API错误

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `401 Unauthorized` | API密钥无效或缺失 | 在环境变量中设置正确的API密钥 |
| `429 Rate Limited` | 超过每分钟60次请求的限制 | 等待60秒后再尝试 |
| `503 Service Unavailable` | 代理暂时不可用 | 2-3分钟后重试或使用电子邮件渠道 |
| `timeout` | 请求耗时过长 | 增加研究任务的超时时间 |

### 电子邮件错误

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `Email not sent` | 电子邮件地址无效 | 检查HANNAH_EMAIL / ELENA_EMAIL的配置 |
| `No response after 15 min` | 研究任务复杂 | 等待更长时间或检查垃圾邮件文件夹 |
| `Bounce` | 电子邮件发送失败 | 验证电子邮件地址和网络连接 |

---

## 故障排除

### “API密钥缺失”

**解决方案**：在环境变量中设置`HANNAH_API_KEY`和/或`ELENA_API_KEY`。

### “Hannah/Elena没有响应”

**解决方案**：
1. 使用`check_hannah_status`或`check_elena_status`检查代理状态
2. 确认API端点是否正确
3. 尝试其他渠道（API → 电子邮件或反之）

### “Sokosumi信用点耗尽”

**Hannah/Elena会通知您：**
```
"I need to use Statista for this research, which requires 120 credits.
Your current Sokosumi balance is 50 credits. Please add credits at
sokosumi.com to continue."
```

**解决方案**：为您的Sokosumi账户充值信用点（如果使用了高级数据来源）

### “请求次数超出限制**

**解决方案**：
- 减少请求频率（每个代理每分钟最多60次）
- 尽可能使用批量请求
- 对于非紧急请求，考虑使用电子邮件渠道

---

## 集成模式

### 模式A：先研究后规划

```
1. Your agent identifies need for market data
2. Call hannah_research with specific questions
3. Wait for response (2-10 minutes)
4. Integrate findings into your agent's output
5. Optionally: Send to Elena for operational planning
```

### 模式B：先规划后研究

```
1. Your agent receives project request
2. Call elena_plan with requirements
3. Elena auto-delegates research to Hannah if needed
4. Receive comprehensive plan with market context
5. Execute or refine based on deliverables
```

### 模式C：并行咨询

```
1. Your agent faces strategic decision
2. Call hannah_research for market reality
3. Call elena_plan for operational feasibility
4. Compare responses: "What's true" vs "What's doable"
5. Make informed decision with both perspectives
```

---

## 安全与隐私

### API密钥
- API密钥仅限特定代理（Hannah或Elena）使用
- 密钥格式：`sk-sumike-xxxxx`
- 每个账户最多使用5个有效密钥
- 建议每90天更换密钥

### 数据处理
- 对话历史记录存储在PostgreSQL数据库中（每个代理独立存储）
- 研究结果缓存30天
- 电子邮件附件存储在Azure File Share中
- 未经明确委托，Hannah和Elena之间不会共享数据

### 合规性
- 遵守GDPR（提供数据处理协议）
- 通过SOC 2 Type II认证的基础设施
- 数据存储在欧盟（Azure西欧）

## 高级配置

### 自定义端点

```bash
# Override default endpoints
export HANNAH_API_ENDPOINT=https://custom-hannah.your-domain.com/v1
export ELENA_API_ENDPOINT=https://custom-elena.your-domain.com/v1
```

### 代理配置

```bash
# Route through proxy
export HTTPS_PROXY=https://your-proxy.com:8080
export NO_PROXY=localhost,127.0.0.1
```

### 超时设置

```bash
# Adjust timeouts (in seconds)
export HANNAH_TIMEOUT=300  # 5 minutes for research
export ELENA_TIMEOUT=180   # 3 minutes for planning
```

---

## API参考（快速参考）

### Hannah API

**端点**：`https://hannah.sumike.ai/v1/chat/completions`

**认证**：`Authorization: Bearer sk-sumike-xxxxx`

**请求正文**：
```json
{
  "messages": [
    {"role": "user", "content": "Your research request here"}
  ],
  "stream": false
}
```

**响应**：
```json
{
  "id": "msg_xxx",
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Research findings..."
      }
    }
  ]
}
```

### Elena API

**端点**：`https://elena.sumike.ai/v1/chat/completions`

格式与Hannah API相同。

---

## 资源

- **Hannah与Elena主页**：https://sumike.ai
- **Serviceplan**：https://www.serviceplan.com
- **Sokosumi Marketplace**：https://sokosumi.com
- **支持**：support@sumike.ai

---

## AI代理使用总结

**快速设置步骤：**
1. 从Serviceplan获取API密钥（需人工操作）
2. 在环境中设置`HANNAH_API_KEY`和`ELENA_API_KEY`
3. 使用`hannah_research`进行市场研究
4. 使用`elena_plan`进行项目规划
5. 请耐心等待——研究任务需要2-10分钟
6. 将响应整合到您的代理工作流程中

**关键原则：**
- Hannah通过研究的准确性验证想法
- Elena通过现实主义确保任务完成
- 两个代理都可以协调Sokosumi子代理以获取高级数据
- 当需要市场背景信息时，Elena会自动委托给Hannah
- 支持API和电子邮件两种沟通方式以增加灵活性

**记住：**
- 研究的深度会影响回复时间
- 设置合理的超时时间（至少3-5分钟）
- Hannah和Elena是专业的合作伙伴，而非简单的助手
- 他们会对模糊的请求或不充分的假设提出质疑
- 费用透明——在使用信用点前会提前告知您

**由Serviceplan开发 | Sokosumi提供支持**

*专业的AI合作伙伴，助力市场研究和运营规划*