---
name: trace-debuger
description: >
  **基于 `trace_id` 的端到端追踪调试功能：**  
  该功能允许您通过 `trace_id` 获取 Jaeger 的追踪数据以及 Elasticsearch 的日志记录，分析潜在的错误（可选地结合本地代码库的上下文信息），并生成结构规范的 Markdown 报告，以便用于持续集成（CI）或问题报告（tickets）流程。
---
# 跟踪调试器

使用此技能生成一个自包含的 Markdown 跟踪调试报告。

## 输入参数

- `trace_id`（必填）
- `jaeger_url`（可选，默认值：`http://127.0.0.1:16686`）
- `es_url`（可选，默认值：`http://127.0.0.1:9200`）
- `repo_path`（可选，绝对路径，默认值：`/Users/noodles/Desktop/code/go-components/examples/tracer`）
- `output_path`（可选，默认值：`./trace_debug_report_{trace_id}.md`）
- `es_index`（可选，默认值：`filebeat-tracer-*`）
- `es_size`（可选，默认值：`2000`）

## 运行方式

```bash
python3 skills/trace_debuger/scripts/trace_debuger.py \
  --trace-id <TRACE_ID> \
  [--jaeger-url http://127.0.0.1:16686] \
  [--es-url http://127.0.0.1:9200] \
  [--repo-path /Users/noodles/Desktop/code/go-components/examples/tracer] \
  [--output-path ./trace_debug_report_<TRACE_ID>.md]
```

## 输出结果

- 将生成的 Markdown 报告写入 `output_path` 文件中。
- **必须在完成任务之前，通过同一会话的聊天窗口将生成的 Markdown 报告作为文件附件发送给用户。**
- **必须将报告作为一条聊天消息发送：在消息的标题/正文中附加 Markdown 文件，并包含简明的总结内容。**
- **“【markdown报告文件】”是一个占位符，必须替换为实际的上传文件名（例如：`trace_debug_report_<trace_id>.md`）。**
- **标题/正文必须使用以下格式：**

```text
<真实markdown报告文件名>
trace_id: xxxx
status: xxx
jaeger_url: xxx
es_url: xxx
代码仓库路径：仓库路径
关键结论摘要：xxxx
```

- 将固定的总结内容打印到标准输出（stdout）：

```text
trace_id: <trace_id>
status: SUCCESS/FAIL
jaeger_url: <jaeger_url>
es_url: <es_url>
代码仓库路径：<repo_path|N/A>
关键结论摘要：<summary>
```

## 注意事项

- 保持日志按时间戳升序排列。
- 获取 ES 日志后，在仓库根目录下运行 Codex（通过 `codex exec` 自动执行，相当于 TUI 的粘贴工作流程），并输入以下提示：
  - “这是我的日志，请根据日志和代码帮我排查分析 bug，并输出 bug 的原因及解决方案，必须保持固定的格式。”
- 如果提供了仓库路径，应包含代码上下文提示以及疑似 bug 的文件位置信息。
- 如果未提供仓库路径，则仅根据日志和 Span 信息来推测 bug 的原因。
- 在聊天工作流程中完成分析后，通过聊天窗口将生成的 Markdown 报告作为文件附件发送给用户，同时在消息的标题/正文中包含简明的总结内容（仅发送一条消息）。
- 第一行必须是实际的 Markdown 文件名（不能是占位符文本）。
- 最后，删除本地的 Markdown 文件。