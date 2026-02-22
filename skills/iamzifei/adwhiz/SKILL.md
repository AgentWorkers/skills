---
name: adwhiz
description: 通过您的人工智能编程工具来管理 Google 广告活动。提供了 44 种 MCP 工具，支持使用自然语言来审核、创建和优化 Google 广告账户。
metadata:
  openclaw:
    primaryEnv: "ADWHIZ_API_KEY"
    requires:
      bins:
        - node
    install:
      - kind: node
        package: "@adwhiz/mcp-server"
    homepage: "https://adwhiz.ai"
---
# AdWhiz — Google Ads MCP 服务器

AdWhiz 是一个远程 MCP（管理控制）服务器，它允许您的 AI 工具直接访问 Google Ads API。它提供了 **44 个工具**，涵盖 5 个类别，让您能够使用简单的英语来审计、创建和管理 Google Ads 广告活动。

## 工具类别

### 账户（2 个工具）
- `list_accounts` — 列出所有可访问的 Google Ads 账户
- `get_account_info` — 获取账户详情（货币、时区、优化得分）

### 读取（14 个工具）
- `list_campaigns` — 列出广告活动的状态、类型和预算
- `get_campaign_performance` — 获取广告活动指标：成本、点击量、转化率、点击成本（CTR）、每次点击成本（CPA）、投资回报率（ROAS）
- `list_ad_groups` — 列出广告组及其出价（按广告活动过滤）
- `list_ads` — 列出广告的标题、描述和最终链接
- `list_keywords` — 列出关键词及其匹配类型、出价和质量得分
- `get_search_terms` — 获取搜索词报告（实际触发广告的查询词）
- `list_negative_keywords` — 获取广告活动、广告组或账户级别的否定关键词
- `list_assets` — 列出站点链接、呼叫out（callout）和结构化片段
- `list_conversion_actions` — 获取转化动作的详细信息（状态、类型、类别）
- `list_budgets` — 获取与广告活动关联的预算
- `list_bidding_strategies` — 创建组合出价策略
- `list_audience_segments` — 获取受众定位标准
- `list_user_lists` — 获取用于再营销/定位的受众列表
- `get_operation_log` — 查看通过 AdWhiz 执行的最新操作

### 编写（25 个工具）
- `create_campaign` — 创建搜索广告活动、展示广告活动、PMax 广告活动或视频广告活动（初始状态为“暂停”）
- `update_campaign` — 更新广告活动名称
- `set_campaign_status` — 暂停、启用或删除广告活动
- `create_ad_group` — 在广告活动中创建广告组
- `update_ad_group` — 更新广告组名称或 CPC 出价
- `set_ad_group_status` — 暂停、启用或删除广告组
- `create_responsive_search_ad` — 创建响应式搜索广告（初始状态为“暂停”）
- `set_ad_status` — 暂停、启用或删除广告
- `add_keywords` — 添加关键词及其匹配类型和出价
- `update_keyword_bid` — 更改关键词的 CPC 出价
- `set_keyword_status` — 暂停、启用或删除关键词
- `add_negative_keyword` — 在广告活动或广告组级别添加否定关键词
- `remove_negative_keyword` — 删除否定关键词
- `create_shared_negative_list` — 创建共享否定关键词列表
- `add_to_shared_list` — 将关键词添加到共享否定列表
- `attach_shared_list` — 将共享列表关联到广告活动
- `create_sitelink` — 创建站点链接资源
- `create_callout` — 创建呼叫out 资源
- `link_asset_to_campaign` — 将资源关联到广告活动
- `create_conversion_action` — 创建转化跟踪动作
- `update_conversion_action` — 更新转化跟踪动作的名称或状态
- `create_budget` — 创建广告活动预算
- `update_budget` — 更新预算金额或名称
- `create_bidding_strategy` — 创建组合出价策略
- `add_audience_to_campaign` — 为广告活动添加受众定位

### 审计（2 个工具）
- `run_mini_audit` — 快速审计：浪费的支出、最佳/最差的 CPA、预计节省额
- `run_full_audit` — 全面审计：广告活动、关键词、搜索词、问题及建议

### 查询（1 个工具）
- `run_gaql_query` — 执行任何只读的 GAQL 查询（最多 1,000 行）

## MCP 服务器配置

### 选项 A：标准输入输出（通过 npx）

将以下内容添加到您的 `openclaw.json` 文件中：

```json
{
  "mcpServers": {
    "adwhiz": {
      "command": "npx",
      "args": ["-y", "@adwhiz/mcp-server"],
      "env": {
        "ADWHIZ_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### 选项 B：HTTP 传输（远程服务器）

```json
{
  "mcpServers": {
    "adwhiz": {
      "transport": "http",
      "url": "https://mcp.adwhiz.ai/mcp",
      "headers": {
        "Authorization": "Bearer your-api-key-here"
      }
    }
  }
}
```

## 快速安装

```bash
clawhub install adwhiz
```

## 示例命令

- “审计我的 Google Ads 账户，并显示浪费最多的 5 个方面”
- “暂停所有 CPA 超过 150 美元的广告活动”
- “将以下否定关键词添加到我的搜索广告活动中：[列表]”
- “创建一个新的搜索广告活动，目标受众为纽约的律师，预算为每天 100 美元”
- “显示浪费资金的搜索词，并建议添加哪些否定关键词”
- “我这个月的平均质量得分是多少？”

## 安全默认设置

- 新创建的广告活动和广告始终处于“暂停”状态
- 所有操作都会被记录在操作日志中
- 只读工具永远不会修改您的账户
- 编写工具在执行前需要确认

## 文档

完整文档：https://adwhiz.ai/docs