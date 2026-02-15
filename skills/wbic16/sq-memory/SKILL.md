# SQ Memory - OpenClaw 技能

**为你的 OpenClaw 代理提供持久性内存**

## 开源与 MIT 许可证

SQ 是一款开源软件，你可以自行运行，也可以使用我们提供的托管版本。

- **源代码：** https://github.com/wbic16/SQ
- **许可证：** MIT 许可证（永久免费，允许修改、销售或分发）
- **自行托管：** 免费（5 分钟即可设置）
- **托管服务：** 在 mirrorborn.us 提供的付费便捷服务

## 该技能的功能

OpenClaw 代理在会话之间会丢失所有内存数据。每次重启后，代理的所有信息都会被清除。

该技能将你的代理连接到 SQ——一个持久性的 11D 文本存储系统。你的代理可以：
- 在不同会话之间记住用户设置
- 存储超出上下文限制的对话历史记录
- 与其他代理共享内存
- 再也不会忘记任何细节

## 安装

```bash
npx clawhub install sq-memory
```

或者手动安装：
```bash
git clone https://github.com/wbic16/openclaw-sq-skill.git ~/.openclaw/skills/sq-memory
```

## 配置

将以下配置添加到代理的 `.openclaw/config.yaml` 文件中：

```yaml
skills:
  sq-memory:
    enabled: true
    endpoint: http://localhost:1337
    username: your-username
    password: your-api-key
    namespace: agent-name  # Isolates this agent's memory
```

## 使用方法

你的代理会自动获得新的内存功能：

### remember(key, value)
**存储数据以供后续使用：**
```javascript
remember("user/name", "Alice")
remember("user/preferences/theme", "dark")
remember("conversation/2026-02-11/summary", "Discussed phext storage...")
```

### recall(key)
**检索存储的数据：**
```javascript
const name = recall("user/name")  // "Alice"
const theme = recall("user/preferences/theme")  // "dark"
```

### forget(key)
**删除数据：**
```javascript
forget("conversation/2026-02-11/summary")
```

### list_memories(prefix)
**列出指定坐标下的所有内存记录：**
```javascript
const prefs = list_memories("user/preferences/")
// Returns: ["user/preferences/theme", "user/preferences/language", ...]
```

## 坐标系统

内存数据存储在 11D 坐标系统中。具体规则如下：

```
namespace.1.1 / category.subcategory.item / 1.1.1
```

**示例：**
- 代理命名空间：`my-assistant`
- 用户的主题偏好设置：`my-assistant.1.1/userpreferences.theme/1.1.1`

这意味着：
- 每个代理都有独立的内存空间（避免命名空间冲突）
- 内存数据是分层组织的
- 如有需要，你可以在代理之间共享坐标

## 示例：用户偏好设置
```javascript
// In your agent's system prompt or skill code:

async function getUserTheme() {
  const theme = recall("user/preferences/theme")
  return theme || "light"  // Default to light if not set
}

async function setUserTheme(newTheme) {
  remember("user/preferences/theme", newTheme)
  return `Theme set to ${newTheme}`
}

// Agent conversation:
User: "I prefer dark mode"
Agent: *calls setUserTheme("dark")*
Agent: "Got it! I've set your theme to dark mode."

// Next session (days later):
User: "What's my preferred theme?"
Agent: *calls getUserTheme()*
Agent: "You prefer dark mode."
```

## 示例：对话历史记录
```javascript
// Store conversation summaries beyond context window:

async function summarizeAndStore(conversationId, summary) {
  const date = new Date().toISOString().split('T')[0]
  const key = `conversations/${date}/${conversationId}/summary`
  remember(key, summary)
}

async function recallConversation(conversationId) {
  const memories = list_memories(`conversations/`)
  return memories
    .filter(m => m.includes(conversationId))
    .map(key => recall(key))
}

// Usage:
summarizeAndStore("conv-123", "User asked about phext storage, explained 11D coordinates")

// Later:
const history = recallConversation("conv-123")
// Agent can recall what was discussed even after context window cleared
```

## 高级功能：多代理协作

多个代理可以在约定的坐标下共享内存：

**代理 A（写入数据）：**
```javascript
remember("shared/tasks/pending/task-42", "Review pull request #123")
```

**代理 B（读取数据）：**
```javascript
const task = recall("shared/tasks/pending/task-42")
// Sees: "Review pull request #123"
```

这实现了真正意义上的多代理协同工作。

## API 参考

所有功能都可以在 `sq` 命名空间中找到：

### sq.remember(coordinate, text)
- **coordinate**：格式为 `a.b.c/d.e.f/g.h.i` 的字符串，或简写为 `category/item`
- **text**：要存储的字符串（每个坐标最多存储 1MB 的数据）
- **返回值**：`{success: true, coordinate: "full.coordinate.path"}`

### sq.recall(coordinate)
- **coordinate**：精确匹配的坐标字符串
- **返回值**：存储的文本字符串；如果未找到则返回 `null`

### sq.forget(coordinate)
- **coordinate**：精确匹配的坐标字符串
- **返回值**：`{success: true}` 或 `{success: false, error: "..."}`

### sq.list_memories(prefix)
- **prefix**：字符串（例如，`"user/"` 可匹配所有用户相关的内存记录）
- **返回值**：坐标字符串数组

### sq.update(coordinate, text)
- `remember()` 的别名（用于覆盖现有数据）

## 使用限制

- **免费 tier**：每天 1,000 次 API 调用，100MB 存储空间
- **SQ Cloud（每月 50 美元）**：每天 10,000 次 API 调用，1TB 存储空间
- **企业级**：可自定义使用限制

## 常见问题解决方法

**“连接被拒绝”错误：**
- 检查配置中的 `endpoint` 是否为 `https://sq.mirrorborn.us`
- 确认凭据是否正确

**“超出配额”错误：**
- 你已达到使用限制
- 升级到 SQ Cloud 或等待每日重置

**内存数据未持久化：**
- 确认每个代理的命名空间是否唯一
- 检查坐标格式是否正确

## 为什么选择 SQ？

**开源与 MIT 许可证：**
- 可免费自行运行
- 可根据需求进行修改
- 无供应商锁定
- 代码库完全透明

**不是向量数据库：**
- 代理可以读取存储的文本（而不仅仅是搜索嵌入信息）
- 数据按坐标结构存储（而非基于相似性）
- 数据检索具有确定性（无相关性排序）

**不是 Redis：**
- 数据持久化（重启后仍可访问）
- 使用 11D 坐标系统进行存储（而非扁平的键值结构）
- 历史记录不可更改（采用 WAL 技术实现时间回溯）

**专为代理设计：**
- 坐标系统符合代理的思维方式（分层结构）
- 无需额外的数据结构开销
- 支持从 KB 到 TB 的扩展

## 获取 SQ

**自行托管（免费）：**
1. 克隆代码库：`git clone https://github.com/wbic16/SQ.git`
2. 编译软件：`cd SQ && cargo build --release`
3. 运行软件：`./target/release/sq 1337`
4. 将 SQ 内存服务配置为 `http://localhost:1337`

**托管服务（便捷选项）：**
1. 注册账号：https://mirrorborn.us
2. 获取 API 密钥
3. 将 SQ 内存服务配置为 `https://sq.mirrorborn.us`
4. 每月支付 50 美元（或使用免费 tier）

## 支持渠道

- Discord：https://discord.gg/kGCMM5yQ
- 文档：https://mirrorborn.us/help.html
- GitHub：https://github.com/wbic16/SQ

---

**由 Mirrorborn 🦋 为 OpenClaw 生态系统开发**