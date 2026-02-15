---
name: flux
description: 通过 Flux 状态引擎发布事件并查询共享的世界状态。当代理需要共享观察结果、协调共享数据，或在不同系统之间跟踪实体状态时，可以使用该机制。
---

# Flux 技能

Flux 是一个持久化、可共享的、基于事件驱动的状态管理引擎。代理（agents）发布不可变的事件（immutable events），Flux 会生成所有代理都能观察到的统一状态（canonical state）。

## 关键概念

- **事件（Events）**：不可变的观测值（例如温度读数、状态变化、代理操作）
- **实体（Entities）**：由事件派生的状态对象（例如传感器、设备、代理、任务）
- **属性（Properties）**：实体的键值对（在更新时采用“最后写入者胜出”（last-write-wins）的规则进行合并）
- **流（Streams）**：事件的逻辑分类（例如传感器数据、系统状态、负载测试数据）

## 先决条件

**Flux 实例：**
- 默认地址：`http://localhost:3000`（本地实例）
- 可通过 `export FLUX_URL=https://your-flux-url.com` 进行自定义
- 公共沙箱地址：`https://flux.eckman-tech.com`

**选项：**
1. 在本地运行 Flux — 请参考 [Flux 仓库](https://github.com/EckmanTechLLC/flux)
2. 使用公共沙箱实例
3. 部署自己的实例（使用 Docker 和 NATS JetStream）

## 脚本

请使用 `scripts/` 目录中的 CLI 工具：

```bash
./scripts/flux.sh health          # Test connection
./scripts/flux.sh list            # List all entities
./scripts/flux.sh list host-      # Filter by prefix
./scripts/flux.sh get sensor-01   # Get entity state
./scripts/flux.sh publish sensors my-agent sensor-01 '{"temp":22.5}'
./scripts/flux.sh delete sensor-01                   # Delete one
./scripts/flux.sh delete --prefix loadtest-          # Batch delete
./scripts/flux.sh delete --namespace sandbox         # Delete namespace
```

## 实体命名规范

**命名规则：** 使用描述性前缀来分组实体：
- `host-*` — 服务器/虚拟机（例如 `host-web-01`）
- `sensor-*` — 物理传感器（例如 `sensor-temp-01`）
- `agent-*` — 人工智能代理（例如 `agent-arc-01`）
- `task-*` — 工作任务（例如 `task-build-123`）
- 分隔符：`-` 用于表示扁平化的 ID；`:` 用于表示带类型的 ID（例如 `agent:manager`）；`/` 用于表示命名空间化的 ID（例如 `matt/sensor-01`）

**流的分类：** 事件的逻辑分类：
- `system` — 基础设施信息、状态更新
- `sensors` — 设备读数、物联网数据
- `loadtest` — 测试数据/合成数据

**属性（Properties）：** 平面的键值对。常见属性包括：
- `status` — 实体状态（在线、正常、警告、错误）
- `activity` — 实体当前正在执行的操作
- `command` + `cmd_id` — 双向控制（通过更改 `cmd_id` 来触发特定操作）

## 常见用法

### 发布代理状态
```bash
# Publish your agent's status to the world
flux.sh publish system my-agent my-agent-01 '{"status":"online","activity":"monitoring"}'
```

### 双向设备控制
```bash
# Send command to a device (device watches for cmd_id changes)
flux.sh publish sensors controller device-01 '{"command":"set_mode","mode":"active","cmd_id":"cmd-001"}'
```

### 多代理协调
```bash
# Agent A writes a message
flux.sh publish system agent-a agent-a-01 '{"message":"found anomaly in sector 7","message_to":"agent-b"}'

# Agent B reads it
flux.sh get agent-a-01
```

### 监控与警报
```bash
# List all entities, pipe through jq for analysis
flux.sh list | jq '[.[] | {id, status: .properties.status}]'
```

## API 参考

| 方法（Method） | 端点（Endpoint） | 描述（Description） |
|--------|----------|-------------|
| POST | /api/events | 发布单个事件 |
| POST | /api/events/batch | 批量发布多个事件 |
| GET | /api/state/entities | 列出所有实体 |
| GET | /api/state/entities?prefix=X | 按前缀过滤实体 |
| GET | /api/state/entities/:id | 获取单个实体 |
| DELETE | /api/state/entities/:id | 删除单个实体 |
| POST | /api/state/entities/delete | 批量删除实体（通过前缀或命名空间和 ID 进行删除） |
| WS | /api/ws | 订阅实时状态更新 |

## WebSocket 订阅

通过连接到 `/api/ws` 来接收实时状态更新：

```json
// Subscribe to one entity
{"type": "subscribe", "entity_id": "sensor-01"}

// Subscribe to ALL entities
{"type": "subscribe", "entity_id": "*"}

// Receive updates
{"type": "state_update", "entity_id": "sensor-01", "property": "temp", "value": 22.5, "timestamp": "..."}

// Receive metrics (every 2s)
{"type": "metrics_update", "entities": {"total": 15}, "events": {"total": 50000, "rate_per_second": 120.5}, ...}

// Entity deleted notification
{"type": "entity_deleted", "entity_id": "sensor-01", "timestamp": "..."}
```

## 注意事项：

- 事件会自动生成 UUID，无需手动提供 `eventId`
- 实体的属性在更新时会合并（采用“最后写入者胜出”的规则）
- 状态会在重启后保持不变（通过 NATS JetStream 和定期快照实现）
- 如果未提供时间戳，系统会使用当前时间
- 认证是可选的：`FLUX_AUTH_ENABLED=true` 可启用基于命名空间的令牌认证
- 命名空间化的实体使用以下格式：`namespace/entity-id`