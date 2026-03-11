---
name: shopify-manager-cli
description: 通过 Shopify Admin 的 GraphQL API 管理 Shopify 商店中的产品、元字段（metafields）、元对象（metaobjects）、博客（blogs）和文章（articles）。这是一个纯官方的 Shopify API 封装层，无需使用任何第三方插件；它基于与 Shopify CLI 相同的 API 接口，让您能够完全控制商店功能而无需额外的依赖项。
user_invocable: true

metadata:
  {
    "openclaw":
      {
        "emoji": "🛍️",
        "requires": { "bins": ["python3"], "env": ["SHOPIFY_STORE_URL", "SHOPIFY_ACCESS_TOKEN", "SHOPIFY_API_VERSION"] },
        "primaryEnv": "SHOPIFY_ACCESS_TOKEN",
        "install": [],
      },
  }
---
# Shopify 商店管理工具

您可以通过运行 `python3 scripts/shopify_admin.py` 命令来帮助用户管理他们的 Shopify 商店。

## 先决条件

必须设置以下环境变量：
- `SHOPIFY_STORE_URL` — 例如：`https://my-store.myshopify.com`
- `SHOPIFY_ACCESS_TOKEN` — 管理员 API 访问令牌（格式为 `shpat_…`）
- `SHOPIFY_API_VERSION` — 可选，默认值为 `2025-01`

如果这些变量未设置，请提醒用户在继续之前先导出它们。

### 所需的管理员 API 访问权限

在 Shopify 管理后台的 **设置 → 应用程序 → 开发应用程序 → 配置** 中，必须为该自定义应用程序授予以下权限：

| 权限 | 使用权限的应用程序 |
|---|---|
| `read_products` / `write_products` | 查看/创建/更新/删除产品 |
| `read_metaobject_definitions` / `write_metaobject_definitions` | 定义元对象 |
| `read_metaobjects` / `write_metaobjects` | 查看/创建/更新/删除元对象 |
| `read_content` / `write_content` | 查看/创建/更新/删除博客文章 |
| `read_files` / `write_files` | 上传文件；通过分阶段上传 API 上传产品图片 |

## 使用方法

1. 从用户的指令中确定资源类型（产品、元字段、元对象、博客文章或文件）以及操作类型（查看、获取、创建、更新、删除、定义、设置或上传）。
2. 根据下面的命令参考将用户指令映射到具体的子命令和参数。当用户省略了可选参数（例如 `--status`、`--author`）时，使用文档中规定的默认值；除非缺少必需的参数，否则不要提示用户输入。
3. 当命令需要 `--image-file` 或本地文件路径时，直接传递该路径；脚本会从磁盘读取文件并通过 Shopify 的分阶段上传 API 进行上传，无需预先处理文件。
4. 使用 Bash 工具运行命令。
5. 以清晰易读的格式呈现输出结果（列表使用表格，详细信息使用 JSON）。
6. **对于删除操作**：在执行前务必确认用户的操作。

## 命令参考

### 产品

```bash
# List products (with optional search filter)
# Output columns: id  title  [status]  vendor  productType  $price  tags
python3 scripts/shopify_admin.py product list [--filter "status:active"] [--limit 20]

# Get product details
# Output includes: id, title, status, vendor, productType, tags, variants (id/title/price/sku), metafields
python3 scripts/shopify_admin.py product get <id>

# Create a product (defaults to DRAFT status)
python3 scripts/shopify_admin.py product create "<title>" [--description "<html>"] [--vendor "<name>"] [--tags tag1 tag2] [--image-url "https://..."] [--image-file "/path/to/a.jpg"] [--image-alt "Alt text"] [--status DRAFT|ACTIVE|ARCHIVED]

# Update a product (only specify fields to change)
python3 scripts/shopify_admin.py product update <id> [--title "..."] [--description "..."] [--vendor "..."] [--tags t1 t2] [--image-url "https://..."] [--image-file "/path/to/a.jpg"] [--image-alt "Alt text"] [--status ...]

# Delete a product (⚠️ irreversible — confirm first)
python3 scripts/shopify_admin.py product delete <id>
```

### 元字段

```bash
# List metafield definitions for a resource type
python3 scripts/shopify_admin.py metafield list <owner_type> [--limit 50]

# Create a metafield definition
python3 scripts/shopify_admin.py metafield define <owner_type> <key> <type> [--name "Display Name"] [--namespace ns] [--pin]

# Set a metafield value on a resource
python3 scripts/shopify_admin.py metafield set <OwnerType> <owner_id> <key> "<value>" [--type type] [--namespace ns]
```

所有者类型：`product`、`customer`、`order`、`shop`、`collection`、`productvariant`、`company`、`location` 等。

元字段类型：`single_line_text_field`、`multi_line_text_field`、`rich_text_field`、`number_integer`、`number_decimal`、`boolean`、`color`、`date`、`date_time`、`url`、`json`、`money`、`weight`、`volume`、`dimension`、`rating`、`product_reference`、`collection_reference`、`file_reference`、`metaobject_reference`、`list.*`

### 元对象

```bash
# Create a metaobject definition
# Field spec format: key:type[:name[:required]]
python3 scripts/shopify_admin.py metaobject define <type> <field_specs>... [--name "Display Name"] [--display-key <field_key>]

# Create/upsert a metaobject entry
# Field value format: key=value
python3 scripts/shopify_admin.py metaobject create <type> <handle> <key=value>...

# List metaobject entries
python3 scripts/shopify_admin.py metaobject list <type> [--limit 20]

# Update a metaobject entry
python3 scripts/shopify_admin.py metaobject update <id> <key=value>...

# Delete a metaobject entry (⚠️ confirm first)
python3 scripts/shopify_admin.py metaobject delete <id>
```

### 博客文章

```bash
# List blogs
python3 scripts/shopify_admin.py blog list [--limit 20]

# Create a blog
python3 scripts/shopify_admin.py blog create "<title>"
```

### 文件

```bash
# Upload a file to Shopify admin → Settings → Files
python3 scripts/shopify_admin.py file upload "/path/to/file.pdf" [--alt "Alt text"] [--filename "file.pdf"] [--content-type FILE|IMAGE|VIDEO|MODEL_3D] [--duplicate APPEND_UUID|RAISE_ERROR|REPLACE]
```

### 博客文章

```bash
# List articles (optionally filter by blog)
python3 scripts/shopify_admin.py article list [--blog <blog_id>] [--limit 20]

# Create an article (--author defaults to "Admin" if omitted)
python3 scripts/shopify_admin.py article create --blog <blog_id> "<title>" "<body_html>" [--author "Name"] [--tags t1 t2] [--publish]

# Create an article with author info
python3 scripts/shopify_admin.py article create --blog 123 "Trail Running Guide" "<p>Tips for trail running.</p>" --author "Jane Smith" --tags running trails --publish

# Update an article's author
python3 scripts/shopify_admin.py article update <id> --author "New Author Name"

# Update an article
python3 scripts/shopify_admin.py article update <id> [--title "..."] [--body "..."] [--author "Name"] [--tags t1 t2] [--publish|--unpublish]

# Publish / unpublish (set visibility)
python3 scripts/shopify_admin.py article update <id> --publish
python3 scripts/shopify_admin.py article update <id> --unpublish

# Delete an article (⚠️ confirm first)
python3 scripts/shopify_admin.py article delete <id>
```

#### 作者信息说明

- `--author` 参数用于设置文章中显示的作者名称（例如：“Jane Smith”）。
- 如果省略此参数，默认显示为 “Admin”。
- 在列出文章时，输出结果中已经包含 “by <author>` 列，因此无需额外显示作者信息。
- 作者信息以纯字符串形式存储，不链接到 Shopify 的员工账户。

## ID 格式

用户可以提供以下两种格式的 ID：
- 数字 ID：`123`
- 完整的 Shopify GID：`gid://shopify/Product/123`

脚本会自动识别并处理这两种格式的 ID。

## 自然语言指令与命令的对应关系示例

| 用户指令 | 对应命令 |
|---|---|
| “列出所有活跃的产品” | `product list --filter "status:active"` |
| “查看产品 123”的详细信息” | `product get 123` |
| “为 GeoStep 品牌创建一款登山靴产品” | `product create "Hiking Boots" --vendor GeoStep` |
| “为产品添加 ‘Care Guide’ 元字段” | `metafield define product care_guide single_line_text_field --name "Care Guide"` |
| “将产品 123 的 ‘Care Guide’ 设置为 ‘仅可手洗’” | `metafield set Product 123 care_guide "Hand wash only"` |
| “定义一个包含名称和简介的元对象” | `metaobject define designer name:single_line_text_field:Name bio:multi_line_text_field:Bio --display-key name` |
| “创建一个名为 ‘Company News’ 的博客文章” | `blog create "Company News"` |
| “在博客 456 中撰写一篇关于夏季徒步的文章” | `article create --blog 456 "Summer Hiking Guide" "<p>...</p>" --publish` |
| “在博客 456 中撰写一篇由 Jane Smith 撰写的文章” | `article create --blog 456 "Article Title" "<p>...</p>" --author "Jane Smith" --publish` |
| “将文章 789 的作者更改为 John Doe” | `article update 789 --author "John Doe"` |
| “列出博客 456 中的文章以查看作者信息” | `article list --blog 456` |