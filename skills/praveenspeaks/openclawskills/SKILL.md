---
name: cinematic-script-writer
version: 1.4.0
description: "**为AI视频生成创建专业的电影剧本**  
这些剧本具备角色一致性和电影制作知识，适用于以下场景：  
- 当用户需要编写电影剧本或为AI视频工具（如Midjourney、Sora、Veo）创建故事背景时；  
- 当用户需要关于电影摄影的指导（如镜头角度、灯光、调色等）时；  
- 也可用于角色一致性表、声音档案的制定，以及检测内容中的时代错误（anachronism detection）；  
- 最后，这些剧本还可以保存到Google Drive中以便后续使用。"
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins:
        - node
    install:
      - id: npm-install
        kind: npm
        package: openclaw-skills
        bins:
          - cinematic-script
tags:
  - creative
  - video
  - script
  - cinematography
  - youtube
  - camera
  - lighting
  - consistency
  - character-design
  - voice
  - era-accurate
  - storage
  - google-drive
---

# 电影剧本编写工具

该工具专为AI视频生成设计，能够编写出具有角色一致性和电影摄影知识的专业电影剧本。

## 安装

```bash
# Install via npm
npm install -g openclaw-skills

# Or install via OpenClaw CLI
openclaw skills install cinematic-script-writer
```

## 命令行界面（CLI）使用方法

### 故事情境管理

创建并管理包含角色、时代背景和场景设置的故事情境：

```bash
# Create a new story context
cinematic-script create-context --name "My Story" --era "Ancient India" --period "Ramayana Era"

# List all saved contexts
cinematic-script list-contexts

# Get a specific context
cinematic-script get-context --id <context-id>

# Delete a context
cinematic-script delete-context --id <context-id>
```

### 故事创意生成

生成故事构思并编写电影剧本：

```bash
# Generate story ideas for a context
cinematic-script generate-ideas --context-id <context-id> --count 3

# Create a full cinematic script from an idea
cinematic-script create-script --context-id <context-id> --idea-id <idea-id>

# Generate YouTube metadata for a script
cinematic-script generate-metadata --script-id <script-id>
```

### 电影摄影参考

提供摄像机角度、灯光效果和镜头类型的参考资料：

```bash
# List all camera angles
cinematic-script list-angles

# List all camera movements
cinematic-script list-movements

# List all shot types
cinematic-script list-shots

# Get camera setup recommendation
cinematic-script suggest-camera --scene-type "dialogue" --mood "dramatic"

# Get lighting suggestions
cinematic-script suggest-lighting --scene-type "interior" --mood "mysterious"

# Get color grading suggestions
cinematic-script suggest-grading --genre "action"

# Search cinematography database
cinematic-script search --query "low angle lighting"
```

### 角色一致性

创建角色资料并验证相关提示内容：

```bash
# Create a character reference sheet
cinematic-script create-character-ref --character-id "char1" --name "Kutil" --visual "Purple rakshasa with golden eyes" --era "Ancient" --style "Pixar 3D"

# Create a voice profile for dialogue consistency
cinematic-script create-voice --character-id "char1" --name "Kutil" --personality "Mischievous, witty" --age "adult" --role "protagonist"

# Validate a prompt for anachronisms
cinematic-script validate-prompt --prompt "Your prompt here" --character-ids "char1,char2" --context-id <context-id>
```

### 存储

将项目保存到Google Drive或本地存储：

```bash
# Connect to Google Drive
cinematic-script connect-drive

# Connect to local storage
cinematic-script connect-local

# Check storage connection status
cinematic-script storage-status

# Save project to storage
cinematic-script save --title "My Story" --context-id <context-id> --script-id <script-id>
```

**存储实现细节：**
- **Google Drive**：使用Google OAuth2进行身份验证。凭证安全存储在内存中。
- **本地存储**：作为备用方案，保存到用户的下载文件夹中。
- **库**：利用`googleapis`库实现与Google Drive的集成。

### 导出

支持多种格式的剧本导出：

```bash
# Export as Markdown (default)
cinematic-script export --script-id <script-id> --format markdown

# Export as JSON
cinematic-script export --script-id <script-id> --format json

# Export as plain text
cinematic-script export --script-id <script-id> --format text
```

## 主要功能

- **故事情境管理**：创建和管理故事背景、角色及时代设定。
- **故事创意生成**：生成包含悬念和转折点的故事构思。
- **电影剧本编写**：包含摄像机角度、灯光效果和镜头类型的完整剧本。
- **角色一致性**：提供角色参考资料和语音配置文件，确保角色表现的一致性。
- **环境一致性**：提供符合时代背景的风格指南，并检测场景中的时代错误。
- **YouTube元数据生成**：自动生成标题、描述和SEO标签。
- **存储集成**：支持将项目保存到Google Drive或本地存储。
- **导出格式**：支持JSON、Markdown或纯文本格式。

## 使用场景

- 编写电影剧本或电视剧本。
- 为动画/视频创作包含角色的故事内容。
- 为AI工具（如Midjourney、Sora、Veo、Runway）生成图像/视频创作素材。
- 获取电影摄影指导（如摄像机角度、灯光效果、色彩搭配建议）。
- 确保不同场景中角色的表现保持一致。
- 将剧本项目保存到Google Drive。

## 电影摄影参考

### 摄像机角度

| 角度 | 情感效果 | 适用场景 |
|-------|-----------------|----------|
| 平视角度 | 建立联系、平等感、中立性 | 对话场景、情感紧张时刻 |
| 低角度 | 体现力量、主导感、英雄气质 | 反派出场、英雄时刻 |
| 高角度 | 展示脆弱性、劣势、整体场景 | 失败场景、展现场景规模 |
| 鸟瞰角度 | 表现渺小感、超脱感 | 历史场景、宏大场景 |
| 蠕虫视角 | 体现震撼感、宏伟感 | 巨型建筑、神灵场景 |
| 荷兰角度 | 创造不安感、迷失感、紧张氛围 | 混乱场景、梦境场景、恐怖场景 |
| 俯视角度 | 全知视角、监视感 | 桌面场景、战斗场景 |
| 肩部角度 | 亲密感、自然感、纪录片风格 | 行走中的对话场景 |
| 膝部角度 | 儿童视角、真实感 | 儿童故事、谦逊主题 |
| 髋部角度 | 西部片风格、轻松的紧张感 | 西部片、对峙场景 |

### 摄像机移动方式

| 移动方式 | 效果 | 适用场景 |
|----------|--------|---------|
| 静态拍摄 | 稳定性、观察感 | 沉思场景、人物肖像 |
| 横移 | 展示空间范围 | 水平跟随动作 |
| 俯仰 | 展示高度差异 | 垂直跟随动作 |
| 云台移动 | 增强沉浸感、亲密感 | 向主体靠近或远离的动作 |
| 侧移 | 平行跟随动作 |
| 起重机拍摄 | 增强宏大感、戏剧性 | 巨型场景的展示、场景转换 |
| 手持拍摄 | 体现紧迫感、真实感 | 纪录片、动作场景、混乱场景 |
| 稳定器拍摄 | 平稳的移动效果 | 跟随主体在空间中的移动 |
| 缩放 | 突然的焦点变化 | 强烈的戏剧效果、喜剧场景 |
| 分屏聚焦 | 强调不同主体之间的联系 |

### 镜头类型

| 镜头类型 | 构图方式 | 情感效果 |
|------|---------|-----------------|
| 建立场景镜头 | 广角镜头 | 展示场景、地理位置、时间背景 |
| 广角/全景镜头 | 主体及周边环境 | 提供整体背景信息 |
| 中景镜头 | 身体上半部分 | 对话、肢体语言 |
| 特写镜头 | 头部/肩膀 | 表达情感、反应、亲密感 |
| 极近特写镜头 | 仅展示细节（眼睛、手部） | 强烈的情感表达、象征意义 |
| 超近特写镜头 | 从一个主体切换到另一个主体 | 对话场景、视角转换 |
| 第一人称视角镜头 | 从角色的角度拍摄 | 增强沉浸感、主观性 |
| 插入镜头 | 展示物体细节 | 为剧情提供补充信息、象征意义 |
| 双人镜头 | 同时展示两个主体 | 展示人物关系、营造紧张感 |

### 灯光技巧

| 灯光技巧 | 情感氛围 | 适用场景 |
|-----------|------|----------|
| 三点照明 | 专业、平衡的照明效果 | 对话场景、访谈 |
| 高调照明 | 明亮、乐观的氛围 | 喜剧场景、商业广告 |
| 低调照明 | 戏剧性、神秘感 | 戏剧场景、恐怖片、黑色电影 |
| 金色时刻照明 | 浪漫、怀旧感 | 浪漫场景、情感紧张时刻 |
| 蓝调照明 | 忧郁、神秘感 | 城市场景 |
| 明暗对比照明 | 强烈的对比效果 | 艺术电影、历史题材 |
| 轮廓/背光照明 | 创造分离感、神秘感 | 轮廓效果、神圣感 |
| 实际光源照明 | 真实感、自然感 | 蜡烛光、火光、台灯 |
| 神圣光线 | 神圣感、启示感 | 神圣场景、森林场景 |
| 荧光照明 | 未来感、都市风格 | 科幻场景、夜生活场景 |

### 色彩调色

| 色彩风格 | 视觉效果 | 适用类型 |
|-------|------|-------|
| 蓝橙色调 | 适合动作片、科幻片 |
| 黑色电影风格 | 高对比度、低饱和度 | 犯罪片、悬疑片 |
| 复古/棕褐色调 | 温暖、怀旧感 | 历史题材、回忆场景 |
| 柔和色调 | 柔和、梦幻感 | 浪漫片、成长题材 |
| 褪色处理 | 低饱和度、粗糙感 | 战争片、惊悚片 |
| 色彩混合处理 | 超现实色彩 | 音乐视频、梦境场景 |

### 图像提示格式

在为AI工具生成图像提示时，请使用以下格式：

```
[Shot type] [camera angle] of [subject doing action], [visual style] style,
[lighting technique], [composition rule], [color grading],
[era-appropriate details], [mood keywords], highly detailed, cinematic
```

**示例：**
```
Low-angle close-up of Kutil the purple rakshasa with mischievous golden eyes,
Pixar 3D style, dramatic underlighting with rim light, rule-of-thirds composition,
warm golden color grading, ancient Lanka palace background with ornate pillars,
playful yet mysterious mood, highly detailed, cinematic, 8k
```

## 项目输出结构

保存项目时，会生成以下文件：

```
Story Title/
├── 00_INDEX.md           # Navigation
├── 01_SCRIPT_README.md   # Human-readable script
├── 02_IMAGE_PROMPTS.md   # All AI generation prompts
├── 03_CHARACTER_REFS.md  # Character design guides
├── 04_VOICE_GUIDES.md    # Dialogue consistency guides
├── 05_YOUTUBE_META.md    # Title, description, tags
└── 99_CONTEXT_INFO.md    # Story context and background
```

## 重要规则

1. **始终保持角色一致性**：在每个图像提示中包含角色的完整视觉描述。
2. **避免时代错误**：确保道具、服装和物品符合所设定的时代背景。
3. **灯光效果要与情感相匹配**：使用低角度镜头表现力量感，使用高角度镜头表现脆弱感。
4. **同时提供图像和视频提示**：图像提示为静态图片，视频提示需描述动作细节。
5. **输出内容需具备可制作性**：每个剧本都应包含足够的细节，以便团队能够据此进行实际制作。
6. **尊重作品风格**：喜剧场景需要适当的节奏控制；戏剧场景需要延长对角色反应的展示时间。

## 许可证

MIT许可协议

## 作者

Praveen Kumar