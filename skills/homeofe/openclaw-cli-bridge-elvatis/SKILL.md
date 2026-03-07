---
name: openclaw-cli-bridge-elvatis
description: 将本地 Codex、Gemini 和 Claude 的 CLI 功能集成到 OpenClaw 中：通过 Codex 的 OAuth 认证机制，以及基于 vllm 的 Gemini/Claude OpenAI 兼容的本地代理服务，实现各工具之间的无缝连接。
homepage: https://github.com/elvatis/openclaw-cli-bridge-elvatis
metadata:
  {
    "openclaw":
      {
        "emoji": "🌉",
        "requires": { "bins": ["openclaw", "codex", "gemini", "claude"] }
      }
  }
---
# OpenClaw CLI Bridge Elvatis

该项目提供了两个主要功能层：

1. **Codex 身份验证桥接层**：用于 `openai-codex/*` 系统，通过从 `~/.codex/auth.json` 文件中读取现有的 Codex CLI OAuth 令牌来实现身份验证。
2. **本地 OpenAI 兼容代理层**（默认地址为 `127.0.0.1:31337`）：用于通过 OpenClaw 的 `vllm` 提供者模型来执行 Gemini/Claude CLI 命令：
   - `vllm/cli-gemini/*`
   - `vllm/cli-claude/*`

有关设置和架构的详细信息，请参阅 `README.md` 文件。