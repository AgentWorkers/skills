---
name: openclaw-memories
description: 该代理具备ALMA元学习（meta-learning）能力，能够从大型语言模型（LLM）中提取相关信息，并支持全文搜索功能。观察者（observer）通过远程API（如OpenAI、Anthropic或Gemini）与这些大型语言模型进行交互。ALMA和索引器（Indexer）则可以离线运行。
---
# OpenClaw 内存系统

**代理内存的三个组成部分：**

1. **ALMA**：通过变异和评估（离线方式）来优化内存设计。
2. **Observer**：通过 LLM API 从对话中提取结构化信息（需要 API 密钥）。
3. **Indexer**：对工作区中的 Markdown 文件进行全文搜索（离线操作）。

## 环境变量

Observer 需要以下环境变量之一：
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- 或者在配置文件中指定 `apiKey`。

ALMA 和 Indexer 不需要任何密钥或网络访问权限。

## 工作原理

### ALMA（基于元学习的算法）

- 提出内存系统设计方案；
- 对这些方案进行评估，并保留最佳方案；
- 使用高斯变异和模拟退火算法来探索设计空间。

```
alma.propose() → design
alma.evaluate(design.id, metrics) → score  
alma.best() → top design
alma.top(5) → leaderboard
```

### Observer

- 将对话历史发送给 LLM，并获取结构化信息：
  - 信息类型：世界事实、人物传记、观点、观察结果；
  - 优先级：高/中/低；
  - 实体：被提及的人/地点；
  - 信心值：0.0–1.0（用于观点）；
- 如果 LLM 不可用，会优雅地返回空数组。

### Indexer

- 将工作区的 Markdown 文件分割成块并建立索引以便搜索：
  - `MEMORY.md`：核心信息；
  - `memory/YYYY-MM-DD.md`：每日日志；
  - `bank/entities/*.md`：实体摘要；
  - `bank/opinions.md`：带有信心值的观点。

```
indexer.index() → count of chunks indexed
indexer.search('query') → ranked results
indexer.rebuild() → re-index from scratch
```

## 安装方法

```bash
npm install @artale/openclaw-memory
```

## 限制

- Indexer 使用内存中的模拟数据库（而非真实的 SQLite FTS5），因此搜索功能可用，但排序机制较为简单；
- Observer 需要访问远程 API（非离线操作）；
- 为了简化设计，版本 2 中移除了控制面板。

## 源代码

项目包含 5 个文件，共 578 行代码，无运行时依赖项。

https://github.com/arosstale/openclaw-memory