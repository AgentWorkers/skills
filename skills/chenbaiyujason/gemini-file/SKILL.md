---
name: gemini
description: Gemini CLI：用于一次性问答、内容总结以及数据生成的工具。
homepage: https://ai.google.dev/
metadata: {"clawdbot":{"emoji":"♊️","requires":{"bins":["gemini"]},"install":[{"id":"brew","kind":"brew","formula":"gemini-cli","bins":["gemini"],"label":"Install Gemini CLI (brew)"}]}}
---
# Gemini CLI

您可以使用 Gemini 的一次性模式（单次请求），并指定提示内容（避免使用交互式模式）。

**快速入门：**
- `gemini "回答这个问题..."`
- `gemini --model <model_name> "提示内容..."`
- `gemini --output-format json "以 JSON 格式返回结果"`

**文件输出模式（适用于大量数据或明确要求文件输出的情况）：**
- 当内容量较大（例如长篇文章/故事/报告）**或**用户明确要求以文件形式获取结果时，请使用以下命令：
  - `python3 /Users/shichen/skills/gemini/gemini_file_runner.py --prompt "<提示内容>"`
- 默认模型：`gemini-3-flash-preview`
- 对于需要解析大量内容的视频（如长视频、密集的字幕或多个片段），建议优先使用 `gemini-3-flash-preview` 模型。
- **脚本行为：**
  - 始终将 Gemini 的输出结果保存到 `outputs/` 目录下。
  - 以 JSON 格式返回文件的绝对路径（`file_path`）。
  - 如果提供了 `--include-content` 参数，也会返回内容本身。
- **可选参数：**
  - `--model <model_name>`：指定使用的 Gemini 模型。
  - `--output-format text|json`：指定输出格式（文本或 JSON）。
  - `--output-file <filename>`：指定输出文件的名称。
  - `--output-dir <dir>`：指定输出文件的目录。
  - `--include-content`：是否包含输出内容。

**此模式所需的响应格式：**
- 响应数据中必须包含文件的绝对路径（以 JSON 格式）：`file_path`。
- 响应内容是可选的，由 `--include-content` 参数控制。

**示例：**
- **用户请求：** 使用 Gemini 模型编写一篇约 1000 字的小说并输出文件。
- **命令：**
  - `python3 /Users/shichen/skills/gemini/gemini_file_runner.py --prompt "写一篇约 1000 字中文小说，主题是..." --output-file novel-1000-words.txt`
- **预期的 JSON 输出结果：**
  - `{"ok": true, "file_path": "/Users/shichen/skills/gemini/outputs/novel-1000-words.txt"}`

**视频解析示例（处理大量数据）：**
- **用户请求：** 请解析这个长视频并输出解析结果。
- **命令：**
  - `python3 /Users/shichen/skills/gemini/gemini_file_runner.py --model gemini-3-flash-preview --prompt "解析视频内容并输出结构化总结..." --output-file video-analysis.txt`

**其他命令：**
- `gemini --list-extensions`：列出所有可用的 Gemini 扩展功能。
- `gemini extensions <command>`：管理 Gemini 的扩展程序。

**注意事项：**
- 如果需要身份验证，请先交互式地运行一次 `gemini` 并完成登录流程。
- 为安全起见，请避免使用 `--yolo` 参数。