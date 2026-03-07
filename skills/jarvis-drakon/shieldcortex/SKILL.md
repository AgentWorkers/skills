---
name: shieldcortex
description: 一种专为人工智能代理设计的持久性内存系统，具备安全防护功能。该系统能够跨会话保存代理的决策、偏好设置、系统架构以及相关上下文信息。它通过知识图谱来实现数据的存储与检索，同时具备数据衰减（老化）检测机制和矛盾检测功能。系统采用六层防御架构，并配备了Iron Dome行为保护机制来增强安全性。当用户需要执行以下操作时，该系统可发挥重要作用：“记住这些信息”、“了解当前掌握的情况”、“回溯上下文”、“扫描潜在威胁”、“执行安全审计”或“检查内存使用情况”；此外，在启动新会话时，该系统也能帮助用户快速获取之前的上下文数据。
license: MIT
metadata:
  author: Drakon Systems
  version: 2.17.0
  mcp-server: shieldcortex
  category: memory-and-security
  tags: [memory, security, knowledge-graph, mcp, iron-dome]
---
# ShieldCortex — 为AI代理提供持久化存储与安全保护

为你的代理程序提供能够在会话之间保持数据持久性的功能，并保护其免受内存污染攻击。

## 适用场景

- 当你需要在会话之间保留某些信息（如决策、偏好设置、系统架构、上下文等）时
- 在会话开始时需要回顾之前的相关内容
- 需要从记忆中提取知识图谱（包括实体及其之间的关系）
- 需要保护内存免受提示注入或污染攻击
- 需要检测内存写入操作中的凭证泄露行为
- 需要审计内存中存储和检索的内容
- 需要扫描指令文件（如SKILL.md、.cursorrules、CLAUDE.md）以发现潜在威胁

## 设置方法

全局安装npm包，然后配置MCP服务器：

```bash
npm install -g shieldcortex
shieldcortex install
```

Python SDK也可使用：

```bash
pip install shieldcortex
```

## 核心工作流程

### 会话开始

在每次会话开始时，检索之前的上下文信息：

1. 调用`start_session`以开始新会话并获取相关记忆数据
2. 或者使用包含当前任务描述的查询调用`get_context`

### 信息保存

当发生以下情况时，立即调用`remember`：

- **系统架构决策**（例如：“我们使用PostgreSQL作为数据库”）
- **错误修复**（记录根本原因和解决方案）
- **用户偏好设置**（例如：“始终使用TypeScript的严格模式”）
- **已完成的功能**（包括开发的内容及原因）
- **错误解决方法**（记录问题及其修复方式）
- **项目上下文**（如技术栈、关键模式、文件结构）

参数：
- `title`（必填）：简短摘要
- `content`（必填）：详细信息
- `category`：类别（如架构、模式、偏好设置、错误、上下文、学习内容、待办事项、备注）
- `importance`：重要性等级（低、普通、高、关键）
- `project`：指定项目范围（省略时自动检测）
- `tags`：用于分类的标签数组

### 信息检索

调用`recall`来搜索过去的记忆内容：

- `mode: "search"`：基于查询的语义搜索（默认模式）
- `mode: "recent"`：最近发生的记忆
- `mode: "important"`：重要性最高的记忆

支持按`category`、`tags`、`project`或`type`（短期、长期、情景化）进行过滤

### 信息删除

调用`forget`来删除过时或不正确的记忆：

- 可通过`id`删除特定记忆
- 可通过`query`根据内容删除记忆
- 删除前务必使用`dryRun: true`进行预览
- 批量删除时使用`confirm: true`确认操作

### 会话结束

调用`end_session`并附上摘要，以触发记忆数据的整合。这有助于将短期记忆转化为长期记忆，并对不再使用的记忆数据进行衰减处理。

## 知识图谱

ShieldCortex能够自动从记忆中提取实体及其之间的关系：

- `graph_query`：从某个实体开始遍历，返回最多N层关联的实体
- `graph_entities`：列出所有已知的实体，并按类型（人、工具、概念、文件、语言、服务、模式）进行过滤
- `graph_explain`：查找两个实体之间的连接路径

利用知识图谱来理解项目中各个概念、技术及决策之间的关联关系。

## 内存智能功能

- `consolidate`：合并重复或相似的记忆数据，并执行衰减处理。使用`dryRun: true`进行预览
- `detect_contradictions`：检测相互矛盾的记忆内容（例如：“使用Redis”与“不使用Redis”）
- `get_related`：查找与特定记忆ID关联的记忆
- `link_memories`：创建明确的关联关系（引用、扩展、矛盾关系等）
- `memory_stats`：查看总记忆数量、类别分布及衰减统计信息

## 安全与防护机制

所有内存写入操作都会经过六层安全防护流程：

1. **输入清洗**：去除控制字符和空字节
2. **模式检测**：使用正则表达式检测已知的内存注入模式
3. **语义分析**：将数据嵌入到攻击语料库中进行相似性比对
4. **结构验证**：检查JSON数据的格式完整性
5. **行为分析**：监测数据随时间的变化情况
6. **凭证泄露检测**：阻止API密钥、令牌和私钥的泄露（支持25种以上检测模式，来自11个供应商）

### Iron Dome（行为安全层）

Iron Dome控制代理程序能够执行的操作，而不仅仅是它们能够记住的内容：

- `iron_domeActivate`：根据配置文件（`school`、`enterprise`、`personal`、`paranoid`）激活该功能
- `iron_dome_status`：查看当前激活的配置文件、可信通道及审批规则
- `iron_dome_check`：在执行操作（如发送邮件、删除文件）前进行审核
- `iron_dome_scan`：扫描文本以检测潜在的提示注入行为

配置文件用于控制操作权限（哪些操作需要审批）、通道信任（哪些指令来源可被信任）以及审批规则。

## 安全工具

- `audit_query`：查询所有内存操作的审计日志
- `defence_stats`：查看安全防护系统的统计信息（拦截的请求、允许的请求、被隔离的请求）
- `quarantine_review`：审查和管理被隔离的记忆（列出、批准或拒绝）
- `scan_memories`：扫描现有记忆以检测污染迹象
- `scan_skill`：扫描指令文件（如SKILL.md、.cursorrules、CLAUDE.md）以发现隐藏的威胁

## 统一内存管理框架

ShieldCortex可作为任何内存后端的安全防护层。使用`ShieldCortexGuardedMemoryBridge`将任何内存系统与完整的防护流程集成：

```javascript
import { ShieldCortexGuardedMemoryBridge, MarkdownMemoryBackend } from 'shieldcortex';

const bridge = new ShieldCortexGuardedMemoryBridge({
  backend: new MarkdownMemoryBackend('~/.my-memories/'),
});

// All writes pass through the 6-layer defence pipeline
await bridge.write({ title: 'Decision', content: 'Use PostgreSQL' });
```

内置的后端包括：`MarkdownMemoryBackend`、`OpenClawMarkdownBackend`。你可以为自定义存储系统实现相应的后端接口。

## 项目范围管理

- `set_project`：切换当前项目范围
- `get_project`：显示当前项目的相关信息
- 使用`project: "*"`可访问全局或跨项目的记忆数据

## 最佳实践

- **及时保存信息**：在做出决策或修复错误后立即调用`remember`
- **使用分类标签**：明确记忆的类别（如架构、模式、偏好设置、错误、上下文等）
- **设置重要性等级**：将关键决策标记为`importance: "critical"`以防止数据被遗忘
- **会话开始时检索信息**：始终先调用`get_context`或`start_session`
- **正确结束会话**：通过`end_session`并附上摘要来触发记忆整合
- **定期检查矛盾信息**：定期运行`detect_contradictions`以发现冲突内容
- **按项目范围管理记忆**：记忆数据会自动关联到当前项目目录

## 常见问题解决方法

- **检索不到记忆**：
  - 尝试使用不同的查询语句调用`mode: "search"
  - 检查`set_project`设置，确保查询的是正确的项目范围
  - 使用`includeDecayed: true`来查找已被删除的记忆

- **内存被防火墙阻止**：
  - 安全防护系统检测到潜在威胁（如注入攻击或凭证泄露）
  - 查看`audit_query`以了解具体的阻止原因
  - 如果是误判，可以使用`quarantine_review`进行复查
- **避免在记忆内容中包含API密钥或令牌**

- **整合过程中删除记忆**：
  - 先使用`dryRun: true`进行预览
  - 将重要记忆标记为`importance: "critical`以防止数据被遗忘
- **定期访问记忆**：定期调用`recall`可以提升记忆的活跃度并防止数据衰减

## OpenClaw自动记忆功能

默认情况下，OpenClaw的自动记忆提取功能是关闭的。若需启用该功能，可进行如下配置：

```bash
npx shieldcortex config --openclaw-auto-memory
```

启用后，系统会自动删除重复的记忆内容：

- `openclawAutoMemory`：启用/禁用自动记忆提取功能（默认值：false）
- `openclawAutoMemoryDedupe`：是否删除重复的记忆（默认值：true）
- `openclawAutoMemoryNoveltyThreshold`：重复检测的相似性阈值（默认值：0.88）
- `openclawAutoMemoryMaxRecent`：检查的最近记忆数量（默认值：300）

## 链接资源

- npm：https://www.npmjs.com/package/shieldcortex
- PyPI：https://pypi.org/project/shieldcortex
- GitHub：https://github.com/Drakon-Systems-Ltd/ShieldCortex
- 官网：https://shieldcortex.ai