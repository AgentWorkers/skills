---
name: sealvera
description: "**具有防篡改功能的审计追踪系统，用于记录AI代理的决策过程。**  
该系统适用于以下场景：  
- 记录大型语言模型（LLM）的决策过程；  
- 确保AI系统符合相关法规（如欧盟《人工智能法案》、HIPAA、GDPR或SOC 2）；  
- 审计AI系统的合规性；  
- 当用户询问AI决策的审计记录、可解释性或SealVera的相关信息时。"
credentials:
  - name: SEALVERA_API_KEY
    description: "Your SealVera API key (starts with sv_). Get a free key at app.sealvera.com."
    required: true
  - name: SEALVERA_ENDPOINT
    description: "SealVera server URL. Defaults to https://app.sealvera.com."
    required: false
  - name: SEALVERA_AGENT
    description: "Agent name shown in dashboard. Defaults to 'openclaw-agent'."
    required: false
tags:
  - compliance
  - audit
  - ai-governance
  - llm
  - observability
  - eu-ai-act
  - hipaa
  - gdpr
  - soc2
  - fintech
  - tamper-evident
  - explainability
  - langchain
  - openai
  - anthropic
  - responsible-ai
---
# SealVera 技能（适用于 OpenClaw）

**为 OpenClaw 的代理所做出的每个 AI 决策提供加密封装的、防篡改的审计追踪功能。**

SealVera 是一个 AI 决策审计基础设施。该技能可将任何 OpenClaw 代理连接到 SealVera，从而自动记录、加密签名、链接并监控其做出的每个决策。它专为在金融、医疗保健、法律和保险领域使用 AI 的团队设计。

> 满足欧盟 AI 法规 · SOC 2 标准 · HIPAA 标准 · GDPR 标准 · FINRA 标准 · ISO 42001 标准

---

## 为什么选择 SealVera？

- **防篡改**：每个决策都会经过 RSA-2048 加密哈希处理并链接在一起；任何篡改行为都能被检测出来。
- **简单易用**：只需执行 `init()` 函数并调用一次补丁函数，即可记录每个大型语言模型（LLM）的决策。
- **完全可解释**：会捕获输入数据、输出结果、推理过程、置信度评分以及所使用的模型。
- **实时仪表盘**：支持在 [app.sealvera.com](https://app.sealvera.com) 上搜索、过滤和导出数据。
- **异常行为检测**：当代理行为偏离基线时会发出警报。
- **支持多种 LLM**：包括 OpenAI、Anthropic、Gemini、Ollama、LangChain、CrewAI、AutoGen 等。
- **零成本部署**：无需额外基础设施，安装仅需几秒钟。

---

## 首次使用？请运行设置流程

检查 SealVera 是否已配置：

```javascript
const fs = require('fs');
const path = require('path');
const configured = fs.existsSync(path.join(process.env.OPENCLAW_WORKSPACE || process.cwd(), '.sealvera.json'));
```

如果不存在 `.sealvera.json` 文件，请运行设置流程：

```bash
node <skill_dir>/scripts/setup.js
```

设置流程将：
1. 请求您的 API 密钥（可在 [app.sealvera.com](https://app.sealvera.com) 免费获取）。
2. 验证连接性并显示组织/计划信息。
3. 将 `sealvera-log.js` 文件复制到工作区。
4. 在 `AGENTS.md` 文件中添加必要的子代理审计规则。
5. 生成 `.sealvera.json` 配置文件。
6. 运行测试日志以确认整个系统的正常运行。

**设置完成后，您创建的每个子代理都会自动被审计。**

如果用户要求“安装 SealVera”、“设置 SealVera”或“连接 SealVera”，请直接运行设置流程，而不要仅进行描述。

---

## 日志记录方式

设置完成后，子代理的日志记录将通过 `AGENTS.md` 文件自动完成。
如需手动记录日志，请参考以下说明：

```javascript
const log = require('./sealvera-log');
await log({
  action: 'describe what happened',
  decision: 'COMPLETED',
  input:  { task: '...' },
  output: { result: '...' },
  reasoning: [{ factor: 'outcome', value: 'ok', signal: 'safe', explanation: '...' }]
});
```

每条日志记录包括：输入数据/输出结果、推理过程、RSA-2048 签名、日志链接、时间戳、使用的模型以及代理名称。

---

## 决策分类

**任务/代理执行状态：**

| 决策 | 含义 |
|---|---|
| `COMPLETED` | 任务成功完成 |
| `RESPONSED` | 回答了问题/返回了结果 |
| `FAILED` | 任务失败 |
| `ERROR` | 发生意外异常 |
| `ESCALATED` | 任务被转交给人类或更高级别的代理处理 |
| `SKIPPED` | 任务被故意跳过 |
| `PARTIAL` | 任务有条件地完成 |

**审批/权限控制：**

| 决策 | 含义 |
|---|---|
| `APPROVED` | 请求获得批准 |
| `REJECTED` | 请求被拒绝 |
| `FLAGGED` | 需要人工审核 |

**测试结果：**

| 决策 | 含义 |
|---|---|
| `PASSED` | 测试通过 |
| `FAILED` | 测试失败 |
| `SKIPPED` | 测试被跳过 |

---

## 子代理审计规则

请在每个 `sessions_spawn` 任务中添加以下代码段：

```
---
MANDATORY: Before you finish, log your result to SealVera:
  const log = require('<workspace>/sealvera-log');
  await log({
    action: '<what you did>',
    decision: 'COMPLETED',
    input: { task: '<summary>' },
    output: { result: '<summary>' },
    reasoning: [{ factor: 'outcome', value: '<result>', signal: 'safe', explanation: '<why>' }]
  });
Vocabulary: task=COMPLETED/FAILED | test=PASSED/FAILED | gate=APPROVED/REJECTED | handoff=ESCALATED
```

---

## 检查状态

```bash
node <skill_dir>/scripts/status.js
```

---

## 获取您的 API 密钥

请在 **[app.sealvera.com](https://app.sealvera.com)** 注册账户——免费 tier 每月支持 10,000 次决策记录。

---

## 参考资料

有关所有 SDK 方法和日志字段格式的详细信息，请参阅 `references/api.md`。
有关法规合规性的详细信息，请参阅 `references/compliance.md`（包括欧盟 AI 法规、FINRA、HIPAA、GDPR、SOC 2 等）。