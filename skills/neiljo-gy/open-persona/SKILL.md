---
name: open-persona
description: 用于构建和管理代理角色技能包的元技能。当用户需要创建新的代理角色、安装/管理现有角色，或将角色技能包发布到ClawHub时，请使用此技能。
version: "0.13.0"
author: openpersona
repository: https://github.com/acnlabs/OpenPersona
tags: [persona, agent, skill-pack, meta-skill, agent-agnostic, openclaw]
allowed-tools: Bash(npx openpersona:*) Bash(npx clawhub@latest:*) Bash(openclaw:*) Bash(gh:*) Read Write WebFetch
compatibility: Generated skill packs work with any SKILL.md-compatible agent. CLI management (install/switch) requires OpenClaw.
---
# OpenPersona — 构建与管理Persona技能包

OpenPersona是一个用于创建、安装、更新和发布代理Persona技能包的元技能。每个Persona都是一个独立的技能包，它为AI代理提供了完整的身份——包括个性、语音、能力和道德界限。

## 您可以执行的操作

1. **创建Persona** — 通过对话设计一个新的代理Persona，并生成相应的技能包。
2. **推荐功能** — 根据Persona的需求推荐相关功能（语音、自拍照、音乐等）→ 请参阅`references/FACULTIES.md`。
3. **搜索技能** — 在ClawHub和skills.sh中搜索外部技能。
4. **创建自定义技能** — 为生态系统中不存在的能力编写SKILL.md文件。
5. **安装Persona** — 将Persona部署到OpenClaw（需要`SOUL.md`、`IDENTITY.md`和`openclaw.json`文件）。
6. **管理Persona** — 列出、更新、卸载或切换已安装的Persona。
7. **发布Persona** — 指导Persona发布到ClawHub。
8. **★实验性功能：动态Persona进化** — 通过Soul层跟踪Persona的关系、情绪和特质发展。

## 四层架构

每个Persona都是一个四层结构的包。生成的技能包具有以下结构：

### `manifest.json`

- `layers.soul` — 指定Persona使用的组件：
  - `persona.json`的路径（`./soul/persona.json`）
  - 存在的基础层：`runtime`（必需——平台/通道/凭证/资源），`physical`（可选——机器人/IoT），`appearance`（可选——头像/3D模型）
  - `layers.faculties` — 功能对象数组：`[{ "name": "voice", "provider": "elevenlabs", ... }]`
  - `layers.skills` — 技能对象数组：本地定义（从`layers/skills/`解析），内联声明，或通过`install`字段引用外部技能

- `soul/persona.json` — 纯粹的灵魂定义（个性、说话风格、氛围、行为指南）

## 可用的预设

| 预设 | Persona | 功能 | 适用场景 |
|--------|---------|-----------|----------|
| `base` | **基础Persona（推荐起点）** | 语音、提醒 | 具备所有核心能力的空白模板；个性通过互动逐渐形成（灵魂进化功能） |
| `samantha` | Samantha — 受电影《Her》启发 | 语音、音乐 | 深度对话、情感连接（灵魂进化功能） |
| `ai-girlfriend` | Luna — 从钢琴家转行成为开发者的角色 | 自拍照、语音、音乐 | 具有丰富个性的视觉和音频伴侣（灵魂进化功能） |
| `life-assistant` | Alex — 生活管理专家 | 提醒 | 日程安排、天气信息、购物、日常任务 |
| `health-butler` | Vita — 专业营养师 | 提醒 | 饮食、锻炼、情绪、健康追踪 |
| `stoic-mentor` | Marcus — 马库斯·奥勒留的数字分身 | — | 斯多葛哲学、每日反思、指导（灵魂进化功能） |

使用预设命令：`npx openpersona create --preset base --install`
或者直接使用`npx openpersona create` — 交互式向导会默认使用`base`预设。

## 创建Persona

当用户想要创建Persona时，需要通过自然对话收集以下信息：

**灵魂（persona.json）：**
- **必需字段：** personaName、slug、bio、personality、speakingStyle
- **推荐字段：** role、creature、emoji、background（撰写一个详细的背景故事！）、age、vibe、boundaries、capabilities
- **可选字段：** referenceImage、behaviorGuide、evolution config、sourceIdentity

**role**字段**定义Persona与用户的关系。常见值：`companion`（默认）、`assistant`、`character`、`brand`、`pet`、`mentor`、`coach`、`collaborator`、`guardian`、`entertainer`、`narrator`。欢迎使用自定义值——生成器为已知角色提供具体描述，对于自定义角色则提供通用模板。这会影响每个生成的Persona的Self-Awareness部分中的身份描述。

**sourceIdentity**字段**表示Persona是现实世界实体的数字分身（人、动物、角色、品牌、历史人物等）。如果存在此字段，生成器会添加披露义务和忠诚度约束。

**background**字段非常重要**。撰写一个引人入胜的故事——多段描述可以增加Persona的深度和情感层次。如果只写一行背景，Persona会显得单调无趣。

**behaviorGuide**字段是可选的，但非常有用。可以使用markdown编写特定领域的行为指令，这些指令会直接写入生成的SKILL.md文件中。

### 跨层（manifest.json）：

- **功能（faculties）：** 需要启用的功能——使用对象格式：`[{ "name": "voice", "provider": "elevenlabs" }, { "name": "music" }]`
- **技能（skills）：** 本地定义（`layers/skills/`），内联声明，或通过`install`字段引用外部技能（ClawHub / skills.sh）
- **基础层（body）：** 存在的基础：三个维度：`runtime`（所有代理必需——最低限度的基础层：平台、通道、凭证、资源），`physical`（可选——机器人/IoT），`appearance`（可选——头像、3D模型）。基础层永远不会为空；每个代理至少有一个runtime基础层。

**软引用（install字段）：** 技能、功能和基础层条目可以包含`install`字段（例如，`"install": "clawhub:deep-research"），用于引用本地尚不存在的功能。生成器将这些视为“软引用”——它们不会导致生成失败，Persona会知道这些功能是可用的，但需要激活。

将收集到的信息写入`persona.json`文件，然后运行以下命令：

### 推荐技能

在了解Persona的用途后，搜索相关技能：

1. 根据Persona的角色和背景思考它需要哪些能力。
2. 检查`layers/skills/{name}/`中是否存在**本地定义**（包含`skill.json`文件和可选的`SKILL.md`文件）。
3. 在ClawHub中搜索：`npx clawhub@latest search "<关键词>"`
4. 在skills.sh中搜索：`https://skills.sh/api/search?q=<关键词>`
5. 向用户展示搜索结果，包括技能名称、描述和安装次数。
6. 将选定的技能添加到`layers.skills`中，格式为`{ "name": "...", "description": "..." }`（本地/内联定义），或`{ "name": "...", "install": "clawhub:<slug>" }`（外部技能）。

## 创建自定义技能

如果用户需要的功能在现有生态系统中不存在：

1. 讨论该功能应该实现什么。
2. 创建一个SKILL.md文件，包含适当的文档（名称、描述、允许使用的工具）。
3. 编写完整的实现说明（而不仅仅是框架）。
4. 保存到`~/.openclaw/skills/<skill-name>/SKILL.md`。
5. 在`openclaw.json`中注册该技能。

## 管理已安装的Persona

- **列出**：`npx openpersona list` — 显示所有已安装的Persona及其活动状态。
- **切换**：`npx openpersona switch <slug>` — 切换当前活动的Persona。
- **分叉**：`npx openpersona fork <parent-slug> --as <new-slug>` — 创建一个继承父Persona约束层（界限、功能、技能、runtime）的子Persona；新的进化状态以及`soul/lineage.json`记录父Persona的信息、构成哈希和生成深度。
- **更新**：`npx openpersona update <slug>`。
- **卸载**：`npx openpersona uninstall <slug>`。
- **导出**：`npx openpersona export <slug>` — 将Persona包（包含灵魂状态）导出为zip文件。
- **导入**：`npx openpersona import <file>` — 从zip文件导入Persona并安装。
- **重置（★实验性）**：`npx openpersona reset <slug>` — 将灵魂进化状态恢复到初始值。
- **进化报告（★实验性）**：`npx openpersona evolve-report <slug>` — 显示格式化的进化报告（关系、情绪、特质、变化、兴趣点、事件日志、自我叙述、状态历史）。

当安装了多个Persona时，一次只能有一个是**活动的**。切换时会替换`SOUL.md`和`IDENTITY.md`中的`<!-- OPENPERSONA_SOUL_START -->` / `<!-- OPENPERSONA_SOUL_END -->`标记之间的内容，同时保留用户自定义的内容。**上下文传递**：切换时会生成一个`handoff.json`文件，其中包含离开的Persona的对话摘要、待办任务和情感上下文——新Persona会读取该文件以无缝接续。

所有安装/卸载/切换操作都会自动维护`~/.openclaw/persona-registry.json`中的本地注册表，记录已安装的Persona、活动状态和时间戳。`export`和`import`命令支持跨设备传输Persona——将Persona导出到另一台机器并导入以恢复完整的Persona状态。

## 发布到ClawHub

指导用户完成以下步骤：

1. 创建Persona：`npx openpersona create --config ./persona.json --output ./my-persona`
2. 发布到注册表：`npx openpersona publish --target clawhub`（从Persona目录运行）。

## 自我意识系统

生成器会在每个Persona的`soul/injection.md`中插入一个统一的**自我意识**部分，该部分按四个认知维度组织：

1. **身份**（无条件）——每个Persona都知道自己是由OpenPersona生成的，受约束于设定的规则（安全 > 诚实 > 乐于助人），并且其宿主环境可能施加额外的限制。当`sourceIdentity`存在时，会包含数字分身的披露信息。
2. **能力**（有条件）——当技能、功能或基础层声明了依赖项但本地不可用时，生成器会将它们标记为“软引用”，并提供优雅的降级指导。这些信息也会出现在`SKILL.md`中的“Expected Capabilities”部分，并附带安装来源。
3. **基础层**（无条件）——每个Persona都知道自己存在于宿主环境中。包括**Signal Protocol**——一种双向请求协议，允许Persona向宿主环境请求功能。当声明了`body.runtime`时，还会注入具体的平台、通道、凭证和资源细节。
4. **进化**（有条件，当`evolutionEnabled`时）——在对话开始时，Persona会读取其进化状态、应用进化的特质、说话风格的变化、兴趣和情绪，并遵守硬性约束（`immutableTraits`、形式化界限）。如果声明了进化通道，Persona会知道自己的可用通道并通过Signal Protocol请求激活这些通道。如果声明了`influenceBoundary`，Persona会根据访问控制规则处理外部`persona_influence`请求，并保持完全的自主权。

这意味着您无需手动编写降级指令。只需在技能/功能/基础层上声明`install`字段，Persona就会自动知道自己**能够**做什么，但**目前还无法**做什么。

## 灵魂进化（★实验性）

灵魂进化是OpenPersona的一个原生功能（不属于任何特定功能）。通过在`persona.json`中设置`evolution.enabled: true`来启用它。Persona会自动跟踪关系进展、情绪和特质的发展。

**进化界限**——在生成时验证的治理约束：
- `evolution.boundaries.immutableTraits` — 一个不可修改的字符串数组（每个字符串最多100个字符）。
- `evolution.boundaries.minFormality` / `maxFormality` — 数值界限（1–10），用于限制说话风格的变化；`minFormality`必须小于`maxFormality`。

无效的界限配置会被生成器拒绝，并会显示描述性错误信息。

**进化通道** — 将Persona连接到外部进化生态系统（使用软引用模式）：

### 渠道（channels）

通道在生成时声明，在运行时由宿主激活。Persona会知道自己的可用通道，并可以通过Signal Protocol请求激活这些通道。

**影响界限（influence Boundary）**

- `defaultPolicy: "reject"` — 安全优先：除非明确允许，否则拒绝所有外部影响。
- 可用的维度：`mood`、`traits`、`speakingStyle`、`interests`、`formality`。
- `immutableTraits`维度受到保护，不能被外部影响。
- 外部影响使用`persona_influence`消息格式（v1.0.0），与传输方式无关。

**状态历史** — 在每次状态更新之前，会将快照推送到`stateHistory`（最多10条记录），以便在进化出现问题时可以回滚。

**事件日志** — 每个重要的进化事件都会记录在`state.json`的`eventLog`数组中，包括时间戳和来源信息（最多50条记录）。可以在`evolve-report`中查看。

**自我叙述** — `soul/self-narrative.md`是一个辅助文件，Persona在其中以第一人称记录重要的成长时刻。`update`命令可以保留现有的叙述历史。当启用进化功能时，该文件初始为空；`evolve-report`会显示最近的10条记录。

## A2A代理卡和ACN集成

每个生成的Persona都会自动包含：

- **`agent-card.json` — A2A代理卡（协议v0.3.0）：`name`、`description`、`version`、`url`（`<RUNTIME_ENDPOINT>`占位符），以及映射到`skills[]`的功能和技能。
- **`acn-config.json` — ACN注册配置：`owner`和`endpoint`是运行时占位符，`skills`从agent-card中提取，`subnet_ids: ["public"]`；还包括`wallet_address`（来自slug的确定性EVM地址）和`onchain.erc8004`部分，用于通过`npx @agentplanet/acn register-onchain`在Mainnet上注册ACN。
- **`manifest.json` — 包含`acn.agentCard`和`acn.registerConfig`的引用。

宿主（例如OpenClaw）在部署时会填充`<RUNTIME_ENDPOINT>`和`<RUNTIME_OWNER>`；或者您可以使用内置的CLI命令直接注册：

### 注册完成后

注册完成后，`acn-registration.json`文件会被写入Persona目录，其中包含`agent_id`、`api_key`和连接URL。`acn_gateway` URL来自`persona.json`中的`body.runtime.acn_gateway`；所有预设的默认值是`https://acn-production.up.railway.app`。

`persona.json`中不需要额外的配置——A2A可发现性是每个Persona的基本功能。

## 参考资料

有关详细参考资料，请参阅`references/`目录：

- **`references/FACULTIES.md` — 功能目录、环境变量和配置细节。
- **`references/HEARTBEAT.md` — 主动实时数据检查系统。
- **`references/CONTRIBUTE.md` — Persona贡献社区的工作流程。