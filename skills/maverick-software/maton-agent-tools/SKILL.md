---
name: maton
description: 通过 Maton AI 连接到 SaaS 工具。该功能支持与 Clawdbot Gateway 仪表板进行完整的 UI 集成。适用于配置 Maton 的集成设置、连接应用程序（如 Gmail、Slack、Notion、HubSpot 等），或管理 OAuth 连接。
metadata: {"clawdbot":{"emoji":"🔗","requires":{"clawdbot":">=2026.1.0"},"category":"integrations"}}
---
# Maton AI

通过 Maton 的 OAuth 连接管理功能，您可以将您的 AI 代理连接到 SaaS 工具。该功能提供以下功能：

- **完整的用户界面仪表板**：配置 API 密钥、查看连接信息、启动 OAuth 流程
- **多应用支持**：Gmail、Slack、Notion、HubSpot、Jira、Google Workspace 等
- **连接管理**：创建、监控和删除应用连接
- **API 密钥集成**：Maton 的 API 密钥会显示在“API 密钥”标签页中，便于配置

## 概述

Maton 提供了一个统一的 API，用于通过 OAuth 连接到 SaaS 工具。连接成功后，您可以通过 Maton 的 AI 功能或直接通过这些工具的 API 与它们进行交互。

## 先决条件

1. **Maton 账户**：在 [maton.ai](https://maton.ai) 注册
2. **API 密钥**：从 Maton 仪表板获取您的 API 密钥
3. **Clawdbot Gateway**：版本需达到 v2026.1.0 或更高，并且启用了用户界面

## 快速入门

### 第 1 步：获取 API 密钥

1. 访问 [maton.ai](https://maton.ai) 并登录
2. 转到“设置” → “API 密钥”
3. 创建或复制您的 API 密钥

### 第 2 步：在 Clawdbot 用户界面中进行配置

**选项 A：通过“API 密钥”标签页**
1. 打开 Clawdbot 仪表板 → “设置” → “API 密钥”
2. 在“环境密钥”部分找到“Maton”
3. 输入您的 API 密钥并点击“保存”

**选项 B：通过“Maton”标签页**
1. 打开 Clawdbot 仪表板 → “工具” → “Maton”
2. 点击“配置”
3. 粘贴您的 API 密钥
4. 点击“保存”

### 第 3 步：连接应用

1. 转到“工具” → “Maton”
2. 点击“连接应用”并选择一个应用（例如 Gmail、Slack）
3. 完成弹出窗口中的 OAuth 流程
4. 当状态显示为“ACTIVE”时，连接即已完成

## 支持的应用

Maton 支持 50 多种 SaaS 应用，包括：

| 类别 | 应用 |
|----------|------|
| **Google Workspace** | Gmail、日历、文档、表格、驱动器、幻灯片、广告、分析 |
| **生产力** | Notion、Airtable、Jira、Calendly |
| **通信** | Slack、Outlook |
| **CRM** | HubSpot、Apollo |
| **媒体** | YouTube |

## API 参考

### 基本 URL
```
https://ctrl.maton.ai
```

### 认证

所有请求都需要一个 Bearer 令牌：
```bash
curl https://ctrl.maton.ai/connections \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### 端点

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/connections` | 列出所有连接 |
| POST | `/connections` | 创建新的连接 |
| GET | `/connections/{id}` | 获取连接详情 |
| DELETE | `/connections/{id}` | 删除连接 |

### 连接状态

| 状态 | 描述 |
|--------|-------------|
| `PENDING` | OAuth 流程未完成；`url` 包含 OAuth 链接 |
| `ACTIVE` | 连接已建立，可以使用 |
| `FAILED` | 连接失败；需要重新连接 |

## 架构

### 配置存储

Maton 的 API 密钥存储在 Clawdbot 的主配置文件中：

```json
{
  "env": {
    "MATON_API_KEY": "your-api-key-here"
  }
}
```

这实现了 API 密钥的集中管理。

### 后端 RPC 方法

| 方法 | 用途 |
|--------|---------|
| `maton.status` | 获取 API 密钥状态和连接数量 |
| `maton.save` | 验证并存储 API 密钥 |
| `maton.test` | 测试 API 密钥 |
| `maton.disconnect` | 删除 API 密钥 |
| `maton.connections` | 列出所有连接 |
| `maton.connect` | 创建新的连接（返回 OAuth 链接） |
| `maton.delete` | 删除连接 |
| `maton.apps` | 列出支持的应用 |

### 用户界面组件

| 文件 | 用途 |
|------|---------|
| `maton-backend.ts` | 代理后端 RPC 处理程序 |
| `maton-controller.ts` | 用户界面状态管理 |
| `maton-views.ts` | HTML 模板 |

## 安装

请参阅 `reference/README.md` 以获取详细的集成说明。

### 快速集成

1. 将后端处理程序复制到 `src/gateway/server-methods/maton.ts`
2. 将用户界面文件复制到 `ui/src/ui/views/` 和 `ui/src/ui/controllers/`
3. 在导航栏中添加“Maton”标签页
4. 在 API 密钥管理中添加 `MATON_API_KEY`
5. 重新构建并重启 Clawdbot

## 用户界面特性

### “Maton”标签页（工具 → Maton）
- 连接状态（显示活跃/待处理的连接数量）
- API 密钥配置表单
- 显示连接状态的应用列表
- 用于新连接的 aplik 选择器模态框
- 一键启动 OAuth 流程

### “API 密钥”标签页集成
- 在“环境密钥”部分显示“Maton”
- 提供 API 密钥的直接输入字段
- 提供保存/清除功能

## 安全性

| 方面 | 实现方式 |
|--------|----------------|
| **密钥存储** | 存储在主配置文件（`~/.clawdbot/clawdbot.json`）中 |
| **密钥访问** | 绝不暴露给 AI 代理 |
| **OAuth 令牌** | 由 Maton 管理（自动刷新）

**最佳实践**：
- 定期轮换 API 密钥
- 定期检查已连接的应用
- 断开未使用的连接

## 故障排除

### 出现“未经授权”的错误
- 确认您的 API 密钥是否正确
- 检查密钥是否已被吊销
- 如有需要，在 Maton 仪表板中重新生成密钥

### 连接状态为“PENDING”
- OAuth 流程未完成
- 重新尝试 OAuth 链接
- 如果链接已过期，请删除并重新创建连接

### 连接状态显示为“FAILED”
- OAuth 令牌可能已过期
- 删除连接并重新创建

### “Maton”未显示在“API 密钥”标签页中
- 确保您使用的 Clawdbot 版本为 v2026.1.0 或更高
- 重新启动代理后刷新页面

## 参考文件

- `reference/maton-backend.ts` — 代理后端 RPC 处理程序
- `reference/maton-controller.ts` — 用户界面控制器逻辑
- `reference/maton-views.ts` — 用户界面渲染代码
- `reference/README.md` — 安装指南

## 支持资源

- **Maton**：[maton.ai](https://maton.ai)
- **ClawdHub**：[clawdhub.com/skills/maton](https://clawdhub.com/skills/maton)
- **Discord**：[discord.com/invite/clawd](https://discord.com/invite/clawd)