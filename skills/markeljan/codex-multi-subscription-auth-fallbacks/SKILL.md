---
name: codex-auth-fallback
description: 配置 OpenClaw 的多提供者认证机制，同时使用 OpenAI Codex 的 OAuth 备用配置文件以及自动模型切换功能。此设置适用于以下场景：配置多个 OpenAI Codex 账户以实现速率限制的故障转移；通过设备流程添加新的 Codex OAuth 配置文件；或设置定时任务（cron job），在某个提供者达到使用限制（cooldown）时自动切换模型。
requires:
  - codex  # OpenAI Codex CLI (npm i -g @openai/codex) — also provides node
files_read:
  - ~/.codex/auth.json                              # Reads OAuth tokens after device-flow login
files_write:
  - ~/.codex/auth.json                              # Temporarily cleared to force fresh login, then restored from backup
  - ~/.openclaw/agents/main/agent/auth-profiles.json # Writes imported OAuth profile tokens
---
# Codex Auth Fallback

这是一个用于 OpenClaw 的多提供者认证设置方案，支持在 Anthropic 和多个 OpenAI Codex OAuth 会话之间自动进行故障切换。

## 概述

OpenClaw 支持每个提供者配置多个认证配置文件。当某个配置文件达到使用频率限制时，系统可以自动切换到另一个配置文件。本技能涵盖以下内容：

1. **通过设备登录（device-flow login）添加 Codex OAuth 配置文件**  
2. **配置 `openclaw.json` 以确定提供者的故障切换顺序**  
3. **设置 `auth-profiles.json` 文件，包含多个认证配置**  
4. **部署定时任务（cron job）以实现模型的自动切换**  

## 先决条件

- OpenClaw 实例已运行  
- 安装了 `codex` CLI（`npm i -g @openai/codex`）——同时确保系统中也安装了 `node`  
- 拥有一个或多个具有 Codex 访问权限的 OpenAI 账户  

## 安全性说明

**本技能访问的文件及权限：**  
| 文件          | 访问权限       | 目的                |
|---------------|--------------|----------------------|
| `~/.codex/auth.json` | 读 + 临时写      | 临时清除 Codex CLI 的认证信息，然后从备份中恢复；原始令牌不会被删除（会先创建时间戳备份） |
| `~/.openclaw/agents/main/agent/auth-profiles.json` | 读 + 写        | 存储导入的 OAuth 令牌；任何修改前都会创建时间戳备份 |

**重要安全提示：**  
- **令牌仅存储在本地。** 令牌不会被发送到任何外部端点。脚本从本地的 Codex CLI 认证文件中读取令牌，并将其写入 OpenClaw 的认证配置文件中。  
- **始终会创建备份。** 两个文件在修改前都会被备份（包含时间戳）。如果登录失败或脚本中断，系统会自动恢复原始的 Codex CLI 认证信息。  
- **需要用户确认。** 脚本在清除 Codex CLI 认证文件前会提示用户确认，以便在需要时中止操作。  
- **无需特殊权限。** 脚本以当前用户的身份运行，不需要 `sudo` 或其他特殊权限。  
- **建议手动备份。** 尽管有自动备份机制，但在首次使用前，建议手动备份 `~/.codex/auth.json` 和 OpenClaw 的配置文件。  
- **使用非生产账户进行测试。** 在初次测试时，建议使用临时或非生产环境的 OpenAI 账户。  

## 第 1 步：添加 Codex OAuth 配置文件  

针对每个 OpenAI 账户，运行相应的脚本：  

```bash
./scripts/codex-add-profile.sh <profile-name>
```  

该脚本会执行以下操作：  
1. 备份 `~/.codex/auth.json` 和 `auth-profiles.json`  
2. 清除 Codex CLI 的认证信息，强制用户重新进行设备登录  
3. 运行 `codex auth login`（打开浏览器进行 OAuth 登录）  
4. 提取令牌并将其导入 OpenClaw 的 `auth-profiles.json` 文件  
5. 恢复原始的 Codex CLI 认证信息  

对每个账户重复此步骤。配置文件的名称应为简短的标识符（例如 OpenAI 用户名）。  

## 第 2 步：配置 openclaw.json  

在 `openclaw.json` 中添加认证配置文件的声明和备用模型配置。具体需要添加的 JSON 内容请参考 `references/config-templates.md`。  

关键部分包括：  
- `auth.profiles`：声明每个认证配置文件及其对应的提供者和模式  
- `auth.order`：设置每个提供者的故障切换优先级  
- `agentsdefaults.model`：设置默认模型及备用模型  

## 第 3 步：认证配置文件的 JSON 结构  

OpenClaw 将有效的令牌存储在 `agents/main/agent/auth-profiles.json` 文件中。具体结构请参考 `references/config-templates.md`。  

每个 Codex 配置文件包含以下字段：  
- `type`：`"oauth"`  
- `provider`：`"openai-codex"`  
- `access`：JWT 访问令牌（由添加配置文件的脚本自动生成）  
- `refresh`：刷新令牌（由脚本自动生成）  
- `expires`：令牌的有效期限（从 JWT 中解析得出）  
- `accountId`：OpenAI 账户 ID（从 JWT 中解析得出）  

`order` 对象用于指定每个提供者的优先切换顺序。`usageStats` 对象会自动跟踪使用频率限制和冷却时间。  

## 第 4 步：模型自动切换的定时任务（可选）  

> **此步骤完全可选。** 第 1-3 步中的配置文件本身就支持 OpenClaw 的内置故障切换功能。此定时任务用于实现模型的自动切换，这意味着你的活跃模型可能会在无需手动干预的情况下发生变化。只有在理解并希望启用此功能时才需要启用它。  

部署一个定时任务，每 10 分钟检查一次模型的冷却状态并切换活跃模型。具体配置请参考 `references/config-templates.md`。  

定时任务的步骤如下：  
1. 运行 `openclaw models status` 命令检查模型的冷却状态  
2. 选择当前可用的最佳模型（优先级：opus > Codex 配置文件中的模型）  
3. 如有必要，更新会话模型  
4. 将状态信息记录到本地内存文件中；仅在模型切换时触发通知  

**启用前的注意事项：**  
- **先进行手动测试：** 运行 `openclaw models status` 命令验证配置文件是否正常工作。  
- **查看定时任务模板：** 定时任务仅执行本地命令并写入本地状态文件，不会影响你的主要聊天功能。  
- **任务在隔离的会话中运行：** 定时任务在隔离的会话中运行，除非发生模型切换，否则不会影响你的主要聊天体验。  

使用 `references` 中提供的模板，将定时任务添加到 `cron/jobs.json` 文件中。  

## 文件结构  

```
codex-auth-fallback/
├── SKILL.md                    # This file
├── scripts/
│   └── codex-add-profile.sh    # Device-flow profile importer
└── references/
    └── config-templates.md     # openclaw.json, auth-profiles, cron templates
```