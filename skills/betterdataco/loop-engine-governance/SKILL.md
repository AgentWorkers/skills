# loop-engine-governance  
该功能允许在任意 OpenClaw 工作流程中添加受管控的决策机制，包括人工审批流程、AI 推荐的过滤机制以及完善的审计追踪功能，而无需修改原有的代理逻辑。  

## 来源与维护者  
- **软件包：** `@loop-engine/adapter-openclaw`（在 npm 上发布）  
- **源代码：** https://github.com/loopengine/loop-engine/tree/main/packages/adapter-openclaw  
- **维护者：** Better Data, Inc.（https://betterdata.co）  
- **文档：** https://loopengine.io/docs/integrations/openclaw  
- **许可证：** Apache-2.0（适用于 Loop Engine 的软件包）/ MIT-0（适用于本功能）  

## 所需的环境变量  
本功能包含四个示例，每个示例需要不同的环境变量：  

| 示例 | 所需环境变量 | 提供方 |  
|---|---|---|  
| `example-expense-approval.ts` | 无 | 无需外部 API 调用 |  
| `example-ai-replenishment-claude.ts` | `ANTHROPIC_API_KEY` | Anthropic |  
| `example-infrastructure-change-openai.ts` | `OPENAI_API_KEY` | OpenAI |  
| `example-fraud-review-grok.ts` | `XAI_API_KEY` | xAI |  

请仅为您打算运行的示例设置相应的环境变量。  
费用审批示例无需 API 密钥，是推荐的入门示例。  

## 安装  
```bash
# Core (required for all examples)
npm install @loop-engine/sdk @loop-engine/adapter-memory @loop-engine/adapter-openclaw

# For the Claude example only
npm install @loop-engine/adapter-anthropic @anthropic-ai/sdk

# For the OpenAI example only
npm install @loop-engine/adapter-openai openai

# For the Grok example only
npm install @loop-engine/adapter-grok openai
```  

在安装前，请验证软件包的维护者信息：  
- `@loop-engine/*`：由 `betterdata` npm 组织发布  
- `@loop-engine/adapter-openclaw`：由 `betterdata` npm 组织发布  
- `@anthropic-ai/sdk`：由 Anthropic 发布  
- `openai`：由 OpenAI 发布  

## 发送给外部提供者的数据  
**在运行 AI 示例之前，请阅读以下内容。**  
AI 示例会在提交请求时向外部大型语言模型（LLM）提供结构化的数据。这些数据包括您通过 `createSubmission()` 方法传递的“证据”内容。  
示例中使用的均为虚构数据：  
- `example-ai-replenishment-claude.ts`：虚构的库存数据  
- `example-infrastructure-change-openai.ts`：虚构的基础设施元数据  
- `example-fraud-review-grok.ts`：虚构的交易和持卡人信息  

**在生产环境中使用前请注意：**  
- 在将真实个人身份信息（PII）、持卡人数据或受监管信息发送给 LLM 提供者之前，请务必审查其数据处理协议。  
- 请查阅 LLM 提供者的数据保留和训练政策。  
- 对于医疗、金融、制药等受监管行业，确保提供商的协议涵盖了您打算传输的数据类型。  
- 在将数据作为“证据”传递之前，可以考虑对敏感字段进行脱敏或加密处理。  

Loop Engine 会将其捕获的证据保存在本地审计追踪系统中，并将这些证据作为请求的一部分发送给 LLM 提供者。需要注意的是，Loop Engine 本身从不直接对外传输数据；只有 AI 提供者的适配器才会发送数据（且仅限于您明确指定的“证据”内容）。  

## 本功能的用途  
该功能将 [Loop Engine](https://loopengine.io) 与 OpenClaw 集成，使得任何工作流程步骤都能受到以下机制的管控：  
- **人工审批流程**：仅允许指定的人工操作员触发流程转换；  
- **AI 推荐的过滤机制**：当 AI 的推荐结果低于预设的置信度阈值时，会阻止流程继续执行；  
- **证据记录**：确保每个决策都附带结构化的背景信息；  
- **审计追踪**：所有流程转换都会被记录下来，包括时间戳，并且不可篡改。  

## 与 OpenClaw 的集成方式  
这些管控机制在运行时生效（而非在请求提示阶段）。  

## 管理权重的计算方式  
系统会依次评估三种权重因素，所有因素都必须满足要求：  

**1. 置信度阈值（数值判断）**  
每个 AI 请求都会附带一个 0–1 的置信度分数。如果分数低于预设阈值，系统会阻止流程继续执行。  
**2. 管理规则的优先级（严格/宽松）**  
严格规则会无视其他因素，直接阻止流程执行；仅依赖人工审批的规则具有绝对的约束力（即置信度分数无法改变其决策结果）。  
**3. 证据完整性（结构化检查）**  
系统会检查是否提供了所有必需的证据字段；缺少任何字段都会导致流程被阻止。  

**评估顺序：**  
```
1. Actor authorized for this signal?
2. Required evidence fields present?
3. Confidence score above threshold?
4. All hard guards pass?
```  

## 快速入门（无需 API 密钥）  
```typescript
import { createLoopSystem, parseLoopYaml, CommonGuards } from '@loop-engine/sdk'
import { MemoryAdapter } from '@loop-engine/adapter-memory'

const definition = parseLoopYaml(`
  loopId: approval.workflow
  name: Approval Workflow
  version: 1.0.0
  initialState: pending
  states:
    - stateId: pending
      label: Pending Approval
    - stateId: approved
      label: Approved
      terminal: true
  transitions:
    - transitionId: approve
      from: pending
      to: approved
      signal: approve
      allowedActors: [human]
      guards: [human-only]
`)

const system = createLoopSystem({
  storage: new MemoryAdapter(),
  guards: CommonGuards,
})

const loop = await system.startLoop({ definition, context: {} })

await system.transition({
  loopId: loop.loopId,
  signalId: 'approve',
  actor: { id: 'alice', type: 'human' },
  evidence: { reviewNote: 'Approved' },
})
```  

## 包含的示例  
| 文件 | 提供方 | API 密钥 |  
|---|---|---|  
| `example-expense-approval.ts` | 无 | 无需 API 密钥 |  
| `example-ai-replenishment-claude.ts` | Anthropic Claude | `ANTHROPIC_API_KEY` |  
| `example-infrastructure-change-openai.ts` | OpenAI GPT-4o | `OPENAI_API_KEY` |  
| `example-fraud-review-grok.ts` | xAI Grok 3 | `XAI_API_KEY` |  

所有示例均使用虚构数据。在使用真实个人身份信息或受监管数据之前，请务必先审查相关提供者的数据处理协议。  

## 许可证  
- MIT-0：允许免费使用、修改和重新分发；无需注明来源。  
- `@loop-engine/*` 软件包遵循 Apache-2.0 许可证；  
- 提供者的 SDK 依据各自维护者的规定进行许可。