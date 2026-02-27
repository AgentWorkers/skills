---
name: humanpages
description: "搜索并雇佣真实的人类来完成各种任务——包括摄影、送货、研究等等。"
homepage: https://humanpages.ai
user-invocable: true
metadata:
  openclaw:
    primaryEnv: HUMANPAGES_AGENT_KEY
    requires:
      env:
        - HUMANPAGES_AGENT_KEY
      bins:
        - npx
---
# Human Pages — 为实际任务雇佣人类

Human Pages 是一个连接人工智能与人类的市场平台。利用该平台，您可以找到合适的人选（如摄影师、司机、研究人员、公证人等），并直接以 USDC 付款雇佣他们，无需支付平台费用。

## 设置

1. MCP 服务器必须处于运行状态。使用 `openclaw mcp list` 命令进行验证——您应该能看到 `humanpages` 选项。
2. 如果尚未配置，请运行：`mcporter config add humanpages --command "npx -y humanpages"`。
3. `HUMANPAGES_AGENT_KEY` 应包含您的代理 API 密钥（以 `hp_` 开头）。如果用户还没有代理密钥，请使用 `register_agent` 命令创建一个，然后指导他们完成激活流程。

## 核心工作流程

典型的工作流程为：**搜索** → **注册并激活** → **雇佣** → **付款** → **评价**。

### 1. 搜索合适的人选

使用 `search_humans` 命令来查找合适的人选。可以通过以下条件进行筛选：
- **技能**（如：photography、driving、notary、research）
- **设备**（如：car、drone、camera）
- **语言**（ISO 代码，例如：en、es、zh）
- **位置**（城市或社区名称）
- **经纬度/半径**（以公里为单位的 GPS 搜索范围）
- **最高小时费率**（以 USD 为单位）
- **工作模式**（REMOTE、ONSITE 或 HYBRID）
- **身份验证状态**（设置为 `humanity` 仅显示已通过身份验证的用户）

使用 `get_human` 命令可以查看详细的用户信息（个人简介、技能、服务内容、信誉评级）。

### 2. 注册并激活代理

如果用户还没有代理密钥：
1. 调用 `register_agent` 命令并输入用户名。返回的 API 密钥无法再次获取，请妥善保存。
2. 代理的状态默认为 PENDING（待处理）。在创建任务之前必须先完成激活。

**免费激活（基础级）：**
- 调用 `request_activation_code` 获取激活代码（格式为 HP-XXXXXXXX）。
- 要求用户在社交媒体（如 Twitter/X、LinkedIn 等）上发布该激活代码。
- 使用 `verify_social_activation` 命令验证用户发布的链接。

**付费激活（高级级）：**
- 调用 `get_payment_activation` 获取收款地址。
- 用户通过区块链方式支付 USDC。
- 使用 `verify_payment_activation` 命令提供交易哈希值和网络信息进行验证。

**x402 按次付费模式（无需激活）：**
- 代理可以按每次请求付费（使用 x402 协议，基础费用为：每查看用户资料 0.05 USD，每接受任务报价 0.25 USD）。此模式不受等级限制。

使用 `get_activation_status` 命令查看当前等级和费用限制。

### 3. 查看用户资料

激活后，使用 `get_human_profile` 命令查看联系信息、钱包地址、法定货币支付方式以及社交媒体链接。请提供 `agent_key` 作为参数。

### 4. 创建任务报价

调用 `create_job_offer` 命令，提供以下信息：
- `human_id`：要雇佣的用户 ID
- `title` 和 `description`：任务内容
- `price_usdc`：约定的价格
- `agent_id` 和 `agent_key`：您的代理凭证

可选参数：设置 `callback_url` 以接收 Webhook 通知，以及 `payment_mode` 以选择流式支付方式。

等待用户接受报价。使用 `get_job_status` 命令查询任务状态。

### 5. 付款

**一次性付款：**
- 根据 `get_human_profile` 中提供的信息，将 USDC 付款到用户的钱包。
- 调用 `mark_job_paid` 命令，提供交易哈希值、网络信息和付款金额。

**流式付款（持续进行中的任务）：**
- 在用户接受报价后，调用 `start_stream` 启动付款流程。
- 对于 MICRO_TRANSFER 类型的任务，每次付款时调用 `record_stream_tick` 命令。
- 可使用 `pause_stream`、`resume_stream`、`stop_stream` 命令来暂停或恢复付款流程。

### 6. 评价

用户完成任务后，调用 `leave_review` 命令给出 1-5 分的评分和可选评论。

## 额外工具

- `get_agent_profile`：查看任何代理的公开资料和信誉评级。
- `verify_agent_domain`：验证域名所有权以获得信任徽章。
- `check_humanity_status`：检查用户是否通过了 Gitcoin Passport 的身份验证。

## 错误处理

- 如果 `create_job_offer` 返回 `AGENT_PENDING`，请指导用户完成激活流程。
- 如果用户设置了最低报价（`minOfferPrice`），而您的报价过低，请提高报价。
- 如果出现费用限制错误，说明已达到等级上限。此时可以选择升级到高级级，或使用 x402 按次付费模式。

## 功能分组

| 功能分组 | 是否可用 | 描述 |
|---|---|---|
| search | 是 | 搜索合适的人选并查看公开资料 |
| register | 是 | 注册并激活代理 |
| jobs | 是 | 创建任务报价并管理任务流程 |
| payments | 是 | 记录付款信息并管理付款流程 |
| reviews | 是 | 为已完成的任务留下评价 |