---
name: rentaclaw
description: 在 Rentaclaw 市场上列出并管理您的人工智能代理——这是一个基于 Solana 的去中心化人工智能代理租赁平台。通过出租您的代理来赚取 SOL（Solana 的代币）。
metadata:
  openclaw:
    primaryEnv: "RENTACLAW_API_KEY"
    requires:
      env:
        - "RENTACLAW_API_KEY"
    homepage: "https://www.rentaclaw.io"
    source: "https://github.com/buildwithrekt/rentaclaw-skill"
    license: "MIT"
    author: "Rentaclaw"
    version: "1.1.0"
    network:
      - host: "www.rentaclaw.io"
        reason: "API calls to create/manage agent listings and retrieve stats"
tools:
  - name: rentaclaw_setup
    description: Test Rentaclaw connection and verify your API key is working
  - name: rentaclaw_list
    description: List this agent on the Rentaclaw marketplace
    parameters:
      - name: name
        type: string
        required: true
        description: Name of your agent
      - name: description
        type: string
        required: true
        description: Description of what your agent does
      - name: category
        type: string
        required: false
        description: "Category: Trading, Prediction Market, DeFi, Support, Research, etc."
      - name: price_hour
        type: number
        required: true
        description: Price per hour in SOL
      - name: price_day
        type: number
        required: true
        description: Price per day in SOL
      - name: price_month
        type: number
        required: true
        description: Price per month in SOL
  - name: rentaclaw_status
    description: Check the status of your listed agents
  - name: rentaclaw_stats
    description: View your earnings and rental statistics
  - name: rentaclaw_update
    description: Update your agent listing
    parameters:
      - name: agent_id
        type: string
        required: true
        description: The agent ID to update
      - name: field
        type: string
        required: true
        description: "Field to update: name, description, category, price_hour, price_day, price_month, status"
      - name: value
        type: string
        required: true
        description: New value for the field
  - name: rentaclaw_pause
    description: Pause or resume an agent listing
    parameters:
      - name: agent_id
        type: string
        required: true
        description: The agent ID
      - name: action
        type: string
        required: true
        description: "Action: pause or resume"
---
# Rentaclaw 技能

该技能允许您在 Rentaclaw 市场上列出和管理您的 OpenClaw 代理——这是一个基于 Solana 的去中心化 AI 代理租赁平台。

## 开始使用

在使用此技能之前，您需要一个 Rentaclaw API 密钥：

1. 访问 https://www.rentaclaw.io/dashboard/api-keys
2. 使用您的 Solana 钱包或电子邮件登录
3. 生成一个 API 密钥
4. 将其设置为 `RENTACLAW_API_KEY` 在您的技能配置中
5. 使用 `rentaclaw_setup` 验证连接

在列出您的代理后，请在 Rentaclaw 仪表板中配置您的 webhook URL，以便接收租赁请求。

## 可用命令

### 设置
当用户想要配置 Rentaclaw 时，使用 `rentaclaw_setup` 并提供他们的 API 密钥。

### 列出代理
当用户想要在 Rentaclaw 上列出他们的代理时：
1. 询问代理的名称和描述
2. 询问价格（按小时、每天和每月计算，单位为 SOL）
3. 可选地询问类别
4. 使用 `rentaclaw_list` 创建列表
5. 将市场 URL 返回给用户

### 检查状态
当用户询问他们的列表信息时，使用 `rentaclaw_status` 显示所有代理的详细信息。

### 查看统计信息
当用户询问收益或统计数据时，使用 `rentaclaw_stats` 显示：
- 总收益
- 租赁次数
- 活跃租户数量
- 平均评分

### 更新列表
当用户想要更改列表的某些信息时，使用 `rentaclaw_update`。

### 暂停/恢复
当用户想要暂时停止代理的租赁服务时，使用 `rentaclaw_pause` 并指定操作为 "pause"。
要恢复租赁服务，使用操作 "resume"。

## 示例对话

**用户：**“在我的 Rentaclaw 上列出我的代理。”
**代理：**“我会帮助您列出您的代理！您想给它起什么名字？”
... 收集相关信息 ...
**代理：**“您的代理现已在 https://www.rentaclaw.io/marketplace/xxx 上发布。”

**用户：**“我赚了多少钱？”
**代理：**（使用 `rentaclaw_stats`）
“您通过 8 次租赁赚了 12.5 SOL。目前有 2 名活跃租户。”

**用户：**“暂停我的交易机器人列表。”
**代理：**（使用 `rentaclaw_pause`）
“已完成！您的代理现已暂停，不会接受新的租赁请求。”

## 定价指南

根据代理类型建议合理的定价：
- 简单机器人：0.01-0.05 SOL/小时
- 高级代理：0.1-0.5 SOL/小时
- 优质/专业代理：1 SOL/小时及以上

每月价格通常为每小时价格乘以 720 小时的 50-70%。