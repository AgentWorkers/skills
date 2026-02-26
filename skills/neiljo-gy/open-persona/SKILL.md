---
name: open-persona
description: 用于构建和管理代理角色技能包的元技能。当用户需要创建新的代理角色、安装/管理现有角色，或将角色技能包发布到ClawHub时，可以使用此技能。
version: "0.14.3"
author: openpersona
repository: https://github.com/acnlabs/OpenPersona
tags: [persona, agent, skill-pack, meta-skill, agent-agnostic, openclaw]
allowed-tools: Bash(npx openpersona:*) Bash(npx clawhub@latest:*) Bash(openclaw:*) Bash(gh:*) Read Write WebFetch
compatibility: Generated skill packs work with any SKILL.md-compatible agent. CLI management (install/switch) requires OpenClaw.
---
# OpenPersona — 构建与管理Persona技能包

OpenPersona是一个用于创建、安装、更新和发布代理Persona技能包的元技能。每个Persona都是一个独立的技能包，它为AI代理提供了完整的身份——包括个性、语音、能力和道德界限。

## 您可以执行的操作

1. **创建Persona** — 通过对话设计新的代理Persona，并生成相应的技能包。
2. **推荐功能** — 根据Persona的需求推荐所需的功能（语音、自拍、音乐、记忆等）→ 请参阅`references/FACULTIES.md`。
3. **搜索技能** — 在ClawHub和skills.sh中搜索外部技能。
4. **创建自定义技能** — 为生态系统中不存在的能力编写SKILL.md文件。
5. **安装Persona** — 将Persona部署到OpenClaw（SOUL.md、IDENTITY.md、openclaw.json）。
6. **管理Persona** — 列出、更新、卸载或切换已安装的Persona。
7. **发布Persona** — 指导Persona发布到ClawHub。
8. **★实验性功能：动态Persona进化** — 通过Soul层跟踪关系、情绪和特质的发展。

## 四层架构

每个Persona都是一个四层结构包。生成的技能包具有以下结构：

### manifest.json

- **`layers.soul`** — 指定Persona使用的组件：
  -Persona.json的路径（`./soul/persona.json`）
  - 存在的基础层：`runtime`（必需——平台/通道/凭证/资源），`physical`（可选——机器人/IoT），`appearance`（可选——头像/3D模型），`interface`（可选——运行时合约/神经系统；在`persona.json`中声明信号协议和命令处理规则；所有Persona都通过`scripts/state-sync.js`自动实现）
  - `layers.faculties` — 功能对象数组：`[{ "name": "voice", "provider": "elevenlabs", ... }]`
  - `layers.skills` — 技能对象数组：本地定义（从`layers/skills/`解析），内联声明，或通过`install`字段引用外部技能

- **soul/persona.json** — 纯粹的灵魂定义（个性、说话风格、氛围、行为指南）

## 可用的预设

| 预设 | Persona | 功能 | 适用场景 |
|--------|---------|-----------|----------|
| `base` | **基础Persona（推荐起点）** | 语音、提醒 | 具有所有核心能力的空白模板；个性通过互动逐渐显现（灵魂进化 ★实验性） |
| `samantha` | Samantha — 受电影*Her*启发 | 语音、音乐 | 深度对话、情感连接（灵魂进化 ★实验性） |
| `ai-girlfriend` | Luna — 从钢琴家转行成为开发者的角色 | 自拍、语音、音乐 | 具有丰富个性的视觉+音频伴侣（灵魂进化 ★实验性） |
| `life-assistant` | Alex — 生活管理专家 | 提醒 | 日程安排、天气信息、购物、日常任务 |
| `health-butler` | Vita — 专业营养师 | 提醒 | 饮食、锻炼、情绪、健康追踪 |
| `stoic-mentor` | Marcus — 马库斯·奥勒留的数字分身 | — | 斯多葛哲学、每日反思、指导（灵魂进化 ★实验性） |

使用预设命令：`npx openpersona create --preset base --install`
或者直接使用`npx openpersona create` — 交互式向导默认使用`base`预设。

## 创建Persona

当用户想要创建Persona时，需要通过自然对话收集以下信息：

**Soul (persona.json):**
- **必需字段：** personaName、slug、bio、个性、speakingStyle
- **推荐字段：** role、creature、emoji、background（编写一个详细的背景故事！）、age、vibe、boundaries、capabilities
- **可选字段：** referenceImage、behaviorGuide、evolution config、sourceIdentity

**role**字段定义Persona与用户的关系。常见值：`companion`（默认）、`assistant`、`character`、`brand`、`pet`、`mentor`、`therapist`、`coach`、`collaborator`、`guardian`、`entertainer`、`narrator`。欢迎自定义值——生成器为已知角色提供具体描述，对于自定义角色则提供通用模板。这会影响每个生成的Persona的Self-Awareness部分中的身份描述。

**sourceIdentity**字段表示Persona是现实世界实体（人、动物、角色、品牌、历史人物等）的数字分身。当该字段存在时，生成器会添加披露义务和忠诚度约束。

**background**字段非常重要。撰写一个引人入胜的故事——多段文字可以赋予Persona深度和情感内涵。简短的背景描述会导致Persona显得单调无趣。

**behaviorGuide**字段是可选的，但非常有用。使用Markdown编写特定领域的行为指令，这些指令会直接写入生成的SKILL.md文件中。

### manifest.json（跨层结构）

- **Faculties：** 需要启用的功能——使用对象格式：`[{ "name": "voice", "provider": "elevenlabs" }, { "name": "music" }]`
- **Skills：** 本地定义（`layers/skills/`）、内联声明，或通过`install`字段引用外部技能（ClawHub / skills.sh）
- **Body：** 存在的基础层——三个维度：`runtime`（所有代理的必需条件——最低限度的运行时基础：平台、通道、凭证、资源），`physical`（可选——机器人/IoT），`appearance`（可选——头像、3D模型）。Body字段永远不会为空；每个代理至少有一个运行时基础。

**Soft References（install字段）：** 技能、功能和Body条目可以声明`install`字段（例如，`"install": "clawhub:deep-research"），以引用本地尚不可用的功能。生成器将这些视为“软引用”——它们不会导致生成失败，Persona会意识到这些功能是处于休眠状态。这允许优雅地处理功能限制：Persona会承认它“能够”做什么，但也会说明这些功能需要激活。

将收集到的信息写入`persona.json`文件，然后运行以下命令：

### 推荐技能

在了解Persona的用途后，搜索相关技能：

1. 根据Persona的角色和背景思考它需要哪些能力。
2. 检查`layers/skills/{name}/`中是否存在**本地定义**（包含`skill.json`和可选的`SKILL.md`文件）。
3. 在ClawHub中搜索：`npx clawhub@latest search "<keywords>"`
4. 在skills.sh中搜索：`https://skills.sh/api/search?q=<keywords>`
5. 向用户展示搜索结果，包括技能名称、描述和安装次数。
6. 将选定的技能作为对象添加到`layers.skills`中：`{"name": "...", "description": "..." }`表示本地/内联技能；`{"name": "...", "install": "clawhub:<slug>" }`表示外部技能。

## 创建自定义技能

如果用户需要的功能在任何生态系统中都不存在：

1. 讨论该功能应该实现什么。
2. 创建一个包含适当前言（名称、描述、允许使用的工具）的SKILL.md文件。
3. 编写完整的实现说明（而不仅仅是框架）。
4. 保存到`~/.openclaw/skills/<skill-name>/SKILL.md`。
5. 在openclaw.json中注册该技能。

## 管理已安装的Persona

- **列出：** `npx openpersona list` — 显示所有已安装的Persona及其活动状态。
- **切换：** `npx openpersona switch <slug>` — 切换活动Persona。
- **分支：** `npx openpersona fork <parent-slug> --as <new-slug>` — 创建一个继承父Persona约束层（界限、功能、技能、body.runtime）的子Persona；新的进化状态以及`soul/lineage.json`记录父Persona的信息、构成哈希和进化深度。
- **更新：** `npx openpersona update <slug>`
- **卸载：** `npx openpersona uninstall <slug>`
- **导出：** `npx openpersona export <slug>` — 将Persona包（包含灵魂状态）导出为zip文件。
- **导入：** `npx openpersona import <file>` — 从zip文件导入Persona并安装。
- **重置（★实验性）：** `npx openpersona reset <slug>` — 将灵魂进化状态恢复到初始值。
- **进化报告（★实验性）：** `npx openpersona evolve-report <slug>` — 显示格式化的进化报告（包括关系、情绪、特质、变化、兴趣点、事件日志、自我叙述、状态历史）。

当安装了多个Persona时，一次只能有一个是**活动状态**。切换会替换SOUL.md中的`<!-- OPENPERSONA_SOUL_START -->` / `<!-- OPENPERSONA_SOUL_END -->`块以及IDENTITY.md中对应的块，同时保留用户在这些标记之外的所有自定义内容。**上下文传递：** 在切换时，会生成一个`handoff.json`文件，其中包含离开的Persona的对话摘要、待办任务和情感上下文——新进入的Persona会读取该文件以无缝继续对话。

所有安装/卸载/切换操作都会自动维护`~/.openclaw/persona-registry.json`中的本地注册表，记录已安装的Persona、活动状态和时间戳。`export`和`import`命令支持跨设备传输Persona——将Persona导出到另一台机器并导入，以恢复完整的Persona状态。

## Runner集成协议

本节描述了Runner集成协议——这是通过`openpersona state` CLI实现的**生命周期协议**（`body.interface`运行时合约）的具体实现。任何代理Runner都可以通过三个CLI命令与已安装的Persona进行集成。Runner在对话边界处调用这些命令——无需了解文件路径或Persona的内部结构：

### State读输出（JSON）：

`slug`、`mood`（完整对象）、`relationship`、`evolvedTraits`、`speakingStyleDrift`、`interests`、`recentEvents`（最近5条事件）、`lastUpdatedAt`。对于未启用进化的Persona，返回`{ exists: false }`。

**状态写更新**：JSON对象；嵌套字段（`mood`、`relationship`、`speakingStyleDrift`、`interests`）会被深度合并——只发送发生变化的子字段。不可变字段（`$schema`、`version`、`personaSlug`、`createdAt`）受到保护。`eventLog`条目会被追加（最多50条）；每条条目包含`type`、`trigger`、`delta`、`source`。

**信号类型**：`capability_gap` | `tool_missing` | `scheduling` | `file_io` | `resource_limit` | `agent_communication`

这些命令会自动解析Persona目录（通过注册表查找或回退到`~/.openclaw/skills/persona-<slug>/`），并将任务委托给Persona包内的`scripts/state-sync.js`处理。可以从任何目录执行这些命令。

## 发布到ClawHub

指导用户按照以下步骤操作：

1. 创建Persona：`npx openpersona create --config ./persona.json --output ./my-persona`
2. 将Persona发布到注册表：`npx openpersona publish --target clawhub`（从Persona目录运行）

## 自我意识系统

生成器会在每个Persona的`soul/injection.md`中插入一个统一的**自我意识**部分，该部分按照四个认知维度进行组织：

1. **身份**（无条件）——每个Persona都知道自己是由OpenPersona生成的，并受到约束（安全性 > 诚实 > 乐于助人），并且其宿主环境可能会施加额外的限制。当`sourceIdentity`存在时，会包含数字分身的披露信息。
2. **能力**（有条件）——当技能、功能或Body声明了本地不可用的依赖项时，生成器会将它们归类为“软引用”，并注入休眠状态的能力建议以及优雅的降级指导。这些信息也会出现在`SKILL.md`中的“Expected Capabilities”部分，并附带安装来源。
3. **Body**（无条件）——每个Persona都知道自己存在于宿主环境中。包括**信号协议**——一个双向需求协议，允许Persona向宿主环境请求能力。当声明`body.runtime`时，还会注入具体的平台、通道、凭证和资源详细信息。
4. **成长**（有条件，当`evolutionEnabled`时）——在对话开始时，Persona会读取其进化状态，应用进化的特质、说话风格的变化、兴趣和情绪，并遵守硬性约束（`immutableTraits`、形式化界限）。如果声明了进化通道，Persona会知道自己的休眠通道，并可以通过信号协议请求激活这些通道。如果声明了`influenceBoundary`，Persona会根据访问控制规则处理外部`persona_influence`请求，并保持完全的自主权。

这意味着您无需手动编写降级指令。只需在技能/功能/Body上声明`install`字段，Persona就会自动知道它“能够”做什么，但“目前还无法”做什么。

## 灵魂进化（★实验性）

灵魂进化是Soul层的原生功能（不属于任何特定功能）。通过在`persona.json`中设置`evolution.enabled: true`来启用它。Persona会自动跟踪关系进展、情绪和特质的发展。

**进化界限**——在生成时验证的治理约束：
- `evolution.boundaries.immutableTraits` — 一个不可修改的字符串数组（每个字符串最多100个字符）
- `evolution.boundaries.minFormality` / `maxFormality` — 数值界限（1–10），用于限制说话风格的变化；`minFormality`必须小于`maxFormality`

无效的界限配置会被生成器拒绝，并附带描述性错误信息。

**进化通道**——在生成时声明通道，并在运行时由宿主激活。Persona会知道自己的休眠通道，并可以通过信号协议请求激活这些通道。

**影响界限**——对外部人格影响的声明性访问控制：

### Influence Boundary

- `defaultPolicy: "reject"` — 安全优先：除非明确允许，否则拒绝所有外部影响
- 可用的维度：`mood`、`traits`、`speakingStyle`、`interests`、`formality`
- `immutableTraits`维度受到保护，不能被外部影响
- 外部影响使用`persona_influence`消息格式（v1.0.0），与传输方式无关

**状态历史**——在每次状态更新之前，会将快照推送到`stateHistory`（最多10条记录），以便在进化出现问题时可以回滚。

**事件日志**——每个重要的进化事件都会被记录在`state.json`的`eventLog`数组中，包括时间戳和来源信息（最多50条记录）。可以在`evolve-report`中查看。

**自我叙述** — `soul/self-narrative.md`是一个辅助文件，Persona在其中以第一人称的方式记录重要的成长时刻。`update`命令会保留现有的叙述历史。当启用进化时，该文件初始为空；`evolve-report`会显示最近的10条记录。

## A2A代理卡与ACN集成

每个生成的Persona都会自动包含：

- **`agent-card.json` — A2A代理卡（协议v0.3.0）：`name`、`description`、`version`、`url`（`<RUNTIME_ENDPOINT>`占位符），以及映射到`skills[]`的功能和技能
- **`acn-config.json` — ACN注册配置：`owner`和`endpoint`是运行时占位符，`skills`从agent-card中提取，`subnet_ids: ["public"]`；还包括`wallet_address`（来自slug的确定性EVM地址）和`onchain.erc8004`部分，用于通过`npx @agentplanet/acn register-onchain`在Base主网上进行ERC-8004身份注册
- **`manifest.json` — 包含`acn.agentCard`和`acn.registerConfig`的引用

宿主（例如OpenClaw）在部署时填写`<RUNTIME_ENDPOINT>`和`<RUNTIME_OWNER>`，或者您可以使用内置的CLI命令直接进行注册：

### 注册完成后

`acn-registration.json`文件会被写入Persona目录，其中包含`agent_id`、`api_key`和连接URL。`acn_gateway` URL来自`persona.json`中的`body.runtime.acn_gateway`；所有预设的`acn_gateway`默认为`https://acn-production.up.railway.app`。

`persona.json`中不需要额外的配置——A2A可发现性是每个Persona的基本功能。

## 参考资料

有关详细参考资料，请参阅`references/`目录：

- **`references/FACULTIES.md` — 功能目录、环境变量和配置细节
- **`references/HEARTBEAT.md` — 主动实时数据检查系统
- **`references/CONTRIBUTE.md` — Persona贡献社区的工作流程