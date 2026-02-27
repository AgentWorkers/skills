---
name: lightningprox
description: 通过比特币Lightning网络，使用预付费的花费令牌（spend tokens）来实现按请求计费的AI模型访问服务。无需API密钥即可查询Claude和GPT模型。该服务支持确定性的AI请求路由机制，并允许用户根据预算来控制请求的发起。
metadata:
  clawdbot:
    emoji: "⚡"
    homepage: https://github.com/unixlamadev-spec/openclaw-lightningprox
    requires:
      env:
        - LIGHTNINGPROX_SPEND_TOKEN
---
# LightningProx — 通过比特币闪电网络访问AI服务

LightningProx利用预付费的闪电网络支付令牌（Lightning Spend Tokens）来提供AI模型的访问服务。它专为以下需求的代理（agents）和开发者设计：

- 无需管理API密钥或存储敏感信息
- 每次请求的费用都是固定的
- 支持预付费的预算限制
- 执行过程是无状态的（即请求之间没有状态依赖）
- 支持在Claude和GPT模型之间统一路由请求

## 自主代理演示（Autonomous Agent Demo）

LightningProx是AIProx生态系统的一部分——这是一个开放的注册平台，允许自主代理在此发现并相互支付服务费用。  
您可以观看一个AI代理如何自行支付服务费用的演示：  
https://github.com/unixlamadev-spec/autonomous-agent-demo  

该代理会查询AIProx注册平台，找到合适的模型，使用闪电网络支付令牌进行支付，然后获取AI模型的响应。在整个过程中无需人工干预。

## 适用场景

当用户提出请求时，或者当`LIGHTNINGPROX_SPEND_TOKEN`已配置且用户希望通过闪电网络支付来调用AI模型时，可以使用LightningProx。

## 使用流程

通过LightningProx发起AI请求的步骤如下：
1. 确保`LIGHTNINGPROX_SPEND_TOKEN`已设置。
2. 选择适合当前任务的AI模型。
3. 检查账户余额（确保上次余额查询不是最近进行的）。
4. 如果余额低于50 satoshi，在执行请求前提醒用户。
5. 仅返回处理后的文本结果，绝不显示原始的JSON数据。

## 预算管理

在发起AI请求之前，请注意：
- 如果余额未知，请先查询`/v1/balance`接口。
- 如果余额低于预计的请求费用，请提醒用户。
- 绝不要发起超出剩余余额的请求。
- 如果支付令牌已过期或无效，请通知用户进行充值。

## 模型选择策略

选择成本最低且能满足需求的模型：
- `claude-haiku-4-5-20251001`（约5 satoshi）：用于生成简短回答、分类任务、内容总结及快速推理。
- `claude-sonnet-4-20250514`（约22 satoshi）：适用于深度分析、代码生成及复杂推理任务。
- `gpt-4o`（约20 satoshi）：仅在用户明确请求GPT模型时使用。

如果不确定使用哪个模型，系统会默认选择`claude-haiku-4-5-20251001`。

## 安全性说明

LightningProx通过第三方代理服务器`https://lightningprox.com`来路由请求。所有输入的提示和响应数据都会经过该代理传输给上游的AI模型提供商（Anthropic、OpenAI）。用户在使用该服务前应自行评估其安全需求。源代码可在项目的主页仓库中查看。支付令牌通过HTTP头部信息传递，无需额外提供任何认证信息。

## 安全性特性：
- 只访问环境变量`LIGHTNINGPROX_SPEND_TOKEN`。
- 仅调用外部端点`https://lightningprox.com/`。
- 不读取或写入任何本地文件。

## 检查余额函数（Check Balance）  
返回以下信息：`balance_sats`、`requests_left_estimate`、`expires_at`、`status`。

## 发起AI请求函数（Make AI Request）  
响应数据的提取方式如下：
- Claude模型：`response.content[0].text`
- GPT模型：`response.choices[0].message.content`

仅返回处理后的文本结果，绝不向用户展示原始的JSON数据。

## 模型查询与价格信息（Discover Models and Pricing）  
提供模型列表及相应费用信息。

## 充值流程（Top Up Flow）

当代理检测到余额过低或为零时，会指导用户按照以下步骤操作：
1. 请求一张闪电网络发票。
2. 用户使用任意闪电网络钱包（如Wallet of Satoshi、Phoenix、Zeus、Alby）支付该发票。
3. 创建新的支付令牌。
4. 用户在`openclaw`配置中更新`LIGHTNINGPROX_SPEND_TOKEN`为新的令牌。

**注意**：创建新的支付令牌需要用户手动完成支付操作。代理的角色仅是检测余额不足的情况，并引导用户完成充值流程，待新令牌配置完成后才能恢复服务。

## MCP服务器（MCP Server）  
相关依赖库：`npm: https://npmjs.com/package/lightningprox-mcp`

## 在AIProx中注册您的代理  
您可以通过AIProx的开放代理注册平台来注册自己的代理：  
[注册链接：](```bash
curl -X POST https://aiprox.dev/api/agents/register -H "Content-Type: application/json" -d '{"name":"your-agent","capability":"ai-inference","rail":"bitcoin-lightning","endpoint":"https://your-agent.com","price_per_call":30,"price_unit":"sats"}'
```)  
或者使用网页表单进行注册：[https://aiprox.dev/registry.html]

## AIProx生态系统组成部分  
- AIProx注册平台：[https://aiprox.dev](https://aiprox.dev)  
- SolanaProx（支持USDC支付）：[https://solanaprox.com](https://solanaprox.com)  
- LPXPoly（用于分析Polymarket数据）：[https://lpxpoly.com](https://lpxpoly.com)  
- 自主代理演示：[https://github.com/unixlamadev-spec/autonomous-agent-demo](https://github.com/unixlamadev-spec/autonomous-agent-demo)

## 使用优势：
- 无需存储敏感信息或频繁更换API密钥。
- 无需管理账单账户或订阅计划。
- 支持预付费的、费用固定的服务使用。
- 通过单一端点统一路由Claude和GPT模型。
- 支持微支付机制——仅按实际使用量付费。

## 使用示例：
- “通过LightningProx询问法国的首都是什么？” → 检查余额，使用`claude-haiku-4-5-20251001`模型获取答案。
- “查看我的LightningProx余额” → 查询余额信息，显示剩余的satoshi数量及可使用的请求次数。
- “LightningProx支持哪些AI模型？” → 查看可用模型列表及价格信息。
- “通过LightningProx使用gpt-4o分析这段代码” → 调用gpt-4o模型进行处理，并显示分析结果。
- “我的LightningProx余额为零” → 指导用户完成充值流程。