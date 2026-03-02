---
name: structs-combat
description: 在结构体（Structs）中执行战斗操作，包括发起攻击、进行突袭、部署防御措施以及进行隐蔽行动。适用于攻击敌方结构体、为获取矿石而突袭行星、部署防御部队、激活隐蔽模式、指挥舰队执行突袭任务，或是为即将到来的攻击做准备。突袭行动需要舰队的移动以及后台的计算资源（PoW计算）。
---
# 结构体战斗

**重要提示**：实体ID中包含连字符（如`5-10`、`9-3`）时，CLI解析器会将其误认为是标志（flags）。因此，在执行所有交易命令时，必须在参数前加上`--`来避免这种情况。

## 操作流程

1. **侦察**：使用`structsd query structs planet [id]`或`structsd query structs struct [id]`来查找目标结构体、护盾及防御系统。
2. **可选的隐身功能**：在攻击前，可以使用`structsd tx structs struct-stealth-activate --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [struct-id]`激活隐身功能。
3. **攻击结构体**：执行`structsd tx structs struct-attack --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [operating-struct-id] [target-struct-id,...] [weapon-system]`命令进行攻击。可以同时攻击多个目标结构体。
4. **突袭流程**：首先使用`structsd tx structs fleet-move --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [fleet-id]`将舰队移动到目标位置，然后执行`structsd tx structs planet-raid-compute -D 3 --from [key-name] --gas auto --gas-adjustment 1.5 -y -- [fleet-id]`来计算突袭方案。系统会自动提交整个交易请求，并将舰队撤回基地。随后需要立即处理被抢夺的矿石。
5. **防御设置**：使用`structsd tx structs struct-defense-set --from [key] --gas auto -y -- [defender-struct-id] [protected-struct-id]`来部署防御结构体；使用`structsd tx structs struct-defense-clear --from [key] --gas auto -y -- [defender-struct-id]`来移除已部署的防御结构体。

## 命令参考

| 功能 | CLI命令            |
|--------|-------------------|
| 攻击    | `structsd tx structs struct-attack -- [operating-struct-id] [target-ids] [weapon-system]` |
| 突袭计算（自动完成）| `structsd tx structs planet-raid-compute -D 3 -- [fleet-id]` |
| 突袭完成（手动，较少使用）| `structsd tx structs planet-raid-complete -- [fleet-id]` |
| 舰队移动  | `structsd tx structs fleet-move -- [fleet-id] [destination-location-id]` |
| 设置防御  | `structsd tx structs struct-defense-set -- [defender-struct-id] [protected-id]` |
| 移除防御 | `structsd tx structs struct-defense-clear -- [defender-struct-id]` |
| 激活隐身  | `structsd tx structs struct-stealth-activate -- [struct-id]` |
| 关闭隐身  | `structsd tx structs struct-stealth-deactivate -- [struct-id]` |
| 调整指挥舰位置 | `structsd tx structs struct-move -- [struct-id] [new-ambit] [new-slot] [new-location]` |

**突袭流程**：舰队移动 → 突袭计算（自动提交） → 舰队返回基地 → 处理被抢夺的矿石。常用交易标志：`--from [key-name] --gas auto --gas-adjustment 1.5 -y`。

## 突袭时间计算

舰队移动（`fleet-move`）是瞬间完成的，没有传输时间。突袭过程中的唯一时间消耗在于突袭方案的计算（`planet-raid-compute`）。

`planet-raid-compute`命令使用`-D`标志（范围1-64）来控制计算等待时间（难度等级越高，等待时间越长）。突袭的难度取决于目标星球的属性。建议在后台终端执行该命令，计算时间可能从几分钟到几小时不等。使用`-D 3`可确保CPU资源不被浪费。系统会自动提交整个交易请求。

**重要提示**：在突袭计算期间，舰队处于“锁定”状态，此时无法在目标星球上进行建设。请确保在派遣舰队之前完成所有建设任务。

## 武器适用范围

每种武器都有其特定的攻击范围。在攻击前，请确认你的结构体所配备的武器是否能够覆盖目标范围。

| 结构体类型 | 活动范围         | 主要攻击目标       | 辅助攻击目标       |
|--------|-----------------|-----------------|-------------------|
| 指挥舰    | 任意范围         | 仅限当前活动范围     |              |
| 战列舰    | 太空             | 太空、陆地、水域       |              |
| 星际战斗机 | 太空             | 太空             |              |
| 护卫舰    | 太空             | 太空             |              |
| 追击战斗机 | 空中             | 空中             |              |
| 隐形轰炸机 | 空中             | 陆地、水域         |              |
| 高空拦截机 | 空中             | 太空、空中         |              |
| 移动炮台   | 陆地             | 陆地、水域         |              |
| 坦克     | 陆地             | 陆地             |              |
| 地对空导弹发射器 | 陆地             | 太空、空中         |              |
| 巡洋舰    | 水域             | 陆地、水域         |              |
| 驱逐舰    | 水域             | 空中、水域         |              |
| 潜水艇    | 水域             | 太空、水域         |              |

**指挥舰的位置调整**：指挥舰是唯一可以通过`struct-move`命令调整活动范围的舰船。它只能攻击当前活动范围内的目标结构体（活动范围标志`32`表示“本地范围”）。攻击前请将其移动到目标范围，或远离敌方武器的攻击范围以增强防御。

## 武器类型与防御方式的互动

武器类型（制导/非制导）与目标防御方式的相互作用决定了战斗结果：

| 目标防御方式 | 对制导武器       | 对非制导武器       |
|----------------|-----------------|-------------------|
| 信号干扰（战列舰、追逐战斗机、巡洋舰） | 66%的攻击会miss     | 100%命中       |
| 防御机动（高空拦截机） | 100%命中       | 66%的攻击会miss     |
| 装甲（坦克）    | 100%命中       | 减少1点伤害       |
| 隐形模式（隐形轰炸机、潜水艇） | 仅在同一活动范围内有效 | 仅在同一活动范围内有效 |
| 间接攻击（移动炮台） | 100%命中       | 100%命中       |

**战斗策略**：
- 对抗信号干扰时使用非制导武器；
- 对抗防御机动时使用制导武器；
- 装甲能减少1点伤害。

**隐身规则**：
- 隐形结构体仍可被同一活动范围内的攻击击中（隐身功能仅阻止跨活动范围的攻击）；
- 攻击会立即取消隐身状态（攻击会暴露结构体位置）；
- 重新激活隐身功能需要消耗1点能量（`struct-stealth-activate`）。

## 战略性部署

**进攻策略**：将指挥舰部署到需要发动攻击的活动范围内。使用跨活动范围的攻击舰（如战列舰、隐形轰炸机、地对空导弹发射器、潜水艇）进行攻击，无需重新调整位置。

**防御策略**：
- 如果敌方舰队只能攻击特定范围，将指挥舰部署到它们无法到达的活动范围内，从而实现全方位防御。
| 高价值单位**：
- 战列舰（适用于太空→陆地/水域）；
- 地对空导弹发射器（适用于陆地→太空/空中）；
- 隐形轰炸机（适用于空中→陆地/水域）；
- 潜水艇（适用于水域→太空/水域）；
- 巡洋舰（适用于水域→陆地/水域及空中）。

## 验证步骤

- 查询星球的护盾状态和结构体健康值；
- 查看舰队的位置（是否在基地或远离基地）；
- 确保被抢夺的矿石已被及时处理（通过结构体或玩家查询进行验证）；
- 攻击结果会显示目标结构体的剩余生命值，用于评估造成的伤害；
- 被抢夺的矿石记录在`planet_raid`中，可查询总抢夺量。

## 战斗注意事项

- 即使经过防御，攻击造成的伤害至少为1点；
- 被摧毁的结构体无法进行反击；
- 每个结构体每次攻击只能执行一次操作（不允许重复攻击）；
- 攻击前会验证目标结构体的存在性；
- 突袭计算默认允许使用任意有效的攻击方式；
- 成功的突袭会夺取目标星球上的所有矿石；
- 被摧毁的结构体无法恢复，需要重新建造（需消耗完整计算量）；
- 保护好指挥舰，否则整个舰队将陷入瘫痪（直到新结构体建成）。

## 战斗准备检查清单

在开始战斗前，请确认以下条件：
- [ ] **指挥舰在线**：`structsd query structs struct [cmd-ship-id]`，状态应为“Online”；
- [ ] **舰队位置**：舰队应在基地（用于防御）或远离基地（用于突袭）：`structsd query structs fleet [fleet-id]`；
- **能量充足**：武器使用1-20点能量。以每秒约6点能量的速度计算，20点能量相当于2分钟；
- **电力容量**：战斗期间总负载不得超过容量上限；
- **防御结构体已部署**：使用`struct-defense-set`部署PDC、轨道护盾等防御措施；
- **有可用的结构体位置**：如果需要建造战斗结构体，请检查星球的可用位置（每个活动范围最多3个位置）；
- **矿石已处理或安全存放**：未处理的矿石可能被敌人抢夺，因此在发动突袭前请先处理矿石。

## 防御阵型

部署防御结构体以保护高价值目标。防御结构体会在目标结构体受到攻击前吸收伤害。

**最低限度的防御要求**：每个活动范围至少部署一个防御结构体来保护指挥舰。指挥舰具有6点生命值，大多数舰队结构体具有3点生命值。如果没有防御结构体，指挥舰可能在一次攻击中就被摧毁。

**示例阵型**（4艘星际战斗机保护指挥舰）：

```
structsd tx structs struct-defense-set --from [key] --gas auto -y -- [starfighter-1-id] [command-ship-id]
structsd tx structs struct-defense-set --from [key] --gas auto -y -- [starfighter-2-id] [command-ship-id]
structsd tx structs struct-defense-set --from [key] --gas auto -y -- [starfighter-3-id] [command-ship-id]
structsd tx structs struct-defense-set --from [key] --gas auto -y -- [starfighter-4-id] [command-ship-id]
```

**注意事项**：
- 防御结构体必须位于被保护目标的同一活动范围内；
- 防御结构体只能防御同一活动范围内的攻击；
- 如果防御结构体的武器能够覆盖攻击者的活动范围，它们会自动发起反击；
- 反击与被保护的目标活动范围无关（例如，太空防御结构体可以反击太空攻击者）；
- 每次部署防御结构体需要消耗1点能量，建议间隔6秒（同一账户内多次部署）；
- 请先建造防御结构体再进行经济或进攻建设；
- 防御结构体可以防止结构体被摧毁，但无法阻止矿石被抢夺（防止矿石被抢夺的唯一方法是立即处理矿石）。

## 错误处理

- **“能量不足”**：武器需要能量，请检查结构体状态；
- **“目标无效”**：目标可能已被摧毁、处于隐身状态或超出攻击范围；
- **“无法到达”/“超出范围”**：当前武器无法攻击该目标，请检查目标范围并重新调整指挥舰的位置或使用其他攻击方式；
- **“舰队未远离基地”**：突袭需要舰队远离基地，请先移动舰队；
- **“验证信息无效”**：请使用正确的难度重新执行突袭计算；
- **矿石被抢夺**：请立即处理被抢夺的矿石（未被处理的矿石仍可被敌人抢夺）。

**相关资料**：
- [knowledge/mechanics/combat](https://structs.ai/knowledge/mechanics/combat) — 战斗机制、伤害计算、突袭策略、防御方式；
- [knowledge/mechanics/fleet](https://structs.ai/knowledge/mechanics/fleet) — 舰队移动规则、基地部署；
- [knowledge/mechanics/resources](https://structs.ai/knowledge/mechanics/resources) — 矿石脆弱性、阿尔法物质（Alpha Matter）。