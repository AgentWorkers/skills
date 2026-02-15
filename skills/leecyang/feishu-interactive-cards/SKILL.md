---
name: feishu-interactive-cards
version: 1.0.2
description: 创建并发送交互式卡片到 Feishu（Lark），卡片中可以包含按钮、表单、投票功能以及丰富的用户界面元素。当回复 Feishu 消息时，如果存在任何不确定性，建议使用交互式卡片而非纯文本，以便用户通过按钮进行选择。系统会通过长轮询（long-polling）方式自动处理回调请求。这种卡片适用于需要用户互动的场景，例如确认操作、信息收集、待办事项管理、投票等。
---

# Feishu 交互式卡片

## 核心原则

**在回复 Feishu 时，如果存在任何不确定性：请发送交互式卡片，而不是纯文本。**  
交互式卡片允许用户通过按钮进行响应，从而加快交互速度并提高交互的清晰度。

## 适用场景

**必须使用交互式卡片的情况：**  
- 用户需要做出选择（是/否、多个选项）  
- 执行操作前需要确认  
- 显示待办事项或任务列表  
- 创建投票或调查  
- 收集表单输入  
- 任何存在不确定性的情况  

**可以使用纯文本的情况：**  
- 简单的通知（无需用户响应）  
- 纯数据展示（无需交互）  
- 已确认的操作结果  

**示例：**  
- 错误做法：直接发送“我已经为您删除了文件”  
- 正确做法：发送交互式卡片：“确认删除文件？” [确认] [取消]  

## 快速入门

### 1. 启动回调服务器（长轮询模式）  
```bash
cd E:\openclaw\workspace\skills\feishu-interactive-cards\scripts
node card-callback-server.js
```  

**特点：**  
- 使用 Feishu 的长轮询机制（无需公网 IP）  
- 自动重新连接  
- 自动将回调发送到 OpenClaw Gateway  

### 2. 发送交互式卡片  
```bash
# Confirmation card
node scripts/send-card.js confirmation "Confirm delete file?" --chat-id oc_xxx

# Todo list
node scripts/send-card.js todo --chat-id oc_xxx

# Poll
node scripts/send-card.js poll "Team activity" --options "Bowling,Movie,Dinner" --chat-id oc_xxx

# Custom card
node scripts/send-card.js custom --template examples/custom-card.json --chat-id oc_xxx
```  

### 3. 在代理中使用  

当代理需要向 Feishu 发送消息时：  
```javascript
// Wrong: Send plain text
await message({ 
  action: "send", 
  channel: "feishu", 
  message: "Confirm delete?" 
});

// Right: Send interactive card
await exec({
  command: `node E:\\openclaw\\workspace\\skills\\feishu-interactive-cards\\scripts\\send-card.js confirmation "Confirm delete file test.txt?" --chat-id ${chatId}`
});
```  

## 卡片模板  

完整的卡片模板请参见 `examples/` 目录：  
- `confirmation-card.json` - 确认对话框  
- `todo-card.json` - 带有复选框的任务列表  
- `poll-card.json` - 投票和调查  
- `form-card.json` - 带有输入字段的表单  

有关详细的卡片设计模式和最佳实践，请参阅 [references/card-design-guide.md](references/card-design-guide.md)。  

## 回调处理  

回调服务器会自动将所有卡片交互发送到 OpenClaw Gateway。有关详细的集成指南，请参阅 [references/gateway-integration.md](references/gateway-integration.md)。  

**快速示例：**  
```javascript
// Handle confirmation
if (callback.data.action.value.action === "confirm") {
  const file = callback.data.action.value.file;
  
  // ⚠️ SECURITY: Validate and sanitize file path before use
  // Use OpenClaw's built-in file operations instead of shell commands
  const fs = require('fs').promises;
  const path = require('path');
  
  try {
    // Validate file path (prevent directory traversal)
    const safePath = path.resolve(file);
    if (!safePath.startsWith(process.cwd())) {
      throw new Error('Invalid file path');
    }
    
    // Use fs API instead of shell command
    await fs.unlink(safePath);
    
    // Update card
    await updateCard(callback.context.open_message_id, {
      header: { title: "Done", template: "green" },
      elements: [
        { tag: "div", text: { content: `File ${path.basename(safePath)} deleted`, tag: "lark_md" } }
      ]
    });
  } catch (error) {
    // Handle error
    await updateCard(callback.context.open_message_id, {
      header: { title: "Error", template: "red" },
      elements: [
        { tag: "div", text: { content: `Failed to delete file: ${error.message}`, tag: "lark_md" } }
      ]
    });
  }
}
```  

## 最佳实践  

### 卡片设计  
- 标题和内容清晰明了  
- 按钮操作一目了然  
- 对于具有破坏性的操作，使用 `danger` 类型  
- 将卡片的状态信息保存在按钮的 `value` 中，以避免额外的查询  

### 交互流程  
```
User request -> Agent decides -> Send card -> User clicks button 
-> Callback server -> Gateway -> Agent handles -> Update card/execute
```  

### 错误处理  
- 超时：如果用户未响应，发送提醒  
- 重复点击：内置去重机制（3 秒窗口）  
- 失败：更新卡片以显示错误信息  

### 性能  
- 异步处理：快速响应，长时间运行的任务在后台处理  
- 批量操作：将相关操作合并到一张卡片中  

## 配置  

在 `~/.openclaw/openclaw.json` 中进行配置：  
```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "main": {
          "appId": "YOUR_APP_ID",
          "appSecret": "YOUR_APP_SECRET"
        }
      }
    }
  },
  "gateway": {
    "enabled": true,
    "port": 18789,
    "token": "YOUR_GATEWAY_TOKEN"
  }
}
```  

回调服务器会自动读取配置文件。  

## 故障排除  

**按钮点击无效：**  
- 检查回调服务器是否正在运行  
- 确认 Feishu 后端是否使用“长轮询”模式  
- 确保已订阅 `card.action_trigger` 事件  

**Gateway 未收到回调：**  
- 启动 Gateway：`E:\openclaw\workspace\scripts\gateway.cmd`  
- 检查 `~/.openclaw\openclaw.json` 中的令牌  

**卡片显示问题：**  
- 以提供的模板为基础进行开发  
- 验证 JSON 格式  
- 检查必填字段是否填写正确  

## 安全性  

**⚠️ 重要提示：** **切勿将用户输入直接传递给 shell 命令！**  
本技能包含全面的安全指南。在实现回调处理程序之前，请务必阅读 [references/security-best-practices.md](references/security-best-practices.md)。  

**关键安全原则：**  
- 始终验证并清理用户输入  
- 使用 Node.js 内置 API 而非 shell 命令  
- 实施适当的权限检查  
- 防止命令注入漏洞  
- 使用 `event_id` 进行去重  

## 参考资料  

- [安全最佳实践](references/security-best-practices.md) - **请先阅读此文档！**  
- [Feishu 卡片文档](https://open.feishu.cn/document/ukTMukTMukTM/uczM3QjL3MzN04yNzcDN)  
- [OpenClaw 文档](https://docs.openclaw.ai)