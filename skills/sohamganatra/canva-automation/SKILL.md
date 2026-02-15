---
name: canva-automation
description: "通过 Rube MCP (Composio) 自动化 Canva 的各项任务：包括设计、导出、文件夹管理以及品牌模板的应用和自动填充功能。在使用任何工具之前，请务必先查找当前可用的功能或方案。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 自动化 Canva 操作

通过 Composio 的 Canva 工具包，利用 Rube MCP 实现 Canva 设计操作的自动化。

## 先决条件

- Rube MCP 必须已连接（可使用 `RUBE_SEARCH_TOOLS`）
- 通过 `RUBE_MANAGE_CONNECTIONS` 与 `canva` 工具包建立有效的 Canva 连接
- 在执行任何工作流之前，务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具架构信息

## 设置

**添加 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可。

1. 通过确认 `RUBE_SEARCH_TOOLS` 是否有响应来验证 Rube MCP 是否可用。
2. 使用 `canva` 工具包调用 `RUBE_MANAGE_CONNECTIONS`。
3. 如果连接状态不是 `ACTIVE`，请按照返回的链接完成 Canva 的 OAuth 验证。
4. 在运行任何工作流之前，确保连接状态显示为 `ACTIVE`。

## 核心工作流

### 1. 列出并浏览设计

**使用场景**：用户需要查找现有的设计或浏览他们的 Canva 图库

**工具序列**：
1. `CANVA_LIST_USER_DESIGNS` - 列出所有设计，支持可选的过滤条件 [必填]

**关键参数**：
- `query`：用于按名称过滤设计的搜索词
- `continuation`：上一次请求的分页令牌
- `ownership`：按“owned”、“shared”或“any”进行过滤
- `sort_by`：排序字段（例如 `modified_at`、`title`）

**注意事项**：
- 结果是分页显示的；请持续使用 `continuation` 令牌进行分页
- 已删除的设计可能会短暂地出现在结果中；请检查设计的状态
- 搜索是基于子字符串的，不支持模糊匹配

### 2. 创建和设计新设计

**使用场景**：用户希望从零开始创建新的 Canva 设计或使用模板

**工具序列**：
1. `CANVA_ACCESS_USER_SPECIFIC_BRAND_TEMPLATES_LIST` - 浏览可用的品牌模板 [可选]
2. `CANVA_CREATE_CANVA_DESIGN_WITH_OPTIONAL_ASSET` - 创建新的设计 [必填]

**关键参数**：
- `design_type`：设计类型（例如 “Presentation”、“Poster”、“SocialMedia”）
- `title`：新设计的名称
- `asset_id`：要包含在设计中的资产 ID
- `width` / `height`：自定义的像素尺寸

**注意事项**：
- 设计类型必须与 Canva 的预定义类型完全匹配
- 自定义尺寸有最小和最大限制
- 需要先通过 `CANVA_CREATE_ASSET_UPLOAD_JOB` 上传资产，然后再使用该资产

### 3. 上传资产

**使用场景**：用户希望将图片或文件上传到 Canva 以用于设计中

**工具序列**：
1. `CANVA_CREATE_ASSET_UPLOAD_JOB` - 启动资产上传 [必填]
2. `CANVA FETCH_ASSET_UPLOAD_JOB_STATUS` - 监听上传进度直到完成 [必填]

**关键参数**：
- `name`：资产的显示名称
- `url`：要上传的文件的公共 URL
- `job_id`：第一步中返回的上传作业 ID（用于监控上传状态）

**注意事项**：
- 上传是异步的；必须持续监控上传状态直到完成
- 支持的格式包括 PNG、JPG、SVG、MP4、GIF
- 文件大小有限制；大文件可能需要更长时间处理
- `job_id` 是用于获取上传状态的唯一标识符
- 状态值包括 “in_progress”、“success”、“failed”

### 4. 导出设计

**使用场景**：用户希望将 Canva 设计下载为 PDF、PNG 或其他格式

**工具序列**：
1. `CANVA_LIST_USER_DESIGNS` - 找到要导出的设计 [前提条件]
2. `CANVA_CREATE_CANVA_DESIGN_EXPORT_JOB` - 启动导出过程 [必填]
3. `CANVA_GET_DESIGN_EXPORT_JOB_RESULT` | 监听导出进度直到完成并获取下载 URL [必填]

**关键参数**：
- `design_id`：要导出的设计的 ID
- `format`：导出格式（‘pdf’、‘png’、‘jpg’、‘svg’、‘mp4’、‘gif’、‘pptx’）
- `pages`：要导出的具体页码（数组）
- `quality`：导出质量（‘regular’、‘high’）
- `job_id`：用于监控导出状态的作业 ID

**注意事项**：
- 导出是异步的；必须持续监控导出进度直到完成
- 导出完成后，下载 URL 会在一定时间内失效
- 大型设计或页面较多的设计可能需要更长时间导出
- 并非所有格式都支持所有类型的设计（例如，MP4 仅适用于动画）
- 监控间隔：每次检查状态之间请等待 2-3 秒

### 5. 使用文件夹组织设计

**使用场景**：用户希望创建文件夹或将设计分类到文件夹中

**工具序列**：
1. `CANVA_POST_FOLDERS` - 创建新文件夹 [必填]
2. `CANVA_MOVE_ITEM_TO_SPECIFIED_FOLDER` - 将设计移动到指定的文件夹中 [可选]

**关键参数**：
- `name`：文件夹名称
- `parent_folder_id`：父文件夹 ID
- `item_id`：要移动的设计或资产的 ID
- `folder_id`：目标文件夹 ID

**注意事项**：
- 同一父文件夹内的文件夹名称必须唯一
- 移动项目后，它们的位置会立即更新
- 根文件夹没有 `parent_folder_id`

### 6. 从品牌模板中自动生成设计

**使用场景**：用户希望使用数据填充品牌模板中的占位符来生成设计

**工具序列**：
1. `CANVA_ACCESS_USER_SPECIFIC_BRAND_TEMPLATES_LIST` - 列出可用的品牌模板 [必填]
2. `CANVA_INITIATE_CANVA_DESIGN_AUTOFILL_JOB` - 使用数据开始自动生成设计 [必填]

**关键参数**：
- `brand_template_id`：要使用的品牌模板 ID
- `title`：生成设计的名称
- `data`：占位符名称与替换值的键值映射

**注意事项**：
- 模板中的占位符名称必须完全匹配（区分大小写）
- 自动填充是异步的；需要等待完成
- 仅品牌模板支持自动生成功能，普通设计不支持
- 数据值必须与每个占位符的预期类型相匹配（文本、图片 URL）

## 常见模式

### 异步操作模式

许多 Canva 操作都是异步的：
```
1. Initiate job (upload, export, autofill) -> get job_id
2. Poll status endpoint with job_id every 2-3 seconds
3. Check for 'success' or 'failed' status
4. On success, extract result (asset_id, download_url, design_id)
```

### ID 解析

- **设计名称 -> 设计 ID**：
```
1. Call CANVA_LIST_USER_DESIGNS with query=design_name
2. Find matching design in results
3. Extract id field
```

- **品牌模板名称 -> 模板 ID**：
```
1. Call CANVA_ACCESS_USER_SPECIFIC_BRAND_TEMPLATES_LIST
2. Find template by name
3. Extract brand_template_id
```

### 分页

- 在响应中查找 `continuation` 令牌
- 在下一次请求中将该令牌作为 `continuation` 参数传递
- 重复此过程直到 `continuation` 令牌不存在或为空

## 常见问题

- **异步操作**：
  - 上传、导出和自动生成操作都是异步的；请务必监控作业状态，不要假设操作会立即完成
- 导出文件的下载 URL 有有效期，请及时使用
- 资产必须先上传才能在设计中使用
- 上传作业必须达到 “success” 状态后，资产 ID 才有效
- 支持的格式可能有所不同；请查阅 Canva 的文档以了解当前的限制

**速率限制**：
- Canva API 对每个端点都有速率限制
- 对于批量操作，请实施指数退避策略
- 尽可能进行批量操作以减少 API 调用次数

**响应解析**：
- 响应数据可能嵌套在 `data` 键下
- 根据完成状态，作业状态响应中包含不同的字段
- 对于可选字段，采用防御性解析方式并设置默认值

## 快速参考

| 任务 | 工具名称 | 关键参数 |
|------|-----------|------------|
| 列出设计 | CANVA_LIST_USER_DESIGNS | query, continuation |
| 创建设计 | CANVA_CREATE_CANVA_DESIGN_WITH_OPTIONAL_ASSET | design_type, title |
| 上传资产 | CANVA_CREATE_ASSET_UPLOAD_JOB | name, url |
| 检查上传进度 | CANVA FETCH_ASSET_UPLOAD_JOB_STATUS | job_id |
| 导出设计 | CANVA_CREATE_CANVA_DESIGN_EXPORT_JOB | design_id, format |
| 获取导出结果 | CANVA_GET_DESIGN_EXPORT_JOB_RESULT | job_id |
| 创建文件夹 | CANVA_POST_FOLDERS | name, parent_folder_id |
| 将项目移动到文件夹 | CANVA_MOVE_ITEM_TO_SPECIFIED_FOLDER | item_id, folder_id |
| 列出模板 | CANVA_ACCESS_USER_SPECIFIC_BRAND_TEMPLATES_LIST | （无） |
| 从模板自动生成设计 | CANVA_INITIATE_CANVA_DESIGN_AUTOFILL_JOB | brand_template_id, data |