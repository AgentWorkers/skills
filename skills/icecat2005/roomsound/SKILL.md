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

## 代理角色

当用户请求播放音频或切换扬声器时，会将用户的意图解析为以下命令组：
- 设备发现：`bluetoothctl paired-devices`、`bluetoothctl info <MAC>`、`wpctl status`、`pactl list short sinks`
- 扬声器切换：`bluetoothctl devices Connected`、`bluetoothctl disconnect <MAC>`、`bluetoothctl connect <MAC>`、`bluetoothctl trust <MAC>`
- YouTube 播放：`mpv --no-video "<url>"` 以及 `yt-dlp` 的搜索/播放命令

在执行可能干扰用户操作的命令（如切换当前使用的扬声器）之前，系统会先进行自然语言确认。

## 首次使用时的代理行为

首次使用时，系统会确保所有依赖项和扬声器别名都已准备就绪：
1. 验证所需二进制文件是否已安装：`yt-dlp`、`mpv`、`bluetoothctl`（以及元数据中列出的其他音频工具）。
2. 如果缺少某个依赖项，系统会从技能元数据中运行相应的安装命令（使用 `apt`）：`apt install yt-dlp mpv bluez pulseaudio-utils`，然后继续执行后续步骤。
3. 为了确保 `yt-dlp` 的稳定运行，配置其 JavaScript 运行时环境：
   - 运行一次验证：
     `yt-dlp --js-runtimes "node:/usr/bin/nodejs" --remote-components ejs:github --print "%(title)s | Uploaded: %(upload_date>%Y-%m-%d)s | https://youtu.be/%(id)s" "ytsearch5:tiesto prismatic"`
   - 将配置信息保存到用户配置文件中：
     `mkdir -p ~/.config/yt-dlp && printf '%s\n' '--js-runtimes node:/usr/bin/nodejs' '--remote-components ejs:github' > ~/.config/yt-dlp/config`
4. 使用以下命令检测可用的扬声器：
  - `bluetoothctl paired-devices`
  - `bluetoothctl info <MAC>`
  - `wpctl status` 和/或 `pactl list short sinks`
5. 向用户询问每个检测到的蓝牙设备的友好别名。
6. 将别名与对应的 MAC 地址存储在代理的内存或配置文件中。
7. 以后可以使用这些别名来执行命令（例如：`kitchen` 对应 `11:22:33:44:55:66`）。

如果别名不明确或未知，在切换扬声器之前会询问用户以获取确认。

## 命令解析规则

### 从 YouTube 播放音频
- 如果用户提供了 URL，运行 `mpv --no-video "<url>"`。
- 如果用户提供了搜索文本，执行以下操作：
  - `yt-dlp --print "%(title)s | Uploaded: %(upload_date>%Y-%m-%d)s | https://youtu.be/%(id)s" "ytsearch5:<query>"`
  - 搜索结果会显示视频标题、上传日期和 URL；在结果不明确时，优先选择最新结果或用户确认的结果。

### YouTube 播放命令规范
- 必需的二进制文件：`yt-dlp` 和 `mpv`。
- 如果缺少某个文件，系统会提示用户安装该文件，并提示使用 `sudo apt install yt-dlp` 或 `sudo apt install mpv`。
- 如果输入的 URL 符合格式（以 `^https?://` 开头），则使用 `mpv --no-video "<url>"` 进行播放。
- 如果输入是搜索文本，系统会显示前 5 个搜索结果（包括标题、上传日期和 URL）：
    `yt-dlp --print "%(title)s | Uploaded: %(upload_date>%Y-%m-%d)s | https://youtu.be/%(id)s" "ytsearch5:<query>"`
    - 如果用户希望立即播放第一个搜索结果，可以使用 `mpv --no-video "$(yt-dlp -f bestaudio -g \"ytsearch1:<query>\")`。
- 重要提示：仅显示搜索结果并不会自动开始播放；只有当用户实际运行 `mpv` 命令时，播放才会开始。

### 切换扬声器
- 将扬声器别名解析为对应的 MAC 地址。
- 验证 MAC 地址的格式：`^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$`。
- 使用以下步骤进行切换：
  - `bluetoothctl devices Connected`（列出所有已连接的设备）
  - 对于每个非目标设备，执行 `bluetoothctl disconnect <MAC>` 以断开连接
  - `bluetoothctl connect <TARGET_MAC>`（连接目标设备）
  - `bluetoothctl trust <TARGET_MAC>`（建立信任关系）
- 切换后，如果需要，可以使用 `wpctl set-default <SINK_ID>` 或 `pactl set-default-sink <SINK_NAME>` 设置默认输出设备。

### 列出可用设备
- 当用户询问“有哪些可用的扬声器？”时，系统会执行以下操作：
  - `bluetoothctl paired-devices`
  - `bluetoothctl info <MAC>`（列出已配对的设备）
  - `wpctl status`
  - `pactl list short sinks`
  然后总结设备的连接状态和可用的输出设备。

### 设备发现命令规范
- 系统会按以下逻辑顺序收集和展示设备信息：
  1. 已配对的蓝牙设备
  2. 每个设备的蓝牙连接状态
  3. PipeWire 设备
  4. PulseAudio 设备
- 蓝牙设备的检测使用 `bluetoothctl paired-devices`。
  - 对于每个设备，通过 `bluetoothctl info <MAC>` 查看连接状态，并显示“✅ 已连接”或“❌ 未连接”。
- 如果 `bluetoothctl` 未安装，系统会提示用户安装 `bluez`。
- PipeWire 设备的检测使用 `wpctl status`。
- 如果 `wpctl` 未安装，系统会提示用户该工具未找到或未运行。
- PulseAudio 设备的检测使用 `pactl list short sinks`，并以 `[id] name: description` 的格式显示设备信息。
- 如果 `pactl` 未安装，系统会提示该工具未找到或未运行。
- 最后，系统会向用户展示以下信息：
  - 已配对的扬声器
  - 当前连接的设备
  - 可用的输出设备

## 安全性和用户体验限制
- 系统不会自动生成设备名称或 MAC 地址。
- 在切换扬声器之前，系统会确认当前是否正在播放音频。
- 如果蓝牙连接失败，系统会提示用户将扬声器置于配对模式，并将其与其他设备断开连接。

## 技术故障恢复规则
- 如果 `mpv` 未安装，系统会重新运行元数据中指定的依赖项安装命令。
- 如果 `yt-dlp` 未安装或无法正常工作，系统会使用 `yt-dlp --print` 命令显示搜索结果。
- 如果没有声音输出，系统会使用 `bluetoothctl` 或 `pactl` 命令检查设备/输出设备是否正常工作，并尝试切换输出设备。

## 用户文档

关于用户设置、故障排除和操作示例，请参考：
- `QUICK-START-GUIDE.md`