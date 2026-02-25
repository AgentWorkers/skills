---
name: supabase-dashboard-builder
description: 使用 Supabase REST API、D3.js 图表库、Chart.js 可视化工具以及纯 JavaScript 技术来构建管理仪表盘和命令中心。这些工具适用于创建数据探索用户界面、管理面板、任务控制面板，或任何需要从 Supabase 数据表中获取数据的可视化界面。无需使用 React 或 Vue——只需纯 HTML、JavaScript 和 CSS，同时支持统一的深色主题样式。
---
# Supabase 仪表板构建器

使用 Supabase 的 PostgREST API、纯 JavaScript 以及 D3/Chart.js 来构建丰富的管理仪表板。无需任何构建步骤，也无需依赖任何框架——只需使用 FastAPI 的 StaticFiles 功能来提供 HTML 文件即可。

## 架构

```
FastAPI Server
├── api.py (thin proxy to Supabase REST)
├── static/
│   ├── shell.js + shell.css (shared theme)
│   ├── dashboard/
│   │   ├── index.html (main page)
│   │   ├── agents.html
│   │   ├── skills.html
│   │   └── ...
```

## 第一步：API 层

创建一个轻量级的 FastAPI 代理，用于封装 Supabase 的 REST 请求。这样可以将 Supabase 的密钥保留在服务器端。

```python
import httpx
from fastapi import FastAPI

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
HEADERS = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}

app = FastAPI()

@app.get("/api/mc/{table}")
async def get_table(table: str, select: str = "*", limit: int = 100, offset: int = 0):
    allowed = {"ai_agents", "skills", "knowledge_vault", "tools", "workflows"}
    if table not in allowed:
        raise HTTPException(403, "Table not allowed")
    url = f"{SUPABASE_URL}/rest/v1/{table}?select={select}&limit={limit}&offset={offset}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url, headers={**HEADERS, "Prefer": "count=exact"})
    return r.json()
```

### 密钥使用规范：仅选择所需字段
对于包含大量文本字段的表格（如 `system_prompt`、`embeddings`），如果执行 `SELECT *` 操作会导致超时。请务必指定需要查询的列：
```
?select=id,name,type,status,created_at
```

在每个 API 端点中添加 `select` 参数，并默认只选择必要的字段。

## 第二步：共享组件（shell.js 和 shell.css）

创建 `shell.js` 和 `shell.css` 文件，所有页面都会导入这些文件：

```javascript
// shell.js
function createShell(pageTitle, navItems) {
    // Returns: sidebar (collapsible) + top bar + main content area
    // navItems: [{label, href, icon, active}]
}

function createCard(title, content, footer) {
    // Dark-themed card with header, body, optional footer
}

function createTable(headers, rows, options) {
    // Sortable, searchable table with pagination
}

function mcFetch(endpoint, params = {}) {
    // Wrapper: fetch(`/api/mc/${endpoint}?${new URLSearchParams(params)}`)
    // Handles errors, loading states
}

function createSearchBar(placeholder, onSearch) {
    // Debounced search input
}
```

### 用于统一主题的 CSS 变量：
```css
:root {
    --bg-primary: #0a0a0f;
    --bg-card: #12121a;
    --bg-hover: #1a1a2e;
    --text-primary: #e0e0e0;
    --text-secondary: #888;
    --accent: #6c63ff;
    --accent-glow: rgba(108, 99, 255, 0.3);
    --border: #2a2a3e;
    --success: #4caf50;
    --warning: #ff9800;
    --danger: #f44336;
}
```

## 第三步：页面模板

### 数据网格页面（代理、技能、工具）
```
┌─────────────────────────────┐
│ Search bar + Filter chips    │
├─────────────────────────────┤
│ Stats row (total, active,    │
│ by type)                     │
├─────────────────────────────┤
│ Sortable table or card grid  │
│ with pagination              │
└─────────────────────────────┘
```

### 强力图页面（系统概览）
使用 D3.js 的强力导向图（force-directed graph）：
- 节点代表实体（代理、工具、技能）
- 边缘代表它们之间的关系（例如代理使用工具、技能教授概念）
- 颜色根据类别区分，大小根据重要性显示
- 点击节点可查看详细信息
- 支持缩放、平移和拖动操作

### 图表页面（分析、指标）
使用 Chart.js：
- 使用雷达图展示多维数据
- 使用折线图展示时间序列数据
- 使用柱状图进行对比
- 使用饼图展示类别分布

## 第四步：使用 FastAPI 的 StaticFiles 功能

```python
from fastapi.staticfiles import StaticFiles

# Mount AFTER API routes
app.mount("/static/mc", StaticFiles(directory="static/mc"), name="mc-static")

# Convenience page routes
@app.get("/mc/{page}")
async def serve_mc_page(page: str):
    return FileResponse(f"static/mc/{page}")

@app.get("/mc/")
async def serve_mc_index():
    return FileResponse("static/mc/index.html")
```

## 常见问题及解决方法

1. **`mcFetch` 函数中的前缀问题**：代理代码中会写入 `mcFetch('/api/mc/agents')`，但实际上 `mcFetch` 已经在路径前添加了 `/api/mc/`。解决方法：直接使用 `mcFetch('agents')`，或者修改 `mcFetch` 函数以接受两种路径格式。

2. **开发环境中的 CORS 问题**：如果前端运行在不同的端口上，需要添加 CORS 中间件：
   ```python
   app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
   ```

3. **Supabase 在处理大型表格时可能超时**：使用 `select` 参数、`limit` 和 `offset` 来限制查询结果的数量。对于行数超过 1000 或文本字段长度超过 1KB 的表格，切勿使用 `SELECT *`。

4. **Chart.js 图表的复用问题**：在同一个画布上创建新图表之前，务必销毁之前的图表实例，否则旧图表可能会影响新图表的显示。

## 部署

该工具可在任何支持 Python 的平台上运行（如 Railway、Fly、Render）：
- 静态文件由 FastAPI 提供，无需额外的 CDN 服务
- Supabase 的密钥通过环境变量保留在服务器端
- 无需任何构建步骤——只需修改 HTML 文件，然后刷新浏览器即可查看效果