---
name: structs-economy
description: >
  **管理结构体中的经济操作**  
  涵盖反应堆质押、能源供应商、协议制定、资源分配、发电机注入以及代币转移等功能。适用于在反应堆中质押Alpha Matter、创建或管理能源供应商、协商协议、分配能源、注入发电机、转移代币，或管理经济基础设施等场景。
---
# 结构经济系统（Structs Economy）

## 操作流程

1. **评估当前状态**：通过 `structsd query structs player/reactor/provider/agreement [id]` 查询玩家、反应堆、供应商及协议的状态。
2. **反应堆质押**：向反应堆质押阿尔法物质（Alpha Matter）：`structsd tx structs reactor-infuse [player-address] [reactor-address] [amount] TX_FLAGS`。`amount` 必须包含货币单位（例如 `60000000ualpha`，而不仅仅是 `60000000`）。此操作会自动增加玩家的容量，无需额外设置。反应堆的佣金率决定了收益分配：玩家获得 `power * (1 - commission)`，剩余部分归反应堆所有。取消质押：`reactor-defuse [reactor-id]`（需要等待冷却时间）。提前结束冷却时间：`reactor-cancel-defusion [reactor-id]`。迁移资源：`reactor-begin-migration [player-address] [source-validator-address] [dest-validator-address] [amount]`。
3. **发电机注入**：`structsd tx structs struct-generator-infuse [struct-id] [amount] TX_FLAGS`。此操作是不可逆的，注入的阿尔法物质无法恢复。虽然转换效率（2-10倍）高于反应堆，但发电机容易受到攻击。
4. **供应商管理**：创建供应商：`provider-create [substation-id] [rate] [access-policy] [provider-penalty] [consumer-penalty] [cap-min] [cap-max] [dur-min] [dur-max] TX_FLAGS`。有效的 `access-policy` 值包括：`open-market`（任何人都可以购买）、`guild-market`（仅限公会成员购买）和 `closed-market`（需要通过 `provider-guild-grant` 邀请）。更新供应商的容量、持续时间或访问权限：`provider-update-capacity-maximum`、`provider-update-duration-minimum` 等。删除供应商：`provider-delete [provider-id]`。提取收益：`provider-withdraw-balance [provider-id]`。授予/撤销公会访问权限：`provider-guild-grant`、`provider-guild-revoke`。
5. **协议管理**：创建协议：`agreement-open [provider-id] [duration] [capacity] TX_FLAGS`。关闭协议：`agreement-close [agreement-id]。调整协议容量或持续时间：`agreement-capacity-increase/decrease`、`agreement-duration-increase`。
6. **资源分配**：创建资源分配：`allocation-create [source-id] [power] --allocation-type static|dynamic|automated TX_FLAGS`。默认情况下，控制权保持在创建分配的玩家账户手中（最安全）。如需指定控制者，可使用 `--controller` 参数（参数类型为地址，而非玩家ID）。更新分配信息：`allocation-update [allocation-id] [new-power]`。删除分配：`allocation-delete [allocation-id]`；只有控制分配的账户才能删除它。转移分配：`allocation-transfer [allocation-id] [new-owner]`。

### 资源分配类型对比

| 类型 | 是否可更新 | 是否可删除 | 是否会自动增长 | 是否有限制 | 使用场景 |
|------|-----------|-----------|------------|-------|----------|
| `static` | 否 | 否（连接状态下不可删除） | 否 | 无限制 | 固定容量的资源路由 |
| `dynamic` | 是 | 是 | 否 | 无限制 | 灵活的、可管理的资源路由 |
| `automated` | 是 | 否 | 是（会根据源容量自动调整） | 每个来源只能创建一个自动分配 | 推荐用于能源交易 |
| `provider-agreement` | 由系统管理 | 由系统管理 | 由系统创建 | 协议创建时会自动生成；禁止手动创建 |

**自动分配限制**：每个来源最多只能创建一个自动分配。尝试为同一来源创建第二个自动分配会导致错误。如需为同一来源创建多个分配，请使用 `dynamic` 类型。

**能源销售推荐**：使用 `automated` 类型的分配。向反应堆注入更多阿尔法物质后，玩家的容量会增加，系统会自动调整分配到各个子站的能源量，无需人工干预。

7. **代币转移**：`player-send [from-address] [to-address] [amount] TX_FLAGS`。

## 命令参考

| 功能 | 对应命令 |
|--------|---------|
| 向反应堆注入资源 | `structsd tx structs reactor-infuse [player-addr] [validator-addr] [amount]`（`validator` 为验证者地址，而非反应堆ID） |
| 取消反应堆质押 | `structsd tx structs reactor-defuse [reactor-id]` |
| 迁移资源到其他反应堆 | `structsd tx structs reactor-begin-migration [player-addr] [src-validator-addr] [dest-validator-addr] [amount]` |
| 提前结束反应堆质押冷却时间 | `structsd tx structs reactor-cancel-defusion [reactor-id]` |
| 向发电机注入资源 | `structsd tx structs struct-generator-infuse [struct-id] [amount]` |
| 创建供应商 | `structsd tx structs provider-create [substation-id] [rate] [access-policy] [prov-penalty] [cons-penalty] [cap-min] [cap-max] [dur-min] [dur-max]` |
| 删除供应商 | `structsd tx structs provider-delete [provider-id]` |
| 提取供应商收益 | `structsd tx structs provider-withdraw-balance [provider-id]` |
| 创建协议 | `structsd tx structs agreement-open [provider-id] [duration] [capacity]` |
| 关闭协议 | `structsd tx structs agreement-close [agreement-id]` |
| 创建资源分配 | `structsd tx structs allocation-create [source-id] [power] --allocation-type` |
| 更新资源分配 | `structsd tx structs allocation-update [allocation-id] [power]` |
| 删除资源分配 | `structsd tx structs allocation-delete [allocation-id]` |
| 发送代币 | `structsd tx structs player-send [from] [to] [amount]` |

**`TX_FLAGS` 参数说明**：`--from [key-name] --gas auto --gas-adjustment 1.5 -y`

**重要提示**：包含破折号的实体ID（如 `3-1`、`4-5`）会被CLI解析器误认为是命令参数。请务必在参数和实体ID之间加上 `--`，例如：`structsd tx structs command TX_FLAGS -- [entity-id] [other-args]`。

## 验证方法

- **反应堆**：`structsd query structs reactor [id]` — 检查 `infusedAmount` 和 `defusionCooldown` 状态。
- **供应商**：`structsd query structs provider [id]` — 核实供应商的容量、费率及活跃的协议。
- **协议**：`structsd query structs agreement [id]` — 查看协议的状态、容量和持续时间。
- **资源分配**：`structsd query structs allocation [id]` — 确认资源的来源和目的地。
- **玩家余额**：`structsd query structs player [id]` — 检查玩家拥有的阿尔法物质数量。

## 错误处理

- **余额不足**：在注入或发送资源前，请确保玩家有足够的阿尔法物质。请先采集足够的矿石。
- **供应商容量超出限制**：查询供应商的 `capacityMaximum` 值；降低协议容量或创建新的供应商。
- **反应堆质押冷却时间**：在冷却期间，可以使用 `reactor-cancel-defusion` 操作重新质押资源，或等待冷却时间结束。
- **发电机注入失败**：操作无法撤销。请确认目标资源确实是发电机类型，并确保输入的金额正确。

## 相关内容

- [structs-energy skill](https://structs.ai/skills/structs-energy/SKILL) — 能源相关的决策流程和工作流程
- [knowledge/economy/energy-market](https://structs.ai/knowledge/economy/energy-market) — 供应商与协议之间的资源流动及定价机制
- [knowledge/economy/guild-banking](https://structs.ai/knowledge/economy/guild-banking) — 公会银行系统与代币管理
- [knowledge/mechanics/resources](https://structs.ai/knowledge/mechanics/resources) — 阿尔法物质及其转换率
- [knowledge/mechanics/power](https://structs.ai/knowledge/mechanics/power) — 系统容量、负载及在线状态相关知识