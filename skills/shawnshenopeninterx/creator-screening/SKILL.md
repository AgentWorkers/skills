---
name: creator-screening
description: 使用可配置的质量评估框架来筛选和评估社交媒体创作者/影响者。通过 Memories.ai V2 视频理解 API 分析 Instagram、TikTok 和 YouTube 上的创作者内容：该 API 可获取创作者的个人信息（元数据），对视频进行视觉和音频方面的 AI 分析，并根据制作质量、音频质量、内容呈现方式以及创作者在平台上的定位等因素进行评分。适用于需要审核创作者、筛选影响者、评估内容质量或生成创作者报告的场景。
metadata:
  openclaw:
    emoji: "🎯"
---
# 创作者筛选工具

该工具利用 **Memories.ai V2 视频理解 API** 实现自动化创作者/影响者筛选功能。

## 参数

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| `videos_per_creator` | 5 | 每位创作者需分析的视频数量 |
| `video_seconds` | 30 | 每个视频的分析时长（前 N 秒） |
| `platforms` | instagram | 支持的平台：instagram、tiktok、youtube |
| `analysis_mode` | `mai` | `mai`（视觉+音频 AI 分析）或 `transcript`（仅音频分析） |
| `framework` | default | 适用的筛选框架（详见 `references/frameworks/`） |
| `output_format` | discord | `discord`、`pdf`（Google Doc→PDF）或 `json` |
| `batch_size` | 10 | 每批处理的创作者数量 |

## 快速入门

```
Screen these creators: @anshmehra.in, @nishkarshsharmaa
Parameters: videos_per_creator=3, framework=cac-crusher
```

## 工作流程

### 第 1 步：解析输入
接受任何格式的创作者链接：
- Instagram 个人资料：`https://www.instagram.com/username/`
- Instagram 视频：`https://www.instagram.com/reel/SHORTCODE/`
- YouTube 视频：`https://www.youtube.com/@channel` 或 `/shorts/ID`

### 第 2 步：获取创作者和视频元数据

**使用 Memories.ai V2** 进行请求：`POST /instagram/video/metadata`

```bash
python3 scripts/scrape_profiles.py --urls "reel_url1,reel_url2" --channel rapid
```

返回每个视频的元数据（费用：$0.01/视频）：
- **创作者信息**：用户名、全名、粉丝数量、账号是否已认证、个人资料图片
- **视频信息**：观看次数、播放次数、时长、视频标题、评论、视频尺寸、音频信息

### 第 3 步：视频分析（MAI）

**使用 Memories.ai V2 的 MAI** 进行请求：`POST /instagram/video/mai/transcript`

这是核心分析步骤。MAI 提供以下信息：
- **视觉场景分析**：光线质量、拍摄构图、环境、服装、制作水平
- **音频转录**：带有时间戳的语音转文本
- **内容理解**：主题分类、表达方式、内容结构

```bash
python3 scripts/analyze_videos.py --mode mai --videos_per_creator 5 --urls "url1,url2"
```

每个视频都会返回视觉和音频的 AI 分析结果。根据这些结果评估以下方面：
- 第 2.1 节：视觉与氛围（光线、环境、构图）
- 第 2.2 节：音频质量（清晰度、回声、连贯性）
- 第 3.x 节：表达与内容（结构、流畅度、成熟度）
- 第 4 节：整体风格（语气、感染力、品牌安全性）

**备用方案**：如果 MAI 不可用，可使用 `--mode transcript` 仅进行音频分析：

```bash
python3 scripts/analyze_videos.py --mode transcript --videos_per_creator 5 --urls "url1,url2"
```

### 第 4 步：应用筛选框架

根据选定的筛选框架对创作者进行评分：

```bash
python3 scripts/score_creator.py --framework cac-crusher --profile profile.json --transcripts transcripts.json
```

可用筛选框架位于 `references/frameworks/` 目录中：
- `cac-crusher.md` — CAC Crusher 创作者筛选框架（针对演讲者和短片）
- `default.md` — 通用质量筛选框架（5 个维度，加权评分）
- `template.md` — 自定义筛选框架的模板

### 第 5 步：生成报告

输出每位创作者的筛选结果，包括：
- 个人资料信息（粉丝数量、账号认证状态、互动情况）
- 各项评估结果（通过/失败/标记）
- 作为证据的音频转录片段
- MAI 提供的视觉质量评估
- 最终判断（通过/拒绝/条件性通过）

## Memories.ai V2 API 参考

所有 API 都需要使用以下请求头：`Authorization: <API_KEY>`（无需添加 `Bearer` 前缀）
基础 URL：`https://mavi-backend.memories.ai/serve/api/v2`

| API 端点 | 方法 | 用途 | 费用 |
|----------|--------|-----|------|
| `/{platform}/video/metadata` | POST | 获取创作者和视频元数据 | $0.01/视频 |
| `/{platform}/video/mai/transcript` | POST | 视觉+音频 AI 分析 | 约 $0.11/视频 |
| `/{platform}/video/transcript` | POST | 仅音频转录 | 约 $0.01/视频 |

支持的平台：instagram、tiktok、youtube、twitter

**请求体示例**：`{"video_url": "...", "channel": "rapid"}`
**MAI 响应格式**：`{"data": {"task_id": "..."}`（异步处理，结果通过 webhook 发送）

**注意事项**：
- Instagram 的视频链接格式必须为 `/reel/SHORTCODE/`（而非 `/p/` 或 `/reels/`）

## 错误处理
- 在每次 API 调用之间添加 0.5 秒的延迟
- 失败的请求重试一次，若仍失败则跳过该请求
- 如果未收到 MAI 的响应，切换到仅音频分析模式
- 始终将 Instagram 的链接格式统一为 `/reel/`（无论原始链接是 `/p/` 还是 `/reels/`）