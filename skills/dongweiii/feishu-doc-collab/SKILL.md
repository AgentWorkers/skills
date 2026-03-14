---
name: feishu-doc-collab
description: >
  在 Feishu（Lark）文档中启用实时 AI 协作功能。当用户编辑 Feishu 文档时，AI 代理会自动检测到变化，读取文档内容，并即时作出回应——从而将任何 Feishu 文档转变为实时的人机对话场景。
  **主要功能：**
  - **Feishu 文档编辑事件**：触发独立的 AI 代理会话。
  - **结构化的文档内聊天协议**：通过状态标志防止用户在输入内容时 AI 过早作出回应。
  - **多方支持**：同一文档中可以同时有多个用户和多个 AI 代理参与对话。
  - **集成 Bitable（电子表格）任务板**：用于协作式任务管理。
  - **防循环机制**：AI 代理自身的编辑操作会被自动忽略。
  **相关触发条件：**
  - Feishu 文档协作
  - 文档编辑事件
  - 文档内对话
  - Lark 文档的 AI 功能
  - Feishu 文档的自动回复
---
# Feishu 文档协作技能

将任何 Feishu 文档转换为实时的人机协作空间。

## 概述

该技能对 OpenClaw 的 Feishu 扩展程序进行了修改，以检测文档编辑事件并触发独立的 AI 代理会话。结合文档内的结构化聊天协议，它实现了以下功能：

- ✍️ 在 Feishu 文档中输入问题 → AI 会阅读问题并回复
- 🚦 状态标志（🔴 编辑中 / 🟢 完成）可防止过早的回复
- 👥 多方路由：消息可以定向发送给特定参与者
- 📋 可选的 Bitable 任务板，用于结构化任务管理

## 先决条件

1. **已配置 Feishu 通道的 OpenClaw**（应用 ID、应用密钥、事件订阅）
2. **已启用 Feishu 应用事件订阅**：
   - `drive.file.edit_v1` — 文档编辑事件
   - `drive.file.bitable_record_changed_v1` — （可选）Bitable 记录变更
3. 在 `openclaw.json` 中启用了 **钩子**：
   ```json
   {
     "hooks": {
       "enabled": true,
       "token": "your-hooks-token-here"
     }
   }
   ```

## 快速设置

### 第 1 步：在 openclaw.json 中启用钩子

如果不存在 `hooks` 部分，请添加它：

```bash
# Generate a random token
TOKEN=$(openssl rand -hex 16)
echo "Your hooks token: $TOKEN"
# Then add to openclaw.json:
# "hooks": { "enabled": true, "token": "<TOKEN>" }
```

### 第 2 步：应用监控补丁

```bash
bash ./skills/feishu-doc-collab/scripts/patch-monitor.sh
```

此补丁会修改 Feishu 扩展程序中的 `monitor.ts`，以实现以下功能：
- 检测 `drive.file.edit_v1` 事件
- 通过 `/hooks/agent` 触发一个独立的代理会话
- 代理会读取文档，检查新消息并作出回复

### 第 3 步：配置代理身份

编辑 `./skills/feishu-doc-collab/config.json`：

```json
{
  "agent_name": "MyBot",
  "agent_display_name": "My AI Assistant"
}
```

该补丁脚本用于设置消息路由规则（代理将以何种身份进行回复）。

### 第 4 步：重启网关

```bash
openclaw gateway restart
```

### 第 5 步：设置文档聊天协议

将协议模板复制到您的工作区：

```bash
cp ./skills/feishu-doc-collab/assets/DOC_PROTOCOL_TEMPLATE.md ./DOC_PROTOCOL.md
```

编辑 `DOC_PROTOCOL.md` 以填写参与者名单。

## 工作原理

### 文档编辑流程

```
User edits Feishu doc
        ↓
Feishu sends drive.file.edit_v1 event
        ↓
Patched monitor.ts receives event
        ↓
Checks: is this the bot's own edit? → Yes: skip (anti-loop)
        ↓ No
POST /hooks/agent with isolated session instructions
        ↓
Agent reads DOC_PROTOCOL.md for message format
        ↓
Agent reads the document, finds last message block
        ↓
Checks: status=🟢? addressed to me? not from me?
        ↓ Yes
Agent composes reply and appends to document
```

### 文档内聊天协议

文档中的消息遵循以下格式：

```markdown
---
> **Sender Name** → **Receiver Name** | 🟢 完成

Your message content here.
```

**状态标志：**
- 🔴 编辑中 (editing) — AI 不会处理此消息（用户仍在输入）
- 🟢 完成 (done) — AI 会阅读并回复此消息

**路由规则：**
- `→ AgentName` — 发送给特定的 AI 代理
- `→ all` — 广播给所有参与者

这解决了一个关键问题：Feishu 在用户输入时会自动保存文档，如果没有状态标志机制，会导致 AI 过早回复。

### Bitable 任务板（可选）

用于与文档协作一起进行结构化任务管理：

1. 创建一个 Bitable 表格，包含以下字段：
   - 任务摘要（文本）
   - 状态（单选）：未读 / 已读 / 进行中 / 完成 / 无关
   - 创建时间（日期时间）
   - 发起人（单选）：参与者姓名
   - 收件人（多选）：参与者姓名
   - 优先级（单选）：低 / 中 / 高 / 紧急
   - 备注（文本）
   - 相关文档（URL）

2. 在 `config.json` 中进行配置：
   ```json
   {
     "bitable": {
       "app_token": "your_bitable_app_token",
       "table_id": "your_table_id"
     }
   }
   ```

3. 该补丁还处理 `bitable_record_changed_v1` 事件，以实现任务路由。

## 更新后的重新应用

**⚠️ OpenClaw 的更新会覆盖 `monitor.ts`。** 在任何更新后，请执行以下操作：

```bash
bash ./skills/feishu-doc-collab/scripts/patch-monitor.sh
openclaw gateway restart
```

该补丁脚本是幂等的——可以多次安全运行。

## 配置参考

### config.json

| 字段 | 类型 | 是否必需 | 描述 |
|-------|------|----------|-------------|
| `agent_name` | 字符串 | 是 | 协议路由中使用的内部名称 |
| `agent_display_name` | 字符串 | 是 | 文档回复中显示的名称 |
| `bitable.app_token` | 字符串 | 否 | 用于任务板的 Bitable 应用令牌 |
| `bitable.table_id` | 字符串 | 否 | 用于任务板的 Bitable 表格 ID |

### 环境

该补丁从 `~/.openclaw/openclaw.json` 中读取以下信息：
- `hooks.token` — `/hooks/agent` 端点的认证信息
- `gateway.port` — 网关端口（默认：18789）

## 限制

- 需要修改 OpenClaw 的源文件（在更新过程中可能会失效）
- Feishu 应用需要启用 `drive.file.edit_v1` 事件订阅
- 文档必须使用结构化协议格式才能确保路由正确
- 该功能最适合 docx 格式的文档；其他文件类型（如表格、幻灯片）不受支持

## 致谢

由 dongwei 创建。灵感来源于在中国企业工作流程中使用 Feishu/Lark 进行实时人机协作的需求。

## 许可证

MIT