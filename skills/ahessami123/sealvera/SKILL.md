---
name: sealvera
description: "**AI代理决策的防篡改审计追踪功能**  
该功能适用于记录大型语言模型（LLM）的决策过程，确保AI系统的合规性。它可用于满足欧盟《人工智能法案》（EU AI Act）、HIPAA、GDPR或SOC 2等法规的要求。当用户对AI决策的审计追踪、可解释性或SealVera相关事宜提出疑问时，该功能也能提供必要的支持。"
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

**为 OpenClaw 的代理所做的每一个 AI 决策提供加密封装、防篡改的审计追踪功能。**

SealVera 是一种 AI 决策审计基础设施。该技能可将任何 OpenClaw 代理连接到 SealVera，从而自动记录、加密签名、链接并监控其做出的每一个决策。它专为在金融、医疗、法律和保险等领域使用 AI 的团队设计。

> 满足欧盟 AI 法规 · SOC 2 标准 · HIPAA 标准 · GDPR 标准 · FINRA 标准 · ISO 42001 标准

---

## 为什么选择 SealVera？

- **防篡改**：每个决策都会通过 RSA-2048 进行加密哈希处理，并形成链式记录；任何篡改行为都能被检测到。
- **简单易用**：只需执行 `init()` 函数并调用一次补丁函数，即可记录所有大型语言模型（LLM）的决策。
- **完全可解释**：系统会捕获输入数据、输出结果、推理过程、置信度评分以及所使用的模型。
- **实时仪表盘**：支持在 [app.sealvera.com](https://app.sealvera.com) 上搜索、过滤和导出日志数据。
- **异常检测**：当代理行为偏离基线时，系统会发出警报。
- **兼容多种 LLM**：支持 OpenAI、Anthropic、Gemini、Ollama、LangChain、CrewAI、AutoGen 等多种大型语言模型。
- **零成本部署**：无需额外基础设施，安装仅需几秒钟。

---

## 首次使用？请运行设置流程

请检查 SealVera 是否已配置：

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

**设置完成后，您创建的每个子代理都将自动接受审计。**

如果用户请求“安装 SealVera”、“设置 SealVera”或“连接 SealVera”，请直接运行设置流程，而无需进行描述。

---

## 日志记录机制

设置完成后，子代理的日志记录将通过 `AGENTS.md` 文件自动完成。如需手动记录日志，请参考以下说明：

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

每条日志记录包含以下内容：输入数据/输出结果、推理过程、RSA-2048 签名、日志链接、时间戳、使用的模型以及代理名称。

---

## 决策分类

**任务/代理执行状态：**

| 决策 | 含义 |
|---|---|
| `COMPLETED` | 任务成功完成 |
| `RESPONSED` | 回答了问题或返回了结果 |
| `FAILED` | 任务失败 |
| `ERROR` | 发生意外异常 |
| `ESCALATED` | 任务被转交给人工处理或更高级别的代理 |
| `SKIPPED` | 任务被有意跳过 |
| `PARTIAL` | 任务部分完成（存在某些限制） |

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

## 检查系统状态

```bash
node <skill_dir>/scripts/status.js
```

---

## 获取您的 API 密钥

请在 **[app.sealvera.com](https://app.sealvera.com)** 注册账户——免费 tier 每月支持记录 10,000 条决策日志。

---

## 参考资料

有关所有 SDK 方法和日志字段格式的详细信息，请参阅 `references/api.md`。
有关相关法规的映射信息（欧盟 AI 法规、FINRA、HIPAA、GDPR、SOC 2），请参阅 `references/compliance.md`。