---
name: cursor-cli
description: 使用 Ask Cursor CLI（Cursor 的终端代理）向它提问，它会返回相应的答案。该工具适用于获取编程帮助、代码审查或相关解释——OpenClaw 负责运行这个代理并为你提供响应。
metadata: {"openclaw":{"requires":{"bins":["agent"]},"emoji":"⌨️","homepage":"https://cursor.com/docs/cli/overview"}}
---
# Cursor CLI 技能

当用户希望从 **Cursor 的 AI**（Cursor CLI/代理）那里获得答案时，请按照以下流程操作：

1. **通过 `bash` 工具以非交互式方式运行 Cursor CLI**：
   - 使用 `agent` 命令，并设置相应的提示信息和文本输出格式。
   - 从用户的工作区或指定的项目目录（例如 `~/.openclaw/workspace` 或用户提供的路径）开始运行命令：
     ```bash
   agent -p "USER_QUESTION_HERE" --output-format text
   ```
   - 如果只是进行读取操作（无需修改代码），请使用 “Ask” 模式：
     ```bash
   agent -p "USER_QUESTION_HERE" --mode=ask --output-format text
   ```
   - 请将 `USER-question_HERE` 替换为用户的实际问题，并确保问题字符串在 shell 中能够正确解析（使用单引号包围提示信息；如果提示信息中包含单引号，请对其进行转义或使用 here-doc 语法）。

2. **捕获并返回输出结果**：代理会将答案输出到标准输出（stdout）中。将整个输出结果作为 OpenClaw 的回复返回给用户；只有在答案过长且用户明确要求摘要时才进行总结。

3. **工作目录**：如果用户指定了项目路径，请从该目录中运行 `agent` 命令（例如：`cd /path/to/project && agent -p "..." --output-format text`）。否则，使用 OpenClaw 的默认工作区或当前上下文。

4. **响应时间**：对于复杂的问题，Cursor CLI 可能需要 30–120 秒才能完成处理。请不要过早判断请求失败。

5. **使用场景**：当用户明确要求 “询问 Cursor”、“使用 Cursor CLI” 或希望获得来自 Cursor 代理的编程帮助/解释时，建议使用此技能。对于一般的聊天交流，请使用 OpenClaw 的常规模型。

## 示例

- 用户：“询问 Cursor CLI：如何解决 Git 中的合并冲突？”
  → 运行命令：`agent -p "how do I fix a merge conflict in git?" --mode=ask --output-format text`，并将输出结果返回给用户。

- 用户：“让 Cursor 代理解释编程中的递归概念”
  → 运行命令：`agent -p "explain what recursion is in programming" --mode=ask --output-format text`，并将输出结果返回给用户。

- 用户：“让 Cursor 检查 ~/myapp 项目中的代码是否存在安全问题”
  → 运行命令：`cd ~/myapp && agent -p "review the code in this project for security issues" --output-format text`，并将输出结果返回给用户。