---
name: baserow
description: >
  **Baserow API集成与受管理的API密钥认证**  
  支持对数据库中的行、字段和表进行管理。  
  当用户需要读取、创建、更新或删除Baserow数据库中的数据，或使用过滤条件查询数据时，可使用此功能。  
  对于其他第三方应用程序，请使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Baserow

您可以使用管理的API密钥进行身份验证来访问Baserow API。通过完整的CRUD操作（创建、读取、更新、删除）来管理数据库中的行，同时支持过滤、排序和批量操作。

## 快速入门

```bash
# List rows from a table
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/baserow/api/database/rows/table/{table_id}/?user_field_names=true')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/baserow/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的Baserow API端点路径。该网关会将请求代理到 `api.baserow.io` 并自动插入您的API令牌。

## 身份验证

所有请求都需要在 `Authorization` 头部包含Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 管理您的Baserow API密钥连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=baserow&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'baserow'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "90a5d047-b856-4577-ac05-faccaabf8989",
    "status": "ACTIVE",
    "creation_time": "2026-03-02T12:01:29.812801Z",
    "last_updated_time": "2026-03-02T12:02:17.932675Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "baserow",
    "metadata": {},
    "method": "API_KEY"
  }
}
```

在浏览器中打开返回的 `url`，以输入您的Baserow数据库令牌。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个Baserow连接，请使用 `Maton-Connection` 头部指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/baserow/api/database/rows/table/123/')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '90a5d047-b856-4577-ac05-faccaabf8989')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略，则网关将使用默认的（最旧的）活动连接。

## API参考

### 行

#### 列出行

```bash
GET /baserow/api/database/rows/table/{table_id}/
```

查询参数：
- `user_field_names=true` - 使用人类可读的字段名称，而不是 `field_123` 这样的ID
- `size` - 每页的行数（默认：100）
- `page` - 页码（从1开始计数）
- `order_by` - 排序的字段名称（以 `-` 为前缀表示降序）
- `filter__{field}__{operator}` - 过滤行（请参阅过滤部分）
- `search` - 在所有字段中搜索
- `include` - 用逗号分隔的字段名称（包含的字段）
- `exclude` - 用逗号分隔的字段名称（排除的字段）

**响应：**
```json
{
  "count": 5,
  "next": "http://api.baserow.io/api/database/rows/table/123/?page=2&size=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "order": "1.00000000000000000000",
      "Assignee Name": "Alice Johnson",
      "Email": "alice.johnson@example.com",
      "Tasks": []
    }
  ]
}
```

#### 获取行

```bash
GET /baserow/api/database/rows/table/{table_id}/{row_id}/
```

**响应：**
```json
{
  "id": 1,
  "order": "1.00000000000000000000",
  "field_7456198": "Alice Johnson",
  "field_7456201": "alice.johnson@example.com",
  "field_7456215": []
}
```

#### 创建行

```bash
POST /baserow/api/database/rows/table/{table_id}/
Content-Type: application/json

{
  "field_7456198": "New User",
  "field_7456201": "newuser@example.com"
}
```

或者使用人类可读的字段名称：

```bash
POST /baserow/api/database/rows/table/{table_id}/?user_field_names=true
Content-Type: application/json

{
  "Assignee Name": "New User",
  "Email": "newuser@example.com"
}
```

**响应：**
```json
{
  "id": 6,
  "order": "6.00000000000000000000",
  "field_7456198": "New User",
  "field_7456201": "newuser@example.com",
  "field_7456215": []
}
```

#### 更新行

```bash
PATCH /baserow/api/database/rows/table/{table_id}/{row_id}/
Content-Type: application/json

{
  "field_7456198": "Updated Name"
}
```

**响应：**
```json
{
  "id": 1,
  "order": "1.00000000000000000000",
  "field_7456198": "Updated Name",
  "field_7456201": "alice.johnson@example.com",
  "field_7456215": []
}
```

#### 删除行

```bash
DELETE /baserow/api/database/rows/table/{table_id}/{row_id}/
```

成功时返回HTTP 204 No Content。

---

### 批量操作

#### 批量创建行

```bash
POST /baserow/api/database/rows/table/{table_id}/batch/
Content-Type: application/json

{
  "items": [
    {"field_7456198": "User 1", "field_7456201": "user1@example.com"},
    {"field_7456198": "User 2", "field_7456201": "user2@example.com"}
  ]
}
```

**响应：**
```json
{
  "items": [
    {"id": 7, "order": "7.00000000000000000000", "field_7456198": "User 1", ...},
    {"id": 8, "order": "8.00000000000000000000", "field_7456198": "User 2", ...}
  ]
}
```

#### 批量更新行

```bash
PATCH /baserow/api/database/rows/table/{table_id}/batch/
Content-Type: application/json

{
  "items": [
    {"id": 7, "field_7456198": "Updated User 1"},
    {"id": 8, "field_7456198": "Updated User 2"}
  ]
}
```

**响应：**
```json
{
  "items": [
    {"id": 7, "order": "7.00000000000000000000", "field_7456198": "Updated User 1", ...},
    {"id": 8, "order": "8.00000000000000000000", "field_7456198": "Updated User 2", ...}
  ]
}
```

#### 批量删除行

```bash
POST /baserow/api/database/rows/table/{table_id}/batch-delete/
Content-Type: application/json

{
  "items": [7, 8]
}
```

成功时返回HTTP 204 No Content。

---

### 字段

#### 列出字段

```bash
GET /baserow/api/database/fields/table/{table_id}/
```

**响应：**
```json
[
  {
    "id": 7456198,
    "table_id": 863922,
    "name": "Assignee Name",
    "order": 0,
    "type": "text",
    "primary": true,
    "read_only": false,
    "description": null
  },
  {
    "id": 7456201,
    "table_id": 863922,
    "name": "Email",
    "order": 1,
    "type": "text",
    "primary": false
  }
]
```

---

### 表

#### 列出所有表

获取您的令牌可以访问的所有表。

```bash
GET /baserow/api/database/tables/all-tables/
```

**响应：**
```json
[
  {
    "id": 863922,
    "name": "Assignees",
    "order": 0,
    "database_id": 419329
  },
  {
    "id": 863923,
    "name": "Tasks",
    "order": 1,
    "database_id": 419329
  }
]
```

---

### 移动行

在表内重新定位一行。

```bash
PATCH /baserow/api/database/rows/table/{table_id}/{row_id}/move/
```

查询参数：
- `before_id` - 要移动到的行的ID（如果省略，则移动到行尾）

**示例 - 将行移动到第3行之前：**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request(
    'https://gateway.maton.ai/baserow/api/database/rows/table/863922/5/move/?before_id=3',
    method='PATCH'
)
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "id": 5,
  "order": "2.50000000000000000000",
  "field_7456198": "Moved User",
  "field_7456201": "moved@example.com"
}
```

---

### 文件上传

#### 通过URL上传文件

从公共可访问的URL上传文件。

```bash
POST /baserow/api/user-files/upload-via-url/
Content-Type: application/json

{
  "url": "https://example.com/image.png"
}
```

**示例：**
```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'url': 'https://httpbin.org/image/png'}).encode()
req = urllib.request.Request(
    'https://gateway.maton.ai/baserow/api/user-files/upload-via-url/',
    data=data,
    method='POST'
)
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "url": "https://files.baserow.io/user_files/...",
  "thumbnails": {
    "tiny": {"url": "...", "width": 21, "height": 21},
    "small": {"url": "...", "width": 48, "height": 48},
    "card_cover": {"url": "...", "width": 300, "height": 160}
  },
  "visible_name": "image.png",
  "name": "abc123_image.png",
  "size": 8090,
  "mime_type": "image/png",
  "is_image": true,
  "image_width": 100,
  "image_height": 100,
  "uploaded_at": "2026-03-02T12:00:00Z"
}
```

#### 使用multipart形式上传文件

直接使用multipart表单数据上传文件。

```bash
POST /baserow/api/user-files/upload-file/
Content-Type: multipart/form-data
```

**示例：**
```bash
curl -X POST "https://gateway.maton.ai/baserow/api/user-files/upload-file/" \
  -H "Authorization: Bearer $MATON_API_KEY" \
  -F "file=@/path/to/file.pdf"
```

**响应：** 与通过URL上传的格式相同。

#### 在行中使用上传的文件

上传后，可以在文件字段中使用该文件对象：

```bash
POST /baserow/api/database/rows/table/{table_id}/?user_field_names=true
Content-Type: application/json

{
  "Attachment": [{"name": "abc123_image.png"}]
}
```

---

## 过滤

使用过滤参数来查询行：

```
filter__{field}__{operator}={value}
```

当 `user_field_names=true` 时：
```bash
GET /baserow/api/database/rows/table/{table_id}/?user_field_names=true&filter__Assignee+Name__contains=Alice
```

多个过滤器默认使用AND逻辑。使用 `filter_type=OR` 可以改为OR逻辑。

### 过滤操作符

#### 文本过滤器
| 操作符 | 描述 |
|----------|-------------|
| `equal` | 完全匹配 |
| `not_equal` | 不等于 |
| `contains` | 包含子字符串 |
| `contains_not` | 不包含子字符串 |
| `contains_word` | 包含整个单词 |
| `doesnt_contain_word` | 不包含整个单词 |
| `length_is_lower_than` | 文本长度小于指定值 |

#### 数值过滤器
| 操作符 | 描述 |
|----------|-------------|
| `higher_than` | 大于 |
| `higher_than_or_equal` | 大于或等于 |
| `lower_than` | 小于 |
| `lower_than_or_equal` | 小于或等于 |
| `is_even_and_whole` | 值是偶数且为整数 |

#### 日期过滤器
| 操作符 | 描述 |
|----------|-------------|
| `date_is` | 日期等于（需指定时区） |
| `date_is_not` | 日期不等于 |
| `date_is_before` | 日期在...之前 |
| `date_is_on_or_before` | 日期在...之前或当天 |
| `date_is_after` | 日期在...之后 |
| `date_is_on_or_after` | 日期在...之后或当天 |
| `date_is_within` | 日期在指定时间段内 |
| `date_equal` | 日期等于（旧格式） |
| `date_not_equal` | 日期不等于（旧格式） |
| `date_equals_today` | 日期是今天 |
| `date_before_today` | 日期在今天之前 |
| `date_after_today` | 日期在今天之后 |
| `date_within_days` | 日期在X天内 |
| `date_within_weeks` | 日期在X周内 |
| `date_within_months` | 日期在X个月内 |
| `date_equals_days_ago` | 日期在X天前 |
| `date_equals_weeks_ago` | 日期在X周前 |
| `date_equals_months_ago` | 日期在X个月前 |
| `date_equals_years_ago` | 日期在X年前 |
| `date_equals_day_of_month` | 日期等于月份中的特定日期 |
| `date_before_or_equal` | 日期在...之前或等于（旧格式） |
| `date_after_or_equal` | 日期在...之后或等于（旧格式） |

#### 布尔过滤器
| 操作符 | 描述 |
|----------|-------------|
| `boolean` | 布尔值等于（true/false） |

#### 链接行过滤器
| 操作符 | 描述 |
|----------|-------------|
| `link_row_has` | 与指定ID有链接的行 |
| `link_row_has_not` | 没有与指定ID有链接的行 |
| `link_row_contains` | 链接行包含指定文本 |
| `link_row_not_contains` | 链接行不包含指定文本 |

#### 单选过滤器
| 操作符 | 描述 |
|----------|-------------|
| `single_select_equal` | 单选等于指定选项ID |
| `single_select_not_equal` | 单选不等于指定选项ID |
| `single_select_is_any_of` | 单选是任意一个选项ID |
| `single_select_is_none_of` | 单选不是任何选项ID |

#### 多选过滤器
| 操作符 | 描述 |
|----------|-------------|
| `multiple_select_has` | 选择了某些选项 |
| `multiple_select_has_not` | 未选择任何选项 |
| `multiple_select_is_exactly` | 精确选择了这些选项 |

#### 协作者过滤器
| 操作符 | 描述 |
|----------|-------------|
| `multiple_collaborators_has` | 有协作者 |
| `multiple_collaborators_has_not` | 没有协作者 |

#### 文件过滤器
| 操作符 | 描述 |
|----------|-------------|
| `filename_contains` | 文件名包含指定内容 |
| `has_file_type` | 文件类型为指定类型（如图片、文档） |
| `files_lower_than` | 文件数量小于指定数量 |

#### 空/非空过滤器
| 操作符 | 描述 |
|----------|-------------|
| `empty` | 字段为空（值为`true`） |
| `not_empty` | 字段不为空（值为`true` |

#### 用户过滤器
| 操作符 | 描述 |
|----------|-------------|
| `user_is` | 用户字段等于指定用户ID |
| `user_is_not` | 用户字段不等于指定用户ID |

### 过滤示例

**文本包含：**
```bash
GET /baserow/api/database/rows/table/{table_id}/?user_field_names=true&filter__Name__contains=John
```

**日期在过去的7天内：**
```bash
GET /baserow/api/database/rows/table/{table_id}/?user_field_names=true&filter__Created__date_within_days=7
```

**多个过滤器（AND）：**
```bash
GET /baserow/api/database/rows/table/{table_id}/?user_field_names=true&filter__Status__single_select_equal=1&filter__Priority__higher_than=3
```

**多个过滤器（OR）：**
```bash
GET /baserow/api/database/rows/table/{table_id}/?user_field_names=true&filter_type=OR&filter__Status__equal=Active&filter__Status__equal=Pending
```

## 排序

使用 `order_by` 参数：

```bash
# Sort ascending by field name
GET /baserow/api/database/rows/table/{table_id}/?user_field_names=true&order_by=Assignee+Name

# Sort descending (prefix with -)
GET /baserow/api/database/rows/table/{table_id}/?user_field_names=true&order_by=-Assignee+Name
```

## 分页

使用 `size` 和 `page` 参数：

```bash
GET /baserow/api/database/rows/table/{table_id}/?size=25&page=2
```

响应中包含 `next` 和 `previous` URL：

```json
{
  "count": 100,
  "next": "http://api.baserow.io/api/database/rows/table/123/?page=3&size=25",
  "previous": "http://api.baserow.io/api/database/rows/table/123/?page=1&size=25",
  "results": [...]
}
```

## 代码示例

### JavaScript

```javascript
// List rows with user field names
const response = await fetch(
  'https://gateway.maton.ai/baserow/api/database/rows/table/863922/?user_field_names=true',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
console.log(data.results);
```

### Python

```python
import os
import requests

# Create a row
response = requests.post(
    'https://gateway.maton.ai/baserow/api/database/rows/table/863922/?user_field_names=true',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'Assignee Name': 'New User',
        'Email': 'newuser@example.com'
    }
)
row = response.json()
print(f"Created row ID: {row['id']}")
```

## 注意事项

- 连接使用API_KEY进行身份验证（数据库令牌），而不是OAuth
- 默认情况下，字段以 `field_{id}` 的格式返回；使用 `user_field_names=true` 可以获得人类可读的字段名称
- 行ID是整数（不是Airtable的 `recXXX` 格式）
- 表ID可以在Baserow UI或API文档中找到
- 数据库令牌仅允许访问数据库行端点，不允许访问管理端点
- 云版本同时支持的API请求数量有限（10个）

## 错误处理

| 状态 | 名称 | 描述 |
|--------|------|-------------|
| 200 | 成功 | 请求完成 |
| 204 | 无内容 | 操作成功（针对DELETE操作） |
| 400 | 错误请求 | 请求包含无效值或JSON无法解析 |
| 401 | 未经授权 | 数据库令牌无效或缺失 |
| 404 | 未找到 | 行或表未找到 |
| 413 | 请求实体过大 | 请求超过了允许的最大负载大小 |
| 429 | 请求过多 | 限制了并发请求数量（云版本为10个）
| 500 | 内部服务器错误 | 服务器遇到意外情况 |
| 502 | 网关错误 | Baserow正在重启或发生意外中断 |
| 503 | 服务不可用 | 服务器无法及时处理您的请求 |

### 故障排除：API密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称无效

确保您的URL路径以 `baserow` 开头。例如：

- 正确：`https://gateway.maton.ai/baserow/api/database/rows/table/{table_id}/`
- 错误：`https://gateway.maton.ai/api/database/rows/table/{table_id}/`

## 资源

- [Baserow API文档](https://baserow.io/api-docs)
- [Baserow数据库API](https://baserow.io/user-docs/database-api)
- [Baserow API规范（OpenAPI）](https://api.baserow.io/api/redoc/)
- [数据库令牌](https://baserow.io/user-docs/personal-api-tokens)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)