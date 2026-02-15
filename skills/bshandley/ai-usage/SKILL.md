---
name: ai-usage
description: >
  检查 Anthropic 以及其他供应商提供的 AI 服务的使用情况。  
  适用场景：  
  1. 当用户询问 AI 服务的使用情况、令牌消耗量或使用配额时。  
  2. 当用户提问“我的 AI 使用量是多少？”或“我使用了多少资源？”时。  
  3. 当用户想了解 Anthropic/Claude 服务的使用限制或功能时。  
  4. 当用户询问 AI 服务的费用或支出情况时。  
  5. 在定期（每日）检查服务使用情况时。
---
# 人工智能使用情况检查

## 快速入门

```bash
python3 scripts/usage_check.py           # Pretty report with gauges
python3 scripts/usage_check.py --json    # JSON output for scripting
```

## 系统要求

- **Python 3.10 或更高版本**（无需安装 `pip`，仅使用 Python 标准库）
- 已安装并配置了 **Claude Code**（`claude` 命令行工具需添加到系统路径中），用于获取 Anthropic 的使用配额信息
- 已安装 **OpenClaw**，用于获取会话日志、令牌统计和费用信息

## 功能展示

**Anthropic（通过 OAuth API 获取的实时配额信息）：**
- 每周使用率及配额重置倒计时
- 5 小时滚动窗口内的使用率
- 若支持，可查看特定模型（如 Sonnet、Opus）的每周使用情况
- 实际使用量与每月限额的对比

**其他提供者的使用情况（通过 OpenClaw 会话日志获取）：**
- 每个模型的令牌使用次数和调用次数
- 自动识别通过 OpenClaw 调用的所有服务（如 Ollama、OpenAI 等）

**OpenClaw 与 Anthropic 的详细信息：**
- 每个模型的令牌使用次数及对应的 API 费用

## 工作原理

- **获取 Anthropic 配额：** 使用 `Claude Code` 从 `~/.claude/.credentials.json` 中获取 OAuth 令牌，然后通过 `GET https://api.anthropic.com/api/oauth/usage` 请求获取配额信息（需要 `user:profile` 权限）
- **令牌自动更新：** 如果令牌过期，脚本会自动通过 `claude --print -p "ok"` 命令刷新令牌（`Claude Code` 会在每次调用时自动更新其 OAuth 令牌），之后重新读取配置文件。如果未安装 `Claude Code`，则跳过 Anthropic 配额信息的获取。
- **会话统计：** 从 `~/.openclaw/agents/main/sessions/*.jsonl` 文件中解析每个提供者/模型的令牌使用量和费用数据

## 环境变量

| 变量          | 默认值        | 说明                          |
|---------------|-------------|-----------------------------------------|
| `OPENCLAW_SESSIONS_DIR` | `~/.openclaw/agents/main/sessions` | OpenClaw 会话日志目录                      |
| `CLAUDE_CREDENTIALS_PATH` | `~/.claude/.credentials.json` | Claude Code 的认证文件                        |

## 使用建议

- 可通过 **Haiku** 或轻量级模型来定期执行该脚本以进行心跳检测或后台监控——脚本只需运行即可，无需额外处理逻辑
- 使用 `--json` 参数可将数据以 JSON 格式输出，便于程序化使用（如定时任务、仪表盘展示、警报系统等）
- 适用于所有 Anthropic 订阅套餐（Pro、Max、Team 等）