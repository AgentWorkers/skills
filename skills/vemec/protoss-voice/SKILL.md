---
name: protoss-voice
description: 将《星际争霸》（StarCraft）中的Protoss族所使用的灵能（psionic）效果应用到任意音频文件上。该效果可用作文本转语音（TTS）或用户录音的后处理环节。
metadata:
  openclaw:
    emoji: "🔮"
    requires:
      bins:
        - ffmpeg
        - sox
    install:
      - id: brew
        kind: brew
        formula: "sox ffmpeg"
        bins:
          - sox
          - ffmpeg
        label: "Install Dependencies (brew)"
---

# Protoss语音效果

该技能使用V9版本的“Massive Void”引擎，对音频文件应用“Khala”灵能转换效果。  
**模块化设计：**该技能本身不生成语音，而是对现有的音频文件进行转换。  

## 使用方法  

只需在任何输入音频文件（如wav、mp3、ogg等）上运行该脚本即可：  

```bash
python3 skills/protoss-voice/protoss_fx.py <path_to_audio_file>
```  

**输出结果：**  
会在同一目录下生成一个后缀为 `_psionic.wav` 的新文件。  

## 特定角色行为（当代理以Protoss角色身份行动时）  

当代理以Protoss角色（例如Selendis、Artanis、Zeratul等）的身份行动时，应执行以下步骤：  
1. **生成/录制基础音频：**  
   * 使用`kokoro-tts`（或其他TTS工具）生成原始语音内容；  
   * 或者接受用户提供的音频录音。  
2. **处理音频文件：**  
   * 对原始音频文件执行`protoss_fx.py`脚本进行转换处理。  
   * *除非进行调试，否则无需在此步骤中添加任何解说内容。*  
3. **交付最终结果：**  
   * 使用`message`工具发送处理后的音频文件（即 `_psionic.wav`）。  
   * 如果原始文件或中间文件是临时生成的，应自动将其删除。  

## 集成示例（以Kokoro为例）  

```bash
# 1. Generate (Raw)
python3 skills/kokoro-tts/speak.py "En Taro Adun." -o raw.wav -v ef_dora

# 2. Transform (Psionic)
python3 skills/protoss-voice/protoss_fx.py raw.wav
# Output: raw_psionic.wav

# 3. Optimize for Transport (Telegram OGG)
ffmpeg -i raw_psionic.wav -c:a libopus -b:a 64k -vbr on final.ogg -y

# 4. Send
message(action="send", media="final.ogg", asVoice=true)
```  

## 所需软件/库：**  
该技能需要`ffmpeg`和`sox`（Sound eXchange）这两个工具的支持。  

```bash
brew install ffmpeg sox
```