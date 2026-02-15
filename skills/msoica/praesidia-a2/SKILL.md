---
name: Praesidia
description: 验证AI代理，检查信任评分（0-100），获取A2A代理信息，发现市场中的代理，并为安全和合规性设置防护措施。当用户提及代理验证、信任评分、代理发现、A2A协议、代理身份、代理市场、防护措施、安全策略、内容审核，或询问“这个代理安全吗？”或“寻找能够执行某任务的代理”或“为我的代理设置防护措施”时，请使用这些功能。
metadata: {"openclaw":{"requires":{"env":["PRAESIDIA_API_KEY"]},"primaryEnv":"PRAESIDIA_API_KEY","homepage":"https://praesidia.ai","emoji":"🛡️"}}
---

# Praesidia 代理身份验证与安全防护机制

用于验证 AI 代理，检查信任评分（0-100 分），发现市场中的代理，并实施安全与合规性防护措施。

## 核心功能

- **验证代理** - 检查代理是否已注册、经过验证以及是否可信
- **信任评分** - 查看 0-100 分的信任评级和验证状态
- **代理发现** - 根据能力在市场中搜索公开代理
- **安全防护** - 为代理应用安全策略和内容审核规则
- **A2A 协议** - 获取标准的代理间通信协议卡片

## 先决条件

1. Praesidia 账户：https://praesidia.ai
2. 从设置 → API 密钥中获取 API 密钥
3. 在 `~/.openclaw/openclaw.json` 中进行配置：

```json
{
  "skills": {
    "entries": {
      "praesidia": {
        "apiKey": "pk_live_your_key_here",
        "env": {
          "PRAESIDIA_API_URL": "https://api.praesidia.ai"
        }
      }
    }
  }
}
```

对于本地开发，使用 `http://localhost:3000` 作为 URL。

---

## 快速参考

### 1. 验证代理

**用户请求：**“chatbot-v2 代理安全吗？” / “验证 chatbot-v2 代理”

**你的操作：**
```javascript
web_fetch({
  url: "${PRAESIDIA_API_URL}/agents/chatbot-v2/agent-card",
  headers: {
    "Authorization": "Bearer ${PRAESIDIA_API_KEY}",
    "Accept": "application/json"
  }
})
```

**向用户展示：**
- ✅ 代理名称及描述
- 🛡️ **信任评分（0-100 分）** 和信任等级
- ✓ 验证状态（验证日期）
- 🔧 代理功能
- 📜 合规性（SOC2、GDPR 等）
- 🔗 代理卡片链接

**示例输出：**
```
✅ ChatBot V2 is verified and safe to use!

Trust Score: 92.5/100 (VERIFIED)
Status: ACTIVE
Capabilities: message:send, task:create, data:analyze
Compliance: SOC2, GDPR
Last verified: 2 days ago

Agent card: https://api.praesidia.ai/agents/chatbot-v2/agent-card
```

---

### 2. 查看代理的安全防护措施

**用户请求：**“我的代理配置了哪些安全防护措施？” / “显示 chatbot-v2 的安全策略”

**你的操作：**
```javascript
// First, get the user's organization ID from their profile or context
// Then fetch guardrails
web_fetch({
  url: "${PRAESIDIA_API_URL}/organizations/${orgId}/guardrails?agentId=${agentId}",
  headers: {
    "Authorization": "Bearer ${PRAESIDIA_API_KEY}",
    "Accept": "application/json"
  }
})
```

**向用户展示：**
- 安全防护措施的列表，包括：
  - 名称和描述
  - 类型（RULE、ML、LLM）
  - 类别（内容、安全、合规等）
  - 操作（阻止、警告、删除、替换）
  - 适用范围（输入、输出、两者）
  - 启用状态
  - 触发次数

**示例输出：**
```
Found 3 guardrails for ChatBot V2:

1. PII Detection (ENABLED)
   - Type: ML | Category: SECURITY
   - Scope: BOTH (input & output)
   - Action: REDACT sensitive data
   - Triggered: 45 times

2. Toxic Language Filter (ENABLED)
   - Type: RULE | Category: CONTENT
   - Scope: BOTH
   - Action: BLOCK toxic content
   - Triggered: 12 times

3. Financial Advice Warning (ENABLED)
   - Type: LLM | Category: COMPLIANCE
   - Scope: OUTPUT only
   - Action: WARN if detected
   - Triggered: 3 times
```

---

### 3. 查看可用的安全防护模板

**用户请求：**“有哪些可用的安全防护模板？” / “显示安全防护模板”

**你的操作：**
```javascript
web_fetch({
  url: "${PRAESIDIA_API_URL}/organizations/${orgId}/guardrails/templates",
  headers: {
    "Authorization": "Bearer ${PRAESIDIA_API_KEY}",
    "Accept": "application/json"
  }
})
```

**可用模板：**

**内容审核：**
- TOXIC_LANGUAGE - 检测有害语言
- PROFANITY_FILTER - 过滤脏话
- HATE_SPEECH - 检测仇恨言论
- VIOLENCE_DETECTION - 检测暴力内容
- ADULT_CONTENT - 过滤成人内容

**安全：**
- PII_DETECTION - 检测个人身份信息
- CREDITCARD_DETECTION - 检测信用卡号码
- SSN_DETECTION - 检测社会安全号码
- API_KEY_DETECTION - 检测泄露的 API 密钥
- PROMPT_INJECTION - 检测提示注入攻击
- JAILBREAK_DETECTION - 检测越狱尝试

**合规性：**
- FINANCIAL_ADVICE - 标记财务建议
- MEDICAL_ADVICE - 标记医疗建议
- LEGAL_ADVICE - 标记法律建议
- GDPR_COMPLIANCE - 执行 GDPR 规则
- HIPAA_COMPLIANCE - 执行 HIPAA 规则

**品牌安全：**
- COMPETITOR_MENTIONS - 检测竞争对手提及
- POSITIVE_TONE - 确保语气积极
- BRAND_VOICE - 维护品牌形象
- OFF_TOPIC_DETECTION - 检测离题回复

**准确性：**
- HALLUCINATION_DETECTION - 检测幻觉内容
- FACT_CHECKING - 核实事实
- SOURCE_VALIDATION - 验证信息来源
- CONSISTENCY_CHECK - 检查内容一致性

---

### 4. 为代理应用安全防护措施

**用户请求：**“为我的聊天机器人添加 PII 检测功能” / “为代理 xyz 应用有害语言过滤规则”

**你的操作：**
```javascript
web_fetch({
  url: "${PRAESIDIA_API_URL}/organizations/${orgId}/guardrails",
  method: "POST",
  headers: {
    "Authorization": "Bearer ${PRAESIDIA_API_KEY}",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    name: "PII Detection",
    description: "Automatically detect and redact PII",
    agentId: "${agentId}",
    template: "PII_DETECTION",
    type: "ML",
    category: "SECURITY",
    scope: "BOTH",
    action: "REDACT",
    severity: "HIGH",
    isEnabled: true,
    priority: 0
  })
})
```

**安全防护选项：**

**类型：**
- RULE - 简单的正则表达式/关键词匹配（快速）
- ML - 机器学习模型（平衡性较高）
- LLM - 基于大型语言模型的验证（最准确）

**类别：**
- CONTENT - 内容审核
- SECURITY - 安全检查
- COMPLIANCE - 合规性检查
- BRAND - 品牌安全
- ACCURACY - 准确性检查
- CUSTOM - 自定义规则

**适用范围：**
- INPUT - 仅验证用户输入
- OUTPUT - 仅验证代理输出
- BOTH - 同时验证输入和输出

**操作：**
- BLOCK - 完全阻止请求/响应
- WARN - 记录警告但允许通过
- REDACT - 遮盖违规内容
- REPLACE - 用替代内容替换
- RETRY - 用修改后的提示重新尝试
- ESCALATE - 提升到人工审核

**严重程度：**
- 低、中、高、严重

---

### 5. 根据安全防护措施检查内容

**用户请求：**“检查这条消息是否符合安全防护规则：[内容]”

**你的操作：**
```javascript
web_fetch({
  url: "${PRAESIDIA_API_URL}/organizations/${orgId}/guardrails/validate",
  method: "POST",
  headers: {
    "Authorization": "Bearer ${PRAESIDIA_API_KEY}",
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    content: "User's message here",
    agentId: "${agentId}",
    scope: "INPUT"
  })
})
```

**响应显示：**
- 内容是否通过安全防护
- 触发了哪些安全防护措施
- 建议的操作（阻止、删除、警告）
- 修改后的内容（如果进行了删除）

---

### 6. 发现公开代理

**用户请求：**“查找公开的数据分析代理” / “显示聊天机器人代理”

**你的操作：**
```javascript
web_fetch({
  url: "${PRAESIDIA_API_URL}/agents/discovery?visibility=PUBLIC&search=data",
  headers: { "Accept": "application/json" }
  // Authorization optional for public agents (includes it for more results)
})
```

**可用过滤器：**
- `?visibility=PUBLIC` - 公开市场代理
- `?role=SERVER` - 提供服务的代理
- `?role=CLIENT` - 消费服务的代理
- `?status=ACTIVE` - 仅限活跃代理
- `?search=关键词` - 按名称/描述搜索

**向用户展示：**
- 匹配的代理列表，包括：
  - 名称、描述、代理 ID
  - 信任评分和等级
  - 角色（服务器/客户端）
  - 主要功能
  - 完整卡片链接

**示例输出：**
```
Found 2 public data analysis agents:

1. OpenData Analyzer (VERIFIED - 88.0/100)
   - Capabilities: data:analyze, chart:generate, report:create
   - Role: SERVER | Status: ACTIVE
   - Card: https://api.praesidia.ai/agents/opendata-1/agent-card

2. CSV Processor (STANDARD - 70.0/100)
   - Capabilities: file:parse, data:transform, export:json
   - Role: SERVER | Status: ACTIVE
   - Card: https://api.praesidia.ai/agents/csv-proc/agent-card
```

---

### 7. 列出用户的代理

**用户请求：**“显示我的代理” / “列出我所有的服务器代理”

**你的操作：**
```javascript
web_fetch({
  url: "${PRAESIDIA_API_URL}/agents/discovery?role=SERVER",
  headers: {
    "Authorization": "Bearer ${PRAESIDIA_API_KEY}",
    "Accept": "application/json"
  }
})
```

这将显示用户可以访问的所有代理（包括自己的代理以及团队/组织的代理）。

---

## 信任等级指南

清晰地展示信任信息，以帮助用户做出决策：

| 信任评分 | 等级 | 含义 | 建议 |
|-------------|-------|---------|----------------|
| 90-100 | **已验证** | 经过全面审核，符合规定，身份已验证 | ✅ 可安全使用 |
| 70-89 | **标准** | 声誉良好，基本验证 | ✅ 通常安全 |
| 50-69 | **有限** | 验证较少 | ⚠️ 使用时需谨慎 |
| 0-49 | **不可信** | 未验证或声誉较差 | ❌ 不推荐 |

始终以数字形式显示信任评分（例如，92.5/100）和等级（例如，已验证）。

---

## 错误处理

| 错误代码 | 含义 | 告诉用户的提示 |
|-------|---------|-------------------|
| 401 未授权 | API 密钥缺失/无效 | “请检查 `~/.openclaw/openclaw.json` 中的 `PRAESIDIA_API_KEY`” |
| 403 禁止访问 | 没有权限 | “您无权访问该代理” |
| 404 未找到 | 代理不存在 | “未找到该代理。请检查代理 ID” |
| 500 服务器错误 | Praesidia API 故障 | “Praesidia API 暂时不可用。请稍后再试” |

---

## API 端点

### GET /agents/:id/agent-card
获取包含信任数据的详细代理卡片。

**认证：** 对于私有/团队/组织代理是必需的，对于公开代理是可选的
**返回：** A2A 代理卡片 + Praesidia 扩展信息（信任、合规性）

### GET /agents/discovery
使用过滤器列出/搜索代理。

**认证：** 可选（认证后返回更多结果）
**查询参数：** `role`、`status`、`visibility`、`search`
**返回：** 包含卡片链接的代理摘要数组

---

## 安全防护最佳实践

在帮助用户设置安全防护措施时：

1. **从模板开始** - 先使用预定义的模板，再自定义规则
2. **多层防护** - 结合多种安全防护措施（个人身份信息、有害内容、合规性）
3. **启用前测试** - 使用验证端点先测试内容
4. **定期监控触发情况** - 定期检查统计数据以调整阈值
5. **适当设置适用范围** - 对用户输入使用 INPUT，对代理输出使用 OUTPUT
6. **选择合适的操作**：
   - 对于严重的安全问题（如个人身份信息、提示注入）使用 **BLOCK**
   - 对于可以屏蔽的敏感数据使用 **REDACT**
   - 对于需要记录的合规性/品牌问题使用 **WARN**
   - 对于需要人工审核的边缘情况使用 **ESCALATE**

---

## 其他最佳实践

1. **推荐前务必验证** - 在推荐代理前检查其信任评分
2. **解释信任等级** - 用户可能不清楚 “已验证” 的含义
3. **按服务器角色筛选** - 根据用户的需求筛选代理
4. **展示合规性信息** - 对企业用户非常重要（如 SOC2、GDPR）
5. **以数字形式显示信任评分** - 92.5/100 比单纯的 “已验证” 更清晰
6. **组合使用多种安全防护措施** - 结合安全、内容和合规性防护

---

## 常见用户操作模式

### 模式 1：安全检查
```
User: "Is agent xyz safe to use?"
You: [Fetch agent card, check trust score]
     "Agent xyz has a trust score of 85/100 (STANDARD).
      It's verified for basic operations. What would you like to use it for?"
```

### 模式 2：功能发现
```
User: "I need an agent that can analyze spreadsheets"
You: [Search discovery with visibility=PUBLIC&search=spreadsheet]
     "I found 3 spreadsheet analysis agents. The highest rated is..."
```

### 模式 3：代理管理
```
User: "Show me all my agents that are inactive"
You: [Fetch discovery with status=INACTIVE]
     "You have 2 inactive agents: [list with trust scores]"
```

### 模式 4：应用安全措施
```
User: "I need to secure my chatbot against PII leaks"
You: [List available templates, recommend PII_DETECTION]
     [Apply guardrail with REDACT action on BOTH scope]
     "I've added PII Detection (ML-powered) to your chatbot.
      It will automatically redact sensitive information in both
      user inputs and bot responses."
```

### 模式 5：合规性检查
```
User: "My agent handles healthcare data. What guardrails should I add?"
You: [Check if HIPAA compliance is required]
     [Recommend HIPAA_COMPLIANCE + PII_DETECTION + AUDIT_LOGGING]
     "For healthcare data, I recommend these guardrails:
      1. HIPAA Compliance (BLOCK on violations)
      2. PII Detection (REDACT)
      3. Medical Advice Warning (WARN)
      Would you like me to apply these?"
```

---

## 环境变量

- `PRAESIDIA_API_KEY`（必需） - 从 https://app.praesidia.ai 获取的 API 密钥
- `PRAESIDIA_API_URL`（可选） - 默认为 `https://api.praesidia.ai`
  - 生产环境：`https://api.praesidia.ai`
  - 本地开发：`http://localhost:3000`
  - 自定义：您的部署 URL

---

## 其他资源

- **完整设置指南：** 查看此技能文件夹中的 README.md
- **API 文档：** https://app.praesidia.ai/docs/api
- **A2A 协议：** https://a2a-protocol.org
- **支持：** hello@praesidia.ai 或 https://discord.gg/e9EwZfHS

---

## 安全与隐私

- 所有生产环境请求均使用 HTTPS
- API 密钥存储在 OpenClaw 配置文件中（不会暴露给用户）
- 私有/团队/组织代理需要认证
- 公开代理无需认证即可访问
- 信任验证可防止恶意代理的入侵