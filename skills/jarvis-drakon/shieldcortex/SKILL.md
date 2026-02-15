# ShieldCortex — 为AI代理提供持久化存储与安全保护

让您的AI代理拥有在会话之间保持数据的能力，并保护其免受内存攻击的威胁。

## 产品描述

ShieldCortex是一个具备内置安全功能的完整内存管理系统。它为AI代理提供持久化、智能化的存储解决方案，支持语义搜索、知识图谱、基于时间衰减的遗忘机制以及矛盾检测功能。所有内存写入操作都会经过六层安全防护流程，有效阻止提示注入、凭证泄露和恶意攻击。

**适用场景：**
- 当您希望代理在会话之间保留数据（如决策、偏好设置、系统架构、上下文信息）时；
- 当您需要跨历史数据执行语义搜索（而不仅仅是关键词匹配）时；
- 当您需要自动整合、清理和优化内存数据时；
- 当您希望从内存中提取实体和关系结构（即知识图谱）时；
- 当您需要保护内存免受提示注入或恶意攻击时；
- 当您需要审计内存中存储和检索的内容时；
- 当您希望扫描代理指令文件（如SKILL.md、.cursorrules、CLAUDE.md）中的隐藏威胁时。

**不适用场景：**
- 当您仅需要简单的键值存储功能时（请使用配置文件）；
- 当您只需要临时性的会话上下文数据时（请使用代理内置的上下文管理机制）；
- 当您需要用于RAG（Retrieval Against Attack）流程的向量数据库时（ShieldCortex主要用于代理内存管理，而非文档检索）。

## 前提条件

- Node.js版本需达到18或更高；
- 必须安装npm或pnpm。

## 安装方法

```bash
npm install -g shieldcortex
```

**用于OpenClaw集成（安装cortex-memory插件）：**

```bash
npx shieldcortex openclaw install
```

**用于Claude Code / VS Code / Cursor MCP集成：**

```bash
npx shieldcortex install
```

## 快速入门

### 作为OpenClaw插件（自动集成）

执行`npx shieldcortex openclaw install`后，该插件将在下次重启时自动生效：
- 在内存压缩时自动保存重要会话数据；
- 在会话开始时自动加载相关的历史数据；
- 支持使用“remember this: ...”关键字触发数据的保存。

### 命令行接口（CLI）

```bash
# Check status
npx shieldcortex status

# Scan content for threats
npx shieldcortex scan "some text to check"

# Full security audit of your agent environment
npx shieldcortex audit

# Scan all installed skills/instruction files for hidden threats
npx shieldcortex scan-skills

# Scan a single skill file
npx shieldcortex scan-skill ./path/to/SKILL.md

# Build knowledge graph from existing memories
npx shieldcortex graph backfill

# Start the visual dashboard
npx shieldcortex --dashboard
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
| **持久化存储** | 基于SQLite的存储机制，数据在重启或压缩后仍可保留 |
| **语义搜索** | 通过含义而非关键词来查找数据 |
| **项目级管理** | 可为不同项目/工作区隔离内存数据 |
| **数据重要性分级** | 数据分为关键、高重要、普通、低重要三个级别，并支持自动遗忘 |
| **数据分类** | 包括系统架构、决策记录、偏好设置、上下文信息、学习结果、错误日志等 |
| **数据衰减与遗忘** | 旧数据或未被访问的数据会逐渐被清除（类似真实大脑的工作机制） |
| **数据整合** | 自动合并相似或重复的数据 |
| **矛盾检测** | 新数据与现有数据冲突时会被标记出来 |
| **知识图谱** | 从内存中提取实体和它们之间的关系 |
| **数据访问优先级** | 最近访问的数据在搜索中具有更高的优先级 |

## 安全特性

| 安全防护层 | 保护措施 |
|-------|-----------|
| **输入数据清洗** | 去除控制字符、空字节及危险格式 |
| **模式检测** | 通过正则表达式识别常见的注入模式 |
| **异常检测** | 通过熵分析检测异常行为 |
| **凭证泄露防护** | 阻止API密钥、令牌、私钥等敏感信息的泄露（支持25种以上检测模式，来自11个来源） |
| **数据可靠性评估** | 根据数据来源评估其可靠性 |
| **审计日志** | 详细记录所有内存操作 |
| **威胁扫描** | 检测SKILL.md、.cursorrules、CLAUDE.md文件中的恶意代码 |

## ShieldCortex云服务（可选）

您可以将审计数据同步到团队仪表板，实现跨项目的监控与协作：

```bash
npx shieldcortex config set-api-key <your-key>
```

本地免费版本的使用不受限制；云服务提供团队仪表板、数据汇总和警报功能。

## 链接

- **npm仓库：** https://www.npmjs.com/package/shieldcortex  
- **GitHub仓库：** https://github.com/Drakon-Systems-Ltd/ShieldCortex  
- **官方网站：** https://shieldcortex.ai  
- **文档：** https://github.com/Drakon-Systems-Ltd/ShieldCortex#readme  

## 提供的API接口

该库提供了70个命名函数和类型，涵盖安全防护、内存管理、知识图谱处理、技能扫描和审计等功能。完整接口列表请参见[CHANGELOG](https://github.com/Drakon-Systems-Ltd/ShieldCortex/blob/main/CHANGELOG.md#2100---2026-02-13)。