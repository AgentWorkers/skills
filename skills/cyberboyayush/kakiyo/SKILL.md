---
name: kakiyo
description: Kakiyo.com提供的官方Kakiyo技能，用于通过Kakiyo MCP服务器管理LinkedIn自动化营销活动、潜在客户以及AI代理。适用于用户需要创建外联营销活动、添加潜在客户、监控运营效果、管理AI代理或自动化LinkedIn消息传递的场景。该技能包含42个工具，涵盖营销活动、潜在客户管理、代理管理、数据分析、工作空间、Webhook集成以及DNC（Direct Mail Campaign）管理等功能。
---

# Kakiyo LinkedIn Automation

这是 Kakiyo.com 提供的一项官方技能，用于通过 Kakiyo MCP 服务器控制 LinkedIn 外展活动及 AI 代理。

## 快速设置（代理辅助）

**检查是否已配置：**
```bash
mcporter config get kakiyo
```

如果未配置，提示用户：“我需要您的 Kakiyo API 密钥来完成设置。请从 https://app.kakiyo.com → 设置 → API 密钥 → 创建 API 密钥（40 个字符）获取。”

**用户提供 API 密钥后，运行以下命令：**
```bash
mcporter config add kakiyo https://api.kakiyo.com/mcp \
  --header "Authorization:Bearer USER_API_KEY"
```

请将 `USER_API_KEY` 替换为用户提供的密钥。

**验证设置：**
```bash
mcporter call kakiyo.verify_api_key --output json
```

## 可用工具（共 42 个）

### 代理（5 个工具）
用于管理 LinkedIn 自动化代理。

**listAgents** - 列出所有代理及其状态和配置
```bash
mcporter call kakiyo.list_agents --output json
```

**get_agent** - 获取代理的详细信息
```bash
mcporter call kakiyo.get_agent agentId:"agent_123" --output json
```

**update_agent** - 修改代理设置（工作时间、限制等）
```bash
mcporter call kakiyo.update_agent agentId:"agent_123" workingHours:'{"start":"09:00","end":"17:00"}' --output json
```

**pause_agent** - 暂停代理的运行
```bash
mcporter call kakiyo.pause_agent agentId:"agent_123" --output json
```

**resume_agent** - 重新启动暂停的代理
```bash
mcporter call kakiyo.resume_agent agentId:"agent_123" --output json
```

### 活动（6 个工具）
用于创建和管理外展活动。

**list_campaigns** - 列出所有活动的状态
```bash
mcporter call kakiyo.list_campaigns --output json
```

**get_campaign_stats** - 获取活动绩效指标
```bash
mcporter call kakiyo.get_campaign_stats campaignId:"camp_123" --output json
```

**create_campaign** - 创建新的活动
```bash
mcporter call kakiyo.create_campaign \
  name:"Tech Founders Outreach" \
  productId:"prod_123" \
  promptId:"prompt_456" \
  agentId:"agent_789" \
  --output json
```

**update_campaign** - 修改活动设置
```bash
mcporter call kakiyo.update_campaign campaignId:"camp_123" name:"New Name" --output json
```

**pause_campaign** - 停止活动
```bash
mcporter call kakiyo.pause_campaign campaignId:"camp_123" --output json
```

**resume_campaign** - 重新启动活动
```bash
mcporter call kakiyo.resume_campaign campaignId:"camp_123" --output json
```

### 潜在客户（9 个工具）
用于管理潜在客户和对话记录。

**list_prospects** - 列出带有基本过滤条件的潜在客户
```bash
mcporter call kakiyo.list_prospects limit:50 --output json
```

**get_prospect** - 获取潜在客户的详细信息及对话记录
```bash
mcporter call kakiyo.get_prospect prospectId:"pros_123" --output json
```

**add_prospect** - 将单个 LinkedIn 账户添加到活动中
```bash
mcporter call kakiyo.add_prospect \
  campaignId:"camp_123" \
  name:"John Doe" \
  url:"https://linkedin.com/in/johndoe" \
  --output json
```

**add_prospects_batch** - 一次性添加多个潜在客户
```bash
mcporter call kakiyo.add_prospects_batch \
  campaignId:"camp_123" \
  prospects:'[{"name":"Jane","url":"https://linkedin.com/in/jane"}]' \
  --output json
```

**search_prospects** - 使用过滤器进行高级搜索
```bash
mcporter call kakiyo.search_prospects status:replied limit:20 --output json
```

**list_campaign_prospects** - 获取活动中的所有潜在客户
```bash
mcporter call kakiyo.list_campaign_prospects campaignId:"camp_123" --output json
```

**pause_prospect** - 暂停对特定客户的联系
```bash
mcporter call kakiyo.pause_prospect prospectId:"pros_123" --output json
```

**resume_prospect** - 恢复与潜在客户的对话
```bash
mcporter call kakiyo.resume_prospect prospectId:"pros_123" --output json
```

**qualify_prospect** - 将潜在客户标记为合格客户
```bash
mcporter call kakiyo.qualify_prospect prospectId:"pros_123" --output json
```

### 分析（2 个工具）
用于监控绩效和指标。

**get_analytics_overview** - 查看所有活动的团队级指标
```bash
mcporter call kakiyo.get_analytics_overview --output json
```

**get_campaign_analytics** - 查看特定活动的详细指标
```bash
mcporter call kakiyo.get_campaign_analytics campaignId:"camp_123" --output json
```

### 产品（1 个工具）
用于查看活动相关的产品/服务信息。

**list_products** - 列出所有产品
```bash
mcporter call kakiyo.list_products --output json
```

### 提示模板（1 个工具）
用于查看 AI 消息模板。

**list_prompts** - 列出所有提示模板
```bash
mcporter call kakiyo.list_prompts --output json
```

### 模型（1 个工具）
用于查看可用的 AI 模型。

**list_models** - 查看用于生成消息的 AI 模型
```bash
mcporter call kakiyo.list_models --output json
```

### Webhook（5 个工具）
用于配置事件通知。

**list_webhooks** - 列出已配置的 Webhook
```bash
mcporter call kakiyo.list_webhooks --output json
```

**create_webhook** - 设置新的 Webhook
```bash
mcporter call kakiyo.create_webhook \
  url:"https://example.com/webhook" \
  events:'["prospect.replied","prospect.qualified"]' \
  --output json
```

**update_webhook** - 修改 Webhook 设置
```bash
mcporter call kakiyo.update_webhook webhookId:"wh_123" url:"https://new-url.com" --output json
```

**delete_webhook** - 删除 Webhook
```bash
mcporter call kakiyo.delete_webhook webhookId:"wh_123" --output json
```

**list_webhook_events** - 查看可用的事件类型
```bash
mcporter call kakiyo.list_webhook_events --output json
```

### 禁止联系（4 个工具）
用于管理黑名单。

**list_dnc** - 列出所有被阻止的 LinkedIn URL
```bash
mcporter call kakiyo.list_dnc --output json
```

**add_dnc** - 将账户添加到黑名单
```bash
mcporter call kakiyo.add_dnc url:"https://linkedin.com/in/blocked" --output json
```

**remove_dnc** - 从黑名单中移除账户
```bash
mcporter call kakiyo.remove_dnc url:"https://linkedin.com/in/unblock" --output json
```

**check_dnc** - 检查 URL 是否被阻止
```bash
mcporter call kakiyo.check_dnc url:"https://linkedin.com/in/check" --output json
```

### 工作空间（7 个工具）
用于管理客户的工作空间（适用于代理）。

**list_workspaces** - 列出所有客户的工作空间
```bash
mcporter call kakiyo.list_workspaces --output json
```

**create_workspace** - 创建新的客户工作空间
```bash
mcporter call kakiyo.create_workspace name:"Acme Corp" --output json
```

**delete_workspace** - 删除工作空间
```bash
mcporter call kakiyo.delete_workspace workspaceId:"ws_123" --output json
```

**invite_client** - 通过电子邮件邀请客户
```bash
mcporter call kakiyo.invite_client workspaceId:"ws_123" email:"client@example.com" --output json
```

**remove_client** - 从工作空间中移除客户
```bash
mcporter call kakiyo.remove_client workspaceId:"ws_123" userId:"user_123" --output json
```

**assign_agent_to_workspace** - 将代理分配给客户
```bash
mcporter call kakiyo.assign_agent_to_workspace workspaceId:"ws_123" agentId:"agent_123" --output json
```

**unassign_agent_from_workspace** - 从工作空间中移除代理
```bash
mcporter call kakiyo.unassign_agent_from_workspace workspaceId:"ws_123" agentId:"agent_123" --output json
```

### 认证（1 个工具）
用于验证连接是否正常。

**verify_api_key** - 检查 API 密钥是否有效
```bash
mcporter call kakiyo.verify_api_key --output json
```

## 常见使用场景

### 检查活动绩效
“我的 LinkedIn 活动表现如何？”
```bash
mcporter call kakiyo.get_analytics_overview --output json
```

### 查找已回复的潜在客户
“显示本周所有回复我的人”
```bash
mcporter call kakiyo.search_prospects status:replied --output json
```

### 将潜在客户添加到活动中
“将这些 LinkedIn 账户添加到我的 Tech Founders 活动中”
1. 获取活动 ID：`mcporter call kakiyo.list_campaigns`
2. 添加潜在客户：`mcporter call kakiyo.add_prospects_batch campaignId:"..." prospects:'[...']`

### 停止代理的运行（周末）
“在周末停止代理的运行”
```bash
mcporter call kakiyo.pause_agent agentId:"agent_123" --output json
```

### 代理：为新客户创建工作空间
“为新客户 Acme Corp 创建工作空间，并分配代理-1”
```bash
mcporter call kakiyo.create_workspace name:"Acme Corp" --output json
mcporter call kakiyo.assign_agent_to_workspace workspaceId:"ws_xxx" agentId:"agent_123" --output json
```

## 故障排除

**出现“服务器未找到”错误：**
使用正确的 API 密钥重新运行设置（请从 https://app.kakiyo.com 获取密钥）。

**检查配置：**
```bash
mcporter config get kakiyo
```

**测试连接：**
```bash
mcporter call kakiyo.verify_api_key --output json
```

**重新配置：**
```bash
mcporter config remove kakiyo
mcporter config add kakiyo https://api.kakiyo.com/mcp \
  --header "Authorization:Bearer YOUR_API_KEY"
```

## 最佳实践

1. **定期检查分析结果** - 监控回复率并调整消息内容
2. **使用黑名单** - 尊重用户的选择（避免向已选择退出联系的人发送消息）
3. **在假期期间暂停代理的运行** - 避免在非工作时间发送消息
4. **及时标记潜在客户为合格客户** - 将符合条件的潜在客户纳入跟踪范围
5. **设置 Webhook** - 为重要事件接收实时通知

## 额外资源

- 文档：https://docs.kakiyo.com
- 仪表板：https://app.kakiyo.com
- MCP 服务器详情：https://docs.kakiyo.com/mcp-server
- API 参考：https://docs.kakiyo.com/api-reference