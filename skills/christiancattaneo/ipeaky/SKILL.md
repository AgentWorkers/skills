---
name: ipeaky
version: "3.0.0"
description: OpenClaw的安全API密钥管理功能：允许用户存储、查看、测试和删除API密钥，同时确保这些密钥不会被记录在聊天历史中。API密钥通过 `gateway config.patch` 直接存储在 `openclaw.json` 文件中，实现了与OpenClaw系统的完全集成。当用户需要提供、管理或测试API密钥时（例如，与OpenAI、ElevenLabs、Anthropic、Brave等服务交互时），该功能可提供便利。系统会自动响应诸如“添加API密钥”、“保存我的密钥”、“管理密钥”、“测试我的密钥”或“设置API密钥”等指令；此外，当某个技能需要使用尚未配置的API密钥时，系统也会触发相应的操作。
metadata:
  openclaw:
    version: "3.0.0"
    platforms: [macos]
    requires:
      bins: [osascript, python3]
    notes: "Secure input popup requires macOS (osascript). python3 required for zero-exposure config write."
---
# ipeaky — 安全的API密钥管理

密钥直接存储在OpenClaw的本地配置文件（`openclaw.json`）中，通过`gateway config.patch`进行更新。这意味着所有声明了`primaryEnv`的技能都会自动获取到该密钥，无需任何手动配置。

## 密钥映射 — 服务与配置路径的对应关系

| 服务 | 配置路径 | primaryEnv |
|---------|------------|------------|
| OpenAI | `skills.entries.openai-whisper-api.apiKey` | OPENAI_API_KEY |
| ElevenLabs | `skills.entries.sag.apiKey` | ELEVENLABS_API_KEY |
| Brave Search | `tools.web.search.apiKey` | BRAVE_API_KEY |
| Gemini | `skills.entries.nano-banana-pro.apiKey` | GEMINI_API_KEY |
| Google Places | `skills.entries.goplaces.apiKey` | GOOGLE_PLACES_API_KEY |
| Notion | `skills.entries.notion.apiKey` | NOTION_API_KEY |
| ElevenLabs Talk | `talk.apiKey` | （直接从配置文件中获取） |
| 自定义技能 | `skills.entries.<技能名称>.apiKey` | （根据具体技能定义） |
| 自定义环境变量 | `skills.entries.<技能名称>.env.<变量名称>` | （可自定义） |

**注意：**某些密钥被多个服务共享。例如，OpenAI密钥同时被`openai-whisper-api`和`openai-image-gen`等技能使用；ElevenLabs密钥被`sag`和`talk`服务使用。在存储密钥时，请确保设置所有相关的配置路径。

## 存储密钥（版本3 — 完全保密）

**使用版本3的脚本进行操作。**代理程序永远不会看到密钥的实际内容。该脚本负责处理密钥的输入和存储过程。

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

该脚本的步骤如下：
1. 在macOS系统中显示一个隐藏的输入框用于输入密钥。
2. 通过Python将密钥直接写入`openclaw.json`文件（不会通过`ps aux`等命令显示密钥内容）。
3. 重启代理程序。
4. 只返回“OK”或“ERROR”作为响应；密钥不会出现在代理程序的输出或聊天记录中。

### 旧版本的方法（版本2 — 代理程序会看到密钥，不推荐使用）

**步骤1：** 在macOS系统中打开安全输入框。
**步骤2：** 获取密钥值后，通过`gateway config.patch`将其存储到配置文件中。

**OpenAI的示例：** ```
gateway config.patch with raw: {"skills":{"entries":{"openai-whisper-api":{"apiKey":"THE_KEY"},"openai-image-gen":{"apiKey":"THE_KEY"}}}}
```

**ElevenLabs的示例：** ```
gateway config.patch with raw: {"skills":{"entries":{"sag":{"apiKey":"THE_KEY"}}},"talk":{"apiKey":"THE_KEY"}}
```

**Brave Search的示例：** ```
gateway config.patch with raw: {"tools":{"web":{"search":{"apiKey":"THE_KEY"}}}}
```

**重要规则：**
- 绝不要在聊天消息或工具调用参数中显示密钥值。
- 绝不要在`config.patch`的`reason`字段中包含密钥值。
- 如果用户直接在聊天中输入密钥，请立即将其存储并提示用户删除该消息。
- `secure_input_mac.sh`脚本会将密钥输出到标准输出（stdout），请将其捕获到一个变量中并用于`config.patch`，切勿将其记录到日志中。

## 查看密钥信息

可以使用`gateway config.get`从配置文件中读取密钥信息。仅显示密钥的前4个字符以及被屏蔽后的部分内容。解析配置文件中的JSON数据，找到所有`apiKey`字段，并显示它们的配置路径和屏蔽后的密钥值。

## 测试密钥的有效性

- **OpenAI**：`curl -s -H "Authorization: Bearer $KEY" https://api.openai.com/v1/models | head`
- **ElevenLabs**：`curl -s -H "xi-api-key: $KEY" https://api.elevenlabs.io/v1/user`
- **Anthropic**：`curl -s -H "x-api-key: $KEY" -H "anthropic-version: 2023-06-01" https://api.anthropic.com/v1/messages -d '{"model":"claude-3-haiku-20240307","max_tokens":1,"messages":[{"role":"user","content":"hi"}]}'`
- **Brave Search**：`curl -s -H "X-Subscription-Token: $KEY" "https://api.search.brave.com/res/v1/web/search?q=test&count=1"`

请从配置文件中获取密钥值（通过`gateway config.get`），进行测试并报告结果。切勿直接显示密钥内容。

## 删除密钥

使用`gateway config.patch`将密钥值设置为空字符串或从配置文件中删除该密钥条目。

## 安全保障措施：
- 密钥的传输路径为：安全输入框 → 标准输出（stdout） → `config.patch` → `openclaw.json`（绝不会通过聊天渠道传递）。
- 所有技能都可以通过OpenClaw的本地环境变量自动获取到密钥。
- 无需单独管理凭证文件。
- 无需手动执行`source`命令。
- `config.patch`会触发代理程序的重新加载，从而使密钥配置立即生效。