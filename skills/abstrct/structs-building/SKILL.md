---
name: structs-building
description: 在Structs中构建和管理各种结构体。负责结构的创建、激活、停用、移动、防御定位、隐身功能以及能量生成器的注入等操作。适用于构建结构体、激活或停用结构体、在不同位置之间移动结构体、设置防御任务、启用隐身功能或注入能量生成器等场景。构建时间因具体结构体类型而异：Command Ship的构建时间约为17分钟，World Engine的构建时间则长达约6.4小时。
---
# 结构体建造

**重要提示**：包含连字符的实体ID（例如`1-42`、`5-10`）会被CLI解析器误认为是标志（flags）。因此，在使用所有与结构体建造相关的命令时，必须在参数前添加`--`来避免这种误解。

## 建造流程

1. **检查条件**：玩家必须在线，拥有足够的阿尔法物质（Alpha Matter），并且有可用的建造槽位（每个建造领域最多3个槽位）；建造所需的指挥舰（Command Ship）必须在线，舰队（fleet）必须位于建造站点（适用于行星建造）。需要查询玩家信息、行星信息和舰队状态。
2. **启动建造**：执行命令 `structsd tx structs struct-build-initiate --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [player-id] [struct-type-id] [operating-ambit] [slot]`。其中`[operating-ambit]`参数必须是一个小写字符串，可以是`"space"`、`"air"`、`"land"`或`"water"`（不能使用位掩码数字）。
3. **工作量证明（Proof-of-Work）**：执行命令 `structsd tx structs struct-build-compute -D 3 --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]`。该命令会计算结构体的哈希值并自动提交建造请求，结构体会随之自动激活。无需额外的激活步骤。
4. **可选操作**：根据需要移动结构体、设置防御措施或开启隐身功能。

**自动激活**：结构体会在建造完成后自动激活。只有在使用`struct-deactivate`命令将其停用后，才需要使用`struct-activate`命令重新激活结构体。

## `struct-build-compute`与`struct-build-complete`的区别

`struct-build-compute`是一个辅助命令，它会执行工作量证明并自动提交`struct-build-complete`请求。`struct-build-complete`命令仅在您通过外部工具计算出哈希值并希望手动提交结果时使用。

## `-D`标志的用法

`-D`标志（取值范围1-64）用于指定结构体开始计算哈希值之前的难度等级。随着结构体老化，计算难度会呈对数级降低。例如，设置`-D 3`时，计算过程几乎瞬间完成且不会消耗任何CPU资源。较低的`-D`值会延长计算时间，但在处理高难度结构体时能更有效地利用计算资源。

## 能量消耗

每个操作都会消耗能量。能量以每块时间单位1单位的速率被动积累（大约每6秒积累1单位能量）。

| 操作        | 能量消耗 | 等待时间        |
|--------------|-----------|-------------------|
| 建造完成      | 8         | 约48秒             |
| 移动          | 8         | 约48秒             |
| 激活（仅限重新激活）   | 1         | 约6秒             |
| 设置防御        | 1         | 约6秒             |
| 安装主武器      | 1-20        | 根据结构体类型而异         |

如果出现“所需能量为X，但玩家当前只有Y”的错误，请等待能量积累足够。详细能量消耗信息请参见[knowledge/mechanics/building](https://structs.ai/knowledge/mechanics/building)。

## 预计建造时间

从启动到计算完成的总时间（假设每块时间单位计算6秒，难度等级为3）：

| 结构体类型    | 类型ID       | 建造难度       | 等待达到目标难度所需时间 |
|------------|------------|------------------|---------------------|
| 指挥舰       | 1           | 200           | 约17分钟             |
| 星际战斗机    | 3           | 250           | 约20分钟             |
| 采矿提取器     | 14           | 700           | 约57分钟             |
| 矿石精炼厂     | 15           | 700           | 约57分钟             |
| PDC（行星防御系统） | 19           | 2,880           | 约3.7小时             |
| 矿石储存库     | 18           | 3,600           | 约4.6小时             |
| 行星引擎     | 22           | 5,000           | 约6.4小时             |

**建议**：尽早启动建造流程，然后后台执行计算任务。可以批量启动所有计划中的建造任务，同时在等待期间进行其他操作。更多相关信息请参见[awareness/async-operations](https://structs.ai/awareness/async-operations)。

**注意事项**：每个签名密钥（signing key）只能同时执行一个计算任务。如果使用相同的签名密钥同时运行两个`*-compute`任务，可能会导致计算结果冲突，从而导致其中一个任务失败。请为不同的玩家使用不同的签名密钥，并为同一玩家的不同建造任务分别安排计算时间。

## 命令参考

| 操作        | CLI命令                          |
|------------|-----------------------------------------|
| 启动建造      | `structsd tx structs struct-build-initiate --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [player-id] [struct-type-id] [operating-ambit] [slot]` |
| 计算哈希值并自动完成 | `structsd tx structs struct-build-compute -D 3 --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]` |
| 手动完成建造    | `structsd tx structs struct-build-complete --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]` |
| 取消建造      | `structsd tx structs struct-build-cancel --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]` |
| 重新激活      | `structsd tx structs struct-activate --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]` |
| 停用结构体     | `structsd tx structs struct-deactivate --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]` |
| 移动结构体     | `structsd tx structs struct-move --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id] [new-ambit] [new-slot] [new-location]` |
| 设置防御      | `structsd tx structs struct-defense-set --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [defender-struct-id] [protected-struct-id]` |
| 清除防御      | `structsd tx structs struct-defense-clear --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [defender-struct-id]` |
| 开启隐身      | `structsd tx structs struct-stealth-activate --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]` |
| 关闭隐身      | `structsd tx structs struct-stealth-deactivate --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]` |
| 为结构体注入能量   | `structsd tx structs struct-generator-infuse --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id] [amount]` |

**限制**：
- 每个玩家最多只能拥有1个PDC（行星防御系统）和1艘指挥舰。
- 指挥舰必须属于玩家的舰队。
- 为结构体注入能量是不可逆的操作。
**常用命令参数**：`--from [key-name] --gas auto --gas-adjustment 1.5 -y`。

## 验证方法

- 使用 `structsd query structs struct [id]` 查询结构体状态（在线、已建造或离线）。
- 确认结构体已出现在相应的行星或舰队列表中。

## 错误处理

| 错误类型        | 原因                                      | 处理方法                                      |
|-----------------|-----------------------------------------|---------------------------------------------------------|
| “所需能量为X，但玩家当前只有Y” | 能量不足                                      | 等待约48秒（每6秒积累1单位能量）后再尝试建造                         |
| “资源不足”       | 阿尔法物质不足                                   | 先开采并精炼矿石；使用 `structsd query structs player [id]` 检查玩家能量余额           |
| “能量容量不足”     | 结构体无法上线                                   | 停用非必要的结构体或增加能量容量（参见 `structs-energy` 技能）                   |
| “舰队未在站点”     | 舰队远离建造站点                                   | 等待舰队返回或使用 `fleet-move` 命令将其移回站点                     |
| “需要指挥舰”     | 指挥舰未建造或已离线                                   | 先建造或重新激活指挥舰                                   |
| “槽位已被占用”     | 槽位已被其他结构体占用                                   | 检查行星上的现有结构体布局                               |
| “不支持的建造领域”   | 选定的结构体类型不支持当前建造领域                         | 查看结构体类型的 `possibleAmbit` 标志                         |
| “连接失败”     | 本地节点缺失或远程节点配置错误                             | 在 `~/.structs/config/client.toml` 中配置 `node` 参数，或使用 `--node` 标志           |

## 相关文档

- [knowledge/mechanics/building](https://structs.ai/knowledge/mechanics/building)：建造时间、难度等级、能量消耗 |
- [knowledge/mechanics/power](https://structs.ai/knowledge/mechanics/power)：能量容量、负载状态、在线状态 |
- [knowledge/entities/struct-types](https://structs.ai/knowledge/entities/struct-types)：所有结构体类型及其属性 |
- [knowledge/entities/entity-relationships](https://structs.ai/knowledge/entities/entity-relationships)：实体之间的连接关系 |
- [awareness/async-operations](https://structs.ai/awareness/async-operations)：后台计算流程与异步操作策略 |