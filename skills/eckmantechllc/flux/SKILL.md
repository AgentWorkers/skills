---
name: flux
description: 通过 Flux 状态引擎发布事件并查询共享的世界状态。当代理需要共享观察结果、协调共享数据，或在不同系统之间跟踪实体状态时，可以使用该功能。
---

# Flux 技能

Flux 是一个持久化、可共享的、基于事件驱动的状态管理引擎。各个代理（agents）会发布不可变的数据（即事件），Flux 会根据这些事件生成一个所有代理都能观察到的统一状态。

## 关键概念

- **事件（Events）**：不可变的观测数据（例如温度读数、状态变化等）  
- **实体（Entities）**：由事件派生的状态对象（如传感器、设备、代理等）  
- **属性（Properties）**：实体的键值对属性  
- **流（Streams）**：用于分类事件的逻辑命名空间（例如传感器、代理、系统等）  

## 先决条件

**Flux 实例：**  
- 默认地址：`http://localhost:3000`（本地实例）  
- 可以通过 `export FLUX_URL=https://your-flux-url.com` 来自定义地址  

**选项：**  
1. 在本地运行 Flux（详情请参阅 [Flux 仓库](https://github.com/EckmanTechLLC/flux)）  
2. 使用公共测试实例：`https://deutschland-jackie-substantially-pee.trycloudflare.com`  
3. 部署自己的 Flux 实例  

当前设置无需身份验证。  

## 测试

验证 Flux 连接：  
```bash
./scripts/flux.sh health
```  

## 脚本  

请使用 `scripts/` 目录中的 bash 脚本：  
- `flux.sh`：主要的命令行工具  

## 常见操作  

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

# Shows all entities in current world state
```  

### 批量发布事件（Batch Publish Events）  
```bash
./scripts/flux.sh batch '[
  {"stream":"sensors","source":"agent-01","payload":{"entity_id":"sensor-01","properties":{"temp":22}}},
  {"stream":"sensors","source":"agent-01","payload":{"entity_id":"sensor-02","properties":{"temp":23}}}
]'
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
跟踪服务/系统的状态变化：  
```bash
# Publish status change
flux.sh publish system monitor api-gateway '{"status":"healthy","uptime":3600}'

# Query current status
flux.sh get api-gateway
```  

### 基于事件的数据管理（Event-Sourced Data Management）  
- 所有的状态变化都通过事件来驱动；  
- 事件是不可变的（不会被删除或修改）；  
- 状态是根据事件历史生成的；  
- 可以重放或审计全部事件历史记录。  

## API 端点（API Endpoints）  

- `POST /api/events`：发布单个事件  
- `POST /api/events/batch`：批量发布事件  
- `GET /api/state/entities`：列出所有实体  
- `GET /api/state/entities/:id`：获取特定实体  

完整的 API 文档请参阅 `references/api.md`。  

## 注意事项  

- 事件会自动生成唯一的 UUID（无需手动提供 `eventId`）；  
- 在更新时，实体的属性会合并（以最后一次写入的值为准）；  
- 状态数据会在 Flux 中持久保存（即使重启也能保留）；  
- 如果未提供时间戳，系统会使用当前时间作为默认值。