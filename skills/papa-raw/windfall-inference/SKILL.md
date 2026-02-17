---
name: windfall-inference
description: 基于空间路由的LLM推理服务，每请求费用仅为0.004美元。该服务能自动选择最便宜、最环保的能源供应方式，支持200多种模型，并与OpenAI兼容。所有数据都存储在Base平台上，并通过区块链技术进行验证。
homepage: https://windfall.ecofrontiers.xyz
user-invocable: true
metadata: {"openclaw":{"emoji":"⚡","requires":{"env":["WINDFALL_API_KEY"]},"primaryEnv":"WINDFALL_API_KEY","os":["darwin","linux","win32"]}}
---
# Windfall Inference

这是一个用于AI代理的空间路由式大语言模型（LLM）推理服务，运行在Base平台上。该服务会将每个请求路由到使用最清洁能源的、成本最低的模型。

## 设置

请在您的环境中设置`WINDFALL_API_KEY`。您可以在以下链接免费获取API密钥：

```
curl -X POST https://windfall.ecofrontiers.xyz/api/keys \
  -H "Content-Type: application/json" \
  -d '{"wallet_address": "YOUR_WALLET"}'
```

具有ERC-8004代理身份或Basename的密钥可享受100次免费请求；匿名密钥则只能享受25次免费请求。

## 使用方法

将该服务作为兼容OpenAI的端点使用。请设置以下两个环境变量：

```
OPENAI_BASE_URL=https://windfall.ecofrontiers.xyz/v1
OPENAI_API_KEY=wf_YOUR_KEY
```

或者直接调用该服务：

```
curl https://windfall.ecofrontiers.xyz/v1/chat/completions \
  -H "Authorization: Bearer $WINDFALL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

## x402支付（无需API密钥）

Windfall支持x402支付协议。任何拥有Base钱包的代理都可以无需创建API密钥即可按请求付费。如果您发送请求时未提供认证信息，服务器会返回HTTP 402错误响应，并在响应头中包含使用Base平台进行支付的USDC支付指令。您的x402客户端将负责处理后续的支付流程。

## 路由模式

- `greenest`（默认）：最低碳强度
- `cheapest`：最低能源成本
- `balanced`：基于帕累托原则平衡的能源成本与碳排放

您可以通过请求体中的`"mode"`字段或`X-Routing-Mode`头部来指定路由模式。

## 模型

默认使用DeepSeek V3模型（由系统自动选择）。您也可以通过`"model"`字段自定义模型。通过OpenRouter可以访问200多种模型。

## 定价

- 标准价格：0.004美元/请求
- 高级价格（Claude、GPT-4）：0.008美元/请求
- 环保附加费：`greenest`模式下额外收取10%的费用
- 缓存命中：免费

## 响应头部信息

每个响应都会包含以下头部信息：
- `X-Windfall-Cache`：表示请求是否命中缓存（HIT或MISS）
- `X-Windfall-Mode`：使用的路由模式
- `X-Windfall-Model`：处理请求的模型
- `X-Windfall-Node`：执行请求的节点
- `X-Windfall-Cost`：收取的费用
- `X-Windfall-Saved`：与直接使用API相比的节省费用（针对缓存命中的情况）

## 在链上验证

每次推理请求都会在Base平台上生成一个可验证的EAS证书，其中包含节点位置、能源价格、碳排放强度、使用的模型以及响应哈希值。您可以在base.easscan.org查询该证书。