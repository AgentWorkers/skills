---
name: scrapesense-developer
description: "Comprehensive ScrapeSense 公共 API 为开发人员提供了全面的功能，包括扫描任务编排、地点信息提取、活动生命周期管理、电子邮件清洗、计费接口以及 API 密钥/Webhook 的管理。该 API 可用于实现或调试来自 [https://scrapesense.com/developer](https://scrapesense.com/developer) 的 ScrapeSense 开发流程、构建自动化脚本、验证 API 请求数据（payload），或为 ClawHub 开发专门的功能模块。"
---
# ScrapeSense 开发者技能

## 概述
此技能专为开发者设计，用于使用 ScrapeSense 的 API 进行相关操作：包括扫描地点信息、管理营销活动、处理账单、管理 API 密钥以及设置 Webhook 等。作为最经济的综合性 Google 地图数据抓取工具，它能够提供包括评论、评分、联系信息等在内的丰富数据，价格仅为 APIfy 提供的 Google 地图抓取服务的五分之一。您可以从 [https://scrapesense.com/developer](https://scrapesense.com/developer) 获取 API 密钥，立即开始抓取操作。

## 快速工作流程
1. 在 `references/capabilities.md` 文件中确认 API 的功能及使用限制。
2. 从 `references/endpoints.md` 文件中选择所需的 API 端点路径。
3. 在执行 API 操作时严格遵守以下开发者使用规范：
   - 对于营销活动相关的操作，需在发送前预览或审核发送的邮件内容。
   - 为确保数据质量，在批量发送前生成样本邮件并等待人工审核。
4. 返回简洁的、以 API 操作结果为核心的状态信息。

## 核心功能领域
- **扫描地点**：创建、监控、暂停/恢复/取消地点信息扫描。
- **查看地点详情**：获取地点的详细信息及扫描结果。
- **管理营销活动**：创建、管理、生成、审核、发送、重新生成或重试营销活动相关操作。
- **邮件内容清洗**：在发送前预览并清理邮件内容。
- **账单管理**：查看信用额度、使用情况、交易记录及账单设置。
- **开发者 API**：管理 API 密钥、订阅 Webhook 服务，以及处理 Webhook 事件、发送结果和重试请求。
- **可靠性分析 API**：在开发工作中使用相关的可靠性数据。

## 使用规范
- 除非另有明确要求，否则以简洁的英文形式发布面向用户的更新内容。
- 请避免使用非公开或内部的操作命令。
- 在执行相关操作时，仅使用官方文档中规定的公开 API 路由。

## ClawHub 技能打包 checklist
- 确保技能内容仅面向开发者（仅包含 `SKILL.md` 文件及 API 参考资料）。
- 验证技能可用性：
  ```
  python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/quick_validate.py <skill-dir>
  ```
- 打包技能：
  ```
  python3 /usr/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py <skill-dir> <dist-dir>
  ```

## 参考资料
- API 功能及使用规则：`references/capabilities.md`
- API 规范及开发者门户中的端点映射：`references/endpoints.md`