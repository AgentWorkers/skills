---
name: crabpath
description: 内存图引擎支持调用者提供的嵌入功能（embed）和大型语言模型（LLM）回调；其核心部分完全基于纯代码实现，具备实时纠错机制，并支持与 OpenAI 的集成（可选）。
metadata:
  openclaw:
    emoji: "🦀"
    requires:
      python: ">=3.10"
---
# CrabPath

这是一个纯图谱核心组件：无需依赖任何外部库，也不进行网络调用。调用者需要提供相应的回调函数。

## 设计原则

- 核心组件不进行任何网络调用。
- 不使用任何秘密发现机制（如 dotfiles、keychain 或环境变量探测）。
- 不提供子进程管理功能。
- 将嵌入器的身份信息存储在状态元数据中；如果状态数据中的维度不匹配，则视为错误。
- 使用统一的状态格式（`state.json`）。

## 快速入门

```python
from crabpath import split_workspace, HashEmbedder, VectorIndex

graph, texts = split_workspace("./workspace")
embedder = HashEmbedder()
index = VectorIndex()
for nid, content in texts.items():
    index.upsert(nid, embedder.embed(content))
```

## 嵌入与大型语言模型（LLM）回调

- 默认嵌入器：`HashEmbedder`（基于哈希算法，1024 维度）
- 实时嵌入：通过回调函数 `embed_fn` 或 `embed_batch_fn` 实现（例如：`text-embedding-3-small`）
- LLM 路由：通过回调函数 `llm_fn` 使用 `gpt-5-mini` 进行交互（示例）

## 会话回放

`replay_queries(graph, queries)` 可以根据历史交互记录快速启动新的会话。

## 命令行界面（CLI）

推荐使用以下命令：

```bash
crabpath query TEXT --state S [--top N] [--json]
crabpath query TEXT --state S --chat-id CID
crabpath doctor --state S
crabpath info --state S
crabpath init --workspace W --output O --embedder openai
crabpath query TEXT --state S --llm openai
crabpath inject --state S --type TEACHING [--type DIRECTIVE]
```

实时修正流程：

```bash
python3 query_brain.py --chat-id CHAT_ID
python3 learn_correction.py --chat-id CHAT_ID
```

## 快速参考

- 主要功能：`init`, `query`, `learn`, `inject`, `health`, `doctor`, `info`
- `query_brain.py` 和 `learn_correction.py` 用于实现实时修正功能
- `query_brain.py` 的配置参数：
  - `beam_width=8`, `max_hops=30`, `fire_threshold=0.01`
- 硬性限制参数：
  - `max_fired_nodes`（最大激活节点数，默认为 `None`）
  - `max_context_chars`（最大上下文长度，默认为 `20000`）
- 相关示例文件夹：`examples/correction_flow/`, `examples/cold_start/`, `examples/openai.embedder/`

## API 参考

- 核心组件接口：
  - `split_workspace`
  - `load_state`
  - `save_state`
  - `ManagedState`
  - `VectorIndex`
- 遍历与学习相关接口：
  - `traverse`
  - `TraversalConfig`（包含遍历配置）
  - `beam_width`, `max_hops`, `fire_threshold`, `max_fired_nodes`, `max_context_chars`, `reflex_threshold`, `habitual_range`, `inhibitory_threshold`
  - `TraversalResult`
  - `apply_outcome`
- 运行时注入接口：
  - `inject_node`
  - `inject_correction`
  - `inject_batch`
- 维护辅助接口：
  - `suggest_connections`, `apply_connections`
  - `suggest_merges`, `apply_merge`
  - `measure_health`, `autotune`, `replay_queries`
- 嵌入器相关接口：
  - `HashEmbedder`
  - `OpenAIEmbedder`
  - `default_embed`
  - `default_embed_batch`
  - `openai_llm_fn`
- LLM 路由回调：
  - `chat_completion`
- 图谱基本元素：
  - `Node`
  - `Edge`
  - `Graph`
  - `split_workspace`
  - `generate_summaries`

## 命令行参数说明

- `crabpath init --workspace W --output O --sessions S --embedder openai`：初始化 CrabPath 服务并指定工作空间和输出格式
- `crabpath query TEXT --state S --top N --json`：查询节点信息（可选显示前 N 条结果，支持 JSON 格式）
- `crabpath learn --state S --outcome N --fired-ids a,b,c --json`：根据节点 ID 和结果类型（CORRECTION/TEACHING/DIRECTIVE）进行学习
- `crabpath inject --state S --id NODE_ID --content TEXT --type CORRECTION|TEACHING|DIRECTIVE`：向图中注入节点信息
- `crabpath inject --state S --id NODE_ID --content TEXT --type TEACHING`：向图中注入节点信息（仅指定类型）
- `crabpath inject --state S --id NODE_ID --content TEXT --type DIRECTIVE`：向图中注入节点信息（仅指定类型）
- `crabpath health --state S`：检查系统健康状况
- `crabpath doctor --state S`：诊断系统问题
- `crabpath info --state S`：显示系统详细信息
- `crabpath replay --state S --sessions S`：回放指定会话的历史交互记录
- `crabpath merge --state S --llm openai`：使用 OpenAI LLM 合并图谱
- `crabpath connect --state S --llm openai`：连接图谱与 OpenAI LLM
- `crabpath journal --stats`：生成系统日志
- `query_brain.py --chat-id CHAT_ID`：查询指定节点的交互记录
- `learn_correction.py --chat-id CHAT_ID`：执行实时修正操作

## 遍历默认配置

- `beam_width=8`
- `max_hops=30`
- `fire_threshold=0.01`
- `reflex_threshold=0.6`
- `habitual_range=0.2-0.6`
- `inhibitory_threshold=-0.01`
- `max_fired_nodes`（最大激活节点数，默认为 `None`）
- `max_context_chars`（最大上下文长度，默认为 `20000`）

## 相关论文

https://jonathangu.com/crabpath/