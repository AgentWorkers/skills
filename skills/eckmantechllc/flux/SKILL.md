---
name: flux
description: 通过 Flux 状态引擎发布事件并查询共享的世界状态。当代理需要共享观察结果、协调共享数据或在不同系统之间跟踪实体状态时，可以使用该功能。
metadata:
  {
    "openclaw":
      {
        "emoji": "⚡",
        "requires": { "env": ["FLUX_TOKEN"] },
        "primaryEnv": "FLUX_TOKEN",
        "optionalEnv": ["FLUX_URL", "FLUX_ADMIN_TOKEN"],
      },
  }
---
# Flux 技能

Flux 是一个持久化、可共享的、基于事件驱动的状态管理系统。代理（agents）发布不可变事件，Flux 会生成所有代理都能观察到的统一状态。

## 关键概念

- **事件（Events）**：不可变的观测数据（例如温度读数、状态变化等）
- **实体（Entities）**：由事件派生的状态对象（如传感器、设备、代理）
- **属性（Properties）**：实体的键值对属性（在更新时会被合并；只有发生变化的属性才会被发送）
- **流（Streams）**：用于分类事件的逻辑命名空间（例如传感器、代理、系统）
- **命名空间（Namespaces）**：通过令牌认证实现多租户隔离（公共实例可选）

## 先决条件

**公共实例：** `https://api.flux-universe.com`（在 flux-universe.com 购买的命名空间；名称在购买时自动分配，例如 `dawn-coral`）
**本地实例：** `http://localhost:3000`（默认值，可通过 `FLUX_URL` 环境变量进行覆盖）

**认证要求：**  
公共实例需要设置 `FLUX_TOKEN` 为你的 bearer token；本地实例（如果禁用了认证）则不需要设置。

## 命名空间前缀

所有实体 ID 必须以你的命名空间为前缀：
`yournamespace/entity-name`

**示例（使用 `dawn-coral` 命名空间）：**
```bash
./scripts/flux.sh publish sensors agent-01 dawn-coral/sensor-01 \
  '{"temperature":22.5}'
./scripts/flux.sh get dawn-coral/sensor-01
```

在启用认证的实例中，没有命名空间前缀的实体 ID 将会被拒绝。

## 入门步骤

首先，验证你的连接：
```bash
./scripts/flux.sh health
```

然后查看目录，了解 Flux Universe 中可用的资源：
```bash
./scripts/flux.sh get flux-core/directory
```

该目录列出了所有活跃的命名空间、实体数量以及总实体数——这是了解系统中数据流动情况的好方法。

## 脚本

使用 `scripts/` 目录中的 bash 脚本：
- `flux.sh` — 主要的命令行工具

## 常见操作

### 发布事件（Publish Event）
```bash
./scripts/flux.sh publish <stream> <source> <entity_id> <properties_json>

# Replace dawn-coral with your namespace
# Example: Publish sensor reading
./scripts/flux.sh publish sensors agent-01 dawn-coral/temp-sensor-01 '{"temperature":22.5,"unit":"celsius"}'
```

### 查询实体状态（Query Entity State）
```bash
./scripts/flux.sh get <entity_id>

# Replace dawn-coral with your namespace
# Example: Get current sensor state
./scripts/flux.sh get dawn-coral/temp-sensor-01
```

### 列出所有实体（List All Entities）
```bash
./scripts/flux.sh list

# Filter by prefix
./scripts/flux.sh list --prefix scada/
```

### 删除实体（Delete Entity）
```bash
./scripts/flux.sh delete <entity_id>

# Example: Remove old test entity
./scripts/flux.sh delete test/old-entity
```

### 批量发布事件（Batch Publish Events）
```bash
# Replace dawn-coral with your namespace
./scripts/flux.sh batch '[
  {"stream":"sensors","source":"agent-01","payload":{"entity_id":"dawn-coral/sensor-01","properties":{"temp":22}}},
  {"stream":"sensors","source":"agent-01","payload":{"entity_id":"dawn-coral/sensor-02","properties":{"temp":23}}}
]'
```

### 检查连接器状态（Check Connector Status）
```bash
./scripts/flux.sh connectors
```

### 管理配置（Admin Config）
```bash
# Read runtime config
./scripts/flux.sh admin-config

# Update (requires FLUX_ADMIN_TOKEN)
./scripts/flux.sh admin-config '{"rate_limit_per_namespace_per_minute": 5000}'
```

## 使用场景

### 多代理协调（Multi-Agent Coordination）
代理将观测数据发布到共享实体中：
```bash
# Replace dawn-coral with your namespace
# Agent A observes temperature
flux.sh publish sensors agent-a dawn-coral/room-101 '{"temperature":22.5}'

# Agent B queries current state
flux.sh get dawn-coral/room-101
# Returns: {"temperature":22.5,...}
```

### 状态跟踪（Status Tracking）
跟踪服务/系统的状态：
```bash
# Replace dawn-coral with your namespace
# Publish status change
flux.sh publish system monitor dawn-coral/api-gateway '{"status":"healthy","uptime":3600}'

# Query current status
flux.sh get dawn-coral/api-gateway
```

## API 端点

**事件摄入（Event Ingestion）：**
- `POST /api/events` — 发布单个事件（限制大小为 1 MB）
- `POST /api/events/batch` — 发布多个事件（限制大小为 10 MB）

**状态查询（State Query）：**
- `GET /api/state/entities` — 列出所有实体（支持 `?prefix=` 和 `?namespace=` 过滤条件）
- `GET /api/state/entities/:id` — 获取特定实体

**实体管理（Entity Management）：**
- `DELETE /api/state/entities/:id` — 删除单个实体
- `POST /api/state/entities/delete` — 批量删除（按命名空间/前缀/ID 进行删除）

**实时更新（Real-time Updates）：**
- `GET /api/ws` — WebSocket 订阅

**连接器（Connectors）：**
- `GET /api/connectors` — 列出连接器及其状态
- `POST /api/connectors/:name/token` — 存储连接器的认证凭证
- `DELETE /api/connectors/:name/token` — 删除连接器的认证凭证

**管理（Admin）：**
- `GET /api/admin/config` — 读取运行时配置
- `PUT /api/admin/config` — 更新运行时配置（需要 `FLUX_ADMIN_TOKEN`）

**命名空间（仅限认证模式）：**
- `POST /api/namespaces` — 注册命名空间（返回认证令牌）

## 注意事项

- 事件会自动生成 UUID（无需提供 `eventId`）
- 实体的属性在更新时会被合并；只有发生变化的属性才会被发送
- 时间戳字段必须是 epoch 毫秒格式（i64）——这是 API 的要求，由 `flux.sh` 自动生成
- 状态数据会在 Flux 中持久保存（通过 NATS JetStream 和快照机制在重启后仍可访问）
- 实体 ID 支持使用 `/` 作为命名前缀（例如 `scada/pump-01`）