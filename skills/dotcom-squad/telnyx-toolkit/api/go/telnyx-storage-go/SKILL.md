---
name: telnyx-storage-go
description: >-
  Manage cloud storage buckets and objects using the S3-compatible Telnyx
  Storage API. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: storage
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 存储 - Go

## 安装

```bash
go get github.com/team-telnyx/telnyx-go
```

## 设置

```go
import (
  "context"
  "fmt"
  "os"

  "github.com/team-telnyx/telnyx-go"
  "github.com/team-telnyx/telnyx-go/option"
)

client := telnyx.NewClient(
  option.WithAPIKey(os.Getenv("TELNYX_API_KEY")),
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 创建预签名对象 URL

返回一个带时间戳和认证信息的 URL，用于下载（GET）或上传（PUT）对象。

`POST /storage/buckets/{bucketName}/{objectName}/presigned_url`

```go
	response, err := client.Storage.Buckets.NewPresignedURL(
		context.TODO(),
		"",
		telnyx.StorageBucketNewPresignedURLParams{
			BucketName: "",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Content)
```

## 获取桶的 SSL 证书

（如适用）返回桶的 SSL 证书详细信息。

`GET /storage/buckets/{bucketName}/ssl_certificate`

```go
	sslCertificate, err := client.Storage.Buckets.SslCertificate.Get(context.TODO(), "")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", sslCertificate.Data)
```

## 添加 SSL 证书

上传 SSL 证书及其对应的密钥，以便将 Telnyx 的存储服务用作 CDN。

`PUT /storage/buckets/{bucketName}/ssl_certificate`

```go
	sslCertificate, err := client.Storage.Buckets.SslCertificate.New(
		context.TODO(),
		"",
		telnyx.StorageBucketSslCertificateNewParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", sslCertificate.Data)
```

## 删除 SSL 证书

删除 SSL 证书及其对应的密钥。

`DELETE /storage/buckets/{bucketName}/ssl_certificate`

## 获取 API 使用情况

按方法类别统计某个桶在特定时间段的 API 使用情况。

`GET /storage/buckets/{bucketName}/usage/api`

```go
	response, err := client.Storage.Buckets.Usage.GetAPIUsage(
		context.TODO(),
		"",
		telnyx.StorageBucketUsageGetAPIUsageParams{
			Filter: telnyx.StorageBucketUsageGetAPIUsageParamsFilter{
				EndTime:   time.Now(),
				StartTime: time.Now(),
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取桶的使用情况

返回桶所占用的存储空间和文件数量。

`GET /storage/buckets/{bucketName}/usage/storage`

```go
	response, err := client.Storage.Buckets.Usage.GetBucketUsage(context.TODO(), "")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出迁移源覆盖范围

`GET /storage/migration_source_coverage`

```go
	response, err := client.Storage.ListMigrationSourceCoverage(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出所有迁移源

`GET /storage/migration_sources`

```go
	migrationSources, err := client.Storage.MigrationSources.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", migrationSources.Data)
```

## 创建迁移源

创建一个用于数据迁移的源。

`POST /storage/migration_sources` — 必需参数：`provider`, `provider_auth`, `bucket_name`

```go
	migrationSource, err := client.Storage.MigrationSources.New(context.TODO(), telnyx.StorageMigrationSourceNewParams{
		MigrationSourceParams: telnyx.MigrationSourceParams{
			BucketName:   "bucket_name",
			Provider:     telnyx.MigrationSourceParamsProviderAws,
			ProviderAuth: telnyx.MigrationSourceParamsProviderAuth{},
		},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", migrationSource.Data)
```

## 获取迁移源信息

`GET /storage/migration_sources/{id}`

```go
	migrationSource, err := client.Storage.MigrationSources.Get(context.TODO(), "")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", migrationSource.Data)
```

## 删除迁移源

`DELETE /storage/migration_sources/{id}`

```go
	migrationSource, err := client.Storage.MigrationSources.Delete(context.TODO(), "")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", migrationSource.Data)
```

## 列出所有迁移记录

`GET /storage/migrations`

```go
	migrations, err := client.Storage.Migrations.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", migrations.Data)
```

## 创建迁移任务

启动从外部提供商到 Telnyx 云存储的数据迁移。

`POST /storage/migrations` — 必需参数：`source_id`, `target_bucket_name`, `target_region`

```go
	migration, err := client.Storage.Migrations.New(context.TODO(), telnyx.StorageMigrationNewParams{
		MigrationParams: telnyx.MigrationParams{
			SourceID:         "source_id",
			TargetBucketName: "target_bucket_name",
			TargetRegion:     "target_region",
		},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", migration.Data)
```

## 获取迁移任务信息

`GET /storage/migrations/{id}`

```go
	migration, err := client.Storage.Migrations.Get(context.TODO(), "")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", migration.Data)
```

## 停止迁移任务

`POST /storage/migrations/{id}/actions/stop`

```go
	response, err := client.Storage.Migrations.Actions.Stop(context.TODO(), "")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```
```