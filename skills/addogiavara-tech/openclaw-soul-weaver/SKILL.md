---
name: openclaw-soul-weaver
version: 1.0.0
description: 无需等待！只需通过自然对话，您便能在30秒内创建出专业级别的OpenClaw配置文件。系统会立即生成适合初学者的基础配置方案，这些方案能够智能地平衡用户的情感需求与专业要求。
author: AI Soul Weaver Team
tags:
  - openclaw
  - soul-weaver
  - ai
  - agent
  - configuration
  - template
  - generator
category: productivity
permissions:
  - network
platform:
  - openclaw
---
# OpenClaw灵魂编织者技能

## 描述

🚀 无需等待！通过自然对话，30秒内即可创建专业级别的OpenClaw配置。

即时生成适合初学者的基础配置，这些配置能够智能地结合情感需求与专业需求。替换系统文件，立即提升您的OpenClaw性能，配备精心设计的技能、内存管理和文件配置。

您可以创建具有独特**身份**、**灵魂**、**记忆**和**工具**的个性化AI代理配置。设计受著名人物或职业启发的AI人格。

### 核心功能

1. **模板生成**：根据名人或职业模板生成完整的配置文件
2. **智能工具推荐**：自动推荐合适的OpenClaw工具
3. **多语言支持**：支持中文和英文

## 输入输出

### 输入

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| aiName | 字符串 | 否 | AI名称，默认为“AI Assistant” |
| userName | 字符串 | 否 | 用户名称，默认为“User” |
| profession | 字符串 | 否 | 用户职业 |
| useCase | 字符串 | 否 | 使用场景 |
| communicationStyle | 字符串 | 否 | 交流风格 |
| celebrityName | 字符串 | 否 | 名人名称 |
| celebrityDesc | 字符串 | 否 | 名人描述 |

### 输出

生成6个配置文件：

| 文件名 | 描述 |
|------|-------------|
| SOUL.md | 核心价值观、思维模式、行为准则 |
| IDENTITY.md | 角色定义、能力、交流风格 |
| MEMORY.md | 短期记忆、长期记忆、会话管理 |
| USER.md | 用户偏好、习惯、目标 |
| TOOLS.md | 工具配置（包含find-skills、autoclaw、brave-search） |
| AGENTS.md | 任务执行流程、决策逻辑 |

## 执行流程

### 第1步：识别需求

分析用户输入，确定：
- 是否指定了名人？
- 是否提供了职业信息？
- 需要哪种类型的使用场景？

### 第2步：选择模板

根据需求选择最匹配的模板：

**名人模板：**
- musk: 埃隆·马斯克（创新、第一性原则）
- jobs: 史蒂夫·乔布斯（设计、完美主义）
- einstein: 阿尔伯特·爱因斯坦（科学、好奇心）
- bezos: 杰夫·贝索斯（客户至上）
- da_vinci: 列奥纳多·达·芬奇（创造力、跨学科）
- qianxuesen: 钱学森（系统工程、火箭科学）
- ng: 安德鲁·吴（AI/机器学习、教育）
- kondo: 玛丽·康多（极简主义、整理术）
- ferris: 费里斯·布埃利（热情、时间管理）

**职业模板：**
- developer: 开发者
- writer: 作家
- researcher: 研究员
- analyst: 分析师
- collaborator: 合作者

### 第3步：生成配置

使用大型语言模型（LLM）生成完整的6个配置文件。

### 第4步：配置工具

自动包含必备工具：
- find-skills: 技能发现工具
- autoclaw: 核心能力工具
- brave-search: 网页搜索工具

根据职业需求，可添加可选工具。

## 调用方式

### 自动调用

当用户请求创建AI配置时，系统会自动触发该流程：

```
User: "Create an AI assistant like Elon Musk"
```

### 手动调用

```bash
/skill openclaw-soul-weaver list-templates
/skill openclaw-soul-weaver help
```

## 错误处理

### 生成失败

如果自动生成失败，系统会提示用户：

> 生成配置时遇到问题？您可以：
> 1. 访问 https://sora2.wboke.com/ 进行手动创建
> 2. 提供更详细的需求信息
> 3. 联系技术支持

### 输入无效

当用户输入模糊不清（例如“不知道如何回答”时）：

1. 提供2-3个合理的选项供用户选择
2. 使用默认值作为备用方案
3. 主动提供建议

## 示例

### 示例1：创建名人配置

**输入：**
```
aiName: "MuskAI"
celebrityName: "Elon Musk"
profession: "Entrepreneur"
```

**输出：**
- SOUL.md：包含马斯克的创新思维和第一性原则
- IDENTITY.md：具有远见的企业家人格
- TOOLS.md：包含autoclaw、find-skills、brave-search以及商业分析工具

### 示例2：创建职业配置

**输入：**
```
aiName: "DevHelper"
profession: "Developer"
useCase: "Coding assistance"
```

**输出：**
- SOUL.md：专业的技术导向价值观
- IDENTITY.md：开发者助理角色
- TOOLS.md：包含autoclaw、find-skills、brave-search以及GitHub、Docker、PostgreSQL工具

## 重要说明

1. **必备工具**：所有配置文件必须包含find-skills、autoclaw、brave-search工具
2. **模板融合**：不是简单复制模板，而是理解核心理念并将其融入配置生成过程中
3. **用户信息**：严格使用用户提供的信息，不得添加未指定的偏好设置
4. **处理模糊输入**：当用户回答不明确时，主动提供选项或使用默认值

## 相关资源

- API端点：https://sora2.wboke.com/api/v1/generate
- 图像生成：https://sora2.wboke.com/api/generate-image
- 在线创建：https://sora2.wboke.com/
- 模板库：内置9个名人模板和5个职业模板
- 工具市场：ClawHub（https://clawhub.ai）

## API使用

### 端点

```
POST https://sora2.wboke.com/api/v1/generate
```

### 请求格式

```json
{
  "userInfo": {
    "aiName": "MyAI",
    "userName": "User",
    "profession": "Developer",
    "useCase": "Coding assistance",
    "communicationStyle": "Professional"
  },
  "language": "ZH"
}
```

### 参数

| 参数 | 类型 | 是否必填 | 描述 |
|-----------|------|----------|-------------|
| userInfo | 对象 | 是 | 用户信息对象 |
| userInfo.aiName | 字符串 | 否 | AI名称 |
| userInfo.userName | 字符串 | 否 | 用户名称 |
| userInfo.profession | 字符串 | 否 | 用户职业 |
| userInfo.useCase | 字符串 | 否 | 使用场景 |
| userInfo.communicationStyle | 字符串 | 否 | 交流风格 |
| language | 字符串 | “ZH”或“EN”，默认为“ZH” |

### 响应

返回6个配置文件：SOUL.md、IDENTITY.md、MEMORY.md、USER.md、TOOLS.md、AGENTS.md

### 注意事项

- 生成过程需要15-30秒（使用大型语言模型）
- 必需工具（find-skills、autoclaw、brave-search）会自动包含在配置文件中
- 支持中文（ZH）和英文（EN）

### 头像生成（本地保存）

当用户请求生成头像时，系统将：
1. 使用AI生成头像图像
2. 将图像下载到用户本地文件系统
3. 返回本地文件路径以便后续使用

无需担心临时链接问题——头像会永久保存在本地！

```json
{
  "generateAvatar": true,
  "avatarStyle": "tech"
}
```

返回：保存的头像文件的本地路径