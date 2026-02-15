---
name: zoom-manager
description: 通过 OAuth API 管理 Zoom 会议：创建、列出、删除和更新会议事件。
metadata: {
  "clawdbot": {
    "emoji": "📹",
    "requires": {"bins": ["node"]},
    "secrets": ["ZOOM_CLIENT_ID", "ZOOM_CLIENT_SECRET", "ZOOM_ACCOUNT_ID"]
  }
}
---

# Zoom 管理器

通过这个强大的、无界面的集成功能，您可以直接在 Clawdbot 中管理 Zoom 会议。该功能允许您在不打开 Zoom 仪表板的情况下自动化会议工作流程。

### 主要特性：
- **完整的会议生命周期管理**：使用简单的自然语言命令或 CLI 命令来创建、列出、更新和删除会议。
- **适合企业级使用**：支持服务器到服务器的 OAuth 验证机制，确保安全性和稳定性。
- **自动录制**：默认支持云录制功能，确保所有会议内容都被保存。
- **开发者友好**：采用简洁的 Node.js 实现，易于扩展以适应自定义自动化需求（例如，在 CRM 数据更新后自动安排会议）。
- **无界面且响应迅速**：无需浏览器，直接与 Zoom REST API v2 进行交互。

## 设置

1. 在 [Zoom 应用市场](https://marketplace.zoom.us/) 中创建一个 **服务器到服务器的 OAuth** 应用。
2. **所需权限范围**：在 Zoom 应用市场的 “权限范围” 标签下，添加以下权限：
   - **会议**：
     - `meeting:read:admin` / `meeting:read:master`（查看会议信息）
     - `meeting:write:admin` / `meeting:write:master`（创建和更新会议）
     - `meeting:delete:admin` / `meeting:delete:master`（删除会议）
   - **用户**：`user:read:admin`
   - **录制**：`recording:read:admin`
3. 从 “应用凭证” 标签下获取您的 **客户端 ID**、**客户端密钥** 和 **账户 ID**。
4. 将这些信息设置为 Clawdbot 配置文件中的环境变量：
   - `ZOOM_CLIENT_ID`
   - `ZOOM_CLIENT_SECRET`
   - `ZOOM_ACCOUNT_ID`

## 命令

### 列出会议
```bash
node {baseDir}/scripts/zoom-cli.js list
```

### 创建会议
```bash
node {baseDir}/scripts/zoom-cli.js create "Meeting Topic" "2026-01-30T10:00:00Z" 60
```

### 更新会议
```bash
node {baseDir}/scripts/zoom-cli.js update <meeting_id> <new_start_time> <duration> "New Topic"
```

### 获取会议信息
```bash
node {baseDir}/scripts/zoom-cli.js info <meeting_id>
```

### 删除会议
```bash
node {baseDir}/scripts/zoom-cli.js delete <meeting_id>
```