---
name: senseaudio-ai-rapper
description: 使用 `/v1/song/lyrics/create`、`/v1/song/lyrics/pending/:task_id`、`/v1/song/music/create` 和 `/v1/song/music/pending/:task_id` 这些 API 来创建和调试 SenseAudio 生成的说唱、嘻哈或声乐歌曲的工作流程。当用户需要说唱歌词、AI 制作的歌曲、风格可控的嘻哈曲目，或者希望查询异步音乐生成任务的进度时，都可以使用这些 API。
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://nightly.senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key for SenseAudio Open Platform
      env_var: SENSEAUDIO_API_KEY
homepage: https://nightly.senseaudio.cn
---
# SenseAudio AI Rapper

使用此技能可完成SenseAudio的音乐生成任务，专注于说唱（rap）、嘻哈（hip-hop）以及其他类型的声乐歌曲创作。

## 阅读前须知

- 请参考 `references/music.md` 文件，仅在需要了解具体的端点（endpoint）、参数、轮询（polling）或响应格式（response-shape）详情时才加载该文件。

## 使用场景

当用户希望执行以下操作时，请使用此技能：
- 根据提示生成说唱或嘻哈歌词；
- 将歌词转化为包含人声的完整歌曲；
- 控制歌曲风格、标题、人声性别或乐器演奏模式；
- 轮询异步进行的歌词或歌曲生成任务；
- 调试与SenseAudio音乐生成请求相关的错误。

## 默认工作流程

1. 确认目标输出类型：
- 仅生成歌词；
- 根据用户提供的歌词生成完整歌曲；
- 或者生成包含平台自动生成歌词的完整歌曲。

2. 从最基本的有效请求开始：
- 生成歌词需要 `prompt` 和 `provider: sensesong` 参数；
- 生成歌曲需要 `model: sensesong` 参数。

3. 将这两种生成流程视为可能异步进行的操作：
- 如果 `create` 方法返回 `task_id`，则需要轮询相应的 `pending` 端点；
- 在读取数据之前，请确保 `status` 状态为 `SUCCESS`；
- 如遇到错误，请明确显示 `FAILED` 而不是假设数据为空。

4. 仅在需要时添加额外的创作选项：
- `lyrics`（歌词）、`title`（标题）、`style`（风格）、`style_weight`（风格权重）、`negative_tags`（负面标签）、`vocal_gender`（人声性别）、`instrumental`（乐器演奏模式）。

5. 提供可立即使用的输出结果：
- 一个使用 `curl` 命令的示例；
- 一个指定语言版本的示例代码；
- 轮询逻辑；
- 以及用于解析 `audio_url`（音频链接）、`cover_url`（封面图片链接）、`lyrics`（歌词）和 `duration`（歌曲时长）的代码。

## 说唱相关的使用建议

- 对于说唱请求，请在提示中明确说明主题、节奏、韵律以及音乐风格（例如：trap、boom bap、drill、conscious rap 或 melodic rap）。
- 如果用户已经提供了歌词或副歌部分，可以直接使用 `lyrics` 参数进行歌曲创作；
- 使用 `style` 参数来指定音乐风格；使用 `negative_tags` 参数来排除某些风格；
- 仅在用户明确要求或根据创作需求时指定 `vocal_gender`（人声性别）为 `"m"` 或 `"f"`；
- 仅在需要纯乐器演奏的版本时使用 `instrumental: true` 参数；否则请省略该参数。

## 实施规则

- 将API密钥存储在环境变量中，切勿将密钥硬编码到代码中；
- 首先推荐使用 `curl` 命令进行测试，如有必要再提供Python或JavaScript实现；
- 不要自行添加额外的请求字段或未文档化的端点；
- 不要假设歌词中包含超出文档示例范围的标签；如果歌词的结构或语法有特殊要求，请严格遵循文档中的示例格式；
- 当文档中指定歌词需要用分号分隔各部分时，请保持该格式，除非用户提供了其他有效的歌词格式。

## 响应解析规则

- 成功获取歌词的结果格式：`response.data[0].text`（歌词内容）以及可选的 `response.data[0].title`（歌曲标题）；
- 成功获取歌曲结果格式：`response.data[0].audio_url`（音频链接）、`cover_url`（封面图片链接）、`duration`（歌曲时长）、`id`（歌曲ID）、`lyrics`（歌词内容）、`title`（歌曲标题）；
- 在访问数组或对象内容之前，请确保 `response` 或 `data` 不为空。

## 输出内容检查清单

使用此技能生成结果时，需包含以下信息：
- 使用了哪些端点；
- 最基本的有效请求格式；
- 是否需要轮询；
- 用户应读取的最终输出字段；
- 以及与用户创作需求相关的任何特定于说唱的提示或风格建议。