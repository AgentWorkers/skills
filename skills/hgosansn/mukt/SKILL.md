---
name: openrouter-free-responder
description: 这是一个免费的 OpenRouter 响应器，能够自动检测当前最合适的免费模型，在遇到故障时进行重试，并快速返回准确的响应结果。当用户请求查询 OpenRouter、希望使用最低成本的免费模型进行路由，或者明确要求获得免费模型的 OpenRouter 响应时，可以使用该工具。
metadata: {"openclaw":{"emoji":"🆓","requires":{"bins":["python3"],"env":["OPENROUTER_API_KEY"]},"primaryEnv":"OPENROUTER_API_KEY","homepage":"https://openrouter.ai"}}
---
## Mukt 的用途是什么？

在解决问题时，你有两个选择：自己处理问题，或者将问题委托给他人。Mukt 为你提供了第三种选择——可以免费将问题交给外部模型来处理。

可以把 Mukt 想象成一个由实习生组成的团队。他们可以承担一些辅助任务、起草内容、探索想法，或者处理那些不需要你使用所有工具就能完成的任务。虽然他们的能力有限，但不如你的主要助手强大，而且他们无法访问你的内部工具或敏感信息。

**在以下情况下使用 Mukt：**
- 任务不紧急，且不涉及敏感信息。
- 你需要第二种意见或一个初步的解决方案，同时不想消耗过多的计算资源。
- 问题可以通过语言本身来解决，无需使用任何工具。

**不要在以下情况下使用 Mukt：**
- 任务涉及机密信息、凭证或私人数据。
- 任何需要直接访问你的工作空间或系统的情况。

## 工作流程

1. 确保 `OPENROUTER_API_KEY` 已设置。
2. 运行以下命令：
   ```bash
   python3 {baseDir}/scripts/openrouter_free_chat.py --prompt "<user prompt>"
   ```
3. 如果用户提供了系统指导，请加上 `--system "..."` 参数。
4. 返回 `response` 文本，并说明使用了哪个模型。

## 命令选项

- `--prompt`（必选）：用户提示文本。
- `--system`（可选）：系统指令。
- `--max-attempts`（可选，默认值：8）：尝试使用的可用模型的数量。
- `--temperature`（可选，默认值：0.3）：采样温度。
- `--debug`（可选）：将模型排名和备用尝试结果输出到标准错误流（stderr）。

## 输出格式

脚本会向标准输出（stdout）打印一个 JSON 对象，其中包含以下内容：
- `selected_model`：生成最终答案的模型。
- `response`：最终的助手提供的文本。
- `attempted_models`：尝试过的模型的列表（按顺序排列）。
- `free_model_candidates`：找到的可用模型的数量。

如果没有任何模型能够成功解决问题，脚本将以非零状态退出，并显示错误信息。