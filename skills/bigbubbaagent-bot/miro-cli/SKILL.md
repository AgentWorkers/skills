---
name: miro-cli
description: Miro CLI 工具用于通过命令行进行板（board）、团队（team）或组织（organization）的管理。适用于查询板信息、导出数据、查看团队/组织信息，以及从终端自动执行 Miro 的工作流程。
metadata:
  {
    "openclaw":
      {
        "requires":
          {
            "bins": ["mirocli", "jq", "column"],
            "system": ["bash"],
            "credentials": ["miro_org_id", "miro_client_id", "miro_client_secret"]
          },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "davitp/mirocli",
              "bins": ["mirocli"],
              "label": "Install Miro CLI from npm (davitp/mirocli)",
              "verify": "Verify package author on https://www.npmjs.com/package/mirocli"
            },
            {
              "id": "jq",
              "kind": "homebrew",
              "package": "jq",
              "bins": ["jq"],
              "label": "Install jq (JSON processor)",
              "optional": true
            },
            {
              "id": "column",
              "kind": "system",
              "bins": ["column"],
              "label": "column command (usually pre-installed)",
              "optional": true
            }
          ],
        "credentials":
          [
            {
              "name": "miro_org_id",
              "type": "text",
              "description": "Miro Organization ID (from organization settings)"
            },
            {
              "name": "miro_client_id",
              "type": "text",
              "description": "Miro App Client ID (from app settings)"
            },
            {
              "name": "miro_client_secret",
              "type": "password",
              "description": "Miro App Client Secret (stored in system keyring by mirocli, never in this skill)"
            }
          ]
      }
  }
---
# Miro CLI 技能

本文档提供了使用 Miro CLI 工具通过命令行与 Miro 平台 API 进行交互的全面指南。

## ⚠️ 安装前的重要安全提示

**1. 验证 mirocli npm 包**
- 包名：`davitp/mirocli`（在 npm 上）
- 请访问 https://www.npmjs.com/package/mirocli 进行验证
- 检查：包的作者、GitHub 仓库以及最近的更新情况
- 是否为官方的 Miro 集成工具？否。这是一个社区开发工具？
- **由您自行判断**：对于您的使用场景来说，这个工具是否可靠？

**2. 外部二进制文件的信任问题**
- 本技能会通过子进程运行 `mirocli`（一个外部 npm 包）
- 您的客户端 ID 和客户端密钥需要手动输入，并由该外部二进制文件进行管理
- **您必须信任**：`mirocli` 将 OAuth 令牌存储在哪里（系统密钥库），以及它如何处理这些凭据

**3. 辅助二进制文件**
- 本技能使用了 `jq`（JSON 处理工具）和 `column`（文本格式化工具）
- 这两个工具都是标准的 Unix 工具，但需要单独安装
- 对于基本使用来说，`jq` 是可选的；对于辅助脚本来说，`column` 也是可选的

**4. 路径设置（可选）**
- 您可以将辅助脚本添加到系统的 `PATH` 中：`export PATH="$PATH:~/.openclaw/workspace/skills/miro-cli/scripts"`
- 这样就可以从任何地方运行这些脚本了：例如 `export-team-boards.sh <team-id>`
- 在进行此操作之前，请务必理解路径设置的变化

**5. 建议**
- 首先在隔离的环境中或使用非敏感账户进行测试
- 在使用生产环境的凭据之前，请先验证 `mirocli` 的行为
- 查看 `mirocli` 的源代码：https://github.com/davitp/mirocli

## 功能概述

Miro CLI 允许通过命令行访问 Miro 的各种资源和企业级功能：
- **看板** — 列出、搜索和管理看板
- **团队** — 查看和组织团队
- **组织** — 查看组织详情和成员信息
- **看板导出** — 将看板导出为 PDF、PNG 或 SVG 格式
- **内容日志** — 查看活动/变更日志（仅限企业版）
- **审计日志** — 访问审计日志（仅限企业版）

非常适合自动化操作、脚本编写和批量处理任务。

## 所需条件

**必备的二进制文件：**
- `mirocli` — Miro CLI 工具（通过 npm 安装）
- `jq` — JSON 查询工具（用于过滤和脚本编写）
- `column` — 文本格式化工具（用于辅助脚本中的表格输出）

**需要手动输入的凭据：**
- **组织 ID** — 您的 Miro 组织标识符
- **客户端 ID** — OAuth 应用的客户端 ID
- **客户端密钥** — OAuth 应用的客户端密钥

**（针对 JSON 工作流程的可选工具：）**
- `jq` — 用于高级过滤和数据转换的 JSON 处理工具

## 安装与配置

### 1. 安装依赖项

**mirocli**（必备）：
```bash
npm install -g mirocli
```

**jq**（可选，但推荐）：
```bash
# macOS
brew install jq

# Linux (Debian/Ubuntu)
sudo apt install jq

# Linux (Fedora)
sudo dnf install jq
```

### 2. 配置上下文（一次性操作）

```bash
mirocli context add
```

系统会提示您输入：
- 上下文名称（例如 `default`）
- 组织 ID（来自您的 Miro 设置）
- 客户端 ID（来自您的 Miro 应用）
- 客户端密钥（来自您的 Miro 应用）

凭据会被 `mirocli` 安全地存储在 `~/.mirocli/` 文件夹中（macOS/Linux 系统的密钥库中）。

### 3. 使用 OAuth 进行身份验证

```bash
mirocli auth login        # Opens browser for OAuth flow
mirocli auth whoami       # Verify authentication
```

## 快速入门

### 查看组织信息
```bash
mirocli organization view
```

### 列出看板
```bash
mirocli boards list                    # All boards
mirocli boards list --json             # JSON output
mirocli boards list --team-id <id>     # Filter by team
mirocli boards list --sort "name"      # Sort by field
```

### 列出团队
```bash
mirocli teams list
mirocli teams list --name "Design"     # Filter by name
mirocli teams list --json
```

### 导出看板
```bash
mirocli board-export <board-id> --format pdf
mirocli board-export <board-id> --format png
mirocli board-export <board-id> --format svg
```

## 常用操作流程

### 按名称查找看板
```bash
mirocli boards list --json | jq '.[] | select(.name | contains("Design"))'
```

### 从团队中导出所有看板
请参考 `scripts/export-team-boards.sh` 脚本

### 列出带有所有者信息的看板
```bash
mirocli boards list --json | jq '.[] | {name, id, owner: .owner.name}'
```

### 按日期过滤看板
```bash
mirocli boards list --modified-after "2026-03-01" --json
```

## 安装步骤

1. **安装依赖项** → `npm install -g mirocli`（如有需要，还需安装 `jq` 和 `column`）
2. **配置上下文** → `mirocli context add`（手动输入组织 ID、客户端 ID 和客户端密钥）
3. **进行身份验证** → `mirocli auth login`（浏览器会弹出 OAuth 登录页面）
4. **验证身份** → `mirocli auth whoami`（确认身份验证是否成功）
5. **使用 CLI** → `mirocli boards list`、`mirocli teams list` 等

**凭据存储方式：** `mirocli` 将凭据安全地存储在 `~/.mirocli/` 文件夹中（使用系统密钥库，仅限本地访问）

## 全局选项

```bash
-c, --context <name>    # Use specific context
-h, --help             # Show help
-v, --version          # Show version
--json                 # Output as JSON
```

## 安全性与信任机制

**凭据的处理方式：**
- **本地存储** — `mirocli` 使用系统密钥库进行存储（安全，仅限本地访问）
- **凭据不存储在技能文件中** — 凭据是通过 `mirocli context add` 功能手动输入的
- **OAuth 令牌** — `mirocli` 负责管理 OAuth 会话令牌；这些令牌不会离开您的设备
- **数据导出** — 看板导出文件仅保存在本地；不会将数据发送给 Miro API 之外的第三方

**本技能的功能：**
- ✅ 通过 Miro API 读取/列出看板、团队和组织信息
- ✅ 将看板导出为 PDF/PNG/SVG 格式
- ✅ 查看活动/审计日志（仅限企业版）
- ❌ 仅支持读取操作，不允许修改看板/团队信息
- ❌ 从不将凭据存储在技能文件中
- ❌ 从不将数据发送到 Miro API 之外的地方

**第三方依赖：**
- 本技能依赖于以下组件：
  - **mirocli**（npm 包）—— 处理凭据存储的外部 CLI 工具
  - **Miro API** — 直接调用 Miro 的官方 API 端点
  - **系统密钥库** — 系统级别的凭据存储机制（macOS Keychain、Linux Secret Service、Windows Credential Manager）

## 命令参考

详细命令文档请参阅 `references/miro-cli-commands.md`。

## 帮助文档

```bash
mirocli --help
mirocli <command> --help
```

## 相关技能
- `miro-mcp` — 用于 Miro 的 MCP 集成工具（AI 编程工具）
- `miro-sdk` — 用于开发插件的 Web SDK
- `miro-api` — 用于程序化访问的 REST API 文档

---

**设置日期：** 2026-03-14  
**最后更新时间：** 2026-03-14  
**状态：** 准备就绪（需完成 OAuth 登录配置）