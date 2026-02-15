---
name: homeassistant-assist
description: 使用 Assist（对话）API 来控制 Home Assistant 智能家居设备。当用户想要控制智能家居设备（如灯光、开关、恒温器、窗帘、吸尘器、媒体播放器或其他智能设备）时，可以使用此技能。该技能会将自然语言直接传递给 Home Assistant 内置的自然语言处理（NLU）系统，从而实现快速且高效的控制。
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

通过向 Home Assistant 的 Assist（对话）API 传递自然语言指令来控制智能家居设备。**无需额外操作**——只需将请求发送出去，让 Assist 负责解析用户意图、匹配设备实体并执行相应的操作。

## 适用场景

当用户想要**控制或查询任何智能家居设备**时，可以使用此功能。只要该设备被 Home Assistant 支持，Assist 都能完成相应的操作。

## 工作原理

将用户的请求直接传递给 Assist：

```bash
curl -s -X POST "$HASS_SERVER/api/conversation/process" \
  -H "Authorization: Bearer $HASS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "USER REQUEST HERE", "language": "en"}'
```

**完全信任 Assist**。它负责处理以下任务：
- 意图解析
- 模糊实体名称的匹配
- 基于用户所在区域的设备识别
- 命令的执行
- 错误响应的生成

## 响应的处理方式

**直接转发 Assist 的返回结果**。`response.speech.plain.speech` 字段包含了用户可以理解的信息：
- `"灯光已打开"` → 表示操作成功
- `"抱歉，我无法理解您的指令"` → 表示 Assist 无法解析用户的请求
- `"抱歉，有多个设备名为 X"` → 表示设备名称存在重复

**不要过度解读**。如果 Assist 表示操作成功，那就说明操作确实完成了。请相信它的反馈。

## 当 Assist 返回错误时

只有当 Assist 返回错误（`response_type: "error"`）时，才建议对 Home Assistant 的配置进行优化：

| 错误类型 | 建议 |
|---------|--------|
| `no_intent_match` | "Home Assistant 无法识别该命令" |
| `no_valid_targets` | "请检查 Home Assistant 中的设备名称，或为设备添加别名" |
| Multiple devices | "可能存在设备名称重复的情况——建议为设备添加唯一的别名" |

这些只是针对 Home Assistant 配置的优化建议，并非技能本身的问题。因为该技能已经成功将请求传递给了 Assist。

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

生成访问令牌：进入 Home Assistant → 个人资料 → 长期访问令牌 → 创建令牌

## API 参考

### 端点

```
POST /api/conversation/process
```

**注意：** 使用 `/api/conversation/process`，而非 `/api/services/conversation/process`。

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

- **完全信任 Assist**：Assist 对用户 Home Assistant 的配置更加熟悉。
- **简单操作**：只需发送请求并接收响应即可。
- **避免故障排查**：如果出现问题，建议优化 Home Assistant 的配置。
- **保持简洁**：通过一次 API 调用，实现自然语言输入到自然语言输出的交互。

## 相关链接

- [Home Assistant 对话 API 文档](https://developers.home-assistant.io/docs/intent_conversation_api/)