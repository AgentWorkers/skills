---
name: agent-protocol
description: **代理间通信协议**  
该协议支持技能通过事件进行交互，能够构建工作流程链，并实现无需人工干预的自动化协调。
version: 1.0.0
---

# 代理间通信协议（Agent-to-Agent Protocol）

**这是Clawdbot技能和代理之间基础性的通信层。**  
它使您的代理能够相互交流，构建自动化工作流程，并在没有人工干预的情况下协调复杂的多步骤任务。

## 愿景（Vision）  
```
Research-Agent finds article
    ↓ publishes "research.found"
Summary-Agent subscribes to events
    ↓ generates digest
    ↓ publishes "summary.ready"
Notification-Agent subscribes
    ↓ posts to Telegram/Discord
```

## 架构（Architecture）  

### 1. **事件总线（Event Bus）**（基于文件的消息传递）  
- 代理将事件发布到`~/.clawdbot/events/`  
- 事件是以JSON格式存储的文件，并经过模式验证  
- 数据具有持久性、可调试性且可审计  
- 处理过的事件会自动清理  

### 2. **工作流引擎（Workflow Engine）**  
- 用JSON或YAML定义工作流  
- 根据事件数据进行条件路由  
- 支持错误处理、重试和备用方案  
- 集成Cron定时器以实现定时执行  

### 3. **共享上下文（Shared Context）**  
- 代理可以读写共享内存空间  
- 在工作流步骤之间传递上下文  
- 代理调用之间保持状态的一致性  

### 4. **代理注册表（Agent Registry）**  
- 查找可用的代理/技能  
- 公示代理的能力  
- 管理权限  

## 核心概念（Core Concepts）  

### 事件（Events）  
事件是通信的基本单位：  
```json
{
  "event_id": "evt_20260128_001",
  "event_type": "research.article_found",
  "timestamp": "2026-01-28T23:00:00Z",
  "source_agent": "research-agent",
  "payload": {
    "title": "ETH 2.0 Upgrade Complete",
    "url": "https://example.com/article",
    "importance": 9,
    "summary": "Major Ethereum upgrade..."
  },
  "metadata": {
    "session_id": "main",
    "requires_action": true
  }
}
```

### 工作流（Workflows）  
工作流定义了代理如何响应事件：  
```json
{
  "workflow_id": "research-to-telegram",
  "name": "Research → Summary → Notification",
  "trigger": {
    "event_type": "research.article_found",
    "conditions": {
      "payload.importance": { "gte": 7 }
    }
  },
  "steps": [
    {
      "agent": "summary-agent",
      "action": "summarize",
      "input": "{{payload}}",
      "output_event": "summary.ready"
    },
    {
      "agent": "notification-agent",
      "action": "notify",
      "input": "{{previous.summary}}",
      "channels": ["telegram"]
    }
  ]
}
```

## 快速入门（Quick Start）  

### 1. 安装（Installation）  
```bash
cd /root/clawd/skills/agent-protocol
python3 scripts/setup.py
```

### 2. 启动事件总线（Start the Event Bus）  
```bash
python3 scripts/event_bus.py start
```

### 3. 发布第一个事件（Publish Your First Event）  
```bash
python3 scripts/publish.py \
  --type "test.hello" \
  --source "my-agent" \
  --payload '{"message": "Hello, world!"}'
```

### 4. 订阅事件（Subscribe to Events）  
```bash
python3 scripts/subscribe.py \
  --types "test.hello" \
  --handler "./my_handler.py"
```

### 5. 定义工作流（Define a Workflow）  
```bash
cp examples/simple-workflow.json config/workflows/my-workflow.json
python3 scripts/workflow_engine.py --validate
```

## 事件类型（Event Types）（Conventions）  

### 标准事件类型（Standard Event Types）  
- `research.article_found`：研究代理找到了相关内容  
- `research.topic_suggested`：建议了新的研究主题  
- `summaryready`：生成了摘要  
- `analytics.insight`：个人分析洞察  
- `sportsgoal_scored`：体育赛事进球事件  
- `sports.match_started`：比赛开始  
- `notification_sent`：通知已发送  
- `workflowstarted`：工作流开始执行  
- `workflow_completed`：工作流完成  
- `workflow_FAILED`：工作流失败  

### 事件命名规则（Event Naming Convention）  
`<domain>.<action_past_tense>`  
- 使用小写字母和下划线  
- Domain：广泛的类别（研究、体育、通知）  
- Action：发生的动作（例如：article_found、goal_scored）  

## 工作流示例（Workflow Examples）  

### 示例1：研究 → 通知（Research → Notification）  
```json
{
  "workflow_id": "eth-news-alert",
  "trigger": {
    "event_type": "research.article_found",
    "conditions": {
      "payload.keywords": { "contains": ["ethereum", "ETH"] },
      "payload.importance": { "gte": 8 }
    }
  },
  "steps": [
    {
      "agent": "notification-agent",
      "action": "send_telegram",
      "input": {
        "message": "🚨 Important ETH News!\n{{payload.title}}\n{{payload.url}}"
      }
    }
  ]
}
```

### 示例2：体育进球 → 语音播报（Sports Goal → TTS Announcement）  
```json
{
  "workflow_id": "goal-announcement",
  "trigger": {
    "event_type": "sports.goal_scored",
    "conditions": {
      "payload.team": { "eq": "Barcelona" }
    }
  },
  "steps": [
    {
      "agent": "tts-agent",
      "action": "announce",
      "input": {
        "text": "Goal for Barcelona! {{payload.scorer}} scores! {{payload.score}}"
      }
    }
  ]
}
```

### 示例3：每日分析 → 研究主题（Daily Analytics → Research Topics）  
```json
{
  "workflow_id": "analytics-to-research",
  "trigger": {
    "event_type": "analytics.daily_report",
    "schedule": "0 9 * * *"
  },
  "steps": [
    {
      "agent": "analytics-agent",
      "action": "generate_insights",
      "output_event": "analytics.insights_ready"
    },
    {
      "agent": "research-agent",
      "action": "suggest_topics",
      "input": "{{previous.insights}}",
      "conditions": {
        "previous.insights.count": { "gte": 3 }
      }
    }
  ]
}
```

## 命令（Commands）  

### 事件总线（Event Bus）  
```bash
# Start the event bus daemon
python3 scripts/event_bus.py start

# Check status
python3 scripts/event_bus.py status

# Stop
python3 scripts/event_bus.py stop

# View recent events
python3 scripts/event_bus.py tail --count 20
```

### 发布事件（Publish Events）  
```bash
# Publish event (JSON payload)
python3 scripts/publish.py \
  --type "research.article_found" \
  --source "research-agent" \
  --payload '{"title": "Article", "url": "..."}'

# Publish from file
python3 scripts/publish.py --file event.json

# Publish with priority
python3 scripts/publish.py \
  --type "alert.urgent" \
  --priority high \
  --payload '{"message": "Critical alert!"}'
```

### 订阅事件（Subscribe to Events）  
```bash
# Subscribe to event types
python3 scripts/subscribe.py \
  --types "research.*,sports.goal_scored" \
  --handler "./handlers/my_handler.py"

# Subscribe with filter
python3 scripts/subscribe.py \
  --types "research.*" \
  --filter '{"importance": {"gte": 8}}' \
  --handler "./handlers/important_only.py"

# List active subscriptions
python3 scripts/subscribe.py --list
```

### 工作流管理（Workflow Management）  
```bash
# Validate workflows
python3 scripts/workflow_engine.py --validate

# Run workflow engine (processes workflows)
python3 scripts/workflow_engine.py --run

# Test specific workflow
python3 scripts/workflow_engine.py --test eth-news-alert

# List workflows
python3 scripts/workflow_engine.py --list

# Enable/disable workflow
python3 scripts/workflow_engine.py --enable research-to-telegram
python3 scripts/workflow_engine.py --disable research-to-telegram
```

### 代理注册表（Agent Registry）  
```bash
# Register your agent
python3 scripts/registry.py register \
  --name "my-agent" \
  --capabilities "summarize,notify" \
  --events "research.article_found"

# List available agents
python3 scripts/registry.py list

# Query agents by capability
python3 scripts/registry.py query --capability "summarize"
```

## 与现有技能的集成（Integration with Existing Skills）  

### 体育赛事比分集成（Sports Ticker Integration）  
修改`sports-ticker/scripts/live_monitor.py`以发布事件：  
```python
from agent_protocol import publish_event

# After detecting a goal:
publish_event(
    event_type="sports.goal_scored",
    source="sports-ticker",
    payload={
        "team": team_name,
        "scorer": player_name,
        "opponent": opponent,
        "score": f"{home_score}-{away_score}",
        "minute": clock
    }
)
```

### 研究代理集成（Research Agent Integration）  
```python
from agent_protocol import publish_event

# After finding an article:
publish_event(
    event_type="research.article_found",
    source="research-agent",
    payload={
        "title": article_title,
        "url": article_url,
        "importance": calculate_importance(article),
        "summary": snippet
    }
)
```

### 个人分析集成（Personal Analytics Integration）  
```python
from agent_protocol import publish_event

# Daily insights:
publish_event(
    event_type="analytics.insight",
    source="personal-analytics",
    payload={
        "type": "productivity",
        "insight": "Your focus time increased 20% this week",
        "recommendations": ["Schedule deep work in morning"]
    }
)
```

## 安全性与权限（Security & Permissions）  

### 权限模型（Permission Model）  
```json
{
  "agent": "research-agent",
  "permissions": {
    "publish": ["research.*"],
    "subscribe": ["summary.*", "notification.*"],
    "workflows": ["research-to-telegram"]
  }
}
```

### 沙箱环境（Sandboxing）  
- 代理只能发布到其被指定的事件类型  
- 订阅需要明确的权限  
- 工作流在执行前会进行验证  

## 配置（Configuration）  

### 主配置文件：`config/protocol.json`  
```json
{
  "event_bus": {
    "storage_path": "~/.clawdbot/events",
    "retention_days": 7,
    "max_event_size_kb": 512
  },
  "workflow_engine": {
    "enabled": true,
    "poll_interval_seconds": 30,
    "max_concurrent_workflows": 5
  },
  "registry": {
    "agents_path": "~/.clawdbot/agents/registry.json"
  },
  "security": {
    "require_permissions": true,
    "audit_log": true
  }
}
```

## 高级功能（Advanced Features）  

### 1. 条件路由（Conditional Routing）  
```json
{
  "steps": [
    {
      "condition": {
        "payload.importance": { "gte": 9 }
      },
      "then": { "agent": "urgent-notifier" },
      "else": { "agent": "standard-notifier" }
    }
  ]
}
```

### 2. 并行执行（Parallel Execution）  
```json
{
  "steps": [
    {
      "parallel": [
        { "agent": "telegram-notifier" },
        { "agent": "discord-notifier" },
        { "agent": "email-notifier" }
      ]
    }
  ]
}
```

### 3. 错误处理（Error Handling）  
```json
{
  "steps": [
    {
      "agent": "external-api",
      "retry": {
        "max_attempts": 3,
        "backoff_seconds": 5
      },
      "on_error": {
        "agent": "error-logger",
        "continue": true
      }
    }
  ]
}
```

### 4. 定时工作流（Scheduled Workflows）  
```json
{
  "trigger": {
    "schedule": "0 9 * * *",
    "event_type": "cron.daily_run"
  }
}
```

## 监控与调试（Monitoring & Debugging）  

### 事件日志（Event Log）  
所有事件都会被记录到`~/.clawdbot/events/log/`  
```bash
# View event log
tail -f ~/.clawdbot/events/log/events.log

# Search events
python3 scripts/query.py --type "research.*" --since "1 hour ago"
```

### 工作流执行日志（Workflow Execution Log）  
```bash
# View workflow executions
python3 scripts/workflow_engine.py --history

# Inspect failed workflow
python3 scripts/workflow_engine.py --inspect <workflow_id>
```

### 统计指标（Metrics）  
```bash
# Show event statistics
python3 scripts/metrics.py

# Output:
# Total events published: 1,234
# Event types: 15
# Active subscriptions: 8
# Workflows executed: 456
# Average workflow duration: 2.3s
```

## 最佳实践（Best Practices）  

1. **事件设计（Event Design）**  
   - 保持事件负载简洁且重点明确  
   - 为处理程序提供足够的上下文信息  
   - 使用一致的命名规范  

2. **工作流设计（Workflow Design）**  
   - 保持工作流简单明了  
   - 使用描述性强的名称  
   - 在启用前进行全面测试  

3. **错误处理（Error Handling）**  
   - 始终定义错误处理机制  
   - 记录错误以便调试  
   - 对于暂时性的失败尝试重试  

4. **性能优化（Performance）**  
   - 避免频繁触发事件  
   - 定期清理旧事件  
   - 监控工作流的执行时间  

5. **安全性（Security）**  
   - 验证事件负载  
   - 使用权限管理系统  
   - 审计敏感操作  

## Python API（Python API）  
```python
from agent_protocol import (
    publish_event,
    subscribe,
    create_workflow,
    register_agent
)

# Publish event
publish_event(
    event_type="my.event",
    source="my-agent",
    payload={"key": "value"}
)

# Subscribe to events
@subscribe(["research.*"])
def handle_research(event):
    print(f"Got research event: {event['payload']}")

# Create workflow programmatically
workflow = create_workflow(
    workflow_id="my-workflow",
    trigger={"event_type": "my.trigger"},
    steps=[
        {"agent": "processor", "action": "process"}
    ]
)

# Register agent
register_agent(
    name="my-agent",
    capabilities=["process", "notify"],
    event_types=["my.event"]
)
```

## JavaScript API（JavaScript API）  
```javascript
const { publishEvent, subscribe, createWorkflow } = require('./scripts/protocol.js');

// Publish event
await publishEvent({
  eventType: 'my.event',
  source: 'my-agent',
  payload: { key: 'value' }
});

// Subscribe
subscribe(['research.*'], (event) => {
  console.log('Got event:', event);
});

// Create workflow
await createWorkflow({
  workflowId: 'my-workflow',
  trigger: { eventType: 'my.trigger' },
  steps: [
    { agent: 'processor', action: 'process' }
  ]
});
```

## 路线图（Roadmap）  
- [ ] 可视化工作流构建工具（Web UI）  
- [ ] 支持实时事件的WebSocket  
- [ ] 跨实例事件转发（多机器人网络）  
- [ ] 基于AI的工作流建议  
- [ ] 事件回放和调试工具  
- [ ] 性能分析  
- [ ] 用于查询事件的GraphQL API  

## 贡献（Contributing）  
此技能是Clawdbot核心基础设施的一部分，欢迎贡献代码！  

## 许可证（License）  
MIT  

---

**由Robby使用🦎开发**