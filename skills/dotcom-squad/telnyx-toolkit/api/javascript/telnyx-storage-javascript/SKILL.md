---
name: telnyx-storage-javascript
description: >-
  Manage cloud storage buckets and objects using the S3-compatible Telnyx
  Storage API. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: storage
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 存储 - JavaScript

## 安装

```bash
npm install telnyx
```

## 设置

```javascript
import Telnyx from 'telnyx';

const client = new Telnyx({
  apiKey: process.env['TELNYX_API_KEY'], // This is the default and can be omitted
});
```

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 创建预签名对象 URL

返回一个带有时间戳和认证信息的 URL，用于下载（GET）或上传（PUT）对象。

`POST /storage/buckets/{bucketName}/{objectName}/presigned_url`

```javascript
const response = await client.storage.buckets.createPresignedURL('', { bucketName: '' });

console.log(response.content);
```

## 获取桶的 SSL 证书

（如适用）返回桶的存储证书详细信息。

`GET /storage/buckets/{bucketName}/ssl_certificate`

```javascript
const sslCertificate = await client.storage.buckets.sslCertificate.retrieve('');

console.log(sslCertificate.data);
```

## 添加 SSL 证书

上传 SSL 证书及其对应的密钥，以便将 Telnyx 的存储服务作为 CDN 使用。

`PUT /storage/buckets/{bucketName}/ssl_certificate`

```javascript
const sslCertificate = await client.storage.buckets.sslCertificate.create('');

console.log(sslCertificate.data);
```

## 删除 SSL 证书

删除 SSL 证书及其对应的密钥。

`DELETE /storage/buckets/{bucketName}/ssl_certificate`

## 获取 API 使用情况

按方法类别分组，返回指定时间范围内桶的 API 使用情况详细信息。

`GET /storage/buckets/{bucketName}/usage/api`

```javascript
const response = await client.storage.buckets.usage.getAPIUsage('', {
  filter: { end_time: '2019-12-27T18:11:19.117Z', start_time: '2019-12-27T18:11:19.117Z' },
});

console.log(response.data);
```

## 获取桶的使用情况

返回桶占用的存储空间大小和文件数量。

`GET /storage/buckets/{bucketName}/usage/storage`

```javascript
const response = await client.storage.buckets.usage.getBucketUsage('');

console.log(response.data);
```

## 列出迁移源覆盖范围

`GET /storage/migration_source_coverage`

```javascript
const response = await client.storage.listMigrationSourceCoverage();

console.log(response.data);
```

## 列出所有迁移源

`GET /storage/migration_sources`

```javascript
const migrationSources = await client.storage.migrationSources.list();

console.log(migrationSources.data);
```

## 创建迁移源

创建一个用于数据迁移的源。

`POST /storage/migration_sources` — 必需参数：`provider`、`provider_auth`、`bucket_name`

```javascript
const migrationSource = await client.storage.migrationSources.create({
  bucket_name: 'bucket_name',
  provider: 'aws',
  provider_auth: {},
});

console.log(migrationSource.data);
```

## 获取迁移源信息

`GET /storage/migration_sources/{id}`

```javascript
const migrationSource = await client.storage.migrationSources.retrieve('');

console.log(migrationSource.data);
```

## 删除迁移源

`DELETE /storage/migration_sources/{id}`

```javascript
const migrationSource = await client.storage.migrationSources.delete('');

console.log(migrationSource.data);
```

## 列出所有迁移记录

`GET /storage/migrations`

```javascript
const migrations = await client.storage.migrations.list();

console.log(migrations.data);
```

## 创建迁移任务

启动从外部提供商到 Telnyx 云存储的数据迁移。

`POST /storage/migrations` — 必需参数：`source_id`、`target_bucket_name`、`target_region`

```javascript
const migration = await client.storage.migrations.create({
  source_id: 'source_id',
  target_bucket_name: 'target_bucket_name',
  target_region: 'target_region',
});

console.log(migration.data);
```

## 获取迁移任务信息

`GET /storage/migrations/{id}`

```javascript
const migration = await client.storage.migrations.retrieve('');

console.log(migration.data);
```

## 停止迁移任务

`POST /storage/migrations/{id}/actions/stop`

```javascript
const response = await client.storage.migrations.actions.stop('');

console.log(response.data);
```