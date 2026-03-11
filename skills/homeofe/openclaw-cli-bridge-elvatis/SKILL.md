---
name: openclaw-cli-bridge-elvatis
description: 将本地的 Codex、Gemini 和 Claude Code CLI 作为 vllm 模型提供者集成到 OpenClaw 中。这些 CLI 提供了 `/cli-*` 系列命令，用于即时切换模型（例如：/cli-sonnet、/cli-opus、/cli-haiku、/cli-gemini、/cli-gemini-flash、/cli-gemini3）。通过最小化的环境配置，可以安全地使用 E2BIG 功能。
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

该工具将本地安装的 AI CLI（如 Codex、Gemini、Claude Code）作为 OpenClaw 的模型提供者进行桥接。整个过程分为三个阶段：

## 第一阶段：Codex 认证桥接
从用户现有的 `~/.codex/auth.json` 文件中注册 `openai-codex` 提供者，无需重新登录。

## 第二阶段：请求代理
一个与 OpenAI 兼容的本地 HTTP 代理（`127.0.0.1:31337`）会将 VLLM 模型的请求路由到相应的 CLI 子进程：
- `vllm/cli-gemini/gemini-2.5-pro` / `gemini-2.5-flash` / `gemini-3-pro`
- `vllm/cli-claude/claude-sonnet-4-6` / `claude-opus-4-6` / `claude-haiku-4-5`

用户输入的提示内容会通过 `stdin/tmpfile` 传递，而不会作为 CLI 参数传递（这样可以避免长时间会话时出现 `E2BIG` 错误）。

## 第三阶段：命令行快捷命令
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
| `/cli-codex-mini` | `openai-codex/gpt-5.1-codex-mini` |
| `/cli-back` | 恢复到上一个使用的模型 |
| `/cli-test [model]` | 健康检查（不切换模型） |

每个命令会原子性地执行 `openclaw models set <model>` 操作，并返回确认信息。

## 设置方法：
1. 启用该插件并重启 gateway。
2. （可选）注册 Codex 认证：`openclaw models auth login --provider openai-codex`
3. 使用 `/cli-*` 命令从任意通道切换模型。

有关完整的配置信息和架构图，请参阅 `README.md`。

**版本：** 0.2.27