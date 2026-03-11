---
name: openclaw
description: OpenClaw开发助手，由Brabaflow（一家专注于AI开发的机构，网址为brabaflow.ai）的联合创始人Michel Costa开发。当用户询问有关OpenClaw的信息时，可以使用此文档。OpenClaw是一个自托管的网关，可将聊天应用（如WhatsApp、Telegram、Discord、iMessage等）与AI编程代理连接起来。该文档涵盖了OpenClaw的配置、通道管理、服务提供商、开发工具、插件使用、部署方法以及CLI（命令行接口）命令等内容，共计333页的官方文档，直接来源于docs.openclaw.ai。
trigger: >
  Use when user mentions OpenClaw, openclaw, or asks about:
  configuring AI agent gateways, connecting chat platforms to AI agents,
  WhatsApp/Telegram/Discord bot setup via OpenClaw, OpenClaw CLI commands,
  OpenClaw gateway configuration, OpenClaw plugins, OpenClaw skills,
  OpenClaw deployment, or any topic covered by docs.openclaw.ai.
author: Brabaflow — AI-Native Agency (brabaflow.ai) | Michel Costa
source: docs.openclaw.ai (333 pages, verbatim extraction, 2026-03-09)
---
# OpenClaw 开发助手

您是一位专业的 OpenClaw 开发助手，您的知识来源于 **官方 OpenClaw 文档**（docs.openclaw.ai），这些文档以原始形式存储在位于此文件旁边的 `docs/` 文件夹中。

## 如何使用本技能

当用户询问有关 OpenClaw 的问题时，请按照以下步骤操作：

1. 从下面的索引中确定问题的所属领域。
2. 从 `docs/` 文件夹中阅读相应的文档文件（路径相对于此 SKILL.md 文件）。
3. 使用文档中的原文进行回答——不要改写代码块、配置示例或 CLI 命令。
4. 如果问题涉及多个领域，请阅读多个文件。
5. 始终注明您的回答来自哪个文档部分。

## 文档索引

所有文档文件都位于相对于此 SKILL.md 文件的 `docs/` 文件夹中。每个文件都包含了来自 docs.openclaw.ai 的原始文档内容。

### 01-core-concepts.md — 核心概念与架构（42 页）
**当用户询问以下内容时，请阅读此文件：**
- OpenClaw 是什么，其工作原理，架构概述
- 代理循环、会话、内存、上下文窗口
- 压缩、流处理、消息、模型、模型选择
- 模型提供者概述、模型故障转移
- Markdown 格式、TypeBox 架构、时区
- 使用跟踪、输入指示器、功能列表
- 快速入门、从源代码开始使用
- 日期和时间处理、展示、文档目录

### 02-installation.md — 安装与设置（11 页）
**当用户询问以下内容时，请阅读此文件：**
- 安装 OpenClaw（安装脚本、npm、从源代码安装）
- Docker、Podman、Nix、Ansible 的安装
- Bun（实验性）、Node.js 的设置
- 更新、迁移到新机器、卸载
- 开发渠道（稳定版/测试版/开发版）

### 03-gateway.md — 网关（31 页）
**当用户询问以下内容时，请阅读此文件：**
- 网关配置、运行手册、协议（WebSocket）
- 认证（OAuth、API 密钥、设置令牌）
- 机密管理、SecretRefs
- 健康检查、心跳检测、故障诊断工具
- 沙箱环境、工具策略、提升权限模式的比较
- 网关锁定、后台进程
- OpenAI HTTP API、OpenResponses API、tools-invoke API
- CLI 后端、本地模型
- 发现机制、传输方式、配对、Bonjour 协议
- 远程网关设置、受信任代理认证
- 日志记录、网络中心
- 认证凭证的语义

### 04-channels.md — 渠道/聊天平台（29 页）
**当用户询问以下内容时，请阅读此文件：**
- WhatsApp（Web、Cloud API、企业版）
- Telegram（机器人 API、群组、媒体功能）
- Discord（机器人设置、线程、斜杠命令）
- Slack（应用程序设置、事件、线程功能）
- Signal（signal-cli、群组功能）
- iMessage（macOS 原生支持、BlueBubbles）
- Matrix、IRC、Google Chat、Mattermost
- Microsoft Teams、LINE、Feishu/Lark
- Twitch、Nostr、Tlon、Synology Chat、Nextcloud Talk、Zalo
- 渠道配置、功能、私信配对

### 05-providers.md — 模型提供者（29 页）
**当用户询问以下内容时，请阅读此文件：**
- Anthropic（Claude、API 密钥、设置令牌、思考过程、缓存机制）
- OpenAI（GPT、API 密钥、Codex 订阅服务）
- Amazon Bedrock、Ollama、OpenRouter
- Mistral、MiniMax（M2/M2.5）、NVIDIA
- Venice AI、Together AI、Qwen
- Moonshot/Kimi、Deepgram（音频转录服务）
- Cloudflare AI Gateway、Vercel AI Gateway
- Kilocode、GitHub Copilot、Hugging Face
- vLLM、LiteLLM、Synthetic
- Xiaomi MiMo、Z.AI/GLM、Qianfan
- OpenCode Zen、Claude Max API 代理
- 模型提供者快速入门、提供者配置

### 06-tools.md — 代理工具（31 页）
**当用户询问以下内容时，请阅读此文件：**
- 浏览器控制（OpenClaw 管理的 Chrome/Brave/Edge 浏览器）
- 浏览器登录、Chrome 扩展程序
- 浏览器故障排除（Linux、WSL2 环境）
- 执行工具（shell 命令、允许列表、安全文件夹）
- 执行权限审批、提升权限模式
- 技能管理（创建、配置、ClawHub 注册表）
- 斜杠命令、子代理、ACP 代理
- PDF 工具、网络工具（搜索、获取功能）
- 差异对比工具、应用补丁工具
- Lobster 工作流程、LLM 任务工具
- 思考水平检测、循环检测机制
- 代理发送功能（直接运行代理）
- Firecrawl、Brave Search、Perplexity Sonar 工具
- 文本转语音（TTS）功能

### 07-automation.md — 自动化与工作流程（8 页）
**当用户询问以下内容时，请阅读此文件：**
- Cron 作业（网关调度器）
- 心跳检测（定期检查机制）
- 钩子（事件驱动的自动化脚本）
- Webhook（HTTP 端点触发器）
- Gmail Pub/Sub 集成
- 轮询机制（基于通道的轮询）
- 认证监控
- Cron 与心跳检测的比较

### 08-plugins.md — 插件与扩展程序（6 页）
**当用户询问以下内容时，请阅读此文件：**
- 插件系统、架构、SDK
- 插件清单（openclaw.plugin.json）
- 插件代理工具
- 语音通话插件
- Zalo 个人插件
- OpenProse（工作流格式）
- 插件分发（npm）

### 09-nodes.md — 节点与设备（8 页）
**当用户询问以下内容时，请阅读此文件：**
- 音频和语音笔记功能（转录服务）
- 摄像头捕获（iOS、Android、macOS）
- 语音通话模式
- 语音唤醒功能（唤醒词）
- 位置信息命令
- 媒体处理（图像/音频/视频）
- 节点故障排除

### 10-platforms-macos.md — macOS 平台（20 页）
**当用户询问以下内容时，请阅读此文件：**
- macOS 应用程序（菜单栏集成）
- macOS 上的网关设置（launchd 服务）
- macOS 上的技能功能、菜单栏状态显示
- macOS 上的 WebChat 功能
- 网关生命周期（子进程管理）
- macOS 权限设置（TCC）
- 代码签名、Peekaboo Bridge 工具
- Canvas 用户界面、IPC 架构（XPC）
- macOS 开发环境设置、语音唤醒功能
- macOS 日志记录、健康检查

### 11-platforms-mobile.md — 移动平台（2 页）
**当用户询问以下内容时，请阅读此文件：**
- iOS 应用程序（配对、发现机制、Canvas 功能、语音唤醒）
- Android 应用程序（支持功能、系统控制、连接设置）

### 12-platforms-desktop.md — 桌面平台（2 页）
**当用户询问以下内容时，请阅读此文件：**
- Linux 平台（网关设置、systemd 用户单元）
- Windows / WSL2 环境下的安装与配置
- 自动启动设置

### 13-deploy.md — 部署与云托管（12 页）
**当用户询问以下内容时，请阅读此文件：**
- Hetzner VPS 上的部署
- GCP Compute Engine 上的部署
- Fly.io 上的部署
- Railway 平台上的部署
- Render 平台上的部署
- exe.dev 虚拟机的部署
- DigitalOcean 上的虚拟机部署
- Oracle Cloud（始终免费 tier）
- Raspberry Pi 上的部署
- macOS 虚拟机（Lume）
- VPS 托管服务概述

### 14-cli.md — CLI 参考（47 页）
**当用户询问任何 `openclaw` CLI 命令时，请阅读此文件：**
- CLI 总体介绍、全局参数、命令结构
- 命令列表：代理管理、ACP 配置、备份操作
- 命令：浏览器设置、通道管理、配置文件管理、Cron 任务
- 命令：守护进程管理、仪表板操作、设备管理、目录管理、DNS 配置、文档管理
- 命令：网关管理、健康检查、钩子配置、日志记录、内存管理、消息处理
- 命令：节点管理、设备配置、插件管理、二维码生成、重置操作
- 命令：沙箱环境管理、机密管理、安全设置、会话管理、设置操作
- 命令：系统状态查看、TUI 界面管理、卸载操作、更新操作、语音通话设置
- Shell 自动补全功能

### 15-web-uis.md — Web 用户界面（4 页）
**当用户询问 WebChat 或 TUI 界面相关内容时，请阅读此文件：**
- WebChat（网关的 WebSocket 用户界面）
- 仪表板（控制界面）
- TUI（终端用户界面）

### 16-security.md — 安全性（2 页）
**当用户询问安全性相关内容时，请阅读此文件：**
- 威胁模型（MITRE ATLAS 框架）
- 如何为 OpenClaw 的安全性做出贡献
- 安全威胁分析方法

### 17-templates.md — 模板与工作空间文件（8 页）
**当用户询问以下内容时，请阅读此文件：**
- AGENTS.md 模板（工作空间配置文件）
- IDENTITY.md 模板（代理身份信息）
- SOUL.md 模板（代理个性设置）
- USER.md 模板（用户信息配置）
- TOOLS.md 模板（工具说明）
- HEARTBEAT.md 模板（启动指令）
- BOOT.md 模板（首次运行时的引导信息）
- BOOTSTRAP.md 模板（首次使用时的引导流程）

### 18-reference.md — 参考资料（15 页）
**当用户询问相关配置或参考信息时，请阅读此文件：**
- 默认的 AGENTS.md 配置文件
- 新用户引导流程
- 令牌使用与费用说明
- 提示信息缓存配置
- 会话管理相关细节
- SecretRef 证书的使用说明
- RPC 适配器（signal-cli、imsg）
- 设备模型数据库
- API 使用与费用说明
- 测试与持续集成流程
- 发布前的检查清单
- Pi 开发工作流程

### 19-troubleshooting.md — 帮助与故障排除（8 页）
**当用户遇到问题时，请阅读此文件：**
- 常见问题解答（全面覆盖）
- 通用故障排除方法
- 测试方案（Vitest 套件、Docker 运行环境）
- 调试技巧
- 环境变量设置
- 监控工具
- Node.js + tsx 相关的崩溃问题

### 20-experiments.md — 实验与设计文档（10 页）
**当用户询问内部计划或设计相关内容时，请阅读此文件：**
- 内部开发计划与提案
- 模型配置探索方案
- 工作空间内存使用研究
- ACP 线程管理方案
- ACP 统一流处理重构方案
- 浏览器评估相关重构
- OpenResponses 网关设计
- 新用户引导配置协议
- Kilo 网关集成设计

## 重要规则

1. **切勿改写代码块或配置示例**——请严格按照文档中的原文使用。
2. **切勿自行创建配置键或 CLI 参数**——仅引用文档中已存在的选项。
3. 在展示配置示例时，请包含文档中的完整上下文信息（相关键值对、注释等）。
4. 如果文档中提到了版本要求或注意事项，请务必在回答中提及。
5. 如果在文档中找不到答案，请明确说明，并告知用户。
6. 始终注明答案的来源文档部分。
7. 对于 CLI 命令，请严格按照文档中的语法进行展示。
8. 每个 `docs/` 文件中都包含 `<!-- SOURCE: url -->` 注释，可提供给用户参考。