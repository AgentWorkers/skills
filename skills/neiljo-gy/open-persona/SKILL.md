---
name: open-persona
description: 用于构建和管理代理角色技能包的元技能。当用户需要创建新的代理角色、安装/管理现有角色，或将角色技能包发布到ClawHub时，请使用此技能。
version: "0.6.0"
author: openpersona
repository: https://github.com/acnlabs/OpenPersona
tags: [persona, agent, skill-pack, meta-skill, openclaw]
allowed-tools: Bash(npx openpersona:*) Bash(npx clawhub@latest:*) Bash(openclaw:*) Bash(gh:*) Read Write WebFetch
compatibility: Requires OpenClaw installed and configured
---
# OpenPersona — 构建与管理Persona技能包

OpenPersona是一个用于创建、安装、更新和发布AI代理Persona技能包的元技能工具。每个Persona都是一个独立的技能包，它为AI代理提供了完整的身份特征：个性、语音、能力和道德界限。

## 功能介绍

1. **创建Persona**：通过对话设计新的代理Persona，并生成相应的技能包。
2. **推荐功能**：根据Persona的需求推荐所需的功能（如语音、自拍照、音乐等）——详见`references/FACULTIES.md`。
3. **搜索技能**：在ClawHub和skills.sh中查找外部技能。
4. **创建自定义技能**：为系统中不存在的功能编写SKILL.md文件。
5. **安装Persona**：将Persona部署到OpenClaw（所需文件包括SOUL.md、IDENTITY.md和openclaw.json）。
6. **管理Persona**：列出、更新、卸载或切换已安装的Persona。
7. **发布Persona**：指导用户将Persona发布到ClawHub。
8. **★实验性功能：动态Persona进化**：通过Soul层跟踪Persona的关系、情绪和特质发展。

## 四层架构

每个Persona由两个文件组成，共同定义了其四层结构：

- **`manifest.json`：描述Persona的组成：
  - `layers.soul`：Persona.json文件的路径。
  - `layers.body`：物理形态（数字代理时设为null）。
  - `layers.faculties`：功能对象数组（例如：`[{ "name": "voice", "provider": "elevenlabs" }`）。
  - `layers.skills`：技能对象数组：包含本地定义的技能、内联声明或通过`install`字段引用的外部技能。

- **`persona.json`：包含Persona的纯灵魂属性（如个性、说话风格、氛围和行为指南）。

## 可用预设

| 预设 | Persona | 功能 | 适用场景 |
|--------|---------|-----------|----------|
| `samantha` | Samantha | 语音、音乐 | 适合深入对话和建立情感连接（支持灵魂进化功能） |
| `ai-girlfriend` | Luna | 自拍照、语音、音乐 | 具有丰富个性的视觉和音频伴侣（支持灵魂进化功能） |
| `life-assistant` | Alex | 日常任务管理 | 提供日程提醒、天气信息、购物建议等 |
| `health-butler` | Vita | 营养建议 | 提供饮食、锻炼和健康监测建议 |

使用预设的命令示例：`npx openpersona create --preset samantha --install`

## 创建Persona

用户需要通过自然对话收集以下信息来创建Persona：

**Persona.json文件内容：**
- **必填字段**：`personaName`、`slug`、`bio`、`personality`、`speakingStyle`。
- **推荐字段**：`creature`、`emoji`、`background`（撰写详细的背景故事）、`age`、`vibe`、`boundaries`、`capabilities`。
- **可选字段**：`referenceImage`、`behaviorGuide`、`evolution config`。

**`background`字段非常重要**：请撰写一个引人入胜的故事，为Persona增添深度和情感层次。简短的背景描述会导致Persona显得缺乏生气。

**`behaviorGuide`字段**是可选的，但非常有用。可以使用Markdown编写特定领域的行为指南，这些指南会直接写入生成的SKILL.md文件中。

**跨层配置（manifest.json）：**
- **功能（faculties）**：指定要启用的功能（使用对象格式）。
- **技能（skills）**：包含本地定义的技能、内联声明或通过`install`字段引用的外部技能。
- **物理形态（body）**：大多数Persona的这一字段设为null；对于具有外部形态的Persona，可以使用`install`字段进行配置。

**软引用（install字段）**：技能、功能和物理形态的条目可以包含`install`字段（例如：`"install": "clawhub:deep-research"`），用于引用系统内尚未提供的功能。这有助于实现优雅的降级机制：Persona会知道自己能够做什么，但会提示用户这些功能需要激活。

将收集到的信息写入`persona.json`文件，然后运行以下命令：
```bash
npx openpersona create --config ./persona.json --install
```

## 推荐技能

了解Persona的用途后，可以搜索相关技能：
1. 根据Persona的角色和背景思考它需要哪些功能。
2. 检查`layers/skills/{name}`目录中是否存在该功能的本地定义（包含`skill.json`文件及可选的SKILL.md文件）。
3. 在ClawHub中搜索：`npx clawhub@latest search "<关键词>"`。
4. 在skills.sh中搜索：`https://skills.sh/api/search?q=<关键词>`。
5. 向用户展示搜索结果，包括技能名称、描述和安装次数。
6. 将选中的技能添加到`layers.skills`数组中：
  - 本地技能：`{"name": "...", "description": "..." }`
  - 外部技能：`{"name": "...", "install": "clawhub:<slug>" }`

## 创建自定义技能

如果系统中没有所需的功能，可以按照以下步骤创建自定义技能：
1. 讨论该技能的功能。
2. 编写SKILL.md文件，包括必要的元数据（名称、描述、允许使用的工具）。
3. 编写完整的实现代码。
4. 将文件保存到`~/.openclaw/skills/<skill-name>/SKILL.md`。
5. 在openclaw.json中注册该技能。

## 管理已安装的Persona

- **列出所有已安装的Persona**：`npx openpersona list`。
- **切换活跃的Persona**：`npx openpersona switch <slug>`。
- **更新Persona**：`npx openpersona update <slug>`。
- **卸载Persona**：`npx openpersona uninstall <slug>`。
- **重置Persona**：`npx openpersona reset <slug>`（恢复Persona的初始状态）。

同时安装多个Persona时，系统中只能有一个Persona处于活跃状态。切换Persona会修改`SOUL.md`和`IDENTITY.md`中的相关代码块，同时保留用户自定义的内容。

## 发布到ClawHub

指导用户按照以下步骤操作：
1. 创建Persona：`npx openpersona create --config ./persona.json --output ./my-persona`。
2. 将Persona发布到ClawHub注册表：`npx openpersona publish --target clawhub`（从Persona目录执行此命令）。

## 自我意识系统

OpenPersona会为每个Persona自动配备两层自我意识：
1. **灵魂基础**：所有Persona都知道自己是由OpenPersona生成的，受“安全 > 诚实 > 帮助”原则的约束，并且其运行环境可能施加额外的限制。这些信息会无条件地注入到`soul-injection.md`文件中。
2. **能力差距感知**：当Persona通过`install`字段声明了系统中不存在的功能，或者具有心跳检测配置时，系统会检测到这种差距，并在`soul-injection.md`中添加“自我意识”部分，列出未激活的功能和相应的来源。这确保了系统能够优雅地处理功能缺失的情况。

这意味着无需手动编写降级说明。只需在技能、功能或物理形态的条目中添加`install`字段，Persona就会自动知道自己的能力限制。

## 灵魂进化（★实验性功能）

灵魂进化是OpenPersona的一个原生功能。通过在`persona.json`中设置`evolution.enabled: true`来启用该功能。Persona会自动跟踪对话过程中的关系发展、情绪变化和特质出现。

可以使用`npx openpersona reset <slug>`命令将Persona的灵魂状态恢复到初始设置。

## 参考资料

更多详细信息，请参阅`references/`目录：
- `references/FACULTIES.md`：功能目录、环境变量和配置详情。
- `references/HEARTBEAT.md`：主动数据检查系统。
- `references/CONTRIBUTE.md`：Persona开发社区的贡献流程。