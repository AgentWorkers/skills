---
name: signet-guardian
description: "**AI代理的支付保护中间件**  
每当某个技能即将发起支付时，都需要使用该中间件。它会预先检查用户的支付政策（是否允许支付、单笔交易限额、每月支付上限等）。中间件会返回三种状态：`ALLOW`（允许支付）、`DENY`（拒绝支付）或`CONFIRM_REQUIRED`（需要进一步确认）。其他支持支付的技能在继续执行前必须先调用 `signet-preflight` 函数，在支付成功后则需调用 `signet-record` 函数。"
metadata: {"openclaw":{"emoji":"🛡️","homepage":"https://getsignet.xyz"}}
---

# Signet Guardian — 支付保护中间件

## 概述

Signet Guardian 是一个用于管理资金交易的 **策略防火墙**。它本身不会在运行时拦截支付；只有那些支持支付的技能才能根据合同约定通过该中间件进行支付：

1. 在进行任何支付之前，必须调用 `signet-preflight` 函数（传入金额、货币、收款人及支付用途）。
2. 如果返回结果是 `ALLOW` 或 `CONFIRM_REQUIRED`（并且用户已确认），则技能可以继续执行支付。
3. 如果返回结果是 `DENY`，则不得继续支付，并向用户说明原因。
4. 支付成功后，需要调用 `signet-record` 函数将交易记录到账本中。

通过这种方式，可以统一管理以下规则：是否允许支付、单次交易的最大金额限制（例如 20 英镑）、每月的最大支出限额（例如 500 英镑），以及是否需要超过某个金额后的用户确认（例如 5 英镑）。

**并发处理**：`signet-preflight` 函数仅提供建议性检查（不进行锁定操作）。`signet-record` 函数在写入账本时会检查每月的支出限额（使用文件锁 `{baseDir}/references/.ledger.lock`）；如果会超出限额，则拒绝记录。因此，每月的支出限制是在记录交易时生效的。即使在并发调用情况下，系统的幂等性和限额控制也能得到保障。`signet-preflight` 仍然可以用于快速判断是否满足支付条件；最终的决定由 `signet-record` 函数做出。

**货币处理**：系统不支持货币兑换。请求的货币必须与配置的策略货币相匹配；否则 `signet-preflight` 会返回 `DENY`。货币兑换的相关规则未在文档中定义。

## 策略配置（用户可设置）

**配置来源**：首先参考 OpenClaw 的配置文件（主配置文件中的 `signet.policy`，如果安装了相应的插件，也可以通过 Control UI 进行编辑），如果没有该配置文件，则会回退到 `{baseDir}/references/policy.json`。OpenClaw 通过 `OPENCLAW_SKILL_DIR` 或 `OPENCLAW_BASE_DIR` 设置 `{baseDir}` 的路径。

| 字段 | 含义 |
|-------|--------|
| `paymentsEnabled` | 是否允许支付。如果设置为 `false`，则所有支付都会被拒绝。 |
| `maxPerTransaction` | 单次交易允许的最大金额。 |
| `maxPerMonth` | 当前月份的累计支出上限。 |
| `currency` | ISO 货币代码（例如 GBP、USD）。请求的货币必须与此匹配。 |
| `requireConfirmationAbove` | 超过此金额时，系统会要求用户明确确认。 |
| `blockedMerchants` | 可选的字符串列表；匹配到该列表中任意一个收款人的交易都会被拒绝。 |
| `allowedMerchants` | 可选的收款人列表；如果存在，只有匹配到这些收款人的交易才会被允许。 |
| `version` | 用于未来策略升级的版本号。 |

**默认行为**：如果策略文件缺失或无效，`signet-preflight` 会返回 `DENY`（即默认拒绝所有支付）。

## 命令

### `signet-preflight`

在开始任何支付操作之前运行此命令。该命令会验证以下条件：是否允许支付、货币是否匹配、金额是否大于 0 且不超过单次交易的最大限额、当前月份的累计支出加上本次支付金额是否不超过每月的总额上限，以及是否需要超过某个金额后的用户确认。金额必须大于 0。

```bash
signet-preflight --amount 15 --currency GBP --payee "shop.example.com" --purpose "Subscription"
```

**可选参数：**
- `--idempotency-key "unique-key"`：用于在后续记录时避免重复记录同一笔交易。
- `--caller-skill "skill-name"`：调用该中间件的技能名称（用于审计记录）。

**输出（JSON 格式）：**
- `{ "result": "ALLOW", "reason": "符合政策规定" }`：允许支付。
- `{ "result": "CONFIRM_REQUIRED", "reason": "..." }`：要求用户明确确认；用户确认后继续支付，并调用 `signet-record`。
- `{ "result": "DENY", "reason": "..." }`：拒绝支付，并向用户说明原因。

所有被拒绝的请求都会被记录到审计日志中。

**退出代码**：
- `0` 表示允许支付或需要用户确认。
- `1` 表示拒绝支付。

### `signet-record`

在支付成功后调用此命令。该命令会将交易记录添加到账本中（仅追加记录，不修改现有数据）。如果在 `signet-preflight` 中使用了幂等性键，此处也需要传递相同的键以避免重复记录。

**记录验证范围**：`signet-record` 仅重新检查货币和每月的支出限额（在文件锁的保护下进行）。系统不会重新检查是否允许支付或哪些收款人可以被接受。策略相关的规则（是否允许支付、允许的收款人列表、单次交易限额）在 `signet-preflight` 阶段就已经生效（未来也可以通过 `authorize` 阶段进行配置）。`signet-record` 主要用于记录支付成功的交易；在并发调用 `signet-preflight` 时，该命令可以确保限额不被重复计算。

**可选参数：** `--caller-skill "skill-name"`（用于审计记录）。

如果之前已经记录过相同的 `idempotency-key`，则该命令不会产生任何效果（即具有幂等性）。

### `signet-report`

用于显示用户的支出和交易历史记录。

```bash
signet-report --period today
signet-report --period month
```

### `signet-policy`

通过可视化界面显示、编辑或配置策略规则。

```bash
signet-policy --show    # Print current policy (config, then file)
signet-policy --edit    # Open policy.json in $EDITOR
signet-policy --wizard  # Interactive step-by-step setup (no JSON)
signet-policy --migrate-file-to-config  # One-time: copy file policy into OpenClaw config
```

## 审计日志（账本和拒绝记录）

账本文件位于 `{baseDir}/references/ledger.jsonl`，采用 **严格的 JSONL** 格式：每行包含一个 JSON 对象，各行之间用换行符分隔（条目之间没有空格）。每条记录包含以下信息：
- `ts`：UTC 时间戳（ISO 8601 格式）。
- `callerSkill`：调用 `signet-preflight` 或 `signet-record` 的技能名称。
- `idempotencyKey`：用于唯一标识记录的键。
- `status`：`completed` 或 `denied`（表示交易状态）。
- `reason`：拒绝交易的理由。
- 其他信息：金额、货币、收款人、支付用途等。

所有被 `signet-preflight` 拒绝的交易都会被记录到账本中，状态标记为 `denied` 并附上拒绝原因。

## 关键规则（对代理程序的要求）：

1. **必须执行 `signet-preflight`**：任何技能发起的支付操作都必须先经过 `signet-preflight` 的检查，没有任何例外。
2. **严格遵循拒绝决定**：如果 `signet-preflight` 返回 `DENY`，则不得尝试支付，并向用户说明原因。
3. **要求用户确认**：如果 `signet-preflight` 返回 `CONFIRM_REQUIRED`，则需要用户明确确认是否允许支付（例如：“是否允许向 Y 支付 X 英镑？”）。只有在用户确认后，才能继续执行支付，并调用 `signet-record`。
4. **务必记录成功交易**：支付成功后，必须使用相同的金额、货币、收款人和幂等性键调用 `signet-record`。
5. **确保幂等性**：对于关键交易，使用稳定的 `--idempotency-key`（例如订单 ID 或请求 ID），以确保重试不会导致每月支出总额重复计算。
6. **默认拒绝**：如果策略文件缺失或损坏，系统会默认拒绝所有支付。
7. **记录仅用于验证限额**：每月的支出限额是在记录交易时生效的（在文件锁的保护下）。如果 `signet-record` 因限额问题失败，说明支付已经发生；在没有用户确认的情况下不得重试。对于那些在支付前需要确保限额安全的交易，可以先通过 `authorize`（在文件锁的保护下进行预留）然后再执行 `settle`（将预留状态更新为已完成）的流程来确保预算得到控制。

## 首次使用说明

首次使用时，用户需要提供一个有效的 `{baseDir}/references/policy.json` 文件。运行 `signet-policy --show` 可以查看当前的策略配置；如果文件缺失，可以使用 `signet-policy --edit` 命令创建该文件，至少需要设置以下参数：
- `paymentsEnabled`：是否允许支付（true/false）。
- `maxPerTransaction`：单次交易的最大金额。
- `maxPerMonth`：每月的最大支出限额。
- `currency`：支持的货币代码。
- `requireConfirmationAbove`：超过该金额后是否需要用户确认。

账本文件保存在 `{baseDir}/references/ledger.jsonl`，无需额外设置。