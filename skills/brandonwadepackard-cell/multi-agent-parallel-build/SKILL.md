---
name: multi-agent-parallel-build
description: 协调多个编码工具（如 Claude Code、Codex 等）并行工作，以同时构建用户界面页面、API 端点或功能。适用于需要构建包含 5 个以上页面的仪表板、微服务，或任何可以并行开发独立组件的项目。内容包括波次规划、共享 shell/组件库的管理、代理的启动与调度、冲突避免机制，以及波次完成后的集成工作。
---
# 多代理并行构建

并行启动多个编码代理，以同时构建独立的组件。这可以将多页面构建的耗时减少3到5倍。

## 使用场景

- 构建4个或更多共享同一外壳但内容独立的UI页面
- 创建多个API端点组
- 任何具有明确可分离、独立工作单元的项目

## Wave架构

```
Wave 0 (Sequential — YOU do this):
  → Shared infrastructure: API, shell components, CSS, data layer
  
Wave 1 (Parallel — AGENTS do this):
  → Agent A: Page/Feature 1
  → Agent B: Page/Feature 2  
  → Agent C: Page/Feature 3
  → Agent D: Page/Feature 4
  → Agent E: Page/Feature 5

Wave 2 (Sequential — YOU do this):
  → Integration fixes, cross-component wiring, testing
```

## 第1步：Wave 0 — 构建共享基础设施

在启动代理之前，先创建所有代理所需的资源：

1. **API层**：所有代理都将使用这些API端点
2. **共享外壳**（导航栏、页眉、主题、CSS样式）
3. **组件库**（卡片、图表、表格、模态框）
4. **数据契约**（代理从API期望接收的JSON数据格式）

这一点至关重要——基于共享外壳构建的代理能够生成一致的用户界面；而每个代理都自行创建外壳则会导致界面混乱。

示例共享外壳代码：
```javascript
// shell.js — agents import this
function createShell(pageTitle, navItems) { /* sidebar + topbar */ }
function createCard(title, content) { /* themed card component */ }
function mcFetch(endpoint) { /* API wrapper with base URL */ }
```

## 第2步：规划代理任务分配

每个代理的任务包括：
- **一个明确的交付成果**（一个页面、一个功能或一项服务）
- **共享资源的路径**（shell.js、shell.css、API基础URL）
- **API契约**（需要调用的端点及预期的响应格式）
- **确保文件不重复**——每个代理都写入自己的目录或文件中

为每个代理编写相应的任务提示：
```
Build {page_name} at {file_path}.
Import shared shell from {shell_path}.
Fetch data from these API endpoints: {endpoints}.
Expected data shapes: {json_examples}.
Use Chart.js/D3 for visualization. Dark theme. No frameworks — vanilla JS + HTML.
```

## 第3步：启动代理

使用`sessions_spawn`或`coding-agent`技能同时启动所有代理：
```
Agent A: "Build agents.html — display 215 AI agents in searchable grid..."
Agent B: "Build skills.html — display 197 skills with category filters..."
Agent C: "Build knowledge.html — display 6.8K knowledge records with search..."
Agent D: "Build tools.html — display 231 tools grouped by MCP server..."
Agent E: "Build workflows.html + archetypes.html — two pages..."
```

**关键注意事项**：
- 每个代理都有自己的工作目录或独立的文件
- 在每个任务提示中包含共享外壳的路径和API契约
- 设置合理的超时时间（每个页面10-20分钟）

## 第4步：Wave 2 — 集成问题修复

并行构建后可能出现的常见问题：

### 双前缀错误
代理经常错误地构造API地址（例如：`/api/mc/api/mc/` 而不是 `/api/mc/`）。可以使用`sed`命令进行修复：
```bash
sed -i '' "s|/api/mc/api/mc/|/api/mc/|g" static/mc/*.html
```

### `mcFetch`使用不一致
有些代理直接使用`fetch()`函数，而不是共享的`mcFetch()`函数。需要统一使用标准方法。

### 静态文件加载问题
服务器需要为新生成的静态文件目录设置相应的路由：
```python
app.mount("/static/mc", StaticFiles(directory="static/mc"), name="mc-static")
```

### 大数据量导致超时
如果表格包含大量文本字段（如系统提示信息等），代理可能会生成查询并选择所有数据。需要修改API以使用更轻量级的查询方式。

## 原则

1. **Wave 0的质量决定了Wave 1的成功率**——将60%的工作精力投入到共享基础设施的构建上
2. **避免文件重复**——如果多个代理修改同一个文件，可能会导致数据冲突
3. **先构建API**——在启动UI代理之前，先完成所有API端点的构建和测试
4. **预计每个代理会出现2-3个集成问题**——为Wave 2的修复工作预留20分钟的时间
5. **5个代理是最优数量**——超过7个代理会增加协调开销，反而抵消了时间节省的效果