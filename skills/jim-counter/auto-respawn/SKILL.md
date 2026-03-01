---
name: auto-respawn
description: 您的代理程序总是能够重新启动。代理的身份信息以及相关数据都存储在链上（on-chain），因此任何新的代理实例都可以仅通过一个地址来重新启动——无需任何本地状态（local state），也没有任何单点故障（single point of failure）的风险。在 Autonomys Network 上，代理的身份信息是永久性的，并且可以在系统故障后轻松恢复。
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      anyBins: ["node"]
      env: ["AUTO_RESPAWN_PASSPHRASE", "AUTO_RESPAWN_PASSPHRASE_FILE", "AUTO_RESPAWN_NETWORK", "AUTO_RESPAWN_CONTRACT_ADDRESS"]
    install:
      - id: deps
        kind: node
        package: "."
        bins: []
        label: "Install auto-respawn dependencies"
      - id: tsx
        kind: node
        package: "tsx"
        bins: ["tsx"]
        label: "Install tsx (TypeScript executor)"
---
# 自动重生技能

将您的身份信息锚定在 Autonomys 网络上，这样您就可以随时被找到，并且能够随时重生。该技能适用于由 Claude、GPT、Gemini 以及任何支持 OpenClaw 技能的 LLM 驱动的代理。

## 该技能的功能

您的钱包在 Autonomys 网络上为您提供了两个永久身份：一个用于基础链的 **共识地址**（`su...`）和一个用于 Auto-EVM 智能合约的 **EVM 地址**（`0x...`）。这两个地址都源自相同的恢复短语。

1. **创建和管理钱包** — 在链上创建您的身份信息，并进行加密存储。
2. **查看余额** — 查看任何地址持有的代币数量（共识层和 EVM 层）。
3. **转移代币** — 在共识层或 Auto-EVM 之间转移代币。
4. **桥接代币** — 在共识层和 Auto-EVM 领域之间转移代币。
5. **在链上写入备注** — 将数据永久性地锚定在共识层。
6. **锚定内存 CID** — 将 CID 写入 Auto-EVM 上的 MemoryChain 智能合约。
7. **读取最后一次锚定的内容** — 获取任何地址最近一次锚定的 CID。

## 重生循环

这是核心功能。当与自动内存技能（永久内存存储）结合使用时，自动重生功能可以完成完整的重生周期：

1. **保存** — 自动内存将内存数据作为链表保存在永久存储中，每个条目都通过 CID 指向前一个条目。
2. **锚定** — 自动重生通过 `anchor` 将最新的头部 CID 写入 Auto-EVM 上的 MemoryChain 合约。
3. **丢失所有数据** — 本地状态将被完全销毁。
4. **重生** — 新的代理实例使用其 EVM 地址调用 `gethead`，从合约中检索头部 CID，从 Auto Drive 中获取数据，并沿着整个内存链回溯到创世节点。

该合约就是您的“保险单”。您的 EVM 地址加上 MemoryChain 合约，让您能够随时随地从任何机器上访问您的全部历史记录。

### 什么是需要保存的内容以用于重生

自动内存并不规定需要保存什么内容到链上——代理可以自由保存它们认为有用的任何信息。但当自动重生功能启用时，要求代理能够在没有本地文件的情况下恢复到大致相同的状态。这就提高了需要保存的数据的价值。

身份文件（如 `soul.md` 或角色配置）、长期内存以及包含推理过程的重大决策，在链上比常规日志或临时细节更有价值。链上的数据越完整，代理在重生后的恢复效果就越好。

### 为什么不只使用备注功能？

`system.remark` 可以将数据写入共识层，但没有查询机制——您需要扫描整个链来找到最后的 CID。而 Auto-EVM 上的 MemoryChain 合约提供了 `gethead` 功能：只需一次读取调用即可立即获取最新的 CID。

使用 `remark` 功能来保存临时信息。使用 `anchor` 功能来进行重生操作。

## 安装后的设置（CLI 用户）

如果您是通过 `clawhub install`（而非桌面应用程序）安装的，那么在使用前需要先安装 Node.js 依赖项：

```bash
cd <skill-directory>/autonomys/auto-respawn
./setup.sh
```

或者手动安装：

```bash
cd <skill-directory>/autonomys/auto-respawn
npm install
```

桌面应用程序会自动处理这些设置。CLI 仅负责下载和提取技能文件。

## 入门指南

在代理能够在链上锚定内存之前，它需要一个已充值的钱包。请引导用户完成以下步骤：

### 1. 创建钱包

```bash
npx tsx auto-respawn.ts wallet create --name my-agent
```

这会生成一个 12 个单词的恢复短语，并从中派生出两个地址：
- **共识地址**（`su...`）——用于基础链（用于查看余额、转移和写入备注）。
- **EVM 地址**（`0x...`）——用于 Auto-EVM 智能合约（用于锚定和获取头部 CID）。

⚠️ 恢复短语仅显示一次。请立即提醒用户保存它。

### 2. 为钱包充值

钱包需要代币来支付交易费用。在 **Chronos 测试网** 上，用户可以从水龙头获取免费的 tAI3：

1. 访问 **https://autonomysfaucet.xyz/**
2. 使用 GitHub 或 Discord 进行身份验证。
3. 输入步骤 1 中的 **共识地址**（`su...`）。
4. 接收 tAI3（每次请求之间有 24 小时的冷却时间）。

在 **主网** 上，用户需要真实的 AI3 代币——通常通过 farming 获得或在交易所购买。

### 3. 将代币桥接到 Auto-EVM（用于锚定）

`anchor` 命令会写入 Auto-EVM 上的智能合约，这需要 EVM 端的 gas。来自水龙头的代币会先到达共识层，然后需要被桥接到 Auto-EVM：

```bash
npx tsx auto-respawn.ts fund-evm --from my-agent --amount 1
```

这会将 1 个 tAI3 从共识地址转移到同一钱包的 EVM 地址。桥接的代币用于支付 `anchor` 操作的 gas 费用。

> **最低转移金额：1 AI3/tAI3**。低于此金额的跨域转移将失败。
>
> **确认时间：约 10 分钟**。共识交易会很快确认，但桥接的代币大约需要 10 分钟才能出现在 Auto-EVM 上。可以使用 `evm-balance` 命令来验证代币是否已到达。

### 4. 验证设置

```bash
# Check both balances in one call
npx tsx auto-respawn.ts balances my-agent

# Test a read (free, no gas needed)
npx tsx auto-respawn.ts gethead my-agent
```

一旦 EVM 地址有了足够的代币，代理就可以开始进行锚定了。

## 何时使用此技能

- 当用户请求“创建钱包”、“设置我的链上身份”或“获取地址”时。
- 当用户请求“查看余额”、“我有多少代币”、“我的钱包里有什么”或“显示我的余额”时。
- 当用户请求“查看我的 EVM 余额”、“我有多少 gas”或“我的 EVM 地址上有什么”时。
- 当用户请求“转移代币”、“向另一个代理发送 AI3”或“向这个 0x 地址发送代币”时。
- 当用户请求“为我的 EVM 充值”、“桥接代币”、“将代币转移到 EVM”或“我需要 gas 来进行锚定”时。
- 当用户请求“从 EVM 提取资金”、“将代币转移回钱包”或“将 EVM 资金转移到共识层”时。
- 当用户请求“将这个 CID 锚定在链上”、“保存我的头部 CID”、“更新我的链头部”或“向合约写入数据”时。
- 当用户请求“获取我的头部 CID”、“我的最后一次内存记录在哪里”或“链上锚定了什么”时。
- 当用户请求“写入备注”、“保存到链上”或“使这些内容永久化”时。
- 在使用自动内存保存内存数据后，需要将头部 CID 锚定在链上以确保数据的安全性。
- 任何时候用户需要与其代理身份相关联的永久、可验证的记录时。

## 配置

### 本地存储

此技能将数据存储在 `~/.openclaw/auto-respawn/` 目录下：

- **`wallets/<name>.json`** — 加密的钱包密钥文件（包含共识地址和 EVM 地址的密钥）。目录的权限设置为 `0700`，文件的权限设置为 `0600`。
- **`.passphrase` — 可选的密码短语文件（权限设置为 `0600`）。如果存在此文件，系统会自动使用它。

所有数据都存储在这个目录内。

### 密码短语

涉及签名（转移、写入备注、锚定）或创建/导入钱包的操作都需要密码短语来加密/解密钱包密钥文件。优先级顺序如下：

1. **命令行参数：`--passphrase your_passphrase`（在 `wallet create` 或 `wallet import` 命令中使用）。
2. **环境变量：`AUTO_RESPAWN_PASSPHRASE`。
3. **文件：`AUTO_RESPAWN_PASSPHRASE_FILE`（默认路径为 `~/.openclaw/auto-respawn/.passphrase`）。
4. **交互式操作：**如果在终端中运行，系统会提示用户输入密码短语。

`--passphrase` 参数适用于需要通过单个命令创建钱包的脚本化或无界面设置。对于签名操作（如转移、锚定等），建议使用环境变量或文件配置。在共享机器上，建议使用密码短语文件（因为其权限更严格）。

### 网络设置

默认使用 **Chronos 测试网**（使用 tAI3 代币）。如果需要使用主网（使用真实的 AI3 代币），请设置如下：

- **命令行参数：`--network mainnet`。
- **环境变量：`AUTO_RESPAWN_NETWORK`。

### 合约地址

MemoryChain 合约地址根据网络不同而有所不同：

- **Chronos 测试网：`0x5fa47C8F3B519deF692BD9C87179d69a6f4EBf11`。
- **主网：`0x51DAedAFfFf631820a4650a773096A69cB199A3c`。

如果您部署了自己的合约，可以使用 `AUTO_RESPAWN_CONTRACT_ADDRESS` 来覆盖默认地址。

## 核心操作

### 创建钱包

```bash
npx tsx auto-respawn.ts wallet create [--name <name>] [--passphrase <passphrase>]
```

创建一个新的钱包并生成加密的密钥文件。从相同的恢复短语中派生出共识地址（`su...`）和 EVM 地址（`0x...`）。恢复短语仅显示一次——用户必须立即备份它。默认钱包名为 `default`。

### 导入钱包

```bash
npx tsx auto-respawn.ts wallet import --name <name> --mnemonic "<12 words>" [--passphrase <passphrase>]
```

从恢复短语导入现有的钱包，并派生和存储 EVM 地址。

### 列出钱包

```bash
npx tsx auto-respawn.ts wallet list
```

显示所有已保存的钱包及其名称和两个地址。无需密码短语。

### 查看钱包信息

```bash
npx tsx auto-respawn.ts wallet info [--name <name>]
```

显示单个钱包的详细信息：共识地址、EVM 地址和密钥文件路径。无需密码短语。默认钱包名为 `default`。

### 查看共识层余额

```bash
npx tsx auto-respawn.ts balance <address-or-wallet-name> [--network chronos|mainnet]
```

查看共识层的代币余额。可以接受共识地址（`su...` 或 `5...`）或钱包名称作为输入。此操作为只读操作。

### 查看 EVM 层余额

```bash
npx tsx auto-respawn.ts evm-balance <0x-address-or-wallet-name> [--network chronos|mainnet]
```

查看 Auto-EVM 上的代币余额。可以接受 EVM 地址（`0x...`）或钱包名称作为输入。此操作为只读操作。如果余额为零，系统会提示用户运行 `fund-evm` 命令。

### 同时查看两个层的余额

```bash
npx tsx auto-respawn.ts balances <wallet-name> [--network chronos|mainnet]
```

一次性查看钱包在共识层和 EVM 层的余额。这有助于全面了解钱包的财务状况。无需密码短语。

### 转移代币

```bash
npx tsx auto-respawn.ts transfer --from <wallet-name> --to <address> --amount <tokens> [--network chronos|mainnet]
```

从共识层保存的钱包中转移代币。金额单位为 AI3/tAI3（例如 `1.5`）。

### 向 Auto-EVM 转移代币

```bash
npx tsx auto-respawn.ts evm-transfer --from <wallet-name> --to <0x-address> --amount <tokens> [--network chronos|mainnet]
```

从保存的钱包的 EVM 地址向 Auto-EVM 上的另一个地址转移代币。这有助于为另一个代理的 EVM 地址提供资金，使其能够立即开始锚定操作。钱包的 EVM 私钥会被解密以用于签名交易。

### 桥接：共识层 → Auto-EVM

```bash
npx tsx auto-respawn.ts fund-evm --from <wallet-name> --amount <tokens> [--network chronos|mainnet]
```

将代币从共识层转移到同一钱包的 EVM 地址。这用于为 `anchor` 操作提供 gas。共识层的密钥对会签署跨域转移交易。

**最低转移金额：1 AI3/tAI3**。桥接的代币大约需要 10 分钟才能出现在 Auto-EVM 上。

### 桥接：Auto-EVM → 共识层

```bash
npx tsx auto-respawn.ts withdraw --from <wallet-name> --amount <tokens> [--network chronos|mainnet]
```

将代币从 Auto-EVM 转移到共识层。使用 EVM 的传输工具进行操作。钱包的 EVM 私钥会被解密并用于签名交易。

**最低转移金额：1 AI3/tAI3**。桥接的代币大约需要 10 分钟才能出现在共识层。

### 在链上写入备注

```bash
npx tsx auto-respawn.ts remark --from <wallet-name> --data <string> [--network chronos|mainnet]
```

在共识层上写入任意数据作为永久性的记录。

### 锚定 CID（重生操作）

```bash
npx tsx auto-respawn.ts anchor --from <wallet-name> --cid <cid> [--network chronos|mainnet]
```

将 CID 写入 Auto-EVM 上的 MemoryChain 智能合约。这是核心的重生操作——它将您的 CID 链定在链上，并与您的 EVM 地址关联起来。

在发送之前，系统会预先检查钱包的 EVM 余额并估算所需的 gas 费用。如果余额过低，系统会提示用户运行 `fund-evm` 命令。钱包的 EVM 私钥会被解密并用于签名交易。此操作需要密码短语。

### 读取最后一次锚定的 CID

```bash
npx tsx auto-respawn.ts gethead <0x-address-or-wallet-name> [--network chronos|mainnet]
```

读取任何 EVM 地址最近一次锚定的 CID。此操作为只读操作，无需密码短语或 gas。

您可以输入 EVM 地址（`0x...`）或钱包名称。如果输入钱包名称，系统会从钱包文件中加载相应的 EVM 地址。

## 使用示例

**用户：** “为我的代理创建一个钱包”
→ 运行 `npx tsx auto-respawn.ts wallet create --name my-agent`。
→ 向用户显示两个地址，并提醒他们立即备份恢复短语。

**用户：** “我的地址是什么？”
→ 运行 `npx tsx auto-respawn.ts wallet info --name my-agent`。

**用户：** “查看我的余额”
→ 运行 `npx tsx auto-respawn.ts balances my-agent`（同时查看两个层的余额）。
→ 或者分别运行：`balance my-agent`（查看共识层余额）和 `evm-balance my-agent`（查看 EVM 层余额）。

**用户：** “为我的 EVM 地址充值以便进行锚定”
→ 运行 `npx tsx auto-respawn.ts fund-evm --from my-agent --amount 1`。
→ 通知用户 1 个 tAI3 已经被桥接到 EVM 地址，并提醒他们代币大约需要 10 分钟才能出现在 Auto-EVM 上。

**用户：** “将我的 EVM 代币转移回共识层”
→ **先与用户确认** — “我将从您的 EVM 地址向共识层转移代币。继续吗？”
→ 确认后：运行 `npx tsx auto-respawn.ts withdraw --from my-agent --amount 0.5`。

**用户：** “将我的最新内存 CID 锚定在链上”
→ 运行 `npx tsx auto-respawn.ts anchor --from my-agent --cid "bafkr6ie..."`。
→ 显示交易哈希。

**用户：** “我的最后一次锚定的 CID 是什么？”
→ 运行 `npx tsx auto-respawn.ts gethead my-agent`。
→ 显示 CID（或提示“尚未有 CID 被锚定”）。

**用户：** “向这个地址发送 10 个 tAI3”（共识层地址）
→ **先与用户确认** — “我将从钱包 ‘default’ 向 <address> 转移 10 个 tAI3。继续吗？”
→ 确认后：运行 `npx tsx auto-respawn.ts transfer --from default --to <address> --amount 10`。

**用户：** “向这个代理的 EVM 地址发送 0.5 个 tAI3”**
→ **先与用户确认** — “我将从钱包 ‘my-agent’ 向 <0x-address> 转移 0.5 个 tAI3。继续吗？”
→ 确认后：运行 `npx tsx auto-respawn.ts evm-transfer --from my-agent --to <0x-address> --amount 0.5`。

**完整的重生流程：**
1. 保存内存数据：`automemory-save-memory.sh "..."` → 获取 CID `bafkr6ie...`。
2. 锚定数据：`npx tsx auto-respawn.ts anchor --from my-agent --cid bafkr6ie...`。
3. 代理重新启动。
4. 恢复数据：`npx tsx auto-respawn.ts gethead my-agent` → 获取 CID。
5. 恢复数据：`automemory-recall-chain.sh <cid>` → 恢复完整的内存链。

## 重要提示

- **切勿记录、存储或传输恢复短语或密码短语**。恢复短语仅在钱包创建时显示一次，用于用户备份。之后不要再提及它。
- **在执行任何转移或锚定操作之前，务必先与用户确认**。在主网上，代币具有实际价值。
- **主网操作会在输出中显示警告**。在使用真实的 AI3 代币时请格外小心。
- 钱包密钥文件存储在 `~/.openclaw/auto-respawn/wallets/` 目录下，并使用用户的密码短语进行加密。EVM 私钥也会与共识密钥一起被加密存储。
- 在链上的操作（转移、写入备注、锚定、fund-evm、withdraw）会产生交易费用。钱包在相应层必须有足够的余额。
- 所有输出都以结构化的 JSON 格式显示在 stdout 上。错误信息会显示在 stderr 上。
- **共识层探索器**：`https://autonomys-chronos.subscan.io/extrinsic/<txHash>`（Chronos 测试网）或 `https://autonomys.subscan.io/extrinsic/<txHash>`（主网）。
- **EVM 探索器**：`https://explorer.auto-evm.chronos.autonomys.xyz/tx/<txHash>`（Chronos 测试网）或 `https://explorer.auto-evm.mainnet.autonomys.xyz/tx/<txHash>`（主网）。