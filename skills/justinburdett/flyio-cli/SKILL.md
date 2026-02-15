---
name: flyio-cli
description: "使用 Fly.io 的 `flyctl` CLI 来部署和操作在 Fly.io 上的应用程序。默认模式下，`flyctl` 仅提供只读诊断功能（如查看应用程序的状态、日志、配置文件及发布信息）。任何会改变应用程序状态的操作（如部署、通过 SSH 执行命令、管理敏感信息、调整资源配置、扩展服务器、管理存储卷或修改 Postgres 数据库）都必须在用户的明确授权下才能执行。`flyctl` 适用于以下场景：根据需求将应用程序部署到 Fly.io 上；调试部署或构建过程中出现的错误；配置 GitHub Actions 以自动化应用程序的部署或预览流程；以及安全地管理和维护 Fly.io 上的应用程序及 Postgres 数据库。"
---

# Fly.io (flyctl) 命令行界面 (CLI)

使用 `flyctl` 可以安全且重复地操作 Fly.io 应用程序。

## 默认设置 / 安全性

- 首先推荐使用 **只读** 命令：`fly status`、`fly logs`、`fly config show`、`fly releases`、`fly secrets list`。
- **未经明确批准，严禁编辑或修改 Fly.io 的应用程序、机器、密钥、卷或数据库。**
  - 只读操作无需批准即可执行。
  - 破坏性操作（如删除或销毁资源）必须获得明确批准。
- 在调试构建过程时，务必记录详细的错误信息，并判断问题出在：
  - 构建/打包环节（Dockerfile、Gemfile.lock、资源预编译问题）
  - 运行时问题（密钥、数据库、迁移操作）
  - 平台相关问题（区域设置、机器状态、健康检查）

## 快速入门（典型部署流程）

从应用程序仓库目录开始：

1) 确认要操作的应用程序：
  - `fly app list`
  - `fly status -a <app>`
  - 查看 `fly.toml` 文件中的 `app = "..."` 配置项。

2) 验证/检查应用程序状态（只读操作）：
  - `fly status -a <app>`
  - `fly logs -a <app>`
  - `fly config show -a <app>`

（部署属于 **高风险操作**，需要用户明确授权。）

## 调试部署/构建失败问题

### 常见问题排查
- `fly deploy --verbose`（显示更多构建日志）
- 如果使用 Dockerfile 进行构建，请确认 Dockerfile 中指定的 Ruby 版本和 Gemfile.lock 中的平台设置与构建环境的操作系统/架构相匹配。

### Rails + Docker + 原生 Gem（如 nokogiri、pg 等）的常见问题
- 建筑过程中可能出现 Bundler 无法找到特定平台版本的 Gem（例如 `nokogiri-…-x86_64-linux`）的情况。

**解决方法**：
- 确保 `Gemfile.lock` 中包含了 Fly 构建工具所支持的 Linux 平台（通常是 `x86_64-linux`）。
  - 示例命令：`bundle lock --add-platform x86_64-linux`
- 确保 Dockerfile 中指定的 Ruby 版本与应用程序的实际版本一致。

（详情请参阅 `references/rails-docker-builds.md`。）

## 日志与配置信息（只读操作）

- 查看日志：`fly logs -a <app>`
- 查看配置信息：`fly config show -a <app>`
- 列出所有密钥（仅显示名称）：`fly secrets list -a <app>`

## 高风险操作（请先请求批准）

这些命令可能在服务器上执行任意代码或更改生产环境的状态。仅当用户明确授权时才能执行：

- 部署：`fly deploy` / `fly deploy --remote-only`
- 通过 SSH 远程执行命令：`fly ssh console -a <app> -C "<命令>"`
- 修改密钥：`fly secrets set -a <app> KEY=value`

更多安全规则请参阅 `references/safety.md`。

## Fly.io 的 Postgres 相关操作

### 查找关联的 Postgres 应用程序：
- `fly postgres list`

### 将 Postgres 数据库连接到应用程序：
- `fly postgres attach <pg-app> -a <app>`

### 在集群中创建数据库：
- `fly postgres db create <db_name> -a <pg-app>`
- `fly postgres db list -a <pg-app>`

### 连接数据库（使用 psql）：
- `fly postgres connect -a <pg-app>`

## 使用 GitHub Actions 进行部署/预览
- 对于生产环境：使用 Fly.io 的 GitHub Action (`superfly/flyctl-actions/setup-flyctl`) 并执行 `flyctl deploy`。
- 对于 Pull Request (PR) 预览：
  - 每个 PR 需要对应一个应用程序和一个数据库。
  - 自动完成创建/部署/添加评论操作；PR 关闭后自动删除相关资源。
  - 详情请参阅 `references/github-actions.md`。

## 其他资源与文档

- `references/safety.md`：安全使用指南（默认为只读模式；修改系统状态前请先请求授权）。
- `references/rails-docker-builds.md`：Rails/Docker 构建过程中可能遇到的问题及解决方法。
- `references/github-actions.md`：Fly.io 的部署和预览工作流程。
- `scripts/fly_app_from_toml.sh`：一个用于从 `fly.toml` 文件中获取应用程序名称的简单脚本（仅支持 Shell 环境，不依赖 Ruby）。