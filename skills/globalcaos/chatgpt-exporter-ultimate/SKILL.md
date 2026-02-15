---
name: chatgpt-exporter-ultimate
version: 1.0.3
description: "您可以立即导出所有与 ChatGPT 的对话记录——无需等待 24 小时，也无需使用浏览器扩展程序。该功能可通过 OpenClaw 浏览器中继或独立的书签工具实现。所有对话记录（包括时间戳、参与者角色、元数据以及代码块）都会被完整保留。您可以将这些对话记录连同完整的对话历史一起迁移到 OpenClaw 中。"
homepage: https://github.com/globalcaos/clawdbot-moltbot-openclaw
repository: https://github.com/globalcaos/clawdbot-moltbot-openclaw
---

# ChatGPT Exporter ULTIMATE

> 🔗 **属于 OpenClaw 生态系统** — 该功能是 OpenClaw 人工智能代理升级项目的一部分。
> 项目完整地址：https://github.com/openclaw/openclaw

**特点：**  
可在几秒钟内导出所有 ChatGPT 对话记录，无需等待 OpenAI 的 24 小时邮件通知。

## 使用方法  
```
Export my ChatGPT conversations
```

## 使用要求：  
1. 用户需通过浏览器中继功能将 Chrome 浏览器中的 ChatGPT 标签页关联到 OpenClaw 代理。  
2. 用户必须已登录 ChatGPT 账户。

## 工作原理：  
1. **关联浏览器标签页**：用户在 chatgpt.com 标签页上点击 OpenClaw 工具栏图标。  
2. **注入脚本**：代理会自动在后台注入导出脚本。  
3. **获取所有对话记录**：脚本通过内部 API 获取所有对话内容。  
4. **自动下载**：导出的 JSON 文件会自动保存到用户的下载文件夹中。

## 技术细节：  
### **身份验证**  
ChatGPT 的内部 API 需要从 `/api/auth/session` 获取 Bearer 令牌：  
```javascript
const session = await fetch('/api/auth/session', { credentials: 'include' });
const { accessToken } = await session.json();
```

### **API 端点**  
| 端点          | 功能            |  
|------------------|------------------------|  
| `/api/auth/session` | 获取访问令牌            |  
| `/backend-api/conversations?offset=N&limit=100` | 列出所有对话记录            |  
| `/backend-api/conversation/{id}` | 获取单条对话记录的详细内容    |  

### **导出脚本**  
该代理会注入一个可自动运行的脚本，执行以下操作：  
1. 获取访问令牌。  
2. 分页获取所有对话记录（每页 100 条）。  
3. 提取每条对话的完整内容。  
4. 从数据结构中提取消息内容。  
5. 生成 JSON 文件并触发下载。

### **进度跟踪**  
```javascript
window.__exportStatus = { phase: 'fetching', progress: N, total: M }
```

## 输出格式：  
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

## **性能限制：**  
- 每次获取对话记录之间有 100 毫秒的延迟。  
- 处理 200 条对话记录大约需要 3 分钟。  
- ChatGPT 允许每分钟发送约 100 次请求。

## **故障排除：**  
| 问题            | 解决方案                    |  
|------------------|---------------------------|  
| 未关联标签页        | 在 ChatGPT 标签页上点击 OpenClaw 工具栏图标            |  
| 出现 401 错误        | 重新登录 ChatGPT 并重新关联标签页            |  
| 导出失败          | 检查浏览器控制台是否有错误信息            |  
| 未下载文件        | 检查下载文件夹或浏览器设置                |  

**相关文件：**  
- `scripts/bookmarklet.js`：独立的控制台脚本（可粘贴到 DevTools 中使用）。  
- `scripts/export.sh`：支持使用令牌参数的命令行导出工具。  

**与其他工具的比较：**  
| 功能                | ChatGPT Exporter                | ChatGPT 扩展程序                |  
|------------------|------------------|---------------------------|  
| 安装方式            | 无需额外安装                | 需通过 Chrome Web Store 安装            |  
| 自动化程度          | 完全自动化（由代理控制）            | 手动操作                          |  
| 输出格式            | JSON                        | JSON、Markdown、HTML、PNG                 |  
| 批量导出            | 支持自动批量导出                | 支持“全选”功能                    |  
| 进度显示            | 通过代理实时显示进度                | 通过 UI 提供进度条显示                |

**适用场景：**  
- 自动化导出操作  
- 程序化访问 ChatGPT 数据  
- 适用于需要高效处理大量对话的场景  

**扩展程序的优势：**  
- 更便捷的安装方式（Chrome Web Store）。  
- 需要用户手动操作（点击按钮）。  
- 支持多种输出格式（JSON、Markdown、HTML、PNG）。  
- 支持批量导出（需手动选择）。  
- 提供直观的进度显示界面。

**使用建议：**  
- 当需要自动化处理大量对话记录时，建议使用 ChatGPT Exporter。  
- 当需要手动导出对话记录或支持多种格式时，可以使用 ChatGPT 扩展程序。