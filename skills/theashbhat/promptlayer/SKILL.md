---
name: promptlayer
description: 通过 PromptLayer API 来管理提示信息、记录大型语言模型（LLM）的请求、执行评估以及跟踪评估结果。该 API 非常适用于处理提示信息的版本控制、A/B 测试、LLM 的可观测性/日志记录、提示信息评估流程、数据集，以及 PromptLayer 的代理/工作流等场景。
---
# PromptLayer

通过 PromptLayer 的 REST API 进行提示管理、日志记录、评估以及可观测性操作。

## 设置

设置环境变量 `PROMPTLAYER_API_KEY`。运行 `scripts/setup.sh` 进行配置，或者将其添加到 `~/.openclaw/.env` 文件中。

## 命令行接口（CLI）——`scripts/pl.sh`

```bash
# Prompt Templates
pl.sh templates list [--name <filter>] [--label <label>]
pl.sh templates get <name|id> [--label prod] [--version 3]
pl.sh templates publish              # JSON on stdin
pl.sh templates labels               # List release labels

# Log an LLM request (JSON on stdin)
echo '{"provider":"openai","model":"gpt-4o",...}' | pl.sh log

# Tracking
pl.sh track-prompt <req_id> <prompt_name> [--version 1] [--vars '{}']
pl.sh track-score <req_id> <score_0_100> [--name accuracy]
pl.sh track-metadata <req_id> --json '{"user_id":"abc"}'
pl.sh track-group <req_id> <group_id>

# Datasets & Evaluations
pl.sh datasets list [--name <filter>]
pl.sh evals list [--name <filter>]
pl.sh evals run <eval_id>
pl.sh evals get <eval_id>

# Agents
pl.sh agents list
pl.sh agents run <agent_id> --input '{"key":"val"}'
```

## API 路径组

- `/prompt-templates` — 提示模板（列表、获取）
- `/rest/` — 跟踪、日志记录、发布
- `/api/public/v2/` — 数据集、评估结果

完整参考文档：`references/api.md`