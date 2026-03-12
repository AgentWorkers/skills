---
name: clawhub-cli
description: 使用 ClawHub CLI 来搜索、安装、更新以及发布来自 clawhub.ai 的代理技能。当您需要即时获取新技能、将已安装的技能同步到最新版本或特定版本，或者使用 npm 安装的 ClawHub CLI 发布新的或已更新的技能文件夹时，请使用该工具。
---
# ClawHub CLI 辅助工具

本文档介绍了如何使用 **ClawHub CLI** 来管理来自公共 ClawHub 注册表的技能。

## 使用场景

当用户需要执行以下操作时，请使用本文档中的命令：

- **按名称或自然语言在 ClawHub 中搜索技能**。
- **将技能从 ClawHub 安装到本地工作空间**。
- **将已安装的技能更新为最新版本或特定版本**。
- **将本地技能文件夹发布到 ClawHub**。

## 前提条件

- **已全局安装 ClawHub CLI**：
  ```bash
  npm i -g clawhub
  ```
  或
  ```bash
  pnpm add -g clawhub
  ```
- **用户已登录**：
  ```bash
  clawhub login
  ```
  或
  ```bash
  clawhub login --token <api-token>
  ```

## 常见工作流程

### 搜索技能

当用户需要查找特定技能（例如 “Postgres backup” 或 “Git tools”）时，可以使用以下命令：
```bash
clawhub search "your query"
```
您可以根据用户的描述提供具体的搜索关键词或技能标识符（slug）。

### 安装技能

要将技能安装到当前工作空间（默认为 `skills` 目录）中，可以使用以下命令：
```bash
clawhub install <skill-slug>
```
示例：
```bash
clawhub install postgres-backup-tools
```
如果用户需要指定特定版本，可以使用 `--version <semver>` 参数。

### 列出已安装的技能

使用以下命令可以查看当前已安装的所有技能：
```bash
clawhub list
```

### 更新已安装的技能

- **更新所有已安装的技能至最新版本**：
  ```bash
  clawhub update --all
  ```
- **更新单个技能**：
  ```bash
  clawhub update <skill-slug>
  ```
  如果需要指定版本号，可以使用 `--version <semver>` 参数。

### 发布本地技能

对于包含 `SKILL.md` 文件的本地技能文件夹（例如 `skills/my-skill`），可以使用以下命令进行发布：
```bash
clawhub publish ./skills/my-skill \
  --slug my-skill \
  --name "My Skill" \
  --version 0.1.0 \
  --tags latest
```
请根据实际情况调整参数：
- `./skills/my-skill`：替换为实际的文件夹路径。
- `slug`：使用唯一的小写连字符标识符。
- `version`：使用有效的版本号（如 `0.1.0`、`1.0.0` 等）。
- `tags`：添加合适的标签（如 `latest`、`beta`、`internal` 等）。

### 同步多个技能

如果用户有多个技能文件夹（位于 `skills/` 目录下），可以使用以下命令进行同步：
```bash
clawhub sync --all
```

可选参数：
- `--tags latest`：为新/更新的技能添加标签。
- `--changelog "Update skills"`：在非交互式模式下执行同步操作时使用。
- `--bump patch|minor|major`：自动更新技能的版本号（`patch`、`minor`、`major`）。
- `--dry-run`：先查看同步结果，再决定是否实际发布。

## 验证与故障排除

在提供命令建议后，请让用户检查 CLI 的输出是否包含错误信息。对于发布或同步操作，可以建议用户执行以下操作：
- 使用 `clawhub list` 查看本地技能列表。
- 打开 `clawhub.ai` 网站，通过技能标识符或名称查找相关技能信息。
- 如果出现错误（例如技能标识符已存在、版本冲突或未登录），请解释错误原因，并提供相应的解决方案（例如使用新的技能标识符、更新版本号或重新登录）。