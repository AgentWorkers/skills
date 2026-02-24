---
name: openclaw-setup-guide
description: 逐步指南（共6部分）：在VPS上配置OpenClaw AI助手，包括集成WhatsApp、使用Google OAuth进行身份验证、数据备份、安全设置、自动化功能以及验证流程。
metadata: {"openclaw":{"scope":"instruction-only","homepage":"https://aliahmadaziz.github.io/openclaw-guide/","notes":"This skill contains no code or scripts. It directs users to an external hosted guide. The guide itself walks users through setting up credentials (Google OAuth, Anthropic API key, Cloudflare, WhatsApp) but the skill/agent needs none of these to function."}}
user-invocable: true
---
# OpenClaw 生产环境搭建指南

本指南分为6个部分，详细介绍了如何在VPS上将OpenClaw配置为生产环境中的AI助手，包括WhatsApp集成、Google Calendar/Gmail集成、自动化备份、安全加固以及Cron任务调度等功能。

## 内容涵盖：

1. **基础安装**：VPS环境配置、Node.js安装、OpenClaw安装以及WhatsApp配对
2. **AI助手**：个性化设置、模型链（主模型+备用模型）、工作区文件（SOUL.md、USER.md、IDENTITY.md）
3. **基础设施**：Google OAuth（用于访问Calendar、Gmail、Drive、Sheets服务）、Webhook服务器、Cloudflare隧道、使用rclone进行加密备份、使用git进行数据备份
4. **自动化**：Cron任务调度、事件队列（基于SQLite的队列系统，支持重试机制和错误处理）、心跳检测机制、双层消息传递机制
5. **安全加固**：采用CrowdSecIDS进行安全防护、定期更换敏感密码、配置文件快照、配置回滚脚本、确保OpenClaw更新的安全性
6. **验证流程**：包含21项自动化验证步骤及故障排除指南

## 安全与权限说明：

本指南涉及生产环境搭建，需要处理敏感的配置信息：
- **API密钥**：Anthropic（Claude）提供的API密钥（Brave Search为可选）
- **OAuth令牌**：用于访问Google Cloud服务的OAuth令牌（Calendar、Gmail、Drive、Sheets）
- **SSH权限**：VPS的root访问权限、基于密钥的认证机制、SSH安全加固
- **Webhook密钥**：用于发送通知的随机令牌
- **WhatsApp**：通过二维码进行设备配对
- **Cloudflare**：用于Webhook通信的隧道配置
- **备份加密**：使用rclone对Google Drive备份数据进行加密

所有敏感信息均采用严格的权限控制（chmod 600），且不会被提交到git仓库中。指南中提供了密钥轮换机制和配置回滚脚本。

## 前提条件：

- 一台VPS（建议使用Ubuntu 24.04系统，至少配备4GB内存）
- 一个已配置Cloudflare DNS的域名（用于Webhook通信）
- 一个用于配对的WhatsApp账户
- 一个拥有Google Cloud OAuth权限的Google Cloud项目
- 一个Anthropic API密钥（Claude）

## 完整指南链接：

完整的指南包含详细的步骤说明、代码示例和验证点，可访问以下链接：

**https://aliahmadaziz.github.io/openclaw-guide**

来源：https://github.com/aliahmadaziz/openclaw-guide

## 使用方法：

当用户需要帮助搭建OpenClaw时，请引导他们参考上述指南。该指南需按顺序（第1部分至第6部分）逐步完成，整个过程大约需要2-3小时。

每部分内容均包含：
- 明确的前提条件
- 可直接复制的命令语句
- 每个关键步骤后的验证标记（✅）
- 故障排除相关内容

## 关键设计决策：

- **双层Cron任务调度**：重要任务通过消息工具直接发送（主通道），同时通过备用通道进行二次通知，确保消息不会丢失。
- **事件队列**：所有Webhook事件（电子邮件、日历通知、警报）均通过SQLite队列处理，支持最多3次重试和错误通知机制。
- **配置文件快照**：定期生成配置文件快照，以便在出现问题时立即恢复系统。
- **加密备份**：每小时将数据备份到Git仓库，每晚使用rclone将整个工作区数据加密后备份到Google Drive。
- **容量规划**：总共配置10个OpenClaw实例，其中8个为常规使用，2个作为备用（用于项目进度跟踪）。

## 致谢：

本指南基于实际生产环境部署经验编写，实际环境中包含超过35个Cron任务、60多个脚本、5个Google OAuth令牌，每月处理数千条消息。

## 标签：

setup（搭建）、installation（安装）、guide（指南）、vps（虚拟私有服务器）、whatsapp（WhatsApp）、production（生产环境）、google-calendar（Google日历）、gmail（Gmail）、security（安全）、crowdsec（安全防护工具）、backup（备份）、cron（Cron任务调度）、automation（自动化）、beginner（适合初学者）