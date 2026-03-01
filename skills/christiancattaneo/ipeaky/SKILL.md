---
name: ipeaky
description: OpenClaw的安全API密钥管理功能：允许用户存储、查看、测试和删除API密钥，同时确保这些密钥不会被记录在聊天历史中。密钥通过`gateway config.patch`直接存储在`openclaw.json`文件中，实现了与OpenClaw系统的完全原生集成。当用户需要提供、管理或测试API密钥（例如与OpenAI、ElevenLabs、Anthropic、Brave等服务的交互）时，可以使用此功能。该功能会在用户输入特定指令（如“add API key”、“store my key”、“manage keys”、“test my key”或“set up API key”）时触发；此外，当某个技能需要使用但尚未配置API密钥时，也会自动触发该功能。
metadata:
  openclaw:
    platforms: [macos]
    requires:
      bins: [osascript]
    notes: "Secure input popup requires macOS (osascript). Linux/Windows users can pipe keys via stdin directly."
---
# ipeaky — 安全的API密钥管理

密钥通过 `gateway config.patch` 直接存储在 OpenClaw 的原生配置文件 `openclaw.json` 中。这意味着任何声明了 `primaryEnv` 的技能都会自动获取到该密钥，无需任何手动配置。

## 密钥映射 — 服务与配置路径的对应关系

| 服务          | 配置路径             | primaryEnv       |
|----------------|------------------|-------------------|
| OpenAI         | `skills.entries.openai-whisper-api.apiKey` | OPENAI_API_KEY     |
| ElevenLabs     | `skills.entries.sag.apiKey`      | ELEVENLABS_API_KEY     |
| Brave Search    | `tools.web.search.apiKey`     | BRAVE_API_KEY     |
| Gemini         | `skills.entries.nano-banana-pro.apiKey` | GEMINI_API_KEY     |
| Google Places    | `skills.entries.goplaces.apiKey`     | GOOGLE_PLACES_API_KEY     |
| Notion        | `skills.entries.notion.apiKey`     | NOTION_API_KEY     |
| ElevenLabs Talk    | `talk.apiKey`         | (直接访问)       |
| 自定义技能       | `skills.entries.<skill-name>.apiKey`   | (根据技能配置)     |
| 自定义环境变量     | `skills.entries.<skill-name>.env.<VAR_NAME>` | (任意环境变量)     |

**重要提示：**某些密钥被多个技能共享。例如，OpenAI 密钥同时被 `openai-whisper-api` 和 `openai-image-gen` 等技能使用；ElevenLabs 密钥被 `sag` 和 `talk` 等技能使用。在存储密钥时，请确保设置所有相关的配置路径。

## 密钥存储方式（v4 — 一次粘贴，零风险）⭐ 推荐使用

只需弹出一个窗口让用户粘贴所有密钥，脚本会自动解析密钥值对，然后保存配置并重启 OpenClaw 代理。密钥永远不会被显示在聊天记录或网络日志中。

```bash
bash {baseDir}/scripts/store_key_v4.sh "<SERVICE_NAME>" "<config_prefix>"
```

### 示例：
```bash
# X API keys (consumer key + secret + bearer in one paste)
bash {baseDir}/scripts/store_key_v4.sh "X API" "skills.entries.x-twitter.env"

# Any service — user pastes in any format:
#   consumer key: abc123
#   secret: xyz789
#   bearer token: AAAA...
```

脚本流程：
1. 显示一个 macOS 弹窗，用户可以以任意格式粘贴密钥。
2. 本地 Python 脚本会解析这些密钥值对（无需使用人工智能或网络连接）。
3. 显示确认弹窗：“找到 3 个密钥：X、Y、Z——是否全部保存？”
4. 通过一次 `openclaw config set` 操作完成所有密钥的配置更新，随后重启代理。
5. 密钥不会出现在聊天记录、日志或 shell 历史记录中。

### 支持的输入格式：
- `key_name: value` 或 `key_name = value`
- `KEY_NAME=value`
- 单独的密钥值（按顺序自动标记）
- 混合格式的密钥值（可一次性粘贴）

---

## 密钥存储方式（v3 — 零风险）

**使用 v3 脚本**。代理程序永远不会直接看到密钥，所有操作均由脚本完成。

```bash
bash {baseDir}/scripts/store_key_v3.sh "<SERVICE_NAME>" "<config_path1>" ["<config_path2>" ...]
```

### 示例：
```bash
# Brave Search
bash {baseDir}/scripts/store_key_v3.sh "Brave Search" "tools.web.search.apiKey"

# OpenAI (multiple paths)
bash {baseDir}/scripts/store_key_v3.sh "OpenAI" "skills.entries.openai-whisper-api.apiKey"

# ElevenLabs (sag + talk)
bash {baseDir}/scripts/store_key_v3.sh "ElevenLabs" "skills.entries.sag.apiKey" "talk.apiKey"
```

脚本流程：
1. 显示一个 macOS 弹窗（输入内容隐藏）。
2. 为每个密钥路径调用 `openclaw config set` 命令。
3. 重启 OpenClaw 代理。
4. 脚本仅返回 “OK” 或 “ERROR”，密钥不会显示在代理的输出或聊天记录中。

### 旧版本的方法（v2 — 代理程序会看到密钥，不推荐使用）

**步骤 1：** 打开安全输入弹窗（macOS 用户界面）。

**步骤 2：** 获取密钥值后（从脚本的输出中获取），通过 `gateway config.patch` 进行存储。

**OpenAI 示例：**  
```
gateway config.patch with raw: {"skills":{"entries":{"openai-whisper-api":{"apiKey":"THE_KEY"},"openai-image-gen":{"apiKey":"THE_KEY"}}}}
```

**ElevenLabs 示例：**  
```
gateway config.patch with raw: {"skills":{"entries":{"sag":{"apiKey":"THE_KEY"}}},"talk":{"apiKey":"THE_KEY"}}
```

**Brave Search 示例：**  
```
gateway config.patch with raw: {"tools":{"web":{"search":{"apiKey":"THE_KEY"}}}}
```

**重要规则：**
- 绝不允许在聊天消息或工具调用参数中显示密钥值。
- 不要在 `config.patch` 的 `reason` 字段中包含密钥值。
- 如果用户直接在聊天中输入密钥，请立即将其存储并提示用户删除该消息。
- `secure_input_mac.sh` 脚本会将密钥值输出到标准输出（stdout），将其存储在变量中并用于配置更新，切勿记录到日志中。

## 查看密钥信息

使用 `gateway config.get` 从当前配置中读取密钥信息，仅显示密钥的前 4 个字符和其余被遮蔽的部分。解析配置 JSON 文件，找到所有包含 `apiKey` 的字段，并显示它们的配置路径和遮蔽后的密钥值。

## 测试密钥的有效性

测试以下 API 端点：
- **OpenAI**：`curl -s -H "Authorization: Bearer $KEY" https://api.openai.com/v1/models | head`
- **ElevenLabs**：`curl -s -H "xi-api-key: $KEY" https://api.elevenlabs.io/v1/user`
- **Anthropic**：`curl -s -H "x-api-key: $KEY" -H "anthropic-version: 2023-06-01" https://api.anthropic.com/v1/messages -d '{"model":"claude-3-haiku-20240307","max_tokens":1,"messages":[{"role":"user","content":"hi"}]}'`
- **Brave Search**：`curl -s -H "X-Subscription-Token: $KEY" "https://api.search.brave.com/res/v1/web/search?q=test&count=1"`

从配置文件中获取密钥值（通过 `gateway config.get`），进行测试并显示结果。切勿直接显示密钥本身。

## 删除密钥

使用 `gateway config.patch` 将密钥值设置为空字符串或删除相应的配置项。

## 💎 付费版本（即将推出）

ipeaky 的基础功能永久免费。付费版本将提供以下高级功能：
- **团队密钥共享**：支持团队成员基于角色的访问权限管理。
- **密钥轮换提醒**：自动发送密钥过期通知。
- **使用情况分析**：追踪各技能的密钥使用情况。
- **安全漏洞监控**：检测密钥泄露事件。
- **跨平台支持**：支持 Linux 和 Windows 系统的安全输入方式。
- **备份与同步**：提供加密的云备份服务。

详情请参阅 `paid_tier/README-paid.md`。计费由 Stripe 平台处理。

```bash
# Set up Stripe integration (uses ipeaky to store its own key!)
bash {baseDir}/paid_tier/stripe-setup.sh

# Create a checkout session
bash {baseDir}/paid_tier/stripe-checkout.sh --price price_XXXXX --mode subscription
```

## 安全保障措施：
- 密钥的传输路径为：安全弹窗 → 标准输出（stdout）→ `config.patch` → `openclaw.json`（绝不通过聊天记录传输）。
- 所有技能均可通过 OpenClaw 的原生环境变量自动获取密钥。
- 无需管理单独的凭证文件。
- 无需手动执行 `source` 命令。
- `config.patch` 会触发代理重新加载，确保密钥配置立即生效。