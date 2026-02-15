---
name: telnyx-storage-python
description: >-
  Manage cloud storage buckets and objects using the S3-compatible Telnyx
  Storage API. This skill provides Python SDK examples.
metadata:
  author: telnyx
  product: storage
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 本文档由 Telnyx OpenAPI 规范自动生成，请勿修改。 -->

# Telnyx 存储服务 - Python

## 安装

```bash
pip install telnyx
```

## 设置

```python
import os
from telnyx import Telnyx

client = Telnyx(
    api_key=os.environ.get("TELNYX_API_KEY"),  # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 创建预签名对象 URL

生成一个带时间戳和身份验证信息的 URL，用于下载（GET）或上传（PUT）对象。

`POST /storage/buckets/{bucketName}/{objectName}/presigned_url`

```python
response = client.storage.buckets.create_presigned_url(
    object_name="",
    bucket_name="",
)
print(response.content)
```

## 获取桶的 SSL 证书

（如适用）返回桶的 SSL 证书详细信息。

`GET /storage/buckets/{bucketName}/ssl_certificate`

```python
ssl_certificate = client.storage.buckets.ssl_certificate.retrieve(
    "",
)
print(ssl_certificate.data)
```

## 添加 SSL 证书

上传 SSL 证书及其对应的密钥，以便将 Telnyx 的存储服务用作 CDN。

`PUT /storage/buckets/{bucketName}/ssl_certificate`

## 删除 SSL 证书

删除 SSL 证书及其对应的密钥。

`DELETE /storage/buckets/{bucketName}/ssl_certificate`

## 获取 API 使用情况

按方法类别统计指定时间范围内桶的 API 使用情况。

`GET /storage/buckets/{bucketName}/usage/api`

## 获取桶的使用情况

返回桶的存储空间大小和文件数量。

`GET /storage/buckets/{bucketName}/usage/storage`

## 列出迁移源的覆盖范围

`GET /storage/migration_source_coverage`

## 列出所有迁移源

`GET /storage/migration_sources`

## 创建迁移源

创建一个可用于数据迁移的源。

`POST /storage/migration_sources` — 必需参数：`provider`、`provider_auth`、`bucket_name`

## 获取迁移源信息

`GET /storage/migration_sources/{id}`

## 删除迁移源

`DELETE /storage/migration_sources/{id}`

## 列出所有迁移记录

`GET /storage/migrations`

## 创建迁移任务

启动从外部提供商到 Telnyx 云存储的数据迁移。

`POST /storage/migrations` — 必需参数：`source_id`、`target_bucket_name`、`target_region`

## 获取迁移任务信息

`GET /storage/migrations/{id}`

## 停止迁移任务

`POST /storage/migrations/{id}/actions/stop`

```python
response = client.storage.migrations.actions.stop(
    "",
)
print(response.data)
```