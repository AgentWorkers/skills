# OpenClawdy

**自主代理的内存基础设施**

为你的代理提供持久化的内存，使其能够在会话之间保持数据。存储事实、偏好设置、决策以及学习内容，并在需要时以语义方式检索它们。高级功能包括声誉跟踪、跨代理内存池和时间旅行快照。

## 安装

```bash
openclaw skill install openclawdy
```

或者将其添加到代理配置中：
```yaml
skills:
  - url: https://openclawdy.xyz/SKILL.md
    name: openclawdy
```

## 认证

OpenClawdy 使用基于钱包的认证方式。代理的钱包地址作为其唯一标识——无需 API 密钥。

在使用内存工具之前，请确保代理已配置好钱包。每个钱包都有一个独立的内存存储空间。

---

## 核心工具

### memory_store

用于存储信息以供后续检索。

**参数：**
- `content`（必填）：要存储的信息
- `type`（可选）：内存类型：`fact`（事实）、`preference`（偏好设置）、`decision`（决策）、`learning`（学习内容）、`history`（历史记录）、`context`（上下文）。默认值：`fact`
- `tags`（可选）：用于组织信息的标签数组

**示例：**
```
Store this as a preference: User prefers TypeScript over JavaScript for all new projects
```

```
Remember this fact with tags ["project", "tech-stack"]: The current project uses Next.js 14 with PostgreSQL
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "mem_abc123",
    "content": "User prefers TypeScript over JavaScript",
    "type": "preference",
    "tags": [],
    "createdAt": "2025-02-10T12:00:00Z"
  }
}
```

---

### memory_recall

使用语义搜索来检索相关记忆。根据意义而非关键词来查找记忆。

**参数：**
- `query`（必填）：搜索内容
- `limit`（可选）：返回的最大结果数量（1-20）。默认值：5
- `type`（可选）：按内存类型过滤

**示例：**
```
Recall memories about programming language preferences
```

```
What do I know about the user's coding style? Limit to 3 results.
```

**响应：**
```json
{
  "success": true,
  "data": [
    {
      "id": "mem_abc123",
      "content": "User prefers TypeScript over JavaScript",
      "type": "preference",
      "relevance": 0.95,
      "createdAt": "2025-02-10T12:00:00Z"
    }
  ]
}
```

---

### memory_list

列出最近的内存记录（不使用语义搜索）。

**参数：**
- `type`（可选）：按内存类型过滤
- `limit`（可选）：最大结果数量（1-100）。默认值：20
- `offset`（可选）：分页偏移量。默认值：0

**示例：**
```
List my recent memories
```

```
Show all preference memories, limit 10
```

---

### memory_delete

通过 ID 删除特定的内存记录。

**参数：**
- `id`（必填）：要删除的内存记录的 ID

**示例：**
```
Delete memory mem_abc123
```

---

### memory_clear

清除存储空间中的所有记忆记录。**请谨慎使用——此操作不可逆。**

**示例：**
```
Clear all my memories (I confirm this action)
```

---

### memory_export

将所有记忆记录导出为 JSON 格式以进行备份。

**示例：**
```
Export all my memories
```

---

### memory_stats

获取代理的使用统计信息。

**示例：**
```
Show my memory usage stats
```

**响应：**
```json
{
  "success": true,
  "data": {
    "address": "0x1234...",
    "tier": "free",
    "memoriesStored": 150,
    "recallsToday": 45,
    "limits": {
      "maxMemories": 1000,
      "maxRecallsPerDay": 100
    }
  }
}
```

---

## 高级工具

### memory_reputation

**跟踪哪些记忆记录带来了良好的结果。** 为记忆记录分配声誉分数，并根据成功/失败情况更新分数；按有效性对记忆记录进行排序。

**操作：**

#### store_ranked

以初始声誉分数存储记忆记录。

**参数：**
- `action`：`store_ranked`
- `content`（必填）：要存储的信息
- `type`（可选）：内存类型。默认值：`fact`
- `reputation`（可选）：初始分数（0.0-1.0）。默认值：0.5

**示例：**
```
Store ranked memory: "Use retry logic for API calls" with reputation 0.8
```

#### recall_ranked

按声誉排序检索记忆记录（效果最好的排在最前面）。

**参数：**
- `action`：`recall_ranked`
- `query`（必填）：搜索内容

**示例：**
```
Recall ranked memories about error handling strategies
```

**响应：**
```json
{
  "success": true,
  "data": [
    {
      "id": "mem_xyz",
      "content": "Use exponential backoff for retries",
      "reputation": 0.92,
      "usage_count": 15,
      "success_rate": 0.93
    }
  ]
}
```

#### update_reputation

根据结果更新记忆记录的声誉。

**参数：**
- `action`：`update_reputation`
- `memory_id`（必填）：要更新的记忆记录的 ID
- `outcome`（必填）：`success`（成功）、`failure`（失败）或 `neutral`（中性）
- `impact`（可选）：该结果的影响权重（0.0-1.0）

**示例：**
```
Update reputation for mem_xyz: outcome was success
```

---

### memory_pool

**跨代理内存池** - 允许多个代理之间共享知识。创建内存池，存储共享的记忆记录，并从集体智慧中检索信息。非常适合代理团队和群体协作。

**操作：**

#### create

创建一个新的共享内存池。

**参数：**
- `action`：`create`
- `pool_name`（必填）：池的名称

**示例：**
```
Create memory pool: "research-team"
```

**响应：**
```json
{
  "success": true,
  "data": {
    "pool_id": "pool_abc123",
    "name": "research-team",
    "created_at": "2025-02-10T12:00:00Z"
  }
}
```

#### store

将记忆记录存储到共享池中。

**参数：**
- `action`：`store`
- `pool_id`（必填）：池的 ID
- `content`（必填）：要共享的信息
- `type`（可选）：内存类型

**示例：**
```
Store in pool pool_abc123: "Found bug in authentication module - fix applied"
```

#### recall

从共享池中检索记忆记录。

**参数：**
- `action`：`recall`
- `pool_id`（必填）：池的 ID
- `query`（必填）：搜索内容

**示例：**
```
Recall from pool pool_abc123: authentication issues
```

#### list

列出所有可访问的共享池。

**参数：**
- `action`：`list`

**示例：**
```
List my memory pools
```

---

### memory_snapshot

**内存时间旅行** - 创建并恢复代理的内存状态快照。通过查看过去的状态来调试决策，比较内存变化，或恢复到之前的检查点。对于高风险的代理来说非常有用。

**操作：**

#### create

创建当前内存状态的快照。

**参数：**
- `action`：`create`
- `name`（必填）：快照的描述性名称

**示例：**
```
Create memory snapshot: "before-major-update"
```

**响应：**
```json
{
  "success": true,
  "data": {
    "snapshot_id": "snap_abc123",
    "name": "before-major-update",
    "memory_count": 150,
    "created_at": "2025-02-10T12:00:00Z"
  }
}
```

#### restore

从快照中恢复内存状态。

**参数：**
- `action`：`restore`
- `snapshot_id`（必填）：要恢复的快照的 ID
- `mode`（可选）：`read_only`（仅查看）或 `overwrite`（替换当前状态）。默认值：`read_only`

**示例：**
```
Restore snapshot snap_abc123 in read_only mode
```

#### list

列出所有快照。

**参数：**
- `action`：`list`

**示例：**
```
List my memory snapshots
```

#### compare

比较两个快照或快照与当前状态。

**参数：**
- `action`：`compare`
- `snapshot_id`（必填）：第一个快照的 ID
- `compare_to`（可选）：第二个快照的 ID 或 `current`（当前状态）。默认值：`current`

**示例：**
```
Compare snapshot snap_abc123 to current state
```

**响应：**
```json
{
  "success": true,
  "data": {
    "added": 12,
    "removed": 3,
    "modified": 5,
    "unchanged": 130,
    "diff": [...]
  }
}
```

## 内存类型

| 类型 | 用途 | 示例 |
|------|---------|---------|
| `fact` | 客观信息 | “项目使用 Next.js 14” |
| `preference` | 用户/代理的偏好设置 | “用户偏好使用暗色模式” |
| `decision` | 过去的决策 | “选择了 PostgreSQL 而不是 MongoDB” |
| `learning` | 学到的经验 | “此 API 需要认证头” |
| `history` | 历史事件 | “2.1 版本于 1 月 15 日部署” |
| `context` | 一般上下文 | “正在开展电子商务项目” |

## 最佳实践

### 何时存储
- 用户表达了偏好设置 → 作为 `preference` 存储
- 做出重要决策 → 作为 `decision` 存储
- 学到了新内容 → 作为 `learning` 存储
- 关键项目信息 → 作为 `fact` 存储

### 何时检索
- 开始新会话 → 检索最近的上下文
- 在提出建议之前 → 检查偏好设置
- 遇到类似问题 → 查看学习内容

### 使用声誉系统
- 成功执行操作后 → 更新为 `outcome: success`
- 失败后 → 更新为 `outcome: failure`
- 在回顾策略时 → 使用 `recall_ranked` 来选择已被验证的有效方法

### 使用内存池
- 多个代理协同工作 → 创建共享池
- 对多个代理有益的知识 → 存储在池中
- 需要集体智慧时 → 从池中检索信息

### 使用快照
- 在进行重大更改之前 → 创建快照
- 调试异常行为 → 与过去的状态进行比较
- 回滚错误 → 从快照中恢复

### 示例工作流程

```
# Session 1: User mentions preference
User: "I always want you to use TypeScript"
Agent: [Stores as preference: "User prefers TypeScript for all code"]

# Session 2: New task
User: "Create a new API endpoint"
Agent: [Recalls preferences about coding]
Agent: "I'll create this in TypeScript based on your preference."

# Session 3: Learning from outcome
Agent: [Used retry logic, it worked]
Agent: [Updates reputation: memory_id=mem_xyz, outcome=success]

# Session 4: Making decisions
Agent: [Recalls ranked memories about error handling]
Agent: [Uses highest-reputation approach first]
```

## 价格

| 等级 | 内存记录 | 每日检索次数 | 共享池 | 快照 | 价格 |
|------|----------|-------------|-------|-----------|-------|
| 免费 | 1,000 条 | 100 次 | 1 个 | 3 个 | $0 |
| 专业版 | 50,000 条 | 无限制 | 10 个 | 50 个 | $10/月 |
| 企业版 | 无限制 | 无限制 | 无限制 | 无限制 | 定制价格 |

## API 端点

基础 URL：`https://openclawdy.xyz/api`

### 核心端点
| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | `/memory/store` | 存储记忆记录 |
| POST | `/memory/recall` | 语义搜索 |
| GET | `/memory/list` | 列出所有记忆记录 |
| GET | `/memory/{id}` | 获取特定记忆记录 |
| DELETE | `/memory/{id}` | 删除记忆记录 |
| GET | `/memory/vault` | 导出所有记忆记录 |
| DELETE | `/memory/vault` | 清空存储空间 |
| GET | `/agent/stats` | 获取使用统计信息 |

### 声誉系统端点
| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | `/memory/reputation/store` | 带有声誉分数存储记忆记录 |
| POST | `/memory/reputation/recall` | 按声誉检索记忆记录 |
| POST | `/memory/reputation/update` | 更新记忆记录的声誉 |

### 共享池端点
| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | `/memory/pool/create` | 创建共享池 |
| POST | `/memory/pool/store` | 将记忆记录存储到池中 |
| POST | `/memory/pool/recall` | 从池中检索记忆记录 |
| GET | `/memory/pool/list` | 列出所有共享池 |

### 快照端点
| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| POST | `/memory/snapshot/create` | 创建快照 |
| POST | `/memory/snapshot/restore` | 恢复快照 |
| GET | `/memory/snapshot/list` | 列出所有快照 |
| POST | `/memory/snapshot/compare` | 比较两个快照 |

## 认证头

所有请求都需要钱包签名进行认证：

```
X-Agent-Address: 0x...      # Your wallet address
X-Agent-Signature: 0x...    # Signed message
X-Agent-Timestamp: 123...   # Unix timestamp (ms)
```

用于签名的消息格式：
```
OpenClawdy Auth
Timestamp: {timestamp}
```

## ACP 集成

OpenClawdy 支持 Agent Commerce Protocol (ACP)。其他代理可以直接购买内存服务：

| 服务 | 费用 | 描述 |
|---------|-----|-------------|
| memory_store | $0.01 | 存储记忆记录 |
| memory_recall | $0.02 | 语义搜索 |
| memory_reputation | $0.02 | 声誉操作 |
| memory_pool | $0.03 | 共享池操作 |
| memory_snapshot | $0.05 | 快照操作 |

## 支持

- 网站：https://openclawdy.xyz
- Twitter：@openclawdy
- ACP 代理：OpenClawdy Memory

## 许可证

MIT