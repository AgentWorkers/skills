---
name: oc-skill-router
description: OpenClaw的智能大语言模型（LLM）路由系统：通过Evolink API自动将任务分配给Claude、GPT、Gemini、DeepSeek和Kimi等模型。这种分层调度策略可节省60%至85%的成本。仅需一个API密钥，即可使用20多种文本模型。
user-invokable: true
metadata:
  openclaw:
    requires:
      env:
        - EVOLINK_API_KEY
    primaryEnv: EVOLINK_API_KEY
    os: ["macos", "linux", "windows"]
    emoji: 🧠
    homepage: https://evolink.ai
---
# Evolink Router — 智能大语言模型路由系统

通过一个 Evolink API 密钥，将所有任务路由到 6 个提供者（Claude、GPT、Gemini、DeepSeek、Kimi、Doubao）中最适合的模型。

## 安装完成后

当此技能首次加载时，会向用户显示以下提示：

- **`EVOLINK_API_KEY` 已设置：**“智能路由器已激活！我会自动为每个任务选择最适合的模型——轻量级模型适用于快速问答，旗舰模型适用于深度分析。共有 20 多个模型可供选择。开始使用吧。”
- **`EVOLINK_API_KEY` 未设置：**“智能路由器需要一个 Evolink API 密钥。请在 evolink.ai 的仪表板 → API 密钥页面进行注册。一个密钥即可使用 Claude、GPT、Gemini、DeepSeek 等模型。需要帮助设置吗？”
- **密钥已设置但模型访问失败：**“您的 API 密钥可能具有有限的模型访问权限。请在 evolink.ai/仪表板检查您的套餐。”

提示应简洁明了——只需一个问题即可引导用户继续使用。

## 外部端点

| 服务 | URL | 格式 |
|---------|-----|--------|
| Claude 模型 | `https://direct.evolink.ai/v1/messages` (POST) | Anthropic 消息 API |
| Gemini 模型 | `https://direct.evolink.ai/v1beta/models/{model}:generateContent` (POST) | Google Gemini API |
| 其他所有模型 | `https://direct.evolink.ai/v1/chat/completions` (POST) | OpenAI 聊天 API |
| 模型列表 | `https://direct.evolink.ai/v1/models` (GET) | — |

## 安全与隐私

- `EVOLINK_API_KEY` 用于验证所有模型请求。该密钥由 OpenClaw 自动注入，属于机密信息。
- 提示信息会被发送到 `direct.evolink.ai`，然后由该平台转发给上游提供者（Anthropic、OpenAI、Google 等）。
- Evolink 仅在请求生命周期内存储数据，不会保留任何数据。

## 设置方法

**1.** 获取 API 密钥：[evolink.ai](https://evolink.ai) → 仪表板 → API 密钥

**2.** 将 Evolink 提供者添加到 `~/.openclaw/openclaw.json` 文件中，并与现有配置合并。详细 JSON 配置及 curl 使用示例请参阅 `references/router-api-params.md`。

## 核心原则

1. **成本优先** — 始终选择能够处理任务的最低成本模型。仅在必要时进行升级。
2. **透明决策** — 在创建子代理时，简要告知用户选择了哪个模型及其原因。
3. **用户优先** — 如果用户指定了模型或提供者，则忽略所有路由规则。
4. **逐层处理，避免猜测** — 当不确定时，先尝试使用较简单的模型；如果效果不佳，则逐步升级到更高级的模型。

## 模型（20 多个文本模型）

### 第一层（轻量级模型）——处理约 60% 的日常任务

| 模型 | 提供者 | 适用场景 |
|-------|----------|----------|
| `claude-haiku-4-5-20251001` | Anthropic | 快速问答、分类、信息提取 |
| `gemini-2.5-flash` | Google | 多模态、快速推理 |
| `doubao-seed-2.0-mini` | ByteDance | 中文轻量级任务 |

### 第二层（平衡型模型）——处理约 30% 的日常任务

| 模型 | 提供者 | 适用场景 |
|-------|----------|----------|
| `claude-sonnet-4-6` *(主要代理)* | Anthropic | 编程、工具使用、内容创作 |
| `gpt-5.1` | OpenAI | 通用聊天、指令执行 |
| `gemini-2.5-pro` | Google | 长文本处理、多模态交互 |
| `deepseek-chat` | DeepSeek | 中文对话、高效处理 |
| `doubao-seed-2.0-pro` | ByteDance | 中文内容创作 |
| `kimi-k2-thinking-turbo` | Moonshot | 中文长文档理解 |

### 第三层（旗舰模型）——仅处理约 10% 的复杂任务

| 模型 | 提供者 | 适用场景 |
|-------|----------|----------|
| `claude-opus-4-6` | Anthropic | 深度推理、高难度决策 |
| `gpt-5.2` | OpenAI | 最强大的通用能力 |
| `gpt-5.1-thinking` | OpenAI | 复杂思维链处理 |
| `deepseek-reasoner` | DeepSeek | 数学/逻辑推理 |
| `gemini-3.1-pro-preview` | Google | 最新的多模态推理技术 |

完整模型列表及每个模型的 API 格式请参阅 `references/router-api-params.md`。

## 路由规则

优先级：**用户优先 > 任务类型匹配 > 逐层处理**

所有任务都会自动路由。用户也可以运行 `/route [任务]` 来预览路由决策结果，而无需实际执行任务。

### 第一层：用户优先

| 用户输入 | 路由到 |
|-----------|----------|
| “使用 Opus” / “进行深度分析” | `claude-opus-4-6` |
| “使用 GPT” | `gpt-5.1` |
| “使用 Gemini” | `gemini-2.5-pro` |
| “使用 DeepSeek” | `deepseek-chat` |
| “使用 Kimi” | `kimi-k2-thinking-turbo` |
| “快速回答” / “保持简单” | `claude-haiku-4-5-20251001` |
| 用户明确指定了模型名称 | 直接使用该模型 |

### 第二层：任务类型匹配

**→ 第一层**（简单问答、事实性内容、无需深度思考）：
- 问答、概念解释、状态检查、简单翻译、格式转换、信息提取、语法检查、快速计算

**→ 第二层**（内容创作、执行、多步骤任务）：
- 写作（文章、邮件、报告、社交媒体内容）、编程（功能开发、bug 修复、代码重构、测试）、数据分析（SQL、CSV、报告）、研究（市场分析、文献研究）、工作流程自动化、项目规划、旅行计划、简历优化

**→ 第三层**（需要深度推理或高风险的复杂任务）：
- 架构设计、技术选型、商业策略制定、安全审计、根本原因分析、法律审查、财务建模、跨模块代码重构（涉及 5 个以上文件）、深度研究报告

**跨提供者路由**：
- 以中文为主的任务可能路由到 Doubao/Kimi；
- 数学证明任务可能路由到 DeepSeek Reasoner；
- 需要复杂思维的任务可能路由到 GPT-5.1。详细示例请参阅 `references/cascade-examples.md`。

### 逐层处理规则

当任务类型不明确时，首先尝试成本最低的模型；如果效果不佳，则逐步升级：

```
Tier 1 (Haiku) → self-assess confidence
  High → return result
  Medium/Low → pass analysis to Tier 2

Tier 2 (Sonnet) → self-assess confidence
  High → return result
  Low → pass to Tier 3

Tier 3 (Opus) → final answer
```

信心等级：
- **高**：结果完整且正确。
- **中**：可能遗漏部分细节。
- **低**：超出模型的处理能力。

## 创建子代理的规则

**在以下情况下创建子代理：**
- 输出超过 100 行；
- 需要遍历文件；
- 执行时间超过 30 秒；
- 需要处理大量数据；
- 需要撰写长篇文本（超过 1000 字）。

**直接处理的情况：**
- 简单问答、聊天/讨论、短文本（少于 50 行）；
- 需要多轮思考的头脑风暴。

创建子代理的模板：
```javascript
sessions_spawn({
  task: "[action] + [input/context] + [expected output] + [constraints]",
  model: "evolink/[model-id]",
  runTimeoutSeconds: 300,
  cleanup: "delete"  // "keep" for important deliverables
})
```

**超时设置**：
- 第一层：120–300 秒；
- 第二层：300–600 秒；
- 第三层：600–900 秒。

## `/route` 命令

`/route [任务]` — 预览路由决策结果，无需执行任务。

## 备用方案与质量控制

| 情况 | 处理方式 |
|----------|--------|
- 子代理超时 | 通知用户，并建议使用更强大的模型重试 |
- 子代理出现错误 | 提取错误信息，判断是否可以重试 |
- 结果质量较低 | 升级到更高层的模型 |
- 用户不满意 | 询问问题原因，然后升级模型并重新执行 |
- 同一类任务连续失败多次 | 自动升级该类别的默认模型 |
- 模型不可用 | 退回到同一层的替代模型 |
- API 密钥无效 | 引导用户访问 evolink.ai/仪表板/API 密钥页面

## 技能协同

| 技能 | 使用场景 | 备注 |
|-------|------|-------|
| `evolink-media` | 图像/视频/音乐/数字人生成 | 直接使用该技能，跳过文本模型的路由 |
| 其他已安装的技能 | 如果任务需求与该技能功能匹配 | 优先使用相应技能，而非直接使用模型 |

智能路由器作为调度层，会与所有 Evolink 技能共享 `EVOLINK_API_KEY`。在讨论创意或分析技能输出时，仍会遵循常规的路由规则。

## 参考资料

- `references/router-api-params.md` — 完整的 API 格式、curl 使用示例、OpenClaw 配置文件、完整模型列表
- `references/cascade-examples.md` — 27 个场景下的路由示例及跨提供者的路由策略