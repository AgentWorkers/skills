---
name: gotchi-pocket
description: 使用 Bankr 在 Base 平台上管理 Aavegotchi 口袋钱包（托管服务）。当用户需要将 ERC20 代币存入 Aavegotchi 口袋、从口袋中提取 ERC20 代币、通过 Aavegotchi ID 查看口袋余额或所有权，或执行简单的命令时，可以使用该服务。
homepage: https://github.com/aavegotchi/aavegotchi-agent-skills
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
        - curl
        - python3
      env:
        - BANKR_API_KEY
    primaryEnv: BANKR_API_KEY
---
# Gotchi Pocket

使用 Aavegotchi 的功能在 Base 平台上发送和接收 ERC20 代币，并通过 Bankr 进行签名和提交操作。

## 该功能的用途

- 根据 Gotchi ID 查找对应的所有者地址和代币存储地址（“pocket”地址）
- 检查所有者和代币的余额
- 将 ERC20 代币从所有者的钱包存入指定的代币存储地址
- 使用 `transferEscrow()` 函数从代币存储地址中提取代币
- 强制执行所有者控制机制（默认情况下，操作必须通过所有者激活的 Bankr 钱包进行）
- 自动解析用户输入的简单英文命令并执行相应的脚本
- 对于涉及提取代币的命令，需要用户的明确授权

## 可用的脚本

- `./scripts/pocket-info.sh <gotchi-id> [--check-bankr]`
- `./scripts/pocket-balance.sh <gotchi-id> <token-alias-or-address>`
- `./scripts/pocket-deposit.sh <gotchi-id> <token-alias-or-address> <amount> [--raw]`
- `./scripts/pocket-withdraw.sh <gotchi-id> <token-alias-or-address> <to-address> <amount> [--raw]`
- `./scripts/pocket-command.sh [--approve-withdraw] [--dry-run] "<natural-language command>"`

## 自然语言命令支持

用户只需输入简单的英文命令，系统会自动解析并执行相应的操作。

**示例：**

```bash
./scripts/pocket-command.sh "send 25 GHST to gotchi 9638 pocket"
./scripts/pocket-command.sh "send 25 GHST from gotchi 9638 pocket to 0xb96b48a6b190a9d509ce9312654f34e9770f2110"
./scripts/pocket-command.sh "check pocket GHST balance for gotchi 9638"
./scripts/pocket-command.sh "show pocket info for gotchi 9638"
```

**注意：** 在执行交易前，系统会先预览命令的解析结果，但不会实际发送交易。

```bash
./scripts/pocket-command.sh --dry-run "send 25 GHST to gotchi 9638 pocket"
```

## 提取代币的安全性

除非用户明确授权，否则系统会阻止任何提取代币的操作。

```bash
# First call returns approval_required=true and exits without sending
./scripts/pocket-command.sh "send 25 GHST from gotchi 9638 pocket to 0xb96b48a6b190a9d509ce9312654f34e9770f2110"

# Approved execution
./scripts/pocket-command.sh --approve-withdraw "send 25 GHST from gotchi 9638 pocket to 0xb96b48a6b190a9d509ce9312654f34e9770f2110"
```

## 代币输入方式

支持使用代币的地址或别名进行输入：

- `GHST`
- `FUD`
- `FOMO`
- `ALPHA`
- `KEK`
- `USDC`
- `WETH`
- `DAI`

## 标准工作流程

1. 根据 Gotchi ID 查找对应的地址。
2. 在执行任何操作前，系统会先检查账户余额。
3. 根据用户指令执行代币的存入或提取操作。
4. 交易完成后，系统会再次检查账户余额。

## 其他注意事项

- 默认情况下，输入的金额单位为代币单位（例如 `100` GHST）。
- 仅当输入的金额已经是 Base 平台的单位时，才需要使用 `--raw` 选项。
- 系统默认会执行所有者身份验证；如果需要跳过此步骤，可以使用 `SKIP BANKR_OWNER_CHECK=1`。
- 所有交易都会使用 `waitForConfirmation=true` 选项，并返回交易生成的 BaseScan URL。

## 相关合约信息

- Aavegotchi Diamond（Base 平台）合约地址：`0xA99c4B08201F2913Db8D28e71d020c4298F29dBF`
- GHST（Base 平台）合约地址：`0xcD2F22236DD9Dfe2356D7C543161D4d260FD9BcB`