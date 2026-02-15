---
name: ai-quota-check
description: "**默认配额检查器**：当用户输入“쿼타”（quota）、“쿼터확인”（quota confirmation）或询问有关配额的信息时，请优先使用此功能。该工具提供了一个统一的仪表板，可在一个界面中显示所有提供商（Antigravity、Copilot、Codex）的配额信息，并提供相应的模型建议。"
metadata: {"clawdbot":{"emoji":"🧮","requires":{"bins":["node","codex"]}}}
---

# ai-quota-check

这是一个统一的配额监控工具，同时具备智能模型推荐功能，适用于所有提供者（service providers）。

## 输出说明

**重要提示：** 在执行此功能时，必须以 markdown 格式 **原样** 显示脚本的输出结果，**禁止** 对输出内容进行总结或改写。脚本会生成一个格式化的仪表板，该仪表板应直接展示给用户。

示例执行方式：
```bash
node skills/ai-quota-check/index.js --current-model="<current_model_name>"
```

然后复制整个输出结果，并将其作为你的回复发送。

## 主要功能

1. **提供者登录检测** - 识别当前登录的提供者。
2. **统一配额仪表板** - 集合了 Antigravity、Copilot 和 OpenAI Codex 的配额信息。
3. **基于任务的模型推荐** - 根据任务需求选择最佳模型，并提供备用方案。
4. **模型状态检测** - 识别可用于任务的模型（新任务周期）。
5. **风险等级提示** - 警告用户关于每周使用配额上限及可能导致的账户锁定风险。

## 使用方法

```bash
# Full dashboard
node skills/ai-quota-check/index.js

# Specific task recommendation
node skills/ai-quota-check/index.js --task=coding
node skills/ai-quota-check/index.js --task=reasoning
```

## 模型路由规则

### 编码/调试（Coding/Debugging）
| 优先级 | 模型            | 备用条件                          |
|---------|-----------------------------|-----------------------------------|
| 1       | `openai-codex/gpt-5.3-codex`    | -                                   |
| 2       | `openai-codex/gpt-5.2-codex`    | 主模型使用率低于 20%                     |
| 3       | `google-antigravity/gemini-3-pro-high` | 所有其他模型的使用率均低于 20%                 |
|          |                                |                                      |
|          |                                |                                      |

### 复杂推理/分析（Complex Reasoning/Analysis）
| 优先级 | 模型            | 备用条件                          |
|---------|-----------------------------|-----------------------------------|
| 1       | `google-antigravity/claude-opus-4.6-thinking` | -                                   |
| 2       | `github-copilot/claude-4.6-opus`    | 主模型使用率低于 20%                     |
| 3       | `github-copilot/claude-3.5-opus`    | 当 `claude-opus-4.6` 不可用时                |
| 4       | `openai-codex/gpt-5.3`    | 所有其他模型的使用率均低于 20%                 |
| 5       | `openai-codex/gpt-5.2`    | 作为最后的备用模型                         |

## 备用模型切换阈值

默认值：**20%** - 当主模型使用率低于此阈值时，系统会自动切换到备用模型。

## Cron 集成

该功能可通过 Cron 任务定期执行，用于：
- 监控配额使用情况
- 检测模型是否可用于新任务
- 自动推荐合适的模型进行使用