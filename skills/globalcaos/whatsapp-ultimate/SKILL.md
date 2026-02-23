---
name: whatsapp-ultimate
version: 3.4.0
description: "WhatsApp技能：具备三重安全验证机制  
该技能中的智能助手仅在以下条件下才会响应用户：  
1. 用户位于正确的聊天频道中；  
2. 与用户对话的是被授权的管理员或客服人员；  
3. 用户使用了正确的身份验证方式（例如：输入正确的密码或验证码）。  
该助手仅会在满足上述三个条件时才进行对话，从而确保用户隐私和系统安全。"
metadata:
  {
    "openclaw":
      {
        "emoji": "💬",
        "os": ["linux", "darwin"],
        "requires": { "bins": ["npx", "tsx", "sed", "python3"], "channels": ["whatsapp"] },
        "patches":
          {
            "description": "Two optional bash scripts patch OpenClaw source files to add (1) self-chat history capture in monitor.ts and (2) model/auth prefix template variables in response-prefix-template.ts, types.ts, reply-prefix.ts, and agent-runner-execution.ts. Both scripts are idempotent (safe to run multiple times) and skip if already applied. Review the scripts before running.",
            "files": ["scripts/apply-history-fix.sh", "scripts/apply-model-prefix.sh"],
            "modifies":
              [
                "src/web/inbound/monitor.ts",
                "src/auto-reply/reply/response-prefix-template.ts",
                "src/auto-reply/types.ts",
                "src/channels/reply-prefix.ts",
                "src/auto-reply/reply/agent-runner-execution.ts",
              ],
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

**我们的智能助手绝不会在公司群组中与你老板调情，也不会主动向你婆婆提供生活建议，更不会用一篇没人要求的400字长文来解决家庭争论，更不会在凌晨2点对你的伴侣的故事回复“其实……”。**  
因为WhatsApp Ultimate遵循三条严格的安全规则：**只有合适的人、合适的聊天对象以及正确的对话前缀，才会得到回应；其他情况，一律保持绝对的沉默。**  

以下是该智能助手的核心功能：  

- **每条回复都会显示模型ID**：每条消息都会附带`claude-opus-4-6|sub`这样的标识，确保用户明白这只是一个机器人，而非真人。  
- **完整消息历史记录**：所有对话都会被保存并可供查询，确保信息不会丢失。  
- **联系人同步与群组管理**：无需人工指导，智能助手就能自动识别群组成员。  
- **实时反馈状态**：输入信息时会有提示信息，让用户知道系统正在处理中。  
- **直接使用Baileys API**：无额外的中间层，响应快速、轻量且可靠。  

## 全套功能  

结合[**jarvis-voice**](https://clawhub.com/globalcaos/jarvis-voice)（用于生成WhatsApp语音消息）和[**ai-humor-ultimate**](https://clawhub.com/globalcaos/ai-humor-ultimate)（用于提升对话趣味性），即可构建一个功能完备的智能助手系统。这两个组件都属于同一个包含13项功能的认知架构中。  

👉 **[克隆它、修改它，让它成为属于你的工具吧。](https://github.com/globalcaos/clawdbot-moltbot-openclaw)**  

---

## 主要特性  

### 消息传递与监控  
- **模型ID前缀**：每条机器人发送的消息都会显示所使用的模型和认证模式（例如`🤖(claude-opus-4-6|sub)`或`🤖(gpt-4o|api)`。  
- **完整消息历史记录**：所有消息（包括Baileys未捕获的私聊消息）都会被保存。  
- **私聊模式**：私聊内容也会被完整记录（在命令频道中）。  
- **安全过滤**：只有授权用户才能与授权的聊天对象进行交流。  
- **历史记录同步**：启用`syncFullHistory`选项后，重新连接时系统会自动补全所有消息。  

### 管理与群组管理  
- **联系人同步**：从所有WhatsApp群组中提取联系人信息（包括电话号码、管理员状态等）。  
- **群组创建**：可编程创建群组并设置成员名单。  
- **群组管理**：可重命名群组、更新描述、添加/删除/提升/降级群组成员。  
- **直接访问Baileys API**：即使Baileys暂时不可用，也能正常使用该功能。  

## 安装说明  
```bash
clawhub install whatsapp-ultimate
```  

### ⚠️ 补丁说明（可选——运行前请阅读）  
该技能包含两个用于修改OpenClaw源代码的bash脚本（可选）。基础功能（安全过滤、管理工具、联系人同步）无需这些脚本也能正常使用。这两个脚本的作用如下：  
- `apply-history-fix.sh`：捕获Baileys未捕获的私聊消息，并修改`monitor.ts`文件。  
- `apply-model-prefix.sh`：在每条回复中添加模型/认证信息，并修改相关模板文件。  

**运行前请注意：**  
- 仔细阅读每个脚本的说明。  
- 先提交你的OpenClaw仓库（以便后续需要时可回滚更改）。  
- 这两个脚本是幂等的（可以多次运行）。  
- 如果已经应用了这些补丁，系统会自动跳过这些脚本。  

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

## 模型ID前缀说明  
`responsePrefix`支持以下模板变量：  
| 变量                | 说明                                      |                                                                                              |  
| ---------------------- | -------------------------------------------------------------------- |                                                                                              |  
| `{model}`            | `claude-opus-4-6`            | 模型名称                                                                                              |  
| `{authMode}`          | `sub`   / `api`          | 认证模式：`sub`表示订阅服务；`api`表示API密钥           |  
| `{provider}`          | `anthropic`            | 提供商名称                                                                                              |  
| `{auth}`            | `sub`            | `{authMode}`的别名                                                                                              |  
| `{authProfile}`        | `anthropic:oauth`        | 完整的认证配置ID                                                                                              |  
| `{think}`            | `low`            | 当前的思考状态                                                                                              |  

**前缀示例：**  
- `🤖(claude-opus-4-6|sub)`：使用订阅服务的Opus模型  
- `🤖(claude-opus-4-6|api)`：使用API密钥的Opus模型  
- `🤖(gpt-4o|api)`：使用GPT-4o模型的备用方案  
- `🤖(llama3.2:1b|api)`：使用本地的Ollama模型  

这些前缀有助于用户立即了解：  
1. 哪个模型提供了响应；  
2. 是否正在消耗订阅服务或API资源。  

### 私聊历史记录修复  
**问题：**用户从手机发送到私聊的消息不会被记录到历史数据库中。  
**解决方案：**补丁在消息处理过程中添加了`insertHistoryMessage()`函数，确保所有消息都被保存。重复的消息会被自动忽略。  
**补充说明：**启用`syncFullHistory`后，重新连接时会自动补全所有消息。  

## 使用方法  

### 管理工具  
### 联人信息同步  
从所有WhatsApp群组中提取联系人信息：  
```bash
npx tsx ~/.openclaw/workspace/skills/whatsapp-ultimate/scripts/wa-fetch-contacts.ts
```  
**输出文件：**`~/.openclaw/workspace/bank/whatsapp-contacts-full.json`  
**内容包含：**所有群组的成员列表、联系人的电话号码（已解析为LID格式）、每个联系人在各群组中的成员身份以及管理员状态。  

### 群组创建  
**输入格式：**电话号码（E.164格式）。创建者会自动被添加为群组管理员，并返回群组的JID。  

### Baileys的核心方法  
| 方法                                      | 说明                                      |                                                                                              |  
| ------------------------------------ | ----------------------------- |                                                                                              |  
| `groupFetchAllParticipating()`            | 获取所有群组及其成员列表            |                                                                                              |  
| `groupMetadata(jid)`                | 获取单个群组的详细信息                |                                                                                              |  
| `groupCreate(name, participants)`           | 创建新群组                              |                                                                                              |  
| `groupUpdateSubject(jid, name)`            | 更改群组名称                              |                                                                                              |  
| `groupUpdateDescription(jid, desc)`            | 更新群组描述                              |                                                                                              |  
| `groupParticipantsUpdate(jid, participants, action)` | 添加/删除/提升/降级群组成员            |                                                                                              |  

### LID解析  
WhatsApp内部使用LID（链接ID）进行识别。联系人同步脚本会根据`~/.openclaw/credentials/whatsapp/default/lid-mapping-*_reverse.json`中的映射关系，自动将LID转换为电话号码。  

## 更新日志  
### 3.4.0版本更新：  
- **改进：**聊天搜索功能现在能识别LID和JID的别名；通过群组名称搜索时，系统会同时查找`@lid`和`@s.whatsapp.net`格式的JID。  
- **新增：**`resolveChatJids()`函数可跨数据库查找聊天记录、联系人和消息记录，以获取指定群组的所有JID别名。  
- **优化：**如果无法解析JID，系统会恢复原有的搜索逻辑，避免功能退化。  

### 3.0.0版本更新：  
- **整合：**将`whatsapp-tools`的功能整合到WhatsApp Ultimate中，包括联系人同步、群组创建和管理操作。  
- **新增：**添加了包含必要配置项的`metadata.openclaw`块。  
- **新增：**添加了管理工具部分，包含Baileys API的参考文档和LID解析说明。  

### 2.2.0版本更新：  
- **新增：**每条消息中都添加了模型和认证模式的前缀（`{model}`、`{authMode}`）。  
- **新增：**提供了用于应用模型前缀的安装脚本。  
- **新增：**完善了模板变量的文档说明。  

### 2.1.0版本更新：  
- **修复：**私聊中的消息现在也会被记录到历史数据库中。  
- **新增：**添加了用于记录历史数据的安装脚本。  
- **新增：**添加了`syncFullHistory`配置选项，用于在重新连接时补全所有消息。  

### 2.0.3版本（ClawHub的首次发布）：  
- 引入了安全过滤机制和机器人消息前缀功能。