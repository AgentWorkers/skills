---
name: openpond-cli
description: 使用 OpenPond CLI 来创建仓库（repositories）、监控部署（deployments）以及运行工具（tools），而无需使用 Web 界面。
metadata:
  short-description: OpenPond CLI workflows
---

# OpenPond CLI

当代理需要通过 CLI（命令行界面）创建或管理 OpenPond 应用程序时，请使用此技能，无需使用 MCP（管理控制面板）。

## 快速设置

- 安装：`npm i -g openpond-code`（或 `npx --package openpond-code openpond <cmd>`）
- 登录：运行 `openpond login` 或设置 `OPENPOND_API_KEY`
- 非交互式登录：`openpond login --api-key opk_...`

## 常见工作流程

- 创建内部仓库并关联远程仓库：
  - `openpond repo create --name my-repo --path .`
- 非交互式推送（使用令牌化身份验证）：
  - `openpond repo create --name my-repo --path . --token`
  - `git add . && git commit -m "init"`
  - `openpond repo push --path . --branch main`
  - `openpond repo push` 会读取 `.git/config` 文件，临时使用令牌进行身份验证，并在推送完成后恢复原设置。
- 监控部署情况：
  - `openpond deploy watch handle/repo --branch main`
- 列出并运行工具：
  - `openpond tool list handle/repo`
  - `openpond tool run handle/repo myTool --body '{"foo":"bar"}'`
- 账户级 API：
  - `openpond apps list [--handle <handle>] [--refresh]`
  - `openpond apps tools`
  - `openpond apps performance --app-id app_123`
  - `openpond apps agent create --prompt "Build a daily digest agent"`

## OpenTool 代理

可以使用 CLI 通过 `npx` 来运行 OpenTool 命令：

- `openpond opentool init --dir .`
- `openpond opentool validate --input tools`
- `openpond opentool build --input tools --output dist`

## 配置和 URL

- 可选的环境变量：`OPENPOND_BASE_URL`、`OPENPOND_API_URL`、`OPENPOND_TOOL_URL`、`OPENPOND_API_KEY`
- 缓存文件：`~/.openpond/cache.json`（下次使用时会自动更新）