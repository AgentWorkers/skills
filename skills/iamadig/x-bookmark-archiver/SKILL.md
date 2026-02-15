# X 书签归档器

将您的 X（Twitter）书签归档为带有 AI 生成摘要的分类 markdown 文件。

## 概述

该工具使用 [bird CLI](https://github.com/steipete/bird) 获取您的 X 书签，根据 URL 模式对它们进行分类，然后利用 OpenAI 生成摘要，并将它们保存为结构化的 markdown 文件。

## 先决条件

1. **bird CLI** - 请从 [steipete/bird](https://github.com/steipete/bird) 安装。
2. **OpenAI API 密钥**（可选）- 为 AI 生成的摘要设置 `OPENAI_API_KEY`。
3. **Node.js 18+**

## 安装

```bash
# Ensure bird CLI is installed and authenticated
bird --version

# Set OpenAI API key (optional, for AI summaries)
export OPENAI_API_KEY="sk-..."
```

## 命令

### `run` - 完整流程

获取新书签并处理它们：

```bash
node skills/x-bookmark-archiver/scripts/run.cjs
```

### `run --force` - 仅处理现有书签

跳过获取步骤，仅处理待处理的书签：

```bash
node skills/x-bookmark-archiver/scripts/run.cjs --force
```

### `fetch` - 仅下载书签

```bash
node skills/x-bookmark-archiver/scripts/fetch.cjs
```

### `process` - 仅归档待处理的书签

```bash
node skills/x-bookmark-archiver/scripts/process.cjs
```

## 分类规则

书签会根据 URL 模式自动分类：

| 分类 | 域名 |
|----------|---------|
| **工具** | github.com, gitlab.com, github.io, huggingface.co, replicate.com, vercel.com, npmjs.com, pypi.org |
| **文章** | medium.com, substack.com, dev.to, hashnode.dev, x.com/i/article, blog.*, towardsdatascience.com |
| **视频** | youtube.com, youtu.be, vimeo.com, twitch.tv |
| **研究** | arxiv.org, paperswithcode.com, semanticscholar.org, researchgate.net, dl.acm.org, ieee.org |
| **新闻** | techcrunch.com, theverge.com, hn.algolia.com, news.ycombinator.com, wired.com, arstechnica.com |
| **书签** | *用于未匹配的 URL 的默认分类* |

## 输出位置

Markdown 文件将保存在 **OpenClaw 工作区** 中：

**旧版本的安装路径：**
```
~/clawd/X-knowledge/
```

**新版本的安装路径：**
```
~/.openclaw/workspace/X-knowledge/
```

**使用配置文件 (`OPENCLAW_PROFILE=prod`) 时：**
```
~/.openclaw/workspace-prod/X-knowledge/
```

**通过环境变量覆盖设置：**
```bash
export OPENCLAW_WORKSPACE=/custom/path
node skills/x-bookmark-archiver/scripts/run.cjs
# Creates: /custom/path/X-knowledge/
```

## 输出结构

```
~/.openclaw/workspace/X-knowledge/
├── tools/
│   ├── awesome-ai-project.md
│   └── useful-cli-tool.md
├── articles/
│   ├── how-to-build-x.md
│   └── ml-best-practices.md
├── videos/
│   └── conference-talk.md
├── research/
│   └── attention-is-all-you-need.md
├── news/
│   └── latest-tech-announcement.md
└── bookmarks/
    └── misc-link.md
```

## Markdown 模板

每个归档的书签都会生成一个包含前置内容的 markdown 文件：

```markdown
---
title: "Awesome AI Project"
type: tool
date_archived: 2026-01-31
source_tweet: https://x.com/i/web/status/1234567890
link: https://github.com/user/repo
tags: ["ai", "machine-learning", "github"]
---

This project implements a novel approach to... (AI-generated summary)
```

## 状态管理

状态文件用于跟踪处理进度：

```
/root/clawd/.state/
├── x-bookmark-pending.json     # Bookmarks waiting to be processed
└── x-bookmark-processed.json   # IDs of already-archived bookmarks
```

## 环境变量

| 变量 | 是否必需 | 描述 |
|----------|----------|-------------|
| `OPENAI_API_KEY` | 否 | 用于 AI 生成摘要的 API 密钥 |

## 工作流程

1. **获取**：从 X 下载最新的 50 个书签。
2. **过滤**：移除已处理过的书签。
3. **解析**：解析 t.co 缩略链接。
4. **分类**：根据域名分配分类。
5. **丰富内容**：生成标题、摘要和标签（使用 AI 生成或使用默认值）。
6. **写入**：将书签保存到 `X-knowledge/{分类}/` 目录中。
7. **跟踪**：更新已处理的书签 ID，并清除待处理的书签。

## 自定义设置

### 添加分类

编辑 `scripts/lib/categorize.cjs` 文件：

```javascript
const CATEGORIES = {
  tools: ['github.com', '...'],
  your_category: ['example.com', '...'],
  // ...
};
```

### 更改输出目录

编辑 `scripts/process.cjs` 文件：

```javascript
const KNOWLEDGE_DIR = 'your-directory-name';
```

### 使用其他 AI 提供商

修改 `scripts/process.cjs` 中的 `generateMetadata()` 函数以使用您喜欢的 API。

## 测试

运行测试套件：

```bash
# Run all tests
cd skills/x-bookmark-archiver/tests
node test-all.cjs

# Run individual test suites
node lib/categorize.test.cjs
node lib/state.test.cjs
node integration.test.cjs
```

### 测试覆盖范围

- **单元测试**：`categorize.js`（21 个测试）- URL 模式匹配
- **单元测试**：`state.js`（9 个测试）- JSON 读写操作
- **集成测试**（12 个测试）- 使用模拟数据的完整流程

### 手动测试

如果没有 bird CLI，您可以使用模拟数据进行测试：

```bash
# Create mock pending data
cat > /tmp/test-pending.json << 'EOF'
[
  {
    "id": "test123",
    "url": "https://github.com/test/repo",
    "text": "Test bookmark"
  }
]
EOF

# Copy to state directory and process
mkdir -p /root/clawd/.state
cp /tmp/test-pending.json /root/clawd/.state/x-bookmark-pending.json
node skills/x-bookmark-archiver/scripts/process.cjs
```

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| `bird CLI 未找到` | 从 GitHub 的发布版本中安装 bird CLI。|
| 未获取到书签** | 确保您已在 bird 中登录到 X 账户。|
| 无法生成 AI 摘要** | 检查是否设置了 `OPENAI_API_KEY`。|
| t.co 链接无法解析** | 可能是网络问题或超时问题；此时会使用原始 URL。|

## 文件结构

```
skills/x-bookmark-archiver/
├── SKILL.md
├── scripts/
│   ├── fetch.cjs          # Download bookmarks from X (CommonJS)
│   ├── process.cjs        # Generate markdown files (CommonJS)
│   ├── run.cjs            # Orchestrate fetch → process (CommonJS)
│   └── lib/
│       ├── categorize.cjs # URL → category mapping (CommonJS)
│       └── state.cjs      # JSON state management (CommonJS)
└── tests/
    ├── test-all.cjs
    ├── lib/
    │   ├── categorize.test.cjs
│   │   └── state.test.cjs
    ├── integration.test.cjs
    └── fixtures/
        └── sample-bookmarks.json
```

## 许可证

MIT