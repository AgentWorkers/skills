---
name: websocket-hub-patterns
model: standard
description: 一种支持水平扩展的WebSocket中心模式，采用懒加载的Redis订阅机制、连接管理机制以及优雅的关闭流程。适用于构建需要跨多个实例进行扩展的实时WebSocket服务器。该模式适用于WebSocket中心、WebSocket扩展、连接管理、Redis与WebSocket的集成、实时数据传输以及水平扩展等场景。
---

# WebSocket 中间件模式

这些模式用于实现基于 Redis 协调的、可水平扩展的 WebSocket 连接。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install websocket-hub-patterns
```


---

## 适用场景

- 实时双向通信
- 聊天应用、协作编辑
- 需要与客户端交互的实时仪表盘
- 需要在多个网关实例之间实现水平扩展的应用

---

## 中间件结构

```go
type Hub struct {
    // Local state
    connections   map[*Connection]bool
    subscriptions map[string]map[*Connection]bool // channel -> connections

    // Channels
    register   chan *Connection
    unregister chan *Connection
    broadcast  chan *Event

    // Redis for scaling
    redisClient  *redis.Client
    redisSubs    map[string]*goredis.PubSub
    redisSubLock sync.Mutex

    // Optional: Distributed registry
    connRegistry *ConnectionRegistry
    instanceID   string

    // Shutdown
    done chan struct{}
    wg   sync.WaitGroup
}
```

---

## 中间件主循环

```go
func (h *Hub) Run() {
    for {
        select {
        case <-h.done:
            return

        case conn := <-h.register:
            h.connections[conn] = true
            if h.connRegistry != nil {
                h.connRegistry.RegisterConnection(ctx, conn.ID(), info)
            }

        case conn := <-h.unregister:
            if _, ok := h.connections[conn]; ok {
                if h.connRegistry != nil {
                    h.connRegistry.UnregisterConnection(ctx, conn.ID())
                }
                h.removeConnection(conn)
            }

        case event := <-h.broadcast:
            h.broadcastToChannel(event)
        }
    }
}
```

---

## 延迟订阅 Redis 数据

仅当第一个本地订阅者加入时，才开始订阅 Redis 数据：

```go
func (h *Hub) subscribeToChannel(conn *Connection, channel string) error {
    // Add to local subscriptions
    if h.subscriptions[channel] == nil {
        h.subscriptions[channel] = make(map[*Connection]bool)
    }
    h.subscriptions[channel][conn] = true

    // Lazy: Only subscribe to Redis on first subscriber
    h.redisSubLock.Lock()
    defer h.redisSubLock.Unlock()

    if _, exists := h.redisSubs[channel]; !exists {
        pubsub := h.redisClient.Subscribe(context.Background(), channel)
        h.redisSubs[channel] = pubsub
        go h.forwardRedisMessages(channel, pubsub)
    }

    return nil
}

func (h *Hub) unsubscribeFromChannel(conn *Connection, channel string) {
    if subs, ok := h.subscriptions[channel]; ok {
        delete(subs, conn)

        // Cleanup when no local subscribers
        if len(subs) == 0 {
            delete(h.subscriptions, channel)
            h.closeRedisSubscription(channel)
        }
    }
}
```

---

## Redis 消息转发

```go
func (h *Hub) forwardRedisMessages(channel string, pubsub *goredis.PubSub) {
    ch := pubsub.Channel()
    for {
        select {
        case <-h.done:
            return
        case msg, ok := <-ch:
            if !ok {
                return
            }
            h.broadcast <- &Event{
                Channel: channel,
                Data:    []byte(msg.Payload),
            }
        }
    }
}

func (h *Hub) broadcastToChannel(event *Event) {
    subs := h.subscriptions[event.Channel]
    for conn := range subs {
        select {
        case conn.send <- event.Data:
            // Sent
        default:
            // Buffer full - close slow client
            h.removeConnection(conn)
        }
    }
}
```

---

## 连接写入泵（Connection Write Pump）

```go
func (c *Connection) writePump() {
    ticker := time.NewTicker(54 * time.Second) // Ping interval
    defer func() {
        ticker.Stop()
        c.conn.Close()
    }()

    for {
        select {
        case message, ok := <-c.send:
            c.conn.SetWriteDeadline(time.Now().Add(10 * time.Second))
            if !ok {
                c.conn.WriteMessage(websocket.CloseMessage, []byte{})
                return
            }
            c.conn.WriteMessage(websocket.TextMessage, message)

            // Batch drain queue
            for i := 0; i < len(c.send); i++ {
                c.conn.WriteMessage(websocket.TextMessage, <-c.send)
            }

        case <-ticker.C:
            if err := c.conn.WriteMessage(websocket.PingMessage, nil); err != nil {
                return
            }
        }
    }
}
```

---

## 用于水平扩展的连接注册表（Connection Registry）

```go
type ConnectionRegistry struct {
    client     *redis.Client
    instanceID string
}

func (r *ConnectionRegistry) RegisterConnection(ctx context.Context, connID string, info ConnectionInfo) error {
    info.InstanceID = r.instanceID
    data, _ := json.Marshal(info)
    return r.client.Set(ctx, "ws:conn:"+connID, data, 2*time.Minute).Err()
}

func (r *ConnectionRegistry) HeartbeatInstance(ctx context.Context, connectionCount int) error {
    info := InstanceInfo{
        InstanceID:  r.instanceID,
        Connections: connectionCount,
    }
    data, _ := json.Marshal(info)
    return r.client.Set(ctx, "ws:instance:"+r.instanceID, data, 30*time.Second).Err()
}
```

---

## 优雅关闭（Graceful Shutdown）

```go
func (h *Hub) Shutdown() {
    close(h.done)

    // Close all Redis subscriptions
    h.redisSubLock.Lock()
    for channel, pubsub := range h.redisSubs {
        pubsub.Close()
        delete(h.redisSubs, channel)
    }
    h.redisSubLock.Unlock()

    // Close all connections
    for conn := range h.connections {
        conn.Close()
    }

    h.wg.Wait()
}
```

---

## 决策树

| 情况 | 对策 |
|-----------|----------|
| 单个实例 | 跳过连接注册表（ConnectionRegistry） |
| 多个实例 | 启用连接注册表（ConnectionRegistry） |
| 通道没有订阅者 | 延迟从 Redis 中取消订阅 |
| 客户端响应缓慢 | 当缓冲区满时关闭连接 |
| 需要消息历史记录 | 使用 Redis Streams 和 Pub/Sub 功能 |

---

## 相关技能

- **元技能：** [ai/skills/meta/realtime-dashboard/](../../meta/realtime-dashboard/) — 完整的实时仪表盘指南
- [dual-stream-architecture](../dual-stream-architecture/) — 事件发布机制
- [resilient-connections](../resilient-connections/) — 连接容错机制

---

## 绝对不要做的事情

- **绝对不要在 `conn.send` 方法中阻塞** — 应使用 `select` 语句并设置默认值来检测缓冲区是否已满
- **绝对不要跳过优雅关闭流程** — 客户端需要接收关闭信号
- **绝对不要在多个通道之间共享 Pub/Sub 订阅** — 每个通道都需要单独的订阅
- **绝对不要忘记发送心跳信号** — 死掉的实例会导致连接处于孤立状态
- **绝对不要在没有发送“ping/pong”信号的情况下发送数据** — 负载均衡器会关闭“空闲”的连接