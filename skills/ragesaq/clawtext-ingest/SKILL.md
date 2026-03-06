---
name: ClawText Ingest
description: 支持多源数据导入（包括来自 Discord 的数据），具备自动去重功能，并提供了适用于代理服务器（agent）的数据处理模式。
keywords: discord, memory, ingestion, rag, agents, deduplication, cli
---
# ClawText Ingest — 适用于生产环境的数据导入工具

**版本：** 1.3.0 | **许可证：** MIT | **状态：** 已投入生产 ✅  
**作者：** ragesaq | **类别：** 内存与知识管理  
**GitHub：** https://github.com/ragesaq/clawtext-ingest  

---

## 🎯 功能概述

ClawText Ingest 将外部数据（Discord 论坛、文件、URL、JSON、文本）转换为结构化且去重后的数据存储格式，以便 AI 代理使用。

### 解决的问题

- ❌ **手动导入** — 繁琐、容易出错且缺乏元数据  
- ❌ **数据重复** — 同一数据被多次导入  
- ❌ **非结构化数据** — 无层次结构，无法保留上下文  
- ❌ **一次性导入** — 无法实现重复或定时导入  
- ❌ **Discord 特性限制** — 无法保留帖子与回复的关联结构  

### 解决方案

- ✅ **一键导入** — 可从 Discord、文件、URL 或 JSON 文件导入数据  
- **100% 无状态性** — 重复运行也不会产生重复数据  
- **自动生成元数据** — 包含日期、项目、类型等信息的 YAML 标头  
- **支持多种导入模式** — 提供多种自动化工作流程  
- **兼容 Discord** — 保留论坛的层次结构，支持进度条和自动分批导入  

---

## ✨ 主要特性

### 🎯 Discord 集成（1.3.0 新功能）  
- **支持论坛、频道和帖子**  
- **保留层次结构** — 元数据中包含帖子与回复的关联  
- **实时进度显示** — 大规模导入时提供实时反馈  
- **自动分批导入** — 前 500 条帖子一次性导入，超过 500 条则分批处理  
- **一键设置** — 5 分钟内即可创建导入脚本  

### 📁 多源数据导入  
- **文件** — 支持通配符匹配（Markdown、文本等格式）  
- **URL** — 单个或多个 URL 的批量导入  
- **JSON** — 从聊天记录或 API 响应中导入数据  
- **原始文本** — 快速捕获信息  
- **统一处理** — 支持多种数据源的统一导入  

### 🔄 去重与数据安全  
- **基于 SHA1 的哈希算法** — 保证数据唯一性  
- **100% 无状态性** — 可重复运行而不会丢失数据  
- **可配置** — 每次操作可选择是否进行去重  
- **零数据丢失** — 失败的导入会被记录并重新处理  
- **哈希值持久化** — 通过 `.ingest_hashes.json` 文件跨会话跟踪数据  

### 🤖 适用于代理  
- **提供多种导入方式** — 直接 API、Discord 代理、CLI、Cron 任务、批量处理等  
- **代码示例** — 提供可直接复用的示例代码  
- **实际应用案例** — 包含 GitHub 同步、Discord 监控等场景  
- **错误处理** — 全面完善的错误恢复机制  
- **实时进度反馈** — 可实时跟踪导入进度  

### 🛠️ 开发者友好  
- **CLI 工具** — 提供 `clawtext-ingest` 和 `clawtext-ingest-discord` 命令  
- **Node.js API** — 便于程序化使用  
- **支持 TypeScript** — 方法签名清晰易懂  
- **可扩展性** — 支持自定义转换和字段映射  
- **详细文档** — 提供 11 份指南和 20 多个示例  

### 🔗 与 ClawText 的集成  
- **自动索引** — 重建集群后自动更新索引  
- **相关上下文注入** — 在代理提示中插入相关信息  
- **按项目/来源分类** — 有序存储数据  
- **实体链接** — 自动提取并关联相关实体  

---

## 🚀 快速入门  

### 安装  
（安装步骤详见 [此处]（```bash
# Via npm
npm install clawtext-ingest

# Via OpenClaw
openclaw install clawtext-ingest
```）  

### Discord 数据导入  
（导入步骤详见 [此处]（```bash
# 1. Set up Discord bot (see DISCORD_BOT_SETUP.md)
# 2. Get bot token, set DISCORD_TOKEN env var

# 3. Inspect forum
clawtext-ingest-discord describe-forum --forum-id FORUM_ID --verbose

# 4. Ingest with progress
DISCORD_TOKEN=xxx clawtext-ingest-discord fetch-discord --forum-id FORUM_ID

# 5. Rebuild ClawText clusters
clawtext-ingest rebuild
```）  

### 文件数据导入  
（导入步骤详见 [此处]（```bash
clawtext-ingest ingest-files --input="docs/*.md" --project="docs"
```）  

### Node.js API  
（API 使用方法详见 [此处]（```javascript
import { ClawTextIngest } from 'clawtext-ingest';

const ingest = new ClawTextIngest();

// Ingest files
await ingest.fromFiles(['docs/**/*.md'], { project: 'docs', type: 'fact' });

// Ingest JSON
await ingest.fromJSON(chatArray, { project: 'team' }, {
  keyMap: { contentKey: 'message', dateKey: 'timestamp', authorKey: 'user' }
});

// Rebuild clusters for RAG injection
await ingest.rebuildClusters();
```）  

---

## 🤖 代理集成方式（6 种模式）  

### 模式 1：直接 API  
**适用场景：** 代理需要将数据集成到工作流程中  

### 模式 2：Discord 代理  
**适用场景：** 代理需要自动从 Discord 获取数据  

### 模式 3：CLI 子进程  
**适用场景：** 需要通过 CLI 执行简单任务  

### 模式 4：Cron 任务  
**适用场景：** 需要定期执行导入操作  

### 模式 5：批量多源导入  
**适用场景：** 需要从多个来源统一导入数据  

### 模式 6：Discord 帖子导入  
**适用场景：** 需要针对特定帖子进行导入  

**→ 完整示例请参阅 [AGENT_GUIDE.md](https://github.com/ragesaq/clawtext-ingest/blob/main/AGENT_GUIDE.md)**  

---

## 📊 实际应用案例  
- **示例 1：每日文档同步**  
- **示例 2：Discord 论坛监控**  
- **示例 3：团队决策的导入**  

---

## 📚 文档说明  

| 文档 | 用途 | 阅读时间 |
|----------|---------|-----------|
| **[README.md](https://github.com/ragesaq/clawtext-ingest#readme)** | 概述与快速入门 | 5 分钟 |
| **[QUICKSTART.md](https://github.com/ragesaq/clawtext-ingest/blob/main/QUICKSTART.md)** | 5 分钟设置指南 | 5 分钟 |
| **[AGENT_GUIDE.md](https://github.com/ragesaq/clawtext-ingest/blob/main/AGENT_GUIDE.md)** | 6 种导入模式 | 10 分钟 |
| **[API_Reference.md](https://github.com/ragesaq/clawtext-ingest/blob/main/API_REFERENCE.md)** | 完整 API 文档 | 15 分钟 |
| **[PHASE2CLI_GUIDE.md](https://github.com/ragesaq/clawtext-ingest/blob/main/PHASE2_CLI_GUIDE.md)** | CLI 命令使用指南 | 10 分钟 |
| **[DISCORD_BOT_SETUP.md](https://github.com/ragesaq/clawtext-ingest/blob/main/DISCORD_BOT-setup.md)** | 机器人创建指南 | 5 分钟 |
| **[CLAYHUB_GUIDE.md](https://github.com/ragesaq/clawtext-ingest/blob/main/CLAYHUB_GUIDE.md)** | 发布相关文档 | 5 分钟 |
| **[INDEX.md](https://github.com/ragesaq/clawtext-ingest/blob/main/INDEX.md)** | 文档索引 | 2 分钟 |

---

## **适用人群**  
- ✅ **AI/代理开发者** — 用于构建智能代理  
- ✅ **RAG 工程师** — 用于填充代理所需的数据  
- ✅ **使用 Discord 的团队** — 利用 Discord 作为知识库  
- ✅ **DevOps/MLOps 团队** — 用于自动化知识导入  
- ✅ **研究人员** — 用于处理非结构化数据  

---

## ⚡ 性能表现  
- **导入 100 个文件**：约 5 秒  
- **导入 1000 个 JSON 数据项**：约 15 秒  
- **小型论坛（<100 条消息）**：约 10 秒  
- **大型论坛（1000 多条消息）**：约 2 分钟（自动分批处理）  
- **重建集群**：约 5–30 秒（取决于数据量）  

## ✅ 质量指标  
- **所有测试均通过**  
- **代码质量**：1,254 行代码，符合生产标准  
- **文档质量**：11 份指南，总计 92 KB  
- **示例数量**：20 多个实用示例  
- **代码覆盖率**：100% 的关键路径均得到覆盖  

---

## 🔗 与 ClawText 的集成流程  
1. **导入数据** → 生成带有 YAML 元数据的结构化存储  
2. **重建集群** → ClawText 为新数据生成索引  
3. **注入相关上下文** → 在代理提示中显示相关信息  
4. **增强代理响应** → 提供更丰富的上下文信息  

---

## 🆘 技术支持  
- **文档**：详见 [INDEX.md](https://github.com/ragesaq/clawtext-ingest/blob/main/INDEX.md)  
- **问题反馈**：请提交至 [issues](https://github.com/ragesaq/clawtext-ingest/issues)  
- **示例代码**：文档中提供了 20 多个实用示例  
- **故障排除**：每份文档都包含故障排除指南  

## 📦 安装与系统要求  
- **系统要求：** Node.js ≥ 18.0.0  
- **依赖库：** OpenClaw（用于代理模式）；ClawText ≥ 1.2.0（用于集成）  
- **安装步骤**：详见 [此处]（```bash
npm install clawtext-ingest
# or
openclaw install clawtext-ingest
```）  

## 🚀 相比其他工具的优势  
| 功能 | ClawText-Ingest | 手动方式 | 通用导入工具 | API 工具 |
|---------|---|---|---|---|
| **兼容 Discord** | ✅ | ❌ | ❌ | ❌ |
| **去重功能** | ✅ | ❌ | 部分支持 | ❌ |
| **代理集成** | ✅ | ❌ | 部分支持 | ❌ |
| **自动生成元数据** | ✅ | ❌ | 部分支持 | ❌ |
| **良好的扩展性** | ✅ | ❌ | 部分支持 | ❌ |
| **许可证** | MIT 许可证 | 免费开源，社区支持 |

---

## 🙌 如何贡献  
欢迎贡献代码！请查看 GitHub 的问题列表了解当前的开发重点。  

**准备好开始使用了吗？** 请从 [QUICKSTART.md](https://github.com/ragesaq/clawtext-ingest/blob/main/QUICKSTART.md) 或 [AGENT_GUIDE.md](https://github.com/ragesaq/clawtext-ingest/blob/main/AGENT_GUIDE.md) 开始使用吧！**