---
name: teamgram-server-architecture
description: >
  **Teamgram服务器架构指南：用于构建兼容Telegram的后端系统**  
  本指南适用于设计服务拓扑结构、实现MTProto协议服务或自行托管Teamgram服务器的场景。内容涵盖了服务拆分、数据流处理、部署模式以及基于官方teamgram/teamgram-server仓库的开发工作流程。
version: 1.0.0
---
# Teamgram 服务器架构

本文档基于官方的 teamgram/teamgram-server 仓库，提供了完整的架构指南。

## 概述

Teamgram 服务器是一个非官方的开源 MTProto 服务器实现，使用 Go 语言编写，兼容 Telegram 客户端，并支持自托管部署。

- **API 层**：223
- **MTProto 版本**：简略版、中间版、扩展版、完整版

## 核心功能

- ✅ **私密聊天**：端到端加密的消息传递
- ✅ **普通群组**：小型群组聊天（最多 200 人）
- ⚠️ **超级群组**：大型群组（需要额外实现）
- ✅ **联系人**：联系人管理和同步
- ✅ **Web**：支持 Web 客户端

## 服务架构

### 高层拓扑结构

```
                    ┌─────────────────┐
                    │   Load Balancer │
                    │    (Nginx/HA)   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐   ┌────────▼────────┐   ┌──────▼──────┐
│   gnetway     │   │   httpserver    │   │   session   │
│  (TCP/MTProto)│   │   (HTTP API)    │   │ (WebSocket) │
└───────┬───────┘   └────────┬────────┘   └──────┬──────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   BFF Layer     │
                    │ (Business Logic)│
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐   ┌────────▼────────┐   ┌──────▼──────┐
│   Service     │   │    Service      │   │   Service   │
│   Layer       │   │    Layer        │   │   Layer     │
└───────────────┘   └─────────────────┘   └─────────────┘
```

### 接口层（app/interface）

| 服务 | 协议 | 功能 |
|---------|----------|---------|
| **gnetway** | TCP/MTProto | 主要客户端网关，处理 MTProto 加密 |
| **httpserver** | HTTP/REST | 机器人 API 和 Webhook |
| **session** | WebSocket | Web 客户端连接管理 |

### 后端转发层（app/bff）

- 负责聚合多个服务调用
- 处理特定于客户端的逻辑
- 降低客户端端的复杂性

### 服务层（app/service）

| 服务 | 负责内容 | 关键功能 |
|---------|----------------|--------------|
| **authsession** | 认证与会话管理 | 认证密钥管理、会话验证 |
| **biz** | 核心业务逻辑 | 聊天、消息处理、用户管理、对话记录、更新 |
| **dfs** | 分布式文件存储 | 文件上传/下载，集成 MinIO |
| **geoip** | 地理位置信息 | 基于 IP 的地理位置判断 |
| **idgen** | ID 生成 | 使用 Snowflake 方式生成分布式 ID |
| **media** | 媒体处理 | 生成缩略图，集成 FFmpeg |
| **status** | 用户在线状态 | 显示用户在线状态、最后可见时间 |

### 消息传递层（app/messenger）

| 服务 | 功能 | 描述 |
|---------|---------|----------------|
| **msg** | 消息路由与传递 |
| **sync** | 多设备消息同步 |

## `biz` 服务详解

`biz` 服务是一个负责处理核心业务逻辑的模块：

```
app/service/biz/
├── biz/        # Core business operations
├── chat/       # Group/channel management
├── code/       # Verification codes (SMS/email)
├── dialog/     # Conversation management
├── message/    # Message storage and retrieval
├── updates/    # Real-time updates push
└── user/       # User profiles and settings
```

### 推荐的代码重构方案

对于大规模部署，建议将 `biz` 服务拆分为多个独立的服务：

```
chat-service/      - Group & channel management
message-service/   - Message CRUD and search
user-service/      - User profiles and contacts
notification-service/ - Push notifications
```

## 数据流

### 消息发送流程

```
Client → gnetway → session → msg → message (biz)
                                           ↓
                                    MySQL (persist)
                                           ↓
                                    Kafka (broadcast)
                                           ↓
                              sync → updates → Client
```

### 认证流程

```
Client → gnetway → authsession
                        ↓
                   MySQL (auth_keys)
                        ↓
                   Redis (sessions)
```

### 文件上传流程

```
Client → gnetway → dfs → MinIO
                  ↓
               MySQL (file_metadata)
```

## 基础设施依赖

| 组件 | 功能 | 必需条件 |
|-----------|---------|----------|
| **MySQL 5.7+** | 主数据存储 | ✅ 是 |
| **Redis** | 缓存、会话管理、去重 | ✅ 是 |
| **etcd** | 服务发现与配置管理 | ✅ 是 |
| **Kafka** | 消息队列、事件处理 | ✅ 是 |
| **MinIO** | 对象存储 | ✅ 是 |
| **FFmpeg** | 媒体转码 | ⚠️ 可选 |

## 项目结构

```
teamgram-server/
├── app/
│   ├── bff/              # Backend-for-Frontend
│   ├── interface/        # Gateway layer
│   │   ├── gnetway/      # MTProto gateway
│   │   ├── httpserver/   # HTTP API
│   │   └── session/      # WebSocket session
│   ├── messenger/        # Message routing
│   │   ├── msg/          # Message service
│   │   └── sync/         # Sync service
│   └── service/          # Core services
│       ├── authsession/  # Auth & session
│       ├── biz/          # Business logic
│       ├── dfs/          # File storage
│       ├── geoip/        # Geo location
│       ├── idgen/        # ID generator
│       ├── media/        # Media processing
│       └── status/       # Online status
├── pkg/                  # Shared packages
│   ├── code/             # Error codes
│   ├── conf/             # Configuration
│   ├── net2/             # Network utilities
│   └── ...
├── clients/              # Client SDKs
├── data/                 # SQL schemas
├── docs/                 # Documentation
└── specs/                # Architecture specs
```

## 开发工作流程

### 1. 代码生成

Teamgram 使用 TL（Type Language）作为代码生成工具：

```bash
# Generate Go code from TL schema
make generate
# or
dalgenall.sh
```

### 2. 数据库迁移

```bash
# Initialize database
mysql -u root -p < data/teamgram.sql

# Run migrations
make migrate
```

### 服务开发模式

每个服务都遵循以下开发模式：

```
app/service/<name>/
├── cmd/              # Entry point
├── etc/              # Configuration
├── internal/
│   ├── config/       # Config structures
│   ├── core/         # Business logic
│   ├── dao/          # Data access
│   ├── server/       # gRPC/HTTP handlers
│   └── svc/          # Service context
└── <name>.go         # Main service file
```

### 3. 添加新的 RPC 接口

1. 在 TL 架构中定义新接口（`specs/mtproto.tl`）
2. 生成相应的代码
3. 在 `internal/core` 目录下实现接口逻辑
4. 在 `internal/server` 目录下注册接口
5. 更新客户端 SDK

## 配置

### 服务配置（YAML 格式）

```yaml
# app/service/biz/etc/biz.yaml
Name: biz
Host: 0.0.0.0
Port: 20001

MySQL:
  DataSource: user:password@tcp(localhost:3306)/teamgram?charset=utf8mb4

Redis:
  Host: localhost:6379

Etcd:
  Hosts:
    - localhost:2379
  Key: biz
```

### 环境变量

```bash
# .env file
MYSQL_DATA_SOURCE=user:password@tcp(localhost:3306)/teamgram
REDIS_HOST=localhost:6379
ETCD_ENDPOINTS=localhost:2379
KAFKA_BROKERS=localhost:9092
MINIO_ENDPOINT=localhost:9000
```

## 部署方案

### Docker Compose（开发环境）

```bash
docker-compose up -d
```

### Kubernetes（生产环境）

```yaml
# Example deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: teamgram-biz
spec:
  replicas: 3
  selector:
    matchLabels:
      app: teamgram-biz
  template:
    spec:
      containers:
      - name: biz
        image: teamgram/biz:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
```

## 扩展策略

### 水平扩展

- **无状态服务**：`biz`、`httpserver`、`dfs`（易于扩展）
- **有状态服务**：`gnetway`（基于连接的状态管理）、`session`（会话管理）
- **数据库**：使用 MySQL 的读复制机制、Redis 集群

### 垂直扩展

- **媒体处理服务**：CPU 资源密集型（如 FFmpeg）
- **消息处理服务**：内存资源密集型（如缓存）
- **认证服务**：资源消耗较低

## 安全最佳实践

1. **网络隔离**：
   - 内部服务部署在 VPC 内
   - 只有 `gnetway` 和 `httpserver` 公开访问
2. **加密**：
   - 使用 MTProto 进行端到端加密
   - HTTP/WebSocket 使用 TLS 协议
   - 服务间通信使用 mTLS 协议（可选）
3. **认证**：
   - 认证密钥存储在安全位置
   - 会话令牌设置过期时间
  - 对每个用户/IP 实施速率限制
4. **数据保护**：
   - 数据库在存储时进行加密
   - 使用 MinIO 进行对象存储加密
   - 备份数据也需加密

## 监控

### 监控指标

```
- Request rate per service
- Response latency (p50, p95, p99)
- Error rates
- Active connections
- Message throughput
```

### 日志记录

```go
// Structured logging
log.Info().
    Str("service", "biz").
    Str("method", "messages.sendMessage").
    Int64("user_id", userID).
    Int64("msg_id", msgID).
    Dur("latency", duration).
    Msg("request processed")
```

## 参考资料

- [Teamgram 服务器架构文档](https://deepwiki.com/teamgram/teamgram-server)
- [服务拓扑结构](specs/architecture.md)
- [依赖库列表](specs/dependencies-and-runtime.md)
- [官方仓库](https://github.com/teamgram/teamgram-server)

## 相关文档

- [服务开发指南](references/service-development.md)：服务创建步骤
- [部署指南](references/deployment.md)：生产环境部署方法
- [性能优化指南](references/tuning.md)：性能调优建议