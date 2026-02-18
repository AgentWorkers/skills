---
name: context-viz
description: 可视化当前上下文窗口的使用情况——显示每个组件（系统提示、工具、工作区文件、消息、可用空间）所占用的令牌数量。当用户询问上下文窗口的大小、令牌的使用情况、上下文的详细构成，或者想知道是什么占用了他们的上下文窗口时，可以使用此功能。
---
# 上下文可视化

用于估算并显示当前上下文窗口的使用情况。

## 工作原理

运行捆绑的脚本以估算工作区文件中的令牌数量：

```bash
python3 scripts/estimate_tokens.py /path/to/workspace
```

该脚本会统计已知工作区文件中的字符数量，并估算每个令牌的平均长度（约为4个字符/令牌）。

然后调用 `session_status` 从 OpenClaw 获取实际的上下文使用情况。

## 生成可视化结果

1. 运行 `session_status` 以获取以下信息：模型、使用的上下文总量、压缩情况。
2. 运行 `scripts/estimate_tokens.py <workspace_path>` 以估算文件的令牌大小。
3. 计算消息令牌的数量：`context_used - system_overhead - file_tokens`。
4. 使用以下格式展示统计结果。

## 输出格式

使用等宽字体和条形图来呈现数据。条形图的长度应与数据量成比例。

```
📊 Context Usage
<model> • <used>k/<total>k tokens (<pct>%)

Component                    Tokens    %     
─────────────────────────────────────────────
⚙️  System prompt + tools    ~Xk      X%    ░░
📋  AGENTS.md                ~Xk      X%    ░
👻  SOUL.md                  ~Xk      X%    
👤  USER.md                  ~Xk      X%    
🔧  TOOLS.md                 ~Xk      X%    ░
💓  HEARTBEAT.md             ~Xk      X%    
🧠  MEMORY.md                ~Xk      X%    ░
🪪  IDENTITY.md              ~Xk      X%    
💬  Messages                 ~Xk      X%    ░░░░░░░░░░░░
📭  Free space               ~Xk      X%    ░░░░░
─────────────────────────────────────────────
```

使用 `░` 块来表示数据：每约2%的总上下文使用量使用一个 `░` 块。结果四舍五入到最接近的 `░` 块。

## 内存统计（不在上下文范围内）

在上下文图表下方，添加一个 **磁盘内存** 部分，显示存储在 `memory/` 目录中的文件内容——按类别进行分组。这些文件不会被加载到上下文中，但代表了代理的总知识库。

```
💾 Memory on Disk (not in context)
Category                     Files  Tokens   Size
──────────────────────────────────────────────────
📰  chinese-ai-digests        12    ~23k     92KB
📁  other                     11    ~12k     46KB
📅  daily-notes                9    ~5k      17KB
🗃️  zettelkasten               8    ~4k      15KB
💼  linkedin                   2    ~1k       5KB
──────────────────────────────────────────────────
     Total:                   42    ~44k    177KB
```

脚本会自动根据文件目录或文件名模式对文件进行分类。

## 注意事项

- 令牌数量的估算基于每个令牌约4个字符的平均长度（适用于英文或混合内容的文件）。
- 对于典型的 OpenClaw 配置，系统提示和工具的开销大约为8,000到10,000个令牌。
- 消息令牌的数量是减去文件数量和系统开销后的剩余部分。
- 内存文件仅用于提供信息——它们显示了代理所积累的数据。
- 对于 Discord/WhatsApp 等平台，跳过Markdown表格，直接使用上述的块格式进行展示。