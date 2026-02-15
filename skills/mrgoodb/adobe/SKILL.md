---
name: adobe
description: **访问 Adobe Creative Cloud API——Photoshop、Lightroom、PDF 服务以及 Firefly AI**  
实现创意工作流程的自动化。
metadata: {"clawdbot":{"emoji":"🎨","requires":{"env":["ADOBE_CLIENT_ID","ADOBE_ACCESS_TOKEN"]}}}
---

# Adobe Creative Cloud

提供用于创意设计和文档处理的API接口。

## 开发环境

```bash
export ADOBE_CLIENT_ID="xxxxxxxxxx"
export ADOBE_ACCESS_TOKEN="xxxxxxxxxx"
```

## Photoshop API - 去除背景

```bash
curl -X POST "https://image.adobe.io/sensei/cutout" \
  -H "Authorization: Bearer $ADOBE_ACCESS_TOKEN" \
  -H "x-api-key: $ADOBE_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "input": {"href": "https://example.com/image.jpg", "storage": "external"},
    "output": {"href": "https://your-bucket.s3.amazonaws.com/output.png", "storage": "external"}
  }'
```

## PDF服务 - 创建PDF文件

```bash
curl -X POST "https://pdf-services.adobe.io/operation/createpdf" \
  -H "Authorization: Bearer $ADOBE_ACCESS_TOKEN" \
  -H "x-api-key: $ADOBE_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "assetID": "{asset_id}"
  }'
```

## PDF服务 - 将PDF文件导出为Word格式

```bash
curl -X POST "https://pdf-services.adobe.io/operation/exportpdf" \
  -H "Authorization: Bearer $ADOBE_ACCESS_TOKEN" \
  -H "x-api-key: $ADOBE_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "assetID": "{asset_id}",
    "targetFormat": "docx"
  }'
```

## Firefly - 生成图片（基于人工智能技术）

```bash
curl -X POST "https://firefly-api.adobe.io/v2/images/generate" \
  -H "Authorization: Bearer $ADOBE_ACCESS_TOKEN" \
  -H "x-api-key: $ADOBE_CLIENT_ID" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic cityscape at sunset",
    "n": 1,
    "size": {"width": 1024, "height": 1024}
  }'
```

## Lightroom - 获取作品集信息

```bash
curl "https://lr.adobe.io/v2/catalogs" \
  -H "Authorization: Bearer $ADOBE_ACCESS_TOKEN" \
  -H "x-api-key: $ADOBE_CLIENT_ID"
```

## 相关链接：
- 控制台：https://developer.adobe.com/console
- 文档资料：https://developer.adobe.com/apis