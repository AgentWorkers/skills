---
name: pi-speaker
description: 在 Raspberry Pi（或网关主机）的默认扬声器上播放文本转语音（TTS）或音频文件。适用于用户请求发布公告、设置闹钟、播放新闻摘要，或者要求“在 Pi 的扬声器上播放某段内容”的场景，前提是网关运行在基于 Raspberry Pi 的系统上（或具有本地音频播放功能的系统中）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔊",
        "requires": { "anyBins": ["paplay", "pw-play"] },
      },
  }
---
# Pi 扬声器（本地音频输出）

在 **网关主机的默认音频输出设备** 上播放文本转语音（TTS）内容或音频文件。典型应用场景：将 OpenClaw 网关安装在 Raspberry Pi 上，并将蓝牙扬声器设置为默认的音频输出设备；用户可以请求播放公告、警报或新闻摘要，并通过该扬声器收听这些内容。

## 使用场景

- 用户请求“在 Pi 扬声器上播放某内容”、“播放某条公告”、“在……时间用某条消息触发警报”，或“播放新闻摘要”。

- 网关运行在 Raspberry Pi（或其他支持本地音频输出的宿主机）上，并且已设置了默认的音频输出设备（例如蓝牙扬声器）。具体设置方法请参考 [Raspberry Pi 音频设置](/platforms/raspberry-pi-audio)。

## 快速操作步骤（仅需两次工具调用）

**没有** `openclaw skill pi-speaker` 这样的 CLI 命令。需要依次使用 `tts` 和 `exec` 工具来完成操作：

1. 使用 `tts` 工具输入要播放的文本。请确保文本简短（建议不超过一句话），以避免 TTS 生成过程过长或导致请求超时。
2. 从 `tts` 的执行结果中获取音频文件的路径（例如 `details.audioPath` 或类似 `MEDIA:/path/to/file` 的内容）。去掉 `MEDIA:` 前缀，以获取主机上的实际文件路径。
3. 使用 `exec` 工具执行以下命令之一：`pw-play <path>`、`paplay <path>` 或 `$HOME/bin/openclaw-speaker-play.sh <path>`。请注意，不要自行创建类似 `openclaw skill pi-speaker --text "..."` 的自定义命令，因为这样的命令并不存在。

只有在 `exec` 命令成功执行（返回退出码 0）后，才能向用户确认音频已成功播放。

## 具体操作步骤

与上述快速操作步骤相同：首先使用 `tts` 生成音频文件，然后使用 `pw-play <path>`、`paplay <path>` 或 `$HOME/bin/openclaw-speaker-play.sh <path>` 命令进行播放。**务必执行 `exec` 步骤**；如果 `exec` 失败，请报告错误，不要错误地告知用户音频已播放。

## 注意事项：

- 音频文件是在网关主机上生成的，因此播放也必须在同一主机上进行（使用无沙箱限制的 bash 工具或具有相应权限的命令）。
- 如果播放失败，请检查以下内容：是否已正确设置了默认的音频输出设备（例如使用 `pactl info` 或 `wpctl status` 命令确认），网关是否以具有音频播放权限的用户身份运行，以及蓝牙扬声器是否已连接。
- 使用 `tts` 生成音频文件后，**必须** 使用相应的 bash 工具（如 `pw-play` 或 `$HOME/bin/openclaw-speaker-play.sh`）在主机上播放该文件。不要将音频直接发送给用户。
- 在实际执行 `pw-play`（或相关脚本）并收到成功结果之前，不要向用户确认音频已播放。
- **示例**：当 `tts` 命令返回文件路径 `/tmp/openclaw/tts-9vdLan/voice-1772897021460.mp3` 时，使用 `pw-play /tmp/openclaw/tts-9vdLan/voice-1772897021460.mp3` 命令在主机上播放该文件。