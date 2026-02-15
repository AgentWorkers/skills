---
name: google-cloud
description: 通过 `gcloud` CLI 管理 Google Cloud 资源。包括计算资源、存储服务以及云函数（cloud functions）。
metadata: {"clawdbot":{"emoji":"☁️","requires":{"bins":["gcloud"]}}}
---
# Google Cloud Platform
云基础设施和服务。

## 身份认证（Auth）
```bash
gcloud auth login
gcloud config set project PROJECT_ID
```

## 计算引擎（Compute Engine）
```bash
gcloud compute instances list
gcloud compute instances create vm-name --zone=us-central1-a --machine-type=e2-micro
gcloud compute instances stop vm-name --zone=us-central1-a
```

## 云函数（Cloud Functions）
```bash
gcloud functions list
gcloud functions deploy myFunction --runtime nodejs18 --trigger-http --allow-unauthenticated
gcloud functions call myFunction --data '{"name": "test"}'
```

## 云存储（Cloud Storage）
```bash
gsutil ls gs://bucket-name/
gsutil cp file.txt gs://bucket-name/
gsutil cp gs://bucket-name/file.txt ./
```

## 云运行（Cloud Run）
```bash
gcloud run services list
gcloud run deploy service-name --image gcr.io/project/image --platform managed
```

## 链接（Links）
- 控制台：https://console.cloud.google.com
- 文档：https://cloud.google.com/sdk/gcloud/reference