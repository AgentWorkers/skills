---
name: nima-core
description: "**Noosphere集成内存架构**——专为AI代理设计的完整认知系统：支持持久性存储、情感智能、梦境整合、群体思维、预知能力以及清晰的意识状态。该架构包含4种嵌入式数据提供者（Embedding Providers），采用LadybugDB图谱作为后端存储系统，并支持零配置安装（zero-config installation）。开发者可访问nima-core.ai了解更多详细信息。"
version: 3.1.1
metadata: {"openclaw":{"emoji":"🧠","source":"https://github.com/lilubot/nima-core","homepage":"https://nima-core.ai","requires":{"bins":["python3","node"],"env":[]},"optional_env":{"NIMA_DATA_DIR":"Override default ~/.nima data directory","NIMA_EMBEDDER":"voyage|openai|ollama|local (default: local — zero external calls)","VOYAGE_API_KEY":"Required when NIMA_EMBEDDER=voyage","OPENAI_API_KEY":"Required when NIMA_EMBEDDER=openai","NIMA_OLLAMA_MODEL":"Model name when NIMA_EMBEDDER=ollama","NIMA_VOICE_TRANSCRIBER":"whisper|local (for voice notes)","WHISPER_MODEL":"tiny|base|small|medium|large","ANTHROPIC_API_KEY":"For memory pruner LLM distillation (opt-in only)"},"permissions":{"reads":["~/.nima/"],"writes":["~/.nima/","~/.openclaw/extensions/nima-*/"],"network":["voyage.ai (only if NIMA_EMBEDDER=voyage)","openai.com (only if NIMA_EMBEDDER=openai)"]},"external_calls":"All external API calls are opt-in via explicit env vars. Default mode uses local embeddings with zero network calls."}}
---
# NIMA Core 3.0

**Noosphere集成记忆架构**——为AI代理提供了一套完整的认知功能：持久性记忆、情感智能、梦境整合、群体智慧以及预知能力。

**官方网站：** https://nima-core.ai · **GitHub仓库：** https://github.com/lilubot/nima-core

## 快速入门

您的机器人现在具备了持久性记忆功能，无需任何额外配置。

## v3.0的新特性

### 完整的认知功能栈

NIMA已从单一的记忆插件发展成为一个全面的认知架构：

| 模块 | 功能 | 版本 |
|--------|-------------|---------|
| **记忆捕捉** | 三层数据捕捉（输入/思考/输出），四阶段噪声过滤 | v2.0 |
| **语义检索** | 向量与文本混合搜索，生态评分，token预算限制 | v2.0 |
| **动态情感** | 根据Panksepp模型划分的七种情感状态（寻求、愤怒、恐惧、欲望、关怀、恐慌、玩耍） | v2.1 |
| **VADER分析器** | 基于上下文的情感分析——包括情感强度提升、否定表达、习语识别及程度修饰词 | v2.2 |
| **记忆修剪器** | 从旧对话中提取语义核心内容，并对内容进行30天的抑制处理 | v2.3 |
| **梦境整合** | 每晚对情景记忆进行整合，提取其中的洞察和模式 | v2.4 |
| **群体智慧** | 通过共享数据库实现多代理间的记忆共享（可选支持Redis发布/订阅机制） | v2.5 |
| **预知能力** | 通过分析时间模式来预加载记忆内容 | v2.5 |
| **清晰时刻** | 情感共鸣的记忆会自发浮现 | v2.5 |
| **达尔文式记忆** | 通过余弦相似度算法对相似记忆进行聚类，并通过LLM模型验证重复内容 | v3.0 |
| **安装工具** | 一键安装脚本（install.sh），包含所有必要的配置文件 | v3.0 |

### v3.0的主要亮点
- 所有认知模块整合到一个包中
- 提供安装工具（install.sh），实现零配置安装
- 所有OpenClaw插件都已打包好，可直接使用
- 更新了README文档，所有版本信息统一更新至v3.0.4

## 架构

## 隐私与权限设置

- ✅ 所有数据均存储在`~/.nima/`目录下
- ✅ 默认情况下，数据仅用于本地处理，不进行任何外部调用
- ✅ NIMA不拥有任何服务器，不进行任何数据追踪，也不会将数据发送到外部服务
- ⚠️ 可选网络功能：群体智慧（Redis发布/订阅）、预知能力（外部LLM接口）、LadybugDB迁移——详见“可选功能”部分
- 🔒 仅在使用相关API时才会触发嵌入功能（VOYAGE_API_KEY、OPENAI_API_KEY等）

### 带有网络访问功能的可选特性

| 特性 | 环境变量 | 需要的网络调用 | 默认设置 |
|---------|----------|------------------|---------|
| 云嵌入服务 | `NIMA_EMBEDDER=voyage` | voyage.ai | 关闭 |
| 云嵌入服务 | `NIMA_EMBEDDER=openai` | openai.com | 关闭 |
| 记忆修剪器 | `ANTHROPIC_API_KEY` | anthropic.com | 关闭 |
| Ollama嵌入服务 | `NIMA_EMBEDDER=ollama` | localhost:11434 | 关闭 |
| 群体智慧 | `HIVE_ENABLED=true` | Redis发布/订阅 | 关闭 |
| 预知能力 | 使用外部LLM | 需配置API端点 | 关闭 |

## 安全性

### 安装内容

| 组件 | 安装位置 | 功能 |
|-----------|----------|---------|
| Python核心 | `~/.nima/` | 负责处理记忆、情感及认知功能 |
| OpenClaw插件 | `~/.openclaw/extensions/nima-*/` | 负责数据捕捉、检索及情感处理 |
| SQLite数据库 | `~/.nima/memory/graph.sqlite` | 用于持久化存储 |
| 日志文件 | `~/.nima/logs/` | 存储调试日志（可选） |

### 认证信息管理

| 环境变量 | 是否必需 | 是否涉及网络调用 | 功能 |
|---------|-----------|----------------|---------|
| `NIMA_EMBEDDER=local` | 否 | ✌ | 默认设置——使用本地嵌入服务 |
| `VOYAGE_API_KEY` | 仅在使用Voyage服务时需要 | ✅ | 用于云嵌入服务 |
| `OPENAI_API_KEY` | 仅在使用OpenAI服务时需要 | ✅ | 用于云嵌入服务 |
| `ANTHROPIC_API_KEY` | 仅在使用记忆修剪器时需要 | ✅ | 用于处理嵌入数据 |
| `NIMA_OLLAMA_MODEL` | 仅在使用Ollama服务时需要 | ❌ | 用于本地GPU嵌入 |

**建议：** 默认情况下使用`NIMA_EMBEDDER=local`。仅在需要更高质量的嵌入服务时再启用云服务。

### 安全措施

- **输入过滤**：系统消息、心跳信号及重复数据在存储前会被过滤掉
- **防止SQL注入**：通过参数化查询防止SQL注入攻击
- **路径安全**：所有文件路径都会经过安全处理
- **临时文件清理**：自动清理临时文件
- **API超时设置**：网络请求有合理的超时限制（Voyage服务30秒，本地服务10秒）

### 最佳实践

1. **安装前检查**：在安装前请仔细阅读`install.sh`脚本及所有插件文件
2. **备份配置**：在添加插件前，请备份`~/.openclaw/openclaw.json`文件
3. **避免以root用户身份运行**：安装过程会写入用户主目录
4. **使用容器化环境**：如果不确定安全性，请先在虚拟机或容器环境中进行测试
5. **定期更换API密钥**：使用云嵌入服务时，请定期更换API密钥
6. **监控日志**：定期检查`~/.nima/logs/`目录以检测异常活动

### 数据存储位置

## 控制设置

## 配置选项

### 嵌入服务提供商

| 提供商 | 配置方式 | 数据维度 | 成本 |
|----------|-------|------|------|
| **本地**（默认） | `NIMA_EMBEDDER=local` | 384维度 | 免费 |
| **Voyage AI** | `NIMA_EMBEDDER=voyage` + `VOYAGE_API_KEY` | 1024维度 | 每百万token费用0.12美元 |
| **OpenAI** | `NIMA_EMBEDDER=openai` + `OPENAI_API_KEY` | 1536维度 | 每百万token费用0.13美元 |
| **Ollama** | `NIMA_EMBEDDER=ollama` + `NIMA_OLLAMA_MODEL` | 768维度 | 免费 |

### 数据库后端

| | SQLite（默认） | 推荐使用LadybugDB | |
|--|-----------------|------------------------|
| 文本搜索 | 31毫秒 | LadybugDB：9毫秒（快3.4倍） |
| 向量搜索 | 外部服务 | OpenAI的HNSW引擎（18毫秒） |
| 图谱查询 | 使用SQL JOIN | LadybugDB的Cypher引擎 |
| 数据库大小 | 约91MB | LadybugDB：约50MB（小44%） |

**升级建议：** 使用`pip install real-ladybug && python -c "from nima_core.storage import migrate; migrate()"`来更新数据库。

### 所有环境变量

## 插件配置

| 插件名称 | 触发条件 | 功能 |
|------|-------|------|
| `nima-memory` | 保存操作后 | 捕捉三层数据 → 过滤噪声 → 存储到图谱数据库 |
| `nima-recall-live` | 在调用LLM之前 | 搜索记忆 → 根据情感状态进行评分 → 作为上下文数据插入（使用3000个token） |
| `nima-affect` | 接收到消息时 | 使用VADER模型分析情感状态 → 调整行为模式 |

## 安装步骤

### 手动安装方法

### 高级功能

### 梦境整合
每晚从情景记忆中提取洞察和模式：

### 记忆修剪器
将旧对话内容提炼成语义核心内容，并过滤掉冗余信息：

### 群体智慧
支持多代理间的记忆共享：

### 预知能力
通过分析时间模式来预加载记忆内容：

### 清晰时刻
情感共鸣的记忆会自发浮现（具备安全机制：过滤创伤性内容，选择合适的时间点，每日使用次数有限制）：

### 情感系统
基于Panksepp模型的七种情感状态及人格特征：

## API接口

## 更新日志

完整的版本历史请参见[CHANGELOG.md](./CHANGELOG.md)。

### 最新版本更新

- **v3.0.4**（2026年2月23日）：引入达尔文式记忆引擎、新的命令行接口（CLI）、修复了多个漏洞
- **v2.5.0**（2026年2月21日）：新增群体智慧和预知功能
- **v2.4.0**（2026年2月20日）：改进梦境整合功能
- **v2.3.0**（2026年2月19日）：优化记忆修剪器、添加连接池支持及Ollama模型兼容性
- **v2.2.0**（2026年2月19日）：改进VADER情感分析器、增强噪声过滤效果、引入生态评分机制
- **v2.0.0**（2026年2月13日）：更新LadybugDB后端、加强安全性并进行了348项测试

## 许可证

NIMA采用MIT许可证——适用于所有AI代理，无论是商业用途还是个人项目。