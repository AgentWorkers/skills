# 释放说明生成器

该工具能够根据 Git 提交记录、Pull Request（PR）或简单的变更列表生成清晰、专业的发布说明。生成的变更日志格式符合用户实际阅读的习惯。

## 使用方法

只需告诉工具哪些内容发生了变化——可以粘贴 Git 提交信息、PR 标题，或者用通俗的语言描述功能变更，工具便会自动生成结构化的发布说明。

### 输入选项：

1. **Git diff/log**：粘贴 `git log --oneline v1.2.0..v1.3.0` 的输出结果
2. **PR 列表**：粘贴已合并的 PR 标题
3. **简单描述**：例如：“我们添加了暗黑模式，修复了登录漏洞，并停止了对 Python 3.7 的支持”

### 输出格式

```markdown
## v1.3.0 — 2026-02-13

### Added
- Dark mode across all pages (#142)

### Fixed
- Login redirect loop on Safari (#138)

### Breaking Changes
- Dropped Python 3.7 support — minimum is now 3.9

### Migration Guide
- Update your CI to use Python 3.9+ images
```

## 工作原理：

- 按变更类型对内容进行分类：新增（Added）、修改（Changed）、修复（Fixed）、弃用（Deprecated）、删除（Removed）、安全问题（Security）、破坏性变更（Breaking Changes）
- 遵循 [Keep a Changelog](https://keepachangelog.com/) 的格式规范
- 为破坏性变更提供迁移指南
- 为最终用户编写说明（除非另有要求）
- 除非特别要求，否则会忽略内部或重构相关的提交记录
- 在可能的情况下，会添加 PR/Issue 的编号
- 保持格式简洁易读（使用项目符号而非段落）

## 目标受众设置：

- 输入 “internal” 用于生成面向内部团队的说明；输入 “external” 用于生成面向客户的说明。默认设置为外部受众。

## 多种输出格式：

- **Changelog**：适合直接添加到 changelog 文件中的格式
- **Email**：可以直接粘贴到发布邮件中的格式
- **Slack**：适合在 #releases 通道中使用的紧凑格式
- **GitHub Release**：适合用于 GitHub 发布页面的 Markdown 格式
- **Tweet thread**：适合在社交媒体上分享的格式

## 使用建议：

- 每次冲刺结束后或每次部署之前运行该工具
- 可与将 Git 日志内容导出到文件的持续集成（CI）步骤配合使用
- 保持一个持续的 `CHANGELOG.md` 文件，并在每次发布时更新其中的内容

---

由 [AfrexAI](https://afrexai-cto.github.io/context-packs/) 开发——专为业务团队提供的 AI 框架（每套售价 47 美元）。请查看我们的 [AI 收入计算器](https://afrexai-cto.github.io/ai-revenue-calculator/)，了解自动化流程为您带来的成本。