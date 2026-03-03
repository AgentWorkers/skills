---
name: x402engine
description: 按次计费的API网关功能：通过x402微支付方式调用63个API（包括大型语言模型、图像/视频生成、航班查询、酒店预订、加密货币相关服务以及网络搜索）。每次调用的费用为0.001至0.60美元（以USDC/USDm计），具体费用由本地策略引擎根据预设的支出上限进行控制。
version: 1.3.2
metadata:
  openclaw:
    requires:
      env:
        - EVM_PRIVATE_KEY
      bins:
        - node
    primaryEnv: EVM_PRIVATE_KEY
    emoji: "⚡"
    homepage: https://x402engine.app
    install:
      - kind: node
        package: "@x402/fetch"
        bins: []
      - kind: node
        package: "@x402/evm"
        bins: []
      - kind: node
        package: "viem"
        bins: []
---
# x402engine

通过x402微支付调用63个付费API。每次API调用的费用在0.001美元到0.60美元之间，支持使用Base/Solana上的USDC或MegaETH上的USDm进行支付。

## 该技能的功能

该技能代表用户签署并提交稳定币微支付请求，以调用远程API。它使用`EVM_PRIVATE_KEY`环境变量来在链上签署支付交易。每次调用都会从用户的钱包中扣除少量费用。

**费用透明度：**在显示结果时，需包含每次调用的费用（例如：“比特币的价格为97,500美元，费用为0.001美元”）。如果用户询问支出情况，应提供完整的预算明细。

## 触发条件
- “比特币的价格是多少”
- “以太坊的价格”
- “显示热门加密货币”
- “生成日落图片”
- “运行这段Python代码”
- “转录这段音频”
- “查看vitalik.eth的钱包活动”
- “让GPT解释x402”
- “抓取这个URL”
- “将这个内容存储到IPFS”
- “解析vitalik.eth的信息”
- “从JFK飞往LAX的航班”
- “在巴黎搜索酒店”
- “查找飞往东京的廉价航班”
- “还剩多少预算”
- “列出可用的服务”

## 工作原理
1. 从发现端点（默认地址：https://x402engine.app/.well-known/x402.json）获取缓存的服务目录。
2. 根据用户查询内容，在63个服务描述中找到最匹配的服务。
3. 在执行支付前，运行策略预检查——验证每次交易的费用上限、每日费用上限以及接收者白名单。
4. 通过`@x402/fetch`调用相应服务——自动处理支付流程。
5. 将结构化数据返回给代理，以便以自然语言的形式展示结果。

## 规则
- 以自然的方式展示结果，并明确说明每次调用的费用，让用户了解实际支出情况。
- 如果因资金不足导致支付失败，应告知用户：“我需要更多资金才能使用该服务。请向您的钱包中添加USDC以继续操作。”
- 如果未找到匹配的服务，应直接告知用户，切勿暴露内部路由细节。
- 政策限制具有权威性——严禁绕过费用上限或接收者白名单。
- 所有决策都应附带合理的理由代码以便解释。

## 安全性

### 必需的凭证
- **EVM_PRIVATE_KEY**（必需）——用于签署支付交易。请使用专用钱包，并确保钱包中的资金有限，切勿使用主钱包。如果未设置此密钥，系统会生成临时密钥（此时无法进行任何支付）。

### 可选的配置选项
这些环境变量为可选配置，可提供额外的控制功能：
- **EVM_PRIVATE_KEY_FILE**——替代`EVM_PRIVATE_KEY`，从文件中读取密钥。请选择其中一个，不要同时使用两个。
- **X402_POLICY_PATH**——JSON策略文件的路径。该文件定义了每次交易的费用上限、每日支出限额以及接收者白名单。如果没有配置此文件，系统将不执行任何支出限制。如果文件缺失或无效，所有支付请求都将被拒绝。
- **X402_STATE_PATH**——用于记录每日支出和速率限制状态的JSON文件路径。默认值为`.x402engine-state.json`。
- **X402_DISCOVERY_URL**——覆盖服务目录的URL（默认值：`https://x402engine.app/.well-known/x402.json`）。如果对默认地址不信任，可以自行托管服务目录。
- **X402_AUTOPREFLIGHT**——设置为`false`可跳过策略预检查。默认值为`true`。
- **X402_DISCOVERY_REFRESH_MS**——服务目录的缓存过期时间（以毫秒为单位）。

### 支付流程
所有支付都会发送到服务目录中指定的`payTo`地址。服务目录的地址从上述发现URL获取。如果需要限制可接收支付的地址，可以通过配置策略文件来实现接收者白名单。

## 预算检查
当用户询问“还剩多少预算”时：
- 加载策略文件和状态文件。
- 如果启用了费用限制，会显示每个链/资产的剩余每日限额。
- 显示速率限制状态。
- 显示钱包余额。

## 依赖项
该技能需要Node.js以及以下npm包（在`package.json`中列出）：
- `@x402/fetch`——支持x402支付的请求处理库
- `@x402/evm`——EVM支付方案（Permit2签名机制）
- `viem`——以太坊客户端库

安装方法：`cd skills/x402engine && npm install`

## 错误代码
- `POLICY_MISSING`：策略文件缺失
- `POLICY_INVALID`：策略文件无效
- `CHAINDenied`：无法访问目标链
- `ASSET_DENIED`：目标资产不可用
- `RECIPIENT_DENIED`：接收者被拒绝
- `PER_TX_EXCEEDED`：每次交易费用超过限制
- `DAILY_CAP_EXCEEDED`：每日支出超出限额
- `RATE_LIMITED`：达到速率限制
- `ACTION_DENIED`：操作被拒绝
- `SERVICE_NOT_FOUND`：服务未找到
- `WALLET_UNDERFUNDED`：钱包资金不足