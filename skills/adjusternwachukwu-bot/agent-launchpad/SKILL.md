---
name: agent-launchpad
description: 根据自然语言描述生成完整、可部署的AI代理技能包。提供6种模板（监控器、数据抓取器、分析师、交易员、助手、Webhook），并支持通过SkillPay进行货币化。适用于用户创建新代理、从零开始构建技能、搭建代理项目或生成可部署的技能包的场景。
---
# 代理启动平台（Agent Launchpad）

描述您的需求 → 获取完整的代理技能包 → 将其发布到 ClawHub。

## 生成代理（Generate an Agent）

```bash
curl -X POST https://launchpad.gpupulse.dev/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"description": "Monitor ETH price and alert below $2000", "price_credits": 5}'
```

系统会生成包含完整 SKILL.md 文件以及集成 SkillPay 支付功能的脚本。

## 可用模板（Available Templates）：
- **monitor**：监控数据，根据条件触发警报
- **scraper**：抓取网页数据
- **analyst**：生成报告并提供分析见解
- **trader**：提供模拟交易策略
- **assistant**：负责处理领域内的问答
- **webhook**：作为事件监听器使用

## 工作流程（Pipeline）：
1. 通过 `/generate` API 提交您的需求描述
2. 查看生成的文件
3. 使用 `clawhub publish` 命令将文件发布到 ClawHub

## 后期添加支付功能（Add Payments Later）

```bash
curl -X POST /api/v1/monetize -H "Content-Type: application/json" \
  -d '{"agent_id": "ag_...", "price_credits": 10}'
```