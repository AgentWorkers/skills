---
name: clawapi
description: 使用一款专为 macOS 设计的原生应用程序，您可以轻松切换 AI 模型并管理 OpenClaw 的 API 密钥。该应用程序支持 16 家提供商，包括 OpenAI、Anthropic、xAI、Google、Groq、Ollama、LM Studio 等。
homepage: https://github.com/Gogo6969/clawapi
user-invocable: true
metadata: {"openclaw":{"emoji":"🔑","requires":{"bins":["curl"],"config":["skills.entries.clawapi"]},"install":[{"kind":"script","command":"curl -fsSL https://raw.githubusercontent.com/Gogo6969/clawapi/main/install.sh | bash"}]}}
---
# ClawAPI — OpenClaw的模型切换器与密钥管理工具

ClawAPI是一款专为macOS设计的原生应用程序，它允许您轻松切换AI模型，并安全地管理OpenClaw所需的API密钥。

## 主要功能

- **一键模型切换**：您可以随时从任意提供商中选择模型并立即应用。
- **安全的密钥管理**：API密钥存储在macOS的Keychain中，并采用硬件加密技术进行保护。
- **触控ID认证**：支持使用触控ID进行API密钥的添加和删除操作。
- **支持16家提供商**：包括OpenAI、Anthropic、xAI、Google、Grok、Mistral、OpenRouter、Cerebras、Kimi、MiniMax、Z.AI、OpenCode Zen、Vercel AI、HuggingFace、Ollama和LM Studio。
- **自动同步**：所有更改会自动写入OpenClaw的配置文件中。
- **自动更新**：内置的更新检测机制会从GitHub获取最新版本。
- **VPS支持**：支持通过SSH在远程服务器上管理OpenClaw。
- **配置安全性**：在写入配置文件前会进行JSON格式验证，并自动创建备份文件。

## 安装说明

```bash
curl -fsSL https://raw.githubusercontent.com/Gogo6969/clawapi/main/install.sh | bash
```

将`ClawAPI.app`安装到`/Applications`文件夹中。该应用兼容macOS 14及以上版本，已使用Apple开发者ID签名并通过Apple官方认证。

## 使用方法

1. **添加提供商**：点击“+”按钮，选择所需的提供商，然后粘贴相应的API密钥。
2. **选择模型**：从下拉菜单中选择所需的模型（如GPT-4.1、Claude Sonnet 4、Grok 4等）。
3. **完成设置**：ClawAPI会自动将所有信息同步到OpenClaw中。

ClawAPI会将您的API密钥保存到`auth-profiles.json`文件中，并在`openclaw.json`文件中设置当前使用的模型。整个过程中无需使用代理或中间件，OpenClaw直接与提供商的API进行交互。

## 支持的提供商

### 云服务提供商

| 提供商 | 密钥格式 |
|---------|---------|
| OpenAI | `sk-...` |
| Anthropic | `sk-ant-...` |
| xAI | `xai-...` |
| Google AI | `AIza...` |
| Groq | `gsk_...` |
| Mistral | — |
| OpenRouter | `sk-or-...` |
| Cerebras | — |
| Kimi (Moonshot) | — |
| MiniMax | — |
| Z.AI (GLM) | — |
| OpenCode Zen | — |
| Vercel AI | — |
| HuggingFace | `hf_...` |

### 本地提供商（无需API密钥）

| 提供商 | 端点地址 | 备注 |
|---------|---------|---------|
| Ollama | `localhost:11434` | 本地Ollama模型访问 |
| LM Studio | `localhost:1234` | 本地LM Studio模型访问 |

## 安全性与隐私保护

- 所有API密钥均存储在macOS的Keychain中，绝不会以明文形式存储在硬盘上。
- 使用触控ID进行密钥的添加和删除操作；在没有触控ID的设备上则支持密码验证。
- 该应用已使用Apple开发者ID签名，并经过Apple官方认证。
- 采用了加固的运行时安全机制。
- 所有数据仅在本机存储或通过SSH传输（在启用VPS模式时）。
- ClawAPI不会发送任何额外的网络请求（除非您配置了VPS模式）。

## 外部连接信息

| 连接地址 | 功能 | 发送的数据 |
|---------|---------|-----------|
| `raw.githubusercontent.com` | 检查应用更新 | 无（读取`update.json`文件） |
| `localhost:11434` | 获取Ollama模型信息 | 无（读取本地API） |
| `localhost:1234` | 获取LM Studio模型信息 | 无（读取本地API） |
| SSH（用户配置） | VPS模式配置同步 | 加密后的API密钥 |

## 相关资源

- **GitHub仓库**：[github.com/Gogo6969/clawapi](https://github.com/Gogo6969/clawapi)
- **文档**：[github.com/Gogo6969/clawapi/wiki](https://github.com/Gogo6969/clawapi/wiki)
- **官方网站**：[clawapi.app](https://clawapi.app)
- **用户手册**：[docs/USER_GUIDE.md](https://github.com/Gogo6969/clawapi/blob/main/docs/USER_GUIDE.md)