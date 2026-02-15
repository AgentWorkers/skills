---
name: box-automation
description: 通过 Rube MCP (Composio) 自动化 Box 云存储操作，包括文件上传/下载、搜索、文件夹管理、共享、协作以及元数据查询。在使用这些功能之前，请务必先使用相应的工具查询当前的数据库架构（schema）。
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Box 自动化

通过 Composio 的 Box 工具包，可以自动化执行 Box 的各种操作，包括文件上传/下载、内容搜索、文件夹管理、协作、元数据查询以及签名请求等。

## 先决条件

- 必须已连接 Rube MCP（支持 `RUBE_SEARCH_TOOLS` 功能）。
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `box` 工具包建立活跃的 Box 连接。
- 在执行任何工作流程之前，务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具架构信息。

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥，只需添加该端点即可。

1. 通过确认 `RUBE_SEARCH_TOOLS` 是否响应来验证 Rube MCP 是否可用。
2. 使用 `box` 工具包调用 `RUBE_MANAGE_CONNECTIONS`。
3. 如果连接未处于活跃状态，请按照返回的链接完成 Box 的 OAuth 认证。
4. 在运行任何工作流程之前，确保连接状态显示为“活跃”。

## 核心工作流程

### 1. 上传和下载文件

**使用场景**：用户需要将文件上传到 Box 或从 Box 下载文件。

**工具顺序**：
1. `BOX_SEARCH_FOR_CONTENT` - 如果路径未知，查找目标文件夹 [先决条件]
2. `BOX_GET_FOLDER_INFORMATION` - 验证文件夹是否存在并获取文件夹 ID [先决条件]
3. `BOX_LIST_ITEMS_IN_FOLDER` - 浏览文件夹内容并获取文件 ID [可选]
4. `BOX_UPLOAD_FILE` - 将文件上传到指定文件夹 [上传时必需]
5. `BOX_DOWNLOAD_FILE` - 根据文件 ID 下载文件 [下载时必需]
6. `BOX_CREATE_ZIP_DOWNLOAD` - 将多个文件/文件夹打包成 zip 文件 [可选]

**关键参数**：
- `parent_id`：上传目标的文件夹 ID（使用 `"0"` 表示根文件夹）
- `file`：包含 `s3key`、`mimetype` 和 `name` 的 `FileUploadable` 对象（用于上传）
- `file_id`：用于下载的唯一文件标识符
- `version`：用于下载特定版本的文件版本 ID（可选）
- `fields`：需要返回的属性列表（以逗号分隔）

**注意事项**：
- 上传到已存在文件名的文件夹可能会引发冲突；需决定是覆盖还是重命名文件。
- 超过 50MB 的文件应使用分块上传 API（标准工具不支持）。
- 上传时的 `attributes` 部分必须位于 `file` 部分之前，否则会收到 HTTP 400 错误（原因可能是 `metadata_after_file_contents`）。
- 文件 ID 和文件夹 ID 可以从 Box 网页 URL 中提取（例如：`https://*.app.box.com/files/123` 的文件 ID 为 `"123"`）。

### 2. 搜索和浏览内容

**使用场景**：用户需要根据文件名、内容或元数据查找文件、文件夹或网页链接。

**工具顺序**：
1. `BOX_SEARCH_FOR_CONTENT` - 对文件、文件夹和网页链接进行全文搜索 [必需]
2. `BOX_LIST_ITEMS_IN_FOLDER` - 浏览特定文件夹的内容 [可选]
3. `BOX_GET_FILE_information` - 获取特定文件的详细元数据 [可选]
4. `BOX_GET_FOLDER_information` - 获取特定文件夹的详细元数据 [可选]
5. `BOX_QUERY_FILES_FOLDERS_BY_METADATA` - 根据元数据模板值进行搜索 [可选]
6. `BOX_LIST_RECENTLY_ACCESSED_ITEMS` - 列出最近访问的文件/文件夹 [可选]

**关键参数**：
- `query`：搜索字符串，支持操作符（`""` 表示精确匹配，`AND`、`OR`、`NOT`——仅区分大小写）
- `type`：按 `"file"`、`folder` 或 `"web_link"` 进行过滤
- `ancestor_folder_ids`：限制搜索范围（以逗号分隔的文件夹 ID）
- `file_extensions`：按文件类型过滤（以逗号分隔，不包含点）
- `content_types`：搜索字段包括 `"name"`、`description`、`file_content`、`comments`、`tags`
- `created_at_range` / `updated_at_range`：日期过滤条件（以 RFC3339 格式的时间戳表示）
- `limit`：每页显示的结果数量（默认为 30 个）
- `offset`：分页偏移量（最大为 10000）
- `folder_id`：用于 `LIST_ITEMS_IN_FOLDER`（使用 `"0"` 表示根文件夹）

**注意事项**：
- 偏移量超过 10000 的查询会收到 HTTP 400 错误。
- `BOX_SEARCH_FOR_CONTENT` 必须提供 `query` 或 `mdfilters` 参数。
- 配置错误的过滤器可能会导致部分结果被忽略；建议先使用小规模测试查询进行验证。
- 布尔运算符（`AND`、`OR`、`NOT`）必须大写。
- `BOX_LIST_ITEMS_IN_FOLDER` 需要通过 `marker` 或 `offset`/`usemarker` 进行分页；通常会返回部分结果。
- 标准文件夹会先按类型排序（文件夹在前，文件和网页链接在后）。

### 3. 管理文件夹

**使用场景**：用户需要创建、更新、移动、复制或删除文件夹。

**工具顺序**：
1. `BOX_GET_FOLDER_information` - 验证文件夹是否存在并检查权限 [先决条件]
2. `BOX_CREATE_FOLDER` - 创建新文件夹 [创建时必需]
3. `BOX_UPDATE_FOLDER` - 重命名、移动或更新文件夹设置 [更新时必需]
4. `BOX_COPY_FOLDER` - 将文件夹复制到新位置 [可选]
5. `BOX_DELETE_FOLDER` - 将文件夹移动到回收站 [删除时必需]
6. `BOX_PERMANENTLY_REMOVE_FOLDER` - 永久删除回收站中的文件夹 [可选]

**关键参数**：
- `name`：文件夹名称（不能包含 `/`、`\`、尾随空格或 `.`/`..`）
- `parent__id`：父文件夹 ID（使用 `"0"` 表示根文件夹）
- `folder_id`：操作的目标文件夹 ID
- `parent.id`：通过 `BOX_UPDATE_FOLDER` 移动文件夹时的目标文件夹 ID
- `recursive`：设置为 `true` 以删除非空文件夹
- `shared_link`：包含 `access`、`password`、`permissions` 的对象，用于创建共享链接
- `description`、`tags`：可选的元数据字段

**注意事项**：
- `BOX_DELETE_FOLDER` 默认会将文件夹移动到回收站；如需永久删除，请使用 `BOX_PERMANENTLY_REMOVE_FOLDER`。
- 非空文件夹删除时必须设置 `recursive: true`。
- 根文件夹（ID 为 `"0"`）不能被复制或删除。
- 文件夹名称不能包含 `/`、`\`、不可打印的 ASCII 字符或尾随空格。
- 移动文件夹时需要通过 `BOX_UPDATE_FOLDER` 设置 `parent.id`。

### 4. 共享文件和管理协作

**使用场景**：用户需要共享文件、管理访问权限或处理协作事宜。

**工具顺序**：
1. `BOX_GET_FILE_information` - 获取文件详细信息和当前的共享状态 [先决条件]
2. `BOX_LIST_FILE_COLLABORATIONS` - 列出文件的访问者 [必需]
3. `BOX_UPDATE_COLLABORATION` - 更改访问权限或接受/拒绝邀请 [必需]
4. `BOX_GET_COLLABORATION` - 获取特定协作的详细信息 [可选]
5. `BOX_UPDATE_FILE` - 创建共享链接、锁定文件或更新权限 [可选]
6. `BOX_UPDATE_FOLDER` - 在文件夹上创建共享链接 [可选]

**关键参数**：
- `collaboration_id`：唯一的协作标识符
- `role`：访问权限（`"editor"`、`"viewer"`、`"co-owner"`、`"owner"`、`"previewer"`、`"uploader"`、`"viewer uploader"`、`"previewer uploader"`）
- `status`：协作邀请的状态（`"accepted"`、`pending"` 或 `"rejected"`）
- `file_id`：要共享或管理的文件
- `lock__access`：设置为 `"lock"` 以锁定文件
- `permissions__can__download`：指定下载权限（`"company"` 或 `"open"`）

**注意事项**：
- 只有特定角色才能邀请协作者；权限不足会导致授权错误。
- `can_view_path` 会增加接收者“所有文件”页面的加载时间；每个用户最多只能邀请 1000 个文件。
- 协作关系的过期需要企业管理员进行配置。
- 嵌套参数名称使用双下划线（例如：`lock__access`、`parent__id`）。

### 5. Box 签名请求

**使用场景**：用户需要管理文档签名请求。

**工具顺序**：
1. `BOX_LIST_BOX_SIGN_REQUESTS` - 列出所有签名请求 [必需]
2. `BOX_GET_BOX_SIGN_REQUEST_BY_ID` - 获取特定签名请求的详细信息 [可选]
3. `BOX_CANCEL_BOX_SIGN_REQUEST` - 取消待处理的签名请求 [可选]

**关键参数**：
- `sign_request_id`：签名请求的 UUID
- `shared_requests`：设置为 `true` 以包含用户为协作者的请求（非所有者）
- `senders`：按发送者邮箱过滤（需要 `shared_requests: true`）
- `limit` / `marker`：分页参数

**注意事项**：
- 企业账户必须启用 Box Sign 功能才能使用此功能。
- 被删除的签名文件或父文件夹会导致请求不在列表中显示。
- 只有创建者可以取消签名请求。
- 签名请求的状态包括：`converting`、`created`、`sent`、`viewed`、`signed`、`declined`、`cancelled`、`expired`、`error_converting`、`error_sending`。

## 常见模式

### ID 解析
Box 使用数字字符串作为所有实体的标识符：
- **根文件夹**：ID 始终为 `"0"`。
- **从 URL 中获取的文件 ID**：`https://*.app.box.com/files/123` 的文件 ID 为 `"123"`。
- **从 URL 中获取的文件夹 ID**：`https://*.app.box.com/folder/123` 的文件夹 ID 为 `"123"`。
- **通过 ID 搜索**：使用 `BOX_SEARCH_FOR_CONTENT` 查找文件，然后从结果中提取 ID。
- **ETag**：使用 `if_match` 和文件的 ETag 来确保并发删除操作的安全性。

### 分页
Box 支持两种分页方式：
- **基于偏移量的分页**：使用 `offset` + `limit`（最大偏移量为 10000）。
- **基于标记的分页**：设置 `usemarker: true` 并根据响应中的 `marker` 进行分页（适用于大数据集）。
- 为避免部分结果，请确保分页完成。

### 嵌套参数
Box 工具使用双下划线表示嵌套对象：
- `parent__id`：用于引用父文件夹
- `lock__access`、`lock__expires__at`、`lock__is__download__prevented`：用于文件锁定
- `permissions__can__download`：用于指定下载权限

## 已知问题

### ID 格式
- 所有 ID 都是数字字符串（例如：`123456`，而非整数）。
- 根文件夹的 ID 始终为 `"0"`。
- 文件和文件夹 ID 可以从 Box 网页 URL 中提取。

### 速率限制
Box API 对每个端点都有速率限制。
- 搜索和列表操作应合理使用分页功能。
- 批量操作之间应适当延迟请求。

### 参数注意事项
- `fields` 参数会改变响应格式：指定该参数后，仅返回所需字段的简略信息。
- 搜索操作必须提供 `query` 或 `mdfilters` 中的一个；两者都不能省略。
- 使用 `BOX_UPDATE_FILE` 且 `lock` 设置为 `null` 会取消文件锁定（仅适用于原始 API）。
- 元数据查询的 `from` 字段格式为 `enterprise_{enterprise_id}.templateKey` 或 `global.templateKey`。

### 权限
- 没有足够的权限会导致删除操作失败；务必处理错误响应。
- 协作角色决定了允许的操作类型。
- 企业设置可能会限制某些共享选项。

## 快速参考

| 任务 | 工具名称 | 关键参数 |
|------|-----------|------------|
| 搜索内容 | `BOX_SEARCH_FOR_CONTENT` | `query`, `type`, `ancestor_folder_ids` |
| 列出文件夹内容 | `BOX_LIST_ITEMS_IN_FOLDER` | `folder_id`, `limit`, `marker` |
| 获取文件信息 | `BOX_GET_FILE_INFORMATION` | `file_id`, `fields` |
| 获取文件夹信息 | `BOX_GET_FOLDER_information` | `folder_id`, `fields` |
| 上传文件 | `BOX_UPLOAD_FILE` | `file`, `parent_id` |
| 下载文件 | `BOX_DOWNLOAD_FILE` | `file_id` |
| 创建文件夹 | `BOX_CREATE_FOLDER` | `name`, `parent__id` |
| 更新文件夹 | `BOX_UPDATE_FOLDER` | `folder_id`, `name`, `parent` |
| 复制文件夹 | `BOX_COPY_FOLDER` | `folder_id`, `parent__id` |
| 删除文件夹 | `BOX_DELETE_FOLDER` | `folder_id`, `recursive` |
| 永久删除文件夹 | `BOX_PERMANENTLY_REMOVE_FOLDER` | folder_id` |
| 更新文件 | `BOX_UPDATE_FILE` | `file_id`, `name`, `parent__id` |
| 删除文件 | `BOX_DELETE_FILE` | `file_id`, `if_match` |
| 列出协作关系 | `BOX_LIST_FILE_COLLABORATIONS` | `file_id` |
| 更新协作关系 | `BOX_UPDATE_COLLABORATION` | `collaboration_id`, `role` |
| 获取协作关系信息 | `BOX_GET_COLLABORATION` | `collaboration_id` |
| 根据元数据查询 | `BOX_QUERY_FILES_FOLDERS_BY_METADATA` | `from`, `ancestor_folder_id`, `query` |
| 列出集合 | `BOX_LIST_ALL COLLECTIONS` | （无） |
| 列出集合项目 | `BOX_LIST_collection_ITEMS` | `collection_id` |
| 列出签名请求 | `BOX_LIST_BOX_SIGN_REQUESTS` | `limit`, `marker` |
| 获取签名请求信息 | `BOX_GET_BOX_SIGN_REQUEST_BY_ID` | `sign_request_id` |
| 取消签名请求 | `BOX_CANCEL_BOX_SIGN_REQUEST` | `sign_request_id` |
| 最近访问的项目 | `BOX_LIST_RECENTLY_ACCESSED_ITEMS` | （无） |
| 创建 zip 下载 | `BOX_CREATE_ZIP_DOWNLOAD` | 文件 ID |