---
name: swarm
description: 将您的大型语言模型（LLM）的成本降低200倍。将并行处理、批量处理以及研究工作交给 Gemini Flash 工作节点来处理，而不是继续使用昂贵的主要模型。
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
- **需要多角度分析的复杂任务** → 使用“链式执行”模式

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

### 链式执行（v1.3）——优化流程
数据经过多个阶段处理，每个阶段都有不同的处理方式/过滤器。各阶段按顺序执行；同一阶段内的任务则并行处理。

**阶段模式：**
- `parallel` — N个输入 → N个工作者（相同处理方式）
- `single` — 合并后的输入 → 1个工作者处理
- `fan-out` — 1个输入 → N个工作者（不同处理方式）
- `reduce` — N个输入 → 1个综合输出

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
在同一任务上比较顺序执行、并行执行和链式执行的效果，由LLM作为评判标准。

```bash
curl -X POST http://localhost:9999/benchmark \
  -d '{"task":"Analyze X","data":"...","depth":"standard"}'
```

评估标准包括6个方面：准确性（权重2倍）、深度（1.5倍）、完整性、连贯性、可操作性（1.5倍）、细微差别。

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
- 可通过`task.cache = false`设置禁用缓存

```bash
# View cache stats
curl http://localhost:9999/cache

# Clear cache
curl -X DELETE http://localhost:9999/cache
```

缓存统计信息可在`swarm status`页面查看。

## 阶段重试（v1.3.2）
如果链式执行中的某个阶段失败，仅重试该阶段的任务，不会重新执行整个流程。默认重试次数为1次。可通过`phase.retries`配置每个阶段的重试次数，或通过`options.stageRetries`全局配置。

## 成本跟踪（v1.3.1）
所有端点在完成任务后都会返回成本数据：
- `session` — 当前守护进程会话的总成本
- `daily` — 数据在重启后持续累积

```bash
swarm status        # Shows session + daily cost
swarm savings       # Monthly savings report
```

## 网页搜索（v1.1）
工作者通过Google搜索功能从网页中获取信息（仅限Gemini版本，无额外费用）。

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
| 并行执行（简单模式） | 5个任务 | 约700毫秒 | 每个任务实际处理时间约142毫秒 |
| 并行执行（高负载模式） | 10个任务 | 约1.2秒 | 每个任务实际处理时间约123毫秒 |
| 链式执行（标准模式） | 5个任务 | 约14秒 | 多阶段、多角度处理 |
| 链式执行（快速模式） | 2个任务 | 约3秒 | 两阶段处理（提取+合成） |
| 缓存命中 | 任意数量的任务 | 约3-5毫秒 | 处理速度提升200-500倍 |
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

| 问题 | 解决方法 |
|-------|-----|
| 守护进程未运行 | 运行`swarm start`命令 |
| 未设置API密钥 | 设置`GEMINI_API_KEY`或运行`npm run setup` |
| 被限制访问频率 | 降低配置文件中的`max_concurrent_api`值 |
| 网页搜索功能失效 | 确保使用Gemini服务并启用`web_search.enabled`选项 |
| 缓存中的结果过时 | 执行`curl -X DELETE http://localhost:9999/cache`清除缓存 |
| 链式执行速度过慢 | 使用`depth: "quick"`设置或检查上下文数据量 |

## 结构化输出（v1.3.7）
强制输出JSON格式，并进行模式验证——确保结构化任务的处理无误。

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

利用Gemini的`responsemime_type: application/json`和`responseSchema`确保输出为JSON格式，并对输出内容进行模式验证。

## 多数投票机制（v1.3.7）
对于相同的问题，通过N个并行执行结果进行投票，选择最佳答案。在事实性或分析性任务中效果更佳。

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
- `judge` — 根据准确性、完整性、连贯性和可操作性对所有答案进行评分，选出最佳答案（调用N+1次API）
- `similarity` — 通过Jaccard相似度算法选择共识答案（调用N次API，无额外费用）
- `longest` — 选择最长的回答作为最佳答案（调用N次API，无额外费用）

**适用场景：** 需要高准确性的问题、关键决策或对速度要求不高的任务

| 策略 | 调用次数 | 额外成本 | 质量 |
|----------|-------|-----------|---------|
| similarity | N次 | 0美元 | 效果较好（基于共识） |
| longest | N次 | 0美元 | 基于长度的启发式选择 |
| judge | N+1次 | 约0.0001美元 | 基于LLM评分的结果 |

## 自我评估（v1.3.5）
在链式执行或生成初步结果后，可选择进行自我评估。评估五个维度，低于阈值时自动优化结果。

```bash
# Add reflect:true to any chain or skeleton request
curl -X POST http://localhost:9999/chain/auto \
  -d '{"task":"Analyze the AI chip market","data":"...","reflect":true}'

curl -X POST http://localhost:9999/skeleton \
  -d '{"task":"Write a market analysis","reflect":true}'
```

实际测试显示：使用该功能后，输出质量从5.0分提升到7.6分。结合初步结果和自我评估后，整体质量达到9.4分。

## 思路框架生成（v1.3.6）
生成内容框架后，再并行处理每个部分，最终合并成连贯的文档。非常适合生成长篇内容。

```bash
curl -X POST http://localhost:9999/skeleton \
  -d '{"task":"Write a comprehensive guide to SaaS pricing","maxSections":6,"reflect":true}'
```

**性能测试：**
生成21,478个字符仅需21秒（处理速度为675个字符/秒），比链式执行快2.9倍。
| 指标 | 链式执行 | 思路框架生成 | 最终结果 |
|--------|-------|---------------------|--------|
| 输出长度 | 2,856字符 | 14,478字符 | 思路框架生成（5.1倍） |
| 处理速度 | 234字符/秒 | 675字符/秒 | 思路框架生成（2.9倍） |
| 执行时间 | 12秒 | 21秒 | 链式执行（更快） |
| 质量（含自我评估） | 7-8分（满分10分） | 9.4分（思路框架生成） |

**适用场景：**
- **思路框架生成**：适用于生成长篇内容、报告、指南、文档等需要自然分段的结构化内容
- **链式执行**：适用于分析、研究、需要多角度评估的任务
- **并行执行**：适用于独立任务和批量处理
- **结构化输出**：适用于提取实体信息、进行分类或需要可靠JSON格式的结果
- **多数投票**：适用于需要高准确性的问题或需要达成共识的任务

## API接口

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | /health | 系统健康检查 |
| GET | /status | 详细状态信息、成本统计和缓存情况 |
| GET | /capabilities | 查看可用的执行模式 |
| POST | /parallel | 并行执行N个提示 |
| POST | /research | 多阶段网页搜索 |
| POST | /skeleton | 生成内容框架（生成→扩展→合并） |
| POST | /chain | 手动构建链式处理流程 |
| POST | /chain/auto | 自动构建并执行链式流程 |
| POST | /chain/preview | 预览链式处理结果（不执行） |
| POST | /chain/template | 执行预定义的链式处理模板 |
| POST | /structured | 强制输出JSON格式的数据，并进行模式验证 |
| GET | /structured/schemas | 查看内置的数据结构 |
| POST | /vote | 使用多数投票机制选择最佳答案 |
| POST | /benchmark | 进行性能测试 |
| GET | /templates | 查看链式处理模板 |
| GET | /cache | 查看缓存统计信息 |
| DELETE | /cache | 清除缓存 |

## 成本对比

| 模型 | 每100万个输入令牌的成本 | 相对成本 |
|-------|-------------------|----------|
| Claude Opus 4 | 约15美元（输入）/约75美元（输出） | 1倍 |
| GPT-4o | 约2.50美元（输入）/约10美元（输出） | 约7倍 |
| Gemini Flash | 约0.075美元（输入）/约0.30美元（输出） | **便宜200倍** |

缓存命中时的处理速度几乎为零（3-5毫秒，无需额外API调用）。