---
name: roomsound
description: RoomSound 为你的智能助手提供了播放音频的功能，支持从 YouTube、蓝牙音箱到本地文件等多种音频来源。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["yt-dlp", "mpv", "bluetoothctl"] },
        "install":
          [
            {
              "id": "apt",
              "kind": "apt",
              "packages": ["yt-dlp", "mpv", "bluez", "pulseaudio-utils"],
              "label": "Install required packages (Debian/Ubuntu)",
            },
          ],
      },
  }
---
# RoomSound - 家庭音频控制

RoomSound 是用于控制扬声器和播放音频的执行层。

## 代理角色（Agent Role）

当用户请求播放音频或切换扬声器时，系统会将用户的意图解析为以下命令组：
- 设备发现：`bluetoothctl paired-devices`、`bluetoothctl info <MAC>`、`wpctl status`、`pactl list short sinks`
- 扬声器切换：`bluetoothctl devices Connected`、`bluetoothctl disconnect <MAC>`、`bluetoothctl connect <MAC>`
- YouTube 播放：`mpv --no-video "<url>"` 以及 `yt-dlp` 的搜索/播放命令
- 按队列顺序播放：除非用户明确请求特定的列表或顺序，否则会自动构建一个播放队列

在执行可能影响用户操作的命令（如切换当前使用的扬声器）之前，系统会先进行自然语言确认。

## 首次运行时的代理行为（First-Run Agent Behavior）

首次使用时，系统会确保所有依赖项和扬声器别名都已准备好：
1. 确保已安装所需的二进制文件：`yt-dlp`、`mpv`、`bluetoothctl`（以及元数据中列出的其他音频工具）。
2. 如果缺少某个依赖项，系统会从技能元数据中获取安装命令（使用 `apt`）并执行安装：`yt-dlp mpv bluez pulseaudio-utils`，然后继续运行。
3. 为了确保 `yt-dlp` 的稳定运行，系统会配置其 JavaScript 运行时环境：
   - 运行一次验证：
     `yt-dlp --js-runtimes "node:/usr/bin/nodejs" --print "%(title)s | Uploaded: %(upload_date>%Y-%m-%d)s | https://youtu.be/%(id)s" "ytsearch5:tiesto prismatic"`
   - 将配置信息保存到文件中：
     `mkdir -p ~/.config/yt-dlp && printf '%s\n' '--js-runtimes node:/usr/bin/nodejs' > ~/.config/yt-dlp/config`
4. 通过以下方式检测可用的扬声器：
  - `bluetoothctl paired-devices`
  - `bluetoothctl info <MAC>`
  - `wpctl status` 和/或 `pactl list short sinks`
5. 请求用户为每个检测到的蓝牙设备提供一个友好的别名。
6. 将别名与对应的 MAC 地址映射保存在代理的内存或配置文件中。
7. 以后可以使用这些别名来执行命令（例如：`kitchen` 对应 `11:22:33:44:55:66`）。

如果别名不明确或未知，系统会在切换扬声器之前询问用户以获取更多信息。

## 命令解析规则（Command Resolution Rules）

### 从 YouTube 播放音频
- 如果用户提供了 URL，系统会运行 `mpv --no-video "<url>"`。
- 如果用户提供了搜索文本，系统会执行以下操作：
  - `yt-dlp --print "%(title)s | Duration: %(duration_string)s | Uploaded: %(upload_date>%Y-%m-%d)s | https://youtu.be/%(id)s" "ytsearch5:<query>"`
  - 搜索结果会显示视频标题、时长、上传日期和 URL；在结果不明确的情况下，系统会优先选择最新或用户确认的结果。

### YouTube 播放命令规范（YouTube Playback Command Contract）
- 必需的二进制文件：`yt-dlp` 和 `mpv`。
- 如果缺少某个文件，系统会提示用户安装该文件，并执行相应的安装命令：
  - `Error: yt-dlp not found. Install with: sudo apt install yt-dlp`
  - `Error: mpv not found. Install with: sudo apt install mpv`
- 如果用户提供了一组 URL，系统会使用一个命令将它们按顺序添加到播放队列中：
  - `mpv --no-video "<url1>" "<url2>" "<url3>" ...`
- 如果用户提供了具体的歌曲列表，系统会先解析每个歌曲的元数据，然后按顺序将它们添加到播放队列中：
  - `yt-dlp -f bestaudio -g "ytsearch1:<item1>"` ... `yt-dlp -f bestaudio -g "ytsearch1:<itemN>"`
  - 然后使用 `mpv --no-video "<stream-url1>" "<stream-url2>" ...` 开始播放。
- 如果用户没有提供具体的歌曲列表，系统会根据用户的上下文生成搜索查询：
  - 为每个查询获取元数据（包括时长）：
    - `yt-dlp --print "%(title)s | Duration: %(duration_string)s | Uploaded: %(upload_date>%Y-%m-%d)s | https://youtu.be/%(id)s" "ytsearch1:<query>"`
  - 使用 `yt-dlp -f bestaudio -g "ytsearch1:<query>"` 为每个查询选择合适的播放 URL。
  - 系统会持续添加歌曲，直到播放队列的总时长达到至少 90 分钟（除非用户另有要求）。
- 使用 `mpv --no-video "<stream-url1>" "<stream-url2>" ...` 按队列顺序开始播放。

### 切换扬声器（Switch Speaker）
- 将扬声器别名解析为对应的 MAC 地址。
- 验证 MAC 地址的格式：`^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$`。
- 使用以下步骤进行切换：
  - `bluetoothctl devices Connected`（获取已连接的设备列表）
  - 对于每个非目标设备的 MAC 地址，执行 `bluetoothctl disconnect <MAC>` 命令
  - 接着执行 `bluetoothctl connect <TARGET_MAC>` 命令连接目标设备
- 切换后，如果需要，可以使用 `wpctl set-default <SINK_ID>` 或 `pactl set-default-sink <SINK_NAME>` 设置默认输出设备。

### 列出设备（List Devices）
- 当用户询问“有哪些可用的扬声器？”时，系统会执行以下操作：
  - `bluetoothctl paired-devices`
  - `bluetoothctl info <MAC>`（显示已配对的设备信息）
  - `wpctl status`
  - `pactl list short sinks`
  然后系统会总结设备的连接状态和可用的输出设备。

### 设备发现命令规范（Device Discovery Command Contract）
- 系统会按以下逻辑顺序展示设备信息：
  1. 已配对的蓝牙设备
  2. 每个设备的连接状态
  3. PipeWire 输出设备
  4. PulseAudio 输出设备
- 蓝牙设备的检测使用 `bluetoothctl paired-devices` 命令。
- 对于每个设备，系统会通过 `bluetoothctl info <MAC>` 获取连接状态，并显示“✅ Connected”或“❌ Disconnected”。
- 如果 `bluetoothctl` 命令不存在，系统会提示用户安装 `bluez` 工具。
- PipeWire 设备的检测使用 `wpctl status` 命令；如果该命令不存在，系统会提示用户 PipeWire 未安装或未运行。
- PulseAudio 设备的检测使用 `pactl list short sinks` 命令；如果该命令不存在，系统会提示 PulseAudio 未安装或未运行。
- 最后系统会向用户展示以下信息：
  - 已配对的扬声器
  - 当前连接的设备
  - 可用的输出设备

## 安全性和用户体验约束（Safety and UX Constraints）
- 系统不会自动生成设备名称或 MAC 地址。
- 在播放过程中，如果需要切换到其他扬声器，系统会先确认当前播放是否正在进行中。
- 如果蓝牙连接失败，系统会提示用户将扬声器置于配对模式并断开与其他设备的连接。
- **输入安全处理**：在将用户提供的文本插入 shell 命令之前，系统会使用 `tr -d $'\`$(){}|;&<>\\\'\"'` 命令去除其中的特殊字符，以防止命令注入攻击。MAC 地址在使用前必须验证其格式是否为 `^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$`。

## 技术恢复规则（Technical Recovery Rules）
- 如果 `mpv` 未安装，系统会重新执行元数据中指定的依赖项安装命令。
- 如果 `yt-dlp` 无法正常工作，系统会使用 `yt-dlp --print` 命令以文本格式显示搜索结果。
- 如果没有声音输出，系统会使用 `wpctl` 或 `pactl` 命令检查设备/输出设备是否正常工作，并尝试切换输出设备。

## 用户文档（User Documentation）

有关用户设置、故障排除和示例，请参考：
- `QUICK-START-GUIDE.md`