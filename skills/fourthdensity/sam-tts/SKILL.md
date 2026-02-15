---
name: sam-tts
description: 使用 SAM（Software Automatic Mouth）——这款经典的 C64 文本转语音合成器——来生成复古风格的机器人语音音频。可以通过执行 `/sam` 命令来生成语音消息。该工具支持开启/关闭语音生成的功能（/sam on/off），所有生成的回复都会使用 SAM 机器人特有的语音风格。同时，还提供了调整音高、语速、说话方式（mouth）和喉咙音效（throat）等参数的功能，以便对语音进行个性化定制。
homepage: https://github.com/discordier/sam
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "npm-install",
              "kind": "node",
              "package": "sam-js",
              "bins": ["node"],
              "label": "Install SAM dependencies (npm install)",
            },
          ],
      },
  }
---

# SAM TTS – 软件自动语音系统

使用经典的SAM文本转语音引擎生成WAV音频文件，该引擎源自Commodore 64时代的标志性机器人语音。

## 系统要求

- Node.js 18及以上版本
- 在技能目录中运行`npm install`以安装所需依赖项

## SAM模式切换

**状态文件：**`memory/sam-mode.json`

### `/sam on` – 启用SAM模式
启用SAM模式后，所有文本回复都将转换为SAM机器人语音。

**实现方式：**
1. 在`memory/sam-mode.json`中设置`enabled: true`
2. 通过语音消息确认：“SAM模式已启用。我现在将用机器人语音回答。”

### `/sam off` – 关闭SAM模式
恢复正常的文本对话模式。

**实现方式：**
1. 在`memory/sam-mode.json`中设置`enabled: false`
2. 通过文本消息确认：“SAM模式已关闭。返回文本对话。”

### 检查当前模式
在会话开始时读取`memory/sam-mode.json`以获取当前模式。

## 回复行为

### SAM模式开启时：
1. 如常生成回复文本
2. 使用`node scripts/sam-tts-wrapper.js "response" --output=/tmp/sam-XXX.wav --quiet`将其转换为SAM语音
3. 将生成的WAV文件作为音频输出
4. 如有必要，可添加简短的文字说明

### SAM模式关闭时：
以普通文本形式回复

## 聊天命令

### `/sam <text>`
使用SAM语音系统生成一次性的语音消息（无论SAM模式是否启用均有效）。

**实现方式：**
1. 提取`/sam`后的文本
2. 生成WAV文件：`node scripts/sam-tts-wrapper.js "text" --output=/tmp/sam-XXX.wav --quiet`
3. 将生成的WAV文件作为音频输出

### `/sam on`
为所有回复启用SAM模式。

### `/sam off`
关闭SAM模式。

### `/sam status`
报告当前的SAM模式状态（以文本形式）

## 语音参数

所有参数的取值范围为0-255。默认值存储在`memory/sam-mode.json`中：

| 参数 | 默认值 | 效果 |
|-----------|---------|--------|
| `pitch`   | 64      | 语音音高（数值越高，音调越高） |
| `speed`   | 72      | 语速（数值越低，语速越快） |
| `mouth`   | 128     | 嘴腔大小（影响共鸣） |
| `throat`  | 128     | 喉咙大小（影响音色） |

### `/sam pitch <数字>`
设置音高参数（0-255）。

### `/sam speed <数字>`
设置语速参数（1-255，数值越低，语速越快）。

### `/sam mouth <数字>`
设置口腔参数（0-255）。

### `/sam throat <数字>`
设置喉咙参数（0-255）。

## 脚本

### `scripts/sam-tts-wrapper.js`
主要封装脚本，用于生成自动化所需的JSON元数据。

```bash
node scripts/sam-tts-wrapper.js "Hello world" --output=/tmp/out.wav --quiet
node scripts/sam-tts-wrapper.js "Hello world" --output=/tmp/out.wav --quiet --pitch=80 --speed=60
```

**选项：**
- `--output=路径`（必需） - 输出WAV文件的路径
- `--quiet` - 抑制调试输出，仅输出JSON
- `--pitch=数值`, `--speed=数值`, `--mouth=数值`, `--throat=数值` - 语音参数
- `--phonetic` - 输入为音标表示

**输出格式：**
```json
{"success":true,"outputPath":"/tmp/sam.wav","duration":1.44,"size":31741}
```

### `scripts/sam-tts.js`
独立的命令行工具，输出人类可读的文本。

```bash
node scripts/sam-tts.js "Hello world" output.wav --pitch=80 --speed=60
```

## 状态管理

### 文件：`memory/sam-mode.json`
```json
{
  "enabled": false,
  "pitch": 64,
  "speed": 72,
  "mouth": 128,
  "throat": 128
}
```

在会话开始时读取该文件。当用户切换模式或更改参数时更新文件。如果该文件不存在，系统会自动创建`memory/`目录。

## 示例

### 启用SAM模式
用户：`/sam on`
机器人：[语音：“SAM模式已启用。我现在将用机器人语音回答。”]

### 在SAM模式下进行普通对话
用户：“天气怎么样？”
机器人：[语音：“当前温度为72度，天空有部分云层。”]

### 关闭SAM模式
用户：`/sam off`
机器人：SAM模式已关闭。返回文本对话。

### 即时语音回复（即使模式关闭）
用户：`/sam 你好`
机器人：[语音：“你好”]

### 自定义语音参数
用户：`/sam pitch 100`
机器人：音高设置为100。

用户：`/sam Testing higher pitch`
机器人：[语音（音高为100）：“测试更高音调”]

## 音标表示

为了准确发音，请使用`--phonetic`选项：

- 元音：`IY`（bee），`IH`（bit），`EY`（bay），`AE`（bat），`AA`（father），`AH`（bought），`AO`（hot），`OW`（boat），`UH`（book），`UW`（boot），`ER`（bird），`AX`（about）
- 数字1-8表示重音位置：`HEH4LOW`（强调第二个音节）

详细音标表请参阅`references/phonemes.md`。

## 输出格式

- **格式**：WAV（RIFF/WAVE PCM）
- **采样率**：22050 Hz
- **位深度**：8位
- **声道**：单声道

## 目录结构

```
sam-tts/
+-- SKILL.md
+-- package.json
+-- scripts/
|   +-- sam-tts-wrapper.js
|   +-- sam-tts.js
+-- references/
|   +-- phonemes.md
+-- memory/
    +-- sam-mode.json
```

## 平台集成

该技能默认输出WAV格式。某些消息平台可能需要其他音频格式。

### 格式转换（可选）

**警告：** 在安装ffmpeg或任何转换工具之前，机器人必须先征求用户的同意。切勿自动安装依赖项。

示例提示：
> “此平台需要OGG/OPUS格式。我需要安装ffmpeg来进行音频转换。您是否同意继续安装？”

只有在用户明确同意后才能进行安装。

### Telegram / WhatsApp（OGG/OPUS）
```bash
ffmpeg -i input.wav -c:a libopus -b:a 24k output.ogg
```

### Discord（MP3/OGG）
```bash
ffmpeg -i input.wav -c:a libmp3lame -b:a 64k output.mp3
```

### Web / 直接播放
WAV格式可以直接使用，无需转换。

**注意：** 机器人应检测目标平台并根据需要处理格式转换，但任何新的依赖项安装都必须获得用户的同意。

## 致谢

**技能开发者：** [fourthdensity](https://github.com/fourthdensity)

**依赖项：** [sam-js](https://github.com/discordier/sam)（由discordier开发）
- 用于TTS合成的npm包（基于JavaScript/Node.js）

**技术起源：** sam-js基于以下社区的早期版本开发：
- [SAM by Stefan Macke](https://github.com/s-macke/SAM)（C语言实现）
- [SAM by Vidar Hokstad](https://github.com/vidarh/SAM)（重构版本）
- [SAM by 8BitPimp](https://github.com/8BitPimp/SAM)（进一步重构版本）

原始的SAM软件（Software Automatic Mouth）版权归Don't Ask Software所有（现为SoftVoice, Inc.）

**许可说明：** 原始SAM软件被视为废弃软件。此JavaScript版本按原样提供。有关完整许可信息，请参阅sam-js仓库。