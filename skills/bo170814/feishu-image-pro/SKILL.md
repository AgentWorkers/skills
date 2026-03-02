---
name: feishu-image-pro
description: >
  Feishu 图片上传与发送工具：通过先上传图片，再使用 `image_key` 将图片发送到 Feishu 聊天中。  
  使用方法：`node feishu-image-tool.js send --target <open_id> --file <path>`
---
# Feishu 图片工具

`feishu_image` 工具用于将图片上传到 Feishu 聊天中并发送图片。

## 工作原理

在 Feishu 中，发送图片需要两个步骤：

1. **上传图片** - 调用 `/open-apis/im/v1/images` 上传图片并获取 `image_key`。
2. **发送消息** - 调用 `/open-apis/im/v1/messages`，并设置 `msg_type` 为 "image" 以及 `image_key`。

## 功能操作

### 上传并发送图片

```json
{
  "action": "send",
  "target": "ou_xxx",  // User open_id or chat_id
  "file_path": "/path/to/image.png",
  "message": "Optional caption"
}
```

**参数：**
- `action`: `"send"`
- `target`: Feishu 用户的 open_id 或聊天 ID（当前对话可省略）
- `file_path`: 服务器上图片文件的路径
- `message`: 可选的消息内容（与图片一起发送）

**返回值：**
- `success`: 布尔值，表示操作是否成功
- `image_key`: 上传后的图片键
- `message_id`: 发送的消息 ID

### 仅上传图片

```json
{
  "action": "upload",
  "file_path": "/path/to/image.png"
}
```

返回 `image_key`，以便后续使用。

### 带有图片键的发送

```json
{
  "action": "send_with_key",
  "target": "ou_xxx",
  "image_key": "img_v3_xxx"
}
```

## 图片限制

- **最大大小**：10 MB
- **支持的格式**：JPG、JPEG、PNG、WEBP、GIF、BMP、ICO
- **分辨率**：
  - GIF：最大 2000 x 2000 像素
  - 其他格式：最大 12000 x 12000 像素

## 配置

### Feishu 应用凭证

所需凭证（按优先级排序）：
1. 环境变量：`FEISHU_APP_ID`、`FEISHU_APP_SECRET`
2. 配置文件：`~/.feishu-image/config.json`

```bash
# Method 1: Environment variables
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"

# Method 2: Config file (~/.feishu-image/config.json)
{
  "appId": "cli_xxx",
  "appSecret": "xxx"
}
```

### 所需权限

- `im:message` - 以机器人身份发送消息
- `im:image` - 上传图片

## 权限说明

- `im:message` - 以机器人身份发送消息
- `im:image` - 上传图片

## 使用示例

### 向用户发送股票图表

```json
{
  "action": "send",
  "target": "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "file_path": "/tmp/stock-report.png",
  "message": "📊 今日股票报告"
}
```

### 发送到当前对话（目标参数省略）

```json
{
  "action": "send",
  "file_path": "/tmp/chart.png"
}
```

## 实现说明

- 使用 Feishu SDK `@larksuiteoapi/node-sdk`：
  - 使用 `client.im.image.create()` 上传图片
  - 使用 `client.im.message.create()` 发送消息
- `image_key` 是永久有效的，同一应用可以重复使用。