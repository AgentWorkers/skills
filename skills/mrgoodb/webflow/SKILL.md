---
name: webflow
description: 通过 API 管理 Webflow 网站、CMS 集合和表单。以编程方式发布网站并管理内容。
metadata: {"clawdbot":{"emoji":"🎨","requires":{"env":["WEBFLOW_API_TOKEN"]}}}
---

# Webflow

Webflow 是一款用于构建网站和内容管理的平台（Website Builder and Content Management System, CMS）。

## 开发环境（Development Environment）

```bash
export WEBFLOW_API_TOKEN="xxxxxxxxxx"
```

## 网站列表（List of Websites）

```bash
curl "https://api.webflow.com/v2/sites" \
  -H "Authorization: Bearer $WEBFLOW_API_TOKEN"
```

## 查看网站详情（View Site Details）

```bash
curl "https://api.webflow.com/v2/sites/{site_id}" \
  -H "Authorization: Bearer $WEBFLOW_API_TOKEN"
```

## 查看集合（Collections, CMS）

```bash
curl "https://api.webflow.com/v2/sites/{site_id}/collections" \
  -H "Authorization: Bearer $WEBFLOW_API_TOKEN"
```

## 查看集合中的项目（Items in Collections, CMS）

```bash
curl "https://api.webflow.com/v2/collections/{collection_id}/items" \
  -H "Authorization: Bearer $WEBFLOW_API_TOKEN"
```

## 创建 CMS 项目（Create a CMS Item）

```bash
curl -X POST "https://api.webflow.com/v2/collections/{collection_id}/items" \
  -H "Authorization: Bearer $WEBFLOW_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fieldData": {
      "name": "New Blog Post",
      "slug": "new-blog-post",
      "content": "Post content here..."
    }
  }'
```

## 发布网站（Publish a Website）

```bash
curl -X POST "https://api.webflow.com/v2/sites/{site_id}/publish" \
  -H "Authorization: Bearer $WEBFLOW_API_TOKEN"
```

## 查看表单提交记录（View Form Submissions）

```bash
curl "https://api.webflow.com/v2/sites/{site_id}/forms/{form_id}/submissions" \
  -H "Authorization: Bearer $WEBFLOW_API_TOKEN"
```

## 链接（Links）

- 控制面板：https://webflow.com/dashboard
- 文档：https://developers.webflow.com