---
name: greptile
description: "查询、搜索以及管理由 Greptile（一种用于代码库智能分析的工具）索引的仓库。适用于对代码库提出疑问、搜索代码模式、将仓库添加到 Greptile 的索引以供审查，或检查 Greptile 的索引状态等场景。使用该功能需要 `GREPTILE_TOKEN` 以及 GitHub/GitLab 的访问令牌。"
metadata:
  openclaw:
    emoji: "🦎"
    publisher: "@iahmadzain"
    requires:
      env: [GREPTILE_TOKEN, GITHUB_TOKEN]
      bins: [curl, jq, gh]
---
# Greptile 技能

通过 REST API 查询和管理由 Greptile 索引的仓库。

## 设置

所需的环境变量：
- `GREPTILE_TOKEN` — Greptile API 令牌（从 https://app.greptile.com 获取）
- `GITHUB_TOKEN` — 具有仓库访问权限的 GitHub PAT（也可以设置 `GREPTILE_GITHUB_TOKEN`，或者通过 `gh auth login` 进行身份验证——脚本会默认使用 `gh auth token`）

## 命令

所有命令都使用 `scripts/greptile.sh`（路径相对于此技能目录）。

### 索引仓库

```bash
scripts/greptile.sh index owner/repo [branch] [--remote github|gitlab] [--no-reload] [--no-notify]
```

默认分支：`main`。如果仓库已经过索引处理，可以使用 `--no-reload` 选项跳过重新索引。

### 检查索引状态

```bash
scripts/greptile.sh status owner/repo [branch] [--remote github|gitlab]
```

返回值：`status`（已完成/正在处理/失败）、`filesProcessed`、`numFiles`。

### 查询代码库（包含 AI 回答和源代码）

```bash
scripts/greptile.sh query owner/repo [branch] "How does auth work?" [--genius] [--remote github|gitlab]
```

- `--genius` — 分析速度较慢但更加准确（适用于 PR 审查、架构相关问题）
- 返回值：AI 生成的答案以及带有行号的源代码文件引用

### 搜索代码库（仅返回源代码，不含 AI 回答）

```bash
scripts/greptile.sh search owner/repo [branch] "payment processing" [--remote github|gitlab]
```

返回值：按相关性排序的相关文件、函数和代码片段列表，以及它们的行号。

## 提示

- 在查询或搜索仓库之前，请务必先对其进行索引。使用 `status` 命令确认索引是否已完成。
- 对于复杂的问题（如架构分析或 PR 审查），请使用 `query --genius` 命令。
- 如果只需要文件的位置而无需 AI 解释，请使用 `search` 命令。
- 对于 GitLab 仓库，请添加 `--remote gitlab` 选项。
- 可以使用 `jq` 对输出进行格式化：`scripts/greptile.sh query ... | jq .`
- 支持对多个仓库进行查询，但需要直接通过 API 来处理多个仓库的相关信息。