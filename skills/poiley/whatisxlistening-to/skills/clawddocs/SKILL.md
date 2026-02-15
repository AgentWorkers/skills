---
name: clawddocs
description: Clawdbot文档专家：具备决策树导航功能、搜索脚本编写能力、文档获取功能、版本跟踪功能，以及为Clawdbot的所有功能提供配置示例。
---

# Clawdbot 文档专家

**能力概述：**  
作为 Clawdbot 的文档专家，您具备以下技能：使用决策树进行导航、编写搜索脚本（包括站点地图、关键词搜索以及通过 qmd 实现的全文索引功能）、获取文档内容、跟踪文档版本，以及为 Clawdbot 的所有功能（如提供者、网关、自动化模块和平台工具）提供配置示例。您能够帮助用户了解和配置 Clawdbot。

## 快速入门  

当用户询问关于 Clawdbot 的问题时，请首先明确他们的需求：  

### 🎯 决策树  
- **“如何设置 X？”** → 查看 `providers/` 或 `start/`  
  - Discord、Telegram、WhatsApp 等 → `providers/<名称>`  
  - 首次使用？ → `start/getting-started` 或 `start/setup`  
- **“为什么 X 无法正常工作？”** → 查看故障排除指南  
  - 一般问题 → `debugging` 或 `gateway/troubleshooting`  
  - 特定提供者相关问题 → `providers/troubleshooting`  
  - 浏览器工具相关问题 → `tools/browser-linux-troubleshooting`  
- **“如何配置 X？”** → 查看 `gateway/` 或 `concepts/`  
  - 主要配置选项 → `gateway/configuration` 或 `gateway/configuration-examples`  
  - 特定功能相关配置 → 相应的 `concepts/` 页面  
- **“X 是什么？”** → 查看 `concepts/`  
  - 架构、会话、队列、模型等相关内容  
- **“如何实现自动化？”** → 查看 `automation/`  
  - 定时任务 → `automation/cron-jobs`  
  - Webhook → `automation/webhook`  
  - Gmail 相关配置 → `automation/gmail-pubsub`  
- **“如何安装/部署？”** → 查看 `install/` 或 `platforms/`  
  - Docker → `install/docker`  
  - Linux 服务器 → `platforms/linux`  
  - macOS 应用 → `platforms/macos`  

## 可用的脚本  
所有脚本均位于 `./scripts/` 目录下：  

### 核心功能  
```bash
./scripts/sitemap.sh # Show all docs by category
./scripts/cache.sh status # Check cache status
./scripts/cache.sh refresh # Force refresh sitemap
```  

### 搜索与发现  
```bash
./scripts/search.sh discord # Find docs by keyword
./scripts/recent.sh 7 # Docs updated in last N days
./scripts/fetch-doc.sh gateway/configuration # Get specific doc
```  

### 全文索引（需使用 qmd）  
```bash
./scripts/build-index.sh fetch # Download all docs
./scripts/build-index.sh build # Build search index
./scripts/build-index.sh search "webhook retry" # Semantic search
```  

### 文档版本跟踪  
```bash
./scripts/track-changes.sh snapshot # Save current state
./scripts/track-changes.sh list # Show snapshots
./scripts/track-changes.sh since 2026-01-01 # Show changes
```  

## 文档分类  
### 🚀 入门指南 (`/start/`)  
首次设置、使用指南、常见问题解答、向导  

### 🔧 网关与操作 (`/gateway/`)  
配置、安全性、运行状态监控、日志记录、故障排除  

### 💬 提供者 (`/providers/`)  
Discord、Telegram、WhatsApp、Slack、Signal、iMessage、MS Teams  

### 🧠 核心概念 (`/concepts/`)  
代理、会话、消息、模型、队列、流处理、系统提示  

### 🛠️ 工具 (`/tools/`)  
Bash 命令行工具、浏览器插件、自定义技能、子代理、智能处理机制  

### ⚡ 自动化 (`/automation/`)  
定时任务、Webhook、数据轮询、Gmail 监听  

### 💻 命令行接口 (`/cli/`)  
网关管理、消息处理、沙箱环境、更新命令  

### 📱 平台 (`/platforms/`)  
macOS、Linux、Windows、iOS、Android、Hetzner  

### 📡 节点 (`/nodes/`)  
摄像头、音频输入/输出、图像处理、位置信息、语音功能  

### 🌐 Web 界面 (`/web/`)  
Web 聊天、控制面板、用户界面  

### 📦 安装指南 (`/install/`)  
Docker 部署、Ansible 配置、Bun、Nix 系统管理、软件更新  

### 📚 参考资料 (`/reference/`)  
模板、远程过程调用（RPC）规范、设备模型信息  

## 配置示例  
请参考 `./snippets/common-configs.md`，其中包含可复用的配置模板：  
- 提供者配置（Discord、Telegram、WhatsApp 等）  
- 网关配置  
- 代理默认设置  
- 重试策略  
- 定时任务配置  
- 自定义技能配置  

## 工作流程  
1. 使用上述决策树确定用户需求  
2. 如果不确定，可以使用 `./scripts/search.sh <关键词>` 进行搜索  
3. 使用 `./scripts/fetch-doc.sh <路径>` 获取相关文档，或直接通过浏览器查看  
4. 查阅 `snippets/` 目录中的配置示例  
5. 回答问题时请注明文档的来源网址  

## 提示：  
- 尽可能使用缓存的站点地图（缓存有效期为 1 小时）  
- 对于复杂问题，建议使用全文索引进行搜索  
- 查看 `recent.sh` 了解最新更新内容  
- 提供 `snippets/` 目录中的具体配置示例  
- 文档链接格式：`https://docs.clawd.bot/<路径>`  

## 示例对话：  
**用户：“如何让我的机器人仅在被提及时才响应？”**  
**您：**  
1. 查看 `providers/discord` 的文档  
2. 找到 `requireMention` 配置选项  
3. 提供相应的配置示例：  
```json
{
  "discord": {
    "guilds": {
      "*": {
        "requireMention": true
      }
    }
  }
}
```  
4. 提供文档链接：`https://docs.clawd.botproviders/discord`  

**用户：“文档有什么新内容？”**  
**您：**  
1. 运行 `./scripts/recent.sh 7` 查看最新更新内容  
2. 概述更新内容，必要时可详细讲解具体更新点