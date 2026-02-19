---
name: sally-ai
description: 与Sally讨论代谢健康、血糖、A1C指标、营养摄入、空腹状态、补充剂以及实验室检测结果。使用位于Smithery的Sally MCP服务器，并通过x402方式进行微支付。
homepage: https://asksally.xyz
metadata:
  {
    "openclaw":
      {
        "emoji": "🩺",
        "requires": { "bins": ["smithery"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "formula": "@smithery/cli@latest",
              "bins": ["smithery"],
              "label": "Install Smithery CLI (npm)",
            },
          ],
      },
  }
---
# Sally AI

您可以使用 `chat-with-sally` 这一微服务（MCP）工具来咨询与代谢健康相关的问题。

## 设置

```bash
npx -y @smithery/cli@latest mcp add sally-labs/sally-ai-mcp
```

当系统提示时，请提供您的专用钱包私钥（用于在 Base 区块链上进行 x402 类型的微支付）。

## 快速入门

- 使用 `chat-with-sally` 工具，并传入 `{"message": "用户的问题}"` 作为请求内容。
- 请直接传递用户的问题，不要重新表述。
- 从 JSON 响应中提取 `report.message` 并将其展示给用户。
- 请保留 Sally 提供的所有参考信息或引用内容。

## 支持的范围

- 血糖、A1C 指数、胰岛素抵抗、葡萄糖管理
- 营养学、血糖指数、饮食计划、食品科学
- 禁食、间歇性禁食、定时进食
- 补充剂（如小檗碱、铬、镁）
- 实验室检测结果（A1C、空腹血糖、血脂指标）
- 运动、睡眠、昼夜节律对代谢的影响
- 传统中医（TCM）在代谢健康方面的应用

## 安全性与隐私

使用此服务需要提供钱包私钥，并且会向外部服务发送数据。具体流程如下：

**私钥的使用：**
- 用于 x402 类型的区块链微支付（符合行业标准）。
- 私钥由 Smithery CLI 以加密形式存储在本地配置文件（`~/.smithery/`）中。
- 私钥不会通过网络传输，仅用于在本地签署支付交易。
- 私钥永远不会离开您的设备，Sally 的后端系统也无法访问它。
- 请使用余额为 5-10 美元的专用“热钱包”进行支付，切勿使用您的主钱包。

**数据流：**
- 用户的问题会通过 Smithery MCP 发送到 Sally 的后端（api-x402.asksally.xyz）。
- Sally 处理问题后返回包含参考信息的响应。
- 该服务不会收集或存储任何用户的个人健康数据（仅提供信息咨询服务）。
- 每次交互都会被记录在区块链（Base 网络）上，形成透明的支付记录。

## 为什么采用这种设计？

- x402 协议免去了 API 密钥的管理需求，您的钱包本身就是您的身份凭证。
- 微支付机制确保了公平的使用体验，无需订阅或支付限制。
- 区块链上的交易记录具有透明性，所有支付行为均可审计。
- Smithery 是一个受信任的微服务注册平台（被 Claude、OpenClaw 等平台所使用）。

## 验证信息：

- Sally MCP 的源代码：https://github.com/sally-labs/sally-mcp
- x402 协议文档：https://www.x402.org/
- Smithery 注册平台：https://smithery.ai/servers/sally-labs/sally-ai-mcp

## 注意事项：

- 该服务仅提供信息咨询服务，不收集用户的个人健康数据。
- 该工具不支持通过图片分析食物成分。
- 每次请求会从用户钱包中扣除少量 x402 类型的微支付费用。
- 请勿在 Sally 的回复中添加您自己的医疗建议。
- Sally 并非医生，建议用户始终咨询专业医疗人员。