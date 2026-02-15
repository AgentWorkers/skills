---
name: chatgpt-exporter-ultimate
version: 1.0.3
description: ChatGPT对话导出工具：支持即时导出所有聊天记录，无需等待24小时，也无需使用任何扩展程序。可通过浏览器代理或独立的书签let进行使用。导出的内容包括完整的对话历史记录（附带时间戳、参与者角色及元数据）。
homepage: https://github.com/openclaw/openclaw
repository: https://github.com/openclaw/openclaw
---

# ChatGPT Exporter ULTIMATE

> 🔗 **OpenClaw生态系统的一部分** — 该功能属于一个更大规模的人工智能代理升级项目。
> 项目完整地址：https://github.com/openclaw/openclaw

**特点：**
- 在几秒钟内导出所有ChatGPT对话记录，无需等待OpenAI发送的24小时导出邮件。

## 使用方法

```
Export my ChatGPT conversations
```

## 使用要求：
1. 用户需通过浏览器代理将Chrome中的ChatGPT标签页关联到OpenClaw。
2. 用户必须已登录ChatGPT。

## 工作原理：
1. **关联标签页**：用户在chatgpt.com标签页上点击OpenClaw工具栏图标。
2. **注入脚本**：代理程序在后台注入导出脚本。
3. **获取所有对话记录**：脚本通过内部API获取所有对话内容。
4. **自动下载**：导出的JSON文件会自动保存到用户的下载文件夹中。

## 技术细节：
### **身份验证**
ChatGPT的内部API需要从 `/api/auth/session` 获取Bearer令牌：
```javascript
const session = await fetch('/api/auth/session', { credentials: 'include' });
const { accessToken } = await session.json();
```

### **API接口**：
| 接口 | 功能 |
|--------|--------|
| `/api/auth/session` | 获取访问令牌 |
| `/backend-api/conversations?offset=N&limit=100` | 列出所有对话记录 |
| `/backend-api/conversation/{id}` | 获取单条对话的详细内容 |

### **导出脚本**：
代理程序会注入一个可自动运行的脚本，该脚本执行以下操作：
1. 获取访问令牌。
2. 分页获取所有对话记录（每页100条）。
3. 提取每条对话的完整内容。
4. 从数据结构中提取消息内容。
5. 生成JSON文件并触发下载。

### **进度跟踪**：
```javascript
window.__exportStatus = { phase: 'fetching', progress: N, total: M }
```

## **输出格式**：
```json
{
  "exported": "2026-02-06T11:10:09.699Z",
  "conversations": [
    {
      "id": "abc123",
      "title": "Conversation Title",
      "created": 1770273234.966738,
      "messages": [
        { "role": "user", "text": "...", "time": 1770273234 },
        { "role": "assistant", "text": "...", "time": 1770273240 }
      ]
    }
  ]
}
```

## **速率限制**：
- 每次获取对话记录之间有100毫秒的延迟。
- 导出200条对话记录大约需要3分钟。
- ChatGPT允许每分钟发送约100个请求。

## **故障排除**：
| 问题 | 解决方案 |
|------|---------|
| 标签页未关联 | 在ChatGPT标签页上点击OpenClaw工具栏图标。 |
| 出现401错误 | 重新登录ChatGPT并重新关联标签页。 |
| 导出失败 | 检查浏览器控制台是否有错误信息。 |
| 未下载文件 | 检查下载文件夹或浏览器设置。

## **相关文件**：
- `scripts/bookmarklet.js`：独立的控制台脚本（可粘贴到DevTools中使用）。  
- `scripts/export.sh`：支持使用令牌参数的命令行导出工具。

**与扩展程序的比较**：
| 功能 | 本功能 | ChatGPT Exporter扩展程序 |
|--------|------------|---------------------------|
| 安装方式 | 无需安装 | 需通过Chrome Web Store安装。 |
| 自动化程度 | 完全自动化（由代理程序控制） | 需用户手动操作。 |
| 输出格式 | JSON | 支持JSON、Markdown、HTML、PNG格式。 |
| 批量导出 | 支持（自动完成） | 支持“全选”功能。 |
| 进度显示 | 由代理程序监控 | 通过UI进度条显示。 |

**适用场景**：
- 适用于需要自动化导出对话记录的场景。  
- 适用于需要通过编程方式访问ChatGPT数据的场景。  
- 适用于需要使用代理程序处理工作流程的场景。

**扩展程序的适用场景**：
- 适用于需要手动导出对话记录的场景。  
- 适用于需要支持多种输出格式的场景。  
- 适用于需要直观的UI界面来查看导出进度的场景。