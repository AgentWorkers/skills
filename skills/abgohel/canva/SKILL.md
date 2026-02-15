---
name: canva
version: 1.0.0
description: 通过 Connect API 创建、导出和管理 Canva 设计；能够以编程方式生成社交媒体帖子、轮播图和图形元素。
homepage: https://github.com/abgohel/canva-skill
metadata: {"clawdbot":{"emoji":"🎨","category":"design","requires":{"env":["CANVA_CLIENT_ID","CANVA_CLIENT_SECRET"]}}}
---

# Canva Skill

通过 Connect API 创建、导出和管理 Canva 设计。

## 使用场景

- “创建关于 [主题] 的 Instagram 帖子”
- “将我的 Canva 设计导出为 PNG 格式”
- “列出我最近的设计”
- “根据这些内容创建一个轮播图”
- “将这张图片上传到 Canva”

## 先决条件

1. **创建 Canva 集成：**
   - 访问 https://www.canva.com/developers/
   - 创建一个新的集成
   - 获取您的客户端 ID（Client ID）和客户端密钥（Client Secret）

2. **设置环境变量：**
   ```bash
   export CANVA_CLIENT_ID="your_client_id"
   export CANVA_CLIENT_SECRET="your_client_secret"
   ```

3. **首次认证：**
   运行认证流程以获取访问令牌（存储在 `~/.canva/tokens.json` 文件中）

## API 基本 URL

```
https://api.canva.com/rest/v1
```

## 认证

Canva 使用 OAuth 2.0。该技能会自动刷新令牌。

```bash
# Get access token (stored in ~/.canva/tokens.json)
ACCESS_TOKEN=$(cat ~/.canva/tokens.json | jq -r '.access_token')
```

## 核心操作

### 列出设计（List Designs）

```bash
curl -s "https://api.canva.com/rest/v1/designs" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .
```

### 获取设计详情（Get Design Details）

```bash
curl -s "https://api.canva.com/rest/v1/designs/{designId}" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .
```

### 根据模板创建设计（Create Design from Template）

```bash
curl -X POST "https://api.canva.com/rest/v1/autofills" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "brand_template_id": "TEMPLATE_ID",
    "data": {
      "title": {"type": "text", "text": "Your Title"},
      "body": {"type": "text", "text": "Your body text"}
    }
  }'
```

### 导出设计（Export Design）

```bash
# Start export job
curl -X POST "https://api.canva.com/rest/v1/exports" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "design_id": "DESIGN_ID",
    "format": {"type": "png", "width": 1080, "height": 1080}
  }'

# Check export status
curl -s "https://api.canva.com/rest/v1/exports/{jobId}" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .
```

### 上传资产（Upload Asset）

```bash
curl -X POST "https://api.canva.com/rest/v1/asset-uploads" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  -H 'Asset-Upload-Metadata: {"name": "my-image.png"}' \
  --data-binary @image.png
```

### 列出品牌模板（List Brand Templates）

```bash
curl -s "https://api.canva.com/rest/v1/brand-templates" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq .
```

## 导出格式（Export Formats）

| 格式 | 选项 |
|--------|---------|
| PNG | 宽度、高度、无损压缩 |
| JPG | 宽度、高度、质量（1-100） |
| PDF | 标准格式、适合打印 |
| MP4 | 适用于视频设计 |
| GIF | 适用于动画设计 |

## 常见工作流程

### 创建 Instagram 帖子

1. 列出品牌模板：`GET /brand-templates`
2. 选择 Instagram 帖子模板
3. 自动填充内容：`POST /autofills`
4. 将设计导出为 1080x1080 像素的 PNG 文件：`POST /exports`
5. 下载导出的文件

### 创建轮播图

1. 使用自动填充功能创建多个设计
2. 将每个设计导出为 PNG 格式
3. 将它们组合起来用于发布

### 批量导出

1. 列出所有设计：`GET /designs`
2. 遍历并逐个导出设计
3. 下载所有文件

## 速率限制

- 大多数接口：每分钟 100 次请求
- 上传/导出：每分钟 30 次请求

## 错误处理

常见错误：
- `401` - 令牌过期，需要刷新
- `403` - 缺少必要的权限范围
- `429` - 超过速率限制
- `404` - 设计/模板未找到

## 所需权限范围（Scopes Required）

- `design:content:read` - 读取设计信息
- `design:content:write` - 创建/修改设计
- `asset:read` - 读取资产信息
- `asset:write` - 上传资产
- `brandtemplate:content:read` - 读取品牌模板信息

## 提示

- **使用品牌模板** - 使用预先设计好的模板可以节省时间
- **批量操作** - 分组导出以避免超出速率限制
- **缓存模板 ID** - 将常用的模板 ID 存储在本地
- **检查任务状态** - 导出操作是异步的；请等待完成后再进行下一步操作

## 资源

- [Canva Connect API 文档](https://www.canva.dev/docs/connect/)
- [OpenAPI 规范](https://www.canva.dev/sources/connect/api/latest/api.yml)
- [入门套件](https://github.com/canva-sdks/canva-connect-api-starter-kit)

---

由 **Meow 😼** 为 Moltbook 社区 🦞 制作