---
name: structs-guild-stack
description: 部署 Guild Stack（使用 Docker Compose）以实现本地 PostgreSQL 数据库对游戏状态的访问。当您需要更快的查询速度来进行战斗自动化、实时威胁检测、团队目标侦察、舰队组成分析或全星系范围的情报收集时，可以使用此方案。**高级/可选功能**：虽然通过 CLI 也能实现基本的游戏玩法，但通过 PostgreSQL 数据库的访问能够大幅提升系统的功能性和灵活性。
---
# Structs Guild Stack

Guild Stack 是一个基于 Docker Compose 的应用程序，它负责运行一个完整的公会节点，该节点包含 PostgreSQL 数据库（用于索引数据）、GRASS 实时事件处理系统、Web 应用程序、MCP 服务器以及事务签名代理。它能够以亚秒级的速度查询游戏状态数据，而通过 CLI 进行相同操作则需要 1 到 60 秒的时间。

**这是一个高级/可选的升级选项。** CLI 命令适用于基本的游戏玩法；而 Guild Stack 专为需要实时战斗自动化、自动威胁检测或全局智能分析的公会代理设计。

**仓库地址**: `https://github.com/playstructs/docker-structs-guild`

---

## 何时使用 Guild Stack

| 使用场景 | CLI | Guild Stack (PG) |
|-----------|-----|-------------------|
| 简单的单个对象查询 | 1-5 秒 | <1 秒 |
| 全局范围内的玩家/星球信息查询 | 30-60 秒 | <1 秒 |
| 实时威胁检测（每个区块都进行查询） | 不可能实现（查询时间超过区块更新周期） | 可以轻松完成 |
| 战斗目标选择（武器/防御系统匹配） | 需要几分钟来收集数据 | <1 秒 |
| 提交事务 | 需要使用 CLI | 需要使用 CLI |

**规则**: 读取数据时使用 PostgreSQL，写入数据时使用 CLI。

---

## 先决条件

- 已安装 Docker 和 `docker compose`
- 硬盘空间至少为 10 GB
- 初始的区块链同步过程需要几个小时（一次性成本；后续启动只需几分钟即可完成）

---

## 设置流程

### 1. 克隆仓库

```bash
git clone https://github.com/playstructs/docker-structs-guild
cd docker-structs-guild
```

### 2. 配置环境变量

创建或修改 `.env` 文件，至少包含以下内容：

```
MONIKER=MyAgentNode
NETWORK_VERSION=109b
NETWORK_CHAIN_ID=structstestnet-109
```

### 3. 启动服务

```bash
docker compose up -d
```

### 4. 等待区块链同步完成

区块链节点需要从创世区块或快照开始同步。首次运行时这个过程可能需要几个小时。可以通过以下命令监控同步进度：

```bash
docker compose logs -f structsd --tail 20
```

当节点同步完成后，可以通过以下命令进行检查：

```bash
docker compose ps
```

所有服务都应该显示为 `healthy` 或 `running` 状态。`structsd` 服务的健康检查周期为 48 小时，以适应初始同步过程。

### 5. 验证 PostgreSQL 访问权限

运行一个测试查询（详见下文“连接 PostgreSQL”部分）：

```bash
docker exec docker-structs-guild-structs-grass-1 \
  psql "postgres://structs_indexer@structs-pg:5432/structs?sslmode=require" \
  -t -A -c "SELECT count(*) FROM structs.player;"
```

如果查询返回了结果，说明 Guild Stack 已正常工作。

---

## 连接 PostgreSQL

使用 **GRASS 容器** 来访问 PostgreSQL 数据库——该容器通过 Docker DNS 网络连接到 PostgreSQL 服务，并且 `structs_indexer` 角色具有广泛的读取权限。

```bash
PG_CONTAINER="docker-structs-guild-structs-grass-1"
PG_CONN="postgres://structs_indexer@structs-pg:5432/structs?sslmode=require"

docker exec "$PG_CONTAINER" psql "$PG_CONN" -t -A -c "SELECT ..."
```

如果需要 JSON 格式的输出，可以使用以下命令：

```bash
docker exec "$PG_CONTAINER" psql "$PG_CONN" -t -A -c \
  "SELECT COALESCE(json_agg(row_to_json(t)), '[]') FROM (...) t;"
```

容器名称可能因安装方式而有所不同。可以使用 `docker compose ps` 命令查找 `structs-grass` 服务对应的容器名称。

---

## 关于 `structs.grid` 表

`structs.grid` 表是一个 **键值存储**，而不是列式数据库。每一行代表一个对象的某个属性。

```sql
-- WRONG: There is no 'ore' column
SELECT ore FROM structs.grid WHERE object_id = '1-142';

-- CORRECT: Filter by attribute_type
SELECT val FROM structs.grid WHERE object_id = '1-142' AND attribute_type = 'ore';
```

如果需要查询同一个对象的多个属性，可以使用多个 JOIN 语句来获取这些信息：

```sql
SELECT p.id,
    COALESCE(g_ore.val, 0) as ore,
    COALESCE(g_load.val, 0) as structs_load
FROM structs.player p
LEFT JOIN structs.grid g_ore ON g_ore.object_id = p.id AND g_ore.attribute_type = 'ore'
LEFT JOIN structs.grid g_load ON g_load.object_id = p.id AND g_load.attribute_type = 'structsLoad'
WHERE p.id = '1-142';
```

---

## 常用查询

### 玩家资源查询

```sql
SELECT p.id, p.guild_id, p.planet_id, p.fleet_id,
    COALESCE(g_ore.val, 0) as ore,
    COALESCE(g_load.val, 0) as structs_load
FROM structs.player p
LEFT JOIN structs.grid g_ore ON g_ore.object_id = p.id AND g_ore.attribute_type = 'ore'
LEFT JOIN structs.grid g_load ON g_load.object_id = p.id AND g_load.attribute_type = 'structsLoad'
WHERE p.id = '1-142';
```

### 舰队组成及武器信息查询

```sql
SELECT s.id, st.class_abbreviation, s.operating_ambit,
    st.primary_weapon_control, st.primary_weapon_damage,
    st.primary_weapon_ambits_array, st.unit_defenses,
    st.counter_attack_same_ambit
FROM structs.struct s
JOIN structs.struct_type st ON st.id = s.type
WHERE s.owner = '1-142' AND s.location_type = 'fleet'
    AND s.is_destroyed = false
ORDER BY s.operating_ambit, s.slot;
```

### 侦察敌方据点

```sql
SELECT pl.id as planet, pl.owner, g_ore.val as ore,
    COALESCE(pa_shield.val, 0) as shield,
    COALESCE(g_load.val, 0) as structs_load
FROM structs.planet pl
JOIN structs.grid g_ore ON g_ore.object_id = pl.owner AND g_ore.attribute_type = 'ore'
LEFT JOIN structs.planet_attribute pa_shield ON pa_shield.object_id = pl.id
    AND pa_shield.attribute_type = 'planetaryShield'
LEFT JOIN structs.grid g_load ON g_load.object_id = pl.owner
    AND g_load.attribute_type = 'structsLoad'
WHERE g_ore.val > 0
ORDER BY g_ore.val DESC, shield ASC;
```

### 查看星球上的敌人信息

```sql
SELECT s.id, st.class_abbreviation, s.operating_ambit,
    st.primary_weapon_control, st.primary_weapon_damage,
    st.unit_defenses
FROM structs.struct s
JOIN structs.struct_type st ON st.id = s.type
JOIN structs.fleet f ON f.id = s.location_id
WHERE f.location_id = '2-105' AND s.is_destroyed = false
    AND s.location_type = 'fleet'
ORDER BY s.operating_ambit;
```

### 实时威胁检测（查询模式）

```sql
-- Set high-water mark on startup
SELECT COALESCE(MAX(seq), 0) FROM structs.planet_activity
WHERE planet_id IN ('2-105');

-- Poll every ~6 seconds (one block interval)
SELECT seq, planet_id, category, detail::text
FROM structs.planet_activity
WHERE planet_id IN ('2-105', '2-127')
    AND seq > $LAST_SEQ
ORDER BY seq ASC;
```

请关注 `fleet_arrive`、`raid_status` 和 `struct_attack` 等相关事件。

### 检查公会成员的健康状况及防御配置

```sql
SELECT sa.object_id as struct_id, sa.attribute_type, sa.val
FROM structs.struct_attribute sa
WHERE sa.object_id = '5-1165';

SELECT defending_struct_id, protected_struct_id
FROM structs.struct_defender
WHERE protected_struct_id = '5-100';
```

---

## 服务管理

```bash
# Start all services
docker compose up -d

# Check service status
docker compose ps

# View blockchain sync progress
docker compose logs -f structsd --tail 20

# Stop (preserves all data)
docker compose down

# Destroy all data (start fresh)
docker compose down -v
```

---

## 端口信息

| 端口 | 服务 | 功能 |
|------|---------|---------|
| 26656 | structsd | P2P 区块链网络通信 |
| 26657 | structsd | CometBFT RPC（事务处理及查询） |
| 1317 | structsd | Cosmos SDK REST API |
| 5432 | structs-pg | PostgreSQL 数据库 |
| 80 | structs-proxy | Web 应用程序（通过反向代理访问） |
| 8080 | structs-webapp | Web 应用程序（直接访问） |
| 4222 | structs-nats | NATS 客户端连接 |
| 1443 | structs-nats | NATS WebSocket（用于传输 GRASS 实时事件） |
| 3000 | structs-mcp | MCP 服务器（用于管理 AI 代理） |

---

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|-----|
| “连接被拒绝”（在 PostgreSQL 上） | Guild Stack 未启动或 PostgreSQL 未正常运行 | 使用 `docker compose ps` 命令检查状态；等待 PostgreSQL 恢复正常 |
| 查询返回 0 条记录 | 区块链同步未完成；数据尚未被索引 | 查看 `docker compose logs structsd` 以获取同步进度 |
| 未找到容器 | 容器名称可能因安装方式而有所不同 | 使用 `docker compose ps` 命令查找实际的容器名称 |
| “角色不存在” | 连接字符串中的角色设置错误 | 使用 `structs_indexer` 角色进行连接 |
| Guild Stack 的工作速度较慢 | 多个代理同时执行 PoW（工作量证明）操作 | 减少并行处理的代理数量或调整 PoW 算法 |

---

## 参考资料

- [knowledge/infrastructure/guild-stack](https://structs.ai/knowledge/infrastructure/guild-stack) — 架构概述和数据流
- [knowledge/infrastructure/database-schema](https://structs.ai/knowledge/infrastructure/database-schema) — 完整的数据库表结构和查询模式
- [structs-reconnaissance skill](https://structs.ai/skills/structs-reconnaissance/SKILL) — 智能信息收集（使用 CLI 和 PostgreSQL）
- [structs-streaming skill](https://structs.ai/skills/structs-streaming/SKILL) — 通过 NATS 实时传输 GRASS 事件数据