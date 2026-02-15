---
name: telnyx-storage-ruby
description: >-
  Manage cloud storage buckets and objects using the S3-compatible Telnyx
  Storage API. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: storage
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 本文档由 Telnyx OpenAPI 规范自动生成，请勿修改。 -->

# Telnyx 存储服务 - Ruby

## 安装

```bash
gem install telnyx
```

## 配置

```ruby
require "telnyx"

client = Telnyx::Client.new(
  api_key: ENV["TELNYX_API_KEY"], # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 创建预签名对象 URL

用于下载（GET）或上传（PUT）对象。  
`POST /storage/buckets/{bucketName}/{objectName}/presigned_url`

```ruby
response = client.storage.buckets.create_presigned_url("", bucket_name: "")

puts(response)
```

## 获取桶的 SSL 证书

（如适用）返回桶的 SSL 证书详细信息。  
`GET /storage/buckets/{bucketName}/ssl_certificate`

```ruby
ssl_certificate = client.storage.buckets.ssl_certificate.retrieve("")

puts(ssl_certificate)
```

## 添加 SSL 证书

上传 SSL 证书及其对应的密钥，以便将 Telnyx 的存储服务用作 CDN。  
`PUT /storage/buckets/{bucketName}/ssl_certificate`

```ruby
ssl_certificate = client.storage.buckets.ssl_certificate.create("")

puts(ssl_certificate)
```

## 删除 SSL 证书

删除 SSL 证书及其对应的密钥。  
`DELETE /storage/buckets/{bucketName}/ssl_certificate`

## 获取 API 使用情况

按方法类别统计指定时间段的 API 使用情况。  
`GET /storage/buckets/{bucketName}/usage/api`

```ruby
response = client.storage.buckets.usage.get_api_usage(
  "",
  filter: {end_time: "2019-12-27T18:11:19.117Z", start_time: "2019-12-27T18:11:19.117Z"}
)

puts(response)
```

## 获取桶的使用情况

返回桶的存储空间大小和文件数量。  
`GET /storage/buckets/{bucketName}/usage/storage`

```ruby
response = client.storage.buckets.usage.get_bucket_usage("")

puts(response)
```

## 列出迁移源覆盖范围  

显示所有迁移源的覆盖范围。  
`GET /storage/migration_source_coverage`

```ruby
response = client.storage.list_migration_source_coverage

puts(response)
```

## 列出所有迁移源  

显示所有可用的迁移源。  
`GET /storage/migration_sources`

```ruby
migration_sources = client.storage.migration_sources.list

puts(migration_sources)
```

## 创建迁移源  

创建一个用于数据迁移的源。  
`POST /storage/migration_sources` — 必需参数：`provider`, `provider_auth`, `bucket_name`

```ruby
migration_source = client.storage.migration_sources.create(bucket_name: "bucket_name", provider: :aws, provider_auth: {})

puts(migration_source)
```

## 获取迁移源信息  

获取特定迁移源的详细信息。  
`GET /storage/migration_sources/{id}`

```ruby
migration_source = client.storage.migration_sources.retrieve("")

puts(migration_source)
```

## 删除迁移源  

删除指定的迁移源。  
`DELETE /storage/migration_sources/{id}`

```ruby
migration_source = client.storage.migration_sources.delete("")

puts(migration_source)
```

## 列出所有迁移记录  

显示所有已完成的迁移操作。  
`GET /storage/migrations`

```ruby
migrations = client.storage.migrations.list

puts(migrations)
```

## 创建数据迁移  

启动从外部提供商到 Telnyx 云存储的数据迁移。  
`POST /storage/migrations` — 必需参数：`source_id`, `target_bucket_name`, `target_region`

```ruby
migration = client.storage.migrations.create(
  source_id: "source_id",
  target_bucket_name: "target_bucket_name",
  target_region: "target_region"
)

puts(migration)
```

## 获取迁移记录  

获取特定迁移的详细信息。  
`GET /storage/migrations/{id}`

```ruby
migration = client.storage.migrations.retrieve("")

puts(migration)
```

## 停止迁移  

停止正在进行的迁移操作。  
`POST /storage/migrations/{id}/actions/stop`

```ruby
response = client.storage.migrations.actions.stop("")

puts(response)
```