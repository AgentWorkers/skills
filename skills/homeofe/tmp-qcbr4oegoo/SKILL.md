---
name: openclaw-cli-bridge-elvatis
description: 将本地的 AI CLI（如 Grok、Gemini、Claude.ai、ChatGPT）与网页浏览器会话（Grok、Gemini、Claude.ai、ChatGPT）集成到 OpenClaw 中，作为模型提供者。系统支持使用 `/cli-*` 命令实现即时模型切换，并为这四种网页提供者维护持久的浏览器会话状态。
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

该工具将本地安装的AI命令行接口（CLI）与网页浏览器会话连接到OpenClaw，作为模型提供者。整个过程分为四个阶段：

## 第一阶段 — Codex认证桥接
从用户现有的`~/.codex/auth.json`文件中注册`openai-codex`提供者，无需重新登录。

## 第二阶段 — 请求代理
一个兼容OpenAI的本地HTTP代理（`127.0.0.1:31337`）负责将VLLM模型的调用路由到相应的CLI子进程：
- `vllm/cli-gemini/gemini-2.5-pro` / `gemini-2.5-flash` / `gemini-3-pro`
- `vllm/cli-claude/claude-sonnet-4-6` / `claude-opus-4-6` / `claude-haiku-4-5`
- `vllm/local-bitnet/bitnet-2b` → 连接到127.0.0.1:8082上的BitNet Llama服务器

用户输入的提示信息通过`stdin/tmpfile`传递，而不是作为CLI参数传递（这样可以避免在长时间会话中遇到“E2BIG”错误）。

## 第三阶段 — 命令行切换模型
只有经过授权的用户才能使用以下六个命令来切换模型：
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
| `/cli-bitnet` | `vllm/local-bitnet/bitnet-2b` |
| `/cli-back` | 恢复上一个使用的模型 |
| `/cli-test [model]` | 健康检查（不切换模型） |

默认情况下，每个命令都会逐步切换模型（可以使用`/cli-apply`命令强制切换）。

## 第四阶段 — 网页浏览器提供者
四个网页浏览器提供者使用持久化的Chromium会话（无需API密钥）：
- **Grok** (`web-grok/*`): `/grok-login`, `/grok-status`, `/grok-logout`
- **Gemini** (`web-gemini/*`): `/gemini-login`, `/gemini-status`, `/gemini-logout`
- **Claude.ai** (`web-claude/*`): `/claude-login`, `/claude-status`, `/claude-logout`
- **ChatGPT** (`web-chatgpt/*`): `/chatgpt-login`, `/chatgpt-status`, `/chatgpt-logout`

这些会话在网关重启后仍会保持有效。`/bridge-status`命令可以一目了然地查看所有四个提供者的状态。

当网关重启时，如果有任何会话过期，系统会自动发送一条WhatsApp提醒，其中包含所需的登录命令（无需用户自行猜测）。

**浏览器健康状况仪表板：** `http://127.0.0.1:31337/status` — 实时显示所有四个提供者的状态、cookie过期情况以及可用模型列表。页面每30秒自动刷新一次。

**设置步骤：**
1. 启用插件并重启网关。
2. （可选）注册Codex认证：`openclaw models auth login --provider openai-codex`
3. 使用`/cli-*`命令从任意渠道切换模型。

详细配置信息和架构图请参阅`README.md`文件。

**版本：** 1.8.2