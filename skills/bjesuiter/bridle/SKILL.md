---
name: bridle
description: 这是一个统一的配置管理器，专为AI编码助手设计。它用于管理用户配置文件，安装各种技能/代理/命令，并在Claude Code、OpenCode、Goose和Amp等多个平台之间切换配置。
author: Benjamin Jesuiter <bjesuiter@gmail.com>
metadata:
  clawdbot:
    emoji: "🐴"
    os: ["darwin", "linux"]
    requires:
      bins: ["bridle"]
    install:
      - id: brew
        kind: brew
        formula: neiii/bridle/bridle
        bins: ["bridle"]
        label: Install bridle via Homebrew
      - id: cargo
        kind: shell
        command: cargo install bridle
        bins: ["bridle"]
        label: Install bridle via Cargo
---

# Bridle 技能

Bride 是一款统一配置管理器，用于管理 AI 编码助手的相关设置。它可以用来管理配置文件、安装各种技能/代理/命令，并在 Claude Code、OpenCode、Goose 和 Amp 等平台之间切换配置。

## 安装

```bash
# Homebrew (macOS/Linux)
brew install neiii/bridle/bridle

# Cargo (Rust)
cargo install bridle

# From source
git clone https://github.com/neiii/bridle && cd bridle && cargo install --path .
```

## 核心概念

- **AI 编码助手**：包括 `claude`、`opencode`、`goose` 和 `amp` 等工具。
- **配置文件**：每个 AI 编码助手对应的保存的配置文件（例如 `work`、`personal`、`minimal` 等）。

## 快速命令

```bash
# Launch interactive TUI
bridle

# Show active profiles across all harnesses
bridle status

# Initialize bridle config and default profiles
bridle init
```

## 配置文件管理

```bash
# List all profiles for a harness
bridle profile list <harness>

# Show profile details (model, MCPs, plugins)
bridle profile show <harness> <name>

# Create empty profile
bridle profile create <harness> <name>

# Create profile from current config
bridle profile create <harness> <name> --from-current

# Switch/activate a profile
bridle profile switch <harness> <name>

# Open profile in editor
bridle profile edit <harness> <name>

# Compare profiles
bridle profile diff <harness> <name> [other]

# Delete a profile
bridle profile delete <harness> <name>
```

## 安装组件

Bride 可以从 GitHub 仓库中安装技能、代理和命令，并自动为每个 AI 编码助手转换相应的路径和配置文件。

```bash
# Install from GitHub (owner/repo or full URL)
bridle install owner/repo

# Overwrite existing installations
bridle install owner/repo --force

# Interactively remove components [experimental]
bridle uninstall <harness> <profile>
```

## 配置设置

配置文件的位置：`~/.config/bridle/config.toml`

**配置键**：`profile-marker`、`editor`、`tui.view`、`default_harness`

## 输出格式

所有命令都支持 `-o, --output <format>` 选项：
- `text`（默认）：人类可读的格式
- `json`：机器可读的格式
- `auto`：TTY（终端）使用文本格式，管道（pipe）使用 JSON 格式

## 支持的 AI 编码助手及配置文件位置

| AI 编码助手 | 配置文件位置         | 支持情况       |
| ----------- | ----------------------- | ------------ |
| Claude Code | `~/.claude/`            | 完全支持 |
| OpenCode    | `~/.config/opencode/`   | 完全支持 |
| Goose       | `~/.config/goose/`      | 完全支持 |
| Amp         | `~/.amp/`               | 实验性支持 |

## 各 AI 编码助手的组件路径

| 组件        | Claude Code     | OpenCode     | Goose       |
| ------------ | -------------- | -------------- |
| 技能        | `~/.claude/skills/`   | `~/.config/opencode/skill/` | `~/.config/goose/skills/` |
| 代理        | `~/.claude/plugins/*/agents/` | `~/.config/opencode/agent/` |            |
| 命令        | `~/.claude/plugins/*/commands/` | `~/.config/opencode/command/` |            |
| MCP（配置管理器） | `~/.claude/.mcp.json` | `opencode.jsonc`   | `config.yaml`    |

## 常见工作流程

### 从当前配置创建一个新的工作配置文件
```bash
bridle profile create claude work --from-current
```

### 从现有配置文件创建新配置文件（复制并修改）
```bash
# 1. Switch to the source profile
bridle profile switch opencode default

# 2. Create new profile from current (now the source profile)
bridle profile create opencode minimal --from-current

# 3. Edit the new profile to remove/modify as needed
bridle profile edit opencode minimal
```

### 在不同配置文件之间切换
```bash
bridle profile switch claude personal
bridle profile switch opencode minimal
```

### 查看所有 AI 编码助手的配置状态
```bash
bridle status
```