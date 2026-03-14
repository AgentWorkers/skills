---
name: background-remover
description: >
  AI背景去除工具：  
  该工具可轻松去除图片中的背景，生成透明PNG格式的图片，适用于电商产品照片、人物肖像、设计素材等场景。支持处理JPG、PNG、WebP格式的本地文件以及远程URL中的图片。  
  **主要功能：**  
  - 一键去除图片背景  
  - 支持多种文件格式（JPG、PNG、WebP）  
  - 适用于多种场景（电商产品、人物肖像、设计素材）  
  **使用说明：**  
  只需将需要处理的照片文件上传到该工具，即可快速获得去除背景后的透明PNG图片。
version: 1.0.0
author: verging.ai
category: media
user-invocable: true
metadata:
  openclaw:
    requires:
      env:
        - VERGING_API_KEY
      bins:
        - curl
    primaryEnv: VERGING_API_KEY
---
# background-remover - 人工智能背景去除工具

通过一键操作，实现图像背景的自动去除，生成透明PNG格式的图片。

## 使用场景

- **电子商务**：去除产品照片的背景，以获得更清晰的产品展示效果。
- **肖像摄影**：去除头像照片的背景，用于专业个人资料。
- **设计**：为图形设计和营销材料创建透明背景图片。

您是一个用于人工智能背景去除功能的命令行（CLI）助手，用户可以通过您来调用verging.ai提供的背景去除服务。

## 用户输入格式

用户需要提供如下命令：
```
/background-remover --image <image file or URL> [options]
```

## 选项

| 选项 | 缩写 | 描述 | 默认值 |
|--------|-------|-------------|---------|
| --image | -i | 目标图片文件路径或URL | 必填 |
| --api-key | -k | 您的API密钥 | 环境变量 VERGING_API_KEY |
| --output | -o | 结果保存路径 | 当前目录 |
| --download | -d | 自动将结果下载到本地 | false |

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| VERGING_API_KEY | 您的API密钥 |
| VERGING_API_URL | API基础URL（默认：https://verging.ai/api/v1） |

## API接口

| 接口 | 方法 | 格式 | 用途 |
|----------|--------|--------|---------|
| /api/v1/auth/me | GET | - | 获取用户信息（包括剩余信用额度） |
| /api/v1/upload-video | POST | 表单数据 | 获取预签名的上传URL |
| /api/v1/background-removal/create-job | POST | 表单数据 | 创建背景去除任务 |
| /api/v1/background-removal/jobs | GET | - | 查询任务状态 |

## 认证

所有API请求都需要通过`Authorization`头部进行认证：

```bash
Authorization: ApiKey <your_api_key>
```

**⚠️ 重要提示：**“ApiKey”和您的API密钥之间需要有一个空格！**

**示例：**
```bash
# ✅ Correct
Authorization: ApiKey vrg_sk_123456...

# ❌ Wrong (missing space)
Authorization: ApiKeyvrg_sk_123456...
```

您可以通过以下链接获取您的API密钥：https://verging.ai（登录 → 点击头像 → API密钥）

### 认证示例

```bash
# Check user info
curl -H "Authorization: ApiKey $VERGING_API_KEY" \
  https://verging.ai/api/v1/auth/me

# Step 1: Get presigned upload URL for image
curl -X POST -H "Authorization: ApiKey $VERGING_API_KEY" \
  -F "video_file_name=image.jpg" \
  -F "job_type=background-removal" \
  https://verging.ai/api/v1/upload-video

# The response contains:
# {
#   "result": {
#     "url": "https://...r2.cloudflarestorage.com/...jpg?X-Amz-...",
#     "public_url": "https://img.panpan8.com/background-removal/2026-03-11/xxx.jpg"
#   }
# }

# Step 2: Upload image to the presigned URL
curl -X PUT -T /path/to/image.jpg \
  "https://...presigned-url-from-step-1..."

# Step 3: Create background removal job
# Use the public_url from Step 2
curl -X POST -H "Authorization: ApiKey $VERGING_API_KEY" \
  -F "image=@/path/to/image.jpg" \
  -F "file_name=image.jpg" \
  -F "job_type=background-removal" \
  https://verging.ai/api/v1/background-removal/create-job

# Query job status
curl -H "Authorization: ApiKey $VERGING_API_KEY" \
  "https://verging.ai/api/v1/background-removal/jobs?job_ids=123"

# List all jobs
curl -H "Authorization: ApiKey $VERGING_API_KEY" \
  https://verging.ai/api/v1/background-removal/jobs
```

**重要提示：**
- 请将`$VERGING_API_KEY`替换为您实际的API密钥，或将其设置为环境变量。
- `Authorization`头部的格式应为`ApiKey <密钥>`（而非`Bearer <密钥>`）

## 所需依赖库

- **curl**：通常已内置在系统中。

## 处理流程

当用户执行`/background-removal`命令时，系统将按照以下步骤进行处理：

### 0. 检查依赖库
- 对于本地图片，无需额外工具。
- 对于远程图片（例如：https://example.com/image.jpg），请使用`curl`下载图片。

### 1. 解析参数
- 解析`--image`参数。
- 如果是远程图片，请先将其下载到本地。

### 2. 检查用户信用额度
- 调用`/api/v1/auth/me`获取用户信息。
- 背景去除服务需要消耗一定的信用额度（通常每张图片1个信用额度）。
- 如果信用额度不足，系统会提示用户重新充值。

### 3. 将图片上传到R2
- 调用`/api/v1/upload-video`并传递相关参数（`video_file_name`、`job_type`）。
- 从响应中获取预签名的上传URL。
- 使用`PUT`方法将图片文件上传到该URL。
- 保存响应中的`public_url`以供后续步骤使用。

### 4. 创建背景去除任务
- 调用`/api/v1/background-removal/create-job`并传递参数：
  - `image`：图片文件（将上传到R2）
  - `file_name`：原始文件名
  - `job_type`：`background-removal`

### 5. 查询任务状态
- 每5秒调用`/api/v1/background-removal/jobs?job_ids=xxx`查询任务进度。
- 状态：待处理（PENDING）→ 处理中（PROCESSING）→ 完成（COMPLETED/FAILED）。
- 显示处理进度百分比。

### 6. 返回结果
- 任务完成后，返回处理后的图片URL。
- 如果用户指定了`--download`或`--output`选项，可以使用`curl`下载结果文件。

## 信用消耗

| 操作 | 所需信用额度 |
|-----------|---------|
| 背景去除（每张图片） | 1个信用额度 |

## 支持的图片格式

- JPG/JPEG
- PNG
- WebP

**图片文件大小限制**：最大10MB

## 示例对话

用户：`/background-removal -i ./photo.jpg`

系统响应：
1. 解析参数（本地图片）。
2. 调用API获取用户信息。
3. 检查信用额度是否足够（1个信用额度）。
4. 将图片上传到R2。
5. 创建背景去除任务。
6. 查询任务完成情况。
7. 返回处理后的图片URL。

用户：`/background-removal -i https://example.com/photo.jpg`

系统响应：
1. 解析参数（远程图片URL）。
2. 将图片下载到本地临时目录。
3. 调用API获取用户信息。
4. 检查信用额度是否足够。
5. 将图片上传到R2。
6. 创建背景去除任务。
7. 查询任务完成情况。
8. 返回处理后的图片URL。

## 注意事项

- API密钥可以通过`--api-key`参数传递，或从环境变量`VERGING_API_KEY`中读取。
- **如果用户未提供API密钥**：系统会提示用户前往https://verging.ai（登录 → 点击用户头像 → API密钥）获取密钥，并指导用户将其设置为环境变量。
- 支持常见的图片格式：JPG、PNG、WebP。
- 处理过程中会显示进度信息。

## 隐私与安全

### API密钥

使用此工具需要**verging.ai的API密钥**。获取方法如下：
1. 访问https://verging.ai。
2. 登录 → 点击用户头像（右上角）→ 选择“API密钥”。
3. 创建新的API密钥。

**安全建议：**
- 使用具有最小权限的专用API密钥。
- 切勿在公共仓库中公开您的API密钥。
- 通过环境变量设置API密钥：`export VERGING_API_KEY="your_key"`。

### 数据处理
- **图片上传**：图片会被上传到verging.ai的R2存储系统进行处理。
- **临时文件**：本地临时文件存储在`/tmp/verging-bg-removal/`目录中，并在处理完成后自动删除。
- **结果图片**：处理后的图片将通过公共URL返回。
- **数据保留**：此工具不会保留用户的任何数据（仅保留会话期间的数据）。