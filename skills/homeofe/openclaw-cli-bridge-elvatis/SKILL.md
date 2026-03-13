---
name: openclaw-cli-bridge-elvatis
description: 将本地的 AI CLI（如 Grok、Gemini、Claude.ai、ChatGPT）与网页浏览器会话（这些工具提供了模型交互功能）集成到 OpenClaw 中，作为模型提供者。系统支持通过 `/cli-*` 命令实现即时模型切换，并为这四个网页工具维护持久的浏览器会话信息。
homepage: https://github.com/elvatis/openclaw-cli-bridge-elvatis
metadata:
  {
    "openclaw":
      {
        "emoji": "🌉",
        "requires": { "bins": ["openclaw", "claude", "gemini"] },
        "commands": ["/cli-sonnet", "/cli-opus", "/cli-haiku", "/cli-gemini", "/cli-gemini-flash", "/cli-gemini3"]
      }
  }
---
# OpenClaw CLI Bridge

该工具将本地安装的AI命令行接口（CLI）以及Web浏览器会话作为模型提供者连接到OpenClaw。整个过程分为四个阶段：

## 第一阶段 — Codex认证桥接
从用户现有的`~/.codex/auth.json`文件中注册`openai-codex`提供者，无需重新登录。

## 第二阶段 — 请求代理
一个兼容OpenAI的本地HTTP代理（`127.0.0.1:31337`）负责将VLLM模型的调用路由到相应的CLI子进程：
- `vllm/cli-gemini/gemini-2.5-pro` / `gemini-2.5-flash` / `gemini-3-pro`
- `vllm/cli-claude/claude-sonnet-4-6` / `claude-opus-4-6` / `claude-haiku-4-5`

用户输入的提示信息会通过`stdin/tmpfile`传递，而不会作为CLI参数传递（这样可以避免长时间会话时出现“E2BIG”错误）。

## 第三阶段 — 命令行命令
共有六个用于切换模型的命令（仅限授权用户使用）：
| 命令 | 对应模型 |
|---|---|
| `/cli-sonnet` | `vllm/cli-claude/claude-sonnet-4-6` |
| `/cli-opus` | `vllm/cli-claude/claude-opus-4-6` |
| `/cli-haiku` | `vllm/cli-claude/claude-haiku-4-5` |
| `/cli-gemini` | `vllm/cli-gemini/gemini-2.5-pro` |
| `/cli-gemini-flash` | `vllm/cli-gemini/gemini-2.5-flash` |
| `/cli-gemini3` | `vllm/cli-gemini/gemini-3-pro` |
| `/cli-codex` | `openai-codex/gpt-5.3-codex` |
| `/cli-codex54` | `openai-codex/gpt-5.4` |
| `/cli-back` | 恢复到上一个使用的模型 |
| `/cli-test [model]` | 健康检查（不切换模型） |

每个命令默认采用分阶段切换的方式（可以使用`/cli-apply`命令进行强制切换）。

## 第四阶段 — Web浏览器提供者
为四个Web提供者创建持久的Chromium浏览器会话（无需API密钥）：
- **Grok** (`web-grok/*`): `/grok-login`, `/grok-status`, `/grok-logout`
- **Gemini** (`web-gemini/*`): `/gemini-login`, `/gemini-status`, `/gemini-logout`
- **Claude.ai** (`web-claude/*`): `/claude-login`, `/claude-status`, `/claude-logout`
- **ChatGPT** (`web-chatgpt/*`): `/chatgpt-login`, `/chatgpt-status`, `/chatgpt-logout`

这些会话在网关重启后仍然保持有效。`/bridge-status`命令可以一次性显示所有四个提供者的状态。

当网关重启时，如果有任何会话过期，系统会自动发送一条WhatsApp提醒，其中包含所需的登录命令（无需用户猜测）。

## 设置方法：
1. 启用该插件并重启网关。
2. （可选）注册Codex认证：`openclaw models auth login --provider openai-codex`
3. 使用`/cli-*`命令从任意渠道切换模型。

有关完整的配置信息和架构图，请参阅`README.md`。

**版本：** 1.6.2