---
name: dream-avatar
description: "使用 DreamAvatar 3.0 Fast API，您可以从图片和音频生成具有对话功能的数字人头像视频。该服务由 Dreamface 提供支持——Dreamface 是一款面向所有人的 AI 工具。更多 AI 产品（包括移动应用、网页版和 PC 版）请访问：https://tools.dreamfaceapp.com/home。该 API 支持通过 URL 输入或上传本地文件来生成视频。当用户需要创建一个会说话的数字人头像视频时，可以尝试使用该服务。API 资源文档请参考：https://api.newportai.com/api-reference/get-started"
metadata: {"openclaw": {"emoji": "🎬", "requires": {"env": ["DREAM_API_KEY"]}, "primaryEnv": "DREAM_API_KEY"}}
---
# DreamAvatar - 数字人视频生成器

使用 DreamAvatar 3.0 快速 API，可以从图片和音频生成会说话的数字人视频。

## 快速入门

### 1. 获取 API 密钥

在使用此功能之前，您需要一个 DreamAPI API 密钥。请访问 **https://api.newportai.com/api-reference/get-started** 进行注册并获取您的 API 密钥。

更多 AI 工具，请访问：**https://tools.dreamfaceapp.com/home**

### 2. 配置 API 密钥

用户必须在 OpenClaw 配置中设置他们的 DreamAPI 密钥：

```bash
openclaw config patch --json '{"skills": {"entries": {"dream-avatar": {"env": {"DREAM_API_KEY": "your-api-key-here"}}}}}'
```

或者将其添加到 `~/.openclaw/openclaw.json` 文件中：
```json
{
  "skills": {
    "entries": {
      "dream-avatar": {
        "env": {
          "DREAM_API_KEY": "your-api-key"
        }
      }
    }
  }
}
```

### 3. 生成视频

您可以通过两种方式提供输入：

#### 选项 A：本地文件（推荐）
- **image**：本地图片文件的路径（jpg、jpeg、png、webp、gif）
- **audio**：本地音频文件的路径（mp3、wav、mp4，最长 3 分钟）
- **prompt**：所需表情/行为的描述
- **resolution**（可选）：“480p”或“720p”，默认为“480p”

该功能会自动上传您的本地文件并生成视频。

#### 选项 B：公共 URL
- **image**：可公开访问的图片 URL（jpg、jpeg、png、webp、gif）
- **audio**：可公开访问的音频 URL（mp3、wav、mp4，最长 3 分钟）
- **prompt**：所需表情/行为的描述
- **resolution**（可选）：“480p”或“720p”，默认为“480p”

## API 详细信息

### 1. 获取上传策略
```
POST https://api.newportai.com/api/file/v1/get_policy
```

**请求头：**
```
Authorization: Bearer {DREAM_API_KEY}
Content-Type: application/json
```

**请求体：**
```json
{
  "scene": "Dream-CN"
}
```

**响应：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "accessId": "LTAI5tF1QzxoHGvEcziVACyc",
    "policy": "eyJ0...",
    "signature": "G2TzrhlybemHbfFakysY4j2EI2I=",
    "dir": "tmp/dream/2024-11-19/5369207820989002/",
    "host": "https://...",
    "expire": "1732005888",
    "callback": "eyJ0..."
  }
}
```

### 2. 上传文件到 OSS

**表单数据：**
| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| policy | 字符串 | 是 | 从 get_policy API 获取的上传策略 |
| OSSAccessKeyId | 字符串 | 是 | 从 get_policy API 获取的访问 ID |
| success_action_status | 字符串 | 是 | 固定值：“200” |
| signature | 字符串 | 是 | 从 get_policy API 获取的签名 |
| key | 字符串 | 是 | 完整路径：目录 + 文件名 |
| callback | 字符串 | 是 | 从 get_policy API 获取的回调函数 |
| file | 二进制数据 | 是 | 文件内容（必须是最后一个参数） |

**响应：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "verifyStatus": false,
    "reqId": "732c9caa-0a2e-4aa1-87d9-52430a8f0314"
  }
}
```

上传后的文件 URL 为：`{host}/{key}`

### 3. 生成视频（图片转视频）
```
POST https://api.newportai.com/api/async/dreamavatar/image_to_video/3.0fast
```

**请求头：**
```
Authorization: Bearer {DREAM_API_KEY}
Content-Type: application/json
```

**请求体：**
```json
{
  "image": "https://.../photo.jpg",
  "audio": "https://.../speech.mp3",
  "prompt": "a person smiling and speaking",
  "resolution": "480p"
}
```

**响应（任务提交）：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "taskId": "aa4bf173ffd84c2f8734d536d6a7b5a7"
  }
}
```

### 4. 查询结果

使用 taskId 来查询结果：
```
POST https://api.newportai.com/api/getAsyncResult
```

请求体：
```json
{
  "taskId": "your-task-id"
}
```

**结果完成时的响应：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "task": {
      "taskId": "aa4bf173ffd84c2f8734d536d6a7b5a7",
      "status": 3,
      "taskType": "dreamavatar/image_to_video/3.0fast"
    },
    "videos": [
      {
        "videoType": "mp4",
        "videoUrl": "https://...video.mp4"
      }
    ]
  }
}
```

## 实现说明

- **本地文件**：该功能会自动处理上传。文件将被上传到 OSS 并生成相应的 URL。
- **URL 输入**：图片和音频的 URL 必须是可公开访问的（不能需要身份验证）。
- **音频时长**：不得超过 3 分钟。
- **API 是异步的**：您需要定期查询结果。
- **建议每 2-3 秒查询一次**，超时时间为约 60 秒。
- **状态码**：0 = 待处理，1 = 处理中，2 = 处理中（未失败！），3 = 完成，4 = 超时。
- **上传的文件 URL**：仅有效期为 1 天（存储服务是免费的，但仅用于 AI 程序支持）。

## 上传流程

```
Local File → Get Upload Policy → Upload to OSS → Get Public URL → Generate Video
```

当提供本地文件时，该功能会自动执行以下流程：
1. 调用 `get_policy` 获取 OSS 凭据。
2. 将图片/音频上传到 OSS。
3. 从主机地址和密钥生成公共 URL。
4. 使用上传的 URL 调用 DreamAvatar API。
5. 查询视频生成进度。
6. 返回最终的视频 URL。