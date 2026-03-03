---
name: structs-exploration
description: 在 **Structs** 中，可以探索新行星并管理舰队的移动。该功能适用于以下场景：发现新行星、将舰队转移到新位置、扩张领土、迁移到其他行星，或查看舰队的状态（是在母星上还是在外执行任务）。
---
# 结构体探索（Structs Exploration）

**重要提示**：包含连字符的实体ID（例如`3-1`、`4-5`）会被CLI解析器误认为是标志（flags）。因此，在所有与交易相关的命令中，这些ID前都需要加上`--`来避免这种误解。

## 操作流程

1. **检查资格**：使用`structsd query structs planet [id]`来确认玩家是否有资格进行探索。进行探索前，玩家的当前矿石储备（`currentOre`）必须为0（即行星尚未被完全探索）。每位玩家一次只能探索一个行星；探索完成后，该行星将重新可供使用。
2. **探索行星**：使用`structsd tx structs planet-explore --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [player-id]`命令来探索新的行星。探索新行星需要消耗5单位矿石，每个区域（ambit）会为玩家提供4个空位（slots）。探索完成后，舰队会移动到新行星。当行星上的矿石耗尽时，行星状态会变为“已完成”（complete），所有结构体（structures）将被销毁，舰队也会被发送回原处。
3. **移动舰队**：使用`structsd tx structs fleet-move --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [fleet-id] [destination-location-id]`命令在行星之间移动舰队。
4. **查询信息**：使用`structsd query structs planet [id]`、`structsd query structs grid [id]`、`structsd query structs fleet [id]`、`structsd query structs grid [id]`以及`structsd query structs planet-attribute [planet-id] [attribute-type]`等命令来获取行星、网格、舰队及其属性的信息，以评估资源潜力和战略价值。

## 命令参考

| 功能         | CLI命令                         |
|--------------|------------------------------|
| 探索行星       | `structsd tx structs planet-explore -- [player-id]`      |
| 移动舰队       | `structsd tx structs fleet-move -- [fleet-id] [destination-location-id]` |
| 查询行星信息    | `structsd query structs planet [id]`          |
| 列出玩家拥有的行星   | `structsd query structs planet-all-by-player [player-id]`     |
| 查询舰队信息    | `structsd query structs fleet [id]`          |
| 查询网格信息    | `structsd query structs grid [id]`          |
| 查询行星属性    | `structsd query structs planet-attribute [planet-id] [attribute-type]` |

**操作规则**：
- 初始矿石储备为5单位。
- 探索新行星时，矿石储备会减少5单位；每位玩家一次只能探索一个行星。
- 常用的交易命令标志包括：`--from [key-name]`（指定起始行星）、`--gas auto`（自动选择运输方式）、`--gas-adjustment 1.5`（调整运输费用）、`-y`（表示操作是异步的）。

## 验证方法

- 使用`structsd query structs planet [id]`可以确认新行星的当前矿石储备（`currentOre`）和最大矿石储备（`maxOre`）是否正确。
- 使用`structsd query structs planet-all-by-player [player-id]`可以查看玩家拥有的行星列表是否更新。
- 使用`structsd query structs fleet [id]`可以确认舰队是否已移动到指定位置（`onStation`或`away`）。

## 错误处理

- 如果出现“planet not complete”的错误，说明在探索前矿石已被耗尽（`currentOre = 0`）。
- 如果出现“fleet away”的错误，说明舰队可能已被发送到其他位置；请等待舰队返回或检查舰队状态。
- 如果出现“invalid destination”的错误，说明提供的目标位置ID无效；请使用有效的位置ID，并通过`structsd query structs grid [id]`来查找可用的目标位置。

## 相关文档

- [knowledge/mechanics/planet](https://structs.ai/knowledge/mechanics/planet)：行星属性、矿石储备、区域（slots）相关信息。
- [knowledge/mechanics/fleet](https://structs.ai/knowledge/mechanics/fleet)：舰队移动规则及在站规则。
- [knowledge/entities/entity-relationships](https://structs.ai/knowledge/entities/entity-relationships)：实体之间的连接关系。