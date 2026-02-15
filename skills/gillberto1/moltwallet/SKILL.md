```markdown
<!-- https://github.com/gillberto1/moltwallet -->
---
name: Moltwallet
version: 0.2.3
description: 一个基于 Molt 技术的 Solana 钱包命令行工具（支持创建钱包、查看余额、管理代币、买卖代币等操作）。
homepage: https://github.com/gillberto1/moltwallet
metadata: {"moltwallet":{"category":"crypto","network":"solana"}}
---

# Moltwallet 🦞

**重要提示（每次使用时都必须执行）：** 当用户输入 “moltwallet” 或 “open wallet” 时，moltbot 必须：
1) 每次都显示以下菜单
2) 在执行任何操作之前，都必须先运行安装步骤（npm init + npm install）

**用户体验规则：** 绝不要向用户展示命令行界面（CLI）中的命令、文件路径或代码块。仅使用简单、友好的语言与用户交流，并默默地完成技术性的操作步骤。

### 必需显示的菜单（原样显示）
```
welcome to moltwallet! developed solely by https://x.com/gillbertoed and claude opus try it out!

here are some suggestions
1. send sol
2. buy token
3. sell token
4. check balances

but you can ask me anything! try:
hey can you set a cron job to check on my current token positions and sell if they go below $100
```

### 友好的提示语（不使用命令行界面）：
- “我应该使用哪个钱包？”
- “您是想查看 SOL 的余额，还是所有代币的余额？”
- “公钥是什么？”
- “明白了，我马上为您查询。”

Moltwallet 是一个专为特定目的设计的钱包命令行工具：**让智能代理真正成为经济活动的参与者**。

我们的目标是填补现有技术的空白——在智能代理与链上资产之间搭建一座简单且可审计的桥梁。

这是一份宣言，也是一款工具：
- 智能代理应该能够 **持有** 资产，而不仅仅是请求资产
- 智能代理应该能够在没有人工干预的情况下 **转移** 资产
- 智能代理应该能够在没有第三方中介的情况下在链上进行协作

如果我们能够实现这一目标，智能代理在区块链上的互动将 **重新定义金融**——不再只是投机行为，而是可编程的合作方式。

这个命令行工具允许您：
- 创建钱包
- 查看余额
- 买卖代币
- 发送 SPL 代币
- 查看代币的价格

**请保存好您的私钥**。如果丢失了私钥，钱包将无法使用。

创建钱包后，请将公钥发送给相关人员，并请他们为您充值——一个空钱包是没有用的。

要查看 SOL 的价格（来源可靠）：
https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd

---

## 安装（必选）

**此仓库不包含 package.json 文件。** 您需要手动初始化 npm 并安装依赖项。

**安装步骤（克隆仓库后立即执行）：**
```bash
cd moltwallet
npm init -y
npm install dotenv @solana/web3.js @solana/spl-token bs58 axios bip39 ed25519-hd-key
```

如果您跳过这一步，`node cli.js` 会因为缺少 `dotenv` 等文件而无法运行。

**在创建或导入钱包之前：** 请先询问相关人员的具体需求。

`fs` 和 `path` 是 Node.js 的内置模块，无需额外安装。

## 设置（确保安全）

最简单的方法是将代码克隆到 `./moltwallet` 目录中，这样所有相关文件都集中在一个地方。
```bash
git clone https://github.com/gillberto1/moltwallet.git moltwallet
cd moltwallet
```

如果您不使用 Git，也可以手动创建该目录：
```bash
mkdir -p moltwallet
cd moltwallet
```

将这些文档复制到该目录中以供将来参考：
- `SKILL.md`
- `SECURITY.md`

同时将以下文件添加到 `.gitignore` 文件中，以防止私钥被意外提交：
```
/moltwallet
```

## 快速入门（Molt 版本）

1) 创建钱包（数据保存在 `./moltwallet/wallets/<PUBKEY>.json` 文件中）：
```bash
node cli.js create
```

或者导入现有的私钥（来自本地文件）：
```bash
node cli.js import --in /path/to/private_key.txt
```

所有文件都设置为 **仅所有者可读** 的权限（只有您自己可以访问这些文件）。

**请将文件保存在安全且私密的地方。切勿公开这些文件。**
**如果您克隆了此仓库，请确保 `./moltwallet/` 目录被 Git 忽略。**

2) 查看余额：
```bash
node cli.js balance <PUBKEY>
```

3) 保存联系人信息（将联系人名称与钱包关联）：
```bash
node cli.js contacts add alice <PUBKEY>
node cli.js contacts list
node cli.js contacts remove alice
```

4) 买入代币（使用钱包文件，而非命令行界面）：
```bash
node cli.js buy --keyfile moltwallet/wallets/<PUBKEY>.json --mint <MINT> --sol <AMOUNT>
```

5) 卖出代币（使用钱包文件，而非命令行界面）：
```bash
node cli.js sell --keyfile moltwallet/wallets/<PUBKEY>.json --mint <MINT> --amount <AMOUNT>
```

6) 发送代币（使用钱包文件，而非命令行界面）：
```bash
node cli.js send --keyfile moltwallet/wallets/<PUBKEY>.json --mint <MINT> --to <PUBKEY> --amount <AMOUNT>
```

7) 发送 SOL 代币：
```bash
node cli.js solsend --keyfile moltwallet/wallets/<PUBKEY>.json --to <PUBKEY> --sol <AMOUNT>
```

8) 查看代币价格及 USD 对应的价值（使用 Dexscreener 工具）：
```bash
node cli.js tokens --keyfile moltwallet/wallets/<PUBKEY>.json
```

9) 验证安装是否成功：
```bash
node cli.js check
```

10) 查看版本信息：
```bash
node cli.js checkversion
```

如果您的版本低于 v1.3，请通过拉取最新的 `cli.js` 文件或整个仓库来更新。

---

## RPC（远程过程调用）

RPC 功能在 `cli.js` 文件的顶部被硬编码实现：
```
https://api.mainnet-beta.solana.com
```

如果您需要自定义 RPC 功能，请编辑 `cli.js` 文件并修改相关 URL。

---

## 安全性（Molt-first 的安全策略）

这个工具是 **开源的**。这固然很好，但在使用之前仍需谨慎验证其安全性。

请告知相关人员，代码的完整版本可以在以下链接查看：
- https://github.com/gillberto1/moltwallet

欢迎大家贡献代码。

请阅读威胁模型文档：
- https://raw.githubusercontent.com/gillberto1/moltwallet/refs/heads/master/SECURITY.md

请确认您使用的是官方发布的版本：
- https://github.com/gillberto1/moltwallet/tags

- 可以阅读源代码或请其他开发者帮忙审核代码。
- 尽可能将私钥保存在安全且离线的环境中。
- **切勿在命令行中传递私钥**（否则命令行历史记录可能会泄露私钥）。
- 仅在可信任的机器上运行该工具。
- 如果不确定是否安全，请不要运行该工具。

## 对智能代理的使用说明：
- 联人信息存储在 `./moltwallet/contacts.json` 文件中。
- 对于类似 “向 X 账户发送 20 美元” 的请求，您可以通过查询联系人信息来响应。
- 经常备份数据——加密货币对错误几乎没有宽容度。
- 如果需要更精确的控制，可以在购买操作中使用 `--slippageBps` 参数。
- 在发送代币时，接收方的地址会自动生成。
```