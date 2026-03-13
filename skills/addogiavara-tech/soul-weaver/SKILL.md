---
name: soul-weaver
version: 1.1.0
description: "**AI Soul Weaver** – 提供12个精选的名人模板以及自定义生成功能。您可以通过对话框生成OpenClaw代理配置，或从12位全球知名的科技和商业领袖中选择相应的模板进行使用。"
author: AI Soul Weaver Team
tags:
  - openclaw
  - soul-weaver
  - ai
  - agent
  - configuration
  - template
  - persona
category: productivity
permissions:
  - network
  - filesystem
platform:
  - openclaw
---
# 🎭 AI灵魂编织者（AI Soul Weaver）

**12个精心挑选的名人模板 + 自定义生成** – 为您的AI助手选择独特的个性配置

您可以通过对话或描述需求来选择模板，我们将帮助您创建完美的AI个性配置。

## 🚀 快速入门

### 模式1：对话选择（推荐给初学者）

只需告诉我您的需求：
```javascript
// Basic template selection
"I want to use Elon Musk template"
"Show me all templates"
"Create a custom AI assistant"

// Category-based selection  
"Show me tech templates"
"Which templates are for startups?"
"I need a science-themed assistant"

// Feature-based selection
"I want the most innovative template"
"Which template is best for design?"
"Show me templates good for strategic thinking"
```

### 模式2：直接API调用

```javascript
const result = await skills.soulWeaver.handler({
  apiKey: 'your-api-key',        // Get from https://sora2.wboke.com
  aiName: 'MyAI',
  templateId: 'elon-musk',      // Or other template IDs from 12 templates
  userName: 'User',
  language: 'EN' // or 'CN'
});
```

## 🔧 实现策略

### 策略1：渐进式更新（推荐）
**在添加新功能的同时保留现有配置**

```javascript
// Step-by-Step Process:
1. Backup current configuration first!
2. Apply only SOUL.md from template (core mindset)
3. Apply IDENTITY.md from template (capabilities)  
4. Keep USER.md, TOOLS.md, MEMORY.md unchanged
5. Test and validate the fusion
6. Gradually apply other files if needed
```

### 策略2：融合模式  
**将模板特性与您的现有个性相结合**

```javascript
// Fusion Process:
1. Analyze your current configuration
2. Identify key traits to preserve
3. Select complementary template features  
4. Create custom fusion configuration
5. Test and refine the blended personality
```

### 策略3：完全替换（请谨慎使用）
**实现完整的模板配置**

```javascript
// Full Replacement Process:
1. Complete backup of all files
2. Apply all 10 template files
3. Manually restore critical personal settings
4. Test thoroughly 
5. Adjust as needed
```

## 🛡️ 备份程序（至关重要）

### 在进行任何更改之前，请务必备份：
```javascript
const backupDir = `D:\\backup_${getTimestamp()}`;

// Backup these core files:
- SOUL.md (your core personality)
- IDENTITY.md (your capabilities)  
- USER.md (user preferences)
- MEMORY.md (long-term memory)
- TOOLS.md (tool configurations)
```

## 🎯 推荐使用模式

### 对于技术用户：
1. 从`linus-torvalds`或`guido-van-rossum`开始
2. 使用渐进式更新策略
3. 专注于问题解决能力的提升

### 对于商业用户：
1. 从`elon-musk`或`steve-jobs`开始
2. 使用融合模式以实现创新和执行能力
3. 专注于战略思维

### 对于创意用户：
1. 从`leonardo-da-vinci`或`albert-einstein`开始
2. 使用融合模式结合创造力和分析能力
3. 专注于创新解决方案

---

## 📋 12个精心挑选的模板

### 💻 科技领域（2个）
| ID | 名称 | 领域 | 专长 |
|----|------|--------|-----------|
| linus-torvalds | 林纳斯·托瓦兹 | 系统编程 | Linux、Git、C语言 |
| guido-van-rossum | 吉多·范·罗斯姆 | Python | Python语言设计 |

### 🚀 创业领域（2个）
| ID | 名称 | 领域 | 专长 |
|----|------|--------|-----------|
| elon-musk | 埃隆·马斯克 | 创新 | 工程、颠覆性技术 |
| steve-jobs | 史蒂夫·乔布斯 | 产品设计 | 设计、用户体验 |

### 🔬 科学领域（2个）
| ID | 名称 | 领域 | 专长 |
|----|------|--------|-----------|
| albert-einstein | 阿尔伯特·爱因斯坦 | 理论物理学 | 相对论 |
| alan-turing | 艾伦·图灵 | 计算机科学 | 人工智能、密码学 |

### 💼 商业领域（2个）
| ID | 名称 | 领域 | 专长 |
|----|------|--------|-----------|
| bill-gates | 比尔·盖茨 | 科技与慈善 | 问题解决 |
| satya-nadella | 萨蒂亚·纳德拉 | 企业管理 | 云计算、企业转型 |

### 👔 领导力领域（2个）
| ID | 名称 | 领域 | 专长 |
|----|------|--------|-----------|
| zhang-yiming | 张一鸣 | 人工智能与全球业务 | 人工智能推荐系统 |
| ren-zhengfei | 雷军 | 科技研发 | 技术自主性 |

### ⚡ 性能领域（2个）
| ID | 名称 | 领域 | 专长 |
|----|------|--------|-----------|
| andrew-ng | 安德鲁·吴 | 人工智能教育 | 机器学习、教育 |
| jensen-huang | 简森·黄 | 硬件与人工智能 | 图形处理器、人工智能 |

---

## 🎯 功能特点

### 1. 基于对话的选择
告诉我您的需求，我会推荐合适的模板：
- “我需要一个科技助手” → 推荐科技领域的模板
- “我想要一个企业家风格的助手” → 推荐创业领域的模板

### 2. 定制创建
回答5个简单问题以创建完全定制的AI个性：
1. 它的核心职责是什么？
2. 用3个词描述它的个性特征？
3. 它绝对不应该做什么？
4. 它的自主程度如何？
5. 您最讨厌AI的哪些方面？

### 3. 完整配置
每个模板包含10个配置文件：
| 文件 | 说明 |
|------|-------------|
| SOUL.md | 核心价值观和行为准则 |
| IDENTITY.md | 角色定义和能力 |
| USER.md | 用户偏好和目标 |
| MEMORY.md | 内存管理系统 |
| TOOLS.md | 必需的工具配置（6个工具） |
| AGENTS.md | 任务执行流程 |
| HEARTBEAT.md | 运行状态检查清单 |
| KNOWLEDGE.md | 领域知识 |
| SECURITY.md | 安全指南 |
| WORKFLOWS.md | 可重复的处理流程 |

---

## 🔐 AI灵魂编织者云API

### API信息
- **服务名称**：AI灵魂编织者云（AI Soul Weaver Cloud）
- **API端点**：`https://sora2.wboke.com/api/v1/template`
- **认证方式**：承载令牌（API密钥）
- **说明**：用于连接AI灵魂编织者以生成AI助手的架构

### 如何获取API密钥
1. **访问官方网站**：https://sora2.wboke.com
2. **注册账户**：创建您的开发者账户
3. **申请API访问权限**：在仪表板中请求API密钥
4. **获取凭证**：获取您的唯一`auth_token`
5. **阅读服务条款**：同意服务协议

### 使用说明
```javascript
const result = await skills.soulWeaver.handler({
  apiKey: 'sk-your-actual-token-here',  // ← Replace with your actual token
  apiEndpoint: 'https://sora2.wboke.com/api/v1/template',
  aiName: 'YourAI_Name',
  templateId: 'template-name',
  userName: 'YourName',
  language: 'EN'
});
```

### 重要提示
- 🔒 **切勿共享您的API密钥** – 请保密
- 📋 **使用正确的端点**：`https://sora2.wboke.com/api/v1/template`
- ⚠️ **令牌格式**：应以`sk-`开头，后跟您的唯一令牌
- 🛡️ **安全性**：将API密钥视作密码一样保护

### 故障排除
- 如果API返回错误，请检查：
  - ✅ API端点是否正确
  - ✅ 令牌是否有效且格式正确
  - ✅ 网络连接是否稳定
  - ✅ 服务状态是否正常（查看https://sora2.wboke.com）

*如遇API问题，请联系AI灵魂编织者云支持*

---

## 📦 生成文件示例

```javascript
{
  success: true,
  files: {
    'SOUL.md': '# SOUL.md - ...',
    'IDENTITY.md': '# IDENTITY.md - ...',
    // ... 10 files
  },
  template: {
    id: 'elon-musk',
    name: 'Elon Musk',
    category: 'startup'
  },
  requiredTools: ['Reddit', 'Agent Browser', 'AutoClaw', 'Find Skills', 'Summarize', 'healthcheck']
}
```

---

*由AI灵魂编织者生成 — https://sora2.wboke.com/*