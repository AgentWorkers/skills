---
name: openrouter-free-responder
description: 这是一个免费的 OpenRouter 回应器，能够自动发现当前最合适的免费模型；在遇到故障时能够重试，并快速返回准确的答案。当用户请求查询 OpenRouter、希望使用最低成本或免费的路由模型，或者明确要求获得免费模型的 OpenRouter 回应时，可以使用这个工具。
metadata: {"openclaw":{"emoji":"🆓","requires":{"bins":["python3"],"env":["OPENROUTER_API_KEY"]},"primaryEnv":"OPENROUTER_API_KEY","homepage":"https://openrouter.ai"}}
---
使用捆绑的脚本对免费的 OpenRouter 模型执行提示操作。

## 工作流程

1. 确保 `OPENROUTER_API_KEY` 已设置。
2. 运行以下命令：
   ```bash
   python3 {baseDir}/scripts/openrouter_free_chat.py --prompt "<user prompt>"
   ```
3. 如果用户提供了系统指导，请使用 `--system "..."` 选项。
4. 返回 `response` 文本，并说明使用了哪个模型。

## 命令选项

- `--prompt`（必选）：用户输入的提示文本。
- `--system`（可选）：系统指令。
- `--max-attempts`（可选，默认值为 `8`）：尝试的免费模型数量。
- `--temperature`（可选，默认值为 `0.3`）：采样温度。
- `--debug`（可选）：将模型排名信息及失败尝试记录到标准错误输出（stderr）。

## 输出格式

脚本会向标准输出（stdout）打印一个 JSON 对象，其中包含以下内容：

- `selected_model`：生成最终响应的模型。
- `response`：最终的辅助文本。
- `attempted_models`：尝试过的模型列表（按顺序排列）。
- `free_model_candidates`：发现的免费模型数量。

如果没有任何模型成功响应，脚本将以非零状态退出，并显示错误信息。