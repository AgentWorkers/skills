---
name: evolink-video
description: AI视频生成工具：Sora、Kling、Veo 3、Seedance、Hailuo、WAN、Grok。支持文本转视频、图片转视频以及视频编辑功能。共37个模型，只需一个API密钥即可使用。
version: 1.1.0
metadata:
  openclaw:
    requires:
      env:
        - EVOLINK_API_KEY
    primaryEnv: EVOLINK_API_KEY
    emoji: 🎬
    homepage: https://evolink.ai
---
# Evolink Video — 人工智能视频生成服务

通过37个视频模型（包括Sora、Kling、Veo 3、Seedance、Hailuo、WAN和Grok）生成AI视频。支持文本转视频、图片转视频、提取视频的首尾帧、视频编辑以及音频生成等功能，所有这些功能都可通过同一个API实现。

> 这是[evolink-media](https://clawhub.ai/EvoLinkAI/evolink-media)中的视频相关功能。如需图像和音乐生成服务，请安装完整的evolink技能包。

## 设置

请在[evolink.ai](https://evolink.ai)获取您的API密钥，并将其设置为`EVOLINK_API_KEY`。

## MCP工具

| 工具 | 功能 |
|------|---------|
| `generate_video` | 从文本或图片生成AI视频 |
| `upload_file` | 上传本地图片/视频以用于视频转换或编辑 |
| `delete_file` | 删除上传的文件以释放存储空间 |
| `list_files` | 查看上传的文件并检查存储空间使用情况 |
| `check_task` | 监控生成进度并获取结果URL |
| `list_models` | 浏览可用的视频模型 |
| `estimate_cost` | 查看模型价格 |

## 视频模型（共37个）

### 推荐模型

| 模型 | 适用场景 | 特点 |
|-------|----------|----------|
| `seedance-1.5-pro` *(默认)* | 图片转视频、提取视频首尾帧 | 支持i2v转换，时长4–12秒，分辨率1080p，支持音频 |
| `sora-2-preview` | 电影级预览效果 | 支持文本转视频（t2v），分辨率1080p |
| `kling-o3-text-to-video` | 文本转视频，分辨率1080p | 支持文本转视频功能 |
| `veo-3.1-generate-preview` | 谷歌视频风格的预览效果 | 支持文本转视频（t2v），分辨率1080p |
| `MiniMax-Hailuo-2.3` | 高质量视频生成 | 支持文本转视频（t2v），分辨率1080p |
| `wan2.6-text-to-video` | 阿里巴巴最新开发的文本转视频模型 | 支持文本转视频（t2v） |
| `sora-2` [测试版] | 电影级效果，严格遵循用户提示 | 支持文本转视频（t2v）和图片转视频（i2v），分辨率1080p |
| `veo3.1-pro` [测试版] | 最高质量视频生成，支持音频 | 支持文本转视频（t2v），分辨率1080p，支持音频 |

### 所有稳定运行的模型（共26个）

`seedance-1.5-pro`, `seedance-2.0`, `doubao-seedance-1.0-pro-fast`, `sora-2-preview`, `kling-o3-text-to-video`, `kling-o3-image-to-video`, `kling-o3-reference-to-video`, `kling-o3-video-edit`, `kling-v3-text-to-video`, `kling-v3-image-to-video`, `kling-o1-image-to-video`, `kling-o1-video-edit`, `kling-o1-video-edit-fast`, `kling-custom-element`, `veo-3.1-generate-preview`, `veo-3.1-fast-generate-preview`, `MiniMax-Hailuo-2.3`, `MiniMax-Hailuo-2.3-Fast`, `MiniMax-Hailuo-02`, `wan2.5-t2v-preview`, `wan2.5-i2v-preview`, `wan2.5-text-to-video`, `wan2.5-image-to-video`, `wan2.6-text-to-video`, `wan2.6-image-to-video`, `wan2.6-reference-video`

### 所有测试版模型（共11个）

`sora-2`, `sora-2-pro`, `sora-2-beta-max`, `sora-character`, `veo3.1-pro`, `veo3.1-fast`, `veo3.1-fast-extend`, `veo3`, `veo3-fast`, `grok-imagine-text-to-video`, `grok-imagine-image-to-video`

## 参数

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `prompt` | 字符串 | — | 视频描述（必填） |
| `model` | 枚举 | `seedance-1.5-pro` | 使用的模型 |
| `duration` | 整数 | 模型默认值 | 视频时长（秒） |
| `aspect_ratio` | 枚举 | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9` | 视频宽高比 |
| `quality` | 枚举 | 模型默认值 | 视频分辨率（480p / 720p / 1080p / 4k） |
| `image_urls` | 字符串数组 | — | 用于视频转换的参考图片路径 |
| `generate_audio` | 布尔值 | 模型默认值 | 是否自动生成音频（仅限`seedance-1.5-pro`和`veo3.1-pro`） |

## 文件上传

在进行图片转视频或视频编辑时，请先上传本地文件：

1. 使用`upload_file`函数，传入`file_path`、`base64_data`或`file_url`，以获取`file_url`（操作为同步执行）。
2. 将获取到的`file_url`作为`generate_video`函数的`image_urls`参数传入。

**支持格式：** 图片（JPEG/PNG/GIF/WebP）/ 视频（所有格式）。文件大小上限为100MB，文件有效期为72小时。存储配额：默认为100个文件，VIP用户可上传500个文件。

## 工作流程

1. 如有需要，上传参考图片/视频（使用`upload_file`函数）。
2. 调用`generate_video`函数以开始视频生成。
3. 每10–15秒调用`check_task`函数检查生成进度。
4. 下载生成结果（结果URL的有效期为24小时）。