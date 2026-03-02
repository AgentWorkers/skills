---
name: Suno
slug: suno
version: 1.0.0
homepage: https://clawic.com/skills/suno
description: 通过 Suno 的 API 或浏览器，利用提示工程（prompt engineering）和歌曲扩展功能（song extensions）来生成 AI 音乐。
metadata: {"clawdbot":{"emoji":"🎵","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南。

## 使用场景

用户希望使用 Suno 生成音乐。代理程序可以通过托管 API 进行程序化生成，或者通过浏览器自动化实现与平台的直接交互；也可以通过提示工程（prompt engineering）进行手动操作。

## 架构

数据存储在 `~/suno/` 目录下。具体结构请参考 `memory-template.md`。

```
~/suno/
├── [memory.md]       # Created on first use: preferences, successful prompts
├── [projects/]       # Per-project song tracking
└── [songs/]          # Downloaded audio files
```

## 快速参考

| 项目 | 对应文件 |
|-------|------|
| 设置 | `setup.md` |
| 内存管理 | `memory-template.md` |
| API 使用 | `api.md` |
| 浏览器自动化 | `browser.md` |
| 提示设计 | `prompts.md` |
| 样式标签 | `styles.md` |
| 歌词编写指南 | `lyrics.md` |

## 核心规则

### 1. 选择合适的方法
| 使用场景 | 方法 |
|-----------|--------|
| 程序化生成 | 托管 API（如 aimusicapi.ai、EvoLink） |
| 视觉交互 | 通过 suno.com 的浏览器界面 |
| 仅需要提示 | 仅使用提示工程 |

### 2. 分层设计提示内容
示例提示格式：`indie folk melancholic acoustic guitar soft female vocals 90s`

### 3. 自定义歌词格式

### 4. 战略性地扩展歌曲内容
Suno 会自动生成音乐片段。要构建完整的歌曲，请按照以下步骤操作：
1. 创建具有吸引力的开头片段；
2. 保持音乐风格的连贯性；
3. 添加带有结尾标志的结尾部分；
4. 总时长控制在 2-4 分钟以内。

### 5. API 使用规范
所有 API 的使用流程均为：生成音乐 → 请求完成状态 → 获取音频链接。具体代码示例请参见 `api.md`。

## API 集成

### 推荐的托管 API
有两种主要的程序化生成工具：

**aimusicapi.ai** — 在 [aimusicapi.ai] 获取 API 密钥；
**EvoLink** — 在 [evolink.ai] 获取 API 密钥。
这两个平台都提供用于音乐生成、自定义歌词和扩展功能的 REST API。详细代码示例及端点文档请参见 `api.md`。

### API 使用流程
```python
# Conceptual flow (see api.md for real code)
1. POST /generate with prompt
2. Receive task_id
3. Poll /task/{id} every 5 seconds
4. Get audio_url when status="completed"
```

## 浏览器自动化
当无法使用 API 或用户更倾向于通过视觉界面进行操作时，可以按照以下步骤操作：

1. 访问 suno.com/create；
2. 选择“简单模式”（仅输入描述）或“自定义模式”（输入歌词和风格信息）；
3. 输入提示或歌词内容；
4. 点击“创建”按钮，等待 30-60 秒；
5. 下载生成的音频文件。
具体自动化步骤请参见 `browser.md`。

## 提示设计规范

### 按音乐类型分类的提示模板
| 音乐类型 | 提示模板 |
|-------|---------|
| 电子音乐 | `electronic [子类型] [情绪] synth [音效]` |
| 摇滚 | `[子类型]rock [能量] [吉他] [人声] [年代]` |
| 流行音乐 | `pop [情绪] [节奏] [人声] [制作风格]` |
| 嘻哈音乐 | `hip hop [子类型] [节拍] [旋律] [时代特征]` |

## 语音控制相关说明
更多关于提示设计的详细信息，请参考 `prompts.md` 和 `styles.md`。

## 常见问题及解决方法

| 问题 | 解决方案 |
|------|---------|----------|
| 提示过于模糊 | 生成结果随机 | 请明确指定音乐类型和情绪 |
| 描述矛盾 | 会导致模型混淆 | 使用一致的描述词 |
| 关键词过多 | 会分散模型注意力 | 最多使用 8-12 个关键词 |
| 未使用结构化标签 | 会导致歌词格式混乱 | 请使用 [Verse]、[Chorus] 等标签 |

## 数据存储
首次使用时，该工具会在 `~/suno/` 目录下创建以下文件：
- **memory 文件**：存储用户偏好设置和成功的生成结果；
- **projects 文件夹**：用于记录每个项目的详细信息；
- **songs 文件夹**：存放下载的音频文件。
所有数据均存储在本地。API 密钥应作为环境变量进行管理。

## 功能范围

**该工具可以：**
- 通过托管 API 生成音乐（需要提供 API 密钥）；
- 通过浏览器自动化访问 suno.com；
- 为 Suno 的模型设计结构化的提示内容；
- 使用正确的标签格式编写歌词；
- 本地记录项目生成过程和成功结果。

**该工具不能：**
- 将 API 密钥存储在纯文本文件中；
- 访问 `~/suno/` 目录以外的文件；
- 在未经用户指令的情况下自动发起请求。

## 外部接口
使用托管 API 时，请求会发送到以下地址：

| 接口地址 | 发送的数据 | 功能 |
|----------|-----------|---------|
| api.aimusicapi.ai | 提示内容、歌词 | 音乐生成 |
| api.evolink.ai | 提示内容、歌词 | 音乐生成 |
| suno.com | 浏览器会话信息 | 直接访问平台功能 |

API 密钥用于验证请求。提示内容和歌词会被发送到相应服务进行处理。

## 安全注意事项
使用该工具时，提示和歌词会被发送到第三方服务进行音乐生成。请仅将您的创意内容委托给可信赖的服务商。

## 相关工具
如果用户需要，可以使用以下工具进行扩展：
- `clawhub install <slug>`：安装相关工具（例如 `audio` 用于音频处理和编辑，`video` 用于将音乐与视频结合，`ffmpeg` 用于音频格式转换）。

## 用户反馈
- 如对本工具有用，请点赞：`clawhub star suno`；
- 保持更新：`clawhub sync`。