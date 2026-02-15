---
name: deepbook-cli
description: 使用 deepbook CLI 进行 DeepBook 的数据读取（支持 REST/SSE 协议）、全局配置文件（~/.deepbook）的编辑与管理、链上现货交易、顶层掉期交易（top-level swap execution）、余额管理（balance-manager operations）以及保证金交易（margin trading）等操作。
---

# DeepBook CLI 技能

当用户希望端到端使用 `deepbook` 时，可以使用此技能：查询市场数据、配置钱包、以及执行链上操作（包括现货交易、掉期交易、管理交易和保证金交易）。

## 安装

检查是否已安装 `deepbook`：

```bash
deepbook --version
```

如果未安装，请进行安装：

```bash
npm install -g deepbook-cli
```

## 设置

1. 在 `deepbook-cli` 项目目录下操作。
2. 确保 `~/.deepbook/config.json` 文件存在（首次运行时会自动生成）。
3. 在 `~/.deepbook` 目录中配置全局默认设置（从任何路径都可以使用这些设置）。
4. 仍可以通过全局参数提供一次性的自定义设置。

`mainnet` 和 `testnet` 是用于表示提供商端读取/数据流以及链上 RPC 的别名。

## 全局参数

- `--json`
- `--provider <名称>`
- `--base-url <网址>`
- `--stream-base-url <网址>`
- `--network <mainnet|testnet>`
- `--rpc-url <网址>`
- `--private-key <私钥>`
- `--address <地址>`
- `--manager <ID>`
- `--trade-cap <ID>`

## 可用命令

- **顶层命令**：
  - `deepbook providers`
  - `deepbook pools`
  - `deepbook orderbook <池名称>` （别名：`deepbook book <池名称>`）
  - `deepbook trades <池名称>`
  - `deepbook ohlcv <池名称>`
  - `deepbook stream ...`
  - `deepbook spot ...`
  - `deepbook swap ...`
  - `deepbook margin ...`
  - `deepbook manager ...`
  - `deepbook config ...`
  - `deepbook account ...`

- **`deepbook config` 命令**：
  - `show`
  - `set-network <网络>`
  - `set-provider <提供商>`
  - `set-rpc-url <网络> <网址>`
  - `set-address <地址>`
  - `set-trade-cap <ID>`
  - `set-read-key [API密钥]`
  - `set-stream-key <池名称> [API密钥]`
  - `set-provider-base-url <网络> <网址>`
  - `set-provider-stream-base-url <网络> <网址>`
  - `import-key [私钥]`

- **`deepbook account` 命令**：
  - `details`
  - `list`
  - `balance`
  - `import <别名> [私钥]`
  - `use <别名>`

- **`deepbook stream` 命令**：
  - `trades <池名称>`

- **`deepbook spot` 命令**：
  - `pools`
  - `buy <池名称>`
  - `sell <池名称>`
  - `limit <池名称>`

- **`deepbook swap` 命令**：
  - `base-for-quote <池名称>`
  - `quote-for-base <池名称>`

- **`deepbook margin` 命令**：
  - `pools`
  - `managers`
  - `deposit <池名称>`
  - `market <池名称>`
  - `limit <池名称>`
  - `position <池名称>`
  - `close <池名称>`

- **`deepbook manager` 命令**：
  - `ls`
  - `create`
  - `deposit`
  - `withdraw`
  - `balance`

## 命令速查表（必需参数/选项）

- `deepbook providers`
- `deepbook pools`
- `deepbook orderbook <池名称>`
- `deepbook trades <池名称>`
- `deepbook ohlcv <池名称>`
- `deepbook stream trades <池名称>`
- `deepbook spot pools`
- `deepbook spot buy <池名称> --数量 <数量> [--价格 <价格>] [--manager <ID>]`
- `deepbook spot sell <池名称> --数量 <数量> [--价格 <价格>] [--manager <ID>]`
- `deepbook spot limit <池名称> --方向 <买入|卖出> --价格 <价格> --数量 <数量> [--manager <ID>]`
- `deepbook spot limit <池名称> --取消 <ID> [--manager <ID>]`

- `deepbook config show`
- `deepbook config set-network <mainnet|testnet>`
- `deepbook config set-provider <提供商>`
- `deepbook config set-rpc-url <mainnet|testnet> <网址>`
- `deepbook config set-address <地址>`
- `deepbook config set-trade-cap <对象ID>`
- `deepbook config set-read-key [API密钥]`（或 `--stdin>`
- `deepbook config set-stream-key <池名称> [API密钥]`（或 `--stdin>`
- `deepbook config set-provider-base-url <mainnet|testnet> <网址>`
- `deepbook config set-provider-stream-base-url <mainnet|testnet> <网址>`
- `deepbook config import-key [私钥]`（或 `--stdin`，可选 `--别名`）

- `deepbook account details`
- `deepbook account list`
- `deepbook account balance [--币种 <SUI|USDC|DEEP|币种类型>]`
- `deepbook account import <别名> [私钥]`（或 `--stdin>`
- `deepbook account use <别名>`

- `deepbook swap base-for-quote <池名称> --金额 <数量>`
- `deepbook swap quote-for-base <池名称> --金额 <数量>`

- `deepbook margin pools`
- `deepbook margin managers`
- `deepbook margin deposit <池名称> --币种 <基础币|报价币|DEEP|币种键> --金额 <数量> [--保证金管理者 <ID>]`
- `deepbook margin market <池名称> --方向 <买入|卖出> --数量 <数量> [--保证金管理者 <ID>]`
- `deepbook margin limit <池名称> --方向 <买入|卖出> --价格 <数量> --数量 <数量> [--保证金管理者 <ID>]`
- `deepbook margin position <池名称> --保证金管理者 <ID>`
- `deepbook margin close <池名称> --保证金管理者 <ID>` + 可选参数：
  - `--全额`
  - 或 `--方向 <买入|卖出> --数量 <数量>`

- `deepbook manager ls`
- `deepbook manager create`
- `deepbook manager deposit --币种 <密钥> --金额 <数量> [--保证金管理者 <ID>]`
- `deepbook manager withdraw --币种 <密钥> --金额 <数量> [--保证金管理者 <ID>]`
- `deepbook manager balance --币种 <密钥> --保证金管理者 <ID>`

## 关键的保证金关闭参数

- `deepbook margin close <池名称> --全额 --withdraw`
- `deepbook margin close <池名称> --全额 --仅减少`
- `deepbook margin close <池名称> --方向 <买入|卖出> --数量 <数量> --仅减少 --不偿还`

## 掉期市场与现货市场的区别

- 掉期交易（`deepbook swap quote-for-base`）是直接在池中进行的对等交易。
- 现货市场买入（`deepbook spot buy <池名称> --数量 ...`）是通过订单簿进行的交易，并使用余额管理器来处理。
- CLI 输出现在会显示 `execution.kind` 和 `execution.type/direction`，以便明确交易模式。

## 安全性默认设置

- 对于所有会改变状态的命令，建议先使用 `--dry-run` 运行以进行测试。
- 在下达或取消订单之前，验证池的密钥和保证金管理器的 ID。
- 涉及 SUI 的存款/抵押品路径会自动从交易中的gas币种中分离出来。
- 绝不打印或记录私钥。
- 保证金管理器的安全性：
  - 保证金管理者是通用类型的对象：`MarginManager<Base, Quote>`。
  - 保证金管理器的类型必须与交易的池对匹配。
  - 例如：`MarginManager<DEEP,USDC>` 可用于 `DEEP_USDC`，但不能用于 `DEEP_SUI`。
- 保证金管理器的处理方式：
  - 如果省略了 `--margin-manager`，CLI 会自动为该池选择一个兼容的保证金管理者；如果不存在，则会在交易中创建一个。
  - 如果提供了 `--margin-manager`，CLI 会严格匹配该参数：必须确保管理器的类型与池匹配；不会进行回退或自动创建。
- 内部保证金费用缓冲区的处理方式：
  - 保证金市场/限价订单在下达前会自动扣除费用缓冲区。
  - 使用 `--no-pay-with-deep` 选项时，缓冲区会作为交易资产抵押品（卖出时的基础币种，买入时的报价币种）进行存放。
  - 不使用 `--no-pay-with-deep` 选项时，缓冲区会以 DEEP 的形式存入保证金管理者。
- 全额关闭时的数量处理：
  - `deepbook margin close <池名称> --全额` 会自动将计算出的数量调整为池的最低交易量。
  - 如果仅减少无法满足最低交易量，CLI 会切换到“仅减少”模式，并在同一个交易中偿还债务。
  - 如果用户明确指定了 `--reduce-only`，CLI 会保持“仅减少”的模式；如果无法表示为有效的交易量，则会报错。

## 端到端的现货交易流程（资金 -> 买入 -> 提取）

当通过余额管理者执行真实的现货交易时，请按照以下步骤操作：

1. 查找余额管理者：
   - `deepbook manager ls`
2. 如果没有找到，创建一个：
   - `deepbook manager create`
3. 向管理者存入报价币种（例如，对于 `DEEP_SUI` 的买入操作，需要存入 SUI）：
   - `deepbook manager deposit --币种 SUI --金额 1 --manager <ID>`
4. 可选：检查余额：
   - `deepbook manager balance --币种 SUI --manager <ID>`
5. 先进行模拟买入：
   - `deepbook spot buy DEEP_SUI --数量 38 --manager <ID> --no-pay-with-deep --dry-run`
6. 执行实际买入：
   - `deepbook spot buy DEEP_SUI --数量 38 --manager <ID> --no-pay-with-deep`
7. 将购买的资产提取到签名者的地址（或指定的接收者地址）：
   - `deepbook manager withdraw --币种 DEEP --金额 38 --manager <ID>`（可选接收者：`--recipient <地址>`）
8. 验证管理者的余额：
   - `deepbook manager balance --币种 DEEP --manager <ID>`

## 现货交易故障排除

- `MoveAbort ... balance_manager::withdraw_with_proof code=3` 表示管理者的可用余额过低。
  - 这包括费用和预留金额，而不仅仅是实际存入的余额。
  - 对于现货买入操作，确保报价币种已在管理者账户中充值（对于 `DEEP_SUI`，报价币种应为 SUI）。
  - 如果尝试使用 DEEP 作为支付币种而管理者账户中没有 DEEP，可以选择存入 DEEP 或使用 `--no-pay-with-deep` 选项。
  - 如果省略了管理者参数，CLI 会动态处理：
    - 找到一个管理者 -> 使用该管理者
    - 未找到管理者 -> 报错
    - 找到多个管理者 -> 需要指定 `--manager <ID>`

## 典型工作流程

1. 查看池和订单簿（`deepbook spot pools`、`deepbook margin pools`、`deepbook orderbook ...`）。
2. 确认保证金管理器的 ID（`deepbook manager ls`）。
3. 模拟订单（`deepbook spot buy ... --dry-run`）。
4. 执行实际订单（去掉 `--dry-run` 参数）。
5. 使用 `deepbook orderbook --watch` 和 `deepbook stream trades ...` 监控交易过程。