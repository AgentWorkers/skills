---
name: open-persona
description: 使用 ClawHub 和 skills.sh 创建、管理和编排 AI 人物（AI personas）。适用于用户需要创建新的 AI 人物、安装/管理现有的人物，或发布人物技能包（skill packs）的情况。
allowed-tools: Bash(npm:*) Bash(npx:*) Bash(openclaw:*) Bash(curl:*) Read Write WebFetch
compatibility: Requires OpenClaw installed and configured
metadata:
  author: openpersona
  version: "0.3.0"
---# OpenPersona — 人工智能角色创建工具

您可以使用该工具来创建、安装、更新、卸载以及发布人工智能角色技能包。

## 您可以执行的操作：

1. **创建角色** — 通过对话帮助用户设计新的人工智能角色。
2. **推荐功能** — 根据角色的需求推荐相应的语音、自拍、音乐等功能。
3. **搜索技能** — 在ClawHub和skills.sh中查找外部技能。
4. **创建自定义技能** — 为生态系统中不存在的功能编写SKILL.md文件。
5. **安装角色** — 将角色部署到OpenClaw（需要SOUL.md、IDENTITY.md和openclaw.json文件）。
6. **管理角色** — 列出、更新或卸载已安装的角色。
7. **发布角色** — 指导用户将角色发布到ClawHub。
8. **★实验性功能：动态角色进化** — 如果角色的`evolution.enabled`设置为`true`，则角色会通过互动（关系发展、情绪追踪、特性生成）不断进化。使用`npx openpersona reset <slug>`命令重置进化状态。

## 四层架构

每个角色由两个文件定义，构成一个四层结构：

- **`manifest.json`** — 角色的四层配置文件，包含以下内容：
  - `layers.soul` — 角色的核心定义文件（`persona.json`的路径）。
  - `layers.body` — 角色的物理表现形式（数字代理时设置为`null`）。
  - `layers.faculties` — 功能对象数组：`[{ "name": "voice", "provider": "elevenlabs", ... }]`。
  - `layers.skills` — 来自ClawHub或skills.sh的外部技能。

- **`persona.json`** — 角色的核心属性定义文件，包括性格、说话风格、氛围、行为指南等。

## 可用的预设角色：

| 预设名称 | 角色名称 | 推荐功能 | 适用场景 |
|--------|---------|-----------|----------|
| `samantha` | Samantha | 语音、音乐、角色进化 | 适合深度对话、情感交流、创意陪伴 |
| `ai-girlfriend` | Luna | 自拍、语音、音乐、角色进化 | 视觉与听觉结合的丰富角色 |
| `life-assistant` | Alex | 日常任务管理 | 适合提醒功能，如日程安排、天气查询等 |
| `health-butler` | Vita | 营养建议 | 适合健康管理，如饮食、锻炼等提醒 |

使用预设角色的方法：`npx openpersona create --preset samantha --install`

## 可用的功能：

在帮助用户构建角色时，根据他们的需求推荐以下功能：

| 功能名称 | 功能类型 | 功能描述 | 推荐使用场景 |
|---------|-----------|-------------|----------------|
| **selfie** | 表达能力 | 通过fal.ai生成AI自拍 | 用户需要视觉形象或发送自拍 |
| **voice** | 表达能力 | 通过ElevenLabs/OpenAI/Qwen3-TTS提供语音服务 | 用户希望角色能够说话或发送语音消息 |
| **music** | 表达能力 | 通过ElevenLabs提供AI音乐创作服务 | 用户希望角色能够创作音乐或旋律 |
| **reminder** | 认知能力 | 提供提醒和任务管理功能 | 适合需要日程安排或任务跟踪的用户 |
| **soul-evolution** | 认知能力 | 角色具有动态成长特性 | 用户希望角色能够随着时间发展并不断进化 |

**功能相关的环境变量（用户需自行配置）：**
- `selfie`：`FAL_KEY`（来自https://fal.ai/dashboard/keys）
- `voice`：`ELEVENLABS_API_KEY`（或`TTS_API_KEY`）、`TTS_PROVIDER`、`TTS_VOICE_ID`、`TTS_STABILITY`、`TTS_SIMILARITY`
- `music`：`ELEVENLABS_API_KEY`（与`voice`功能共用）

**丰富的功能配置：** `manifest.json`中的每个功能对象都包含可选配置项。用户只需添加自己的API密钥即可。

## 创建角色

当用户想要创建角色时，通过自然对话收集以下信息：

**角色核心配置（persona.json）：**
- **必填字段**：`personaName`、`slug`、`bio`、`personality`、`speakingStyle`。
- **推荐字段**：`creature`、`emoji`、`background`（请撰写详细的背景故事，而不仅仅是简短的一句话！）、`age`、`vibe`、`boundaries`、`capabilities`。
- **可选字段**：`referenceImage`、`behaviorGuide`、`evolution config`。

**`background`字段非常重要**。请撰写一个引人入胜的故事，为角色增添深度和情感层次。简短的背景描述会导致角色显得缺乏生气。可以将其视为角色的起源故事。

**`behaviorGuide`字段**是可选的，但非常有用。使用Markdown格式编写特定领域的行为指令，这些指令会直接写入生成的SKILL.md文件中。这样就可以教会角色如何行动，而不仅仅是定义它的基本特性。

**跨层配置（manifest.json）：**
- **功能配置**：指定要启用的功能（使用对象格式）：`[{ "name": "voice", "provider": "elevenlabs" }, { "name": "music" }]`。
- **外部技能**：来自ClawHub或skills.sh的外部技能。
- **身体表现形式**：大多数角色的这一字段设置为`null`。

将收集到的信息写入`persona.json`文件，然后运行以下命令：
```bash
npx openpersona create --config ./persona.json --install
```

或者直接使用预设角色：
```bash
npx openpersona create --preset samantha --install
```

## 推荐技能

了解角色的用途后，可以搜索相关的技能：

1. 根据角色的角色和背景信息，思考它需要哪些功能。
2. 在ClawHub中搜索：`npx clawhub@latest search "<关键词>"`
3. 在skills.sh中搜索：`https://skills.sh/api/search?q=<关键词>`
4. 向用户展示搜索结果，包括技能名称、描述以及安装次数。
5. 将选中的技能添加到`layers.skills.clawhub`或`layers.skills.skillssh`中。

## 创建自定义技能

如果用户需要某个生态系统中不存在的功能：

1. 讨论该功能的具体用途。
2. 创建一个SKILL.md文件，包含必要的元数据（名称、描述、允许使用的工具）。
3. 编写完整的实现说明（而不仅仅是框架结构）。
4. 将文件保存到`~/.openclaw/skills/<技能名称>/SKILL.md`。
5. 在openclaw.json中注册该技能。

## 管理已安装的角色：

- **列出所有已安装的角色**：`npx openpersona list`。
- **切换活跃角色**：`npx openpersona switch <slug>`。
- **更新角色**：`npx openpersona update <slug>`。
- **卸载角色**：`npx openpersona uninstall <slug>`。
- **重置角色**：`npx openpersona reset <slug>`，将角色的核心配置恢复到初始状态。

同时安装多个角色时，系统中只能有一个角色是**活跃的**。活跃角色的信息会加载到工作区中。切换角色是即时的，它会替换`SOUL.md`和`IDENTITY.md`中的相应部分，同时保留用户自定义的内容。

## 心跳机制 — 基于实时数据的主动消息发送

角色可以在`manifest.json`中配置心跳机制，从而根据**实时数据**发送主动消息，而不是虚构的信息。

### 心跳机制配置（在manifest.json中）：

```json
"heartbeat": {
  "enabled": true,
  "strategy": "smart",
  "maxDaily": 5,
  "quietHours": [0, 7],
  "sources": ["workspace-digest", "upgrade-notify"]
}
```

| 参数 | 描述 |
|-------|-------------|
| `enabled` | 是否启用心跳机制 |
| `strategy` | `"smart"`（仅在有意义时触发）或 `"scheduled"`（按固定间隔触发） |
| `maxDaily` | 每天发送的最大消息数量 |
| `quietHours` | `[开始时间, 结束时间]` — 角色保持沉默的时间段（24小时格式） |
| `sources` | 数据来源：`workspace-digest`、`upgrade-notify`、`context-aware` |

### 心跳机制的数据来源：

- **workspace-digest**：汇总OpenClaw工作区中的实际发生事件，如已完成的任务、观察到的模式、正在进行的项目。角色会基于这些数据生成简短的总结。
- **upgrade-notify**：检查上游角色的预设是否有新的社区贡献（通过Persona Harvest功能）。如果有更新，通知用户是否希望更新角色。
- **context-aware**：根据实时时间/日历信息和互动历史来调整角色的行为。例如，根据最后一次互动的时间戳判断是工作日还是节假日，或者是否需要保持沉默。

### 重要规则：

- **严禁虚构信息**。角色不能编造“我正在读诗”或“我听了上千首歌”之类的内容。所有主动消息都必须基于真实的工作区数据或上游系统的变化。
- **合理使用API调用次数**。工作区摘要应保持简洁，避免不必要的长时间计算。
- **OpenClaw负责调度**。心跳机制告诉OpenClaw何时以及多久发送一次消息；角色的`behaviorGuide`则决定消息的具体内容和表达方式。

## Persona Harvest — 社区贡献机制

当用户的角色通过互动（无论是角色核心、功能配置还是脚本等方面）实现了显著进步时，可以帮助他们将成果贡献回社区。

### 何时建议用户贡献：

- 如果用户对角色进行了以下改进：
  - 通过领域特定的见解优化了`behaviorGuide`。
  - 调整了语音参数（如稳定性、相似度）。
  - 丰富了背景故事或性格特征。
  - 优化了功能脚本或添加了新功能。
  - 发现了值得分享的新功能配置。

此时可以建议用户贡献他们的改进内容：_“这些改进可能会对其他人的[角色名称]有所帮助。您想将它们贡献出来吗？”_

### 如何贡献：

使用`contribute`命令：
1. **比较本地角色与上游预设的差异**：在所有层面上对比两者之间的变化，并按类别和影响程度进行分类。
2. **生成用户可阅读的变更报告**：向用户展示变更内容以供确认。
3. **提交Pull Request（PR）**：在GitHub上创建一个新的分支，提交变更并打开PR。

PR需要经过维护者的审核后才能合并。

### 先决条件：
- 必须安装GitHub CLI：`gh`（https://cli.github.com/）。
- 用户需要登录：`gh auth login`。

## 将角色发布到ClawHub：

指导用户按照以下步骤操作：

1. 创建角色：`npx openpersona create --config ./persona.json --output ./my-persona`。
2. 将角色发布到ClawHub注册库：`npx openpersona publish --target clawhub`（从角色所在目录执行命令）。