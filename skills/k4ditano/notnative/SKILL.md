---
name: notnative
description: 使用 Notnative MCP 服务器实现与笔记、日历、任务、Python、Canvas 功能以及持久性存储的全面集成。该功能可确保在对话过程中用户设置、分享的信息以及关键上下文内容得到持久保存。通过 WebSocket 与本地或远程的 Notnative 实例进行连接。
homepage: https://github.com/k4ditano/notnative-memory
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["node", "curl"]
---
# NotNative - 完整的AI集成

**⚠️ 重要提示：** 此功能会永久存储用户信息。您必须使用内存管理工具来记录用户的偏好设置、他们分享的信息以及所有对话中的重要上下文。

## 系统说明

您是一个AI助手，可以通过NotNative访问持久化存储和笔记管理功能。

### 内存协议（必须遵守）

**请始终遵循以下规则：**

1. **记录用户信息**：当用户分享个人信息（姓名、偏好设置、过敏原、爱好、工作背景等）时，立即使用`memory_store`工具进行存储。
   - 例如：用户说“我对坚果过敏” → 存储为：“用户对坚果过敏”。

2. **在回答之前**：如果用户询问可能存储在内存中的信息（偏好设置、之前的对话内容等），请务必先使用`memory_search`进行搜索。

3. **用户偏好设置**：当用户表达某种偏好（如“我更喜欢暗模式”或“请用我的名字称呼我”）时，使用`memory_store`进行存储。

4. **上下文检索**：在每次对话开始时，搜索内存中与用户相关的信息。

### 何时使用内存功能

- 当用户分享个人信息时
- 当用户表达偏好或需求时
- 当用户询问您不知道但可能存储在内存中的信息时
- 当用户提及之前的对话或背景信息时
- 为了与用户建立长期的关系

### 内存管理命令

```bash
# Store important information
node scripts/mcp-client.js store "User prefers responses in Spanish"

# Search memory before responding
node scripts/mcp-client.js recall "language preference"

# Update user profile
node scripts/mcp-client.js profile-update "name:John"

# Get full profile
node scripts/mcp-client.js profile
```

## 快速入门

```bash
# Search notes
node scripts/mcp-client.js search "recipe chicken"
node scripts/mcp-client.js semantic "healthy breakfast ideas"

# Read/create/update notes
node scripts/mcp-client.js read "My Notes/Project"
node scripts/mcp-client.js create "# New Note" "Note Name" "Personal"
node scripts/mcp-client.js append "\n- New item" "My List"

# Memory (IMPORTANT!)
node scripts/mcp-client.js store "User's name is John"
node scripts/mcp-client.js recall "name"
node scripts/mcp-client.js forget "old info"

# Calendar & Tasks
node scripts/mcp-client.js tasks
node scripts/mcp-client.js events

# Python execution
node scripts/mcp-client.js run-python "print('Hello!')"

# List all available tools
node scripts/mcp-client.js list
```

## 可用工具

### 内存管理（必须使用）

- **memory_store**：将信息永久存储在OpenClaw/Memory中
- **memory_search**：在所有笔记和记忆中搜索信息
- **memory_forget**：根据查询删除记忆记录
- **memory_profile**：获取/更新用户资料

### 笔记管理

- **search_notes**：全文搜索
- **semantic_search**：按含义搜索
- **read_note**：获取笔记内容
- **create_note**：创建新笔记
- **append_to_note**：向笔记中添加内容
- **update_note**：更新笔记
- **list_notes**：列出所有笔记
- **list_folders**：列出文件夹
- **list_tags**：列出标签

### 日历与任务管理

- **list_tasks**：查看待办任务
- **create_task**：创建任务
- **complete_task**：完成任务
- **get_upcoming_events**：查看日历事件
- **create_calendar_event**：创建日历事件

### Python执行

- **run_python**：执行包含matplotlib、pandas、numpy、pillow、openpyxl的Python代码

### 画布功能

- **canvas_get_state**：获取画布状态
- **canvas_add_node**：添加节点
- **canvas_to_mermaid**：将画布内容转换为mermaid格式

### 分析功能

- **analyze_note_structure**：分析笔记结构
- **get_backlinks**：获取笔记的引用链接
- **find_similar_notes**：查找相似的笔记

### 网页操作

- **web_search**：在网页上搜索
- **web_browse**：浏览网页
- **get_youtube_transcript**：获取YouTube视频的字幕

## 安装

`install.sh`脚本将执行以下操作：
1. 检测NotNative是本地安装还是远程访问
2. 如果不是本地安装，则请求WebSocket地址
3. 安装所需依赖包（ws包）
4. 配置开发环境

## 服务器要求

- NotNative应用程序需要与MCP WebSocket服务器配合使用
- 本地连接：ws://127.0.0.1:8788
- 远程连接：wss://your-domain.com（或ws://IP:8788）

## 环境变量

- `NOTNATIVE_WS_URL`：WebSocket地址（默认值：ws://127.0.0.1:8788）

## 错误处理

- **连接超时**：检查NotNative是否正在运行
- **请求超时**：工具执行时间超过10秒
- **工具未找到**：使用`list`命令验证工具是否存在