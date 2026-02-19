---
name: product-changelog
description: "产品变更日志和发布说明，这些内容是用户实际会阅读的。涵盖内容分类、面向用户的语言表述、视觉呈现方式以及产品的发布方式。适用于：发布说明、变更日志、产品更新、功能公告、版本管理。相关触发事件包括：变更日志更新、发布说明发布、产品更新通知、版本更新信息、新功能公告、产品变更记录、更新日志、发布公告、版本发布通知等。"
allowed-tools: Bash(infsh *)
---
# 产品更新日志

通过 [inference.sh](https://inference.sh) 命令行工具，编写用户会阅读并关注的更新日志和发布说明。

## 快速入门

```bash
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a feature announcement visual
infsh app run falai/flux-dev-lora --input '{
  "prompt": "clean product UI screenshot mockup, modern dashboard interface showing a new analytics chart feature, light mode, minimal design, professional SaaS product",
  "width": 1248,
  "height": 832
}'
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统/架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需提升权限或后台进程。也可通过 [手动安装与验证](https://dist.inference.sh/cli/checksums.txt) 进行操作。

## 更新日志条目的格式

### 一个优秀更新日志条目的构成

```markdown
### New: Bulk Export for Reports 📊

You can now export up to 10,000 rows at once from any report view.
Select your rows, click Export, and choose CSV or Excel format.

Previously limited to 500 rows per export.

![Bulk export button in the reports toolbar](screenshot.png)
```

**结构：** 类别标签 -> 面向用户的标题 -> 用户现在可以做什么 -> 实现方式 -> 发生了哪些变化 -> 可视化展示

### 面向用户的语言风格

```
❌ Internal language:
"Implemented batch processing queue for the export service"
"Refactored the ReportExporter class to support pagination"
"Fixed bug in CSV serialization (PR #4521)"

✅ User-facing language:
"You can now export up to 10,000 rows at once from any report"
"Reports now load 3x faster when filtering large datasets"
"Fixed an issue where exported CSV files had missing columns"
```

**规则：**
- 描述用户可以“做什么”，而不是您“构建了什么”
- 以 “您现在可以...” 或 “修复了以下问题...” 开头
- 仅说明好处，而不仅仅是实现机制
- 使用现在时态

## 分类

### 标准分类

| 分类 | 颜色 | 图标 | 适用场景 |
|----------|-------|------|---------|
| **新增功能** | 绿色 | ✨ 或 🆕 | 完全新的功能或能力 |
| **功能改进** | 蓝色 | ⚡ 或 🔧 | 对现有功能的优化 |
| **问题修复** | 黄色/橙色 | 🐛 或 🔨 | 错误修复 |
| **功能移除** | 红色 | 🗑️ 或 ⚠️ | 已弃用或移除的功能 |
| **安全修复** | 紫色 | 🔒 | 安全补丁 |

### 分类规则

- **新增功能**：用户之前完全无法使用的功能 |
- **功能改进**：用户原本可以使用该功能，现在使用起来更好、更快或更便捷 |
- **问题修复**：之前存在问题的功能，现在已修复 |
- **请避免使用“更新”一词”——这个术语没有实际意义。需要明确是改进了还是修复了问题？ |

## 版本编号

### 语义版本控制（SemVer）

```
MAJOR.MINOR.PATCH
  3   .  2  .  1
```

| 组件 | 版本更新时机 | 例子 |
|-----------|---------------|---------|
| **重大版本** | 引起重大变化的更新、重大设计变更 | 2.0.0 -> 3.0.0 |
| **次要版本** | 新功能的添加、向后兼容 | 3.1.0 -> 3.2.0 |
| **补丁版本** | 修复错误、小规模改进 | 3.2.0 -> 3.2.1 |

### 基于日期的版本控制

```
2026-02-08  or  2026.02.08  or  February 8, 2026
```

适用于持续部署的 SaaS 产品。

## 更新日志页面的结构

```markdown
# Changelog

## February 8, 2026

### New
- **Bulk Export for Reports** — Export up to 10,000 rows at once. [Learn more →](link)
- **Dark Mode** — Toggle dark mode from Settings > Appearance.

### Improved
- **Dashboard Loading** — Dashboards now load 3x faster on large datasets.
- **Search** — Search results now include archived items.

### Fixed
- Fixed an issue where exported CSV files had missing column headers.
- Fixed a bug where the date picker showed incorrect timezone.

---

## February 1, 2026

### New
- **API Webhooks** — Get notified when events happen in your account.

### Fixed
- Fixed an issue where email notifications were delayed by up to 2 hours.
```

## 可视化更新日志

### 何时添加可视化内容

| 更新类型 | 可视化展示方式 |
|-------------|--------|
| 新用户界面功能 | 新功能的截图 |
| 用户界面重新设计 | 设计前后对比图 |
| 新工作流程 | 分步截图或短视频 |
| 性能提升 | 显示性能提升的图表 |
| 复杂功能 | 动态 GIF 或视频演示 |

### 生成可视化内容

```bash
# Feature screenshot (if you have the app running, use agent browser)
infsh app run infsh/agent-browser --input '{
  "url": "https://your-app.com/new-feature",
  "action": "screenshot"
}'

# Before/after comparison
infsh app run infsh/stitch-images --input '{
  "images": ["before-screenshot.png", "after-screenshot.png"],
  "direction": "horizontal"
}'

# Annotated screenshot with callout
infsh app run bytedance/seededit-3-0-i2i --input '{
  "prompt": "add a red circle highlight around the export button in the top right area",
  "image": "screenshot.png"
}'

# Feature announcement banner
infsh app run falai/flux-dev-lora --input '{
  "prompt": "clean modern product announcement banner, gradient blue to purple background, abstract geometric shapes, professional SaaS aesthetic, wide format",
  "width": 1248,
  "height": 832
}'
```

## 引起重大变化的更新

引起重大变化的更新需要特别处理：

```markdown
### ⚠️ Breaking: API v2 Endpoints Deprecated

**What changed:** API v1 endpoints will stop working on March 15, 2026.

**What you need to do:**
1. Update your API calls to use v2 endpoints ([migration guide →](link))
2. Update authentication to use Bearer tokens instead of API keys
3. Test your integration before March 15

**Timeline:**
- Now: v2 endpoints available, v1 still works
- March 1: v1 returns deprecation warnings
- March 15: v1 stops working

If you need help migrating, contact support@company.com.
```

## 分发渠道

| 分发渠道 | 发布形式 | 发布时机 |
|---------|--------|------|
| **更新日志页面** | 所有更新内容的完整详情 | 每次发布时 |
| **应用内通知** | 1-2 行的简要总结 | 新功能、重大变化 |
| **电子邮件** | 精选的重点内容、可视化展示 | 重大版本更新（每月/每季度） |
| **博客文章** | 深入解析 | 重要版本发布 |
| **社交媒体** | 单个功能的亮点展示 | 显著的功能更新 |
| **Slack/Discord** | 简短的公告 | 如果有社区的话 |

### 社交媒体发布格式

```
🆕 New in [Product]: [Feature Name]

[1-2 sentence description of what you can now do]

[Screenshot or demo video]

Try it now → [link]
```

## 编写技巧

### 应该做的：
- 将相关的更新内容放在一起
- 首先介绍最重要或用户需求最多的更新
- 对于复杂功能，提供相应的文档链接
- 明确指出是谁提出的请求（例如：“根据用户需求...”）
- 为引起重大变化的更新提供迁移指南
- 为每条更新内容标注日期

### 不应该做的：
- 不要笼统地写“各种错误修复”——应列出具体的修复内容
- 不要包含内部参考信息（如 PR 编号、工单 ID、分支名称）
- 不要在不说明具体改进内容的情况下使用“更新了[某功能]”
- 不要列出用户不关心的更新（如依赖关系的调整、内部重构）
- 不要将多次提交的内容合并到一条更新日志中

## 更新日志的发布频率

| 产品类型 | 发布频率 | 备注 |
|-------------|-----------|-------|
| SaaS（持续部署） | 每周批量发布 | 将一周内的更新内容汇总 |
| SaaS（新增功能） | 每个新功能发布时 | 附带博客文章 |
| 分版本软件 | 每个版本发布时 | 与语义版本号对应 |
| API | 每个版本更新时 | 包含弃用通知 | 提供迁移指南 |
| 移动应用 | 每次应用商店更新时 | 与应用商店的“新增内容”部分一致 |

## 常见错误

| 错误 | 问题 | 解决方法 |
|---------|---------|-----|
| 使用开发者术语 | 用户难以理解 | 用用户能理解的语言描述 |
| 只写“错误修复和功能改进” | 没有提供具体信息 | 列出具体的修复内容 |
| 不标注日期 | 用户无法判断哪些内容是新的 | 为每条更新内容标注日期 |
| 没有可视化内容 | 用户会忽略文本 | 为重要功能提供截图 |
| 重要更新被埋没在日志中 | 用户发现得太晚 | 使用醒目的警告提示 + 时间线 |
| 将提交日志直接作为更新日志使用 | 内容混乱、难以理解 | 对更新日志进行整理和重写 |

## 相关技能

```bash
npx skills add inference-sh/skills@ai-image-generation
npx skills add inference-sh/skills@prompt-engineering
```

查看所有应用：`infsh app list`