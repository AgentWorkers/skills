---
name: miro-mcp
description: 将 OpenClaw 代理通过 Model Context Protocol (MCP) 连接到 Miro。该协议适用于生成图表、可视化代码、设计头脑风暴板布局，或将 Miro 集成到基于人工智能的设计工作流程中。支持 OAuth 2.1 身份验证，兼容 14 种以上的 MCP 客户端（如 Cursor、Claude Code、Replit、Lovable、VSCode/Copilot、Gemini CLI、Windsurf、Kiro CLI、Amazon Q 等）。非常适合用于设计思维、架构可视化、项目规划及协作式创意构思。
---
# Miro MCP集成

## 快速入门

Miro MCP允许AI代理通过Model Context Protocol（一种用于AI与外部系统集成的开放标准）读取和写入Miro画布内容。您的代理可以生成图表、分析画布内容，并根据视觉设计创建代码。

**先决条件：**
- 支持MCP的客户端（Cursor、Claude Code、Replit、Lovable、VSCode等）
- 客户端需支持OAuth 2.1
- 拥有有效的Miro工作区访问权限

**最小化设置：**
1. 添加MCP配置：`url: https://mcp.miro.com/`
2. 点击“连接”并通过OAuth 2.1进行身份验证
3. 在OAuth流程中选择您的Miro团队
4. 开始使用画布URL进行操作

**快速示例：**
```
Prompt: "Summarize the content on this board: https://miro.com/app/board/uXjVGAeRkgI=/"
Result: Agent reads board items and returns a summary
```

有关每个客户端的详细设置说明，请参阅[references/mcp-connection.md]。

## 核心功能

Miro MCP主要支持两种用途：**图表生成**和**代码生成**。

### 图表生成

- **从代码生成图表：** 提供仓库URL或代码片段 → 代理生成架构图/数据流图（UML、流程图、ERD）
- **从产品需求文档（PRD）生成图表：** 分享产品需求文档 → 代理创建可视化的工作流程图、用户流程图、状态图
- **从文本描述生成图表：** 描述系统结构 → 代理将其可视化
- **从GitHub URL生成图表：** 代理分析GitHub仓库并生成架构图

**工具：** 使用`code_explain_on_board`提示或`diagram_create`工具（支持DSL格式，如流程图、UML类图/序列图、ERD）。

### 代码生成

- **从产品需求文档（PRD）生成代码：** 画布中包含产品需求 → 代理生成文档及实现指南
- **从架构图生成代码：** 画布上的架构图 → 代理生成相应的代码结构
- **从原型图生成代码：** 画布上的原型图 → 代理将其作为实现指南

**工具：** 使用`code_create_from_board`提示来分析画布内容并生成代码。

### 协作功能
- 读取画布中的内容（框架、文档、原型图、图表、表格、图片）
- 向画布中添加新的图表和文档
- 通过查找和替换功能更新现有内容
- 使用基于光标的页面导航来访问画布元素
- Miro MCP应用是团队级使用的

## 支持的客户端

Miro MCP已与14个以上兼容的客户端进行了测试和验证：

| 客户端 | 连接方式 | 备注 |
|--------|--------|-------|
| **Cursor** | 配置文件 + OAuth | 在设置中配置JSON文件 |
| **Claude Code** | 命令行：`claude mcp add` | 通过命令行设置 |
| **Replit** | Web界面 + OAuth | 通过安装按钮集成 |
| **Lovable** | Web界面 + OAuth | 在设置中选择集成选项 |
| **VSCode/GitHub Copilot** | MCP注册表 + OAuth | 通过GitHub MCP注册表链接连接 |
| **Windsurf** | 配置文件 + OAuth | 在设置中配置JSON文件 |
| **Gemini CLI** | 命令行设置 | 提供视频教程 |
| **Kiro CLI** | 配置文件 + OAuth | 在`.kiro/settings/mcp.json`中配置 |
| **Amazon Q IDE** | 在设置中配置OAuth | 通过IDE扩展集成 |
| **Claude（Web/桌面版）** | 通过聊天界面添加连接器 |
| **Kiro IDE** | 内置支持 | 支持MCP |
| **Glean** | 内置支持 | 支持MCP集成 |
| **Devin** | 内置支持 | 支持MCP |
| **OpenAI Codex** | 基于协议直接连接 |

有关每个客户端的详细设置步骤，请参阅[references/ai-coding-tools.md]。

## 配置指南

### OAuth 2.1流程概述

Miro MCP使用OAuth 2.1和动态客户端注册进行安全认证：
1. **请求授权** → 客户端构建包含`client_id`、`redirect_uri`、`scope`的授权URL
2. **Miro OAuth服务器** → 用户登录（或确认现有会话）并同意请求的权限
3. **团队选择**（关键步骤） → 用户明确选择MCP应用可以访问的Miro团队
4. **授权码** → Miro返回`authorization_code`
5. **令牌交换** → 客户端用`authorization_code`交换获取`access_token`和`refresh_token`
6. **访问画布** → 代理在调用Miro MCP服务器的API时包含`access_token`

**为什么团队选择很重要：** MCP是团队级使用的。如果您引用的画布不属于您登录的团队，将会出现访问错误。只需重新登录并选择正确的团队即可。

### 配置JSON

标准JSON配置（适用于大多数客户端）：
```json
{
  "mcpServers": {
    "miro-mcp": {
      "url": "https://mcp.miro.com/",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### 速率限制

- 所有操作均受标准API速率限制（按用户和所有工具调用次数统计）
- 各工具可能有更严格的限制（可能会更改）
- `context_get`操作较为耗资源 → 会消耗Miro AI信用点数（仅此操作需要）
- **优化建议：** 批量操作、避免并行调用`context_get`、缓存频繁访问的内容

### 企业注意事项

如果您使用的是**Miro Enterprise Plan**，管理员需要先在您的组织中启用Miro MCP服务器才能使用该功能。请联系您的Miro管理员进行启用。

## 常见工作流程

### 工作流程1：从代码库生成架构图
```
User prompt: "Analyze my codebase at ~/dev/myapp and create an architecture diagram on this board: [board-URL]"

Agent steps:
1. Read codebase structure
2. Analyze dependencies and modules
3. Use code_explain_on_board to generate UML diagram
4. Create diagram on Miro board via diagram_create tool
```

### 工作流程2：从产品需求文档（PRD）生成代码
```
User prompt: "This board has our PRD. Generate implementation docs and code guidance."

Agent steps:
1. Use context_explore to find PRD document on board
2. Use context_get to read PRD details
3. Use code_create_from_board prompt
4. Generate docs and implementation guidance
5. Create doc_create items on board with generated content
```

### 工作流程3：迭代设计反馈
```
User prompt: "Summarize this prototype and suggest improvements"

Agent steps:
1. Use context_explore to find prototype screens
2. Use context_get to read screen details/markup
3. Analyze and suggest UX improvements
4. Use doc_create to add feedback document to board
```

## REST API直接集成（自动化与脚本编写）

除了MCP之外，Miro的**REST API**还支持通过curl/bash脚本实现自动化操作：
- 批量创建和模板化画布
- 自动生成形状和内容
- 与OpenClaw工作流程集成
- 自定义持续集成/持续交付（CI/CD）流程中的画布生成
- 模板复制和版本管理

### 认证

使用OAuth 2.1承载令牌：
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" https://api.miro.com/v2/...
```

令牌通过OAuth流程获取（详见SKILL.md中的OAuth设置），仅在指定范围内有效。

### 画布创建
```bash
curl -X POST https://api.miro.com/v2/boards \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Board",
    "description": "Auto-generated template"
  }' | jq '.id'
```

### 形状创建（关键API格式）

**正确的嵌套结构**（通过第二阶段测试确认）：
```bash
curl -X POST https://api.miro.com/v2/boards/{board_id}/shapes \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "shapeType": "rectangle",
      "content": "Label text"
    },
    "geometry": {
      "width": 200,
      "height": 100
    },
    "position": {
      "x": 0,
      "y": 0,
      "origin": "center"
    },
    "style": {
      "fillColor": "#3b82f6",
      "borderColor": "#1e40af",
      "borderWidth": 2
    }
  }'
```

**形状类型：** 矩形、圆形、椭圆形、菱形、三角形、五边形、六边形等

### 文本元素
```bash
curl -X POST https://api.miro.com/v2/boards/{board_id}/text \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "<b>Bold</b> and <i>italic</i> text",
    "geometry": {
      "width": 300,
      "height": 100
    },
    "position": {
      "x": 0,
      "y": 0,
      "origin": "center"
    },
    "style": {
      "fontSize": 24,
      "color": "#000000",
      "fontFamily": "Arial",
      "textAlign": "center"
    }
  }'
```

### 性能与扩展性

- **形状创建速度：** 每个形状约46毫秒（测试结果）
- **批量操作：** 每秒可快速创建10-20多个形状
- **速率限制：** 遵循标准Miro API限制（对于大多数用例来说已经很宽松）
- **脚本执行：** Bash/curl脚本可在5秒内完成包含40多个元素的画布创建

### 模板复制模式

有效的模板复制结构：
```
1. Board creation (metadata)
2. Section headers (color-coded background + text)
3. Content containers (boxes, cards, lists)
4. Visual hierarchy (title → sections → items)
5. Guides (methodology, examples, legends)
```

有关工作示例，请查看工作区中的`miro-journey-map-recreation.sh`文件。

### 常见REST API端点

| 方法 | 端点 | 功能 |
|--------|----------|---------|
| POST | `/boards` | 创建画布 |
| GET | `/boards/{id}` | 获取画布信息 |
| POST | `/boards/{id}/shapes` | 添加形状 |
| POST | `/boards/{id}/text` | 添加文本 |
| POST | `/boards/{id}/frames` | 添加框架（容器） |
| GET | `/boards/{id}/items` | 列出画布元素 |
| PATCH | `/boards/{id}/items/{id}` | 更新元素 |
| DELETE | `/boards/{id}/items/{id}` | 删除元素 |

### 实际示例：使用颜色编码区分不同部分
```bash
# Create section background
curl -X POST https://api.miro.com/v2/boards/$BOARD_ID/shapes \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"data\": {\"shapeType\": \"rectangle\"},
    \"geometry\": {\"width\": 1400, \"height\": 120},
    \"position\": {\"x\": 0, \"y\": -400, \"origin\": \"center\"},
    \"style\": {\"fillColor\": \"#3b82f6\", \"borderWidth\": 2}
  }"

# Add section title
curl -X POST https://api.miro.com/v2/boards/$BOARD_ID/text \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"content\": \"<b>Section Title</b>\",
    \"geometry\": {\"width\": 1300, \"height\": 100},
    \"position\": {\"x\": -650, \"y\": -400, \"origin\": \"center\"},
    \"style\": {\"fontSize\": 28, \"color\": \"#ffffff\"}
  }"
```

### 关键要点

- **API结构很重要：** `data`、`geometry`、`position`、`style`的正确嵌套至关重要
- **Bash自动化可靠：** 当API接口清晰时，无需使用SDK
- **颜色方案至关重要：** 一致的颜色（蓝色、紫色、绿色、黄色）使模板更加专业
- **定位使用中心原点：** (0, 0)表示画布中心；调整x/y坐标以实现网格布局
- **模板脚本可重用：** 保存有效的脚本；可针对颜色/内容/布局进行迭代优化

## 资源链接

- **客户端设置指南：** 请参阅[references/ai-coding-tools.md]，了解所有14个支持客户端的详细设置步骤
- **连接详情：** 请参阅[references/mcp-connection.md]，了解OAuth流程、先决条件、故障排除和企业级设置
- **MCP概述：** 请参阅[references/mcp-overview.md]，了解MCP的功能、重要性、安全模型和概述
- **工具与提示：** 请参阅[references/mcp-prompts.md]，了解所有14个工具的完整参考信息、内置提示和速率限制详情
- **最佳实践：** 请参阅[references/best-practices.md]，了解工作流程模式、常见问题（团队不匹配、OAuth过期、速率限制）及优化策略
- **REST API基础：** 请参阅[references/rest-api-essentials.md]，了解每个工具的API参考、错误处理、成本模型和实际应用示例
- **REST API自动化脚本：** 请查看`/Users/bigbubba/.openclaw/workspace/miro-journey-map-recreation.sh`，了解模板复制的实际示例