---
name: git-changelog
description: 从 Git 提交中生成变更日志。支持 markdown、纯文本和 JSON 格式输出，并支持基于日期范围和标签的过滤。
---
# Git 变更日志（Git Changelog）

## 使用场景

从 Git 提交历史中生成易于阅读的变更日志。适用于任何 Git 仓库。

## 安装要求

无需额外依赖，仅使用 Git 和 Bash。

## 使用方法

### 基本变更日志（过去 30 天或自最后一个标签以来的提交）

```bash
bash scripts/changelog.sh --repo /path/to/repo
```

### 自指定日期以来的提交

```bash
bash scripts/changelog.sh --repo /path/to/repo --since "2026-01-01"
```

### 日期范围

```bash
bash scripts/changelog.sh --repo /path/to/repo --since "2026-01-01" --until "2026-02-01"
```

### JSON 格式输出（用于程序化处理）

```bash
bash scripts/changelog.sh --repo /path/to/repo --format json
```

### 纯文本输出

```bash
bash scripts/changelog.sh --repo /path/to/repo --format plain
```

## 输出格式

| 格式 | 描述 |
|--------|-------------|
| `markdown` | 默认格式：包含标题、提交哈希、作者和日期 |
| `plain` | 简单的列表格式 |
| `json` | 包含提交对象（包含哈希、主题、作者和日期）的数组 |

## 配置选项

| 选项 | 描述 | 默认值 |
|------|-------------|---------|
| `--repo <路径>` | 仓库路径 | 当前目录 |
| `--since <日期>` | 开始日期 | 最后一个标签或 30 天前 |
| `--until <日期>` | 结束日期 | 当前时间 |
| `--format <格式>` | 输出格式（`markdown`/`plain`/`json`） |
| `--group` | 按提交类型分组 | 关闭（需要 Bash 4.0 或更高版本） |

## 注意事项

- 自动检测最后一个 Git 标签并将其作为输出起点 |
- 排除合并提交以获得更清晰的日志内容 |
- 会提取常见的提交类型（如 `feat`、`fix`、`docs` 等）以生成 JSON 格式的输出 |
- 使用 `--group` 选项时需要 Bash 4.0 或更高版本（macOS 默认使用的是 Bash 3.2；可通过 `brew install bash` 安装）