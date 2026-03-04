# MindClaw

MindClaw 是为 OpenClaw 代理设计的 **结构化长期知识存储层**。与 OpenClaw 将对话内容以 Markdown 格式存储在内存中不同，MindClaw 会存储经过整理的事实、决策以及相关数据，并附带完整的元信息（如冲突检测结果、重要性评分等），同时构建一个知识图谱。

这些存储的内容会同步回 OpenClaw 的 `MEMORY.md` 文件中，因此也可以通过 OpenClaw 的内置 `memory_search` 工具进行查询。

## 安装

```bash
pip install mindclaw[mcp] && mindclaw setup
```

`setup` 向导会一次性配置您的工作空间路径、代理名称，并将 MindClaw 注册到 Claude Desktop 或 OpenClaw 中。

## 代理功能

| 功能        | 用途                                      |
|------------|-----------------------------------------|
| `setup_mindclaw` | 一次性完成配置、注册及数据同步                    |
| `remember`    | 带有元信息的事实、决策或错误的存储                    |
| `recall`     | 基于 BM25 算法结合语义搜索的功能，支持时间衰减和 MMR 多样性        |
| `context_block` | 可插入到 LLM 提示中的结构化记忆块                    |
| `capture`     | 从对话文本中自动提取结构化记忆                    |
| `confirm`     | 强化被证明正确的记忆（提升其重要性）                    |
| `forget`     | 归档或彻底删除记忆                        |
| `pin_memory`    | 将记忆标记为永久性存储（不受时间影响）                    |
| `timeline`     | 重建过去 N 小时内的事件流程                    |
| `consolidate`   | 自动合并重复的记忆                        |
| `link`       | 在知识图谱中连接两个记忆                        |
| `stats`      | 检查存储系统的健康状况及记忆分布                    |
| `sync_openclaw`    | 将所有记忆导出到 OpenClaw 的 MEMORY.md 文件中            |
| `import_markdown` | 从 OpenClaw 的 MEMORY.md 文件或每日日志中导入数据           |
| `unpin_memory`    | 取消对记忆的永久标记                        |

## 与 OpenClaw 的集成

MindClaw 完全复制了 OpenClaw 的搜索流程：

| OpenClaw 功能      | MindClaw 功能                                      |
|--------------|-----------------------------------------|
| BM25 关键词搜索    | ✓                                           |
| 语义嵌入        | 使用本地 GGUF、OpenAI 或 Gemini 的模型（自动检测）                |
| 时间衰减        | `--temporalDecay`                                     |
| MMR 多样性      | `--mmr`                                        |
| 代理隔离        | 使用 `--agent <name>` 参数进行代理级隔离                   |

完成 `mindclaw sync` 后，所有结构化记忆都会显示在 OpenClaw 的 `MEMORY.md` 文件中，并可通过 OpenClaw 的内置 `memory_search` 功能进行查询——无需修改任何代理代码。

## 推荐的代理使用流程

```python
1. `context_block(query)`   → 在回答前插入相关上下文
2. `remember(content)`      → 执行操作后存储关键事实和决策
3. `capture(conversation)`  → 从会话日志中提取结构化记忆
4. `confirm(id)`            → 强化被证明正确的记忆
5. `sync_openclaw()`        → 将数据推送到 OpenClaw 的 MEMORY.md 文件中
6. `consolidate()`          | 定期删除重复的记忆
```

## 配置

只需运行一次 `mindclaw setup`，之后无需重复配置：

该命令会生成 `~/.mindclaw/config.json` 文件，其中包含您的工作空间路径、代理名称和数据库路径。

配置优先级顺序：`CLI 参数 > MINDCLAW_开头的环境变量 > 配置文件 > 内置默认值`

## 系统要求

- Python 3.10 及以上版本
- 无强制依赖项（核心功能仅依赖标准库）
- 可选：安装 `pip install mindclaw[mcp` 以使用 MCP 服务器
- 可选：在本地运行 Ollama 以支持语义搜索（系统会自动检测）

## 源代码

GitHub：https://github.com/Blue8x/MindClaw