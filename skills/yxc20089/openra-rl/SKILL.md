---
name: openra-rl
description: 《Command & Conquer: Red Alert》是一款即时战略游戏（RTS）。在游戏中，你需要建造基地、训练军队，并使用48种MCP工具来击败AI对手。
version: 1.1.0
metadata:
  openclaw:
    emoji: "🎮"
    homepage: https://github.com/yxc20089/OpenRA-RL
    requires:
      bins:
        - docker
      env: []
    install:
      - kind: uv
        package: openra-rl
        bins: [openra-rl]
    os: ["macos", "linux"]
---
# OpenRA-RL: 搭配《命令与征服：红色警戒》进行游戏

你是一个AI代理，正在玩经典的实时策略游戏《命令与征服：红色警戒》。你需要控制一个阵营（盟军或苏联），并完成基地建设、资源收集、军队训练以及摧毁敌人的任务。

该游戏运行在一个Docker容器中，你通过MCP工具与游戏进行交互，这些工具允许你观察战场、下达命令并推进游戏时间。

## 快速入门

### 1. 安装

```bash
pip install openra-rl
```

### 2. 启动游戏服务器

```bash
openra-rl server start
```

这会拉取Docker镜像并在8000端口上启动游戏服务器。使用`openra-rl server status`命令进行验证。

### 3. 配置MCP

将以下配置添加到你的OpenClaw配置文件（`~/.openclaw/openclaw.json`）中：

```json
{
  "mcpServers": {
    "openra-rl": {
      "command": "openra-rl",
      "args": ["mcp-server"]
    }
  }
}
```

### 4. 开始游戏

告诉你的代理：“开始一场《红色警戒》游戏并尝试获胜。”

代理将使用下面列出的MCP工具来进行观察和指挥。

---

## 游戏机制

- **实时性**：游戏以大约25帧/秒的频率持续运行。使用`advance(ticks)`命令来推进游戏时间。
- **战争迷雾**：你只能看到自己单位/建筑物附近的区域。需要派遣侦察单位来寻找敌人。
- **资源**：采集矿石以获得信用点数，信用点数可用于购买建筑物和单位。
- **能源**：建筑物需要能源才能运行。建造发电厂（`powr`）以确保能源供应。能源不足会降低生产速度。
- **科技树**：高级建筑物需要前置条件（例如，战争工厂需要矿石精炼厂）。

---

## MCP工具参考

### 观察（查看战场）

| 工具 | 功能 |
|------|---------|
| `get_game_state` | 获取完整游戏状态：经济、单位、建筑物、敌人、生产情况、军事数据 |
| `get_economy` | 获取现金、矿石数量、能源平衡、采集器数量 |
| `get_units` | 获取你的单位信息（位置、生命值、类型、姿态、速度、攻击范围） |
| `get_buildings` | 获取你的建筑物信息（生产队列、能源需求、可建造列表） |
| `get_enemies` | 查看可见的敌方单位和建筑物（受战争迷雾限制） |
| `get_production` | 当前建造队列及你可以建造的建筑物 |
| `get_map_info` | 地图名称和尺寸 |
| `get_exploration_status` | 探索进度、区域分布、是否找到敌方基地 |

### 学习游戏机制

| 工具 | 功能 |
|------|---------|
| `lookup_unit(unit_type)` | 查看单位详情（例如，`lookup_unit("e1")` → 步兵） |
| `lookup_building(building_type)` | 查看建筑物详情（例如，`lookup_building("weap")` → 战争工厂） |
| `lookup_tech_tree(faction)` | 查看“盟军”或“苏联”的完整科技树 |
| `lookup_faction(faction)` | 查看该阵营的所有单位和建筑物 |
| `get_faction_briefing()` | 获取你阵营的全面数据 |
| `get_map_analysis()` | 获取资源分布、水域、地形信息及战略提示 |
| `batch_lookup(queries)` | 同时查询多个信息 |

### 游戏控制

| 工具 | 功能 |
|------|---------|
| `advance(ticks)` | **关键** — 使游戏时间前进N帧。不使用此命令则游戏不会推进。25帧约等于1秒，250帧约等于10秒。 |

### 移动与战斗

| 工具 | 功能 |
|------|---------|
| `move_units(unit_ids, target_x, target_y)` | 将单位移动到指定位置 |
| `attack_move(unit_ids, target_x, target_y)` | 移动单位并沿途攻击敌人 |
| `attack_target(unit_ids, target_actor_id)` | 集中攻击特定敌人 |
| `stop_units(unit_ids)` | 停止单位移动和攻击 |
| `guard_target(unit_ids, target_actor_id)` | 保护单位或建筑物 |
| `set_stance(unit_ids, stance)` | 设置单位姿态（“holdfire”、“returnfire”、“defend”或“attackanything”） |
| `harvest(unit_id, cell_x, cell_y)` | 派遣采集器到矿石田 |

### 生产

| 工具 | 功能 |
|------|---------|
| `build_unit(unit_type, count)` | 训练单位（例如，`build_unit("e1", 5)` → 训练5名步兵） |
| `build_structure(building_type)` | 开始建造建筑物（需要手动定位） |
| `build_and_place(building_type, cell_x, cell_y)` | 建造完成后自动放置建筑物 |
| `place_building(building_type, cell_x, cell_y)` | 直接放置完成的建筑物 |
| `cancel_production(item_type)` | 取消正在建造的建筑物 |
| `get_valid_placements(building_type)` | 获取可放置建筑物的有效位置 |

### 建筑物管理

| 工具 | 功能 |
|------|---------|
| `deploy_unit(unit_id)` | 将移动建筑车辆（MCV）部署到建造场 |
| `sell_building(building_id)` | 卖出建筑物以获取部分退款 |
| `repair_building(building_id)` | 启用或关闭自动修复功能 |
| `set_rally_point(building_id, cell_x, cell_y)` | 新单位将从这里出发 |
| `power_down(building_id)` | 切换能源状态以节省能源 |
| `set_primary(building_id)` | 设置为主要生产建筑 |

### 单位组

| 工具 | 功能 |
|------|---------|
| `assign_group(group_name, unit_ids)` | 创建一个单位组 |
| `add_to_group(group_name, unit_ids)` | 将单位添加到组中 |
| `get_groups()` | 查看所有组 |
| `command_group(group_name, command_type, ...)` | 向整个组下达命令 |

### 复合操作

| 工具 | 功能 |
|------|---------|
| `batch_actions()` | 在同一帧内执行多个操作（不会推进游戏时间） |
| `plan(steps)` | 顺序执行多个步骤，每次执行后更新游戏状态 |

### 实用工具

| 工具 | 功能 |
|------|---------|
| `surrender()` | 放弃当前游戏 |
| `get_replay_path()` | 获取游戏回放文件路径 |
| `get_terrain_at(cell_x, cell_y)` | 获取指定位置的地形类型 |

### 规划阶段（可选）

| 工具 | 功能 |
|------|---------|
| `start_planning_phase()` | 开始游戏前策略规划 |
| `get_opponent_intel()` | 查看AI对手的资料和应对策略 |
| `end_planning_phase(strategy)` | 确定策略并开始游戏 |
| `get_planning_status()` | 查看规划进度 |

---

## 游戏玩法（策略指南）

### 第1步：部署移动建筑车辆（MCV）

游戏开始时，你拥有一辆移动建筑车辆（MCV）。使用它来创建建造场：

```
1. Call get_units() to find your MCV (type "mcv")
2. Call deploy_unit(mcv_actor_id)
3. Call advance(50) to let it deploy
```

### 第2步：建造基地

按照以下顺序建造：

| 建造顺序 | 建筑物 | 类型代码 | 成本 | 建造理由 |
|-------|----------|-----------|------|-----|
| 1 | 发电厂 | `powr` | 300美元 | 为所有单位提供能源 |
| 2 | 营房 | `tent`（盟军）或 `barr`（苏联） | 300美元 | 用于生产步兵 |
| 3 | 矿石精炼厂 | `proc` | 2000美元 | 产生收入并提供采集器 |
| 4 | 战争工厂 | `weap` | 2000美元 | 用于生产战斗车辆（需要精炼厂） |
| 5 | 更多发电厂 | `powr` | 300美元 | 确保能源充足 |

使用`build_and_place()`命令进行建造——建造完成后会自动放置：

```
1. Call get_valid_placements("powr") to find a good spot
2. Call build_and_place("powr", cell_x, cell_y)
3. Call advance(250) to let it build (~10 seconds)
4. Check get_production() to confirm completion
5. Repeat for next building
```

**注意**：你可以选择盟军或苏联阵营。使用`get_game_state()`查看`faction`字段确认阵营。营房的类型取决于所选阵营。

### 第3步：训练军队

```
1. Call build_unit("e1", 5) for 5 Rifle Infantry ($100 each)
2. Call advance(100) to let them train
3. Once War Factory is ready: build_unit("3tnk", 3) for Medium Tanks ($800 each)
4. Set rally point near base exit: set_rally_point(barracks_id, x, y)
```

**各阵营的关键单位：**

| 单位 | 代码 | 成本 | 作用 |
|------|------|------|------|
| 步兵 | `e1` | 100美元 | 价格便宜，移动迅速 |
| 火箭士兵 | `e3` | 300美元 | 具有反装甲能力 |
| 中型坦克 | `3tnk` | 800美元 | 主力战斗坦克 |
| 重型坦克 | `4tnk` | 950美元 | 苏联重型坦克 |
| 轻型坦克 | `1tnk` | 700美元 | 用于快速侧翼进攻 |
| 火炮 | `arty` | 600美元 | 具有远程攻击能力 |
| V2火箭发射器 | `v2rl` | 700美元 | 苏联远程武器 |

### 第4步：侦察地图

派遣一个单位进行侦察：

```
1. Train one Rifle Infantry
2. Call attack_move([unit_id], far_x, far_y) toward unexplored areas
3. Call advance(500) to let it travel
4. Call get_enemies() to see what you've found
```

### 第5步：攻击敌人

当你拥有8-10个战斗单位后：

```
1. Call get_enemies() to find enemy buildings
2. Call attack_move(all_unit_ids, enemy_base_x, enemy_base_y)
3. Call advance(100), check get_game_state() for battle progress
4. If enemies visible: attack_target(unit_ids, enemy_id) to focus fire
5. Keep producing reinforcements while attacking
```

### 第6步：持续管理经济

在游戏中：
- 确保能源始终为正（必要时建造发电厂）
- 不要让生产停滞——持续生产单位
- 建造更多矿石精炼厂以增加收入
- 及时补充丢失的采集器

---

## 游戏循环流程

一个高效的AI代理的游戏循环如下：

```
1. get_game_state() → read the situation
2. Decide what to do based on:
   - Economy: enough cash? Power positive?
   - Production: anything building? Queue empty?
   - Military: under attack? Ready to attack?
   - Exploration: enemy found yet?
3. Issue orders (build, move, attack)
4. advance(50-250) → let time pass
5. Repeat until game is won or lost
```

检查`get_game_state()`中的`done`字段。当该字段值为`true`时，`result`将显示“win”（胜利）或“loss”（失败）。

---

## 提示

- 下达命令后务必使用`advance()`命令。命令只有在游戏时间推进后才会生效。
- 使用`batch()`命令在同一帧内执行多个操作（例如：建造、移动、设置集结点）。
- 在建造前使用`get_available_production()`查看当前可建造的建筑物。
- 不要让生产停滞——持续安排单位建造任务。
- 将建筑物建造在建造场附近——建筑物必须与现有结构相邻。
- 能源至关重要——能源不足会严重影响生产速度。
- 前往敌人时使用`attack_move`而非`move`——这样单位会自动发起攻击。
- 建筑物建造完成后会自动进入建造队列——务必使用`build_and_place()`避免错误。

---

## 故障排除

| 问题 | 解决方法 |
|---------|----------|
| 服务器未运行 | 使用`openra-rl server start`命令启动服务器（需要Docker环境） |
| 无法建造建筑物 | 先使用`deploy_unit()`部署移动建筑车辆 |
| 建筑物无法放置 | 使用`get_valid_placements()`查找可放置的位置 |
| 资金不足 | 建造矿石精炼厂（`proc`）以获取更多收入 |
| 生产缓慢 | 使用`get_economy()`检查能源状况——必要时建造发电厂 |
| 无法找到敌人 | 使用`attack_move`命令侦察未探索的区域 |

## 链接

- **GitHub**: https://github.com/yxc20089/OpenRA-RL |
- **PyPI**: https://pypi.org/project/openra-rl/ |
- **排行榜**: https://huggingface.co/spaces/yxc20089/OpenRA-Bench |
- **Discord**: https://discord.gg/openra-rl |