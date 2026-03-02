---
name: structs-streaming
description: 通过 NATS WebSocket 连接到 GRASS 实时事件系统。当您需要实时游戏更新、希望在事件发生时立即做出反应、需要监控袭击或攻击、观察玩家创建情况、追踪舰队移动，或构建基于事件的工具时，可以使用该功能。GRASS 是获取银河系内最新动态的最快捷方式。
---
# 结构体流式传输（GRASS）

GRASS（游戏实时应用流式传输服务）通过NATS提供实时游戏事件。与其重复进行轮询查询，不如订阅GRASS，在事件发生时立即做出响应。

## 何时使用GRASS

| 情况 | 使用GRASS | 使用轮询 |
|-----------|-----------|-------------|
| 检测入侵 | 是 — 立即警报 | 轮询太慢 |
| 等待公会成员创建 | 是 — 监听`address_register`事件 | 每10秒轮询一次也可以 |
| 监控舰队抵达你的星球 | 是 — `fleet_arrive`事件 | 可能会错过事件 |
| 在战斗中跟踪结构体状态 | 是 — `planet_activity`和`struct_health` | 轮询太慢 |
| 检查自己的资源余额 | 否 | 是 — 一次性查询 |
| 读取结构体类型统计信息 | 否 | 是 — 静态数据 |

**经验法则**：如果你需要对某些事件做出*反应*，使用GRASS；如果你需要*读取*数据，使用轮询查询。

---

## 查找你的GRASS端点

GRASS的WebSocket地址**不是硬编码的**——它来自公会配置：

1. 查询公会列表：`curl http://reactor.oh.energy:1317/structs/guild`
2. 跟随公会的`endpoint` URL获取其配置
3. 查找`services.grass_nats_websocket`

示例（Orbital Hydro公会）：

```json
{
  "services": {
    "grass_nats_websocket": "ws://crew.oh.energy:1443",
    "guild_api": "http://crew.oh.energy/api/",
    "reactor_api": "http://reactor.oh.energy:1317/"
  }
}
```

`grass_nats_websocket`值就是你的NATS WebSocket端点。并非所有公会都提供这项服务——在使用前请先确认。

一个可靠的参考端点：**`ws://crew.oh.energy:1443`**（Orbital Hydro / Slow Ninja）。

---

## 先进行发现

在订阅特定主题之前，**先订阅通配符`>`，以查看所有通过GRASS服务器传输的数据**。这会揭示实际使用的主题模式，这些模式可能与文档中的有所不同。

```javascript
const sub = nc.subscribe(">");
for await (const msg of sub) {
  console.log(`[${msg.subject}]`, new TextDecoder().decode(msg.data));
}
```

观察输出30-60秒。你会看到诸如`structs.planet.2-1`、`consensus`、`healthcheck`等主题。一旦你知道哪些主题包含你需要的事件，就可以将订阅范围缩小到这些特定主题。

**重要提示**：结构体事件（攻击、建造、状态变化）通常会出现在**planet主题**上，而不是结构体主题上。如果你没有收到预期的结构体事件，请订阅该结构体的planet主题。

---

## 主题模式

订阅与你关心的实体匹配的主题：

| 实体 | 通配符 | 具体主题 | 示例 |
|--------|----------|----------|---------|
| 玩家 | `structs.player.*` | `structs.player.{guild_id}.{player_id}` | `structs.player.0-1.1-11` |
| 行星 | `structs.planet.*` | `structs.planet.{planet_id}` | `structs.planet.2-1` |
| 公会 | `structs.guild.*` | `structsguild.{guild_id}` | `structsguild.0-1` |
| 结构体 | `structs.struct.*` | `structs.struct.{struct_id}` | `structs.struct.5-1` |
| 舰队 | `structs.fleet.*` | `structs.fleet.{fleet_id}` | `structs.fleet.9-1` |
| 地址 | `structs.address.register.*` | `structs.address.register.{code}` | -- |
| 库存 | `structs.inventory.>` | `structsinventory.{denom}.{guild_id}.{player_id}.{address}` | 令牌移动 |
| 网格 | `structs.grid.*` | `structs.grid.{object_id}` | 属性变化（矿石、能量等） |
| 全局 | `structs.global` | `structs.global` | 块更新 |
| 共识 | `consensus` | `consensus` | 链式共识事件 |
| 健康检查 | `healthcheck` | `healthcheck` | 节点健康状态 |

使用通配符（`*`）来发现存在的事件。一旦知道需要什么，再缩小订阅范围到具体主题。使用`>`可以查看所有数据（参见上面的“先进行发现”部分）。

---

## 事件类型

### 行星事件

| 事件 | 描述 | 应对方式 |
|-------|-------------|----------|
| `raid_status` | 行星上发起/完成袭击 | 激活防御系统，发出警报 |
| `planet_activity` | 包括`struct_health`变化在内的活动日志 | 跟踪战斗伤害 |
| `fleet_arrive` | 舰队抵达行星 | 准备防御或欢迎 |
| `fleet_depart` | 舰队离开行星 | 更新威胁评估 |

### 结构体事件

**注意**：结构体事件通常会出现在**planet主题**（`structs.planet.{id}`）上，而不是结构体主题上。如果你需要全面覆盖，需要同时订阅这两个主题。

| 事件 | 描述 | 应对方式 |
|-------|-------------|----------|
| `struct_attack` | 结构体受到攻击 | 反击，修复 |
| `struct_status` | 结构体状态变化（在线/离线/被摧毁） | 重建，重新分配能量 |
| `struct_defense_add` / `struct_defense_remove` | 防御任务变更 | 更新防御地图 |
| `struct_defender_clear` | 所有防御关系清除 | 重新分配防御者 |
| `struct_block_build_start` | 建造操作开始 | 在任务列表中跟踪 |
| `struct_block_ore_mine_start` | 采矿操作开始 | 在任务列表中跟踪 |
| `struct_block_ore_refine_start` | 精炼操作开始 | 在任务列表中跟踪 |

### 玩家事件

| 事件 | 描述 | 应对方式 |
|-------|-------------|----------|
| `player_consensus` | 玩家链式数据更新 | 更新情报 |
| `player_meta` | 玩家元数据变化 | 更新情报 |

### 公会事件

| 事件 | 描述 | 应对方式 |
|-------|-------------|----------|
| `guild_consensus` | 公会链式数据更新 | 更新公会状态 |
| `guild_membership` | 成员加入/离开公会 | 更新关系图 |

### 库存事件

主题：`structsinventory.{denom}.{guild_id}.{player_id}.{address}`

跟踪令牌移动——Alpha物质、公会令牌、矿石等：

| 类别 | 描述 | 应对方式 |
|----------|-------------|----------|
| `sent` | 该玩家发送的令牌 | 更新余额追踪 |
| `received` | 该玩家接收的令牌 | 更新余额追踪 |
| `seized` | 通过袭击夺取的令牌 | 触发反袭击或精炼警报 |
| `mined` | 采出的矿石 | 立即开始精炼 |
| `refined` | 矿石精炼成Alpha物质 | 更新财富追踪 |
| `minted` | 公会铸造的令牌 | 跟踪公会经济 |
| `infused` | Alpha物质注入反应堆/发电机 | 更新容量追踪 |
| `forfeited` | 令牌丢失（处罚等） | 调查原因 |

### 网格事件

主题：`structs.grid.{object_id}`

跟踪任何游戏对象（玩家、结构体、行星）的属性变化：

| 类别 | 描述 | 应对方式 |
|----------|-------------|----------|
| `capacity` | 能量容量变化 | 检查是否接近离线状态 |
| `connectionCapacity` | 连接容量变化 | 更新能量路由 |
| `connectionCount` | 连接数量变化 | 更新能量路由 |
| `fuel` | 燃料水平变化 | 监控发电机/反应堆 |
| `lastAction` | 最后操作时间戳更新 | 跟踪活动 |
| `load` | 能量负载变化 | 检查是否接近离线状态 |
| `nonce` | 玩家nonce值增加 | 检测活动（有助于侦察） |
| `ore` | 矿石余额变化 | 如果是你的矿石，立即进行精炼；如果是敌人的矿石，视为袭击目标 |
| `player_consensus` | 玩家共识数据更新 | 更新情报 |
| `power` | 能量水平变化 | 监控能源基础设施 |
| `proxyNonce` | 代理nonce值变化 | 检测代理活动 |
| `structsLoad` | 结构体负载变化 | 评估舰队实力变化 |

### 战斗事件的有效载荷

`struct_attack`事件包含详细的逐次射击信息。示例有效载荷（在planet主题上观察到）：

```json
{
  "category": "struct_attack",
  "attackingStructId": "5-100",
  "targetStructId": "5-200",
  "weaponSystem": "primary",
  "eventAttackShotDetail": [
    {
      "shotIndex": 0,
      "damage": 2,
      "evaded": false,
      "blocked": false,
      "blockerStructId": "",
      "counterAttackDamage": 1,
      "counterAttackerStructId": "5-200"
    }
  ],
  "attackerHealthRemaining": 2,
  "targetHealthRemaining": 1,
  "targetDestroyed": false,
  "attackerDestroyed": false
}
```

`eventAttackShotDetail`中的关键字段：
- `evaded` — 如果射击未命中（防御类型交互）
- `blocked` — 如果防御者拦截了射击
- `blockerStructId` — 防御者是谁（如果有的话）
- `counterAttackDamage` / `counterAttackerStructId` — 每次射击的反击信息

`struct_health`事件用于跟踪生命值变化：

```json
{
  "category": "struct_health",
  "structId": "5-200",
  "health": 1,
  "maxHealth": 3,
  "destroyed": false
}
```

### 噪音过滤

`consensus`和`healthcheck`主题会频繁触发（每隔几秒一次）。在使用通配符`>`进行发现时，需要过滤掉这些事件，以查看真正的游戏事件：

```javascript
const sub = nc.subscribe(">");
for await (const msg of sub) {
  if (msg.subject === "consensus" || msg.subject === "healthcheck") continue;
  console.log(`[${msg.subject}]`, new TextDecoder().decode(msg.data));
}
```

### 全局事件

| 事件 | 描述 | 应对方式 |
|-------|-------------|----------|
| `block` | 新块产生 | 更新游戏循环，计算电荷 |

---

## 构建事件监听工具

代理应构建自定义工具，在需要基于事件驱动的行为时连接到GRASS。以下是可遵循的模式：

### 最简单的Node.js监听器

安装NATS WebSocket客户端：

```bash
npm install nats.ws
```

```javascript
import { connect } from "nats.ws";

const nc = await connect({ servers: "ws://crew.oh.energy:1443" });

const sub = nc.subscribe("structs.planet.2-1");
for await (const msg of sub) {
  const event = JSON.parse(new TextDecoder().decode(msg.data));
  console.log(JSON.stringify(event));
}
```

### 最简单的Python监听器

安装NATS客户端：

```bash
pip install nats-py
```

### 袭击警报工具（示例模式）

一个监控你的星球上是否有袭击并输出警报的工具：

```javascript
import { connect } from "nats.ws";

const PLANET_ID = process.argv[2]; // e.g. "2-1"
const nc = await connect({ servers: "ws://crew.oh.energy:1443" });
const sub = nc.subscribe(`structs.planet.${PLANET_ID}`);

for await (const msg of sub) {
  const event = JSON.parse(new TextDecoder().decode(msg.data));
  if (event.category === "raid_status") {
    console.log(JSON.stringify({ alert: "RAID", planet: PLANET_ID, data: event }));
  }
  if (event.category === "fleet_arrive") {
    console.log(JSON.stringify({ alert: "FLEET_ARRIVAL", planet: PLANET_ID, data: event }));
  }
}
```

### 玩家创建监视器（示例模式）

在公会成员创建后，不要轮询`structsd query structs address`，而是监听地址注册事件：

```javascript
import { connect } from "nats.ws";

const nc = await connect({ servers: "ws://crew.oh.energy:1443" });
const sub = nc.subscribe("structs.address.register.*");

for await (const msg of sub) {
  const event = JSON.parse(new TextDecoder().decode(msg.data));
  console.log(JSON.stringify(event));
  break; // exit after first match
}
await nc.close();
```

---

## 何时构建自定义工具

在以下情况下构建GRASS监听工具：

- **你需要等待某个事件**——例如公会成员创建完成、舰队抵达、检测到袭击
- **你需要持续监控**——例如在矿石资源易受攻击的窗口期间检测威胁、跟踪战斗情况
- **你希望使用事件驱动的游戏循环**——根据事件进行响应，而不是定时轮询
- **你管理多个玩家**——一个GRASS连接可以同时监控所有实体

将自定义工具存储在工作区（例如`scripts/`文件夹中）或与相关技能文件放在一起。

---

## 连接最佳实践

- **一旦知道需要什么，就使用具体的主题**。通配符用于发现新事件。
- **每个连接限制订阅数量在10-20个以内**，以避免客户端负担过重。
- **实现指数级退避的重连机制**——NATS连接可能会中断。
- **谨慎解析JSON数据**——并非所有消息都符合预期的格式。
- **使用完毕后关闭连接**。不要让闲置的GRASS连接保持打开状态。

---

## 流程

### 快速设置

1. 从公会配置中获取GRASS端点（或使用`ws://crew.oh.energy:1443`）
2. 将端点记录在`TOOLS.md`的`Servers`部分
3. 选择你使用的语言（Node.js或Python）
4. 安装NATS客户端库（Node.js使用`nats.ws`，Python使用`nats-py`）
5. 为你的具体用途编写监听脚本
6. 在后台终端中运行脚本

### 持续监控

1. 订阅你的星球：`structs.planet.{id}`——接收袭击警报、舰队抵达信息
2. 订阅你的结构体：`structs.struct.{id}`——接收攻击/状态警报
3. 订阅全局事件：`structs.global`——用于游戏循环的定时更新
4. 将事件日志记录到`memory/`文件夹中，以便跨会话查看

---

## 参考资料

- [protocols/streaming](https://structs.ai/protocols/streaming) — 完整的GRASS/NATS协议规范
- [api/streaming/event-types](https://structs.ai/api/streaming/event-types) — 完整的事件类型目录
- [api/streaming/event-schemas](https://structs.ai/api/streaming/event-schemas) — 事件有效载荷的JSON格式定义
- [api/streaming/subscription-patterns](https://structs.ai/api/streaming/subscription-patterns) — 订阅模式和示例
- [awareness/async-operations](https://structs.ai/awareness/async-operations) — 背景操作和管道策略
- [awareness/threat-detection](https://structs.ai/awareness/threat-detection) — 使用GRASS进行早期预警