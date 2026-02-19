---
name: clawapi
description: 使用一款原生 macOS 应用程序来切换 AI 模型并管理 OpenClaw 的 API 密钥。该应用程序支持 16 家提供商，包括 OpenAI、Anthropic、xAI、Google、Groq、Ollama、LM Studio 等。
homepage: https://github.com/Gogo6969/clawapi
user-invocable: true
metadata: {"openclaw":{"emoji":"🔑","requires":{"bins":["curl"],"config":["skills.entries.clawapi"]},"install":[{"kind":"script","command":"curl -fsSL https://raw.githubusercontent.com/Gogo6969/clawapi/main/install.sh | bash"}]}}
---
# ClawAPI — OpenClaw的模型切换器与密钥管理工具

ClawAPI是一款专为macOS设计的应用程序，它允许用户切换AI模型并管理OpenClaw的API密钥。

## 主要功能

- **一键模型切换**：用户可以从任意提供商中选择模型，并立即应用该模型。
- **Touch ID身份验证**：支持使用Touch ID进行API密钥的添加和删除操作。
- **支持16个提供商**：包括OpenAI、Anthropic、xAI、Google、Grok、Mistral、OpenRouter、Cerebras、Kimi、MiniMax、Z.AI、OpenCode Zen、Vercel AI、HuggingFace、Ollama、LM Studio等。
- **安全配置**：在写入API密钥前会进行JSON格式验证，并自动创建备份文件（`.bak`）。

## 安装方法

### 方法1：从GitHub Releases下载（推荐）

从[GitHub Releases](https://github.com/Gogo6969/clawapi/releases)下载最新的、已签名且经过公证的`.zip`文件，解压后将其放入`/Applications`目录中。

### 方法2：使用安装脚本

```bash
curl -fsSL https://raw.githubusercontent.com/Gogo6969/clawapi/main/install.sh | bash
```

该安装脚本会从GitHub Releases下载相同的已签名`.zip`文件，验证其SHA-256校验和，解压后将其放入`/Applications`目录。在运行脚本之前，您可以[查看脚本源代码](https://github.com/Gogo6969/clawapi/blob/main/install.sh)。

该应用程序要求macOS系统版本在14.0或以上。该应用已使用Apple开发者ID进行签名，并经过Apple官方的公证。

## 工作原理

1. **添加提供商**：点击“+”按钮，选择所需的提供商，然后粘贴相应的API密钥。
2. **选择模型**：通过下拉菜单选择具体的模型（如GPT-4.1、Claude Sonnet 4、Grok 4等）。
3. **完成设置**：ClawAPI会自动将所有配置信息同步到OpenClaw中。

## API密钥的存储位置

API密钥被设计为存储在**两个地方**：

- **macOS Keychain（主副本）**：用户输入的API密钥会存储在macOS Keychain中，受到硬件加密和Touch ID的保护。这是密钥的权威存储位置。
- `auth-profiles.json`（OpenClaw的同步副本）：OpenClaw会从自身的`auth-profiles.json`配置文件中读取API密钥。ClawAPI会将密钥的副本写入该文件，以便OpenClaw能够使用。该文件位于`~/Library/Application Support/OpenClaw/`目录下。

当前选定的模型信息会保存在`openclaw.json`文件中。ClawAPI不使用任何代理或中间件，直接与提供商的API进行通信。

## 安全性与隐私保护

- API密钥通过macOS Keychain进行存储，并采用硬件加密技术进行保护；同时会在OpenClaw的`auth-profiles.json`文件中保存一份同步副本。
- 支持使用Touch ID进行密钥的添加和删除操作（在没有Touch ID功能的Mac设备上会使用密码验证）。
- 该应用已使用Apple开发者ID进行签名，并经过Apple官方的公证。
- 该应用启用了安全加固机制（hardened runtime）。
- 所有数据仅在本机存储和处理，不会被传输到外部。
- 该应用不收集任何用户数据或发送任何遥测信息。

## 外部接口

| 接口地址 | 功能 | 发送的数据 |
|----------|---------|-----------|
| `raw.githubusercontent.com` | 检查应用更新 | 不发送任何数据（仅读取`update.json`文件） |
| `localhost:11434` | 获取Ollama模型信息 | 不发送任何数据（仅读取本地API） |
| `localhost:1234` | 获取LM Studio模型信息 | 不发送任何数据（仅读取本地API） |

ClawAPI不会发起任何其他网络请求。

## 相关链接

- **GitHub仓库**：[github.com/Gogo6969/clawapi](https://github.com/Gogo6969/clawapi)
- **文档**：[docs/USER_GUIDE.md](https://github.com/Gogo6969/clawapi/blob/main/docs/USER_GUIDE.md)