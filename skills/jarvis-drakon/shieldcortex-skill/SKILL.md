# ShieldCortex — 为AI代理提供持久内存与安全保障

让您的AI代理拥有在会话之间保持数据持久性的能力，并保护其免受内存污染攻击。

## 产品描述

ShieldCortex是一个具备内置安全功能的完整内存管理系统。它为AI代理提供持久化、智能化的存储空间，支持语义搜索、知识图谱、基于遗忘机制的数据管理以及矛盾检测功能。所有内存写入操作都会经过六层安全防护机制的审核，有效阻止提示注入、凭证泄露和恶意攻击。

**适用场景：**
- 当您希望代理在会话之间保留数据（如决策、偏好设置、系统架构、上下文信息）时；
- 当您需要跨历史数据执行语义搜索（而不仅仅是简单的关键词匹配）时；
- 当您需要自动整理、清理和更新内存内容时；
- 当您希望从内存中提取知识图谱（包括实体和关系信息）时；
- 当您需要保护内存免受提示注入或恶意攻击时；
- 当您需要审计内存中存储和检索的内容时；
- 当您希望扫描代理指令文件（如SKILL.md、.cursorrules、CLAUDE.md）中的隐藏威胁时。

**不适用场景：**
- 当您仅需要简单的键值存储功能时（请使用配置文件）；
- 当您只需要临时性的会话上下文数据时（请使用代理内置的上下文管理功能）；
- 当您需要用于RAG（Retrieval-Augmentation-Generation）流程的向量数据库时（ShieldCortex主要用于代理内存管理，而非文档检索）。

## 先决条件

- Node.js版本 >= 18
- npm或pnpm

## 安装方法

```bash
npm install -g shieldcortex
```

**用于OpenClaw集成（安装cortex-memory插件）：**

```bash
shieldcortex openclaw install
```

**用于Claude Code / VS Code / Cursor MCP集成：**

```bash
shieldcortex install
```

## 快速入门

### 作为OpenClaw插件（自动启用）

在安装`shieldcortex openclaw`后，该插件会在下次重启时自动生效：
- 在内存压缩时自动保存重要会话数据；
- 在会话开始时自动加载相关的历史记忆内容；
- 支持通过关键词“remember this: ...”来保存特定记忆内容。

### 命令行接口（CLI）命令

```bash
# Check status
shieldcortex status

# Scan content for threats
shieldcortex scan "some text to check"

# Full security audit of your agent environment
shieldcortex audit

# Scan all installed skills/instruction files for hidden threats
shieldcortex scan-skills

# Scan a single skill file
shieldcortex scan-skill ./path/to/SKILL.md

# Build knowledge graph from existing memories
shieldcortex graph backfill

# Start the visual dashboard
shieldcortex --dashboard
```

### 作为编程库使用

```javascript
import {
  addMemory,
  getMemoryById,
  runDefencePipeline,
  scanSkill,
  extractFromMemory,
  consolidate,
  initDatabase
} from 'shieldcortex';

// Initialize
initDatabase('/path/to/memories.db');

// Add a memory (automatically passes through defence pipeline)
addMemory({
  title: 'API uses OAuth2',
  content: 'The payment API requires OAuth2 bearer tokens, not API keys',
  category: 'architecture',
  importance: 'high',
  project: 'my-project'
});

// Scan content before processing
const result = runDefencePipeline(untrustedContent, 'Email Import', {
  type: 'external',
  identifier: 'email-scanner'
});

if (result.allowed) {
  // Safe to process
}

// Extract knowledge graph entities
const { entities, triples } = extractFromMemory(
  'Database Migration',
  'We switched from MySQL to PostgreSQL for the auth service',
  'architecture'
);
// entities: [{name: 'MySQL', type: 'service'}, {name: 'PostgreSQL', type: 'service'}, ...]
// triples: [{subject: 'auth service', predicate: 'uses', object: 'PostgreSQL'}, ...]
```

## 内存系统特性

| 特性 | 说明 |
|---------|-------------|
| **持久化存储** | 基于SQLite的存储系统，数据在重启和压缩后仍可保留 |
| **语义搜索** | 通过内容含义而非关键词进行记忆查找 |
| **项目级管理** | 可为不同项目/工作区隔离内存数据 |
| **数据重要性分级** | 数据分为关键、高优先级、普通和低优先级，并支持自动遗忘机制 |
| **数据分类** | 包括系统架构、决策记录、偏好设置、上下文信息、学习成果、错误日志等 |
| **数据衰减与遗忘** | 旧数据或未被访问的数据会逐渐被清除（类似真实大脑的工作原理） |
| **数据整合** | 自动合并相似或重复的数据 |
| **矛盾检测** | 当新数据与现有数据冲突时发出警报 |
| **知识图谱生成** | 从内存中提取实体和关系信息 |
| **访问优先级** | 最近访问的数据在搜索中具有更高的显示优先级 |

## 安全特性

| 防护层 | 保护措施 |
|-------|-----------|
| **输入数据清洗** | 去除控制字符、空字节及危险格式的输入数据 |
| **模式检测** | 通过正则表达式识别常见的注入模式 |
| **异常检测** | 通过熵分析检测异常行为 |
| **凭证泄露防护** | 阻止API密钥、令牌和私钥的泄露（支持25种以上检测模式，覆盖11种常见来源） |
| **数据可靠性评估** | 根据数据来源评估其可靠性 |
| **审计追踪** | 详细记录所有内存操作的历史记录 |
| **威胁扫描** | 检测SKILL.md、.cursorrules、CLAUDE.md文件中的恶意代码注入行为 |

## ShieldCortex云服务（可选）

您可以将审计数据同步到团队仪表板，实现跨项目的监控与协作：

```bash
shieldcortex config set-api-key <your-key>
```

本地免费版本的使用不受限制。云服务提供团队仪表板、数据汇总和警报功能。

## 相关链接

- **npm仓库：** https://www.npmjs.com/package/shieldcortex
- **GitHub仓库：** https://github.com/Drakon-Systems-Ltd/ShieldCortex
- **官方网站：** https://shieldcortex.ai
- **文档说明：** https://github.com/Drakon-Systems-Ltd/ShieldCortex#readme

## 提供的API接口

该库提供了70个命名函数和类型，涵盖安全防护、内存管理、知识图谱生成、技能扫描和审计等功能。完整接口列表请参见[CHANGELOG](https://github.com/Drakon-Systems-Ltd/ShieldCortex/blob/main/CHANGELOG.md#2100---2026-02-13)。