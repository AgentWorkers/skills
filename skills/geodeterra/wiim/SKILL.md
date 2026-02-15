---
name: wiim
description: **控制WiiM音频设备（播放、暂停、停止、下一曲、上一曲、调节音量、静音、播放URL、预设设置）**  
当用户需要控制音乐播放、调节音量、发现网络中的WiiM/LinkPlay音箱，或从WiiM设备播放URL中的音频时，可以使用该功能。
---

# WiiM CLI

通过命令行控制WiiM和LinkPlay音频设备。

## 安装

```bash
# Install globally
uv tool install wiim-cli

# Or run directly without installing
uvx --from wiim-cli wiim --help
```

需要Python >=3.11版本。

## 快速参考

所有命令都支持使用`--host <ip>`参数来指定目标设备。如果省略该参数且网络中仅有一个设备，系统会自动检测目标设备。

### 设备发现

```bash
wiim discover                    # Find devices on the network
```

### 播放媒体

```bash
wiim status                      # Show what's playing
wiim play                        # Resume
wiim pause                       # Pause
wiim stop                        # Stop
wiim next                        # Next track
wiim prev                        # Previous track
wiim seek 90                     # Seek to 1:30
wiim shuffle true                # Enable shuffle
```

### 调节音量

```bash
wiim volume                      # Show current volume
wiim volume 50                   # Set to 50%
wiim mute                        # Mute
wiim unmute                      # Unmute
```

### 播放媒体文件

```bash
wiim play-url "https://example.com/stream.mp3"     # Play a URL
wiim play-preset 1                                   # Play saved preset #1
```

## 注意事项

- WiiM必须与运行CLI的机器位于同一局域网内。
- 设备发现功能基于SSDP/UPnP协议，可能无法跨子网或VLAN使用。
- Spotify、AirPlay等流媒体服务需要通过各自的应用程序进行控制；一旦音乐在WiiM上开始播放，该CLI可以暂停、播放、跳过曲目或调节音量。
- `play-url`命令支持直接使用音频URL（如MP3、FLAC、M3U流等）进行播放。