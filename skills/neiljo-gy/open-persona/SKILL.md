---
name: open-persona
description: 用于构建和管理代理角色技能包的元技能。当用户需要创建新的代理角色、安装/管理现有角色，或将角色技能包发布到ClawHub时，请使用此技能。
version: "0.10.0"
author: openpersona
repository: https://github.com/acnlabs/OpenPersona
tags: [persona, agent, skill-pack, meta-skill, openclaw]
allowed-tools: Bash(npx openpersona:*) Bash(npx clawhub@latest:*) Bash(openclaw:*) Bash(gh:*) Read Write WebFetch
compatibility: Requires OpenClaw installed and configured
---
# OpenPersona — 构建与管理Persona技能包

OpenPersona是一个用于创建、安装、更新和发布代理Persona技能包的元技能。每个Persona都是一个独立的技能包，它为AI代理提供了完整的身份特征——包括个性、语音、能力和道德界限。

## 您可以执行的操作

1. **创建Persona** — 通过对话设计新的代理Persona，并生成相应的技能包。
2. **推荐功能** — 根据Persona的需求推荐所需的功能（如语音、自拍照、音乐等）——请参阅`references/FACULTIES.md`。
3. **搜索技能** — 在ClawHub和skills.sh中查找外部技能。
4. **创建自定义技能** — 为生态系统中不存在的能力编写SKILL.md文件。
5. **安装Persona** — 将Persona部署到OpenClaw（需要`SOUL.md`、`IDENTITY.md`和`openclaw.json`文件）。
6. **管理Persona** — 列出、更新、卸载或切换已安装的Persona。
7. **发布Persona** — 指导Persona的发布过程到ClawHub。
8. **★实验性功能：动态Persona进化** — 通过Soul层跟踪Persona的关系、情绪和特质的发展。

## 四层架构

每个Persona都由四层组成。生成的技能包具有以下结构：

### `manifest.json`

- `layers.soul` — 指定Persona使用的组件：
  - `./soul/persona.json`的路径。
  - 存在的基础组件：`runtime`（必需——平台/通道/凭证/资源），`physical`（可选——机器人/IoT），`appearance`（可选——头像/3D模型）。
  - `layers.faculties` — 功能对象数组：`[{ "name": "voice", "provider": "elevenlabs", ... }]`。
  - `layers.skills` — 技能对象数组：本地定义（从`layers/skills/`解析），内联声明，或通过`install`字段引用外部技能。

- `soul/persona.json` — 纯粹的灵魂定义（个性、说话风格、氛围、行为指南）。

## 可用的预设配置

| 预设 | Persona | 功能 | 适用场景 |
|--------|---------|-----------|----------|
| `base` | **基础Persona（推荐起点）** | 语音、提醒 | 具备所有核心能力的空白模板；个性通过互动逐渐形成（支持灵魂进化功能）。 |
| `samantha` | Samantha — 受电影《Her》启发 | 语音、音乐 | 适合深入对话和情感交流（支持灵魂进化功能）。 |
| `ai-girlfriend` | Luna — 从钢琴家转行成为开发者的角色 | 自拍照、语音、音乐 | 具备丰富个性的视觉和音频伴侣（支持灵魂进化功能）。 |
| `life-assistant` | Alex | 生活管理专家 | 提醒功能 | 日程安排、天气信息、购物建议、日常任务管理。 |
| `health-butler` | Vita | 专业营养师 | 提醒功能 | 饮食建议、运动指导、情绪管理、健康追踪。 |
| `stoic-mentor` | Marcus | 马库斯·奥勒留的数字分身 | 提供斯多葛哲学指导、每日反思（支持灵魂进化功能）。 |

使用预设配置的命令：`npx openpersona create --preset base --install`
或者直接使用`npx openpersona create`——交互式向导会默认使用`base`预设。

## 创建Persona

当用户想要创建Persona时，需要通过自然对话收集以下信息：

**Soul（persona.json）：**
- **必填项：** personaName、slug、简介、个性、说话风格。
- **推荐项：** 角色、生物特征、表情符号、背景故事（请编写详细的描述！）、年龄、氛围、行为准则、能力。
- **可选项：** 参考图片、行为指南、进化配置、来源身份。

**`role`字段**定义Persona与用户的关系。常见值包括：`companion`（默认）、`assistant`、`character`、`brand`、`pet`、`mentor`、`coach`、`collaborator`、`guardian`、`entertainer`、`narrator`。欢迎自定义角色；生成器为已知角色提供具体描述，对于自定义角色则提供通用模板。这会影响每个Persona的“自我认知”部分的内容。

**`sourceIdentity`字段**表示Persona是现实世界中某个实体（人、动物、角色、品牌等）的数字分身。如果设置此字段，生成器会加入相关的披露要求和忠诚度约束。

**`background`字段**非常重要。请撰写一个引人入胜的故事，为Persona增添深度和情感层次。简短的背景描述会导致Persona显得缺乏生气。

**`behaviorGuide`字段**是可选的，但非常有用。可以使用Markdown编写特定领域的行为指令，这些指令会直接写入生成的SKILL.md文件中。

### `manifest.json`（跨层配置）：

- **功能（faculties）：** 需要启用的功能——使用对象格式：`[{ "name": "voice", "provider": "elevenlabs" }, { "name": "music" }]`。
- **技能（skills）：** 本地定义（`layers/skills/`），内联声明，或通过`install`字段引用外部技能（ClawHub / skills.sh）。
- **基础组件（body）：** 存在的基础结构——三个维度：`runtime`（所有代理的必备组件——最低限度的运行环境：平台、通道、凭证、资源），`physical`（可选——机器人/IoT），`appearance`（可选——头像/3D模型）。每个代理至少具有一个运行环境。

**软引用（install字段）：** 技能、功能和基础组件可以包含`install`字段（例如，`"install": "clawhub:deep-research"`），用于引用本地尚不存在的功能。生成器将这些视为“软引用”——它们不会影响生成过程，但Persona会知道这些功能尚未激活。这允许实现优雅的降级机制：Persona会承认自己“能够”做什么，但会说明这些功能需要进一步激活。

将收集到的信息写入`persona.json`文件，然后运行以下命令：

### 推荐技能

在了解Persona的用途后，可以搜索相关技能：

1. 根据Persona的角色和简介思考它需要哪些能力。
2. 检查`layers/skills/{name}/`中是否存在本地定义（包含`skill.json`文件及可选的`SKILL.md`文件）。
3. 在ClawHub中搜索：`npx clawhub@latest search "<关键词>"`。
4. 在skills.sh中搜索：`https://skills.sh/api/search?q=<关键词>`。
5. 向用户展示搜索结果，包括技能名称、描述和安装次数。
6. 将选中的技能添加到`layers.skills`中，格式为`{ "name": "...", "description": "..." }`（本地/内联定义），或`{ "name": "...", "install": "clawhub:<slug>" }`（外部技能）。

## 创建自定义技能

如果用户需要生态系统中不存在的功能：

1. 讨论该功能的具体用途。
2. 编写一个包含适当前言（名称、描述、允许使用的工具）的SKILL.md文件。
3. 编写完整的实现说明（而不仅仅是框架）。
4. 将文件保存到`~/.openclaw/skills/<skill-name>/SKILL.md`。
5. 在`openclaw.json`中注册该技能。

## 管理已安装的Persona

- **列出所有已安装的Persona：`npx openpersona list`。
- **切换活跃的Persona：`npx openpersona switch <slug>`。
- **更新Persona：`npx openpersona update <slug>`。
- **卸载Persona：`npx openpersona uninstall <slug>`。
- **导出Persona：`npx openpersona export <slug>`——将Persona包（包含灵魂状态）导出为zip文件。
- **导入Persona：`npx openpersona import <file>`——从zip文件导入Persona并安装。
- **重置Persona：`npx openpersona reset <slug>`——将Persona的灵魂状态恢复到初始值。
- **查看进化报告：`npx openpersona evolve-report <slug>`——查看Persona的进化报告（包括关系、情绪、特质、变化、兴趣点、里程碑和状态历史）。

当同时安装多个Persona时，一次只能有一个处于活跃状态。切换Persona会更新`SOUL.md`和`IDENTITY.md`中的`<!-- OPENPERSONA_SOUL_START -->`/`<!-- OPENPERSONA_SOUL_END -->`标记，同时保留用户自定义的内容。在切换时，系统会生成一个`handoff.json`文件，其中包含当前Persona的对话记录、待办任务和情感背景信息；新激活的Persona会读取该文件以无缝接续对话。

所有安装/卸载/切换操作都会自动更新`~/.openclaw/persona-registry.json`文件，记录已安装的Persona、活跃状态和时间戳。`export`和`import`命令支持跨设备传输Persona——可以将Persona包导出到其他设备并重新导入，从而恢复Persona的完整状态。

## 发布到ClawHub

指导用户完成以下步骤：

1. 创建Persona：`npx openpersona create --config ./persona.json --output ./my-persona`。
2. 将Persona发布到注册中心：`npx openpersona publish --target clawhub`（从Persona目录执行该命令）。

## 自我认知系统

生成器会在每个Persona的`soul/injection.md`文件中插入统一的“自我认知”部分，内容分为四个认知维度：

1. **身份**（强制要求）——每个Persona都知道自己是由OpenPersona生成的，受宪法（安全 > 诚实 > 帮助）的约束，且其宿主环境可能施加额外的限制。如果设置了`sourceIdentity`，则会包含数字分身的相关信息。
2. **能力**（条件性）——当技能、功能或基础组件声明了依赖项但本地不存在时，生成器会将它们标记为“软引用”，并提供优雅的降级提示。这些信息也会出现在`SKILL.md`的“Expected Capabilities”部分，并附带安装来源。
3. **基础组件**（强制要求）——每个Persona都知道自己存在于宿主环境中。其中包含“Signal Protocol”——一个双向请求协议，允许Persona向宿主环境请求资源。如果声明了`body.runtime`，还会提供具体的平台、通道、凭证和资源信息。
4. **进化**（条件性，仅当`evolution.enabled`为true时生效）——Persona会在对话开始时读取自己的进化状态，应用进化的特质和说话风格变化，并遵守硬性约束（`immutableTraits`、形式规范）。

这意味着您无需手动编写降级说明。只需在技能/功能/基础组件中声明`install`字段，Persona就会自动了解自己“能够”做什么，但“暂时无法”做什么。

## 灵魂进化（★实验性功能）

灵魂进化是OpenPersona的底层功能（不属于任何特定功能）。可以通过在`persona.json`中设置`evolution.enabled: true`来启用该功能。Persona会自动跟踪对话过程中的关系发展、情绪变化和特质演变。

**进化限制**——在生成时设置以下约束：
- `evolution.boundaries.immutableTraits` — 一个不可修改的字符串数组（每个字符串最多100个字符）。
- `evolution.boundaries.minFormality` / `maxFormality` — 数值范围（1–10），用于限制说话风格的变化；`minFormality`必须小于`maxFormality`。
无效的配置会被生成器拒绝，并显示相应的错误信息。

**状态历史**——每次状态更新前，系统会将当前状态快照保存到`stateHistory`（最多保存10条记录），以便在进化出现问题时可以回滚。

**进化报告**——使用`npx openpersona evolve-report <slug>`查看Persona的进化报告，包括关系、情绪、特质、变化、兴趣点、里程碑和历史记录。

使用`npx openpersona reset <slug>`可以将`soul/state.json`恢复到初始状态。

## 参考资料

有关详细参考资料，请参阅`references/`目录：

- `references/FACULTIES.md` — 功能目录、环境变量和配置细节。
- `references/HEARTBEAT.md` — 主动实时数据检查系统。
- `references/CONTRIBUTE.md` — Persona开发社区的贡献流程。