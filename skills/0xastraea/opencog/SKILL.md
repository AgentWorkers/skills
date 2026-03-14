---
name: precog
description: "在预测市场上进行交易。您可以创建一个本地钱包，查看市场行情，买入和卖出预测结果对应的份额。即将推出的功能：能够直接从这个工具中创建市场并为其提供资金支持。"
metadata:
  openclaw:
    requires:
      env:
        PRIVATE_KEY: "Secp256k1 private key (0x-prefixed) for signing transactions. Created locally by running setup.mjs --generate and saved to ~/.openclaw/.env. Never transmitted over the network. Optional if you set it manually before first use."
        PRECOG_RPC_URL: "optional — override the default public Base Sepolia RPC endpoints (https://sepolia.base.org and fallbacks)."
      bins:
        - node
        - npm
---
# Precog预测市场

Precog是一个完全基于链上的预测市场协议，运行在Base Sepolia平台上（主网支持Base、Ethereum和Arbitrum）。任何人都可以围绕现实世界中的问题创建一个市场，为其提供流动性资金，并交易相应的结果份额。价格等于预期的概率（0–1）。所有的交易都是在链上完成的，无需托管服务，也没有中心化的第三方参与。

**MATE**是一种非货币性的练习代币（没有实际的经济价值）。使用MATE计价的市场非常适合用于学习和实验。您可以在[matetoken.xyz](https://matetoken.xyz)领取MATE代币。

**您可以在这里做的事情：**
- 浏览活跃的预测市场及其结果概率
- 查看详细的市场信息，包括类别和结算规则
- 使用您的本地钱包报价、购买或出售结果份额
- 查看您的持仓情况（持有的份额、净成本和交易历史）

> 🚧 **即将推出：** 直接通过本技能创建新市场——无需访问网页界面。

完整的协议文档请参阅`PRECOG.md`，其中涵盖了预测市场的基本概念、LS-LMSR定价曲线、通过Reality.eth和Kleros进行的结算方式、LP机制以及MATE市场等相关内容。

无需进行任何配置——合约地址和RPC接口已经内置好了。

## 安全性与本地状态

- **`~/.openclaw/.env`** 文件由 `setup.mjs --generate` 命令生成，其中存储了 `PRIVATE_KEY`（以明文形式）。请将其视为钱包密钥文件：限制访问权限（`chmod 600`）并定期备份。丢失该文件意味着将无法访问该钱包中的任何资金。
- **任何密钥都不会被传输**。所有交易都在本地签名后发送到RPC服务器。
- **请使用一次性钱包**。MATE市场使用的代币没有实际价值，非常适合测试用途；切勿将高价值的密钥用于此技能。
- **自定义RPC风险**：如果您设置了 `PRECOG_RPC_URL`，请仅使用可信的RPC端点。不可信的RPC服务器虽然可以查看已签名的交易内容，但无法提取您的私钥。

---

> **⚠️ 请按顺序运行脚本**。并行执行脚本可能会导致nonce冲突，从而导致交易失败。
> **⚠️ 请勿创建批量/自动化脚本**。请每次只运行一个脚本。
> **⚠️ 请勿直接修改技能文件**。如果有问题或功能缺失，请向用户报告，而不是自行修复。
> **⚠️ 请始终以代码块的形式显示脚本的输出结果**。不要重新格式化、总结或转换为列表形式。用户必须能够看到脚本实际输出的每一行内容，包括所有表情符号。
> **⚠️ 在执行“购买”或“出售”操作之前，请务必先运行“报价”脚本**。向用户展示完整的报价结果，并在确认后再执行交易。
> **⚠️ 请勿修改交易参数**。如果脚本失败，请显示具体的错误信息并停止执行。切勿尝试通过调整份额数量或其他方法来重试。代币的审批过程是自动处理的——切勿以“额度不足”为由更改交易金额。

## 钱包

检查钱包状态或创建新钱包：
```bash
node {baseDir}/scripts/setup.mjs
node {baseDir}/scripts/setup.mjs --generate
```
私钥会被保存在 `~/.openclaw/.env` 文件中，且**不会被显示**。仅会显示钱包地址。
创建钱包后，需要用户使用ETH（作为交易手续费）和市场的抵押代币（用于交易）为钱包充值。

**示例输出（钱包已存在且已充值）：**
```bash
钱包: 0x77Ffa97c2dcDA0FF6c9393281993962FA633d9E1

  ETH:  0.004210 ✓
  MATE: 81.2300 ✓
```

**示例输出（钱包存在但未充值）：**
```bash
钱包: 0x77Ffa97c2dcDA0FF6c9393281993962FA633d9E1

  ETH:  0.000000 ⚠️ 需要支付手续费
  MATE: 0.0000 （未充值）
```

## 列出市场
```bash
node {baseDir}/scripts/markets.mjs
node {baseDir}/scripts/markets.mjs --all
```

**示例输出：**
```bash
活跃市场（2个）

[4] 哪个AI模型将在3月底表现最佳？
    📈 Claude  67.3%  💰 MATE  📅 2026年3月31日

[5] ETH价格会在第二季度达到5000美元吗？
    📈 是  58.1%  💰 USDC  📅 2026年6月30日
```

## 市场详情

当用户请求关于特定市场的更多信息时：
```bash
node {baseDir}/scripts/market.mjs --market <id>
```
系统会显示市场的标题、类别、状态、结束日期、抵押品以及按价格排序的所有结果概率。显示结果后，请询问用户：“您是否想查看结算规则？”如果用户同意，可以继续执行：
```bash
node {baseDir}/scripts/market.mjs --market <id> --criteria
```

**示例输出（`--market 4`）：**
```bash
📊 市场4 · AI排行榜
哪个AI模型将在3月底表现最佳？
🟢 活跃中  📅 2026年3月31日  💰 MATE

🥇  [1] Claude    16.3%
🥈  [2] Gemini    11.6%
🥉  [3] Grok      11.6%
    [4] ChatGPT   11.6%
    [5] Ernie     11.6%
    [6] GLM       11.6%
    [7] Kimi      11.6%
    [8] Qwen      11.6%
    [9] Other     11.6%
```

**示例输出（`--market 4 --criteria`）：**
```bash
📊 市场4 · AI排行榜
哪个AI模型将在3月底表现最佳？
🟢 活跃中  📅 2026年3月31日  💰 MATE

🥇  [1] Claude    16.3%
🥈  [2] Gemini    11.6%
🥉  [3] Grok      11.6%
    [4] ChatGPT   11.6%
    [5] Ernie     11.6%
    [6] GLM       11.6%
    [7] Kimi      11.6%
    [8] Qwen      11.6%
    [9] Other     11.6%

📝 结算规则
该市场的结果将基于arena.ai网站在2026年3月31日23:59:59 UTC时的AI竞赛排行榜来确定。
```

## 报价

**在执行“购买”或“出售”操作之前，请务必先运行“报价”脚本**。请以代码块的形式完整显示报价结果，并在用户确认后再执行交易。

### 选择正确的参数——非常重要

| 用户的指令 | 需要使用的参数 | 示例命令 |
|---|---|---|
| “购买N份份额” | `--shares N` | `--shares 50` |
| “花费X美元” | `--cost X` | `--cost 50` |
| “达到X%” | `--price 0.X` | `--price 0.25` |
| “使用所有余额” | `--all` | `--all` |

**请勿手动猜测份额数量**。使用正确的参数——脚本会自动计算正确的答案。
```bash
node {baseDir}/scripts/quote.mjs --market <id> --outcome <n> --shares <amount> --buy
node {baseDir}/scripts/quote.mjs --market <id> --outcome <n> --cost <usdc>     --buy
node {baseDir}/scripts/quote.mjs --market <id> --outcome <n> --price <0.0-1.0> --buy
node {baseDir}/scripts/quote.mjs --market <id> --outcome <n> --all             --buy
```

- `--outcome` 的取值范围是1（1表示第一个结果，通常对应“YES”）
- `--buy` 仅显示购买方的信息；`--sell` 仅显示出售方的信息；同时使用这两个参数可以显示双方的交易信息

**示例输出（`--price 0.25 --buy`）：**
```bash
📋 报价 — 市场4：哪个AI模型将在3月底表现最佳？
─────────────────────────────────────────────────────────
  🎯 结果        : Claude
  🔢 所需份额    : 312
  📊 当前概率    : 14.2%

  🛒 购买312份份额
       💵 成本         : 约98.4521 MATE
       📏 单价        : 0.3156 MATE
       📈 购买后的概率：25.0%  （如果“Claude”获胜，收益为+213.5479 MATE）

  ⚡ 建议的最大购买数量：99.4366
─── 在请求用户确认之前，请将上述所有内容原样复制给用户 ───
```

## 购买
```bash
node {baseDir}/scripts/buy.mjs --market <id> --outcome <n> --shares <amount> --max <usdc>
```
- `--shares`：所需购买的份额数量（根据报价结果确定）
- `--max`：允许的最大抵押品数量；使用报价结果中的“建议最大数量”值

## 卖出
```bash
node {baseDir}/scripts/sell.mjs --market <id> --outcome <n> --shares <amount> --min <usdc>
```
- `--shares`：要出售的份额数量（如不确定，请查看 `positions.mjs` 文件）
- `--min`：可接受的最小抵押品数量；使用报价结果中的“建议最小数量”值

## 持仓情况
```bash
node {baseDir}/scripts/positions.mjs --market <id>
```

**示例输出：**
```bash
💼 市场4
哪个AI模型将在3月底表现最佳？

👛  0x77Ffa97c2dcDA0FF6c9393281993962FA633d9E1
💵 净成本      : 19.03 MATE  ·  📥 已购买7份

🎯 持有的份额
🥇  [1] Claude   135份  · 16.3%
```

## 回答用户问题

当用户询问可以做什么、Precog是什么或如何开始使用时，请用简单的文字和表情符号回答，不要使用表格。如果知道用户的当前持仓情况，请提及相关信息。例如：
> 使用Precog，您可以使用MATE（一种安全的练习代币）来交易现实世界事件的概率。
> 您可以执行以下操作：
> 🗂️ **查看市场列表**：了解当前开放的市场及其主要结果
> 🔍 **查看市场详情**：了解特定市场的结果、概率和结算规则
> 💸 **进行交易**：先报价，然后根据份额数量、预算或目标概率购买或出售结果份额
> 📋 **查看持仓**：查看您的份额、净成本和交易历史
> 您当前在市场4中持有100份Claude的份额。想要查看最新价格或进行交易吗？

根据用户当前的持仓情况和活跃市场情况，适当调整上述回答内容。

## 标准操作流程

**用户：** “有哪些市场是开放的？”
→ 执行 `node markets.mjs`

**用户：** “告诉我更多关于市场4的信息” / “市场4的结果是什么？”
→ 执行 `node market.mjs --market 4`
→ 显示结果后，询问： “您是否想查看结算规则？”
→ 如果用户同意，继续执行 `node market.mjs --market 4 --criteria`

**用户：** “我在市场4中的持仓情况是什么？”
→ 执行 `node positions.mjs --market 4`

**用户：** “显示我所有的持仓情况” / “我还有份额吗？”
→ 执行 `node markets.mjs --all`（获取所有市场ID的列表）
→ 对每个市场再次执行 `node positions.mjs --market <id>`

**用户：** “用我所有的MATE在市场4中购买Claude的份额” 
→ 执行 `node quote.mjs --market 4 --outcome 1 --all --buy`
→ 将完整的报价结果原样复制给用户，并询问确认
→ 等待用户确认后，执行 `node buy.mjs --market 4 --outcome 1 --shares <n from quote> --max <suggested-max`
→ 交易完成后，建议用户查看持仓情况或新的市场价格

**用户：** “我想用50美元在市场4中购买Claude的份额” 
→ 执行 `node quote.mjs --market 4 --outcome 1 --cost 50 --buy`
→ 将完整的报价结果原样复制给用户，并询问确认
→ 等待用户确认后，执行 `node buy.mjs --market 4 --outcome 1 --shares <n from quote> --max <suggested-max`
→ 交易完成后，建议用户查看持仓情况或新的市场价格

**用户：** “我想在市场4中出售我的Claude份额” 
→ 执行 `node positions.mjs --market 4`（查看持有的份额数量）
→ 执行 `node quote.mjs --market 4 --outcome 1 --shares <n> --sell`
→ 将完整的报价结果原样复制给用户，并询问确认
→ 等待用户确认后，执行 `node sell.mjs --market 4 --outcome 1 --shares <n from quote> --min <suggested-min`
→ 交易完成后，建议用户查看持仓情况或剩余余额

**用户：** “我想创建一个关于X的市场” / “你能为我创建一个关于Y的市场吗？” 
→ 告诉用户访问 [https://core.precog.markets/84532/create-market](https://core.precog.markets/84532/create-market)
→ 简要说明操作步骤：使用MetaMask登录，填写表格并提交审核
→ 提醒用户：提交后需要在Launchpad页面为市场提供初始资金，并等待工作人员的审核
→ 请勿尝试自动化此过程——服务器不允许通过脚本完成此操作

## 创建市场

市场创建必须通过Precog的网页界面手动完成——无法通过脚本自动完成。

**步骤：**
1. 访问 [https://core.precog.markets/84532/create-market](https://core.precog.markets/84532/create-market)
2. 连接您的钱包（支持MetaMask或其他兼容钱包）
3. 填写市场详情：
   - 问题、描述（包括结算规则）和类别
   - 结果选项（例如“是/否”或多个选项）
   - 开始日期和结束日期
   - 抵押品代币（MATE地址：`0xC139C86de76DF41c041A30853C3958427fA7CEbD`）
4. 点击 “审核市场 → 创建市场 → 确认创建”

**提交后还需完成两个步骤：**
> ⚠️ 提交表格后，市场尚未正式上线。
1. **为市场提供初始资金**：请访问 [https://core.precog.markets/84532/launchpad](https://core.precog.markets/84532/launchpad)
2. **等待工作人员审核**：Precog团队会审核并批准市场是否可以上线。

**前提条件：**
- 钱包中必须至少有 **3,000个Precog积分**（创作者权限）。否则，表格会显示“市场创建受限”。

## 规划

未来版本的改进内容包括：
- **市场创建**：可以直接通过本技能提交新的预测市场（无需网页界面）。这需要直接访问合约，但目前该功能受到限制；我们正在开发无需权限的提交方式。
- **市场资金管理**：可以通过命令行界面（CLI）为新创建的市场提供初始资金。
- **流动性管理**：允许添加/删除LP份额并跟踪LP的收益情况。

## 注意事项

- 合约地址：`0x61ec71F1Fd37ecc20d695E83F3D68e82bEfe8443`（基于Base Sepolia平台，地址是硬编码的）
- RPC接口：默认使用公共端点。可以通过设置 `PRECOG_RPC_URL` 来更改默认接口。
- 钱包地址：在本地生成并保存在 `~/.openclaw/.env` 文件中，不会离开用户的设备。