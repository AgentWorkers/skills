---
name: whatsapp-ultimate
version: 3.3.0
description: "WhatsApp技能：具备三重安全验证机制  
该技能使您的智能助手仅在以下条件下才会响应用户的请求：  
1. 用户位于正确的聊天频道中；  
2. 发起请求的用户身份经过验证；  
3. 请求内容符合预设的规则或条件。  
该智能助手仅在被明确唤醒（即用户与其进行对话）时才会执行操作，从而确保了对话的私密性和安全性。"
metadata:
  {
    "openclaw":
      {
        "emoji": "💬",
        "os": ["linux", "darwin"],
        "requires":
          {
            "bins": ["npx", "tsx", "sed", "python3"],
            "channels": ["whatsapp"],
          },
        "patches":
          {
            "description": "Two optional bash scripts patch OpenClaw source files to add (1) self-chat history capture in monitor.ts and (2) model/auth prefix template variables in response-prefix-template.ts, types.ts, reply-prefix.ts, and agent-runner-execution.ts. Both scripts are idempotent (safe to run multiple times) and skip if already applied. Review the scripts before running.",
            "files": ["scripts/apply-history-fix.sh", "scripts/apply-model-prefix.sh"],
            "modifies": ["src/web/inbound/monitor.ts", "src/auto-reply/reply/response-prefix-template.ts", "src/auto-reply/types.ts", "src/channels/reply-prefix.ts", "src/auto-reply/reply/agent-runner-execution.ts"],
            "mechanism": "sed + python3 string replacement with anchor-point matching",
            "reversible": "git checkout on modified files restores originals",
          },
        "notes":
          {
            "security": "PATCHES: Two optional install scripts modify OpenClaw source files using sed and python3 to add history capture and model prefix features. Both are idempotent and skip if already applied. Review scripts/apply-history-fix.sh and scripts/apply-model-prefix.sh before running. ADMIN SCRIPTS: wa-fetch-contacts.ts and wa-create-group.ts connect to WhatsApp via Baileys using existing OpenClaw credentials in ~/.openclaw/credentials/whatsapp/. No new credentials are requested. No external network calls beyond WhatsApp's own WebSocket connection. All operations are local.",
          },
      },
  }
---
# WhatsApp Ultimate

**我们的机器人不会在公司群组中与你的老板调情，也不会主动向你婆婆提供生活建议，更不会用一篇长达400字的文章来解决家庭关于海鲜饭的争论，也不会在凌晨2点对你的伴侣的故事回复“其实……”。**

因为WhatsApp Ultimate遵循三条严格的安全规则：**正确的人 + 正确的聊天对象 + 正确的前缀 = 适当的回应**；其他情况一律保持绝对的沉默。没有“也许会帮忙”这样的回应，也没有“我就稍微帮个忙”的说法。只有冷酷、严格、且恰到好处的沉默。

以下是该机器人的核心功能：

- **每条回复都会显示模型ID**：每条消息都会附带`claude-opus-4-6|sub`这样的标识，确保用户不会将机器人误认为是人类。
- **完整消息历史记录的捕获**：所有对话都会被存储并可供查询，确保信息不会丢失。
- **联系人同步与群组管理**：机器人能自动识别群组中的成员。
- **处理过程中的反馈提示**：在机器人处理消息时会显示相应的提示信息，让用户知道它正在工作。
- **直接使用Baileys API**：没有多余的中间层，响应速度快、体积小且可靠。

三条规则，零尴尬时刻——因为我们就是这么一丝不苟的。

## 全套功能

可以将该机器人与[**jarvis-voice**](https://clawhub.com/globalcaos/jarvis-voice)（用于发送语音消息）和[**ai-humor-ultimate**](https://clawhub.com/globalcaos/ai-humor-ultimate)（用于提升机器人智能）结合使用，它们共同构成了一个包含13项功能的认知架构。

👉 **[克隆它、修改它，让它成为你的专属工具。](https://github.com/globalcaos/clawdbot-moltbot-openclaw)**

---

## 主要功能

### 消息传递与监控
- **模型ID前缀**：每条机器人发送的消息都会显示所使用的模型和认证模式：`🤖(claude-opus-4-6|sub)` 或 `🤖(gpt-4o|api)`，让你随时了解当前运行的模型。
- **完整消息历史记录**：捕获所有消息，包括Baileys可能遗漏的自我对话消息。
- **自我对话模式**：在你的聊天频道中记录所有双向对话。
- **安全机制**：只有经过授权的用户才能与特定的聊天对象进行交流。
- **历史记录同步**：通过设置`syncFullHistory: true`，可以在重新连接时补全所有消息。

### 管理与群组管理
- **联系人同步**：从所有WhatsApp群组中提取联系人信息（包括电话号码、管理员状态等）。
- **群组创建**：可以编程方式创建群组并指定成员。
- **群组管理**：可以重命名群组、更新描述、添加/移除/提升/降级群组成员。
- **直接使用Baileys API**：即使服务暂时不可用，也能正常使用。

## 安装说明
```bash
clawhub install whatsapp-ultimate
```

### ⚠️ 补丁（可选——运行前请阅读）

该技能包含两个**可选的**bash脚本，用于修改OpenClaw的源代码。基础功能（安全机制、管理工具、联系人同步）无需这些脚本也能正常使用。这些补丁的作用如下：
- `apply-history-fix.sh`：捕获Baileys可能遗漏的自我对话消息，修改`monitor.ts`文件。
- `apply-model-prefix.sh`：在每条回复中添加模型/认证信息，修改`response-prefix-template.ts`、`types.ts`、`reply-prefix.ts`、`agent-runner-execution.ts`文件。

**运行前注意事项：**
- 请仔细阅读每个脚本的说明。
- 先执行`git commit`操作，以便后续可以随时回滚更改。
- 这两个脚本都是幂等的（可以多次运行）。
- 如果已经应用了这些补丁，系统会自动跳过这些脚本。

```bash
# Review first, then run:
bash ~/.openclaw/workspace/skills/whatsapp-ultimate/scripts/apply-history-fix.sh
bash ~/.openclaw/workspace/skills/whatsapp-ultimate/scripts/apply-model-prefix.sh
```

**这些补丁会修改的文件及内容：**
| 脚本 | 修改的文件 | 修改内容 |
|--------|---------------|-------------|
| apply-history-fix.sh | `src/web/inbound/monitor.ts` | 添加`insertHistoryMessage()`函数以保存所有收到的消息 |
| apply-model-prefix.sh | `src/`目录下的4个文件 | 添加`{authMode}`和`{authProfile}`模板变量 |

**如需回滚更改：**从OpenClaw仓库根目录执行`git checkout -- src/`。

### 配置文件（openclaw.json）
```json
{
  "channels": {
    "whatsapp": {
      "selfChatMode": true,
      "syncFullHistory": true,
      "responsePrefix": "🤖({model}|{authMode})",
      "dmPolicy": "allowlist",
      "allowFrom": ["+your_number"],
      "triggerPrefix": "jarvis"
    }
  }
}
```

## 模型ID前缀

`responsePrefix`支持以下模板变量：
| 变量 | 例子 | 说明 |
|----------|---------|-------------|
| `{model}` | `claude-opus-4-6` | 模型名称 |
| `{authMode}` | `sub` / `api` | 认证模式：`sub`表示订阅服务，`api`表示使用API密钥 |
| `{provider}` | `anthropic` | 提供商名称 |
| `{auth}` | `sub` | `{authMode`的别名 |
| `{authProfile}` | `anthropic:oauth` | 完整的认证信息ID |
| `{think}` | `low` | 当前的思考状态 |

**前缀示例：**
- `🤖(claude-opus-4-6|sub)`：使用订阅服务的Claude Opus模型。
- `🤖(claude-opus-4-6|api)`：使用API密钥的Claude Opus模型（需要付费）。
- `🤖(gpt-4o|api)`：使用GPT-4o模型。
- `🤖(llama3.2:1b|api)`：使用本地的Ollama模型。

这些前缀有助于用户立即识别：
1. 哪个模型提供了响应。
2. 当前使用的是订阅服务还是API密钥。

## 自我对话历史记录的修复

**问题：**当你从手机发送自我对话消息时，Baileys不会将这些消息记录到历史数据库中。

**解决方案：**补丁在消息处理过程中添加了`insertHistoryMessage()`函数，确保所有消息都被保存。重复的消息会被自动忽略。

**补充说明：**设置`syncFullHistory: true`后，重新连接时系统会补全所有消息。

## 使用方法

```
whatsapp_history(action="search", query="meeting tomorrow")
whatsapp_history(action="search", chat="Oscar", limit=20)
whatsapp_history(action="stats")
```

## 管理工具

### 联系人同步

从所有WhatsApp群组中提取联系人信息：
```bash
npx tsx ~/.openclaw/workspace/skills/whatsapp-ultimate/scripts/wa-fetch-contacts.ts
```

**输出文件：**`~/.openclaw/workspace/bank/whatsapp-contacts-full.json`

文件内容包括：
- 所有群组的成员列表。
- 每个联系人的电话号码（已解析为LID）。
- 每个联系人在各个群组中的成员身份。
- 每个联系人的管理员状态。

### 群组创建

```bash
npx tsx ~/.openclaw/workspace/skills/whatsapp-ultimate/scripts/wa-create-group.ts "Group Name" "+phone1" "+phone2"
```

输出格式为E.164格式的电话号码。创建者会被自动设置为群组管理员，并返回群组的JID。

### Baileys的核心方法

| 方法 | 说明 |
|--------|-------------|
| `groupFetchAllParticipating()` | 获取所有群组及其成员信息。 |
| `groupMetadata(jid)` | 获取单个群组的详细信息。 |
| `groupCreate(name, participants)` | 创建新群组。 |
| `groupUpdateSubject(jid, name)` | 重命名群组。 |
| `groupUpdateDescription(jid, desc)` | 更新群组描述。 |
| `groupParticipantsUpdate(jid, participants, action)` | 添加/移除/提升/降级群组成员。 |

### LID解析

WhatsApp内部使用LID（链接ID）。联系人同步脚本会自动根据`~/.openclaw/credentials/whatsapp/default/lid-mapping-*_reverse.json`中的映射关系，将LID转换为电话号码。

## 更新日志

### 3.0.0版本
- **合并功能：**将`whatsapp-tools`的功能整合到WhatsApp Ultimate中，包括联系人同步、群组创建和管理操作。
- **新增内容：**添加了包含必要字段、通道和安全说明的`metadata.openclaw`块。
- **新增内容：**增加了管理工具部分，包含Baileys API的参考信息和LID解析的文档。

### 2.2.0版本
- **新增功能：**每条消息中都添加了模型和认证模式的前缀（`{model}`、`{authMode}`模板变量）。
- **新增功能：**提供了用于应用模型前缀的安装脚本。
- **新增内容：**完善了模板变量的文档说明。

### 2.1.0版本
- **修复问题：**现在自我对话的消息也会被记录到历史数据库中。
- **新增功能：**添加了用于记录历史数据的安装脚本。
- **新增功能：**添加了`syncFullHistory`配置选项，用于在重新连接时补全所有消息。

### 2.0.3版本
- **首次发布：**包含了安全机制和机器人前缀功能。