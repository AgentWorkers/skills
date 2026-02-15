---
name: gemini
description: Gemini CLI：用于一次性问答、内容总结以及内容生成的工具。
homepage: https://ai.google.dev/
metadata: {"clawdbot":{"emoji":"♊️","requires":{"bins":["gemini"]},"install":[{"id":"brew","kind":"brew","formula":"gemini-cli","bins":["gemini"],"label":"Install Gemini CLI (brew)"}]}}
---

# Gemini CLI

您可以使用 Gemini 的一次性执行模式（即不进入交互式模式），并通过位置参数传递提示内容。

**快速入门：**
- `gemini "回答这个问题..."`
- `gemini --model <模型名称> "提示内容..."`
- `gemini --output-format json "以 JSON 格式返回结果"`

**扩展功能：**
- 列出所有可用扩展：`gemini --list-extensions`
- 管理扩展：`gemini extensions <命令>`

**注意事项：**
- 如果需要身份验证，请先以交互式模式运行一次 `gemini`，并按照提示完成登录流程。
- 为确保安全，请避免使用 `--yolo` 参数。