---
name: alicloud-ai-video-wan-video
description: 使用 Model Studio DashScope SDK 和 Wan i2v 模型（wan2.6-i2v-flash、wan2.6-i2v、wan2.6-i2v-us）生成视频。适用于实现或记录视频生成相关的请求/响应数据，以及配置提示信息（prompt/negative_prompt）、视频时长（duration）、帧率（fps）、视频大小（size）、参考图像（reference_image）、动作强度（motion_strength）等参数。同时，该功能也可用于将视频生成过程集成到视频代理（video-agent）的流程中。
version: 1.0.0
---
**类别：提供者（Provider）**

# Model Studio Wan Video

## 验证（Validation）

```bash
mkdir -p output/alicloud-ai-video-wan-video
python -m py_compile skills/ai/video/alicloud-ai-video-wan-video/scripts/generate_video.py && echo "py_compile_ok" > output/alicloud-ai-video-wan-video/validate.txt
```

**通过标准：**命令执行成功（退出状态码为0），并且生成了 `output/alicloud-ai-video-wan-video/validate.txt` 文件。

## 输出与证据（Output and Evidence）

- 将任务ID、轮询响应以及最终的视频URL保存到 `output/alicloud-ai-video-wan-video/` 目录中。
- 保留一个端到端的运行日志以供故障排查使用。

**注意事项：**  
通过标准化 `video.generate` 的输入/输出参数，并使用 DashScope SDK（Python）以及正确的模型名称，确保视频生成过程的稳定性。

## 关键模型名称（Critical Model Names）

请使用以下模型名称之一：  
- `wan2.2-t2v-plus`  
- `wan2.2-t2v-flash`  
- `wan2.6-i2v-flash`  
- `wan2.6-i2v`  
- `wan2.6-i2v-us`  
- `wan2.6-t2v-us`  
- `wanx2.1-t2v-turbo`

## 先决条件（Prerequisites）

- 安装 SDK（建议在虚拟环境（venv）中安装，以避免 PEP 668 的限制）：  
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashscope
```  
- 在环境中设置 `DASHSCOPE_API_KEY`，或者将 `dashscope_api_key` 添加到 `~/.alibabacloud/credentials` 文件中（环境变量优先级更高）。

## 规范化的接口（Normalized Interface: video.generate）

### 请求（Request）  
- `prompt`（字符串，必填）  
- `negative_prompt`（字符串，可选）  
- `duration`（数字，必填）：视频时长（秒）  
- `fps`（数字，必填）：帧率  
- `size`（字符串，必填）：视频分辨率（例如：`1280*720`）  
- `seed`（整数，可选）  
- `reference_image`（字符串 | 字节数据，t2v模型可选；i2v系列模型必填）  
- `motion_strength`（数字，可选）：动作强度  

### 响应（Response）  
- `video_url`（字符串）：视频URL  
- `duration`（数字）：视频时长  
- `fps`（数字）：帧率  
- `seed`（整数）：随机数种子  

## 快速入门（Python + DashScope SDK）  

视频生成通常是异步的。需要获取任务ID并持续轮询直到任务完成。  
**注意：** Wan i2v模型需要输入图像；纯t2v模型可以省略 `reference_image` 参数。

```python
import os
from dashscope import VideoSynthesis

# Prefer env var for auth: export DASHSCOPE_API_KEY=...
# Or use ~/.alibabacloud/credentials with dashscope_api_key under [default].

def generate_video(req: dict) -> dict:
    payload = {
        "model": req.get("model", "wan2.6-i2v-flash"),
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

## 异步处理（Async Handling: Polling）  

```python
import os
from dashscope import VideoSynthesis

task = VideoSynthesis.async_call(
    model=req.get("model", "wan2.6-i2v-flash"),
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

## 操作指南（Operational Guidance）  

- 视频生成可能需要几分钟时间；请展示生成进度，并提供取消/重试的功能。  
- 使用 `(prompt, negative_prompt, duration, fps, size, seed, reference_image_hash, motion_strength)` 作为缓存键。  
- 将视频文件存储在对象存储中，并仅将视频URL保存在元数据中。  
- `reference_image` 可以是URL或本地路径；SDK会自动上传本地文件。  
- 如果出现错误提示“Field required: input.img_url”，说明参考图像缺失或未正确上传。

## 关于视频分辨率的注意事项（Size Notes）  

- 使用 `WxH` 格式（例如：`1280*720`）。  
- 建议使用常见的视频分辨率；不支持的分辨率可能会导致生成失败（例如返回错误代码400）。  

## 输出路径（Output Location）  

- 默认输出路径：`output/alicloud-ai-video-wan-video/videos/`  
- 可通过 `OUTPUT_DIR` 变量覆盖默认路径。  

## 避免的错误做法（Anti-patterns）  

- 不要自行创建模型名称或别名；请仅使用官方的Wan i2v模型名称。  
- 在没有进度更新的情况下不要阻塞用户界面。  
- 对于4xx错误（表示请求失败），不要盲目重试；应明确处理验证失败的情况。  

## 工作流程（Workflow）  

1) 确认用户的操作意图、所在区域、相关标识符，以及操作是只读还是修改操作。  
2) 首先执行一个最小的只读查询以验证连接性和权限。  
3) 使用明确的参数和受限的范围执行目标操作。  
4) 验证结果并保存输出文件及相关证据。  

## 参考资料（References）  

- 有关DashScope SDK的详细信息，请参阅 `references/api_reference.md`。  
- 源代码列表：`references/sources.md`