---
name: telnyx-storage-java
description: >-
  Manage cloud storage buckets and objects using the S3-compatible Telnyx
  Storage API. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: storage
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 存储 - Java

## 安装

```text
// See https://github.com/team-telnyx/telnyx-java for Maven/Gradle setup
```

## 设置

```java
import com.telnyx.sdk.client.TelnyxClient;
import com.telnyx.sdk.client.okhttp.TelnyxOkHttpClient;

TelnyxClient client = TelnyxOkHttpClient.fromEnv();
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 创建预签名对象 URL

返回一个带时间戳和认证信息的 URL，用于下载（GET）或上传（PUT）对象。

`POST /storage/buckets/{bucketName}/{objectName}/presigned_url`

```java
import com.telnyx.sdk.models.storage.buckets.BucketCreatePresignedUrlParams;
import com.telnyx.sdk.models.storage.buckets.BucketCreatePresignedUrlResponse;

BucketCreatePresignedUrlParams params = BucketCreatePresignedUrlParams.builder()
    .bucketName("")
    .objectName("")
    .build();
BucketCreatePresignedUrlResponse response = client.storage().buckets().createPresignedUrl(params);
```

## 获取桶的 SSL 证书

（如适用）返回桶的存储证书详细信息。

`GET /storage/buckets/{bucketName}/ssl_certificate`

```java
import com.telnyx.sdk.models.storage.buckets.sslcertificate.SslCertificateRetrieveParams;
import com.telnyx.sdk.models.storage.buckets.sslcertificate.SslCertificateRetrieveResponse;

SslCertificateRetrieveResponse sslCertificate = client.storage().buckets().sslCertificate().retrieve("");
```

## 添加 SSL 证书

上传 SSL 证书及其对应的密钥，以便将 Telnyx 的存储服务用作 CDN。

`PUT /storage/buckets/{bucketName}/ssl_certificate`

```java
import com.telnyx.sdk.models.storage.buckets.sslcertificate.SslCertificateCreateParams;
import com.telnyx.sdk.models.storage.buckets.sslcertificate.SslCertificateCreateResponse;

SslCertificateCreateResponse sslCertificate = client.storage().buckets().sslCertificate().create("");
```

## 删除 SSL 证书

删除 SSL 证书及其对应的密钥。

`DELETE /storage/buckets/{bucketName}/ssl_certificate`

## 获取 API 使用情况

按方法类别统计指定时间段的 API 使用情况。

`GET /storage/buckets/{bucketName}/usage/api`

```java
import com.telnyx.sdk.models.storage.buckets.usage.UsageGetApiUsageParams;
import com.telnyx.sdk.models.storage.buckets.usage.UsageGetApiUsageResponse;
import java.time.OffsetDateTime;

UsageGetApiUsageParams params = UsageGetApiUsageParams.builder()
    .bucketName("")
    .filter(UsageGetApiUsageParams.Filter.builder()
        .endTime(OffsetDateTime.parse("2019-12-27T18:11:19.117Z"))
        .startTime(OffsetDateTime.parse("2019-12-27T18:11:19.117Z"))
        .build())
    .build();
UsageGetApiUsageResponse response = client.storage().buckets().usage().getApiUsage(params);
```

## 获取桶的使用情况

返回桶所占用的存储空间和文件数量。

`GET /storage/buckets/{bucketName}/usage/storage`

```java
import com.telnyx.sdk.models.storage.buckets.usage.UsageGetBucketUsageParams;
import com.telnyx.sdk.models.storage.buckets.usage.UsageGetBucketUsageResponse;

UsageGetBucketUsageResponse response = client.storage().buckets().usage().getBucketUsage("");
```

## 列出迁移源覆盖范围

`GET /storage/migration_source_coverage`

```java
import com.telnyx.sdk.models.storage.StorageListMigrationSourceCoverageParams;
import com.telnyx.sdk.models.storage.StorageListMigrationSourceCoverageResponse;

StorageListMigrationSourceCoverageResponse response = client.storage().listMigrationSourceCoverage();
```

## 列出所有迁移源

`GET /storage/migration_sources`

```java
import com.telnyx.sdk.models.storage.migrationsources.MigrationSourceListParams;
import com.telnyx.sdk.models.storage.migrationsources.MigrationSourceListResponse;

MigrationSourceListResponse migrationSources = client.storage().migrationSources().list();
```

## 创建迁移源

创建一个可用于数据迁移的源。

`POST /storage/migration_sources` — 必需参数：`provider`、`provider_auth`、`bucket_name`

```java
import com.telnyx.sdk.models.storage.migrationsources.MigrationSourceCreateParams;
import com.telnyx.sdk.models.storage.migrationsources.MigrationSourceCreateResponse;
import com.telnyx.sdk.models.storage.migrationsources.MigrationSourceParams;

MigrationSourceParams params = MigrationSourceParams.builder()
    .bucketName("bucket_name")
    .provider(MigrationSourceParams.Provider.AWS)
    .providerAuth(MigrationSourceParams.ProviderAuth.builder().build())
    .build();
MigrationSourceCreateResponse migrationSource = client.storage().migrationSources().create(params);
```

## 获取迁移源信息

`GET /storage/migration_sources/{id}`

```java
import com.telnyx.sdk.models.storage.migrationsources.MigrationSourceRetrieveParams;
import com.telnyx.sdk.models.storage.migrationsources.MigrationSourceRetrieveResponse;

MigrationSourceRetrieveResponse migrationSource = client.storage().migrationSources().retrieve("");
```

## 删除迁移源

`DELETE /storage/migration_sources/{id}`

```java
import com.telnyx.sdk.models.storage.migrationsources.MigrationSourceDeleteParams;
import com.telnyx.sdk.models.storage.migrationsources.MigrationSourceDeleteResponse;

MigrationSourceDeleteResponse migrationSource = client.storage().migrationSources().delete("");
```

## 列出所有迁移记录

`GET /storage/migrations`

```java
import com.telnyx.sdk.models.storage.migrations.MigrationListParams;
import com.telnyx.sdk.models.storage.migrations.MigrationListResponse;

MigrationListResponse migrations = client.storage().migrations().list();
```

## 创建迁移任务

启动从外部提供者到 Telnyx 云存储的数据迁移。

`POST /storage/migrations` — 必需参数：`source_id`、`target_bucket_name`、`target_region`

```java
import com.telnyx.sdk.models.storage.migrations.MigrationCreateParams;
import com.telnyx.sdk.models.storage.migrations.MigrationCreateResponse;
import com.telnyx.sdk.models.storage.migrations.MigrationParams;

MigrationParams params = MigrationParams.builder()
    .sourceId("source_id")
    .targetBucketName("target_bucket_name")
    .targetRegion("target_region")
    .build();
MigrationCreateResponse migration = client.storage().migrations().create(params);
```

## 获取迁移任务信息

`GET /storage/migrations/{id}`

```java
import com.telnyx.sdk.models.storage.migrations.MigrationRetrieveParams;
import com.telnyx.sdk.models.storage.migrations.MigrationRetrieveResponse;

MigrationRetrieveResponse migration = client.storage().migrations().retrieve("");
```

## 停止迁移任务

`POST /storage/migrations/{id}/actions/stop`

```java
import com.telnyx.sdk.models.storage.migrations.actions.ActionStopParams;
import com.telnyx.sdk.models.storage.migrations.actions.ActionStopResponse;

ActionStopResponse response = client.storage().migrations().actions().stop("");
```