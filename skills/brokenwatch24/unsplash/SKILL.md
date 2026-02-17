# Unsplash API

您可以通过Unsplash API搜索、浏览并下载其海量免费图片库中的高质量图片。

## 设置与认证

### 获取访问密钥
1. 在 https://unsplash.com/developers 注册账户。
2. 注册一个新的应用程序。
3. 复制您的 **访问密钥**（密钥以您的应用程序名称开头）。

### 存储凭据
```bash
mkdir -p ~/.config/unsplash
echo "YOUR_ACCESS_KEY" > ~/.config/unsplash/access_key
chmod 600 ~/.config/unsplash/access_key
```

或者，您可以通过设置环境变量来存储凭据：
```bash
export UNSPLASH_ACCESS_KEY="your_access_key_here"
```

### 速率限制
- **演示模式**：每小时50次请求
- **生产模式**：每小时5,000次请求（应用程序获得批准后）
- 仅 `/v1/messages` 端点计入请求次数；图片URL（`images.unsplash.com`）不计入请求次数

## 常见操作

### 搜索图片
```bash
curl "https://api.unsplash.com/search/photos?query=nature&per_page=10" \
  -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}"
```

**参数：**
- `query`：搜索关键词（必填）
- `page`：页码（默认值：1）
- `per_page`：每页显示的结果数量（默认值：10，最大值：30）
- `order_by`：排序方式（默认值：`relevant` 或 `latest`）
- `color`：按颜色过滤（`black_and_white`、`black`、`white`、`yellow`、`orange`、`red`、`purple`、`magenta`、`green`、`teal`、`blue`）
- `orientation`：图片方向（`landscape`、`portrait` 或 `squarish`）

### 获取随机图片
```bash
curl "https://api.unsplash.com/photos/random?query=coffee&count=1" \
  -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}"
```

**参数：**
- `query`：可选的搜索关键词
- `count`：所需图片数量（1-30张，默认值：1）
- `orientation`：图片方向
- `collections`：按集合ID过滤（用逗号分隔）

### 获取图片详情
```bash
curl "https://api.unsplash.com/photos/PHOTO_ID" \
  -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}"
```

返回完整的图片元数据，包括EXIF信息、位置、用户信息以及所有图片URL。

### 下载跟踪（必填！）
**重要提示：** 下载图片时必须触发此接口，以遵守API使用规范。
```bash
curl "https://api.unsplash.com/photos/PHOTO_ID/download" \
  -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}"
```

此操作会更新下载计数器。响应中包含下载URL。

### 列出编辑内容
```bash
curl "https://api.unsplash.com/photos?per_page=10" \
  -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}"
```

### 浏览图片集合
```bash
# List all collections
curl "https://api.unsplash.com/collections?per_page=10" \
  -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}"

# Get collection photos
curl "https://api.unsplash.com/collections/COLLECTION_ID/photos" \
  -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}"
```

### 用户图片
```bash
curl "https://api.unsplash.com/users/USERNAME/photos?per_page=10" \
  -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}"
```

## 图片处理

### 图片URL
每张图片的响应中都包含以下URL：
```json
{
  "urls": {
    "raw": "https://images.unsplash.com/photo-xxx?ixid=xxx",
    "full": "...?ixid=xxx&q=80&fm=jpg",
    "regular": "...?ixid=xxx&w=1080&fit=max",
    "small": "...?w=400&fit=max",
    "thumb": "...?w=200&fit=max"
  }
}
```

### 动态缩放
您可以对任何图片URL添加以下参数（请保留 `ixid` 参数）：
- `w=1500`：设置宽度
- `h=800`：设置高度
- `dpr=2`：设备像素比
- `q=75`：图片质量（1-100）
- `fm=jpg`：图片格式（jpg、png、webp、avif）
- `fit=crop`：裁剪模式（裁剪、最大尺寸、裁剪区域）
- `crop=entropy`：裁剪方式

**示例：**
```
https://images.unsplash.com/photo-xxx?ixid=xxx&w=1500&h=1000&fit=crop&q=85
```

### `blur_hash` 占位符
每张图片都包含一个 `blur_hash` 字段——这是一个用于在图片加载时显示模糊占位符的紧凑字符串。

## 响应结构

### 图片对象（简化版）
```json
{
  "id": "LBI7cgq3pbM",
  "created_at": "2016-05-03T11:00:28-04:00",
  "width": 5245,
  "height": 3497,
  "color": "#60544D",
  "blur_hash": "LoC%a7IoIVxZ_NM|M{s:%hRjWAo0",
  "description": "A man drinking coffee",
  "urls": { "raw": "...", "full": "...", "regular": "..." },
  "links": {
    "download": "...",
    "download_location": "https://api.unsplash.com/photos/xxx/download"
  },
  "user": {
    "username": "johndoe",
    "name": "John Doe",
    "profile_image": { "small": "...", "medium": "...", "large": "..." }
  }
}
```

### 搜索结果
```json
{
  "total": 133,
  "total_pages": 7,
  "results": [ /* array of photo objects */ ]
}
```

## 最佳实践

### 致谢
始终注明图片的来源和创作者：
```
Photo by [Name] on Unsplash
```
如果可能的话，提供摄影师在Unsplash上的个人资料链接。

### 下载跟踪
- 在允许用户下载图片之前，先调用 `/photos/:id/download` 接口。
- 这是Unsplash API的使用规范要求。
- 请勿仅为了显示图片而使用此接口（图片的显示会通过热链接自动被记录）。

### 热链接
- 您可以直接从 `images.unsplash.com` 链接图片。
- 这些链接不会计入请求次数限制。
- 浏览量会自动被记录。
- 在使用或处理图片URL时，请务必保留 `ixid` 参数。

### 缓存
- 公共接口（搜索、图片）支持缓存。
- 建议在客户端缓存搜索结果，以减少API调用次数。

## 快速参考
```bash
# Store key
export UNSPLASH_ACCESS_KEY="your_key"

# Search
curl "https://api.unsplash.com/search/photos?query=ocean&per_page=5" \
  -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}"

# Random photo
curl "https://api.unsplash.com/photos/random?query=mountains" \
  -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}"

# Get photo
curl "https://api.unsplash.com/photos/PHOTO_ID" \
  -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}"

# Track download (required when downloading!)
curl "https://api.unsplash.com/photos/PHOTO_ID/download" \
  -H "Authorization: Client-ID ${UNSPLASH_ACCESS_KEY}"
```

## 注意事项

- 基础URL：`https://api.unsplash.com`
- 所有响应均为JSON格式。
- 通过 `page` 和 `per_page` 参数实现分页。
- 响应头中包含首页、上一页、下一页和最后一页的URL。
- 对 `images.unsplash.com` 的图片请求不计入请求次数限制。
- 在使用或处理图片URL时，请保留 `ixid` 参数。
- 如需在生产环境中使用Unsplash API，请在控制台申请更高的请求次数限制。

## 常用过滤条件

### 颜色
`black_and_white`、`black`、`white`、`yellow`、`orange`、`red`、`purple`、`magenta`、`green`、`teal`、`blue`

### 图片方向
`landscape`、`portrait`、`squarish`

### 排序选项
- 图片：`latest`（最新）、`oldest`（最旧）、`popular`（最受欢迎）
- 搜索：`relevant`（相关）、`latest`（最新）

## 错误处理
- `401 Unauthorized`：访问密钥无效或缺失
- `403 Forbidden`：超出请求次数限制或禁止的操作
- `404 Not Found`：图片、用户或集合不存在

请查看 `X-Ratelimit-Remaining` 头部字段以监控您的请求次数使用情况。