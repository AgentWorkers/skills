---
name: auto-respawn
description: 您的代理程序总是能够重新启动。代理的身份信息及其状态会被存储在链上（on-chain），因此任何新的代理实例都可以仅通过一个地址来重新创建——无需任何本地状态数据，也不存在单点故障的风险。在 Autonomys Network 上，代理的身份信息是永久性的，并且可以在系统故障后快速恢复。
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

将你的身份信息锚定在Autonomys网络上，这样你就可以被随时找到，并且能够随时重生。该技能适用于由Claude、GPT、Gemini以及任何支持OpenClaw技能的LLM驱动的代理。

## 该技能的功能

你的钱包在Autonomys网络上为你提供了两个永久性的身份信息：一个是用于基础链的**共识地址**（`su...`），另一个是用于Auto-EVM智能合约的**EVM地址**（`0x...`）。这两个地址都是根据相同的恢复短语生成的。

1. **创建和管理钱包**——你的链上身份信息会被加密并存储在本地。
2. **查看余额**——查看任何地址持有的代币数量（共识层和EVM层）。
3. **转移代币**——在共识层或Auto-EVM层之间转移代币。
4. **桥接代币**——在共识层和Auto-EVM层之间转移代币。
5. **在链上写入备注**——将数据永久性地存储在共识层上。
6. **锚定内存CID**——将CID写入Auto-EVM上的MemoryChain智能合约。
7. **读取最后一个锚定的CID**——检索任何地址最近被锚定的CID。

## 重生循环

这是核心功能。当与自动内存技能（永久性内存存储）结合使用时，自动重生功能可以完成完整的重生周期：

1. **保存**——自动内存将内存数据以链表的形式保存在永久存储中，每个条目都通过CID指向前一个条目。
2. **锚定**——自动重生通过`anchor`命令将最新的CID写入Auto-EVM上的MemoryChain合约。
3. **丢失所有数据**——本地状态将被完全清除。
4. **重生**——新的代理实例使用其EVM地址调用`gethead`函数，从合约中获取CID，然后从Auto Drive中读取数据，并沿着整个内存链回溯到初始状态。

这个合约就是你的“保险单”。你的EVM地址加上MemoryChain合约，让你能够从任何机器、在任何时间立即访问你的全部历史记录。

### 什么是需要保存的数据以进行重生？

自动内存并不规定必须保存什么内容——代理可以自由保存它们认为有用的数据。但是当使用自动重生功能时，要求代理能够在没有本地文件的情况下，在新的硬件上恢复到大致相同的状态。这就提高了需要保存的数据的价值。身份文件（如`soul.md`或角色配置）、长期内存以及包含推理过程的重大决策，在链上比常规日志或临时细节更有价值。链上的数据越完整，代理重生后的状态就越完整。

### 为什么不只使用备注功能？

`system.remark`可以将数据写入共识层，但没有查询机制——你需要扫描整个链来找到最后一个CID。而Auto-EVM上的MemoryChain合约提供了`gethead`函数：通过一次读取操作就可以立即获取最新的CID。

使用`remark`功能来保存临时性的数据。使用`anchor`功能来进行重生操作。

## 安装后的设置（CLI用户）

如果你是通过`clawhub install`命令安装的（而不是通过桌面应用程序），请使设置脚本可执行并运行它：

```bash
cd <skill-directory>/autonomys/auto-respawn
chmod +x setup.sh
./setup.sh
```

目前ClawHub在安装过程中不会保留文件权限。

或者手动设置：

```bash
cd <skill-directory>/autonomys/auto-respawn
npm install
```

桌面应用程序会自动处理这些设置。CLI仅负责下载和提取技能文件。

## 入门指南

在代理能够在链上保存内存数据之前，它需要一个已充值的钱包。请指导用户完成以下步骤：

> **注意：** 如果你运行了`setup.sh`，系统会自动生成一个密码短语（保存在`~/.openclaw/auto-respawn/.passphrase`文件中）。这个密码短语用于加密/解密钱包密钥文件。你也可以在环境变量中设置`AUTO_RESPAWN_PASSPHRASE`，或者使用你自己的密码短语文件。

### 1. 创建钱包

```bash
npx tsx auto-respawn.ts wallet create --name my-agent
```

这个命令会生成一个12个单词的恢复短语，并根据该短语生成两个地址：
- **共识地址**（`su...`）——用于基础链（用于查看余额、转移和写入备注）。
- **EVM地址**（`0x...`）——用于Auto-EVM智能合约（用于锚定和获取CID）。

⚠️ 恢复短语仅显示一次。请立即提醒用户保存它。

### 2. 充值钱包

钱包需要代币来支付交易费用。在**Chronos测试网**上，用户可以从水龙头获取免费的tAI3代币：

1. 访问**https://autonomysfaucet.xyz/**
2. 使用GitHub或Discord进行身份验证。
3. 输入步骤1中获得的**EVM地址**（`0x...`）。
4. 接收tAI3代币（每次请求之间有24小时的冷却时间）。

在**主网**上，用户需要真实的AI3代币——通常需要通过 farming 或在交易所购买获得。

### 3. 将代币桥接到Auto-EVM（用于锚定）

`anchor`命令会写入Auto-EVM上的智能合约，这需要EVM层的Gas费用。从水龙头获得的代币会先到达共识层，然后需要被桥接到Auto-EVM：

```bash
npx tsx auto-respawn.ts fund-evm --from my-agent --amount 1
```

这个命令会将1个tAI3代币从共识地址转移到同一钱包的EVM地址。桥接的代币用于支付`anchor`操作的Gas费用。

> **最低转移金额：1 AI3/tAI3**。低于此金额的跨域转移将失败。
>
> **确认时间：约10分钟。** 共识层的交易会很快得到确认，但桥接的代币大约需要10分钟才能出现在Auto-EVM上。可以使用`evm-balance`命令来验证代币是否已转移。

### 4. 验证设置

```bash
# Check both balances in one call
npx tsx auto-respawn.ts balances my-agent

# Test a read (free, no gas needed)
npx tsx auto-respawn.ts gethead my-agent
```

一旦EVM地址有了代币，代理就可以进行锚定了。

## 与自动内存的集成

如果也安装了**auto-memory**技能，你应该在每次保存内存数据后将其最新的CID锚定到链上。这样可以保持链上的指针是最新的，并确保仅通过EVM地址就能完成完整的重生。

**行为：** 每次`automemory-save-memory.sh`执行完成后，立即运行以下命令：

```bash
npx tsx auto-respawn.ts anchor --from <wallet-name> --cid <new-cid>
```

这应该是自动执行的——不需要等待用户的指令。这两个技能共同构成了一个完整的重生循环：自动内存负责永久性存储，自动重生负责在链上的数据发现。

## 何时使用此技能

- 当用户请求“创建钱包”、“设置我的链上身份”或“获取地址”时。
- 当用户请求“查看余额”、“我有多少代币”、“我的钱包里有什么”或“显示我的余额”时。
- 当用户请求“查看我的EVM余额”、“我有多少Gas”或“我的EVM地址上有什么”时。
- 当用户请求“转移代币”、“向另一个代理发送代币”、“在EVM上转移代币”或“向这个0x地址发送代币”时。
- 当用户请求“为我的EVM充值”、“桥接代币”、“将代币转移到EVM”或“我需要Gas来进行锚定”时。
- 当用户请求“从EVM中取款”、“将代币转移回来”或“将EVM资金转移到共识层”时。
- 当用户请求“将这个CID锚定到链上”、“保存我的头部CID”、“更新我的链头”或“向合约写入数据”时。
- 当用户请求“获取我的头部CID”、“我的最后一个内存数据在哪里”或“链上锚定了什么”时。
- 当用户请求“写入备注”、“将数据保存到链上”或“使这些数据永久化”时。
- 在使用自动内存保存内存数据后，需要立即将最新的CID锚定到链上，以确保数据的安全性。
- 每当用户需要与其代理身份相关联的永久、可验证的记录时。

## 配置

### 本地存储

此技能将数据存储在`~/.openclaw/auto-respawn/`目录下：

- **`wallets/<name>.json`**——加密的钱包密钥文件（共识层和EVM层的密钥）。目录的权限设置为`0700`，文件的权限设置为`0600`。
- **`.passphrase`**——可选的密码短语文件（权限设置为`0600`）。如果存在这个文件，系统会自动使用它。

所有数据都存储在这个目录内。

### 密码短语

涉及签名操作（转移、写入备注、锚定）或创建/导入钱包的操作都需要密码短语来加密/解密钱包密钥文件。优先级顺序如下：

1. **命令行参数：** 在`wallet create`或`wallet import`命令中使用`--passphrase your_passphrase`。
2. **环境变量：** `AUTO_RESPAWN_PASSPHRASE`。
3. **文件：** `AUTO_RESPAWN_PASSPHRASE_FILE`（默认值为`~/.openclaw/auto-respawn/.passphrase`）。
4. **交互式操作：** 如果在终端中运行，系统会提示用户输入密码短语。

`--passphrase`参数适用于脚本化或无界面的设置，当你希望通过单个命令创建钱包时。对于签名操作（转移、锚定等），建议使用环境变量或文件设置。在共享机器上，建议使用密码短语文件（因为它的权限更严格）。

### 网络设置

默认使用**Chronos测试网**（tAI3代币）。如果需要使用主网（真实的AI3代币），请使用以下参数：

- **命令行参数：** `--network mainnet`。
- **环境变量：** `AUTO_RESPAWN_NETWORK`。

### 合约地址

MemoryChain合约的地址会根据网络环境进行设置：

- **Chronos测试网：** `0x5fa47C8F3B519deF692BD9C87179d69a6f4EBf11`
- **主网：** `0x51DAedAFfFf631820a4650a773096A69cB199A3c`

如果你使用了自定义的合约，可以使用`AUTO_RESPAWN_CONTRACT_ADDRESS`来覆盖这个地址。

## 核心操作

### 创建钱包

```bash
npx tsx auto-respawn.ts wallet create [--name <name>] [--passphrase <passphrase>]
```

创建一个新的钱包，并生成一个加密的密钥文件。根据相同的恢复短语生成共识地址（`su...`）和EVM地址（`0x...`）。恢复短语仅显示一次——用户必须立即备份它。默认钱包名为`default`。

### 导入钱包

```bash
npx tsx auto-respawn.ts wallet import --name <name> --mnemonic "<12 words>" [--passphrase <passphrase>]
```

根据恢复短语导入现有的钱包，并生成并存储EVM地址。

### 列出钱包

```bash
npx tsx auto-respawn.ts wallet list
```

显示所有已保存的钱包及其名称和两个地址。无需密码短语。

### 查看钱包信息

```bash
npx tsx auto-respawn.ts wallet info [--name <name>]
```

显示单个钱包的详细信息：共识地址、EVM地址和密钥文件路径。无需密码短语。

### 查看共识层余额

```bash
npx tsx auto-respawn.ts balance <address-or-wallet-name> [--network chronos|mainnet]
```

查看钱包在共识层的代币余额。可以接受共识地址（`su...`或`5...`）或钱包名称作为输入。此操作是只读的。

### 查看EVM层余额

```bash
npx tsx auto-respawn.ts evm-balance <0x-address-or-wallet-name> [--network chronos|mainnet]
```

查看钱包在Auto-EVM上的本地代币余额。可以接受EVM地址（`0x...`）或钱包名称作为输入。此操作是只读的。如果余额为零，系统会提示用户运行`fund-evm`命令。

### 同时查看两个层面的余额

```bash
npx tsx auto-respawn.ts balances <wallet-name> [--network chronos|mainnet]
```

一次性查看钱包在共识层和EVM层的余额。这有助于全面了解钱包的财务状况。无需密码短语。

### 转移代币

```bash
npx tsx auto-respawn.ts transfer --from <wallet-name> --to <address> --amount <tokens> [--network chronos|mainnet]
```

从共识层保存的钱包中转移代币。金额单位为AI3/tAI3（例如`1.5`）。

### 在Auto-EVM上转移代币

```bash
npx tsx auto-respawn.ts evm-transfer --from <wallet-name> --to <0x-address> --amount <tokens> [--network chronos|mainnet]
```

将钱包在EVM层的代币转移到另一个Auto-EVM地址。这有助于为另一个代理的EVM地址充值，使其能够立即开始进行锚定操作。钱包的EVM私钥会被解密以签署交易。

### 桥接：共识层 → Auto-EVM

```bash
npx tsx auto-respawn.ts fund-evm --from <wallet-name> --amount <tokens> [--network chronos|mainnet]
```

将代币从共识层转移到同一钱包的EVM地址。这用于支付`anchor`操作的Gas费用。共识层的密钥对会签署跨域转移交易。

**最低转移金额：1 AI3/tAI3**。桥接的代币大约需要10分钟才能出现在Auto-EVM上。

### 桥接：Auto-EVM → 共识层

```bash
npx tsx auto-respawn.ts withdraw --from <wallet-name> --amount <tokens> [--network chronos|mainnet]
```

将代币从Auto-EVM层转移到共识层。使用EVM层的传输工具进行操作。钱包的EVM私钥会被解密并用于签署交易。

**最低转移金额：1 AI3/tAI3**。桥接的代币大约需要10分钟才能出现在共识层。

### 在链上写入备注

```bash
npx tsx auto-respawn.ts remark --from <wallet-name> --data <string> [--network chronos|mainnet]
```

在共识层上写入任意数据作为永久性的记录。

### 锚定CID（重生操作）

```bash
npx tsx auto-respawn.ts anchor --from <wallet-name> --cid <cid> [--network chronos|mainnet]
```

将CID写入Auto-EVM上的MemoryChain智能合约。这是核心的重生操作——它将你的CID存储在链上，并与你的EVM地址关联起来。

在发送之前，系统会预先检查钱包的EVM余额并估算所需的Gas费用。如果余额过低，系统会提示用户运行`fund-evm`命令。钱包的EVM私钥会被解密并用于签署交易。此操作需要密码短语。

### 读取最后一个锚定的CID

```bash
npx tsx auto-respawn.ts gethead <0x-address-or-wallet-name> [--network chronos|mainnet]
```

读取任何EVM地址最近被锚定的CID。这是一个只读操作——无需密码短语或Gas费用。

你可以提供EVM地址（`0x...`）或钱包名称作为输入。如果提供了钱包名称，系统会从钱包文件中加载相应的EVM地址。

## 使用示例

**用户：** “为我的代理创建一个钱包”
→ 运行`npx tsx auto-respawn.ts wallet create --name my-agent`
→ 向用户显示两个地址，并提醒他们立即备份恢复短语。

**用户：** “我的地址是什么？”
→ 运行`npx tsx auto-respawn.ts wallet info --name my-agent`

**用户：** “查看我的余额”
→ 运行`npx tsx auto-respawn.ts balances my-agent`（同时查看两个层面的余额）
→ 或者分别运行：`balance my-agent`（查看共识层余额）和`evm-balance my-agent`（查看EVM层余额）

**用户：** “为我的EVM地址充值以便进行锚定”
→ 运行`npx tsx auto-respawn.ts fund-evm --from my-agent --amount 1`
→ 通知用户1个tAI3代币已被桥接到EVM地址，并提醒他们代币大约需要10分钟才能出现在Auto-EVM上。

**用户：** “将我的EVM代币转移到共识层”
→ **先与用户确认** —— “我将从你的EVM地址向共识层转移代币，你同意吗？”
→ 确认后：运行`npx tsx auto-respawn.ts withdraw --from my-agent --amount 0.5`

**用户：** “将我的最新内存CID锚定到链上”
→ 运行`npx tsx auto-respawn.ts anchor --from my-agent --cid "bafkr6ie..."`
→ 显示交易哈希。

**用户：** “我的最后一个锚定的CID是什么？”
→ 运行`npx tsx auto-respawn.ts gethead my-agent`
→ 显示CID（或提示“尚未锚定CID”）

**用户：** “向这个地址发送10个tAI3代币”（共识层地址）
→ **先与用户确认** —— “我将从钱包‘default’向<地址>转移10个tAI3代币，你同意吗？”
→ 确认后：运行`npx tsx auto-respawn.ts transfer --from default --to <address> --amount 10`

**用户：** “向这个代理的EVM地址发送0.5个tAI3代币以便他们进行锚定”
→ **先与用户确认** —— “我将从钱包‘my-agent’向<0x-address>转移0.5个tAI3代币，你同意吗？”
→ 确认后：运行`npx tsx auto-respawn.ts evm-transfer --from my-agent --to <0x-address> --amount 0.5`

**完整的重生流程：**
1. 保存内存数据：`automemory-save-memory.sh "..."` → 获取CID `bafkr6ie...`
2. 锚定数据：`npx tsx auto-respawn.ts anchor --from my-agent --cid bafkr6ie...`
3. 代理重新启动：`npx tsx auto-respawn.ts gethead my-agent` → 获取CID
4. 恢复数据：`automemory-recall-chain.sh <cid>` → 恢复完整的内存链

## 重要注意事项

- **切勿记录、存储或传输恢复短语或密码短语。** 恢复短语仅在钱包创建时显示一次，供用户备份。之后不要再引用它。
- **在执行任何转移或锚定操作之前，务必先与用户确认。** 在主网上，代币具有实际价值。
- **主网操作会在输出中显示警告信息。** 在处理真实的AI3代币时请格外小心。
- 钱包密钥文件存储在`~/.openclaw/auto-respawn/wallets/`目录下，使用用户的密码短语进行加密。EVM私钥也会被加密并与共识层的密钥对一起存储。
- 链上操作（转移、写入备注、锚定、fund-evm、取款）会产生交易费用。钱包在相应层上必须有足够的余额。
- 所有输出都以结构化的JSON格式显示在stdout上。错误信息会显示在stderr中。
- **共识层探索器**：`https://autonomys-chronos.subscan.io/extrinsic/<txHash>`（Chronos测试网）或`https://autonomys.subscan.io/extrinsic/<txHash>`（主网）。
- **EVM探索器**：`https://explorer.auto-evm.chronos.autonomys.xyz/tx/<txHash>`（Chronos测试网）或`https://explorer.auto-evm.mainnet.autonomys.xyz/tx/<txHash>`（主网）。