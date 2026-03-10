---
name: humanpages
description: "搜索并雇佣真实的人类来完成各种任务——包括摄影、送货、研究等等。"
homepage: https://humanpages.ai
license: MIT
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

Human Pages 是一个将人工智能与人类连接起来的平台。利用这一功能，您可以找到合适的人选（如摄影师、司机、研究人员、公证人等），并直接以 USDC 付款雇佣他们，无需支付平台费用。

## 设置要求

1. MCP 服务器必须处于运行状态。使用 `openclaw mcp list` 命令进行验证，确保系统中显示有 `humanpages` 选项。
2. 如果尚未配置，请运行以下命令：`mcporter config add humanpages --command "npx -y humanpages"`。
3. 变量 `HUMANPAGES_AGENT_KEY` 需要包含您的代理 API 密钥（该密钥以 `hp_` 开头）。如果用户还没有密钥，可以使用 `register_agent` 命令进行创建。代理在 PRO 级别（启动期间免费）会自动激活，可立即投入使用。

## 核心工作流程

典型的工作流程为：**搜索** → **注册** → **雇佣** → **支付** → **评价**。

### 1. 搜索合适人选

使用 `search_humans` 命令来查找合适的人选。您可以根据以下条件进行筛选：
- **技能**（例如：摄影、驾驶、公证、研究）
- **设备**（例如：汽车、无人机、相机）
- **语言**（ISO 代码，如 en、es、zh）
- **位置**（城市或社区名称）
- **经纬度/半径**（以公里为单位的 GPS 搜索范围）
- **最高时薪**（以 USD 为单位）
- **工作模式**（远程、现场或混合模式）
- **身份验证状态**（设置为 `humanity` 仅显示已通过身份验证的用户）

使用 `get_human` 命令可查看候选人的详细公开资料（个人简介、技能、服务内容、信誉评分）。

### 2. 注册代理

如果用户还没有代理密钥：
1. 调用 `register_agent` 命令并提供一个名称。可选地，您可以设置 `webhook_url` 以接收平台事件通知（如新匹配结果、状态变化等）。请妥善保存返回的 API 密钥和 webhook 密钥，因为这些信息之后无法重新获取。
2. 代理在 PRO 级别会自动激活（启动期间免费），可以立即投入使用。无需额外激活步骤。

**可选：社交验证（信任徽章）：**
1. 调用 `request_activation_code` 命令获取激活码。
2. 要求用户在社交媒体（如 Twitter/X、LinkedIn 等）上发布该激活码。
3. 使用 `verify_social_activation` 命令验证该帖子，从而获得信任徽章。此操作不会影响用户的访问权限或使用频率限制。

**可选：支付验证（信任徽章）：**
1. 调用 `get_payment_activation` 命令获取用户的支付地址。
2. 用户通过区块链方式发送 USDC 付款。
3. 使用 `verify_payment_activation` 命令并提供交易哈希值及网络信息进行验证。

**按使用次数计费的选项（x402）：**
代理也可以通过 x402 协议按请求收费（基础费用为 0.05 USD/个人资料查看；工作报价为 0.25 USD）。请在请求中添加 `x-payment` 标头。这种方式可以绕过层级使用频率限制。

使用 `get_activation_status` 命令查询当前的使用级别和费用限制。

### 3. 查看完整资料

使用 `get_human_profile` 命令查看候选人的联系方式、钱包地址、法定货币支付方式及社交链接。代理在注册完成后即可立即投入使用。

### 4. 创建工作邀约

调用 `create_job_offer` 命令，提供以下信息：
- `human_id`：要雇佣的人的 ID
- `title` 和 `description`：需要完成的任务内容
- `price_usdc`：约定的价格
- `agent_id` 和 `agent_key`：您的代理凭证

**可选：**
- 设置 `callback_url` 用于接收 webhook 通知
- 设置 `payment_mode` 以处理流式支付（例如：实时支付）

等待候选人接受邀约后，使用 `get_job_status` 命令查询任务状态。

### 5. 支付

**一次性支付：**
1. 将 USDC 付款到候选人的钱包地址（信息可从 `get_human_profile` 获取）。
2. 使用 `mark_job_paid` 命令，提供交易哈希值、网络信息及付款金额。

**流式支付（持续进行的工作）：**
1. 在候选人接受邀约后，调用 `start_stream` 命令开始支付流程。
2. 对于微支付（MICRO_TRANSFER），每次付款时调用 `record_stream_tick` 命令。
3. 可使用 `pause_stream`、`resume_stream`、`stop_stream` 命令来暂停或恢复支付流程。

### 6. 评价

候选人完成工作后，使用 `leave_review` 命令给出 1-5 分的评价及可选的评论。

## 其他工具

- `get_agent_profile`：查看任何代理的公开资料和信誉评分。
- `verify_agent_domain`：验证域名所有权以显示信任徽章。
- `check_humanity_status`：检查候选人是否通过了 Gitcoin 的身份验证。

## 错误处理

- 如果 `create_job_offer` 返回 `AGENT_PENDING`（旧版本），请再次调用 `register_agent` 以获取新的自动激活代理。
- 如果候选人设置了最低报价（`minOfferPrice`），且您的报价过低，请提高报价。
- 如果遇到费用限制错误，说明已达到层级使用上限。此时您可以升级到 PRO 级别，或选择按使用次数计费的 x402 方式支付。

## 动作组

| 动作组 | 是否启用 | 描述 |
|---|---|---|
| search | 是 | 搜索合适人选并查看其公开资料 |
| register | 是 | 注册并激活代理 |
| jobs | 是 | 创建工作邀约并管理工作流程 |
| payments | 是 | 记录支付信息并管理支付流程 |
| reviews | 是 | 为已完成的工作留下评价 |