---
name: kaggle
description: >
  **Kaggle API集成与托管认证**  
  支持用户通过托管认证方式访问Kaggle的数据集、模型、竞赛信息以及相关计算资源（如ClawHub提供的计算内核）。  
  当用户需要搜索、下载或与Kaggle资源进行交互时，可使用此功能。  
  对于其他第三方应用程序，建议使用`api-gateway`功能（https://clawhub.ai/byungkyu/api-gateway）进行集成。
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji:
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---
# Kaggle

您可以通过管理的API认证来访问Kaggle的数据集、模型、竞赛和笔记本。

## 快速入门

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({}).encode()
req = urllib.request.Request('https://gateway.maton.ai/kaggle/v1/datasets.DatasetApiService/ListDatasets', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基础URL

```
https://gateway.maton.ai/kaggle/{native-api-path}
```

该代理将请求转发到`api.kaggle.com`，并自动注入您的凭据。

## 认证

所有请求都需要Maton API密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的API密钥设置为`MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取您的API密钥

1. 在[maton.ai](https://maton.ai)登录或创建账户。
2. 访问[maton.ai/settings](https://maton.ai/settings)。
3. 复制您的API密钥。

## 连接管理

您可以在`https://ctrl.maton.ai`管理您的Kaggle连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=kaggle&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'kaggle'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

在浏览器中打开返回的`url`以完成认证。Kaggle使用API密钥进行认证——您需要提供您的Kaggle用户名和从[kaggle.com/settings](https://www.kaggle.com/settings)获取的API密钥。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

---

## API参考

Kaggle使用RPC风格的API。所有请求都是POST请求，并且请求体为JSON格式。

```
POST /kaggle/v1/{ServiceName}/{MethodName}
Content-Type: application/json
```

---

### 数据集

#### 列出数据集

```bash
POST /kaggle/v1/datasets.DatasetApiService/ListDatasets
Content-Type: application/json

{}
```

**请求体参数：**
- `search` - 搜索词（可选）
- `user` - 按用户名过滤（可选）
- `pageSize` - 每页显示的结果数量（可选）
- `pageToken` - 分页令牌（可选）

**搜索示例：**
```json
{
  "search": "covid"
}
```

**响应：**
```json
{
  "datasets": [
    {
      "id": 9481458,
      "ref": "amar5693/screen-time-sleep-and-stress-analysis-dataset",
      "title": "Screen Time, Sleep & Stress Analysis Dataset",
      "subtitle": "ML-ready dataset analyzing smartphone usage and productivity.",
      "totalBytes": 787136,
      "downloadCount": 11659,
      "voteCount": 236,
      "usabilityRating": 1,
      "licenseName": "CC0: Public Domain",
      "ownerName": "Amar Tiwari",
      "tags": [...]
    }
  ]
}
```

#### 获取数据集

```bash
POST /kaggle/v1/datasets.DatasetApiService/GetDataset
Content-Type: application/json

{
  "ownerSlug": "amar5693",
  "datasetSlug": "screen-time-sleep-and-stress-analysis-dataset"
}
```

**响应：**
```json
{
  "id": 9481458,
  "title": "Screen Time, Sleep & Stress Analysis Dataset",
  "subtitle": "ML-ready dataset analyzing smartphone usage and productivity.",
  "totalBytes": 787136,
  "downloadCount": 11659,
  "usabilityRating": 1
}
```

#### 列出数据集文件

```bash
POST /kaggle/v1/datasets.DatasetApiService/ListDatasetFiles
Content-Type: application/json

{
  "ownerSlug": "amar5693",
  "datasetSlug": "screen-time-sleep-and-stress-analysis-dataset"
}
```

**响应：**
```json
{
  "datasetFiles": [
    {
      "name": "Smartphone_Usage_Productivity_Dataset_50000.csv",
      "creationDate": "2026-02-13T06:56:19.803Z",
      "totalBytes": 2958561
    }
  ]
}
```

#### 获取数据集元数据

```bash
POST /kaggle/v1/datasets.DatasetApiService/GetDatasetMetadata
Content-Type: application/json

{
  "ownerSlug": "amar5693",
  "datasetSlug": "screen-time-sleep-and-stress-analysis-dataset"
}
```

**响应：**
```json
{
  "info": {
    "datasetId": 9481458,
    "datasetSlug": "screen-time-sleep-and-stress-analysis-dataset",
    "ownerUser": "amar5693",
    "title": "Screen Time, Sleep & Stress Analysis Dataset",
    "description": "...",
    "totalViews": 44291,
    "totalVotes": 236,
    "totalDownloads": 11661
  }
}
```

#### 下载数据集

```bash
POST /kaggle/v1/datasets.DatasetApiService/DownloadDataset
Content-Type: application/json

{
  "ownerSlug": "amar5693",
  "datasetSlug": "screen-time-sleep-and-stress-analysis-dataset"
}
```

返回二进制数据（ZIP文件）。响应头信息：
- `Content-Type: application/zip`
- `Content-Length: <文件大小（字节）`

---

### 模型

#### 列出模型

```bash
POST /kaggle/v1/models.ModelApiService/ListModels
Content-Type: application/json

{}
```

**请求体参数：**
- `owner` - 按所有者过滤（可选）
- `search` - 搜索词（可选）
- `pageSize` - 每页显示的结果数量（可选）

**示例：**
```json
{
  "owner": "google"
}
```

**响应：**
```json
{
  "models": [
    {
      "id": 1,
      "owner": "google",
      "slug": "gemma",
      "title": "Gemma",
      "subtitle": "Gemma is a family of lightweight, state-of-the-art models",
      "instanceCount": 16,
      "framework": "transformers"
    }
  ]
}
```

#### 获取模型

```bash
POST /kaggle/v1/models.ModelApiService/GetModel
Content-Type: application/json

{
  "ownerSlug": "google",
  "modelSlug": "gemma"
}
```

**响应：**
```json
{
  "id": 1,
  "title": "Gemma",
  "slug": "gemma",
  "owner": "google",
  "subtitle": "Gemma is a family of lightweight, state-of-the-art models",
  "publishTime": "2024-02-21T16:00:00Z",
  "instanceCount": 16
}
```

---

### 竞赛

#### 列出竞赛

```bash
POST /kaggle/v1/competitions.CompetitionApiService/ListCompetitions
Content-Type: application/json

{}
```

**请求体参数：**
- `search` - 搜索词（可选）
- `category` - 按类别过滤（可选）
- `pageSize` - 每页显示的结果数量（可选）

**示例：**
```json
{
  "search": "nlp"
}
```

**响应：**
```json
{
  "competitions": [
    {
      "id": 118448,
      "ref": "https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3",
      "title": "AI Mathematical Olympiad - Progress Prize 3",
      "url": "https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3",
      "deadline": "2026-06-06T23:59:00Z",
      "category": "Featured",
      "reward": "$1,048,576",
      "teamCount": 1234,
      "userHasEntered": false
    }
  ]
}
```

---

### 核心（Notebooks）

#### 列出核心（Notebooks）

```bash
POST /kaggle/v1/kernels.KernelsApiService/ListKernels
Content-Type: application/json

{}
```

**请求体参数：**
- `search` - 搜索词（可选）
- `user` - 按用户名过滤（可选）
- `language` - 按语言过滤（如`python`、`r`等）（可选）
- `pageSize` - 每页显示的结果数量（可选）

**示例：**
```json
{
  "search": "titanic"
}
```

**响应：**
```json
{
  "kernels": [
    {
      "id": 5660537,
      "ref": "alexisbcook/titanic-tutorial",
      "title": "Titanic Tutorial",
      "author": "alexisbcook",
      "language": "Python",
      "totalVotes": 1234,
      "totalViews": 56789
    }
  ]
}
```

#### 获取核心（Kernel）

```bash
POST /kaggle/v1/kernels.KernelsApiService/GetKernel
Content-Type: application/json

{
  "userName": "alexisbcook",
  "kernelSlug": "titanic-tutorial"
}
```

**响应：**
```json
{
  "metadata": {
    "id": 5660537,
    "ref": "alexisbcook/titanic-tutorial",
    "title": "Titanic Tutorial",
    "author": "alexisbcook",
    "language": "Python"
  }
}
```

---

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/kaggle/v1/datasets.DatasetApiService/ListDatasets',
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ search: 'covid' })
  }
);
const data = await response.json();
console.log(data);
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/kaggle/v1/datasets.DatasetApiService/ListDatasets',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={'search': 'covid'}
)
print(response.json())
```

---

## 注意事项

- 所有API调用都使用POST方法，并且请求体为JSON格式。
- API遵循RPC模式：`/v1/{ServiceName}/{MethodName}`。
- 数据集的引用格式为：`{owner}/{dataset-slug}`。
- 模型的引用格式为：`{owner}/{model-slug}`。
- 核心的引用格式为：`{user}/{kernel-slug}`。
- 下载端点返回二进制数据（ZIP文件）。
- 某些操作需要特定的权限（例如参与竞赛或访问核心）。

## 错误处理

| 状态码 | 含义 |
|--------|---------|
| 200 | 成功 |
| 400 | 请求参数无效 |
| 401 | 认证无效或缺失 |
| 403 | 权限被拒绝 |
| 404 | 资源未找到 |
| 429 | 请求频率受限 |

## 资源

- [Kaggle API文档](https://www.kaggle.com/docs/api)
- [Kaggle数据集](https://www.kaggle.com/datasets)
- [Kaggle模型](https://www.kaggle.com/models)
- [Kaggle竞赛](https://www.kaggle.com/competitions)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)