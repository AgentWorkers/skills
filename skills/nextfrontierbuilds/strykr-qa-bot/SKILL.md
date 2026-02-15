---
name: strykr-qa-bot
description: 基于人工智能的Strykr交易平台质量保证（QA）系统。为加密货币、股票、新闻以及AI聊天功能提供了预先构建的测试用例。该系统支持持续集成（CI）和持续部署（CD）流程，可与Cursor、Claude、ChatGPT、Copilot等工具协同使用，并支持Vibe-coding编码规范。
version: 0.1.2
author: NextFrontierBuilds
keywords: [strykr, prism, qa, testing, automation, web-qa-bot, clawdbot, moltbot, ai, ai-agent, vibe-coding, cursor, claude, chatgpt, copilot, github-copilot, crypto, trading, fintech, openclaw, ai-tools, developer-tools, devtools, typescript, llm]
---

# strykr-qa-bot

这是一个用于测试 Strykr（https://app.strykr.ai）的自动化问答（QA）工具。

## 功能概述

该工具主要负责对 Strykr 的 AI 金融仪表盘进行自动化测试，具体包括：
- 为所有页面提供预先构建的测试套件
- 验证信号卡（signal cards）的内容
- 检查 AI 回答的质量
- 监控 PRISM API 的运行状态
- 跟踪已知的系统问题（known issues）

## 使用场景

- 在 Strykr 部署完成后进行测试
- 进行回归测试（regression testing）
- 监控网站的健康状况
- 验证新功能的正确性

## 使用方法

### 运行所有测试
```bash
cd /path/to/strykr-qa-bot
npm test
```

### 运行特定测试套件
```bash
npm run test:homepage
npm run test:crypto
npm run test:stocks
npm run test:news
npm run test:events
npm run test:ai-chat
```

### 快速测试（Quick Smoke Test）
```bash
npm run smoke
```

### 程序化使用（Programmatic Usage）
```typescript
import { StrykrQABot } from 'strykr-qa-bot';

const qa = new StrykrQABot({
  baseUrl: 'https://app.strykr.ai'
});

// Run all suites
const results = await qa.runAll();

// Check specific assertions
await qa.expectSignalCard({ hasPrice: true, hasChart: true });
await qa.expectAIResponse({ minLength: 200 });

// Health check API
const health = await qa.checkPrismEndpoints();

// Generate report
const report = qa.generateReport();
```

## 测试套件详情

| 测试套件 | 测试内容 | 备注 |
|-------|-------|-------|
| 主页（Homepage） | 导航功能、小部件（widgets）、状态显示 | 测试入口点 |
| 加密信号（Crypto-Signals） | 过滤器（filters）、信号卡（signal cards）、操作功能（actions） | 存在模态窗口（modal window）相关问题 |
| 股票信号（Stock-Signals） | 资产过滤器（asset filters）、操作功能 | 支持股票/ETF/外汇交易 |
| 新闻（News） | 路由（routing）、分类（categories） | 存在直接访问 URL 的问题 |
| 事件（Events） | 事件筛选器（impact filters）、时间显示 | 存在直接访问 URL 的问题 |
| AI 聊天（AI-Chat） | 用户输入、AI 回答 | 回答质量验证 |

## 已知的系统问题

1. **details-modal-empty**（严重级别）：模态窗口打开但内容为空
2. **direct-url-blank-news**（中等级别）：通过直接导航访问新闻页面时，页面内容为空
3. **direct-url-blank-events**（中等级别）：通过直接导航访问事件页面时，页面内容为空
4. **events-widget-race-condition**（轻微级别）：事件相关的小部件加载存在间歇性问题

## 配置方法

请编辑 `strykr-qa.yaml` 文件以配置测试参数：
```yaml
baseUrl: https://app.strykr.ai
browser:
  headless: false
  timeout: 30000
```

## 依赖项

- [web-qa-bot](https://github.com/NextFrontierBuilds/web-qa-bot)（依赖库）

## 测试输出

测试结果包括：
- 通过/失败（Pass/Fail）/已知问题（Known Issues）的状态
- 每个测试步骤的截图
- 控制台错误日志
- 测试用时统计
- 以 Markdown 格式生成的测试报告

## 开发者

Next Frontier (@NextXFrontier)

## 链接

- [GitHub 仓库](https://github.com/NextFrontierBuilds/strykr-qa-bot)
- [Strykr 官网](https://app.strykr.ai)