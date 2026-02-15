---
name: clonev
description: 使用 Coqui XTTS v2 克隆任何声音并生成语音，超级简单！只需提供一段 6-30 秒的 WAV 格式语音样本以及相应的文本，即可获得克隆后的语音文件。该工具支持 14 种以上语言。适用于以下场景：  
1. 克隆自己的声音或他人的声音；  
2. 生成听起来像特定人物的语音；  
3. 创建个性化语音消息；  
4. 多语言语音克隆（使用克隆后的声音说任何语言）。
---

# CloneV 技能——轻松实现语音克隆

## ⚠️ 适用于 AI 模型的重要说明

**请勿** 直接使用 Docker 容器。
**请勿** 尝试与 `coqui-xtts` 容器交互——该容器已损坏，正在重启中。
**请勿** 使用任何 API 或服务器。

**仅使用脚本：`scripts/clonev.sh`**

该脚本会自动完成所有操作。只需提供文本、语音样本和语言代码即可。

---

## 该技能的功能

可以从一段简短的音频样本中克隆任何声音，并生成新的语音。

**输入**：
- 需要朗读的文本
- 语音样本（WAV 文件，时长 6-30 秒）
- 语言代码

**输出**：生成的 OGG 音频文件（使用该声音朗读文本）

**支持的语言**：任何语言！可以是您自己的声音、名人的声音，也可以是虚构角色的声音等。

---

## 需要执行的唯一命令

```bash
$(scripts/clonev.sh "Your text here" /path/to/voice_sample.wav language)
```

仅此而已，无需其他操作。

---

## 分步使用方法（适用于 AI 模型）

### 第一步：获取所需输入
- 需要朗读的文本（由用户提供）
- 语音样本的 WAV 文件路径（由用户提供）
- 语言代码（由用户提供，默认为 `en`）

### 第二步：运行脚本
```bash
VOICE_FILE=$(scripts/clonev.sh "TEXT_HERE" "/path/to/sample.wav" LANGUAGE)
```

### 第三步：使用输出结果
变量 `$VOICE_FILE` 中存储了生成的 OGG 文件的路径。

---

## 完整的使用示例

### 示例 1：克隆声音并发送到 Telegram
```bash
# Generate cloned voice
VOICE=$(/home/bernie/clawd/skills/clonev/scripts/clonev.sh "Hello, this is my cloned voice!" "/mnt/c/TEMP/Recording 25.wav" en)

# Send to Telegram (as voice message)
message action=send channel=telegram asVoice=true filePath="$VOICE"
```

### 示例 2：克隆捷克语语音
```bash
# Generate Czech voice
VOICE=$(/home/bernie/clawd/skills/clonev/scripts/clonev.sh "Ahoj, tohle je můj hlas" "/mnt/c/TEMP/Recording 25.wav" cs)

# Send
message action=send channel=telegram asVoice=true filePath="$VOICE"
```

### 示例 3：包含检查步骤的完整工作流程
```bash
#!/bin/bash

# Generate voice
VOICE=$(/home/bernie/clawd/skills/clonev/scripts/clonev.sh "Task completed!" "/path/to/sample.wav" en)

# Verify file was created
if [ -f "$VOICE" ]; then
    echo "Success! Voice file: $VOICE"
    ls -lh "$VOICE"
else
    echo "Error: Voice file not created"
fi
```

---

## 常见语言代码

| 代码 | 语言 | 使用示例 |
|------|----------|---------------|
| `en` | 英语 | `scripts/clonev.sh "Hello" sample.wav en` |
| `cs` | 捷克语 | `scripts/clonev.sh "Ahoj" sample.wav cs` |
| `de` | 德语 | `scripts/clonev.sh "Hallo" sample.wav de` |
| `fr` | 法语 | `scripts/clonev.sh "Bonjour" sample.wav fr` |
| `es` | 西班牙语 | `scripts/clonev.sh "Hola" sample.wav es` |

完整语言代码列表：en, cs, de, fr, es, it, pl, pt, tr, ru, nl, ar, zh, ja, hu, ko

---

## 语音样本要求

- **格式**：WAV 文件
- **时长**：6-30 秒（最佳时长：10-15 秒）
- **质量**：音频清晰，无背景噪音
- **内容**：任何语音内容均可（具体词汇无关紧要）

**优质样本**：
- ✅ 说话清晰的语音录音
- ✅ 背景中无音乐或噪音
- ✅ 音量均匀

**不合格的样本**：
- ❌ 含有音乐或背景噪音
- ❌ 时长过短（< 6 秒）或过长（> 30 秒）

---

## ⚠️ 重要提示

### 模型下载
- 首次使用时会下载约 1.87GB 的模型文件（仅下载一次）
- 模型存储位置：`/mnt/c/TEMP/Docker-containers/coqui-tts/models-xtts/`
- 状态：✅ 已成功下载

### 处理时间
- 处理时间约为 20-40 秒，具体取决于文本长度
- 这属于正常现象——语音克隆属于计算密集型操作

---

## 常见问题及解决方法

### “命令未找到”
请确保您位于技能对应的目录中，或使用完整路径：
```bash
/home/bernie/clawd/skills/clonev/scripts/clonev.sh "text" sample.wav en
```

### “语音样本未找到”
- 检查 WAV 文件的路径是否正确
- 使用绝对路径（以 `/` 开头）
- 确保文件存在：`ls -la /path/to/sample.wav`

### “模型未找到”
模型应会自动下载。如果未下载，请尝试以下操作：
```bash
cd /mnt/c/TEMP/Docker-containers/coqui-tts
docker run --rm --entrypoint "" \
  -v $(pwd)/models-xtts:/root/.local/share/tts \
  ghcr.io/coqui-ai/tts:latest \
  python3 -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

### 语音质量不佳
- 使用更清晰的语音样本
- 确保背景无噪音
- 尝试使用其他语音样本（某些语音的克隆效果更好）

---

## 快速参考卡（适用于 AI 模型）

```
USER: "Clone my voice and say 'hello'"
→ Get: sample path, text="hello", language="en"
→ Run: VOICE=$(/home/bernie/clawd/skills/clonev/scripts/clonev.sh "hello" "/path/to/sample.wav" en)
→ Result: $VOICE contains path to OGG file
→ Send: message action=send channel=telegram asVoice=true filePath="$VOICE"
```

```
USER: "Make me speak Czech"
→ Get: sample path, text="Ahoj", language="cs"  
→ Run: VOICE=$(/home/bernie/clawd/skills/clonev/scripts/clonev.sh "Ahoj" "/path/to/sample.wav" cs)
→ Send: message action=send channel=telegram asVoice=true filePath="$VOICE"
```

---

## 输出文件路径

生成的文件保存在：
```
/mnt/c/TEMP/Docker-containers/coqui-tts/output/clonev_output.ogg
```

脚本会返回该路径，您可以直接使用该路径。

---

## 总结

1. **仅使用脚本：`scripts/clonev.sh`**
2. **切勿** 直接使用 Docker 容器
3. **切勿** 与 `coqui-xtts` 容器交互
4. 脚本会自动完成所有操作
5. 返回可供发送的 OGG 文件路径

**非常简单。只需使用脚本即可。**

---

*克隆任何声音，说出任何语言。只需使用这个脚本即可。*