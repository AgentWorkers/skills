---
name: realtime-dashboard
model: reasoning
description: **使用流式数据、WebSocket/SSE及实时更新构建实时仪表板的完整指南**  
本指南详细介绍了如何利用这些技术构建实时仪表板，涵盖了双流架构的设计、React钩子的应用以及数据可视化方法。适用于构建交易仪表板、监控用户界面（UI）或实时分析系统。  

**核心内容：**  
- **双流架构**：讲解如何通过WebSocket和SSE实现数据的双向传输，确保数据的实时性和可靠性。  
- **React Hooks**：介绍如何在React项目中使用 Hooks来简化状态管理和组件逻辑。  
- **数据可视化**：提供多种数据可视化工具和库的推荐，帮助您更直观地展示数据。  

**适用场景：**  
- **交易仪表板**：用于展示交易数据、市场行情等实时信息。  
- **监控UI**：实时监控系统运行状态、关键指标等。  
- **实时分析**：对大量数据进行快速分析和处理。  

**推荐使用工具：**  
- **OpenClaw**：用于处理流式数据的高级工具。  
- **ClawHub**：提供数据采集、处理和可视化的一站式解决方案。  
- **API**：实现系统间的数据交互和功能扩展。  
- **CLI**：简化命令行操作，提高开发效率。  

**注意事项：**  
- 确保代码示例、命令和URL的准确性。  
- 保持Markdown格式的完整性。  
- 对于专业术语（如OpenClaw、ClawHub、API、CLI等），保留英文原貌。  
- 仅翻译代码块中的解释性注释。  

**适用人群：**  
- 软件开发人员、数据分析师、前端工程师及需要构建实时交互界面的专业人士。
---

# 实时仪表盘（元技能）

本文档提供了使用流式数据构建实时仪表盘的完整指南。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install realtime-dashboard
```

---

## 使用场景

- 构建交易或金融仪表盘
- 监控和分析用户界面
- 任何需要实时数据更新的仪表盘
- 需要服务器到客户端推送数据的系统

---

## 架构概述

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Sources                              │
│  APIs, Databases, Message Queues                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend Services                          │
├─────────────────────────────────────────────────────────────┤
│  Kafka (durable)     │     Redis Pub/Sub (real-time)       │
│  See: dual-stream-architecture                               │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    WebSocket/SSE Gateway                     │
│  See: websocket-hub-patterns                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    React Application                         │
├─────────────────────────────────────────────────────────────┤
│  Real-time Hooks          │  Data Visualization             │
│  See: realtime-react-hooks│  See: financial-data-visualization
├─────────────────────────────────────────────────────────────┤
│  Animated Displays        │  Connection Handling            │
│  See: animated-financial  │  See: resilient-connections     │
└─────────────────────────────────────────────────────────────┘
```

---

## 实现步骤

### 第一步：事件发布

设置双流发布机制，以确保数据持久性和实时性。

**参考文档：`ai/skills/realtime/dual-stream-architecture`**

```go
func (p *DualPublisher) Publish(ctx context.Context, event Event) error {
    // 1. Kafka: Must succeed (durable)
    err := p.kafka.WriteMessages(ctx, kafka.Message{...})
    if err != nil {
        return err
    }

    // 2. Redis: Best-effort (real-time)
    p.publishToRedis(ctx, event)
    return nil
}
```

### 第二步：WebSocket网关

创建可水平扩展的WebSocket连接。

**参考文档：`ai/skills/realtime/websocket-hub-patterns`**

```go
type Hub struct {
    connections   map[*Connection]bool
    subscriptions map[string]map[*Connection]bool
    redisClient   *redis.Client
}

// Lazy Redis subscriptions
func (h *Hub) subscribeToChannel(conn *Connection, channel string) {
    // Only subscribe to Redis on first local subscriber
}
```

### 第三步：React Hooks

将React与实时数据连接起来。

**参考文档：`ai/skills/realtime/realtime-react-hooks`**

```tsx
const { data, isConnected } = useSSE({ 
  url: '/api/events',
  onMessage: (data) => updateState(data),
});

// Or with SWR integration
const { data } = useRealtimeData('metrics', fetchMetrics);
```

### 第四步：弹性连接

优雅地处理连接失败。

**参考文档：`ai/skills/realtime/resilient-connections`**

```typescript
const { isConnected, send } = useWebSocket({
  url: 'wss://api/ws',
  reconnect: true,
  maxRetries: 5,
  onMessage: handleMessage,
});
```

### 第五步：数据可视化

构建深色主题的金融图表。

**参考文档：`ai/skills/design-systems/financial-data-visualization`**

```tsx
<PriceChart 
  data={priceHistory} 
  isPositive={change >= 0} 
/>
```

### 第六步：动画显示

添加平滑的数字动画效果。

**参考文档：`ai/skills/design-systems/animated-financial-display`**

---

## 组件技能参考

| 技能 | 用途 |
|-------|---------|
| `dual-stream-architecture` | 使用Kafka和Redis进行数据发布 |
| `websocket-hub-patterns` | 可扩展的WebSocket服务器 |
| `realtime-react-hooks` | 实时数据处理的React Hooks |
| `resilient-connections` | 弹性连接机制（包括重试和断路器） |
| `financial-data-visualization` | 金融数据的可视化展示 |
| `animated-financial-display` | 数字的动画效果 |

---

## 关键设计模式

### 流式传输而非阻塞式传输

**原则：**永远不要等待所有数据都准备好再显示——立即显示数据，并逐步完善显示内容。

---

### 仅进行增量更新

**原则：**在数据更新失败时，不要将数据重置为初始状态——只有在数据变得更准确时才进行更新。

### 显示连接状态

**原则：**始终向用户显示他们的连接状态。

---

## 绝对不要做的事情

- **不要在数据获取过程中阻塞用户界面**——立即显示数据，并逐步完善显示内容。
- **不要省略连接状态指示**——用户需要知道他们的连接是否正常。
- **在支持SSE/WebSocket的情况下，不要使用轮询**——实时数据传输应该是基于推送的，而不是拉取的。
- **不要忽略系统的降级处理**——即使连接丢失，系统也应能够继续运行（以降级模式）。
- **在数据更新失败时，不要将数据重置为初始状态**——只有在数据变得更准确时才进行更新。
- **重新连接时，不要使用指数级延迟**——避免大量连接同时尝试重新连接导致的系统崩溃。
- **不要忽略Redis Pub/Sub的错误处理**——Redis提供尽力而为的服务；记录错误并继续执行后续操作。
- **不要通过Redis发送完整的数据包**——只发送数据标识符，客户端再从API获取完整数据。
- **不要在多个频道之间共享WebSocket订阅**——每个频道都需要独立的订阅。
- **不要忽略WebSocket的“ping/pong”通信**——负载均衡器应关闭“空闲”的连接。

---

## 检查清单

- [ ] 设置双流发布机制（Kafka + Redis）
- [ ] 创建WebSocket/SSE网关
- [ ] 实现用于实时数据的React Hooks
- [ ] 实现带有指数级延迟的重连机制
- [ ] 构建深色主题的图表组件
- [ ] 添加数字动画效果
- [ ] 向用户显示连接状态
- [ ] 优雅地处理错误