---
name: tomoviee-video-scoring
description: 生成与视频内容相匹配的音乐。适用于用户请求视频音轨相关操作或相关任务的情况。
---
# Tomoviee AI - 视频配乐（Video Soundtrack）

## 概述

Tomoviee AI 可根据视频内容生成定制的音乐。

**API**: `tm_video_scoring`

## 快速入门

### 认证

```bash
python scripts/generate_auth_token.py YOUR_APP_KEY YOUR_APP_SECRET
```

### Python 客户端

```python
from scripts.tomoviee_video_soundtrack_client import TomovieeClient

client = TomovieeClient("app_key", "app_secret")
```

## API 使用方法

### 基本示例

```python
task_id = client._make_request({
    video='https://example.com/my-video.mp4'
    prompt='Modern tech product music, clean'
})

result = client.poll_until_complete(task_id)
import json
output = json.loads(result['result'])
```

### 参数

- `video`（必填）：视频 URL（MP4 格式，文件大小不超过 200MB）
- `prompt`（可选）：音乐风格提示
- `duration`：音频时长（5-900 秒，默认值：20 秒）

## 异步工作流程

1. **创建任务**：通过 API 调用获取任务 ID。
2. **检查任务进度**：使用 `poll_until_complete(task_id)` 函数查询任务完成情况。
3. **提取结果**：解析返回的 JSON 数据以获取音频文件的 URL。

**状态码**：
- 1 = 已排队
- 2 = 正在处理
- 3 = 成功（音频文件已生成）
- 4 = 失败
- 5 = 取消
- 6 = 超时

## 资源

### 脚本文件
- `tomoviee_video_soundtrack_client.py`：API 客户端
- `generate_auth_token.py`：认证令牌生成工具

### 参考资料
请参阅随附的参考文档以获取详细的 API 文档和示例。

## 外部资源

- **开发者门户**：https://www.tomoviee.cn/developers.html
- **API 文档**：https://www.tomoviee.cn/doc/
- **获取 API 认证信息**：在开发者门户上进行注册