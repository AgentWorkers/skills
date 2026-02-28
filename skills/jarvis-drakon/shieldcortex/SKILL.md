# ShieldCortex — 为AI代理提供持久化存储与安全保障

让您的AI代理在会话之间保持数据持久性，并保护其免受内存攻击的威胁。

## 产品描述

ShieldCortex是一个具备内置安全功能的完整内存管理系统。它为AI代理提供持久化、智能化的存储解决方案，支持语义搜索、知识图谱管理、基于时间衰减的遗忘机制以及矛盾检测功能。所有内存写入操作都会经过六层安全防护机制的审核，有效阻止提示注入、凭证泄露等攻击。此外，Iron Dome功能还提供了行为防护机制（如动作限制、安全配置文件以及详细的审计记录）。

**适用场景：**
- 当您希望代理在不同会话之间保留数据（如决策、偏好设置、系统架构、上下文信息）时；
- 当您需要基于语义对历史记忆进行搜索（而不仅仅是简单的关键词匹配）时；
- 当您需要自动整合、清理和优化内存内容时；
- 当您希望从记忆中提取实体和关系数据以构建知识图谱时；
- 当您需要保护内存免受提示注入或恶意篡改的攻击时；
- 当您需要检测内存写入操作中的凭证泄露风险（支持25种以上检测模式，11种第三方库）时；
- 当您希望审计内存中存储和检索的内容时；
- 当您希望扫描代理指令文件（如SKILL.md、.cursorrules、CLAUDE.md）以发现潜在威胁时；
- 当您希望利用Iron Dome的功能进行行为防护时；
- 当您希望使用Universal Memory Bridge来保护任何内存后端时。

**不适用场景：**
- 当您只需要简单的键值存储功能时（请使用配置文件）；
- 当您只需要临时性的会话上下文数据时（请使用代理内置的上下文管理机制）；
- 当您需要使用向量数据库来支持RAG（Retrieval-Augmented Grammar）流程时（ShieldCortex主要用于存储代理数据，而非文档检索）。

## 前提条件

- Node.js版本需达到18或更高；
- 需要npm或pnpm（或Python的pip）环境。

## 安装方法

```bash
npm install -g shieldcortex
```

Python SDK安装方法：

```bash
pip install shieldcortex
```

集成OpenClaw（安装cortex-memory插件）：

```bash
shieldcortex openclaw install
```

集成Claude Code、VS Code或Cursor MCP：

```bash
shieldcortex install
```

## 快速入门

### 作为OpenClaw插件（自动启用）

安装`shieldcortex openclaw`后，该插件会在下次重启时自动生效：
- 在会话开始时自动加载相关的历史记忆；
- 支持使用`"remember this: ..."`命令将重要信息保存到内存中；
- （可选）在会话结束时自动提取并整合重要记忆内容（支持智能去重）。

启用自动记忆功能：
```bash
npx shieldcortex config --openclaw-auto-memory
```

### 命令行接口（CLI）

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
| **持久化存储** | 基于SQLite的存储系统，可跨重启和数据压缩机制保持数据完整性 |
| **语义搜索** | 通过语义内容而非关键词进行记忆查找 |
| **项目级管理** | 可按项目或工作区隔离记忆数据 |
| **重要性分级** | 数据分为关键、高级、普通、低级三种级别，并支持自动遗忘机制 |
| **分类管理** | 提供多种分类选项（如系统架构、决策记录、偏好设置、上下文信息、学习成果、错误日志等） |
| **数据衰减与遗忘** | 旧数据或未被访问的数据会逐渐被删除，模拟真实大脑的记忆机制 |
| **数据整合** | 自动合并重复或相似的记忆内容 |
| **矛盾检测** | 当新记忆与现有记忆冲突时发出警报 |
| **知识图谱构建** | 从记忆中提取实体和关系信息 |
| **访问优先级** | 最近访问的记忆内容优先被检索 |
| **内容显性排序** | 重要记忆在搜索结果中优先显示 |

## 安全特性

| 安全层级 | 保护措施 |
|-------|-----------|
| **输入清洗** | 过滤掉控制字符、空字节及危险格式的数据 |
| **模式检测** | 使用正则表达式检测常见的攻击模式 |
| **语义分析** | 通过嵌入到攻击语料库中进行相似性判断 |
| **结构验证** | 检查数据的JSON格式是否正确 |
| **行为监控** | 长期监控异常行为以发现潜在安全问题 |
| **凭证保护** | 阻止API密钥、令牌和私钥等敏感信息的泄露（支持25种以上检测模式，11种第三方库） |
| **信任评分** | 根据数据来源评估内存写入操作的可靠性 |
| **审计记录** | 详细记录所有内存操作的审计日志 |
| **威胁扫描** | 检查SKILL.md、.cursorrules、CLAUDE.md文件中的潜在威胁 |

### Iron Dome

Iron Dome是 ShieldCortex 的行为安全层，用于控制代理的可执行操作：
- **安全配置文件**：提供`school`、`enterprise`、`personal`、`paranoid`四种安全级别，每种级别配备相应的动作限制和信任设置 |
- **动作限制**：对某些危险操作（如发送邮件、删除文件、调用API）设置审批流程 |
- **注入检测**：扫描文本以识别提示注入的尝试，并根据严重程度进行分类 |
- **完整审计记录**：所有操作都会被详细记录以供后续审查

### Universal Memory Bridge

通过Universal Memory Bridge，您可以保护任何使用 ShieldCortex 的内存后端：

```javascript
import { ShieldCortexGuardedMemoryBridge, MarkdownMemoryBackend } from 'shieldcortex';

const bridge = new ShieldCortexGuardedMemoryBridge({
  backend: new MarkdownMemoryBackend('~/.my-memories/'),
});
```

内置的后端支持包括 `MarkdownMemoryBackend` 和 `OpenClawMarkdownBackend`；您也可以自定义后端接口以实现其他存储需求。

## ShieldCortex Cloud（可选）

支持将审计数据同步到团队仪表板，实现跨项目的数据共享与监控：

```bash
shieldcortex config set-api-key <your-key>
```

免费本地版本的使用不受限制；云服务提供团队仪表板、审计数据汇总和警报功能。

## 链接

- **npm仓库：** https://www.npmjs.com/package/shieldcortex  
- **PyPI仓库：** https://pypi.org/project/shieldcortex  
- **GitHub仓库：** https://github.com/Drakon-Systems-Ltd/ShieldCortex  
- **官方网站：** https://shieldcortex.ai  
- **文档资料：** https://shieldcortex.ai/docs