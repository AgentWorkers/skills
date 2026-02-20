---
name: swarm
description: 将您的大语言模型（LLM）成本降低200倍。将并行处理、批量处理以及研究工作交给Gemini Flash工作者来完成，而不是继续使用昂贵的主要模型。
homepage: https://github.com/Chair4ce/node-scaling
metadata: {"clawdbot":{"emoji":"🐝","requires":{"bins":["node"]}}}
---
# Swarm — 将您的LLM成本降低200倍

**将昂贵的模型转变为经济实惠的日常工具。将繁琐的任务交给Gemini Flash工作者来处理——并行处理、批量处理、进行研究——成本仅为原来的几分之一。**

## 一目了然

| 任务类型 | 所需时间 | 成本 |
|--------------|------|------|
| Opus（顺序执行） | 约30秒 | 约0.50美元 |
| Swarm（并行执行） | 约1秒 | 约0.003美元 |

## 适用场景

Swarm非常适合以下场景：
- **3个或更多独立任务**（如研究、总结、比较）
- **比较或研究多个主题**
- **获取/分析多个URL的内容**
- **批量处理**（文档、实体、事实）
- **需要多角度分析的复杂任务** → 使用链式执行方式

## 快速参考

```bash
# Check daemon (do this every session)
swarm status

# Start if not running
swarm start

# Parallel prompts
swarm parallel "What is X?" "What is Y?" "What is Z?"

# Research multiple subjects
swarm research "OpenAI" "Anthropic" "Mistral" --topic "AI safety"

# Discover capabilities
swarm capabilities
```

## 执行模式

### 并行执行（v1.0）
每个提示同时由N个工作者处理。最适合独立任务。

```bash
swarm parallel "prompt1" "prompt2" "prompt3"
```

### 研究模式（v1.1）
多阶段处理：搜索 → 获取 → 分析。利用Google搜索功能进行数据获取。

```bash
swarm research "Buildertrend" "Jobber" --topic "pricing 2026"
```

### 链式执行模式（v1.3） —— 精细化流程
数据会经过多个处理阶段，每个阶段都有不同的处理方式/过滤器。各阶段按顺序执行；同一阶段内的任务则并行处理。

**阶段类型：**
- `parallel` —— N个输入 → N个工作者（相同处理方式）
- `single` —— 合并后的输入 → 1个工作者
- `fan-out` —— 1个输入 → N个具有不同处理方式的工作者
- `reduce` —— N个输入 → 1个综合输出结果

**自动构建链式流程：** 指定处理需求，系统会自动选择最佳流程：
```bash
curl -X POST http://localhost:9999/chain/auto \
  -d '{"task":"Find business opportunities","data":"...market data...","depth":"standard"}'
```

**手动构建链式流程：**
```bash
swarm chain pipeline.json
# or
echo '{"stages":[...]}' | swarm chain --stdin
```

**深度预设：** `quick`（2个阶段），`standard`（4个阶段），`deep`（6个阶段），`exhaustive`（8个阶段）

**内置的处理方式：** 提取器、过滤器、丰富器、分析器、合成器、挑战者、优化器、策略师、研究员、评论者

**预览（不执行）：**
```bash
curl -X POST http://localhost:9999/chain/preview \
  -d '{"task":"...","depth":"standard"}'
```

### 基准测试（v1.3）
在同一任务上比较顺序执行、并行执行和链式执行的效果，使用LLM作为评估标准。

```bash
curl -X POST http://localhost:9999/benchmark \
  -d '{"task":"Analyze X","data":"...","depth":"standard"}'
```

评估指标包括6个方面：准确性（权重2倍）、深度（1.5倍）、完整性、连贯性、可操作性（1.5倍）、细微差别。

### 功能发现（v1.3）
允许用户发现可用的执行模式：

```bash
swarm capabilities
# or
curl http://localhost:9999/capabilities
```

## 提示缓存（v1.3.2）
使用LRU缓存机制存储LLM的响应结果。**缓存命中速度提升212倍**（并行执行时），**链式执行时提升514倍**。
- 缓存键由指令哈希值、输入内容和处理方式共同决定
- 最大缓存容量为500条记录，缓存有效期为1小时
- 可在守护进程重启后保留缓存数据
- 可通过设置`task.cache = false`来禁用缓存

```bash
# View cache stats
curl http://localhost:9999/cache

# Clear cache
curl -X DELETE http://localhost:9999/cache
```

缓存统计信息可在`swarm status`中查看。

## 阶段重试（v1.3.2）
如果链式执行中的某个阶段失败，仅重试该阶段的任务，不会重新执行整个流程。默认重试次数为1次。可通过`phase.retries`配置每个阶段的重试次数，或通过`options.stageRetries`全局配置。

## 成本跟踪（v1.3.1）
所有端点在完成任务时会返回成本数据：
- `session` —— 当前守护进程会话的总成本
- `daily` —— 在重启后持续记录，累计全天成本

```bash
swarm status        # Shows session + daily cost
swarm savings       # Monthly savings report
```

## 网页搜索（v1.1）
工作者通过Google搜索功能在网页上查找信息（仅限Gemini，无额外费用）。

```bash
# Research uses web search by default
swarm research "Subject" --topic "angle"

# Parallel with web search
curl -X POST http://localhost:9999/parallel \
  -d '{"prompts":["Current price of X?"],"options":{"webSearch":true}}'
```

## JavaScript API

```javascript
const { parallel, research } = require('~/clawd/skills/node-scaling/lib');
const { SwarmClient } = require('~/clawd/skills/node-scaling/lib/client');

// Simple parallel
const result = await parallel(['prompt1', 'prompt2', 'prompt3']);

// Client with streaming
const client = new SwarmClient();
for await (const event of client.parallel(prompts)) { ... }
for await (const event of client.research(subjects, topic)) { ... }

// Chain
const result = await client.chainSync({ task, data, depth });
```

## 守护进程管理

```bash
swarm start              # Start daemon (background)
swarm stop               # Stop daemon
swarm status             # Status, cost, cache stats
swarm restart            # Restart daemon
swarm savings            # Monthly savings report
swarm logs [N]           # Last N lines of daemon log
```

## 性能（v1.3.2）

| 执行模式 | 任务数量 | 所需时间 | 备注 |
|------|-------|------|-------|
| 并行执行（简单模式） | 5个任务 | 约700毫秒 | 每个任务实际执行时间约142毫秒 |
| 并行执行（高负载模式） | 10个任务 | 约1.2秒 | 每个任务实际执行时间约123毫秒 |
| 链式执行（标准模式） | 5个任务 | 约14秒 | 多阶段、多角度处理 |
| 链式执行（快速模式） | 2个任务 | 约3秒 | 两阶段处理（提取+合成） |
| 缓存命中 | 任意数量的任务 | 约3-5毫秒 | 执行速度提升200-500倍 |
| 研究模式（网页搜索） | 2个任务 | 约15秒 | 使用Google搜索功能 |

## 配置文件位置：`~/.config/clawdbot/node-scaling.yaml`

```yaml
node_scaling:
  enabled: true
  limits:
    max_nodes: 16
    max_concurrent_api: 16
  provider:
    name: gemini
    model: gemini-2.0-flash
  web_search:
    enabled: true
    parallel_default: false
  cost:
    max_daily_spend: 10.00
```

## 故障排除

| 问题 | 解决方案 |
|-------|-----|
| 守护进程未运行 | 执行`swarm start`命令 |
| 未设置API密钥 | 设置`GEMINI_API_KEY`或运行`npm run setup` |
| 被限制请求频率 | 降低配置文件中的`max_concurrent_api`值 |
| 网页搜索无法使用 | 确保已启用`web_search.enabled`功能 |
| 缓存中的结果过时 | 使用`curl -X DELETE http://localhost:9999/cache`清除缓存 |
| 链式执行速度过慢 | 设置`depth: "quick"`或检查上下文大小 |

## 结构化输出（v1.3.7）
强制输出JSON格式，并进行模式验证——确保结构化任务的处理过程无误。

```bash
# With built-in schema
curl -X POST http://localhost:9999/structured \
  -d '{"prompt":"Extract entities from: Tim Cook announced iPhone 17","schema":"entities"}'

# With custom schema
curl -X POST http://localhost:9999/structured \
  -d '{"prompt":"Classify this text","data":"...","schema":{"type":"object","properties":{"category":{"type":"string"}}}}'

# JSON mode (no schema, just force JSON)
curl -X POST http://localhost:9999/structured \
  -d '{"prompt":"Return a JSON object with name, age, city for a fictional person"}'

# List available schemas
curl http://localhost:9999/structured/schemas
```

**内置的数据结构：** `entities`、`summary`、`comparison`、`actions`、`classification`、`qa`

使用Gemini的原生格式`responsemime_type: application/json`和`responseSchema`来保证输出为JSON格式，并对输出内容进行模式验证。

## 多数投票机制（v1.3.7）
对于相同的问题，通过N个并行执行结果来选择最佳答案。在事实性或分析性任务中效果更佳。

```bash
# Judge strategy (LLM picks best — most reliable)
curl -X POST http://localhost:9999/vote \
  -d '{"prompt":"What are the key factors in SaaS pricing?","n":3,"strategy":"judge"}'

# Similarity strategy (consensus — zero extra cost)
curl -X POST http://localhost:9999/vote \
  -d '{"prompt":"What year was Python released?","n":3,"strategy":"similarity"}'

# Longest strategy (heuristic — zero extra cost)
curl -X POST http://localhost:9999/vote \
  -d '{"prompt":"Explain recursion","n":3,"strategy":"longest"}'
```

**策略选择：**
- `judge` —— 根据准确性、完整性、清晰度和可操作性对所有答案进行评分，选择最佳答案（调用N+1次API）
- `similarity` —— 基于Jaccard相似度选择共识答案（调用N次API，无额外费用）
- `longest` —— 选择最长的答案作为结果（调用N次API，无额外费用）

**适用场景：** 需要高准确性的问题、关键决策或任何注重准确性的任务。

| 策略 | 调用次数 | 额外成本 | 优点 |
|----------|-------|-----------|---------|
| similarity | N次 | 0 | 适合需要共识的场合 |
| longest | N次 | 0 | 适合需要快速结果的场合 |
| judge | N+1次 | 约0.0001美元 | 依赖LLM评分 |

## 自我评估（v1.3.5）
在链式执行或生成初步结果后，可进行自我评估。根据评估结果自动优化输出。

```bash
# Add reflect:true to any chain or skeleton request
curl -X POST http://localhost:9999/chain/auto \
  -d '{"task":"Analyze the AI chip market","data":"...","reflect":true}'

curl -X POST http://localhost:9999/skeleton \
  -d '{"task":"Write a market analysis","reflect":true}'
```

实践证明：使用该功能后，输出质量从5.0分提升到平均7.6分。初步结果+自我评估后的最终质量可达到9.4分。

## 思路框架生成（v1.3.6）
生成内容大纲 → 并行扩展每个部分 → 合并成连贯的文档。非常适合生成长篇内容。

```bash
curl -X POST http://localhost:9999/skeleton \
  -d '{"task":"Write a comprehensive guide to SaaS pricing","maxSections":6,"reflect":true}'
```

**性能对比：**
- **链式执行**：21秒内生成14,478个字符（675个字符/秒），吞吐量是链式执行的2.9倍。
- **思路框架生成**：21秒内生成14,478个字符，吞吐量是链式执行的5.1倍。

| 指标 | 链式执行 | 思路框架生成 | 最终结果 |
|--------|-------|---------------------|--------|
| 输出长度 | 2,856个字符 | 14,478个字符 | 思路框架生成（5.1倍） |
| 吞吐量 | 234个字符/秒 | 675个字符/秒 | 思路框架生成（2.9倍） |
| 执行时间 | 12秒 | 21秒 | 链式执行（更快） |
| 质量（含自我评估） | 7-8分（满分10分） | 9.4分（思路框架生成） |

**适用场景：**
- **思路框架生成**：适用于生成长篇内容、报告、指南、文档等需要自然分段的结构化内容
- **链式执行**：适用于分析、研究、需要多角度分析的任务
- **并行执行**：适用于独立任务和批量处理
- **结构化输出**：适用于提取实体信息、进行分类或需要可靠JSON格式的输出
- **多数投票**：适用于需要高准确性的问题、关键决策或需要达成共识的场景

## API接口

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | /health | 系统健康检查 |
| GET | /status | 详细状态信息、成本统计和缓存情况 |
| GET | /capabilities | 查看可用的执行模式 |
| POST | /parallel | 并行执行N个提示 |
| POST | /research | 多阶段网页搜索 |
| POST | /skeleton | 生成内容大纲 |
| POST | /chain | 手动构建链式执行流程 |
| POST | /chain/auto | 自动构建并执行链式流程 |
| POST | /chain/preview | 预览链式执行结果（不执行） |
| POST | /chain/template | 执行预定义的链式流程模板 |
| POST | /structured | 强制输出JSON格式并进行模式验证 |
| GET | /structured/schemas | 查看内置的数据结构 |
| POST | /vote | 使用多数投票机制选择最佳答案 |
| POST | /benchmark | 进行性能对比测试 |
| GET | /templates | 查看链式执行模板 |
| GET | /cache | 查看缓存统计信息 |
| DELETE | /cache | 清空缓存 |

## 成本对比

| 模型 | 每100万个令牌的成本 | 相对成本 |
|-------|-------------------|----------|
| Claude Opus 4 | 约15.00美元/100万个令牌 | 1倍 |
| GPT-4o | 约2.50美元/100万个令牌 | 约7倍 |
| Gemini Flash | 约0.075美元/100万个令牌 | **便宜200倍** |

缓存命中几乎无需成本（处理时间约3-5毫秒，无需调用API）。