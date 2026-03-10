---
name: tomoviee-redrawing
description: 使用掩码重新绘制图像的特定区域（白色表示需要重新绘制，黑色表示保持原样）。适用于用户请求图像重新绘制操作或相关任务的情况。
---
# Tomoviee AI - 图像重绘 (Image Redrawing)

## 概述

使用掩码（白色区域表示需要重绘，黑色区域表示保持原样）来重新绘制图像的特定区域。

**API**: `tm_redrawing`

## 快速入门

### 认证

```bash
python scripts/generate_auth_token.py YOUR_APP_KEY YOUR_APP_SECRET
```

### Python 客户端

```python
from scripts.tomoviee_image_redrawing_client import TomovieeClient

client = TomovieeClient("app_key", "app_secret")
```

## API 使用方法

### 基本示例

```python
task_id = client._make_request({
    prompt='Clear blue sky with fluffy clouds'
    image='https://example.com/photo.jpg'
})

result = client.poll_until_complete(task_id)
import json
output = json.loads(result['result'])
```

### 参数

- `prompt` (必填): 需要重绘区域的描述
- `image` (必填): 原始图像的 URL
- `mask` (必填): 掩码图像的 URL
- `resolution`: `512*512`, `768*768`, `1024*1024`
- `image_num`: 变体数量（1-4）

## 异步工作流程

1. **创建任务**: 通过 API 调用获取 `task_id`
2. **检查任务完成情况**: 使用 `poll_until_complete(task_id)` 监控任务进度
3. **提取结果**: 解析返回的 JSON 数据以获取输出图像的 URL

**状态代码**:
- 1 = 排队中
- 2 = 处理中
- 3 = 成功（已完成）
- 4 = 失败
- 5: 取消
- 6: 超时

## 资源

### 脚本/
- `tomoviee_image_redrawing_client.py` - API 客户端
- `generate_auth_token.py` - 认证令牌生成器

### 参考资料/
请参阅随附的参考文档以获取详细的 API 文档和示例。

## 外部资源

- **开发者门户**: https://www.tomoviee.ai/developers.html
- **API 文档**: https://www.tomoviee.ai/doc/
- **获取 API 凭据**: 在开发者门户注册