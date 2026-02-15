**notion-cli**  
通过 `notion-cli` 与您的 Notion 工作区进行交互。  
这是一个针对 Notion API 的生产级命令行工具（CLI），支持搜索、创建和管理页面、数据库、内容块（blocks）、用户以及评论，并提供多种输出格式（JSON、表格、CSV）。  

**安装方法**  
克隆并安装该 CLI：  
```
git clone https://github.com/FroeMic/notion-cli
cd notion-cli
npm install
npm run build
npm link
```  

**设置 `NOTION_API_KEY` 环境变量**：  
1. 在 [https://www.notion.so/profile/integrations](https://www.notion.so/profile/integrations) 创建一个集成（integration）。  
2. 复制内部集成密钥（以 `ntn_` 或 `secret_` 开头）。  
3. 将您希望访问的页面/数据库共享给该集成：  
  - 推荐：将其添加到 `~/.claude/.env` 文件中（适用于 Claude 代码）。  
  - 或者：将其添加到 `~/.bashrc` 或 `~/.zshrc` 文件中：`export NOTION_API_KEY="your-api-key"`。  

**可选设置**：  
设置 `NOTION_DEBUG=true` 以启用详细的请求/响应日志记录。  

**仓库地址**：[https://github.com/FroeMic/notion-cli](https://github.com/FroeMic/notion-cli)  

**常用命令**  
- 在工作区内搜索：  
```
notion search [query]                                  # Search pages, databases, and data sources
notion search [query] --filter page                    # Search only pages
notion search [query] --filter database                # Search only databases
notion search [query] --sort ascending                 # Sort by last edited time
```  
- 操作页面：  
```
notion pages get <page-id>                             # Get page details
notion pages create --parent <id> --title <text>       # Create a new page
notion pages update <page-id> --properties <json>      # Update page properties
notion pages archive <page-id>                         # Archive a page
notion pages restore <page-id>                         # Restore an archived page
notion pages property <page-id> <property-id>          # Get a specific property value
```  
- 操作数据库：  
```
notion databases get <database-id>                     # Get database schema
notion databases create --parent <id> --title <text>   # Create a database
notion databases update <database-id> --title <text>   # Update database metadata
notion databases query <data-source-id>                # Query records in a data source
notion databases query <id> --filter <json>            # Query with filters
notion databases query <id> --sort <json>              # Query with sorting
```  
- 操作内容块：  
```
notion blocks get <block-id>                           # Get a block
notion blocks children <block-id>                      # List child blocks
notion blocks append <block-id> --content <json>       # Append new blocks
notion blocks update <block-id> --content <json>       # Update a block
notion blocks delete <block-id>                        # Delete a block
```  
- 操作用户：  
```
notion users list                                      # List workspace members
notion users get <user-id>                             # Get user details
notion users me                                        # Get the authenticated bot user
```  
- 操作评论：  
```
notion comments list --block <block-id>                # List comments on a block
notion comments create --page <page-id> --content <text>  # Add a comment to a page
```  

**全局选项**  
（所有命令均支持以下全局选项）：  
```
--api-key <key>                                        # Override NOTION_API_KEY env var
-f, --format <fmt>                                     # Output format: json (default), table, csv
--limit <n>                                            # Max results to return
--cursor <cursor>                                      # Pagination cursor
```  

**关键概念**  
| 概念          | 用途                                      | 示例                                      |  
|----------------|-----------------------------------------|-----------------------------------------|  
| 页面（Pages）      | 单个 Notion 页面                          | 会议记录、项目概要                              |  
| 数据库（Databases）  | 结构化的页面集合                          | 任务跟踪器、客户关系管理（CRM）表格                |  
| 数据源（Data Sources）| 数据库中的单个表格                          | 数据库中的特定视图/表格                         |  
| 内容块（Blocks）    | 页面中的内容元素                          | 段落、标题、列表、代码块                         |  
| 属性（Properties）    | 数据库页面上的可输入字段                        | 标题、状态、日期、选择项、关联关系                   |  
| 用户（Users）      | 工作区成员及集成工具                          | 团队成员、机器人集成工具                          |  
| 评论（Comments）    | 页面/内容块上的讨论线程                          | 反馈信息、审阅备注                          |  

**API 参考**  
- 基本 URL：`https://api.notion.com/v1`  
- API 版本：`2022-06-28`  
- 认证方式：`Authorization: Bearer $NOTION_API_KEY`  
- 速率限制：自动重试（采用指数退避策略，最多重试 3 次）  

**常见 API 操作**  
- 搜索页面：  
```
curl -X POST https://api.notion.com/v1/search \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"query": "Meeting Notes", "filter": {"value": "page", "property": "object"}}'
```  
- 使用过滤器查询数据库：  
```
curl -X POST https://api.notion.com/v1/databases/<database-id>/query \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"property": "Status", "status": {"equals": "In Progress"}}}'
```  
- 在数据库中创建页面：  
```
curl -X POST https://api.notion.com/v1/pages \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"parent": {"database_id": "<database-id>"}, "properties": {"Name": {"title": [{"text": {"content": "New Task"}}]}}}'
```  
- 向页面添加内容：  
```
curl -X PATCH https://api.notion.com/v1/blocks/<block-id>/children \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"children": [{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Hello world"}}]}}]}'
```  

**注意事项**  
- 必须通过 Notion 的用户界面（菜单 > “连接” > “添加集成”）明确共享您想要访问的每个页面或数据库。  
- 页面的 ID 可以是 UUID 或 Notion 的 URL 格式——CLI 会自动解析这两种格式。  
- 所有列表相关的 API 都支持通过 `--limit` 和 `--cursor` 参数进行基于游标的分页。  
- 输出格式可以通过 `-f` 标志设置为 `json`（默认）、`table` 或 `csv`。  
- 属性类型包括：`title`（标题）、`rich_text`（富文本）、`number`（数字）、`select`（选择项）、`multi_select`（多选）、`status`（状态）、`date`（日期）、`people`（人员信息）、`files`（文件）、`checkbox`（复选框）、`url`（URL）、`email`（电子邮件）、`phone_number`（电话号码）、`relation`（关联关系）、`rollup`（汇总数据）、`formula`（公式）和 `timestamp`（时间戳）。  

**文件列表**  
- 共 1 个文件：`SKILL.md`