---
name: create-telegram-agent
description: 在 OpenClaw 中创建一个新的 Telegram 代理，并进行适当的配置。此操作适用于用户需要创建一个新的 Telegram 机器人代理的情况，包括设置代理工作区、绑定 Telegram 账户以及配置机器人令牌。在修改 `openclaw.json` 文件之前，需要用户的确认。
---
# 创建 Telegram 代理技能

此技能用于创建一个具有完整配置的新 Telegram 代理。

## 先决条件

在开始之前，请确保您已具备以下条件：
1. 一个 Telegram 机器人令牌（从 @BotFather 获取）
2. 代理的用途/描述
3. 所需的代理名称

## 工作流程

### 第一步：收集所需信息

向用户询问以下信息：

1. **代理名称**（必填）
   - 必须是唯一的
   - 可以使用小写字母、数字和连字符
   - 例如：`healthman`、`news-bot`、`task-manager`

2. **代理用途**（必填）
   - 该代理将执行什么功能？
   - 例如：“个人健康教练”、“每日新闻摘要器”、“任务提醒助手”

3. **Telegram 机器人令牌**（必填）
   - 格式：`1234567890:ABCdefGHIjklMNOpqrSTUvwxyz`
   - 从 Telegram 上的 @BotFather 处获取

   **如果用户没有令牌，请提供以下步骤：**

   > **如何创建 Telegram 机器人令牌：**
   > 1. 打开 Telegram 并搜索 **@BotFather**
   > 2. 与 BotFather 开始聊天并发送 `/newbot`
   > 3. 按照提示操作：
   >    - 为机器人输入一个 **名称**（显示名称，例如：“CookMaster”）
   >    - 为机器人输入一个 **用户名**（必须以 'bot' 结尾，例如：“cookmaster_bot”）
   > 4. BotFather 会发送一条包含您的 **HTTP API 令牌** 的消息
   > 5. 复制令牌（格式：`1234567890:ABCdefGHIjklMNOpqrSTUvwxyz`）
   >
   > **重要提示：** 请妥善保管您的令牌。任何拥有该令牌的人都可以控制您的机器人。

### 第二步：生成代理配置

根据用户的输入，准备以下配置：

#### 代理定义
```json
{
  "id": "<agent-id>",
  "name": "<Agent Name>",
  "workspace": "/Users/<user>/.openclaw/workspace-<agent-id>",
  "agentDir": "/Users/<user>/.openclaw/agents/<agent-id>/agent"
}
```

#### Telegram 绑定
```json
{
  "agentId": "<agent-id>",
  "match": {
    "channel": "telegram",
    "accountId": "<bot-id>"
  }
}
```

#### Telegram 机器人账户
```json
"<bot-id>": {
  "enabled": true,
  "dmPolicy": "pairing",
  "botToken": "<full-bot-token>",
  "groupPolicy": "allowlist",
  "streamMode": "partial"
}
```

### 第三步：展示配置以供审核

**重要提示：** **切勿直接修改 openclaw.json**

以清晰的格式向用户展示以下内容：

---

## 📋 配置摘要

将对 `openclaw.json` 进行以下修改：

### 1. 代理定义（添加到 agents.list 中）
```json
{
  "id": "<agent-id>",
  "name": "<Agent Name>",
  "workspace": "/Users/<user>/.openclaw/workspace-<agent-id>",
  "agentDir": "/Users/<user>/.openclaw/agents/<agent-id>/agent"
}
```

### 2. Telegram 绑定（添加到 bindings 中）
```json
{
  "agentId": "<agent-id>",
  "match": {
    "channel": "telegram",
    "accountId": "<bot-id>"
  }
}
```

### 3. Telegram 机器人账户（添加到 channelsTelegram.accounts 中）
```json
"<bot-id>": {
  "enabled": true,
  "dmPolicy": "pairing",
  "botToken": "<full-bot-token>",
  "groupPolicy": "allowlist",
  "streamMode": "partial"
}
```

---

### 4. 代理职责（建议在 AGENTS.md 中说明）

根据提供的用途，生成一份职责描述，内容包括：
- 代理的核心功能
- 工作方式
- 与用户的关系

---

**请确认是否继续进行修改。需要任何调整吗？**

### 第四步：等待用户确认

只有在用户明确表示同意（例如：“confirm”、“proceed”、“execute”、“go ahead”）后，才能继续下一步。

### 第五步：执行配置

确认后，请执行以下操作：

1. **创建目录：**
   ```bash
   mkdir -p /Users/<user>/.openclaw/workspace-<agent-id>
   mkdir -p /Users/<user>/.openclaw/agents/<agent-id>/agent
   ```

2. **更新 openclaw.json：**
   - 将代理添加到 `agents.list` 中
   - 将绑定信息添加到 `bindings` 中
   - 将机器人账户添加到 `channelsTelegram.accounts` 中

3. **创建代理文件：**
   - `AGENTS.md` - 代理的职责和工作流程
   - `SOUL.md` - 代理的个性和价值观

4. **报告完成情况：**
   - 显示创建的内容摘要
   - 提醒用户重启 OpenClaw 网关（如适用）
   - 提供下一步操作（例如：测试机器人）

## 重要规则

1. **未经用户明确确认，切勿修改 openclaw.json**
2. **在应用任何更改之前，务必展示完整的配置内容**
3. **从令牌中提取机器人 ID**（冒号前的数字）
4. **在编写文件之前，先创建所有必要的目录**
5. **根据代理的用途生成相应的 AGENTS.md 和 SOUL.md 文件**