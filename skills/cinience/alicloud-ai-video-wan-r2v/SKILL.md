---
name: alicloud-ai-video-wan-r2v
description: 使用 Alibaba Cloud Model Studio Wan R2V (wan2.6-r2v-flash) 生成基于参考的视频。该工具适用于从参考视频/图像素材创建多帧视频、保持角色风格的一致性，或记录视频请求/响应的处理流程。
---

**类别：提供者（Provider）**

# Model Studio Wan R2V

使用 Wan R2V 生成视频参考文件。这与 i2v（从单张图片生成视频）的功能不同。

## 关键模型名称

**仅使用以下确切的模型名称：**
- `wan2.6-r2v-flash`

## 先决条件

- 在虚拟环境中安装 SDK：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```

- 在您的环境中设置 `DASHSCOPE_API_KEY`，或将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中。

## 标准化接口（video.generate_reference）

### 请求参数
- `prompt`（字符串，必填）
- `reference_video`（字符串 | 字节数据，必填）
- `reference_image`（字符串 | 字节数据，可选）
- `duration`（数字，可选）
- `fps`（数字，可选）
- `size`（字符串，可选）
- `seed`（整数，可选）

### 响应参数
- `video_url`（字符串）
- `task_id`（字符串，异步请求时返回）
- `request_id`（字符串）

## 异步处理

- 对于生产环境中的请求，建议使用异步提交方式。
- 以 15-20 秒的间隔轮询任务结果。
- 当返回 `SUCCEEDED` 或终端故障状态时，停止轮询。

## 本地辅助脚本

准备一个标准化的请求 JSON 数据，并验证响应数据结构：

```bash
.venv/bin/python skills/ai/video/alicloud-ai-video-wan-r2v/scripts/prepare_r2v_request.py \
  --prompt "Generate a short montage with consistent character style" \
  --reference-video "https://example.com/reference.mp4"
```

## 输出路径

- 默认输出路径：`output/ai-video-wan-r2v/videos/`
- 可通过 `OUTPUT_DIR` 变量覆盖默认路径。

## 参考资料

- `references/sources.md`