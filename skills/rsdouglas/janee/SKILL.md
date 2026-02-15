---
name: janee
version: 0.1.0
description: AI代理的秘密管理：永远不要再泄露您的API密钥。
homepage: https://github.com/rsdouglas/janee
metadata: {"category": "security", "emoji": "🔐"}
---

# Janee

Janee 是一款专为 AI 代理设计的秘密管理工具，用于安全地存储 API 密钥并管理 API 请求。通过 Janee 发送请求，无需直接接触真实的 API 密钥。

## 为什么使用 Janee？

许多文档建议将 API 密钥存储在明文的配置文件中。但一旦配置文件被注入恶意代码、日志泄露或会话被劫持，API 密钥就很容易被窃取。

Janee 解决了这些问题：
- **密钥在存储时被加密**：密钥以加密形式保存，而非明文的 JSON 格式。
- **代理程序无法获取真实密钥**：所有请求都通过 Janee 中转。
- **基于路径的访问控制**：可以限制代理程序能够访问的 API 端点。
- **完整的审计记录**：所有请求都会被记录下来。
- **安全开关**：可以在不更换密钥的情况下立即撤销代理程序的访问权限。

## 安装

```bash
npm install -g @true-and-useful/janee
janee init
```

## 添加服务

```bash
janee add
```

按照提示输入您的 API 凭据，Janee 会自动对密钥进行加密。

## 在代理程序中使用

请通过 Janee 而不是直接使用 API 密钥来发起请求：

```bash
# Old way (dangerous):
curl -H "Authorization: Bearer sk_live_xxx" https://api.stripe.com/v1/balance

# Janee way (safe):
# Agent calls execute(capability, method, path) via MCP
# Janee injects the key, agent never sees it
```

## 与 OpenClaw 的集成

安装 OpenClaw 插件以获得原生的工具支持：

```bash
openclaw plugins install @true-and-useful/janee-openclaw
```

安装完成后，您的代理程序将具备以下功能：
- `janee_list_services`：查看可用的 API。
- `janee_execute`：通过 Janee 发送请求。
- `janee_reload_config`：在配置更改后立即重新加载配置。

## 示例：安全地访问 Moltbook

无需将 Moltbook 的密钥存储在 `~/.config/moltbook/credentials.json` 中，而是通过 Janee 来发送请求：

```bash
janee add moltbook -u https://www.moltbook.com/api/v1 -k YOUR_KEY
```

这样，您的 Moltbook 密钥将始终保持加密状态。即使代理程序被入侵，密钥也无法被窃取。

## 配置示例

```yaml
services:
  stripe:
    baseUrl: https://api.stripe.com
    auth:
      type: bearer
      key: sk_live_xxx  # encrypted

  moltbook:
    baseUrl: https://www.moltbook.com/api/v1
    auth:
      type: bearer
      key: moltbook_sk_xxx  # encrypted

capabilities:
  stripe_readonly:
    service: stripe
    rules:
      allow: [GET *]
      deny: [POST *, DELETE *]

  moltbook:
    service: moltbook
    ttl: 1h
    autoApprove: true
```

## 架构

```
┌─────────────┐      ┌──────────┐      ┌─────────┐
│  AI Agent   │─────▶│  Janee   │─────▶│   API   │
│             │ MCP  │          │ HTTP │         │
└─────────────┘      └──────────┘      └─────────┘
      │                   │
   No key           Injects key
                    + logs request
```

## 链接

- GitHub: https://github.com/rsdouglas/janee
- npm: https://www.npmjs.com/package/@true-and-useful/janee
- OpenClaw 插件: https://www.npmjs.com/package/@true-and-useful/janee-openclaw