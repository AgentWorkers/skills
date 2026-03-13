---
name: openclaw-cli-bridge-elvatis
description: 将本地的 AI CLI（如 Grok、Gemini、Claude.ai、ChatGPT）与网页浏览器会话（Grok、Gemini、Claude.ai、ChatGPT）集成到 OpenClaw 中，作为模型提供者。系统支持使用 `/cli-*` 命令实现即时模型切换，并为这四个网页提供者维护持久的浏览器会话状态。
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

该工具将本地安装的AI命令行接口（CLI）与网页浏览器会话作为模型提供者连接到OpenClaw。整个过程分为四个阶段：

## 第一阶段 — Codex认证桥接
从用户现有的`~/.codex/auth.json`文件中注册`openai-codex`提供者，无需重新登录。

## 第二阶段 — 请求代理
一个兼容OpenAI的本地HTTP代理（`127.0.0.1:31337`）将VLLM模型的调用路由到相应的CLI子进程：
- `vllm/cli-gemini/gemini-2.5-pro` / `gemini-2.5-flash` / `gemini-3-pro`
- `vllm/cli-claude/claude-sonnet-4-6` / `claude-opus-4-6` / `claude-haiku-4-5`
- `vllm/local-bitnet/bitnet-2b` → 连接到127.0.0.1:8082上的BitNet Llama服务器

用户输入的提示信息通过`stdin/tmpfile`传递，永远不会作为CLI参数传递（这样可以避免长时间会话导致的“E2BIG”错误）。

## 第三阶段 — 命令行快捷命令
只有经过授权的用户才能使用以下六个即时模型切换命令：

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

每个命令默认采用分阶段切换的方式（可以使用`/cli-apply`命令强制应用切换）。

## 第四阶段 — 网页浏览器提供者
四个网页浏览器提供者使用持久的Chromium会话（无需API密钥）：
- **Grok** (`web-grok/*`): `/grok-login`, `/grok-status`, `/grok-logout`
- **Gemini** (`web-gemini/*`): `/gemini-login`, `/gemini-status`, `/gemini-logout`
- **Claude.ai** (`web-claude/*`): `/claude-login`, `/claude-status`, `/claude-logout`
- **ChatGPT** (`web-chatgpt/*`): `/chatgpt-login`, `/chatgpt-status`, `/chatgpt-logout`

会话在网关重启后仍然保持有效。`/bridge-status`命令可以一目了然地查看所有四个提供者的状态。

当网关重启时，如果有任何会话过期，系统会自动发送一条WhatsApp提醒，其中包含所需的登录命令（无需用户猜测）。

**浏览器健康状况仪表板：** `http://127.0.0.1:31337/status` — 提供所有四个提供者的实时状态、cookie过期信息以及模型列表。页面每30秒自动刷新一次。

**设置步骤：**
1. 启用插件并重启网关。
2. （可选）注册Codex认证：`openclaw models auth login --provider openai-codex`
3. 使用`/cli-*`命令从任意渠道切换模型。

有关完整的配置参考和架构图，请参阅`README.md`文件。

**版本：** 1.8.2