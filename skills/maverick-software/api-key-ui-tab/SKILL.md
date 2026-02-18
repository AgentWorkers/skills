---
name: apikeys-ui
description: OpenClaw仪表板的API密钥管理界面：用户可以直接在浏览器中输入并保存API密钥，无需将这些密钥暴露给AI代理。该界面会显示已配置的API密钥、缺失的API密钥，并为每个密钥提供安全的输入字段。
version: 1.1.0
author: OpenClaw Community
metadata: {"clawdbot":{"emoji":"🔑","requires":{"clawdbot":">=2026.1.0"},"category":"settings"}}
---
# API密钥管理界面

在OpenClaw的控制面板（**Settings**）下，新增了一个**API密钥**选项卡。您可以直接在浏览器中管理您的API密钥——这些密钥会被保存到配置文件中，而永远不会被发送给AI代理。

## 主要功能

| 功能 | 说明 |
|---------|-------------|
| **动态检测** | 自动扫描整个配置文件以查找API密钥（无需使用硬编码的密钥列表） |
| **控制面板选项卡** | 在侧边栏的**Settings**下显示“API密钥”选项卡 |
| **密钥状态** | 查看哪些密钥已配置（✓）或缺失 |
| **安全输入** | 密码字段在保存后不会显示密钥内容 |
| **直接保存** | 密钥会通过`config.patch` RPC命令直接保存到配置文件 |
| **提供商链接** | 为已知的API提供商提供“获取密钥”按钮 |
| **清除密钥** | 一键清除配置文件中的密钥 |
| **自动分组** | 根据环境、技能或其他类别对密钥进行分组 |

## 动态密钥检测

该界面会**自动扫描整个配置文件**以查找API密钥。如果没有硬编码的密钥列表，任何符合API密钥格式的字段都会被识别并显示。

### 密钥检测规则
以下字段会被识别为API密钥：
- `apiKey`, `api_key`
- `token`, `secret`
- `*_KEY`, `*_TOKEN`, `*_SECRET`

### 密钥可能存在的位置
- `env.*`：环境变量
- `skills.entries.*.apiKey`：与特定技能相关的密钥
- `messages.tts.*.apiKey`：TTS提供商的密钥
- 任何嵌套的配置路径

### 已知API提供商（优化后的用户界面）
这些提供商会显示友好的名称、描述以及“获取密钥”的链接：

| 提供商 | 环境变量密钥 |
|----------|---------|
| Anthropic | `ANTHROPIC_API_KEY` |
| OpenAI | `OPENAI_API_KEY` |
| Brave Search | `BRAVE_API_KEY` |
| ElevenLabs | `ELEVENLABS_API_KEY` |
| Google | `GOOGLE_API_KEY` |
| Deepgram | `DEEPGRAM_API_KEY` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Fireworks | `FIREWORKS_API_KEY` |
| Mistral | `MISTRAL_API_KEY` |
| xAI | `XAI_API_KEY` |
| Perplexity | `PERPLEXITY_API_KEY` |
| GitHub | `GITHUB_TOKEN` |

未知的密钥仍然会被显示，但系统会从它们的配置路径自动生成名称。

## 安全机制

**重要提示：**AI代理**永远不会看到您的API密钥。所有操作都是通过浏览器直接与网关进行交互的，网关负责将密钥写入配置文件。

## 代理安装提示

（此处应包含代理安装的相关信息）

## 包含的文件

（此处应列出包含在项目中的所有文件）

## 工作原理

1. **控制器**（`apikeys-controller.ts`）：
   - `scanForKeys()`：递归遍历配置文件，查找符合密钥格式的字段
   - `loadApiKeys()`：获取配置文件内容，进行扫描，并补充缺失的环境变量密钥
   - `saveApiKey()`：构建用于更新配置的JSON对象，并通过`config.patch` RPC命令保存
   - `clearApiKey()`：将密钥值设置为`null`
   - `KNOWN_PROVIDERS`：为已识别的密钥提供元数据（名称、描述、文档链接）

2. **视图组件**（`apikeys-views.ts`）：
   - 按类别（环境、技能等）对密钥进行分组
   - 显示带有保存/清除按钮的密码输入框
   - 对已配置的密钥显示屏蔽后的预览内容
   - 为已知的API提供商提供“获取密钥”的链接

3. **安全性**：
   - 在浏览器中输入的密钥内容会通过WebSocket直接发送到网关
   - AI代理无法获取密钥的实际值
   - 用户界面仅显示密钥的前4个和后4个字符（进行屏蔽处理）

## 更新记录

### v1.1.0
- **动态密钥检测**：自动扫描整个配置文件，而非依赖硬编码的密钥列表
- 密钥按环境、技能或其他类别进行自动分组
- 增加了刷新按钮以重新加载页面
- 即使未配置，也会显示常见的环境变量密钥

### v1.0.0
- 初始版本发布
- 提供商信息采用硬编码方式
- 支持保存和清除密钥的功能