# Discord语音备忘录升级 - 技能文档

## 概述

此技能为Moltbot提供了一个核心补丁，用于修复语音备忘录的TTS自动回复问题。该问题是由于块流（block streaming）机制导致最终数据未能传递到TTS合成流程中而引起的。

## 类型

**核心补丁 / 文档**

这不是一个扩展功能的传统插件，而是一个包含核心Clawdbot修改补丁文件的文档包。

## 使用场景

如果您遇到以下情况，请使用此补丁：
- 语音备忘录无法触发TTS响应
- TTS对文本消息有效，但对音频消息无效
- TTS自动模式设置为“inbound”时无法正常工作

## 安装方法

### 方法1：手动补丁（推荐用于开发环境）

```bash
# 1. Locate your clawdbot installation
CLAWDBOT_PATH=$(which clawdbot)
CLAWDBOT_DIR=$(dirname $(dirname $CLAWDBOT_PATH))

# 2. Backup original files
cp $CLAWDBOT_DIR/lib/node_modules/clawdbot/dist/auto-reply/reply/dispatch-from-config.js \
   $CLAWDBOT_DIR/lib/node_modules/clawdbot/dist/auto-reply/reply/dispatch-from-config.js.backup

cp $CLAWDBOT_DIR/lib/node_modules/clawdbot/dist/tts/tts.js \
   $CLAWDBOT_DIR/lib/node_modules/clawdbot/dist/tts/tts.js.backup

# 3. Apply patch
cp patch/dispatch-from-config.js $CLAWDBOT_DIR/lib/node_modules/clawdbot/dist/auto-reply/reply/
cp patch/tts.js $CLAWDBOT_DIR/lib/node_modules/clawdbot/dist/tts/

# 4. Restart clawdbot
clawdbot restart
```

### 方法2：等待上游更新

如果此补丁被纳入Clawdbot的核心代码中，您可以简单地执行以下操作进行更新：
```bash
npm install -g clawdbot@latest
```

## 配置

除了现有的TTS设置外，无需额外配置。请确保您已正确配置以下内容：
```json
{
  "messages": {
    "tts": {
      "auto": "inbound",  // or "always"
      "provider": "openai",  // or "elevenlabs" or "edge"
      "elevenlabs": {
        "apiKey": "your-key-here"
      }
    }
  }
}
```

## 测试方法

1. 将TTS设置为自动模式“inbound”。
2. 向机器人发送一条语音备忘录。
3. 查看日志以获取调试信息：
   ```
   [TTS-DEBUG] inboundAudio=true ttsAutoResolved=inbound ttsWillFire=true
   [TTS-APPLY] PASSED all checks, proceeding to textToSpeech
   [TTS-SPEECH] ...
   ```
4. 确认机器人能够以音频形式进行回复。

## 调试日志

该补丁包含详细的调试日志。您可以通过以下方式查看日志：
```bash
# Logs will show in your clawdbot console
clawdbot gateway start
```

请关注以下日志信息：
- `[TTS-DEBUG]`：显示TTS检测逻辑
- `[TTS-APPLY]`：显示TTS数据包处理过程
- `[TTS-SPEECH]`：显示TTS合成尝试

## 生产环境部署

**重要提示**：在部署到生产环境之前，请考虑以下事项：
1. **移除调试日志**：应删除`console.log`语句或将其设置为可配置选项。
2. **彻底测试**：确保语音备忘录功能正常工作。
3. **监控性能**：禁用块流机制可能会影响数据流的行为。

要移除调试日志，请编辑被修改的文件，并删除以下行：
- `console.log('[TTS-DEBUG']`
- `console.log('[TTS-APPLY']`
- `console.log('[TTS-SPEECH']`

## 回滚补丁

如果您需要恢复到补丁应用前的状态，请执行以下操作：
```bash
# Restore backups
CLAWDBOT_PATH=$(which clawdbot)
CLAWDBOT_DIR=$(dirname $(dirname $CLAWDBOT_PATH))

cp $CLAWDBOT_DIR/lib/node_modules/clawdbot/dist/auto-reply/reply/dispatch-from-config.js.backup \
   $CLAWDBOT_DIR/lib/node_modules/clawdbot/dist/auto-reply/reply/dispatch-from-config.js

cp $CLAWDBOT_DIR/lib/node_modules/clawdbot/dist/tts/tts.js.backup \
   $CLAWDBOT_DIR/lib/node_modules/clawdbot/dist/tts/tts.js

clawdbot restart
```

## 技术细节

### 问题根源

块流机制用于在文本生成过程中逐步向用户发送数据。然而，TTS默认会处理“最终”数据包。当启用块流时：
1. 文本片段作为“block”数据包发送。
2. 最终组装好的文本作为“final”数据包发送。
3. 但由于块流机制的存在，最终数据包（已发送的文本）会被忽略。
4. 因为TTS仅处理“final”数据包，所以无法触发TTS响应。

### 解决方案

该补丁添加了检测逻辑，以确定何时应触发TTS：
- 收到的消息包含音频附件（`isInboundAudioContext()`）。
- TTS自动模式设置为“inbound”或“always”。
- 配置了有效的TTS提供商和API密钥。

当满足这些条件时，系统会暂时禁用块流机制，确保最终数据包能够成功传递到TTS合成流程。

### 代码流程

```
dispatchReplyFromConfig()
  ├─ isInboundAudioContext(ctx) → detects audio
  ├─ resolveSessionTtsAuto(ctx, cfg) → gets TTS settings
  ├─ ttsWillFire = conditions met?
  └─ getReplyFromConfig({ disableBlockStreaming: ttsWillFire })
       └─ maybeApplyTtsToPayload() receives final payload
            └─ textToSpeech() synthesizes audio
```

## 兼容性

- **Clawdbot**：1.0.0及以上版本
- **Node.js**：18及以上版本
- **支持平台**：所有Clawdbot支持的平台

## 已知问题

- 调试日志信息量较大（在生产环境中应予以移除）。
- 该补丁会修改编译后的dist文件（而非源代码）。
- 在Clawdbot更新后可能需要重新应用此补丁。

## 贡献方式

若要改进此补丁，请：
1. 使用不同的TTS提供商（如OpenAI、ElevenLabs、Edge）进行测试。
2. 测试不同的自动模式（“always”、“inbound”、“tagged”）。
3. 提出减少调试日志开销的优化方案。
4. 建议将此补丁集成到Clawdbot的源代码中。

## 支持与帮助

如果您遇到问题，请：
1. 查看日志中的`[TTS-DEBUG]`输出信息。
2. 确认TTS配置是否正确。
3. 检查API密钥是否有效。
4. 确认块流机制已被正确禁用（日志中应显示`disableBlockStreaming: true`）。

## 许可证

此补丁的许可证与Moltbot相同。