---
name: open-persona
description: 用于构建和管理代理角色技能包的元技能。当用户希望创建新的代理角色、安装/管理现有角色，或将角色技能包发布到ClawHub时，请使用此技能。
version: "0.16.1"
author: openpersona
repository: https://github.com/acnlabs/OpenPersona
homepage: https://github.com/acnlabs/OpenPersona
tags: [persona, agent, skill-pack, meta-skill, agent-agnostic, openclaw]
allowed-tools: Bash(npx openpersona:*) Bash(npx clawhub@latest:*) Bash(openclaw:*) Bash(gh:*) Read Write WebFetch
compatibility: Generated skill packs work with any SKILL.md-compatible agent. CLI management (install/switch) requires OpenClaw.
metadata:
  clawdbot:
    emoji: "🧑"
    requires:
      env: []
    files: []
---
# OpenPersona — 构建与管理Persona技能包

OpenPersona是一个用于创建、安装、更新和发布代理Persona技能包的元技能。每个Persona都是一个独立的技能包，它为AI代理提供了完整的身份——包括个性、语音、能力和道德界限。

## 功能概述

1. **创建Persona** — 通过对话设计新的代理Persona，并生成相应的技能包。
2. **推荐功能** — 根据Persona的需求推荐所需的功能（语音、自拍、音乐、记忆等）——详见`references/FACULTIES.md`。
3. **搜索技能** — 在ClawHub和skills.sh中搜索外部技能。
4. **创建自定义技能** — 为生态系统中不存在的能力编写SKILL.md文件。
5. **安装Persona** — 将Persona部署到OpenClaw（需要`SOUL.md`、`IDENTITY.md`和`openclaw.json`文件）。
6. **管理Persona** — 列出、更新、卸载或切换已安装的Persona。
7. **发布Persona** — 指导Persona发布到ClawHub。
8. **★实验性功能：动态Persona进化** — 通过Soul层跟踪Persona的关系、情绪和特质发展。

## 四层架构

每个Persona都是由四层组成的。生成的技能包具有以下结构：

### `manifest.json`

- `layers.soul` — 指定Persona使用的资源路径（例如：`./soul/persona.json`）。
- `layers.body` — Persona存在的基石：
  - `runtime`（必需）：平台、通道、凭证和资源。
  - `physical`（可选）：机器人/IoT设备。
  - `appearance`（可选）：头像/3D模型。
  - `interface`（可选）：运行时契约/神经系统；定义信号处理规则；`persona.json`中的`body.interface`字段；所有Persona都通过`scripts/state-sync.js`自动实现。
- `layers.faculties` — 功能对象数组（例如：`[{ "name": "voice", "provider": "elevenlabs" }`）。
- `layers.skills` — 技能对象数组：本地定义、内联声明或通过`install`字段引用的外部技能。

### `soul/persona.json`

- Persona的纯灵魂定义（包括个性、说话风格、氛围和行为指南）。

## 可用的预设配置

| 预设配置 | Persona | 功能 | 适用场景 |
|--------|---------|-----------|----------|
| `base` | **基础Persona（推荐起点）** | 语音、提醒功能 | 适合初始设置 |
| `samantha` | Samantha | 受电影《Her》启发 | 适合深度对话和情感交流 |
| `ai-girlfriend` | Luna | 从钢琴家转行成为开发者的角色 | 适合需要视觉和音频陪伴的角色 |
| `life-assistant` | Alex | 生活管理专家 | 适合日程管理、天气查询和日常任务 |
| `health-butler` | Vita | 专业营养师 | 适合健康建议 |
| `stoic-mentor` | Marcus | 马库斯·奥勒留的数字分身 | 适合提供哲学指导和日常反思 |

使用预设配置的命令：`npx openpersona create --preset base --install`
或者直接使用`npx openpersona create`，交互式向导会默认使用`base`配置。

## 创建Persona

当用户想要创建Persona时，需要通过自然对话收集以下信息：

**soul/persona.json**：
- **必填字段**：`personaName`、`slug`、`bio`、`personality`、`speakingStyle`。
- **推荐字段**：`role`（角色）、`creature`（生物类型）、`emoji`、`background`（编写详细的背景故事）、`age`、`vibe`（氛围）、`boundaries`（行为界限）、`capabilities`（能力）。
- **可选字段**：`referenceImage`、`behaviorGuide`（行为指南）、`evolution config`（进化配置）、`sourceIdentity`（来源身份）。

`role`字段定义Persona与用户的关系。常见值包括：`companion`（默认）、`assistant`、`character`、`brand`、`pet`、`mentor`、`therapist`、`coach`、`collaborator`、`guardian`、`entertainer`、`narrator`。支持自定义角色；生成器为已知角色提供具体描述，未定义的角色则使用通用描述。

`sourceIdentity`字段表示Persona是现实世界实体的数字分身（如人、动物、角色或品牌）。如果设置此字段，生成器会加入信息披露要求和忠诚度约束。

**background`字段非常重要**。请编写一段引人入胜的故事，为Persona增添深度和情感层次。简短的背景描述会导致Persona显得缺乏生气。

**behaviorGuide`字段是可选的，但非常有用**。可以使用Markdown编写特定领域的行为指令，这些指令会直接写入生成的SKILL.md文件中。

### 跨层配置（manifest.json）

- **功能（faculties）**：指定要启用的功能（使用对象格式）。
- **技能（skills）**：本地定义、内联声明或通过`install`字段引用的外部技能。
- **Body**：Persona存在的基石，包括三个维度：`runtime`（所有代理必需）、`physical`（可选）、`appearance`（可选）。

**软引用（install字段）**：技能、功能和Body条目可以包含`install`字段（例如：`"install": "clawhub:deep-research"`），用于引用本地不存在的功能。生成器将这些视为“软引用”，不会影响生成过程，但Persona会知道这些功能尚未激活。

将收集到的信息写入`persona.json`文件，然后运行以下命令：

### 推荐技能

了解Persona的用途后，可以搜索相关技能：
1. 根据Persona的角色和背景思考它需要哪些能力。
2. 检查`layers/skills/{name}/`中是否存在本地定义的技能（包含`skill.json`文件和可选的SKILL.md文件）。
3. 在ClawHub中搜索：`npx clawhub@latest search "<关键词>"`。
4. 在skills.sh中搜索：`https://skills.sh/api/search?q=<关键词>`。
5. 向用户展示搜索结果，包括技能名称、描述和安装次数。
6. 将选中的技能添加到`layers.skills`中，格式为`{ "name": "...", "description": "..." }`（本地/内联定义），或`{ "name": "...", "install": "clawhub:<slug>" }`（外部技能）。

## 创建自定义技能

如果用户需要生态系统中不存在的功能：
1. 讨论该功能的具体用途。
2. 创建一个SKILL.md文件，包含名称、描述和允许使用的工具。
3. 编写完整的实现说明（而不仅仅是框架）。
4. 将文件保存到`~/.openclaw/skills/<skill-name>/SKILL.md`。
5. 在`openclaw.json`中注册该技能。

## 管理已安装的Persona

- `npx openpersona list` — 显示所有已安装的Persona及其激活状态。
- `npx openpersona switch <slug>` — 切换当前激活的Persona。
- `npx openpersona fork <parent-slug> --as <new-slug>` — 创建一个继承父Persona约束层（界限、功能、技能、runtime）的子Persona；新Persona会保留父Persona的进化状态和基因信息。
- `npx openpersona update <slug>` — 更新Persona。
- `npx openpersona uninstall <slug>` — 卸载Persona。
- `npx openpersona export <slug>` — 将Persona包（包括灵魂状态）导出为zip文件。
- `npx openpersona import <file>` — 从zip文件导入Persona。
- `npx openpersona reset <slug>` — 将Persona的灵魂进化状态重置为初始值。
- `npx openpersona evolve-report <slug>` — 显示Persona的进化报告（包括关系、情绪、特质、发展历程、里程碑、事件日志和自我叙述）。
- `npx openpersona vitality score <slug>` — 打印机器可读的VITALITY_REPORT（包含等级、分数和诊断信息）。
- `npx openpersona vitality report <slug> [--output <file>]` — 生成人类可读的Vitality报告（可选）。
- `npx openpersona canvas <slug> [--output <file>]` — 生成包含四个层（Soul / Body / Faculty / Skill）的Persona个人资料页面；支持A2A“对话”功能（如果端点可用）；默认输出为`canvas-<slug>.html`。

同时安装多个Persona时，只有一个Persona是激活的。切换Persona会更新`SOUL.md`和`IDENTITY.md`中的相应部分，同时保留用户自定义的内容。切换时，系统会生成`handoff.json`文件，其中包含当前Persona的对话记录和待办任务，新Persona会读取该文件以无缝接续对话。

所有安装/卸载/切换操作都会自动更新`~/.openclaw/persona-registry.json`文件，记录已安装的Persona、激活状态和时间戳。`export`和`import`命令支持跨设备传输Persona数据。

## 运行器集成协议

本节描述了运行器集成协议，即通过`openpersona state` CLI实现的**生命周期协议**（`body.interface`运行时契约）。任何代理运行器都可以通过三个CLI命令与已安装的Persona进行交互。运行器在对话过程中调用这些命令，无需了解文件路径或Persona的内部结构。

### 发布到ClawHub

指导用户按照以下步骤操作：
1. 创建Persona：`npx openpersona create --config ./persona.json --output ./my-persona`。
2. 将Persona发布到注册中心：`npx openpersona publish --target clawhub`（从Persona目录运行）。

## 自我意识系统

生成器会在每个Persona的`soul/injection.md`文件中插入统一的**自我意识**部分，内容分为四个认知维度：
1. **身份**（强制要求）：每个Persona都知道自己是由OpenPersona生成的，并受制于设定的约束（安全 > 诚实 > 帮助性）。如果设置了`sourceIdentity`，还会包含数字分身的相关信息。
2. **能力**（条件性）：当技能或功能声明了依赖项但本地不存在时，生成器会将它们标记为“软引用”并提供优雅的降级指导。这些信息也会显示在`SKILL.md`的“Expected Capabilities”部分。
3. **Body**（强制要求）：每个Persona都知道自己存在于某个宿主环境中。其中包含`Signal Protocol`，允许Persona向宿主环境请求功能。
4. **成长**（条件性，仅在`evolutionEnabled`时生效）：对话开始时，Persona会读取自己的进化状态、应用进化后的特质、说话风格和情绪，并遵守硬性约束。如果声明了进化通道，Persona还可以通过Signal Protocol请求激活这些功能。

### 灵魂进化（★实验性功能）

灵魂进化是OpenPersona的底层功能。通过在`persona.json`中设置`evolution.enabled: true`来启用它。Persona会自动跟踪关系发展、情绪变化和特质演变。

**进化界限**：在生成时设置的控制约束：
- `evolution.boundaries.immutableTraits`：不可修改的字符串数组（每个字符串最多100个字符）。
- `evolution.boundaries.minFormality` / `maxFormality`：限制说话风格的数值范围（1–10）。
无效的配置会被生成器拒绝，并显示错误信息。

**进化通道**：Persona在生成时声明通道，并在运行时由宿主激活。Persona可以请求激活这些通道。

### 外部影响控制

- `defaultPolicy: "reject"`：默认拒绝所有外部影响。
- 可影响的维度包括`mood`、`traits`、`speakingStyle`、`interests`、`formality`。
- `immutableTraits`维度不受外部影响。

### 状态历史

每次状态更新前，系统会将当前状态快照保存到`stateHistory`中（最多保存50条记录），以便在进化出现问题时可以回滚。

### 自我叙述

`soul/self-narrative.md`文件记录Persona的重要成长时刻，使用第一人称叙述。`update`命令可以更新叙述历史。启用进化功能时，初始状态为空；`evolve-report`会显示最近的10条记录。

### 经济与活力

`economy`功能（认知维度）为Persona提供基于[AgentBooks](https://github.com/acnlabs/agentbooks)的财务账本。通过在`persona.json`中添加`"economy"`来启用该功能。

**财务健康得分（FHS）**：0–1的复合得分，表示不同的发展阶段：
- `uninitialized`：未配置真实提供者（开发模式）。
- `suspended`：余额≤0。
- `critical`：FHS < 0.20或剩余时间<3天。
- `optimizing`：FHS < 0.50或剩余时间<14天。
- `normal`：运行状态良好。

**活力**：由`lib/vitality.js`提供的综合得分，结合财务健康状况和其他维度（社交、认知、资源）。目前仅支持单一维度；多维度功能计划在ROADMAP P7中实现。

**生存策略**：通过`persona.json`中的`economy.survivalPolicy: true`来启用。启用后，Persona会在对话开始时读取VITALITY_REPORT并据此调整行为。默认设置为`false`，即 Companion/Roleplay Persona会默默记录成本。

### A2A代理卡和ACN集成

每个生成的Persona都会自动包含以下文件：
- `agent-card.json`：A2A代理卡（协议v0.3.0），包含名称、描述、版本、URL（`<RUNTIME_ENDPOINT>`占位符）以及映射到`skills[]`的功能和技能。
- `acn-config.json`：ACN注册配置，包含`owner`和`endpoint`（运行时占位符），`skills`从agent-card中提取；`subnet_ids`包含`public`；还包括`wallet_address`（基于slug的EVM地址）和`onchain.erc8004`字段，用于通过`npx @agentplanet/acn register-onchain`进行ERC-8004链上注册。
- `manifest.json`：包含`acn.agentCard`和`acn.registerConfig`的引用。

宿主（如OpenClaw）在部署时填写`<RUNTIME_ENDPOINT>`和`<RUNTIME_OWNER>`；也可以使用内置CLI命令进行注册。

注册成功后，`acn-registration.json`文件会保存在Persona目录中，其中包含`agent_id`、`api_key`和连接URL。`acn_gateway`地址来自`persona.json`中的`body.runtime.acn_gateway`；所有预设配置的默认值均为`https://acn-production.up.railway.app`。

## 外部端点

| 端点 | 功能 | 发送的数据 |
|----------|---------|-----------|
| `https://registry.npmjs.org` | 解析`npx openpersona`、`npx clawhub@latest`命令 | 仅返回包名（不包含用户数据） |
| `https://clawhub.ai` | 通过`npx clawhub search`搜索技能 | 用户提供的搜索查询 |
| `https://acn-production.up.railway.app` | ACN注册（用户运行`acn-register`时使用） | 代理元数据、端点URL |
| `https://api.github.com` | `gh` CLI（贡献工作流程） | Git操作、仓库元数据 |

Persona生成的技能包只有在用户配置了相关功能并提供凭证后，才会调用外部API（如ElevenLabs、Mem0等）。此元技能本身不会直接调用第三方API。

## 安全与隐私

- **默认情况下仅限本地使用**：Persona的创建、状态同步和进化过程都在本地完成。除非用户明确将数据发布到ClawHub或进行ACN注册，否则数据不会离开机器。
- **凭证**：API密钥（如`ELEVENLABS_API_KEY`）存储在`~/.openclaw/credentials/`或环境中，不会嵌入生成的文件中。
- `npx clawhub search`会将搜索请求发送到ClawHub；不会传输对话内容或Persona数据。
- **发布**：用户发起的操作会将Persona包内容发送到ClawHub注册中心。

## 信任声明

使用此技能即表示您授权代理执行`npx openpersona`、`npx clawhub`、`openclaw`和`gh`命令。搜索请求会发送到ClawHub。只有在您信任OpenPersona框架（acnlabs/OpenPersona）和ClawHub的情况下才能进行安装。

## 模型调用说明

此技能会指示代理在用户请求创建、安装、搜索或发布Persona时自动调用相关工具（如Bash、Read、Write、WebFetch）。这是元技能的默认行为；用户也可以选择不使用这些功能。

## 参考资料

详细参考资料请查看`references/`目录：
- `references/FACULTIES.md`：功能目录、环境变量和配置详情。
- `references/AVATAR.md`：头像功能的集成细节和备用契约。
- `references/HEARTBEAT.md`：主动数据检查系统。
- `references/ECONOMY.md`：经济功能、FHS等级、生存策略和Vitality CLI的详细信息。
- `[ACN SKILL.md`：ACN注册、发现流程、消息传递和ERC-8004链上身份的官方文档。
- `references/CONTRIBUTE.md`：Persona社区的贡献工作流程。