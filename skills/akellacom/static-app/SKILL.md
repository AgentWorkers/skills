---
name: Static Website Hosting - Static.app
description: 将静态网站部署到 Static.app 托管平台上。当用户需要将静态网站部署、上传或托管在 Static.app 上时，可以使用此方法。该流程会在检测到以下关键词时触发：`deploy to static.app`、`upload to static`、`host on static.app`、`static.app deploy`，或在处理 Static.app 托管服务相关操作时启动。
---

# Static.app 部署技能

您可以直接从 OpenClaw 将静态网站和应用程序部署到 [Static.app](https://static.app) 托管平台上。

## 工作区结构

您工作区中的所有 Static.app 操作都遵循一个专门的文件夹结构：

```
workspace/
└── staticapp/              # Main folder for all Static.app operations
    ├── new-site/           # New sites created locally
    └── {pid}/              # Downloaded existing sites (by PID)
```

- **新网站**：在部署前创建于 `staticapp/` 子文件夹中。
- **已下载的网站**：解压到 `staticapp/{pid}/` 目录中以供编辑。

## Static.app 如何处理文件

Static.app 会自动根据文件名生成简洁的 URL：

| 文件名 | 对应的 URL |
|------|-----|
| `index.html` | `/`（首页） |
| `about.html` | `/about` |
| `portfolio.html` | `/portfolio` |
| `contact.html` | `/contact` |

**无需创建子目录！** 只需在根目录下创建 `.html` 文件即可。

## 项目结构

### 简单的多页面网站

```
my-site/
├── index.html          # Homepage → /
├── about.html          # About page → /about
├── portfolio.html      # Portfolio → /portfolio
├── contact.html        # Contact → /contact
├── style.css           # Stylesheet
├── js/                 # JavaScript files
│   ├── main.js
│   └── utils.js
└── images/             # Images folder
    ├── logo.png
    └── photo.jpg
```

### JavaScript 应用程序（React、Vue 等）

对于 JavaScript 应用程序，请先进行构建，然后部署 `dist`（或 `build`）文件夹：

```bash
# Build your app
npm run build

# Deploy the dist folder
node scripts/deploy.js ./dist
```

## 先决条件

1. **获取 API 密钥**：访问 https://static.app/account/api 并创建一个 API 密钥（密钥以 `sk_` 开头）。
2. **设置环境变量**：将 API 密钥存储在 `STATIC_APP_API_KEY` 环境变量中。

## 使用方法

### 部署多页面网站

```bash
# Create your pages
echo '<h1>Home</h1>' > index.html
echo '<h1>About</h1>' > about.html
echo '<h1>Portfolio</h1>' > portfolio.html

# Deploy
node scripts/deploy.js
```

### 部署特定目录

```bash
node scripts/deploy.js ./my-site
```

### 更新现有网站

```bash
node scripts/deploy.js . --pid olhdscieyr
```

### 列出所有网站

```bash
node scripts/list.js
```

### 列出网站文件

```bash
node scripts/files.js YOUR_PID
```

**选项：**
- `--raw` — 输出原始 JSON 数据
- `-k <密钥>` — 指定 API 密钥

### 删除网站

```bash
node scripts/delete.js YOUR_PID
```

**选项：**
- `-f, --force` — 跳过确认提示
- `-k <密钥>` — 指定 API 密钥

### 下载网站

将现有网站下载到您的工作区以供编辑：

```bash
node scripts/download.js YOUR_PID
```

具体步骤如下：
1. 从 Static.app API 获取下载 URL。
2. 下载网站压缩文件。
3. 将文件解压到 `staticapp/{pid}/` 目录中。

**选项：**
- `-p, --pid` — 要下载的网站 PID。
- `-o, --output` — 自定义输出目录（默认：`./staticapp/{pid}`）。
- `-k <密钥>` — 指定 API 密钥。
- `--raw` — 输出原始 JSON 响应。

**示例：**
```bash
# Download site to default location
node scripts/download.js abc123

# Download to custom folder
node scripts/download.js abc123 -o ./my-site
```

## 脚本选项

```
node scripts/deploy.js [SOURCE_DIR] [OPTIONS]

Arguments:
  SOURCE_DIR          Directory to deploy (default: current directory)

Options:
  -k, --api-key       API key (or set STATIC_APP_API_KEY env var)
  -p, --pid           Project PID to update existing site
  -e, --exclude       Comma-separated exclude patterns
  --keep-zip          Keep zip archive after deployment
```

## 默认排除项

以下文件在部署过程中会被自动排除：
- `node_modules`
- `.git`, `.github`
- `*.md`
- `package*.json`
- `.env`
- `.openclaw`

## 重要说明

### ✅ 支持的内容

- **静态 HTML 网站**：任意数量的 `.html` 页面。
- **CSS 和 JavaScript**：前端框架或纯 JavaScript 代码。
- **图片和资源文件**：放置在 `images/` 目录或根目录中。
- **JavaScript 文件**：放置在 `js/` 目录或根目录中。
- **构建好的 JavaScript 应用程序**：部署 `dist/` 或 `build/` 文件夹（在运行 `npm run build` 后生成）。

### ❌ 不支持的内容

- **Node.js 服务器应用程序**：不支持服务器端渲染、Express.js 或 API 路由。
- **PHP、Python、Ruby**：Static.app 仅支持静态文件。
- **数据库**：请使用客户端存储或外部 API。

### JavaScript 应用程序的部署流程

```bash
# 1. Build your React/Vue/Angular app
npm run build

# 2. Deploy the build output
node scripts/deploy.js ./dist --pid YOUR_PID
```

## API 参考

### 部署网站
- **端点**：`POST https://api.static.app/v1/sites/zip`
- **认证**：需要携带 Bearer 令牌（API 密钥）。
- **请求体**：包含 `archive`（压缩文件）和可选的 `pid` 的 multipart 请求。

### 列出网站
- **端点**：`GET https://api.static.app/v1/sites`
- **认证**：需要携带 Bearer 令牌（API 密钥）。
- **请求头**：`Accept: application/json`

### 列出网站文件
- **端点**：`GET https://api.static.app/v1/sites/files/{pid}`
- **认证**：需要携带 Bearer 令牌（API 密钥）。
- **请求头**：`Accept: application/json`

### 删除网站
- **端点**：`DELETE https://api.static.app/v1/sites/{pid}`
- **认证**：需要携带 Bearer 令牌（API 密钥）。
- **请求头**：`Accept: application/json`

### 下载网站
- **端点**：`GET https://api.static.app/v1/sites/download/{pid}`
- **认证**：需要携带 Bearer 令牌（API 密钥）。
- **请求头**：`Accept: application/json`
- **响应**：返回网站的下载 URL。

## 所需依赖库

- `archiver`：用于创建压缩文件。
- `form-data`：用于处理 multipart 请求。
- `node-fetch`：用于发送 HTTP 请求。
- `adm-zip`：用于解压文件。

**安装方式：** `cd scripts && npm install`

## 响应结果

成功执行后，脚本会输出以下内容：
```
✅ Deployment successful!
🌐 Site URL: https://xyz.static.app
📋 PID: abc123

STATIC_APP_URL=https://xyz.static.app
STATIC_APP_PID=abc123
```

## 工作流程

1. 检查 `STATIC_APP_API_KEY` 环境变量或 `--api-key` 是否已设置。
2. 从源目录创建压缩文件（排除指定文件）。
3. 将文件上传到 Static.app API。
4. 解析响应并生成相应的 URL。
5. 清理临时生成的压缩文件。

## 错误处理

- 如果缺少 API 密钥，会显示相应的错误信息及处理方法。
- 如果遇到网络问题，会显示 HTTP 错误详情。
- 如果提供的 PID 无效，会返回 API 错误信息。