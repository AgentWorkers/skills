---
name: wip-file-guard
description: 该功能用于阻止对受保护的身份文件进行破坏性编辑。适用于 Claude Code CLI 和 OpenClaw 工具。
license: MIT
interface: [cli, module, hook, plugin, skill]
metadata:
  display-name: "Identity File Protection"
  version: "1.0.1"
  homepage: "https://github.com/wipcomputer/wip-file-guard"
  author: "Parker Todd Brooks"
  category: dev-tools
  capabilities:
    - file-protection
    - edit-blocking
    - identity-guard
  requires:
    bins: [node]
  openclaw:
    requires:
      bins: [node]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-file-guard"
        bins: [wip-file-guard]
        label: "Install via npm"
    emoji: "🛡️"
compatibility: Requires node. Node.js 18+.
---
# wip-file-guard

这是一个用于阻止对受保护的身份文件进行破坏性编辑的钩子（hook），适用于 Claude Code CLI 和 OpenClaw 工具。

## 何时使用此功能

**适用于以下场景：**
- 保护 CLAUDE.md、SOUL.md、IDENTITY.md、MEMORY.md 等身份文件不被覆盖
- 阻止 AI 代理替换文件内容，而非仅对其进行扩展
- 在上下文压缩后仍能保护文件内容（虽然行为规则可能会被清除，但钩子仍然有效）

**注意：** 这只是一个技术性的防护机制，而非命令或提示。它会在操作发生之前就将其阻止。

### 不适用的情况

- 不能用于保护二进制文件或图像文件
- 不能阻止所有编辑操作（仅阻止破坏性编辑，允许进行少量修改）

### 工作原理

有两个主要规则：
1. 对受保护的文件，任何写入操作（Write）都会被阻止，应使用“Edit”命令进行修改。
2. 如果对受保护文件的修改导致文件内容减少了超过 2 行，那么“Edit”操作也会被阻止。

### 受保护的文件

CLAUDE.md、SHARED-CONTEXT.md、SOUL.md、IDENTITY.md、CONTEXT.md、TOOLS.md、MEMORY.md

### 受保护的文件命名模式

任何包含 “memory”、“memories”、“journal”、“diary” 或 “daily log” 等关键词的文件都属于受保护文件。

## API 参考

### CLI

```bash
node guard.mjs --list          # list protected files
bash test.sh                   # run test suite
```

### Claude Code 中的配置方法

将以下配置添加到 `~/.claude/settings.json` 文件中：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "node \"/path/to/wip-file-guard/guard.mjs\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

## 故障排除

### 代理持续尝试写入文件

系统会向代理发送拒绝消息，提示其重新读取文件并使用 “Edit” 命令进行修改。如果代理忽略该提示，可能是因为文件在上下文压缩后被损坏（导致信息丢失），此时钩子会继续阻止操作。

### 编辑操作被意外阻止

请检查文件内容的修改情况：如果修改导致文件内容减少了超过 2 行，编辑操作将被阻止；而添加或替换 1-2 行的少量修改则是允许的。