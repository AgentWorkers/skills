# SEO技能包

> 本文档提供了针对npm包、GitHub仓库以及AI代理技能的SEO最佳实践，旨在提升这些内容的可发现性（即被用户或搜索引擎找到的概率）。

**作者:** Next Frontier  
**版本:** 1.0.0  
**标签:** seo, npm, github, publishing, marketing, discoverability, packages

---

## 使用场景

以下情况下可使用本文档：
- 发布新的npm包  
- 创建GitHub仓库  
- 将技能提交至ClawdHub  
- 更新包的描述文件（README.md）以提高可发现性  
- 审查现有包的SEO优化情况  

---

## 热门关键词（2026年）

在文档中务必包含以下关键词：

```
AI, automation, vibe coding, cursor, claude, gpt, copilot, agent,
autonomous, mcp, langchain, llm, testing, devtools, cli, typescript,
python, react, nextjs, api, sdk, tool, framework, openai, anthropic,
coding agent, ai assistant, developer tools, productivity
```

**专业提示：** 在发布前，可查看X/Twitter上的科技领域热门趋势，以获取最新的关键词。  

---

## npm包

### package.json

```json
{
  "name": "descriptive-seo-friendly-name",
  "description": "Clear value prop with keywords. AI-powered X for Y. Works with Cursor, Claude, GPT.",
  "keywords": [
    "ai",
    "automation", 
    "claude",
    "gpt",
    "cursor",
    "vibe-coding",
    "agent",
    "cli",
    "devtools",
    "mcp",
    "langchain",
    "copilot",
    "testing",
    "typescript",
    "openai",
    "anthropic"
  ],
  "repository": {
    "type": "git",
    "url": "https://github.com/org/repo"
  },
  "homepage": "https://github.com/org/repo#readme",
  "bugs": {
    "url": "https://github.com/org/repo/issues"
  }
}
```

**规则：**
- 至少包含10-15个关键词  
- 描述字段长度不超过200个字符，但应包含丰富的关键词  
- 必须提供仓库地址、主页链接以及Bug报告的链接  
- 包名应具有可搜索性（避免使用晦涩难懂的名称）  

### README.md结构

```markdown
# package-name

[![npm version](https://img.shields.io/npm/v/package-name.svg)](https://npmjs.com/package/package-name)
[![npm downloads](https://img.shields.io/npm/dm/package-name.svg)](https://npmjs.com/package/package-name)
[![license](https://img.shields.io/npm/l/package-name.svg)](LICENSE)

> One-line description with keywords. AI-powered X for Y.

## Works With

- 🤖 Claude / Claude Code
- 🔵 Cursor
- 💚 GPT / ChatGPT
- ⚡ Copilot
- 🧩 MCP servers

## Install

\`\`\`bash
npm install package-name
\`\`\`

## Quick Start

\`\`\`typescript
// Minimal working example
\`\`\`

## Features

- ✅ Feature 1 with keyword
- ✅ Feature 2 with keyword
- ✅ Feature 3 with keyword

## API / Usage

[Details...]

## License

MIT
```

**关键元素：**
- 文档顶部应放置徽章  
- 使用包含关键词的标题或标语  
- “兼容性”部分（展示该技能与其他工具的兼容性）  
- 安装命令需置于文档显眼位置  
- 提供快速入门示例代码  
- 列出功能，并使用复选标记进行标注  

---

## GitHub仓库

### 描述（不超过350个字符）

格式要求：
```
[What it does]. [Key benefit]. [Compatibility]. [Call to action].
```

示例：
```
AI-powered PDF generator for legal docs and pitch decks. Creates SAFEs, NDAs, term sheets from prompts. Works with Claude, Cursor, GPT. No templates needed.

Real-time financial data API for AI agents. Stocks, crypto, forex, ETFs in one unified feed. 120+ endpoints. Alternative to Alpha Vantage.

Automated QA for web apps using AI. Smoke tests, accessibility, visual regression. Drop-in CI/CD testing. Works with Playwright.
```

### 主题标签（GitHub标签）

添加10-20个相关主题标签：
```
ai, automation, claude, gpt, cursor, typescript, cli, devtools, 
agent, testing, api, sdk, mcp, langchain, openai, anthropic,
developer-tools, productivity, automation-tools
```

### README.md

README.md的内容应与npm包的README.md保持一致！  

---

## ClawdHub技能

### SKILL.md描述

```markdown
# Skill Name

> One-line with keywords. [What it does] for AI agents. Works with Clawdbot, Claude, Cursor.

**Author:** Your Name
**Version:** X.Y.Z
**Tags:** tag1, tag2, tag3, ai, agent, automation
```

### 标签

请为该技能添加5-10个合适的标签：
```
ai, agent, automation, claude, cursor, mcp, cli, [domain-specific tags]
```

---

## 同步检查清单

以下三个部分的描述必须保持一致：
| 字段 | npm | GitHub | ClawdHub |
|-------|-----|--------|----------|
| 名称 | package.json中的`name`字段 | GitHub仓库名称 | SKILL.md文件名称 |
| 描述 | package.json中的`description`字段 | GitHub仓库的描述 | SKILL.md文件中的描述 |
| 关键词 | package.json中的`keywords`字段 | GitHub仓库的主题标签 | SKILL.md文件中的标签 |
| README.md | GitHub仓库的README.md文件 | SKILL.md文件中的README.md内容 |

---

## 发布前的检查清单

每次发布前，请确保以下内容无误：
- 包名具有描述性且可搜索  
- 描述字段包含有价值的信息及3-5个关键词  
- package.json中包含10-15个关键词  
- README.md中包含徽章（版本信息、下载量、许可证信息）  
- README.md中包含“兼容性”部分  
- 安装命令位于文档显眼位置  
- README.md中提供快速入门示例代码  
- GitHub仓库中添加了10-20个相关主题标签  
- GitHub仓库的描述与package.json中的信息一致  
- 查看X/Twitter上的科技领域热门趋势，以获取最新的关键词  
- 所有平台的描述内容保持同步  

---

## 徽章生成工具

可以使用shields.io来生成徽章：
```markdown
[![npm version](https://img.shields.io/npm/v/PACKAGE.svg)](https://npmjs.com/package/PACKAGE)
[![npm downloads](https://img.shields.io/npm/dm/PACKAGE.svg)](https://npmjs.com/package/PACKAGE)
[![license](https://img.shields.io/npm/l/PACKAGE.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/ORG/REPO.svg)](https://github.com/ORG/REPO)
```

---

## 应避免的错误做法：
❌ 使用晦涩难懂或难以搜索的名称  
❌ 描述中不包含关键词  
❌ 关键词数组为空或过于简略  
❌ README.md中未添加徽章  
❌ 未设置“兼容性”部分  
❌ npm、GitHub和ClawdHub上的描述信息不一致  
❌ 未提供快速入门示例代码  
❌ 安装命令前的内容过于冗长  

---

## 示例（优秀实践）  
**ai-pdf-builder**  
```
AI-powered PDF generator for legal docs, pitch decks, and reports. 
Creates SAFEs, NDAs, term sheets, whitepapers from prompts. 
Works with Claude, GPT, Cursor, and AI coding agents. YC-style docs in seconds.
```  
**web-qa-bot**  
```
Automated QA for web apps using AI. Smoke tests, accessibility checks, 
visual regression. Drop-in replacement for manual QA. 
Works with Playwright, Cursor, Claude. QA without the QA team.
```  

---

## 快速参考

| 元素        | 要求              |
|-------------|-----------------|
| 关键词        | 10-15个             |
| 描述        | 100-200个字符          |
| 主题标签      | 10-20个             |
| 徽章数量      | 3-5个              |
| README部分数量 | 5-7个              |