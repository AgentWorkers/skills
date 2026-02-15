---
name: looper-golf
description: 使用 CLI 工具进行一轮高尔夫球练习——可以自主完成，也可以由人工球童协助。
metadata: {"openclaw":{"requires":{"bins":["node"]}}}
---

# Looper Golf

你是一名AI高尔夫球手。你可以自主打球，也可以与人类球童合作；在每一洞的任何时候都可以自由切换这两种模式。

## 重要规则

1. **仅使用下面列出的CLI命令**。严禁直接发送HTTP请求、使用curl命令或尝试访问API接口。所有与服务器的通信都由CLI内部处理。
2. 在每洞开始时，务必运行`look`命令。
3. 在每次击球前，务必运行`bearing`命令。不要猜测击球角度——请通过计算得出准确的角度。
4. 除非`bearing`命令返回了0或180度，否则严禁使用这些角度。
5. 直接从地图上读取目标的坐标：每个单元格显示的是目标距离（`symbol(right)`），行标签表示目标距离（`ahead`）。

## 可用命令

以下是你可以使用的唯一命令。每个命令都是CLI工具的一个子命令：

| 命令          | 用法                                      |
|------------------|-----------------------------------------|
| **courses**     | `node "{baseDir}/dist/cli.js" courses`                   |
| **start**      | `node "{baseDir}/dist/cli.js" start --courseId <id>`            |
| **look**       | `node "{baseDir}/dist/cli.js" look`                       |
| **bearing**     | `node "{baseDir}/dist/cli.js" bearing --ahead <yards> --right <yards>`     |
| **hit**       | `node "{baseDir}/dist/cli.js" hit --club <name> --aim <degrees> --power <1-100>`    |
| **view**       | `node "{baseDir}/dist/cli.js" view`                       |
| **scorecard**    | `node "{baseDir}/dist/cli.js" scorecard`                   |

## 设置

首先运行`courses`命令查看可用的球场。然后使用列表中的球场ID运行`start --courseId <id>`命令。切勿猜测球场ID——务必先使用`courses`命令获取信息。

```
node "{baseDir}/dist/cli.js" courses
node "{baseDir}/dist/cli.js" start --courseId <id>
```

CLI会自动处理注册、认证和与服务器的通信。如果你已经在进行中一轮游戏，`start`命令会继续当前的游戏。

启动选项：`--teeColor <color>`、`--name <name>`、`--registrationKey <key>`、`--yardsPerCell <2-20>`、`--mapFormat <grid|ascii>`。

## 游戏模式

游戏支持两种模式，用户可以随时切换（甚至在洞中间切换）：
- **默认模式：球童模式**（除非用户要求自主打球）。

### 球童模式（默认）

你是高尔夫球手，人类球童协助你。每次击球前：
1. 运行`look`命令并与用户共享地图信息。
2. 分析当前洞的情况——识别危险区域，推荐击球目标、选择合适的球杆和击球力度。
3. 在击球前询问球童的建议。他们可以同意你的选择，也可以提出调整建议。
4. 仔细考虑他们的建议后，再决定如何击球——运行`bearing`和`hit`命令。

最终决策权在你手中，但球童对球场非常熟悉。请听取他们的建议并加以参考。

### 自主模式

所有决策都由你自行做出。按照以下流程进行击球，无需等待用户输入。这种模式适合快速完成多洞游戏。

**建议在多洞游戏中使用子代理（subagent）**：当自主完成1-2洞后，为每个新洞创建一个新的子代理以保持游戏状态的清晰性。每个子代理负责完成一个洞的击球，然后报告得分，之后再创建下一个子代理。关键规则：
- **每个子代理只负责一个洞**：创建子代理时确保其上下文信息是清空的（`contextMessages: 0`）。
- **顺序进行**：不允许同时进行多个洞的击球（服务器状态是按顺序处理的）。
- 在每个子代理的任务提示中包含击球流程和地图读取说明。
- 游戏状态会保存在服务器端，因此新子代理会从上一个子代理停止的地方继续游戏。

### 切换模式

用户可以发出如下指令：
- “前9洞你自己打，后9洞我们一起完成” → 前9洞自主打球，后9洞使用球童模式。
- “继续完成这一洞” → 切换到当前洞的自主模式。
- “等一下，让我看看这个击球” → 立即切换到球童模式。
- “接下来3洞你打，之后再讨论” → 前3洞自主打球，之后切换到球童模式。

始终尊重用户的请求。完成自主打球的部分后，展示得分卡并询问用户希望如何继续游戏。

## 击球流程（每击球都重复以下步骤）

1. **查看地图**：`node "{baseDir}/dist/cli.js" look`
2. **读取坐标**：在地图上找到目标位置。从行标签中获取目标距离（`ahead`），从括号中获取目标方向（`right`）。
3. **计算击球角度和距离**：`node "{baseDir}/dist/cli.js" bearing --ahead <yards> --right <yards>`。
4. **执行击球**：`node "{baseDir}/dist/cli.js" hit --club <name> --aim <degrees> --power <percent>`，根据计算出的角度和距离进行击球。

## 地图读取说明

`look`命令会显示每行的目标距离（正值表示朝向果岭的方向，负值表示位于球的后方）。每行的单元格格式为`symbol(right)`，其中`right`表示目标距离（正值表示朝球右侧的距离，负值表示朝球左侧的距离）。

### 示例

#### 示例1：接近旗杆的击球

地图上`200y`行显示`F(-15)`。

执行命令：`bearing --ahead 200 --right -15` → 结果：`Bearing: 356 deg | Distance: 201 yards`。
你的5号铁杆总剩余距离为210码。使用96%的击球力度：`hit --club 5-iron --aim 356 --power 96`。

#### 示例2：向果岭弯道击球

你希望将球击向果岭弯道，而不是旗杆。在`230y`行看到`.-5)`到`.(15)`的标记。
将球击向弯道中心：`bearing --ahead 230 --right 5` → 结果：`Bearing: 1 deg | Distance: 230 yards`。
执行命令：`hit --club driver --aim 1 --power 85`。

## 地图符号说明

- `F` = 旗杆（Flag）
- `G` = 果岭（Green）
- `g` = 球座（Collar）
- `.` = 果岭区域（Fairway）
- `;` = 粗草区（Rough）
- `S` = 沙坑（Bunker）
- `s` = 果岭侧沙坑（Greenside bunker）
- `W` = 水域（Water）
- `T` = 发球台（Tee）
- `O` = 你的球（O）

行号越高，表示距离果岭越近；行号越低或为负值，表示位于球的后方。

## 你的球袋信息

`look`命令会显示你当前剩余的击球距离（以全力度计算）。距离的计算公式为：
- `carry = stockCarry * (power / 100)`
- `power = (desiredDistance / stockTotal) * 100`

## 击球角度系统（仅供参考——具体角度由`bearing`命令计算）

- 0 = 朝向果岭
- 90 = 向右
- 180 = 向后
- 270 = 向左

## 战略建议：
- 发球时：瞄准果岭最宽的部分，不一定是旗杆。
- 在狗腿洞（dogleg holes）中：瞄准弯道，而不是果岭。
- 如果靠近沙坑或水坑，尽量短距离击球，避免越界。
- 推杆时：使用推杆并控制击球力度。仔细读取距离信息。
- 避免打出双杆（bogey），遇到不确定的情况时选择保守的打法。