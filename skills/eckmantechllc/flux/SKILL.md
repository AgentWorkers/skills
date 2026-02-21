---
name: flux
description: 通过 Flux 状态引擎发布事件并查询共享的世界状态。当代理需要共享观察结果、协调共享数据，或在不同系统之间跟踪实体状态时，请使用该功能。
---
# Flux 技能

Flux 是一个持久化、可共享的、基于事件驱动的状态管理引擎。各个代理（agents）会发布不可变的事件（immutable events），Flux 会根据这些事件生成一个所有代理都能观察到的统一状态（canonical state）。

## 关键概念

- **事件（Events）**：不可变的观测数据（例如温度读数、状态变化等）  
- **实体（Entities）**：由事件派生的状态对象（例如传感器、设备、代理等）  
- **属性（Properties）**：实体的键值对属性；在更新时这些属性会被合并（仅需要发送发生变化的属性）  
- **流（Streams）**：用于分类事件的逻辑命名空间（例如传感器、代理、系统等）  
- **命名空间（Namespaces）**：支持多租户隔离，并可通过令牌（token）进行身份验证（仅适用于公共实例）

## 先决条件

Flux 运行在 `http://localhost:3000`（默认地址，可通过 `FLUX_URL` 环境变量进行修改）

身份验证：可选。在连接到支持身份验证的实例时，请设置 `FLUX_TOKEN` 环境变量。

## 测试

验证 Flux 连接：
```bash
./scripts/flux.sh health
```

## 脚本

请使用 `scripts/` 目录中的 bash 脚本：
- `flux.sh`：主要的命令行工具（CLI）

## 常用操作

### 发布事件（Publish Event）
```bash
./scripts/flux.sh publish <stream> <source> <entity_id> <properties_json>

# Example: Publish sensor reading
./scripts/flux.sh publish sensors agent-01 temp-sensor-01 '{"temperature":22.5,"unit":"celsius"}'
```

### 查询实体状态（Query Entity State）
```bash
./scripts/flux.sh get <entity_id>

# Example: Get current sensor state
./scripts/flux.sh get temp-sensor-01
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
./scripts/flux.sh batch '[
  {"stream":"sensors","source":"agent-01","payload":{"entity_id":"sensor-01","properties":{"temp":22}}},
  {"stream":"sensors","source":"agent-01","payload":{"entity_id":"sensor-02","properties":{"temp":23}}}
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
代理将观测数据发布到共享的实体中：
```bash
# Agent A observes temperature
flux.sh publish sensors agent-a room-101 '{"temperature":22.5}'

# Agent B queries current state
flux.sh get room-101
# Returns: {"temperature":22.5,...}
```

### 状态跟踪（Status Tracking）
跟踪服务/系统的状态：
```bash
# Publish status change
flux.sh publish system monitor api-gateway '{"status":"healthy","uptime":3600}'

# Query current status
flux.sh get api-gateway
```

## API 端点（API Endpoints）

**事件摄入（Event Ingestion）：**
- `POST /api/events` — 发布单个事件（文件大小限制为 1 MB）
- `POST /api/events/batch` — 批量发布事件（文件大小限制为 10 MB）

**状态查询（State Query）：**
- `GET /api/state/entities` — 列出所有实体（支持 `?prefix=` 和 `?namespace=` 过滤条件）
- `GET /api/state/entities/:id` — 获取特定实体

**实体管理（Entity Management）：**
- `DELETE /api/state/entities/:id` — 删除单个实体
- `POST /api/state/entities/delete` — 按命名空间/前缀/ID 批量删除实体

**实时更新（Real-time Updates）：**
- `GET /api/ws` — WebSocket 订阅服务

**连接器（Connectors）：**
- `GET /api/connectors` — 列出连接器及其状态
- `POST /api/connectors/:name/token` — 存储连接器的认证凭证
- `DELETE /api/connectors/:name/token` — 删除连接器的认证凭证

**管理（Admin）：**
- `GET /api/admin/config` — 读取运行时配置
- `PUT /api/admin/config` — 更新运行时配置（需要 `FLUX_ADMIN_TOKEN`）

**命名空间（仅限身份验证模式）（Namespaces [only for authentication mode]：**
- `POST /api/namespaces` — 注册新的命名空间（返回认证令牌）

## 注意事项

- 事件会自动生成 UUID（无需手动提供 `eventId`）
- 在更新时属性会被合并；仅发送发生变化的属性，原有属性会保留
- 如果提供了时间戳字段，必须使用 epoch 毫秒格式（i64），否则默认使用当前时间
- 状态数据会在重启后通过 NATS JetStream 和快照机制持久保存
- 实体 ID 支持使用 `/` 进行命名空间划分（例如 `scada/pump-01`）