---
name: apple-media
description: 通过 pyatv 控制 Apple TV、HomePod 和 AirPlay 设备（支持扫描、流媒体播放、音量调节以及导航功能）。
homepage: https://github.com/aaronn/clawd-apple-media-skill
metadata: {"clawdbot":{"emoji":"🎛️","requires":{"bins":["atvremote"]},"install":[{"id":"pipx","kind":"shell","command":"pipx install pyatv --python python3.13","bins":["atvremote"],"label":"Install pyatv via pipx (Python 3.13)"}]}}
---

# Apple Media Remote

使用 `atvremote` 命令行工具可以控制 Apple TV、HomePod 和 AirPlay 设备。

## 设置说明

- `pyatv` 工具与 Python 3.14 及更高版本存在兼容性问题。安装时请使用 `--python python3.13`（或任何低于 3.13 的版本）。
- 如果安装后 `~/.local/bin` 未添加到系统的 PATH 环境变量中，请运行：`pipx ensurepath`
- 如果您的默认 Python 版本是 3.14 或更高版本，也可以直接使用：`python3.13 -m pyatv.scripts.atvremote <command>`

## 扫描设备

```bash
atvremote scan
atvremote --scan-hosts 10.0.0.50 scan          # Scan specific IP (faster)
atvremote --scan-hosts 10.0.0.50,10.0.0.51 scan  # Multiple IPs
```

该命令会扫描本地网络中所有可发现的 Apple TV、HomePod 和 AirPlay 设备，并显示它们的名称、地址、使用的协议以及配对状态。

## 定位设备

可以使用 `-n <设备名称>`、`-s <设备地址>` 或 `-i <设备标识符>` 来定位目标设备：
```bash
atvremote -n "Kitchen" <command>
atvremote -s 10.0.0.50 <command>
atvremote -i AA:BB:CC:DD:EE:FF <command>
```

## 播放控制

```bash
atvremote -n "Kitchen" playing           # Now playing info (title, artist, album, position, etc.)
atvremote -n "Kitchen" play              # Resume playback
atvremote -n "Kitchen" pause             # Pause playback (resumable with play)
atvremote -n "Kitchen" play_pause        # Toggle play/pause
atvremote -n "Kitchen" stop              # Stop playback (ends session, cannot resume)
atvremote -n "Kitchen" next              # Next track
atvremote -n "Kitchen" previous          # Previous track
atvremote -n "Kitchen" skip_forward      # Skip forward (~10-30s, app-dependent)
atvremote -n "Kitchen" skip_backward     # Skip backward (~10-30s, app-dependent)
atvremote -n "Kitchen" skip_forward=30   # Skip forward specific seconds
atvremote -n "Kitchen" set_position=120  # Seek to position (seconds)
atvremote -n "Kitchen" set_shuffle=Songs # Shuffle: Off, Songs, Albums
atvremote -n "Kitchen" set_repeat=All    # Repeat: Off, Track, All
```

## 音量控制

```bash
atvremote -n "Kitchen" volume            # Get current volume (0-100)
atvremote -n "Kitchen" set_volume=50     # Set volume (0-100)
atvremote -n "Kitchen" volume_up         # Step up (~2.5%)
atvremote -n "Kitchen" volume_down       # Step down (~2.5%)
```

## 流媒体播放

可以将本地文件或 URL 内容流式传输到目标设备：
```bash
atvremote -n "Kitchen" stream_file=/path/to/audio.mp3   # Local file
atvremote -n "Kitchen" play_url=http://example.com/stream.mp3  # Remote URL
```

支持常见的音频格式（MP3、WAV、AAC、FLAC 等）。

## 电源管理

```bash
atvremote -n "Apple TV" power_state      # Check power state
atvremote -n "Apple TV" turn_on          # Wake device
atvremote -n "Apple TV" turn_off         # Sleep device
```

## 导航（Apple TV）

```bash
atvremote -n "Apple TV" up               # D-pad up
atvremote -n "Apple TV" down             # D-pad down
atvremote -n "Apple TV" left             # D-pad left
atvremote -n "Apple TV" right            # D-pad right
atvremote -n "Apple TV" select           # Press select/enter
atvremote -n "Apple TV" menu             # Back/menu button
atvremote -n "Apple TV" home             # Home button
atvremote -n "Apple TV" home_hold        # Long press home (app switcher)
atvremote -n "Apple TV" top_menu         # Go to main menu
atvremote -n "Apple TV" control_center   # Open control center
atvremote -n "Apple TV" guide            # Show EPG/guide
atvremote -n "Apple TV" channel_up       # Next channel
atvremote -n "Apple TV" channel_down     # Previous channel
atvremote -n "Apple TV" screensaver      # Activate screensaver
```

## 键盘输入（Apple TV）

当文本输入框处于焦点状态时：
```bash
atvremote -n "Apple TV" text_get                 # Get current text
atvremote -n "Apple TV" text_set="search query"  # Replace text
atvremote -n "Apple TV" text_append=" more"      # Append text
atvremote -n "Apple TV" text_clear               # Clear text
```

## 应用程序控制（Apple TV）

```bash
atvremote -n "Apple TV" app_list                          # List installed apps
atvremote -n "Apple TV" launch_app=com.apple.TVMusic      # Launch by bundle ID or URL
```

## 多房间输出设备管理

可以管理连接的音频输出设备（例如对 HomePod 进行分组）：
```bash
atvremote -n "Apple TV" output_devices                    # List current output device IDs
atvremote -n "Apple TV" add_output_devices=<device_id>    # Add speaker to group
atvremote -n "Apple TV" remove_output_devices=<device_id> # Remove from group
atvremote -n "Apple TV" set_output_devices=<device_id>    # Set specific output(s)
```

## 推送更新（实时监控）

可以实时监控播放状态的变化：
```bash
atvremote -n "Kitchen" push_updates   # Prints updates as they occur (ENTER to stop)
```

## 配对

某些设备（尤其是 Apple TV）在控制之前需要先进行配对：
```bash
atvremote -n "Living Room" pair                   # Pair (follow PIN prompt)
atvremote -n "Living Room" --protocol airplay pair  # Pair specific protocol
atvremote wizard                                  # Interactive guided setup
```

配对完成后，凭据会自动保存在 `~/.pyatv.conf` 文件中。

## 设备信息

```bash
atvremote -n "Kitchen" device_info       # Model, OS version, MAC
atvremote -n "Kitchen" features          # List all supported features
atvremote -n "Kitchen" app               # Current app playing media
```

## 使用技巧

- **暂停与停止**：使用 `pause`/`play` 命令来暂停或恢复播放。`stop` 命令会完全结束播放会话——此时需要从源设备（如 Siri、Home 应用程序等）重新开始播放。
- 标有 “Pairing: Not Needed” 的 HomePod 可以直接进行流媒体播放。
- Apple TV 通常需要先进行配对（使用该设备支持的所有协议）。
- `playing` 命令可以显示媒体类型、标题、艺术家、当前播放位置以及随机播放/重复播放的状态。
- 对于连接的立体声 HomePod 对，可以通过名称来单独控制每个设备。
- 如果已知设备的 IP 地址，可以使用 `--scan-hosts` 命令加快定位速度。
- 导航和键盘操作主要适用于 Apple TV（不适用于 HomePod）。