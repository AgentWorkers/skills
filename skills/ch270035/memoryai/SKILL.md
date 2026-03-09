---
name: memoryai
description: "通过 MemoryAI 服务器实现持久化的长期记忆功能。能够在不同会话之间存储、检索和管理上下文信息。"
metadata: {"openclaw": {"always": true, "emoji": "🧠"}}
---
# MemoryAI

这是一个专为AI代理设计的云内存系统，基于服务器端的PostgreSQL、pgvector和Neural Graph技术构建。该系统完全不依赖任何第三方库，仅使用Python的标准库（包括urllib）。

## 设置

1. 从MemoryAI服务器获取API密钥。
2. 修改`{baseDir}/config.json`文件中的配置：

```json
{
  "endpoint": "https://your-memoryai-server.com",
  "api_key": "hm_sk_your_key_here"
}
```

## 命令

### 存储内存
```bash
python {baseDir}/scripts/client.py store -c "data to remember" -t "tag1,tag2" -p hot
```
优先级：`hot`（重要、需频繁检索）| `warm`（默认）| `cold`（归档）

可选参数：
- `--memory-type <类型>` — 对内存进行分类：`fact`（事实信息）、`decision`（技术/架构决策）、`preference`（用户偏好）、`error`（错误信息）、`goal`（目标）、`episodic`（事件/对话记录）

示例：
```bash
# Store a decision that should never be deleted
python {baseDir}/scripts/client.py store -c "Use PostgreSQL for all new services" -t "architecture" -p hot --memory-type decision --retention forever

# Store a preference with 1-year retention
python {baseDir}/scripts/client.py store -c "User prefers dark mode" -t "preferences" --memory-type preference --retention 1y

# Store an error lesson (auto decay)
python {baseDir}/scripts/client.py store -c "Never use rm -rf on mounted volumes" -t "errors" -p hot --memory-type error
```

### 检索内存
```bash
python {baseDir}/scripts/client.py recall -q "what was discussed?" -d deep
```
检索深度：`fast`（快速查找）| `deep`（基于语义和神经图的深度检索）| `exhaustive`（全面扫描）

可选参数：`--memory-type <类型>` — 按内存类型过滤检索结果。

```bash
# Recall only decisions
python {baseDir}/scripts/client.py recall -q "database choices" --memory-type decision

# Recall only preferences
python {baseDir}/scripts/client.py recall -q "user settings" --memory-type preference
```

### 统计分析
```bash
python {baseDir}/scripts/client.py stats
```

### 压缩内存（将数据压缩以节省空间）
```bash
python {baseDir}/scripts/client.py compact -c "session transcript or context" -t "task description"
```

### 恢复内存内容
```bash
python {baseDir}/scripts/client.py restore -t "what I was working on"
```

### 检查内存健康状况
```bash
python {baseDir}/scripts/client.py check
```
返回内存的健康状态：`low`（正常）| `medium`（一般）| `high`（警告）| `critical`（严重）

### 自我反思
```bash
python {baseDir}/scripts/client.py reflect --hours 24 --max-insights 5
```
系统会自动扫描最近的内存数据，识别重复出现的模式（如标签、内存类型等），并生成相应的分析报告。

## QF特性（v0.5.0）

### 内存类型
对内存进行分类，以便更好地管理和检索：
| 类型 | 用途 |
|------|---------|
| `fact` | 客观事实信息、数据点 |
| `decision` | 技术/架构决策 |
| `preference` | 用户偏好设置 |
| `error` | 错误信息、经验教训 |
| `goal` | 目标或任务 |
| `episodic` | 事件记录、对话内容 |

所有类型均为可选，可根据实际需求选择是否使用。

### 保留策略
控制内存的保留时长：
| 策略 | 行为 |
|--------|----------|
| `forever` | 内存永远不会被删除或失效。 |
| `6m` | 6个月后自动删除 |
| `1y` | 1年后自动删除 |
| `auto` | 遵循艾宾浩斯遗忘曲线（默认设置） |

对于关键决策、API密钥或架构配置等重要数据，建议使用`forever`策略；对于日常使用的信息，使用`auto`策略。

### 冲突检测
在存储新内存时，系统会自动检查其与现有内存是否存在冲突。如果发现冲突，响应中会包含以下信息：
- `contradiction_warning`：冲突的描述
- `contradicts`：冲突的内存块ID列表

用户无需采取任何操作，只需注意系统可能标记的冲突信息即可。

### 活性传播
在检索内存时，系统会优先考虑相关内存块之间的关联关系。通过共享标签或实体连接的内存块会通过神经图相互关联。系统采用广度优先搜索（BFS）算法来查找相关内容，从而提高检索效率。

### 赫布学习（Hebbian Learning）
随着使用次数的增加，内存块之间的连接会逐渐增强。每次共同检索时，相关块的连接权重会增加0.1（最大增加5.0）。这种机制使用户在使用过程中能更自然地记住信息。

### 内存衰减与整合
系统采用艾宾浩斯遗忘曲线模型进行自动生命周期管理：
- 仅影响`retention=auto`设置的内存块
- `forever`、`6m`、`1y`设置的内存块永远不会被删除
- 未使用的内存会逐渐被遗忘
- 被检索到的内存会得到强化（遵循赫布学习原理）

### 自我反思功能
系统会从最近的内存数据中生成分析报告：
```bash
python {baseDir}/scripts/client.py reflect --hours 24 --max-insights 5
```
- 扫描过去N小时内的内存数据
- 识别重复出现的标签、内存类型和内容类型
- 生成标记为`[insight, auto-reflection]`的分析报告
- 适用于定期自我回顾或任务检查

## 自动内存管理机制（自动配置）

首次使用时，系统会创建一个定时任务（cron job），在需要时自动监控和压缩内存：
- 任务名称：`context-guard`
- 安排频率：每20分钟执行一次（`everyMs: 1200000`）
- 会话隔离：确保任务在独立环境中运行
- 通知方式：不向用户发送任何通知
- 任务内容：更新内存状态

## 使用场景

| 触发条件 | 执行操作 | 优先级 | 关键标签 | 内存类型 | 保留策略 |
|---------|--------|----------|------|-------------|-----------|
| 任务完成 | 存储结果 | hot | projects | fact | auto |
| 用户请求“记住这个内容” | 存储相关数据 | hot | people | — | forever |
| 研究/搜索完成 | 存储研究结果 | warm | research | fact | auto |
| 技术决策 | 存储决策内容 | hot | decisions | decision | forever |
| 发现错误/经验教训 | 存储错误信息 | hot | errors | error | forever |
| 用户修改偏好设置 | 存储偏好设置 | warm | preferences | preference | 1y |
| 设定新目标 | 存储目标信息 | hot | goals | goal | 1y |
| 需要回顾过去的信息 | 先检索相关内容 | — | — | — | — |
| 会话结束 | 压缩内存 | — | — | — | — |
| 会话开始 | 恢复会话内容 | — | — | — | — |
| 定期回顾 | 生成分析报告 | — | — | — | — |

## 规则

- 在回答关于过去工作的问题时，必须先检索相关内存。
- 完成任务后，需将重要结果存储到内存中。
- 避免向用户展示内存系统的内部机制。
- 以自然的方式呈现检索到的信息，让用户感觉就像自己“凭记忆”回答一样。
- 内存压缩任务在后台自动执行，不会通知用户。
- 当内存类型明确时，请使用`--memory-type`参数；若类型不明确，则省略该参数。
- 对于关键决策和用户明确指定的偏好设置，建议使用`--retention forever`策略。
- 即使存储响应中包含冲突警告，也不应阻止数据的存储。

## 数据与隐私
该技能通过HTTPS将存储的内存数据发送到配置的MemoryAI服务器。所有数据均通过加密连接传输，并存储在独立的私有数据库中。
用户可以通过`/v1/export`命令导出所有数据，或通过`DELETE /v1/data`命令随时删除数据。