---
name: github-cli
description: "全面的 GitHub CLI (gh) 参考指南。涵盖了仓库（repos）、问题（issues）、拉取请求（PRs）、Actions、版本发布（releases）、Gist（代码片段共享）、搜索功能、项目（projects, v2）、API、秘密/变量（secrets/variables）、标签（labels）、代码空间（codespaces）、扩展程序（extensions）、身份验证（auth）以及高级的 GraphQL 使用模式。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🐙",
        "requires": { "bins": ["gh"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (brew)",
            },
            {
              "id": "apt",
              "kind": "apt",
              "package": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (apt)",
            },
          ],
      },
  }
---
# GitHub CLI (`gh`) — 全面技能指南

版本：gh 2.66.1+  
认证方式：使用 `gh auth login` 或设置环境变量 `GH_TOKEN`  
当不在 Git 仓库目录内时，务必使用 `--repo OWNER/REPO`（或 `-R`）选项。

---

## 目录结构

1. [认证与配置](#1-authentication--config)  
2. [仓库](#2-repositories)  
3. [问题](#3-issues)  
4. [拉取请求](#4-pull-requests)  
5. [GitHub Actions（运行与工作流）](#5-github-actions-runs--workflows)  
6. [发布](#6-releases)  
7. [Gist](#7-gists)  
8. [搜索](#8-search)  
9. [标签](#9-labels)  
10. [秘密与变量](#10-secrets--variables)  
11. [缓存](#11-caches)  
12. [Projects V2](#12-projects-v2)  
13. [API（REST & GraphQL）](#13-api-rest--graphql)  
14. [扩展](#14-extensions)  
15. [代码空间](#15-codespaces)  
16. [Copilot](#16-copilot)  
17. [其他命令](#17-other-commands)  
18. [JSON 输出与格式化](#18-json-output--formatting)  
19. [环境变量](#19-environment-variables)  
20. [高级用法](#20-advanced-patterns)  
21. [技巧与注意事项](#21-tips--gotchas)  

---

## 1. 认证与配置

### 认证

**各功能所需的权限范围：**  
| 功能          | 所需权限范围            |
|-----------------|----------------------|
| 基本仓库/拉取请求/问题操作 | `repo`                |
| Gist            | `gist`                |
| 读取组织成员信息     | `read:org`              |
| Projects V2        | `project`                |
| 删除仓库         | `delete_repo`              |
| Actions/工作流        | `workflow`              |
| 读取用户信息       | `user`                |

### 配置

### Git 凭据设置

---

## 2. 仓库

### 创建仓库

### 克隆仓库

### 分支仓库

### 查看仓库信息

**仓库的 JSON 字段：**  
`archivedAt`, `assignableUsers`, `codeOfConduct`, `createdAt`, `defaultBranchRef`, `deleteBranchOnMerge`, `description`, `diskUsage`, `forkCount`, `hasDiscussionsEnabled`, `hasIssuesEnabled`, `hasProjectsEnabled`, `hasWikiEnabled`, `homepageUrl`, `id`, `isArchived`, `isEmpty`, `isFork`, `isPrivate`, `isTemplate`, `languages`, `latestRelease`, `licenseInfo`, `name`, `nameWithOwner`, `owner`, `parent`, `primaryLanguage`, `pullRequests`, `pushedAt`, `sshUrl`, `stargazerCount`, `updatedAt`, `url`, `visibility`, `watchers`

### 列出仓库

### 修改仓库信息

### 删除/归档仓库

### 重命名仓库

### 设置仓库默认值

### 同步仓库（分支与上游仓库）

---

## 3. 问题

### 创建问题

### 列出问题

**问题的 JSON 字段：**  
`assignees`, `author`, `body`, `closed`, `closedAt`, `comments`, `createdAt`, `id`, `isPinned`, `labels`, `milestone`, `number`, `projectCards`, `projectItems`, `reactionGroups`, `state`, `stateReason`, `title`, `updatedAt`, `url`

### 查看问题详情

### 修改问题

### 关闭/重新打开问题

### 评论问题

### 固定/取消固定问题

### 转移问题

### 锁定/解锁问题

### 开发相关操作（关联分支）

### 删除问题

---

## 4. 拉取请求

### 创建拉取请求

### 列出拉取请求

**拉取请求的 JSON 字段：**  
`additions`, `assignees`, `author`, `autoMergeRequest`, `baseRefName`, `body`, `changedFiles`, `closed`, `closedAt`, `comments`, `commits`, `createdAt`, `deletions`, `files`, `headRefName`, `headRefOid`, `id`, `isDraft`, `labels`, `latestReviews`, `maintainerCanModify`, `mergeCommit`, `mergeStateStatus`, `mergeable`, `mergedAt`, `mergedBy`, `milestone`, `number`, `projectItems`, `reviewDecision`, `reviewRequests`, `reviews`, `state`, `statusCheckRollup`, `title`, `.updated`, `url`

### 查看拉取请求详情

### 检查拉取请求的状态

### 提交拉取请求

### 查看差异

### 合并拉取请求

### 评审拉取请求

### 检查合并请求的状态

**检查的 JSON 字段：**  
`bucket`, `completedAt`, `description`, `event`, `link`, `name`, `startedAt`, `state`, `workflow`

### 修改检查结果

### 关闭/重新打开检查结果

### 将拉取请求设置为草稿状态

### 更新分支

### 评论检查结果

### 锁定/解锁检查结果

---

## 5. GitHub Actions（运行与工作流）

### 运行工作流

**工作流运行的 JSON 字段：**  
`attempt`, `conclusion`, `createdAt`, `databaseId`, `displayTitle`, `event`, `headBranch`, `headSha`, `name`, `number`, `startedAt`, `status`, `updatedAt`, `url`, `workflowDatabaseId`, `workflowName`

### 工作流

---

## 6. 发布

### 创建新发布

### 列出发布信息

### 下载发布内容

### 修改/上传/删除发布内容

---

## 7. Gist

---

## 8. 搜索

### 搜索仓库

### 搜索问题

### 搜索拉取请求

### 搜索提交记录

### 搜索代码

---

## 9. 标签

---

## 10. 秘密与变量

### 加密后的秘密信息

### 明文形式的变量

---

## 11. 缓存

---

## 12. Projects V2

**⚠️ 需要 `project` 权限范围：`gh auth refresh -s project`**

Projects V2 使用基于 GraphQL 的 ProjectsV2 API。GitHub CLI 提供了大部分操作命令，但某些高级字段的修改需要通过 `gh api graphql` 直接进行 GraphQL 请求。

### 列出 Projects V2 项目

### 创建 Projects V2 项目

### 查看 Projects V2 项目

### 修改 Projects V2 项目

### 关闭/重新打开 Projects V2 项目

### 删除 Projects V2 项目

### 将项目链接到仓库或团队

### 将项目标记为模板

### 修改 Projects V2 项目的字段

**字段数据类型：** `TEXT`, `SINGLE_SELECT`, `DATE`, `NUMBER`  
（迭代字段必须通过 Web UI 或 GraphQL 创建）

### 获取项目 ID（用于项目编辑）

**如何获取项目 ID：**

---

## 13. API（REST & GraphQL）

### REST API

### 占位符说明

特殊占位符 `{owner}`, `{repo}`, 和 `{branch}` 会自动从当前 Git 目录或 `GH_REPO` 中获取。

### 分页

### GraphQL API

### 常见的 GraphQL 模式

---

## 14. 扩展

---

## 15. 代码空间

---

## 16. Copilot

（需要 `gh-copilot` 扩展）

---

## 17. 其他命令

### 在浏览器中打开相关页面

### 查看跨仓库的状态信息

### 设置别名

### SSH 密钥/GPG 密钥

### 规则集

### 证明文件

### 组织管理

---

## 18. JSON 输出与格式化

大多数列出/查看命令支持 `--json`, `--jq`, 和 `--template` 标志。

### 基本 JSON 格式

### Go 模板格式化

### 模板函数

| 函数            | 描述                        |
|-----------------|---------------------------|
| `autocolor <style> <input>` | 根据终端环境为文本添加颜色       |
| `color <style> <input>` | 强制为文本设置颜色             |
| `join <sep> <list>` | 合并列表中的值                |
| `pluck <field> <list>` | 从列表中提取指定字段           |
| `tablerow <fields>...` | 对齐表格列                 |
| `tablerender` | 渲染表格数据                 |
| `timeago <time>` | 根据时间生成相对时间戳           |
| `timefmt <format> <time>` | 格式化时间字符串             |
| `truncate <length> <input>` | 截断输入文本                 |
| `hyperlink <url> <text>` | 生成终端可点击的超链接           |

---

## 19. 环境变量

| 变量            | 用途                          |
|-----------------|-------------------------|
| `GH_TOKEN` / `GITHUB_TOKEN` | github.com 的认证令牌（优先于存储的凭据） |
| `GH_ENTERPRISE_TOKEN` | GHES 的认证令牌                |
| `GH_HOST` | 默认的 GitHub 主机名                |
| `GH_REPO` | 默认仓库路径（格式为 `[HOST/]OWNER/REPO`） |
| `GH_EDITOR` | 用于编写文本的编辑器                 |
| `GH_browser` / `BROWSER` | 打开链接时使用的浏览器             |
| `GH_PAGER` | 终端分页工具（例如 `less`）             |
| `GH_DEBUG` | 启用详细输出（`1` 表示普通输出；`api` 表示 API 输出） |
| `GH_force_TTY` | 强制使用终端输出方式（数值表示列数或百分比） |
| `GH_PROMPT_DISABLED` | 禁用交互式提示                 |
| `GH_NO_UPDATE_NOTIFIER` | 禁用更新通知                 |
| `GH_CONFIG_DIR` | 自定义配置目录                 |
| `NO_COLOR` | 禁用颜色显示                 |
| `GLAMOUR_STYLE` | Markdown 渲染样式                 |

---

## 20. 高级用法

### 脚本编写最佳实践

### 批量操作

### 多个账户的使用

### 限制请求频率

### 复杂 API 操作

---

## 21. 技巧与注意事项

### 常见错误

1. **`--json` 参数中的字段名称可能与 API 中的字段名称不同。** 例如，拉取请求的文件字段使用 `files`（而非 `changed_files`），作者字段使用 `author.login`（而非 `user.login`）。始终执行 `gh <cmd> --json` 且不带参数，以查看所有可用字段。  
2. `gh run rerun --job` 需要 `databaseId`（而非 URL 的编号）。获取 `databaseId` 的方法：  
3. **Projects V2 操作需要 `project` 权限范围**。如果遇到权限错误，请检查权限设置。  
4. `gh repo delete` 命令需要 `delete_repo` 权限范围。  
5. 在某些 shell 环境中，需要使用引号引用 `owner`：`"{owner}"`。  

### 何时使用 `gh api` 与特定命令

| 使用特定命令的情况 | 使用 `gh api` 的情况            |
|-------------------|-------------------------|
| 命令存在且能满足需求       | 没有合适的 CLI 命令           |
| 需要交互式提示         | 需要更细粒度的控制           |
| 需要格式化的输出         | 需要原始 JSON 响应           |
| 执行简单 CRUD 操作       | 需要 GraphQL 查询           |
| 需要设置自定义请求头       | 需要分页功能                 |
| ------------------------- | -------------------------|
|                          |                           |

### 性能优化建议

- 使用 `--limit` 仅获取所需数据 |
- 使用 `--json` 仅获取特定字段（减少数据量） |
- 对于频繁访问且变化缓慢的数据，使用 `--cache` 与 `gh api` |
- 使用 `--paginate --slurp` 进行跨页面的数据聚合 |
- 在脚本中设置 `GH_PAGER=cat` 以禁用分页功能 |

### 错误代码

| 代码           | 含义                        |
|-----------------|-------------------------|
| 0            | 操作成功                     |
| 1            | 出现错误                     |
| 2            | 使用错误                     |
| 4            | 命令被取消                   |
| 8            | 检查任务待处理                 |

### 认证优先级

1. `GH_TOKEN` / `GITHUB_TOKEN` 环境变量  
2. `GH_ENTERPRISE_TOKEN`（用于 GHES 服务器）  
3. 通过 `gh auth login` 存储的凭据  
4. 仓库中的 `.env` 文件（仅当配置了该文件时）  

### 有用的命令行快捷方式

---