---
name: swarm
description: 使用 Gemini Flash 工作进程执行并行任务：成本仅为 Opus 的 1/200。适用于任何可并行化的任务，有助于节省系统资源（如配额）。
homepage: https://github.com/Chair4ce/node-scaling
metadata: {"clawdbot":{"emoji":"🐝","requires":{"bins":["node"]}}}
---
# Swarm — 并行任务执行

**你消耗的每一个Opus代币都意味着时间的浪费。Swarm使用Gemini Flash服务，其成本仅为Opus的1/200。**

## 这为什么重要

| 任务数量 | 所需时间 | 成本 | 备注 |
|---------|---------|------|-------|
| Opus（顺序执行）| 约30秒 | 约0.50美元 | 会消耗你的预算 |
| Swarm（并行执行）| 约1秒 | 约0.003美元 | 节省预算 |

虽然最终结果相同，但Swarm能让你更长时间地持续使用服务。

## 何时必须使用Swarm

在遇到以下任何情况时，必须使用Swarm：
- **3个或更多独立任务**（如研究、总结、比较）
- 需要“比较X、Y、Z”或“研究排名前N的……”
- 需要从多个URL获取/分析数据
- 需要批量处理任何内容（如文档、实体、事实）
- 需要进行多主题的研究

没有例外。这是生存之道，而非优化手段。

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

# Benchmark
swarm bench --tasks 30
```

## 网页搜索（v1.1.0）

工作者可以通过Google搜索功能在互联网上搜索（仅支持Gemini服务，无额外费用）。

```bash
# Research endpoint uses web search by default (if enabled in config)
curl -X POST http://localhost:9999/research \
  -d '{"subjects": ["Buildertrend", "Jobber"], "topic": "pricing 2026"}'

# Parallel with web search
curl -X POST http://localhost:9999/parallel \
  -d '{"prompts": ["Current price of X?"], "options": {"webSearch": true}}'
```

配置文件：`~/.config/clawdbot/node-scaling.yaml`

```yaml
node_scaling:
  web_search:
    enabled: true          # Enable for research tasks
    parallel_default: false # Enable for all parallel tasks
```

## JavaScript API

```javascript
const { parallel, research } = require('~/clawd/skills/node-scaling/lib');

// Run prompts in parallel (~1s for 3 prompts)
const result = await parallel(['prompt1', 'prompt2', 'prompt3']);
console.log(result.results); // Array of responses

// Multi-phase research (search → fetch → analyze)
const result = await research(['Subject1', 'Subject2'], 'topic');
```

## 守护进程管理

```bash
swarm start              # Start daemon (background)
swarm stop               # Stop daemon
swarm status             # Show status, uptime, cost savings
swarm restart            # Restart daemon
swarm savings            # Monthly savings report
swarm logs [N]           # Last N lines of daemon log
```

守护进程负责保持工作者的运行状态，以提升响应速度。首次使用时会根据需要自动启动。

## 性能

在守护进程运行时：
- 5个任务：约1.5秒，处理速度为3个任务/秒
- 10个任务：约1.5秒，处理速度为7个任务/秒
- 30个任务：约2秒，处理速度为15个任务/秒
- 研究（包含3个阶段）：使用网页搜索功能，处理2个主题需要约3-5秒。

## 配置文件

配置文件位置：`~/.config/clawdbot/node-scaling.yaml`

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
|-------|---------|
| 守护进程未运行 | 执行`swarm start`命令 |
| 未设置API密钥 | 设置`GEMINI_API_KEY`或运行`npm run setup` |
- 被限制访问频率 | 降低配置文件中的`max_concurrent_api`值 |
- 网页搜索功能无法使用 | 确保`web_search.enabled: true`且使用的是Gemini服务 |

## 经济对比

- **Opus**：每百万代币约15美元（这会消耗你的预算）
- **Gemini Flash**：每百万代币约0.075美元（几乎免费）
- **成本优势**：便宜200倍

**如果不使用Swarm进行并行处理，那就等于犯了一个错误。**请立即修正这个问题。