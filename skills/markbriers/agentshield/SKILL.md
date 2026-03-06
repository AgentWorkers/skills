---
name: agentshield
description: "AI Agent Detection & Response：利用Sigma规则和基于大语言模型（LLM）的智能分类机制实现实时安全监控  
**概述：**  
本方案结合了AI技术、实时安全监控系统以及先进的规则引擎（Sigma Rules），旨在有效检测潜在的恶意行为或异常活动。通过分析系统日志、网络流量等数据，AI代理检测模块能够快速识别异常行为，并利用基于大语言模型的分类系统（LLM-powered triage）对事件进行智能分类和处理。这种机制能够显著提升安全响应的效率和准确性，帮助安全团队更快地应对各种安全威胁。  
**核心功能：**  
1. **AI Agent Detection（AI代理检测）：**  
   - 利用机器学习算法识别系统中可能存在的不寻常行为或恶意活动。  
   - 能够检测到传统的攻击模式以及新型的、难以预测的攻击手段。  
2. **Sigma Rules（Sigma规则）：**  
   - 一套高度可定制的安全规则集，用于定义哪些行为属于异常或恶意行为。  
   - 支持动态更新和扩展，以适应不断变化的安全威胁。  
3. **LLM-powered triage（基于大语言模型的智能分类）：**  
   - 基于大语言模型（如GPT-3）的智能分类系统，对检测到的事件进行自动分类。  
   - 根据事件的严重性和紧迫性，自动分配处理优先级。  
4. **实时响应：**  
   - 一旦检测到异常行为，系统会立即触发相应的安全响应机制。  
   - 安全团队可以快速接收警报，并根据分类结果采取相应的行动。  
**优势：**  
- **高效性：**  
  - 结合AI和LLM技术，实现快速、准确的威胁检测和响应。  
- **灵活性：**  
  - Sigma规则支持灵活配置，便于根据实际需求调整安全策略。  
- **可扩展性：**  
  - 随着新威胁的出现，可以轻松添加新的规则或调整现有规则。  
- **自动化：**  
  - 大部分处理流程自动化，减少人工干预的需求。  
**应用场景：**  
- 适用于各种安全监控系统，包括网络监控、应用程序安全、数据中心安全等。  
**技术架构：**  
- 包括数据收集、处理、分析、响应等关键环节。  
- 使用分布式架构，确保系统的稳定性和高可用性。  
**示例代码：**  
（由于SKILL.md文件通常包含具体的技术实现细节和代码示例，这里省略了具体的代码内容。）  
**参考文献：**  
（如相关技术文档、论文等。）  
**更新日志：**  
（记录规则的更新内容、系统版本的变更等。）"
homepage: "https://github.com/agentshield-ai/agentshield"
user-invocable: true
metadata: {"openclaw":{"requires":{"anyBins":["go","curl"]},"os":["darwin","linux"]}}
---
# AgentShield

**AI Agent Detection & Response (AADR)** — 实时安全监控功能，支持Sigma规则和基于大型语言模型（LLM）的事件分类处理。

## 什么是AgentShield？

AgentShield是一个用Go语言编写的安全监控引擎，能够实时监控AI代理工具的调用行为。它会根据Sigma安全规则对每个调用进行评估，并可选择将可疑事件转发给大型语言模型（LLM）进行进一步分析，以获得更准确的判断结果。该引擎以单一的二进制文件形式运行，无需依赖任何外部运行时环境。

## 架构

AgentShield由一个单一的Go二进制文件（`agentshield`）组成，包含以下组件：
- HTTP服务器（默认使用Chi路由器，地址为`127.0.0.1:8433`）
- Sigma规则引擎（基于`pkg/sigma/`中的`sigmalite`实现）
- SQLite数据库用于存储警报和反馈信息
- 可选的大型语言模型（LLM）事件分类服务（支持OpenAI或Anthropic）
- 支持基于bearer令牌的身份验证机制
- 每个IP地址的请求速率限制（默认为每分钟约100次请求，突发上限为10次）

系统服务配置方式如下：
- 在Linux系统中使用`systemd`服务：`agentshield-engine.service`
- 在macOS系统中使用`launchd`服务：`ai.agentshield.engine`

## 安装

### 快速安装

```bash
./install.sh
```

安装过程包括：
1. 识别操作系统（Linux或Darwin）和架构（amd64或arm64）
2. 从GitHub仓库下载二进制文件（如无法下载，则使用`go install`命令进行安装）
3. 创建`~/.agentshield/`目录用于存放配置文件、规则文件和数据库
4. 从`agentshield-ai/sigma-ai`仓库克隆Sigma规则文件
5. 生成一个64位的认证令牌
6. 编写`~/.agentshield/config.yaml`配置文件
7. 配置系统服务（Linux）或`launchd`代理（macOS）
8. 通过`openclaw config patch`命令更新OpenClaw插件的配置
9. 启动服务并检查服务是否正常运行

### 手动安装

```bash
# Build from source
go build ./cmd/agentshield/

# Create directory structure
mkdir -p ~/.agentshield/rules

# Clone rules
git clone --depth 1 https://github.com/agentshield-ai/sigma-ai.git ~/.agentshield/rules

# Generate auth token
openssl rand -hex 32

# Create config.yaml (see Configuration section)
# Start the engine
~/.agentshield/agentshield-engine serve --config ~/.agentshield/config.yaml
```

## 配置

配置文件位于`~/.agentshield/config.yaml`。

### 环境变量覆盖

以下环境变量可以覆盖默认配置：
| 变量            | 默认值        |
|-----------------|-------------|
| `AGENTSHIELD_PORT`     | `server.port`     |
| `AGENTSHIELD_ADDR`     | `server.addr`     |
| `AGENTSHIELD_AUTH_TOKEN` | `auth.token`     |
| `AGENTSHIELD_RULES_DIR`    | `rules.dir`     |
| `AGENTSHIELD_DB_PATH`    | `store.sqlite_path`   |
| `AGENTSHIELD_MODE`     | `evaluation_mode`   |
| `AGENTSHIELD_LOG_LEVEL`    | `log_level`     |
| `AGENTSHIELD_TRIAGE_API_KEY` | `triage.api_key`    |

### 认证

必须使用长度至少为32个字符的认证令牌。安装程序会自动生成一个64位的十六进制令牌。

```bash
# Generate manually
openssl rand -hex 32

# Or via Python
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## 评估模式

- **enforce**：阻止符合规则的代理工具调用。适用于生产环境。
- **audit**：仅记录警报信息，不阻止调用。默认设置为测试模式。
- **shadow**：进行静默监控，不向用户显示任何警报。

## 命令行接口（CLI）

```bash
# Start the server
agentshield serve --config ~/.agentshield/config.yaml [--daemon] [--verbose]

# Check server status (queries /api/v1/health)
agentshield status [--verbose]

# List recent alerts
agentshield alerts [-l LIMIT] [-s SEVERITY] [--since RFC3339] [-r RULE]

# List loaded rules
agentshield rules list

# Reload rules (sends SIGHUP to running server)
agentshield rules reload

# Analyze rule performance using feedback data
agentshield refine [rule-name] [--apply] [--threshold FP_RATE]

# Show version
agentshield version
```

### 服务管理

- **Linux（systemd服务）**：使用相应的系统管理服务命令进行配置和管理。
- **macOS（launchd）**：使用`launchd`命令进行配置和管理。

## API接口

所有API接口均位于`/api/v1/`路径下。请求时需要添加`Authorization: Bearer <token>`头部以进行身份验证。

| API接口        | 方法           | 功能描述                |
|-----------------|-----------------|----------------------|
| /api/v1/evaluate   | POST          | 根据规则评估代理工具调用并进行事件分类    |
| /api/v1/health     | GET          | 检查服务运行状态（无需认证）         |
| /api/v1/alerts     | GET          | 查询存储的警报信息（支持分页和过滤）     |
| /api/v1/feedback    | POST          | 提交警报反馈（例如：false_positive, true_positive, improvement） |
| /api/v1/feedback?rule=<name> | GET          | 查询特定规则的反馈信息及调用频率       |

## 服务限制

- 请求体大小上限：1 MB
- 单个字段的最大值：10 KB
- 每次请求允许的字段数量：100个
- 每个IP地址的请求速率限制：每分钟约100次，突发上限为10次
- 请求超时时间：30秒

## LLM事件分类

（可选功能）启用后，引擎会将可疑事件发送给大型语言模型（LLM）进行更详细的分析。支持的提供者包括OpenAI和Anthropic。

### Sigma规则

规则文件保存在`~/.agentshield/rules/`目录下。引擎会自动加载该目录下的所有`.yml`或`.yaml`格式的规则文件。

### 规则格式

遵循标准Sigma规则格式，专为代理工具监控场景进行了优化。

### 规则管理

- 支持热加载功能（`rules.hot_reload: true`）
- 可手动重新加载规则：`agentshield rules reload`（发送SIGHUP信号）
- 查看已加载的规则：`agentshield rules list`
- 规则仓库地址：`agentshield-ai/sigma-ai`

## 与OpenClaw的集成

AgentShield插件会以`agentshield`的名称注册到OpenClaw的插件系统中。安装程序会自动更新OpenClaw的配置文件。

### 插件钩子

AgentShield插件在OpenClaw中注册了以下钩子：
- `before_tool_call`（优先级-100）：同步评估代理工具调用
- `after_tool_call`：生成审计报告
- `session_start`, `session_end`, `before_agent_start`, `agent_end`：处理与代理会话相关的生命周期事件

有关插件使用的详细文档，请参阅[插件README](../README.md)。

## 故障排除

### 服务无法启动

- 确保使用有效的认证令牌（长度至少32个字符，可使用`openssl rand -hex 32`生成）
- 检查端口是否被占用（使用`netstat -an | grep 8433`命令）
- 确保规则文件存在且格式正确
- 调整`triage.timeout_sec`参数以增加事件分类的响应时间，或尝试将`health_check_mode`设置为`"connectivity`

### 直接测试引擎

提供了直接测试AgentShield引擎的方法。

## 文件位置

- 二进制文件：`~/.agentshield/agentshield-engine`
- 配置文件：`~/.agentshield/config.yaml`
- 规则文件：`~/.agentshield/rules/`
- 数据库文件：`~/.agentshield/agentshield.db`
- 系统服务配置文件：`~/.config/systemd/user/agentshield-engine.service`
- `launchd`代理配置文件：`~/Library/LaunchAgents/ai.agentshield.engine.plist`

## 卸载

卸载过程包括停止服务、删除相关文件和目录、恢复OpenClaw的插件配置，并清理系统路径中的引用。

## 许可证

AgentShield遵循Apache 2.0许可证。