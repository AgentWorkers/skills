---
name: github-kb
description: 管理一个本地的 GitHub 知识库，并通过 `gh CLI` 提供搜索功能。当用户询问关于仓库（repositories）、 pull 请求（PRs）、问题（issues）的信息，或者需要克隆 GitHub 仓库、探索代码库（codebases）或获取 GitHub 项目的相关信息时，可以使用该功能。支持通过 `gh CLI` 在 GitHub 上进行搜索，同时也支持使用 `GITHUB_KB.md` 目录来管理本地知识库。配置方式是通过 `GITHUB_TOKEN` 和 `GITHUB_KB_PATH` 环境变量来设置。
---

# GitHub知识库

通过`gh CLI`管理本地GitHub知识库，并提供GitHub搜索功能。关键文件：`GITHUB_KB.md`，位于知识库目录的根目录下，该文件记录了所有项目的简要描述。

## 配置

使用前请设置环境变量：
- `GITHUB_TOKEN` - GitHub个人访问令牌（可选，用于私有仓库）
- `GITHUB_KB_PATH` - 本地知识库目录的路径（默认值：`/home/node/clawd/github-kb`）

示例：
```bash
export GITHUB_TOKEN="ghp_xxxx..."
export GITHUB_KB_PATH="/your/path/github-kb"
```

**令牌安全性提示：**切勿将令牌硬编码在代码中。应通过环境变量或容器秘密进行配置。

## GitHub CLI（gh）

**要求：**必须安装并登录GitHub CLI。

**安装方法：**
- **macOS：** `brew install gh`
- **Linux：** `apt install gh` 或参考[官方安装指南](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
- **Windows：** `winget install GitHub.cli`

**登录：**
```bash
# Interactive login
gh auth login

# Or use token from GITHUB_TOKEN env var
gh auth login --with-token <(echo "$GITHUB_TOKEN")
```

**验证：**运行 `gh auth status` 检查是否已成功登录。

如果未安装`gh`或未登录，请跳过搜索操作，仅使用本地知识库的功能。

### 搜索仓库

```bash
# Search repos by keyword
gh search repos <query> [--limit <n>]

# Examples:
gh search repos "typescript cli" --limit 10
gh search repos "language:python stars:>1000" --limit 20
gh search repos "topic:mcp" --limit 15
```

**搜索条件：**
- `language:<lang>` - 按编程语言筛选
- `stars:<n>` 或 `stars:><n>` - 按星数筛选
- `topic:<name>` - 按主题筛选
- `user:<owner>` - 在用户的仓库中搜索
- `org:<org>` - 在组织内搜索

### 搜索问题

```bash
gh search issues "react hooks bug" --limit 20
gh search issues "repo:facebook/react state:open" --limit 30
gh search issues "language:typescript label:bug" --limit 15
```

**搜索条件：**
- `repo:<owner/repo>` - 在特定仓库中搜索
- `state:open|closed` - 按问题状态筛选
- `author:<username>` - 按作者筛选
- `label:<name>` - 按标签筛选
- `language:<lang>` - 按仓库语言筛选
- `comments:<n>` 或 `comments:><n>` - 按评论数量筛选

### 搜索拉取请求（Pull Requests）

```bash
# Search PRs
gh search prs <query> [--limit <n>]

# Examples:
gh search prs "repo:vercel/next.js state:open" --limit 30
gh search prs "language:go is:merged" --limit 15
```

**搜索条件：**
- `repo:<owner/repo>` - 在特定仓库中搜索
- `state:open|closed|merged` - 按拉取请求状态筛选
- `author:<username>` - 按作者筛选
- `label:<name>` - 按标签筛选
- `language:<lang>` - 按仓库语言筛选
- `is:merged|unmerged` - 按合并状态筛选

### 查看拉取请求/问题详情

```bash
# View issue/PR details
gh issue view <number> --repo <owner/repo>
gh pr view <number> --repo <owner/repo>

# View with comments
gh issue view <number> --repo <owner/repo> --comments
gh pr view <number> --repo <owner/repo> --comments
```

## 本地知识库的工作流程

### 在知识库中查询仓库信息

1. 阅读`GITHUB_KB.md`以了解有哪些项目。
2. 在`${GITHUB_KB_PATH}`目录下找到相应的项目目录。

### 将新仓库克隆到知识库

1. 如果不知道完整的仓库名称，可以在GitHub上搜索。
2. 将仓库克隆到知识库目录：
   ```bash
   git clone https://github.com/<owner>/<name>.git ${GITHUB_KB_PATH:-/home/node/clawd/github-kb}/<name>
   ```
3. 生成项目描述：阅读`README`文件或关键文件以了解项目详情。
4. 更新`GITHUB_KB.md`：按照现有格式为新仓库添加条目：
   ```markdown
   ### [<name>](/<name>)
   Brief one-line description of what the project does. Additional context if useful (key features, tech stack, etc.).
   ```
5. 确认操作完成：告知用户仓库已克隆的位置。

### 默认克隆位置

如果用户仅输入“clone X”而没有指定目录，系统会自动克隆到默认位置：`${GITHUB_KB_PATH}`。

## `GITHUB_KB.md`的格式

该目录文件遵循以下结构：

```markdown
# GitHub Knowledge Base

This directory contains X GitHub projects covering various domains.

---

## Category Name

### [project-name](/project-name)
Brief description of the project.
```

在更新时，请保持分类的一致性和格式的规范性。