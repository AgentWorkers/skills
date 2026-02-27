# HeyLead — 自动化的LinkedIn销售代表（SDR）

HeyLead是一款基于MCP框架开发的自动化LinkedIn销售代表工具，它能让您的OpenClaw代理自主执行LinkedIn销售任务，包括寻找潜在客户、发送个性化消息、跟进以及促成交易。

## 功能介绍

该工具将HeyLead作为MCP服务器集成到您的OpenClaw代理中，为您提供34种专业的LinkedIn销售工具：

- **理想客户画像生成（ICP Generation）**：利用RAG（Rule-Based Generation）技术生成包含客户痛点、顾虑、障碍以及LinkedIn搜索参数的详细画像。
- **活动管理（Campaign Management）**：创建、暂停、恢复、归档和比较销售活动。
- **个性化沟通（Personalized Outreach）**：发送与您的声音相匹配的邀请消息，让客户感觉像是与真人交流，而非机器操作。
- **多步骤沟通流程（Multi-Touch Sequences）**：包括跟进私信、互动引导（如评论、点赞、推荐）等。
- **回复处理（Reply Handling）**：自动分析客户情绪并回复，或安排会议。
- **数据分析（Analytics）**：提供销售漏斗报告、转化率数据、潜在客户活跃度分析以及投资回报率。
- **自动化调度（Autonomous Scheduling）**：24/7全天候自动安排邀请、跟进和回复任务。

## 设置

### 先决条件

- 已安装[uv](https://docs.astral.sh/uv/getting-started/installation/)工具（在Mac上使用`brew install uv`，或在Linux上使用`curl -LsSf https://astral.sh/uv/install.sh | sh`命令安装）。

### 配置

将以下配置添加到您的`openclaw.json`文件中：

```json
{
  "mcp": {
    "servers": [
      {
        "name": "heylead",
        "command": "uvx",
        "args": ["heylead"]
      }
    ]
  }
}
```

### 首次账户设置

添加MCP服务器后，告诉您的OpenClaw代理：

> “设置我的HeyLead账户”

系统会提供登录链接，您需要使用Google账户进行身份验证，连接LinkedIn账户，然后复制生成的Token并粘贴回配置文件中。整个过程大约需要1分钟，无需API密钥。

## 使用示例

```
"Find me CTOs at fintech startups in New York"
"Generate an ICP for AI SaaS founders"
"Create a campaign targeting VP of Sales at Series B startups"
"Send outreach to the campaign"
"Check my replies"
"How's my outreach doing?"
"Suggest next action"
"Enable the cloud scheduler"
```

## 常见工作流程

```
1. setup_profile(backend_jwt="...")        → Connect LinkedIn
2. generate_icp(target="CTOs fintech")     → Create buyer personas
3. create_campaign(target="...", icp_id="...") → Find prospects
4. toggle_scheduler(enabled=True)          → Autopilot outreach
5. check_replies() / show_status()         → Monitor pipeline
6. close_outreach(outcome="won")           → Track conversions
```

## 两种使用模式

- **自动模式（Autopilot）**：AI在规定的频率和工作时间内自动执行销售任务。
- **辅助模式（Copilot）**：在发送每条消息之前，由人工审核内容。

## 所有34种工具的详细功能

| 工具 | 功能描述 |
|------|-------------|
| `setup_profile` | 连接LinkedIn账户，分析写作风格，生成语音签名。 |
| `generate_icp` | 根据客户画像生成理想客户画像。 |
| `create_campaign` | 寻找潜在客户并创建销售活动。 |
| `generate_and_send` | 发送个性化的邀请消息。 |
| `send_followup` | 在客户接受邀请后发送跟进私信。 |
| `reply_to_prospect` | 根据客户情绪自动回复。 |
| `engage_prospect` | 与客户互动（评论、点赞、推荐）。 |
| `send_voice_memo` | 在LinkedIn上发送语音留言。 |
| `check_replies` | 监控收件箱，分析客户情绪，筛选重要潜在客户。 |
| `show_status` | 提供活动状态和统计信息。 |
| `campaign_report` | 提供详细分析和销售漏斗报告。 |
| `suggest_next_action` | 提供AI推荐的下一步行动建议。 |
| `approve_outreach` | 审批/编辑/跳过辅助模式下的消息。 |
| `show_conversation` | 查看与客户的完整对话记录。 |
| `edit_campaign` | 更新活动名称、模式、预约链接和设置。 |
| `pause_campaign` | 暂停当前活动。 |
| `resume_campaign` | 恢复暂停的活动。 |
| `archive_campaign` | 将活动标记为已完成。 |
| `delete_campaign` | 永久删除活动。 |
| `skip_prospect` | 删除不符合条件的潜在客户。 |
| `retry_failed` | 重试失败的沟通尝试。 |
| `emergency_stop` | 立即停止所有活动。 |
| `export_campaign` | 以表格/CSV/JSON格式导出数据。 |
| `compare_campaigns` | 对比多个销售活动。 |
| `close_outreach` | 记录销售结果（成功/失败/客户选择退出）。 |
| `toggle_scheduler` | 启用/禁用自动化调度功能。 |
| `scheduler_status` | 查看调度器状态和待处理任务。 |
| `create_post` | 生成并发布LinkedIn帖子。 |
| `brand_strategy` | 审查和优化个人LinkedIn品牌。 |
| `import_prospects` | 从CSV文件导入潜在客户信息。 |
| `crm_sync` | 将成功成交的客户信息同步到HubSpot CRM系统。 |
| `show_strategy` | 查看销售策略相关数据。 |
| `manage_watchlist` | 管理关键词监控列表。 |
| `showsignals` | 查看检测到的购买信号。

## 价格

| 计划 | 价格 | 限制 |
|------|-------|--------|
| **免费** | $0 | 每月50次邀请，1个活动，30次互动。 |
| **专业版** | $29/月 | 无限活动次数，支持5个LinkedIn账户，包含自动化调度功能。 |

## 隐私政策

- 客户信息和消息存储在本地SQLite数据库中。
- AI通话通过HeyLead的后端（Gemini 2.0 Flash）或您自己的服务器路由。
- HeyLead服务器上不存储任何消息或客户数据。

## 链接

- [PyPI](https://pypi.org/project/heylead/) | 官方Python包下载链接。
- [GitHub](https://github.com/D4umak/heylead) | 项目GitHub仓库。
- [Issue Tracker](https://github.com/D4umak/heylead/issues) | 问题反馈渠道。

## 许可证

HeyLead采用MIT许可证。