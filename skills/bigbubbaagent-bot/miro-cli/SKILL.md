---
name: miro-cli
description: Miro CLI（命令行界面工具）用于通过命令行管理板（board）、团队（team）或组织（organization）。适用于查询板信息、导出数据、查看团队/组织结构，以及从终端自动化执行Miro的工作流程。
required_binaries:
  - mirocli
  - jq
  - column
required_credentials:
  - miro_org_id
  - miro_client_id
  - miro_client_secret
metadata:
  openclaw:
    type: cli-tool
    trust_model: external-binary-managed-credentials
    requires:
      binaries:
        - mirocli
        - jq
        - column
      system_tools:
        - bash
      credentials:
        miro_org_id: Organization ID from Miro settings
        miro_client_id: OAuth Client ID from Miro app
        miro_client_secret: OAuth Client Secret (stored in system keyring, NOT in skill)
    install:
      - id: mirocli
        package: davitp/mirocli
        kind: npm
        command: npm install -g mirocli
        required: true
        verify_url: https://www.npmjs.com/package/mirocli
      - id: jq
        package: jq
        kind: homebrew
        command: brew install jq
        required: false
        note: Optional but recommended for JSON filtering
      - id: column
        package: util-linux
        kind: system
        command: Usually pre-installed
        required: false
        note: Optional for table formatting in helper scripts
    security:
      external_binary: true
      binary_name: mirocli
      manages_credentials: true
      credential_storage: system-keyring
      credential_scope: local-only
    capabilities:
      - read-boards
      - read-teams
      - read-organization
      - export-boards
      - view-audit-logs
      - view-content-logs
    limitations:
      - read-only (no create/update/delete)
      - requires-oauth-setup
      - trusts-external-npm-package
---
# Miro CLI 技能

本文档提供了使用 Miro CLI 工具通过命令行与 Miro 平台 API 进行交互的全面指南。

## ⚠️ 信任模型与安全声明

**元数据声明：**
- 类型：CLI 工具封装器（用于管理外部二进制文件）
- 外部二进制文件：`mirocli`（npm 包：davitp/mirocli）
- 是否管理凭据：是（将凭据存储在系统密钥库中，而非技能文件中）
- 凭据存储位置：系统密钥库（仅限本地，由操作系统管理）
- 功能：仅支持读取板、团队、组织和日志的信息
- 限制：无法创建、更新或删除数据；需要先设置 OAuth 访问权限

**关键信任要求：**

**1. 你必须信任 `mirocli` npm 包：**
- 作者：@davitp（社区维护，非官方 Miro 项目）
- 包链接：https://www.npmjs.com/package/mirocli
- 代码仓库链接：https://github.com/davitp/mirocli
- 验证方式：检查 npm 下载记录、最新更新时间、问题报告以及 GitHub 星标数量
- **重要性说明：** 此外部二进制文件负责处理你的客户端 ID、客户端密钥和 OAuth 令牌

**2. 你必须信任你的系统密钥库：**
- macOS：Keychain
- Linux：Secret Service
- Windows：Credential Manager
- **本技能不会：** 存储凭据、缓存令牌或传输它们

**3. 所使用的辅助二进制文件均为标准 Unix 工具：**
- `jq` — JSON 处理工具（开源软件）
- `column` — 文本格式化工具（标准实用程序）
- 这些工具仅用于辅助功能，不涉及凭据处理

**4. 网络访问：**
- 直接通过 HTTPS 连接到 `api.miro.com`（Miro 的官方 API 端点）
- 使用浏览器的 OAuth 认证机制
- 不会通过第三方进行数据代理或凭据传输

**建议：**
在使用生产环境中的凭据之前，请执行以下操作：
1. 查看 `mirocli` 的源代码：https://github.com/davitp/mirocli
2. 使用非敏感的 Miro 账户进行测试
3. 确认 `~/.mirocli/` 文件夹中是否正确存储了 OAuth 令牌
4. 最初在隔离环境中运行该技能

## 功能概述

Miro CLI 允许通过命令行访问 Miro 的各种资源和企业功能：
- **板**：列出、搜索和管理板
- **团队**：查看和组织团队
- **组织**：查看组织详情和成员信息
- **导出板**：将板导出为 PDF、PNG 或 SVG 格式
- **内容日志**：查看活动日志或变更记录（仅限企业版）
- **审计日志**：访问审计日志（仅限企业版）

非常适合自动化脚本编写和批量操作。

## 所需软件

**必备二进制文件：**
- `mirocli` — Miro CLI 工具（通过 npm 安装）
- `jq` — JSON 处理工具（用于过滤和脚本编写）
- `column` — 文本格式化工具（用于辅助脚本中的表格输出）

**凭据（需要手动输入）：**
- 组织 ID：你的 Miro 组织标识符
- 客户端 ID：OAuth 应用的客户端 ID
- 客户端密钥：OAuth 应用的客户端密钥

**（可选，用于 JSON 数据处理：）**
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

系统会提示你输入以下信息：
- 上下文名称（例如：`default`）
- 组织 ID（来自你的 Miro 设置）
- 客户端 ID（来自你的 Miro 应用）
- 客户端密钥（来自你的 Miro 应用）

`mirocli` 会将凭据安全地存储在 `~/.mirocli/` 文件夹中（macOS/Linux 系统的密钥库中）。

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

### 列出板
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

### 导出板
```bash
mirocli board-export <board-id> --format pdf
mirocli board-export <board-id> --format png
mirocli board-export <board-id> --format svg
```

## 常见操作流程

### 按名称查找板
```bash
mirocli boards list --json | jq '.[] | select(.name | contains("Design"))'
```

### 从团队中导出所有板
请参考 `scripts/export-team-boards.sh` 脚本

### 查看带有所有者信息的板
```bash
mirocli boards list --json | jq '.[] | {name, id, owner: .owner.name}'
```

### 按日期筛选板
```bash
mirocli boards list --modified-after "2026-03-01" --json
```

## 安装步骤：

1. **安装依赖项** → `npm install -g mirocli`（如需 `jq` 和 `column`，请同时安装）
2. **配置上下文** → `mirocli context add`（手动输入组织 ID、客户端 ID 和客户端密钥）
3. **进行身份验证** → `mirocli auth login`（浏览器会弹出 OAuth 登录页面）
4. **验证身份** → `mirocli auth whoami`（确认身份验证成功）
5. **开始使用 CLI** → `mirocli boards list`、`mirocli teams list` 等命令

**凭据存储方式：** `mirocli` 将凭据安全地存储在 `~/.mirocli/` 文件夹中（使用系统密钥库，仅限本地访问）。

## 全局选项

```bash
-c, --context <name>    # Use specific context
-h, --help             # Show help
-v, --version          # Show version
--json                 # Output as JSON
```

## 安全性与信任机制

**凭据处理方式：**
- **本地存储**：`mirocli` 使用系统密钥库进行存储（安全，仅限本地访问）
- **不存储在技能文件中**：凭据通过 `mirocli context add` 交互式输入
- **OAuth 令牌**：`mirocli` 负责管理 OAuth 会话令牌；这些令牌不会离开你的设备
- **数据导出**：导出的板文件仅保存在本地，不会发送给 Miro API 之外的第三方

**本技能的功能：**
- ✅ 通过 Miro API 读取/列出板、团队和组织数据
- ✅ 将板导出为 PDF/PNG/SVG 格式
- ✅ 查看活动日志或审计日志（仅限企业版）
- ❌ 无法修改板或团队数据（仅支持读取操作）
- ❌ 不会将凭据存储在技能文件中
- ❌ 不会将数据发送到 Miro API 之外的任何地方

**第三方依赖：**
- **mirocli**：用于处理凭据存储的外部 CLI 工具（npm 包）
- **Miro API**：直接调用 Miro 的官方 API 端点
- **系统密钥库**：操作系统级别的凭据存储机制（macOS Keychain、Linux Secret Service、Windows Credential Manager）

## 命令参考

详细命令文档请参阅 `references/miro-cli-commands.md`。

## 帮助文档

```bash
mirocli --help
mirocli <command> --help
```

**相关技能：**
- `miro-mcp`：用于 Miro 的 MCP 集成（AI 编码工具）
- `miro-sdk`：用于开发插件的 Web SDK
- `miro-api`：用于程序化访问的 REST API 文档

---

**设置日期：** 2026-03-14  
**最后更新时间：** 2026-03-14  
**状态：** 准备就绪（需完成 OAuth 登录设置）