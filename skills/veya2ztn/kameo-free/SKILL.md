---
name: kameo
description: 使用 Kameo AI 从静态图像生成富有表现力的头像视频。该工具可以将静态头像或肖像转换为时长为 5 秒的动态视频，这些视频包含逼真的面部表情、唇形同步以及动作效果。适用于需要让静态图像“活起来”的场景，例如制作 AI 角色视频、展示视觉沟通内容，或从照片中生成可说话的头像。
---

# Kameo AI – 生成具有真实动作和口型的头像视频

将静态图片转换为表情丰富、具有真实动作和口型的头像视频。

## 快速入门

```bash
scripts/generate_video.sh <image_path> <prompt> [output_file]
```

**示例：**
```bash
scripts/generate_video.sh avatar.jpg "Hello, I am an AI assistant" output.mp4
```

## 功能介绍

- 接收一张静态图片（肖像/头像）
- 根据您的提示添加真实的面部动作、表情和口型同步
- 生成时长为5秒的视频，支持9:16、16:9或1:1的宽高比
- 立即返回视频的CDN链接（处理时间约10-30秒）

## 认证

设置您的Kameo API密钥：
```bash
export KAMEO_API_KEY="kam_I3rdx43IymFNbfBw1c0ZbSc7o3aUfQgz8cljZA6T7fs"
```

或者将其存储在`~/.config/kameo/credentials.json`文件中：
```json
{
  "api_key": "kam_I3rdx43IymFNbfBw1c0ZbSc7o3aUfQgz8cljZA6T7fs"
}
```

**获取API密钥：**

1. 在kameo.chat注册（需要验证邮箱）
2. 登录以获取JWT令牌
3. 通过`/api/public/keys`端点创建API密钥
4. 或者使用辅助工具`scripts/register.sh`进行注册

## 提示设计

### 基本提示（简单）

仅提供对话内容：
```
"Hello, I'm here to help you today"
"こんにちは、私はガッキーです。愛してます。"
```

虽然可以生成视频，但效果较为普通。

### 高级提示（推荐）

**格式：**
```
[Detailed scene/environment], [person's complete appearance and expression], speaking in [tone], "[DIALOGUE]". [Camera and lighting details].
```

**示例：**
```
In a bright outdoor winter setting with soft, overcast daylight, a young woman with long dark hair wearing a white knitted winter hat with ear flaps and a colorful patterned sweater stands centered in frame. She looks directly into the camera with a warm, genuine smile, her eyes crinkling with joy, speaking in a cheerful, affectionate tone, "こんにちは、私はガッキーです。愛してます。" The scene is captured in a medium close-up shot, framed at eye level. The lighting is natural and diffused from above, creating soft, even illumination.
```

**高级提示的重要性：**
- 更符合场景背景的面部表情
- 更自然的动作和手势
- 更优质的口型同步效果
- 更贴合情境的情感表达

### 提示优化流程

为了获得最佳效果，请先使用视觉AI分析图片：

1. 将图片输入到视觉模型（如Gemini、GPT-4V、Claude）中
2. 让模型详细描述场景
3. 将您的对话内容插入描述中
4. 使用优化后的提示来生成视频

**参考：`scripts/enhance_prompt.sh`以获取自动化优化功能。**

## API详情

**基础URL：** `https://api.kameo.chat/api/public`

### 生成视频

```bash
curl -X POST https://api.kameo.chat/api/public/generate \
  -H "X-API-Key: kam_I3rdx43IymFNbfBw1c0ZbSc7o3aUfQgz8cljZA6T7fs" \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "<base64_encoded_image>",
    "prompt": "Your detailed prompt here",
    "seconds": 5,
    "aspect_ratio": "9:16"
  }'
```

**参数：**
- `image_base64`（必填）：Base64编码的JPEG/PNG图片
- `prompt`（必填）：对话内容或场景描述
- `seconds`（可选）：5秒（默认）或10秒
- `aspect_ratio`（可选）："9:16"（默认）、"16:9"或"1:1"

**响应：**
```json
{
  "job_id": "uuid",
  "status": "completed",
  "video_url": "https://cdn.kameo.chat/videos/{uuid}.mp4",
  "duration_seconds": 5,
  "processing_time_ms": 15000
}
```

### 查看剩余信用

```bash
curl -H "X-API-Key: kam_..." \
  https://api.kameo.chat/api/public/credits
```

**响应：**
```json
{
  "permanent_credits": 294,
  "subscription_credits": 0,
  "total_available": 294
}
```

## 价格

**费用：** 每个视频3个信用点

## 性能

- **处理时间：** 8-35秒（取决于宽高比和队列情况）
- **9:16（肖像）：** 约30-35秒
- **16:9（横屏）：** 约15-20秒
- **1:1（正方形）：** 约10-15秒

## 最佳实践

1. **优化图片大小**：在编码前调整图片大小（节省带宽，加快上传速度）
   ```bash
   ffmpeg -i large.jpg -vf scale=720:-1 optimized.jpg
   ```

2. **使用详细的提示**：高级提示可生成更好的效果

3. **合理选择宽高比**
   - 9:16：适用于移动设备/社交媒体（如TikTok、Instagram Stories）
   - 16:9：适用于桌面/YouTube
   - 1:1：适用于个人资料图片或正方形帖子

4. **监控信用点数**：使用`scripts/check_credits.sh`查看剩余信用

## 限制

- **CDN访问：** 视频链接可能具有时间限制或需要认证
- **下载：** 使用curl下载视频时可能会收到403错误（建议使用浏览器或已认证的会话）
- **使用限制：** 每分钟最多生成10个视频

## 故障排除

**“401未经授权”**
- 确保API密钥设置正确
- 验证密钥是否已被吊销

**“402信用不足”**
- 查看剩余信用点数：`scripts/check_credits.sh`
- 需要在kameo.chat补充信用点数

**“超时错误”**
- 9:16格式的视频处理时间较长（约30秒）
- 增加脚本中的超时设置
- 如果服务器繁忙，请稍后重试

**“下载视频时出现403错误”**
- CDN链接可能具有时间限制
- 建议在视频生成后立即通过浏览器访问
- 或者保存生成的Base64编码内容

## 应用场景

- **AI角色视频**：让机器人头像动起来
- **社交媒体内容**：动态的个人资料视频
- **演示文稿**：带有AI演示者的产品展示
- **教育内容**：包含AI讲解者的视频教程
- **多语言内容**：同一个头像使用不同语言进行演讲