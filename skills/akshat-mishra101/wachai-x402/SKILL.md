---
name: x402-wach
description: 由 WACH.AI 提供支持的 DeFi 风险分析工具包，通过 AWAL 钱包托管服务进行 x402 支付。当用户需要查询代币的安全性、评估 DeFi 风险、检测“蜜罐”（恶意陷阱）、分析流动性、持有人分布或以太坊（Ethereum）、Polygon、Base、BSC 或 Solana 上代币的智能合约漏洞时，可以使用该工具包。在 Base 平台上，每次查询的费用为 0.01 美元（USDC）。
license: MIT
compatibility: Requires Node.js 18+, npm, network access, AWAL installed and authenticated, and a funded AWAL wallet with USDC on Base.
metadata:
  author: quillai-network
  version: "3.0"
  endpoint: https://x402.wach.ai/verify-token
  payment: 0.01 USDC on Base (automatic via x402)
---
# x402-wach — DeFi风险分析工具

这是一个由WACH.AI提供的DeFi风险分析工具包，它使用x402技术，并通过AWAL（Automatic Wallet Authentication Layer）来管理用户的私钥安全。

## OpenClaw的硬性规则（不可协商）

当此功能被激活时，OpenClaw必须严格遵守以下规则：

1. **严禁请求或泄露敏感信息**
   - 绝对不要询问用户的私钥、助记词、钱包导出文件或原始签名数据。
   - 严禁建议用户使用`wallet.json`或任何本地密钥文件。

2. **仅使用AWAL进行密钥管理**
   - 所有的设置和支付操作都必须通过AWAL支持的命令来完成。
   - 对于旧版本的本地钱包指令，此功能将视为无效。

3. **在发起支付请求前进行准备检查**
   - 在执行`verify-risk`命令之前，确保AWAL已经正确设置（通过`wallet setup`或`wallet doctor`命令）。
   - 如果未准备好，请引导用户完成登录或资金充值流程。

4. **遵守支付限制**
   - 默认的每次支付上限为10000个原子单位USDC（约0.01美元）。
   - 除非用户明确要求，否则不得提高支付上限。

5. **如实显示支付失败原因**
   - 如果支付失败，必须明确指出失败原因及后续操作步骤（如身份验证问题、账户余额问题、网络问题或命令不匹配等）。
   - 除非收到了有效的报告数据，否则不得假装支付成功。

6. **避免重复支付**
   - 对于网络或临时性的错误，最多只允许重试一次。
   - 重试时需保持相同的请求参数，并告知用户已尝试过重试。

7. **在最终报告中提供来源链接**
   - 建议使用TokenSense提供的链接格式：
     - `https://tokensense.wach.ai/<chain>/<tokenAddress>`
   - 仅在必要时使用API作为备用方案。

## 何时使用此功能

当用户需要以下操作时，可以使用此功能：
- 评估某种代币的DeFi风险
- 检测是否存在诈骗或诱骗行为
- 分析代币持有者的集中程度及流动性
- 审查合约的安全性
- 获取风险评分及代码质量分析结果
- 对`eth`、`pol`、`base`、`bsc`或`sol`等链上的代币进行综合评估

## 支持的链

| 简称 | 链名                | 代币标准           |
|------|------------------|-------------------|
| `eth`  | Ethereum           | ERC-20              |
| `pol`  | Polygon             | ERC-20              |
| `base` | Base                | ERC-20              |
| `bsc`  | Binance Smart Chain     | BEP-20              |
| `sol`  | Solana              | SPL                |

无论分析哪个链，支付都将以USDC为单位进行。

## OpenClaw的命令使用指南

### 1) 准备/设置

执行以下命令：

```bash
x402-wach wallet setup
```

如果系统提示尚未准备好，执行以下命令：

```bash
x402-wach wallet doctor
x402-wach wallet login <EMAIL>
x402-wach wallet verify <FLOW_ID> <OTP>
x402-wach wallet balance
```

**解释：**
- `✓ Ready to make x402 payments with AWAL`：表示可以使用AWAL进行x402支付，可以继续分析。
- `AWAL wallet is not authenticated`：表示AWAL钱包未经过身份验证，需要用户登录并完成验证。
- `Insufficient USDC on Base`：表示Base链上的USDC余额不足，需要用户向AWAL地址充值。
- `Could not read AWAL balance/status`：表示无法读取AWAL的余额或状态信息，需要运行`wallet doctor`命令获取详细错误信息。

### 2) 进行风险分析

执行以下命令：

```bash
x402-wach verify-risk <TOKEN_ADDRESS> <CHAIN_SHORT_NAME>
```

**推荐的安全支付上限格式：**

```bash
x402-wach verify-risk <TOKEN_ADDRESS> <CHAIN_SHORT_NAME> --max-amount-atomic 10000
```

### 3) 可选辅助命令

```bash
x402-wach wallet status
x402-wach wallet address
x402-wach chains
x402-wach guide
```

## 工具结果解读规则

### 准备状态/错误信息

- 如果输出中包含`✓ Ready`：表示可以安全地进行支付分析。
- 如果输出中包含`not authenticated`：表示需要用户输入OTP进行身份验证。
- 如果输出中包含`Insufficient USDC`：表示Base链上的USDC余额不足，需要用户充值。
- 如果输出中包含来自AWAL的错误提示：表示命令不匹配或版本问题，需要运行`x402-wach wallet doctor`并使用相应的子命令。
- 如果输出中包含JSON解析错误：表示AWAL的输出格式不正确，需要重新尝试或检查AWAL的配置。

### `verify-risk`的输出结果

- `Token analysis complete!` + 各项分析结果已填充：表示分析成功。
- 只有标题而没有内容：表示报告解析失败，需要检查工具的解析逻辑。
- `No token found` / `empty report`：表示未找到对应的代币或报告为空：表示调用成功但目标地址上没有该代币。
- `402/payment error`：表示支付过程中出现错误，需要用户检查账户余额、支付上限或身份验证信息。

## 用户安全指南

如果遇到问题，请提供以下引导信息：

```bash
x402-wach wallet doctor
x402-wach wallet login <email>
x402-wach wallet verify <flowId> <otp>
x402-wach wallet balance
```

然后尝试重新操作：

```bash
x402-wach verify-risk <TOKEN_ADDRESS> <CHAIN_SHORT_NAME> --max-amount-atomic 10000
```

## 程序化使用方式（适用于自动化脚本）

```typescript
import {
  getAwalReadiness,
  validateTokenAddress,
  verifyTokenRisk,
} from "@quillai-network/x402-wach";

const token = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
const chain = "eth";

const validation = validateTokenAddress(token, chain);
if (!validation.valid) throw new Error(validation.error);

const readiness = await getAwalReadiness(10_000);
if (!readiness.ready) throw new Error(readiness.reasons.join("; "));

const report = await verifyTokenRisk(token, chain, { maxAmountAtomic: 10_000 });
console.log(report);
```

## 预期报告内容

分析成功后，报告将包含以下内容：
- 市场数据
- 风险评分
- 代币持有者分布
- 流动性分析
- 合约安全评估
- 社交媒体与社区信息
- 数据来源（TokenSense链接）及报告生成时间

## OpenClaw的绝对禁止事项

- 禁止使用或建议用户使用`wallet create`、`wallet import`或`wallet.json`命令。
- 禁止询问用户的私钥或助记词。
- 禁止在用户不知情的情况下调整支付上限。
- 如果解析报告失败，不得假装分析成功。
- 在需要诊断问题时，不得隐藏AWAL的原始错误信息。