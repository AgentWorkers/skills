---
name: ipeaky
description: OpenClaw的安全API密钥管理功能：允许用户存储、查看、测试和删除API密钥，同时确保这些密钥不会被记录在聊天历史中。密钥通过 `gateway config.patch` 直接存储在 `openclaw.json` 文件中，实现了与系统的完全原生集成。当用户需要提供、管理或测试API密钥（例如来自OpenAI、ElevenLabs、Anthropic、Brave等服务的密钥）时，该功能可发挥作用。系统会响应诸如“添加API密钥”、“保存我的密钥”、“管理密钥”、“测试我的密钥”或“设置API密钥”等指令；此外，当某个技能需要使用尚未配置的API密钥时，该功能也会自动触发。
metadata:
  openclaw:
    platforms: [macos]
    requires:
      bins: [osascript]
    notes: "Secure input popup requires macOS (osascript). Linux/Windows users can pipe keys via stdin directly."
---

# ipeaky — 安全的API密钥管理

密钥直接存储在OpenClaw的本地配置文件（`openclaw.json`）中，通过`gateway config.patch`进行更新。这意味着任何声明了`primaryEnv`的技能都会自动获取到该密钥，无需任何手动配置。

## 密钥映射 — 服务与配置路径的对应关系

| 服务 | 配置路径 | primaryEnv |
|---------|------------|------------|
| OpenAI | `skills.entries.openai-whisper-api.apiKey` | OPENAI_API_KEY |
| ElevenLabs | `skills.entries.sag.apiKey` | ELEVENLABS_API_KEY |
| Brave Search | `tools.web.search.apiKey` | BRAVE_API_KEY |
| Gemini | `skills.entries.nano-banana-pro.apiKey` | GEMINI_API_KEY |
| Google Places | `skills.entries.goplaces.apiKey` | GOOGLE_PLACES_API_KEY |
| Notion | `skills.entries.notion.apiKey` | NOTION_API_KEY |
| ElevenLabs Talk | `talk.apiKey` | （直接关联） |
| 自定义技能 | `skills.entries.<技能名称>.apiKey` | （根据具体技能而定） |
| 自定义环境变量 | `skills.entries.<技能名称>.env.<变量名称>` | （可自定义） |

**重要提示：**某些密钥被多个技能共享。例如，OpenAI密钥同时被`openai-whisper-api`和`openai-image-gen`等技能使用；ElevenLabs密钥被`sag`和`talk`技能使用。在存储密钥时，请确保设置所有相关的配置路径。

## 存储密钥

**步骤1：** 打开安全输入弹窗。在macOS系统中，操作如下：
```bash
bash {baseDir}/scripts/secure_input_mac.sh KEY_NAME
```

**步骤2：** 获取密钥值后（该值会输出到脚本的stdout中），通过`gateway config.patch`将其保存到配置文件中。

**OpenAI的示例：**  
```
gateway config.patch with raw: {"skills":{"entries":{"openai-whisper-api":{"apiKey":"THE_KEY"},"openai-image-gen":{"apiKey":"THE_KEY"}}}}
```

**ElevenLabs的示例：**  
```
gateway config.patch with raw: {"skills":{"entries":{"sag":{"apiKey":"THE_KEY"}}},"talk":{"apiKey":"THE_KEY"}}
```

**Brave Search的示例：**  
```
gateway config.patch with raw: {"tools":{"web":{"search":{"apiKey":"THE_KEY"}}}}
```

**关键规则：**
- **严禁**在任何聊天消息或工具调用参数中显示或传递密钥值。
- **严禁**在`gateway config.patch`的`reason`字段中包含密钥值。
- 如果用户直接在聊天中输入密钥，请立即将其存储起来，并提醒他们删除该消息。
- `secure_input_mac.sh`脚本会将密钥输出到stdout中，请将其捕获并用于`gateway config.patch`，切勿将其记录到日志中。

## 查看密钥列表

使用`gateway config.get`从配置文件中读取密钥信息，仅显示经过掩码处理的密钥值（前4个字符及后续字符被替换为“****”）。解析配置文件中的JSON数据，找到所有`apiKey`字段，并显示其配置路径和掩码后的密钥值。

## 测试密钥的有效性

**测试端点：**
- **OpenAI**：`curl -s -H "Authorization: Bearer $KEY" https://api.openai.com/v1/models | head`
- **ElevenLabs**：`curl -s -H "xi-api-key: $KEY" https://api.elevenlabs.io/v1/user`
- **Anthropic**：`curl -s -H "x-api-key: $KEY" -H "anthropic-version: 2023-06-01" https://api.anthropic.com/v1/messages -d '{"model":"claude-3-haiku-20240307","max_tokens":1,"messages":[{"role":"user","content":"hi"}]}'`
- **Brave Search**：`curl -s -H "X-Subscription-Token: $KEY" "https://api.search.brave.com/res/v1/web/search?q=test&count=1"`

**操作流程：**
1. 从配置文件中获取密钥值。
2. 使用该密钥值进行测试。
3. 严禁直接显示密钥内容。

## 删除密钥

使用`gateway config.patch`将密钥值设置为空字符串或删除相应的配置条目。

## 安全保障措施：
- 密钥的传输过程为：安全输入弹窗 → stdout → `gateway config.patch` → `openclaw.json`（绝不会通过聊天渠道传输）。
- 所有技能都能通过OpenClaw的本地环境变量自动获取到密钥。
- 无需单独管理凭证文件。
- 无需手动执行`source`命令。
- `gateway config.patch`会触发配置文件的重新加载，从而使密钥配置立即生效。