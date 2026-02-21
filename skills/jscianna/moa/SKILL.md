---
name: moa
description: "**代理混合模型：** 让3个前沿模型进行讨论，然后将它们各自的最佳见解综合成一个更优的答案。费用约为每条查询0.03美元。"
author: John Scianna (@Scianna)
version: 1.2.0
requires:
  - OPENROUTER_API_KEY
cost: ~$0.03 per query (paid tier)
---
# 联合代理（Mixture of Agents, MoA）

**简而言之：** 让3个AI模型相互争论，从而获得比任何单一模型更准确的答案。成本：约0.03美元。

## 两种使用模式

### A. 独立命令行接口（Node.js）
```bash
export OPENROUTER_API_KEY="your-key"
node scripts/moa.js "Your complex question"
```

### B. OpenClaw技能（由代理协调）
```bash
# Install
clawhub install moa

# Or copy to ~/clawd/skills/moa/
```

该代理可以调用MoA来执行复杂的分析任务。

---

## 背景故事

“联合代理”（Mixture of Agents）的概念源于研究，研究表明大型语言模型（LLMs）可以通过协作提升彼此的输出质量。我开发这个工具是为了用于风险投资（VC）项目分析——在评估初创企业时，需要多种视角，而不仅仅是单一模型的观点。

**开发过程：**
1. 最初使用了5个免费的OpenRouter模型（Llama、Gemini、Mistral、Qwen、Nemotron）；
2. 在高峰时段，由于速率限制，这些模型的使用受到了严重限制；
3. 后来改用了3个付费的先进模型；
4. 结果是：每次查询的成本约为0.03美元，且得到的答案比任何单一模型都要准确。

---

## 适用场景

- **复杂分析**——尽职调查、市场研究、技术评估
- **头脑风暴**——收集多样化的想法并综合最佳方案
- **事实核查**——跨具有不同训练数据的模型进行交叉验证
- **高风险的决策**——当某个模型的盲点可能带来负面影响时
- **逆向思维**——不同的模型具有不同的偏见

**不适用场景：**
- 快速问答（响应速度较慢，延迟30-90秒）
- 实时聊天（该工具并非为实时流式对话设计）
- 简单的信息查询（使用该工具属于过度设计）

---

## 模型配置

### 收费版本（推荐）

| 角色 | 模型 | 延迟时间 | 优势 |
|------|-------|----------|----------|
| 提案者1 | `moonshotai/kimi-k2.5` | 23秒 | 具备较长的上下文理解能力和强大的推理能力 |
| 提案者2 | `z-ai/glm-5` | 36秒 | 具备较高的技术深度和不同的训练数据集 |
| 提案者3 | `minimax/minimax-m2.5` | 64秒 | 能捕捉细微差别，进行彻底的分析 |
| 整合者 | `moonshotai/kimi-k2.5` | 15秒 | 快速整合多个模型的观点 |

**选择这些模型的原因：**
- 属于前沿级别的模型，但使用量相对较少（相比GPT-4/Claude）
- 不同的训练数据意味着模型具有不同的视角
- 中文模型在某些推理任务上表现优异
- 综合使用这些模型的成本仍低于单独使用Opus模型的成本

**成本明细：**
```
3 proposers × ~$0.008 = $0.024
1 aggregator × ~$0.005 = $0.005
─────────────────────────────
Total: ~$0.029/query
```

### 免费版本（备用方案）
5个模型：Llama 3.3 70B、Gemini 2.0 Flash、Mistral Small、Nemotron 70B、Qwen 2.5 72B

⚠️ **警告：** 免费版本在高峰时段会受到速率限制。仅建议用于测试。

---

## 工作原理

```
        ┌─────────────┐
        │   PROMPT    │
        └──────┬──────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐
│Kimi 2.5│ │ GLM 5  │ │MiniMax │  ← Parallel (they "argue")
│(reason)│ │(depth) │ │(nuance)│
└───┬────┘ └───┬────┘ └───┬────┘
    │          │          │
    └──────────┼──────────┘
               ▼
       ┌──────────────┐
       │  AGGREGATOR  │
       │  (Kimi 2.5)  │
       │              │
       │ • Best of 3  │
       │ • Resolve    │
       │   conflicts  │
       │ • Synthesize │
       └──────┬───────┘
              ▼
       ┌──────────────┐
       │ FINAL ANSWER │
       │ (Synthesized)│
       └──────────────┘
```

---

## API参考

### 函数签名

```typescript
interface MoAOptions {
  prompt: string;           // Required: The question to analyze
  tier?: 'paid' | 'free';   // Default: 'paid'
}

interface MoAResult {
  synthesis: string;        // The final aggregated answer
}

// Throws on complete failure (all models down, invalid key)
// Returns partial synthesis if 1-2 models fail
async function handle(options: MoAOptions): Promise<string>
```

### 命令行接口使用方法

```bash
# Paid tier (default)
node scripts/moa.js "Your complex question"

# Free tier
node scripts/moa.js "Your question" --free
```

### 程序化使用方法

```javascript
const { handle } = require('./scripts/moa.js');

const synthesis = await handle({ 
  prompt: "Analyze the competitive moats in AI code generation",
  tier: 'paid'
});

console.log(synthesis);
```

---

## 故障处理方式

| 故障情况 | 处理方式 |
|----------|----------|
| **1个提案者失败** | 从剩余的2个模型中合成答案 |
| **2个提案者失败** | 从1个模型中合成答案（结果可能较差） |
| **所有提案者失败** | 返回错误信息 |
| **API密钥无效** | 立即显示错误并提供设置指南 |
| **免费版本的速率限制** | 显示速率限制错误 |

系统设计为能够优雅地处理故障情况。即使只有2个或3个模型能够响应，也能提供有价值的结果。

---

## 示例用法

### 风险投资尽职调查
```bash
node scripts/moa.js "Analyze the competitive landscape for AI code generation. \
Who has defensible moats? Who's likely to be commoditized? Be specific."
```

### 技术评估
```bash
node scripts/moa.js "Compare RLHF vs DPO vs RLAIF for LLM alignment. \
Which scales better? What are the failure modes of each?"
```

### 市场研究
```bash
node scripts/moa.js "What are the emerging use cases for embodied AI in 2026? \
Focus on robotics, drones, and autonomous systems. Include specific companies."
```

---

## 性能指标

| 指标 | 收费版本 | 免费版本 |
|--------|-----------|-----------|
| **50%请求的响应时间** | 约45秒 | 约60秒 |
| **95%请求的响应时间** | 约90秒 | 超过120秒 |
| **成功率** | >99% | 约80%（受速率限制影响） |
| **每次查询的成本** | 约0.03美元 | 0美元 |

---

## 使用技巧

1. **具体说明请求内容**——模糊的请求会导致模糊的回答 |
2. **要求提供结构化的信息**——例如“列出优缺点”或“列出前5个选项”，这有助于整合者更好地工作 |
3. **用于分析，而非聊天**——MoA更适合复杂的推理任务 |
4. **批量处理请求**——每次查询的延迟约为30-90秒，请相应地规划查询次数 |

---

## 安装方法

### 推荐方式：通过ClawHub安装
```bash
clawhub install moa
```

### 手动安装
1. 将`skills/moa/`文件夹复制到`~/clawd/skills/`目录中 |
2. 在环境中设置`OPENROUTER_API_KEY`变量 |
3. 之后代理就可以调用MoA来执行复杂的查询了。

---

## 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | 是 | 你的OpenRouter API密钥 |

获取API密钥的链接：https://openrouter.ai/keys

---

## 致谢

- “联合代理”（MoA）的概念来自：[Together AI Research](https://www.together.ai/blog/together-moa)
- 实现者：[@Scianna](https://x.com/Scianna)
- 该工具专为[OpenClaw](https://github.com/openclaw/openclaw)开发