---
name: alicloud-ai-video-wan-video
description: 使用 Model Studio DashScope SDK 和 wan2.6-i2v-flash 模型生成视频。该功能适用于实现或记录 `video.generate` 请求/响应的处理过程，以及配置参数（如 `prompt`、`negative_prompt`、`duration`、`fps`、`size`、`seed`、`reference_image`、`motion_strength`）的设置；同时也可用于将视频生成功能集成到视频代理（video-agent）的流程中。
---

**类别：提供者（Provider）**

# Model Studio Wan Video

通过标准化 `video.generate` 的输入/输出参数，并使用 DashScope SDK（Python）以及正确的模型名称，为视频生成流程提供一致的行为。

## 关键模型名称

**仅使用以下确切的模型字符串：**
- `wan2.6-i2v-flash`

**请勿添加日期后缀或别名。**

## 先决条件**

- 安装 SDK（建议在虚拟环境（venv）中安装，以避免违反 PEP 668 的限制）：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```

- 在您的环境中设置 `DASHSCOPE_API_KEY`，或将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中（环境变量优先级更高）。

## 规范化的接口（`video.generate`）

### 请求参数
- `prompt`（字符串，必填）
- `negative_prompt`（字符串，可选）
- `duration`（数字，必填）：秒
- `fps`（数字，必填）
- `size`（字符串，必填）：例如 `1280*720`
- `seed`（整数，可选）
- `reference_image`（字符串 | 字节流，对于 `wan2.6-i2v-flash` 是必填的）
- `motion_strength`（数字，可选）

### 响应参数
- `video_url`（字符串）
- `duration`（数字）
- `fps`（数字）
- `seed`（整数）

## 快速入门（Python + DashScope SDK）

视频生成通常是异步的。您需要获取任务 ID 并持续轮询直到任务完成。
**注意：** `wan2.6-i2v-flash` 需要一个输入图像；请将 `reference_image` 映射到 `img_url`。

```python
import os
from dashscope import VideoSynthesis

# Prefer env var for auth: export DASHSCOPE_API_KEY=...
# Or use ~/.alibabacloud/credentials with dashscope_api_key under [default].

def generate_video(req: dict) -> dict:
    payload = {
        "model": "wan2.6-i2v-flash",
        "prompt": req["prompt"],
        "negative_prompt": req.get("negative_prompt"),
        "duration": req.get("duration", 4),
        "fps": req.get("fps", 24),
        "size": req.get("size", "1280*720"),
        "seed": req.get("seed"),
        "motion_strength": req.get("motion_strength"),
        "api_key": os.getenv("DASHSCOPE_API_KEY"),
    }

    if req.get("reference_image"):
        # DashScope expects img_url for i2v models; local files are auto-uploaded.
        payload["img_url"] = req["reference_image"]

    response = VideoSynthesis.call(**payload)

    # Some SDK versions require polling for the final result.
    # If a task_id is returned, poll until status is SUCCEEDED.
    result = response.output.get("results", [None])[0]

    return {
        "video_url": None if not result else result.get("url"),
        "duration": response.output.get("duration"),
        "fps": response.output.get("fps"),
        "seed": response.output.get("seed"),
    }
```

## 异步处理（轮询）

```python
import os
from dashscope import VideoSynthesis

task = VideoSynthesis.async_call(
    model="wan2.6-i2v-flash",
    prompt=req["prompt"],
    img_url=req["reference_image"],
    duration=req.get("duration", 4),
    fps=req.get("fps", 24),
    size=req.get("size", "1280*720"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
)

final = VideoSynthesis.wait(task)
video_url = final.output.get("video_url")
```

## 操作指南

- 视频生成可能需要几分钟时间；请显示进度并允许用户取消或重试操作。
- 使用 `(prompt, negative_prompt, duration, fps, size, seed, reference_image_hash, motion_strength)` 作为缓存键。
- 将视频文件存储在对象存储中，并仅在元数据中保存视频的 URL。
- `reference_image` 可以是 URL 或本地路径；SDK 会自动上传本地文件。
- 如果出现 “Field required: input.img_url” 的错误，说明参考图像缺失或未正确映射。

## 关于视频尺寸的注意事项

- 使用 `WxH` 格式（例如 `1280*720`）。
- 建议使用常见的视频尺寸；不支持的尺寸可能会导致生成失败（返回错误代码 400）。

## 输出位置

- 默认输出路径：`output/ai-video-wan-video/videos/`
- 可通过 `OUTPUT_DIR` 变量覆盖默认输出目录。

## 避免的错误做法

- 不要自定义模型名称或别名；请始终使用 `wan2.6-i2v-flash`。
- 在没有进度更新时不要阻塞用户界面。
- 对于 4xx 错误，请不要盲目重试；应明确处理验证失败的情况。

## 参考资料

- 有关 DashScope SDK 的使用方法和异步处理的详细信息，请参阅 `references/api_reference.md`。
- 源代码列表：`references/sources.md`