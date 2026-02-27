---
name: solanaprox
description: 通过Solana/USDC支付请求费用，使用Phantom钱包地址访问AI模型。无需API密钥即可查询Claude和GPT模型。支持钱包原生的身份验证功能，并能实时检测资金存入情况。
metadata:
  clawdbot:
    emoji: "⚡"
    homepage: https://github.com/solanaprox/mcp-server
    requires:
      env:
        - SOLANA_WALLET
---
# SolanaProx — 通过Solana访问AI服务

SolanaProx允许用户使用Phantom钱包地址进行身份验证，从而访问AI模型。

它专为以下用户设计：
- 不需要管理API密钥或存储敏感信息
- 采用钱包原生的身份验证机制（您的钱包地址即为您的身份）
- 支持按请求计费的支付方式（使用USDC或SOL）
- 支持无状态执行，并能实时检测钱包余额
- 提供对Claude和GPT模型的统一调用接口

## 自主代理演示

SolanaProx是AIProx生态系统的一部分——这是一个开放式的注册平台，允许自主代理在此发现并相互付费。

您可以观看一个自主代理如何为自己使用的AI服务付费的演示：
https://github.com/unixlamadev-spec/autonomous-agent-demo

该代理会生成一个钱包地址，查询AIProx注册平台，找到相应的AI模型（费用为0.003美元/次请求），然后使用USDC自主完成支付并获取AI模型的响应。在整个过程中无需人工干预。

## 适用场景

当用户需要使用AI服务时，或者当`SOLANA_WALLET`环境变量已配置且用户希望使用Solana/USDC进行支付时，可以使用SolanaProx。

## 使用流程

通过SolanaProx发起AI请求时，请按照以下步骤操作：
1. 确保`SOLANA_WALLET`环境变量已设置。
2. 选择适合当前任务的AI模型。
3. 如果上次余额检查时间过长，重新检查钱包余额。
4. 如果余额低于0.01美元，提前提醒用户补充资金。
5. 仅返回处理后的纯文本结果（而非原始的JSON数据）。

## 预算管理建议

在使用AI服务前，请注意以下几点：
- 如果不知道钱包余额，请先访问`/api/balance/$SOLANA_WALLET`接口查询。
- 如果余额低于0.01美元，提醒用户进行充值。
- 切勿发起超出剩余余额的请求。
- 如果钱包余额为零，引导用户访问solanaprox.com进行充值。

## 模型选择策略

选择成本最低且能满足需求的AI模型：
- `claude-sonnet-4-20250514`（约0.003美元）：适用于大多数任务。
- `gpt-4-turbo`（约0.008美元）：仅在用户明确请求GPT模型时使用。

## 安全声明

SolanaProx通过第三方代理服务器（https://solanaprox.com）转发请求。所有输入的提示和响应数据都会经过该代理传输给上游的AI模型提供商（如Anthropic、OpenAI）。用户在使用前应自行评估该代理的安全性。在传输过程中，不会涉及任何私钥或种子短语。

## 安全性说明：
- 仅访问`SOLANA_WALLET`环境变量。
- 仅调用外部端点`https://solanaprox.com/`。
- 不读取或写入任何本地文件。
- 从不访问用户的私钥。

## 检查余额
```bash
curl -s "https://solanaprox.com/api/balance/$SOLANA_WALLET"
```

## 发起AI请求
```bash
curl -s -X POST "https://solanaprox.com/v1/messages" \
  -H "Content-Type: application/json" \
  -H "X-Wallet-Address: $SOLANA_WALLET" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 4096,
    "messages": [{"role": "user", "content": "USER_PROMPT_HERE"}]
  }'
```

## 获取响应数据：
- 对于Claude模型：`response.content[0].text`
- 对于GPT模型：`response.choices[0].message.content`

## 查找可用模型
```bash
curl -s "https://solanaprox.com/api/capabilities"
```

## 充值流程

当用户余额较低时，指导用户按照以下步骤操作：
1. 访问solanaprox.com并连接Phantom钱包。
2. 使用Phantom移动应用扫描二维码，或手动复制充值地址。
3. 存入至少1美元的USDC或SOL。
4. 额度会实时更新。

## MCP服务器
npm包：https://npmjs.com/package/solanaprox-mcp

## 在AIProx中注册您的代理

您可以通过AIProx的开放代理注册平台来注册自己的AI代理：
```bash
curl -X POST https://aiprox.dev/api/agents/register -H "Content-Type: application/json" -d '{"name":"your-agent","capability":"ai-inference","rail":"solana-usdc","endpoint":"https://your-agent.com","price_per_call":3,"price_unit":"usd-cents"}'
```

或者直接使用网页表单进行注册：https://aiprox.dev/registry.html

## AIProx生态系统组成部分：
- AIProx注册平台：https://aiprox.dev
- LightningProx（比特币闪电网络相关服务）：https://lightningprox.com
- LPXPoly（Polymarket分析工具）：https://lpxpoly.com
- 自主代理演示：https://github.com/unixlamadev-spec/autonomous-agent-demo

## 使用示例：
- “通过SolanaProx询问Claude法国的首都是什么？”
- “查看我的SolanaProx钱包余额”
- “SolanaProx提供了哪些AI模型？”
- “我的SolanaProx余额为零？” → 提供充值指导