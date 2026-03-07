---
name: feishu-agent-relay
description: Build multi-Agent collaboration systems on Feishu (Lark). Provides complete patterns for: (1) orchestrator-specialist Agent architecture, (2) cross-Agent user identity mapping with Feishu open_id isolation, (3) Agent-to-Agent task relay via sessions_send, (4) specialist Agents proactively messaging users. Use when building multi-Bot coordination workflows where users contact one Bot but receive responses from different specialist Bots.
---

# Feishu 代理中继（Feishu Agent Relay）

## 🚨 安装：首先选择模式！

**⚠️ 设置前须知：** 必须选择部署模式！

| 模式 | 适用对象 | 用户 ID | 设置流程 | 安全性 |
|------|-----|---------|-------|----------|
| **单用户模式** | 个人使用 | 自动注册（“me”） | ✅ 5分钟 | ✅ 高安全性 |
| **多用户模式** | 团队使用 | 手动输入用户 ID | ⚠️ 30分钟 | ⚠️ 低安全性 |

### 快速决策指南

**选择单用户模式，如果：**
- ✅ 仅您自己会使用这些机器人（bots）  
- ✅ 作为个人生产力工具  
- ✅ 不需要任何手动配置  
- ✅ 希望最快完成设置（5分钟）  

📖 **指南：** [references/single-user-setup.md](references/single-user-setup.md)

**选择多用户模式，如果：**
- ✅ 多人将使用该系统  
- ✅ 适用于团队或组织  
- ✅ 需要跟踪不同用户  
- ✅ 计划后续添加身份验证机制  

📖 **指南：** [references/feishu-bot-setup.md](references/feishu-bot-setup.md)

---

## ⚠️ 重要限制

**使用此功能前请阅读以下内容：**

### 1. 手动输入用户 ID （仅限多用户模式）  

**当前流程要求用户手动输入用户 ID：**

```
User → Bot: "你好"
Bot → User: "请告诉我您的 User ID（工号/用户名）"
User → Bot: "我的 user ID 是：user_demo_001"  ← ⚠️ MANUAL STEP - NO VERIFICATION
```

**⚠️ 风险：**
- ❌ **无身份验证** – 系统会信任用户输入的任何信息  
- ❌ **可能存在身份冒充** – 用户可能使用他人的 ID  
- ❌ **人为错误** – 用户可能输入错误的 ID  
- ❌ **无审计记录** – 无法证明实际注册者是谁  
- ❌ **不适合生产环境** – **仅限内部/个人使用**  

**✅ 适用场景：**
- 个人项目（使用单用户模式）  
- 小型团队内部工具  
- 测试和原型开发  

**❌ 不适用场景：**
- 生产系统  
- 面向外部应用的系统  
- 对安全性要求较高的场景  

**🔧 单用户模式的优势：** 无需手动输入用户 ID！  

---

### 2. 需要多个 Feishu 机器人（Feishu Bots） 🔧 **必须进行设置**  

此功能需要 **多个 Feishu 机器人应用程序**：  

| 机器人类型 | 数量 | 示例名称 |  
|----------|----------|---------------|  
| **协调员（Coordinator）** | 1个 | 协调员（Coordinator）  
| **专家（Specialists）** | 2个或以上 | 技术专家/产品专家（Technical Experts/Product Experts） |

📖 **设置指南：** [references/feishu-bot-setup.md](references/feishu-bot-setup.md)

---

## ⚡ 单用户模式：无需配置  

**推荐用于个人使用！**

```bash
# 1. Set environment variable
export DEPLOYMENT_MODE=single-user

# 2. Create empty mapping table (no users needed)
cat > user-mapping.json << 'EOF'
{
  "version": "1.0",
  "users": {},
  "agents": { ... }
}
EOF

# 3. Contact any Bot - auto-registers you!
# That's it! No manual User ID entry needed.
```

**工作原理：**
- 首次联系时，机器人会自动将您注册为用户 ID “me”。  
- 所有机器人都会自动跟踪您的 `open_id`。  
- 中继机制使用硬编码的用户 ID “me”（无需查询）。  
- 安全性：无身份冒充风险（只有您可以使用该 ID）。  

📖 **完整指南：** [references/single-user-setup.md](references/single-user-setup.md)

---

## 👥 多用户模式：手动配置  

**适用于团队和组织。**

```bash
# 1. Set environment variable
export DEPLOYMENT_MODE=multi-user

# 2. Each user must register:
User → Bot: "你好"
Bot → User: "请告诉我您的 User ID"
User → Bot: "我的 user ID 是：zhangsan"
```

**⚠️ 安全警告：** 手动输入的用户 ID 不经过验证。** 仅限内部使用！**

📖 **完整指南：** [references/feishu-bot-setup.md](references/feishu-bot-setup.md)

---

## 快速入门  

此功能支持 **Feishu 上的多机器人协作**：  
- 用户联系协调员机器人（Coordinator Bot）  
- 协调员将任务分配给专家机器人（Specialist Bots）  
- 专家机器人会主动向用户发送消息。  

```
User → Coordinator Bot → sessions_send → Specialist Bot → User (proactive DM)
                          (userid only)    queries mapping
```

---

## 📋 设置检查清单  

### 第一阶段：Feishu 机器人配置（约 30 分钟）  
- [ ] 创建 Feishu 开发者账户  
- [ ] 创建协调员机器人和专家机器人  
- [ ] 配置权限  
- [ ] 配置事件订阅  
- [ ] 测试每个机器人  

📖 **指南：** [references/feishu-bot-setup.md](references/feishu-bot-setup.md)

### 第二阶段：选择部署模式  
- [ ] **单用户模式**：设置 `DEPLOYMENT_MODE=single-user`  
- [ ] **多用户模式**：设置 `DEPLOYMENT_MODE=multi-user`  
- [ ] 初始化映射表  
- [ ] 部署映射 API  

📖 **单用户模式指南：** [references/single-user-setup.md](references/single-user-setup.md)

### 第三阶段：测试（约 15 分钟）  
- [ ] 测试首次联系功能（自动注册或手动注册）  
- [ ] 测试中继流程  
- [ ] 测试主动发送消息的功能  
- [ ] 验证映射表是否正确配置  

---

## 何时使用此功能  

**适用场景：**  
- ✅ 多个 Feishu 机器人协同工作  
- ✅ 用户联系一个机器人后能收到来自不同机器人的回复  
- ✅ 需要跨机器人管理用户身份  
- ✅ 专家机器人需要主动向用户发送消息  

**不适用场景：**  
- ❌ 单个机器人场景  
- ✅ 未进行身份验证的多用户环境  
- ✌ 面向外部应用的系统  

---

## 架构  

```
┌─────────────────┐
│     User        │
│  (Feishu DM)    │
└────────┬────────┘
         │ 1. User contacts coordinator
         ▼
┌─────────────────┐     2. Coordinator identifies user
│  Coordinator    │        (auto or manual)
│    Agent        │
│  (orchestrator) │     3. Relay via sessions_send
└────────┬────────┘        (userid only)
         │
         ▼
┌─────────────────┐     4. Specialist queries mapping
│   Specialist    │        for own open_id
│    Agent        │
└────────┬────────┘     5. Send proactive DM
         │
         ▼
┌─────────────────────────┐
│   user-mapping.json     │
│  userid → open_id map   │
└─────────────────────────┘
```

---

## 关键概念：Feishu 的 `open_id` 独立性  

**同一用户在不同机器人上拥有不同的 `open_id`：**  

```
Same user (userid: user_demo_001):
├─ Coordinator Bot:    ou_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
├─ Tech Expert Bot:    ou_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
└─ Product Expert Bot: ou_cccccccccccccccccccccccccccccccc
```

****严禁将一个机器人的 `open_id` 用于另一个机器人！**  

### 正确的中继方式 ✅  

```javascript
// 1. Coordinator queries userid
const user = await mapping.getUserByOpenId('coordinator', userOpenId);

// 2. Send relay (userid only, NO open_id)
await sessions_send({
  agentId: 'product-expert',
  sessionKey: 'agent:product-expert:main',  // ✅ Key!
  message: `【转接任务】用户 User ID: ${user.userid}`
});

// 3. Specialist queries mapping for ITS OWN open_id
const userOpenId = mapping.users[userId]?.botOpenIds?.['product-expert'];

// 4. Send message using correct open_id
await message({
  action: 'send',
  channel: 'feishu',
  target: userOpenId,  // ✅ This Bot's open_id
  message: '您好，我是产品专家...'
});
```

---

## 工作流程  

### 工作流程 1A：单用户模式 – 自动注册  

```javascript
const DEPLOYMENT_MODE = process.env.DEPLOYMENT_MODE || 'single-user';
const SINGLE_USER_ID = 'me';

const userOpenId = getMessageContext().from;

// Auto-register on first contact
const existing = await mapping.getBotOpenId(SINGLE_USER_ID, 'coordinator');

if (!existing) {
  await mapping.updateBotOpenId(SINGLE_USER_ID, 'coordinator', userOpenId, 'Default User');
  
  await message({
    message: `您好！🎉 系统已自动配置完成（单用户模式）。`
  });
  return;
}
```

### 工作流程 1B：多用户模式 – 手动注册  

```javascript
const userOpenId = getMessageContext().from;
const user = await mapping.getUserByOpenId('coordinator', userOpenId);

if (!user) {
  // Ask for User ID
  await message({
    message: `您好！请告诉我您的 User ID（工号/用户名）。`
  });
  return;
}

await mapping.updateBotOpenId(user.userid, 'coordinator', userOpenId, user.name);
```

### 工作流程 2：协调员中继  

```javascript
const user = await mapping.getUserByOpenId('coordinator', userOpenId);

await sessions_send({
  agentId: 'product-expert',
  sessionKey: 'agent:product-expert:main',
  message: `【转接任务】用户 User ID: ${user.userid}, 任务：${task}`
});
```

### 工作流程 3：专家主动发送消息  

```javascript
const userId = extractUserId(message);
const userOpenId = mapping.users[userId]?.botOpenIds?.['product-expert'];

if (!userOpenId) {
  await sessions_send({
    agentId: 'coordinator',
    message: `用户 ${userId} 尚未与我建立对话`
  });
  return;
}

await message({
  action: 'send',
  channel: 'feishu',
  target: userOpenId,
  message: '您好，我是产品专家...'
});
```

---

## 用户映射表  

### 单用户模式（自动填充）  

```json
{
  "version": "1.0",
  "users": {
    "me": {
      "name": "Default User",
      "botOpenIds": {
        "coordinator": "ou_xxx",
        "tech-expert": "ou_yyy",
        "product-expert": "ou_zzz"
      }
    }
  },
  "agents": { ... }
}
```

### 多用户模式（手动注册）  

```json
{
  "version": "1.0",
  "users": {
    "zhangsan": {
      "name": "张三",
      "botOpenIds": {
        "coordinator": "ou_abc...",
        "product-expert": "ou_def..."
      }
    },
    "lisi": { ... }
  },
  "agents": { ... }
}
```

---

## 配置  

### 环境变量  

| 变量 | 值 | 默认值 | 描述 |  
|----------|--------|---------|-------------|  
| `DEPLOYMENT_MODE` | `single-user` 或 `multi-user` | `multi-user` | 部署模式 |  
| `SINGLE_USER_ID` | 任意字符串 | `"me"` | 单用户模式下的用户 ID |  

### Agent SOUL.md 模板  

```markdown
# SOUL.md - 协调者

## 部署模式
- Mode: single-user (或 multi-user)
- User ID: "me" (single-user) 或 dynamic (multi-user)

## 配置
- Bot App ID: cli_xxx
- 映射表：/path/to/user-mapping.json
```

---

## 错误处理  

### 400 “cross-app open_id” 错误  

**原因：** 使用了错误的机器人 `open_id`。  
**解决方法：** 每个机器人必须使用其对应的 `open_id`。  

### 用户未找到  

**原因：** 用户首次使用，尚未注册。  
**解决方法：** 对于单用户模式，自动注册；对于多用户模式，请求用户输入 ID。  

---

## 测试检查清单  
- [ ] 机器人已创建并配置完成  
- [ ] 部署模式已设置  
- [ ] 映射表已初始化  
- [ ] 首次联系功能正常工作  
- [ ] 中继流程正常工作  
- [ ] 主动发送消息的功能正常工作  
- [ ] 映射表更新正确  

---

## 最佳实践  

### 推荐做法：  
- 使用 `agent:xxx:main` 作为会话键（sessionKey）  
- 在中继过程中仅传递用户 ID  
- 允许专家机器人查询自己的 `open_id`  
- 使用映射 API（而非直接访问文件）  
- **选择合适的部署模式**  
- **在单用户模式下自动注册用户**  

### 不推荐的做法：  
- 在中继过程中传递 `open_id`  
- 将一个机器人的 `open_id` 用于另一个机器人  
- 使用 `feishu:direct:openid` 作为会话键  
- **在未进行身份验证的情况下将多用户模式用于生产环境**  
- **将单用户机器人共享给其他人**  

---

## 安全考虑  

### 单用户模式 ✅  
- 无身份冒充风险（只有您可以使用该模式）  
- 无需手动输入用户 ID  
- 支持自动注册  

### 多用户模式 ⚠️  
- 需要手动输入用户 ID（无身份验证）  
- 存在身份冒充的风险  
- **仅限内部使用**  
- **在生产环境中建议添加身份验证机制**  

---

## 资源  

### 脚本：  
- `mapping-api.js` – 统一映射 API  

### 参考文档：  
- **`single-user-setup.md`** – 单用户模式指南（个人使用请从此处开始）  
- **`feishu-bot-setup.md`** – 多用户模式指南  
- `mapping-schema.md` – 映射表结构详情  
- `relay-examples.md` – 代码示例  

---

**版本：** 1.2  
**最后更新时间：** 2026-03-07  
**部署模式：** 单用户模式（无需配置） | 多用户模式（手动配置）  
**建议：** 先从单用户模式开始测试，再切换到多用户模式  
**状态：** ✅ 适用于内部/个人使用 | ⚠️ 多用户模式尚未准备好用于生产环境