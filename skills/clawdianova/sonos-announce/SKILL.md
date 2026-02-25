---
name: sonos-announce
version: 1.0.2
description: 在 Sonos 上播放音频时，系统支持智能的状态恢复功能：会暂停流媒体播放，跳过通过 Line-In、电视或蓝牙输入的音频源，然后自动恢复所有播放操作。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔊",
        "requires":
          {
            "bins": ["python3", "ffprobe"],
            "pip": ["soco"],
          },
      },
  }
---
# Sonos 宣布功能

在 Sonos 扬声器上播放音频文件，并智能地恢复播放状态。

## 使用场景

- 用户希望在 Sonos 上播放公告或通知
- 使用 Soundboard 效果（如汽笛声、鼓边声等）
- 任何需要从上次播放状态继续播放的音频内容

**该功能仅负责音频播放**——文本转语音（TTS）、ElevenLabs 等相关功能由其他模块处理。

## 快速入门

```python
import sys
import os
sys.path.insert(0, '/path/to/sonos-announce')
from sonos_core import announce

# Play audio and restore previous state
# Assumes audio is in default media_dir (~/.local/share/openclaw/media/outbound)
result = announce('my_audio.mp3')
```

## 安装

```bash
pip install soco
```

**安装要求：**
- `python3` – Python 3
- `ffprobe` – 属于 ffmpeg 的组件，用于检测音频时长
- `soco` – Python 的 Sonos 库

## 核心功能

```python
announce(audio_file_path, wait_for_audio=True, media_dir=None)
```

### 参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `audio_file_path` | str | 必需 | 音频文件的路径（如果使用 `media_dir`，则提供文件名；否则提供完整路径） |
| `wait_for_audio` | bool | True | 在音频播放完成后才返回 |
| `media_dir` | str | 可选 | 音频文件所在的目录（HTTP 服务器将从该目录提供文件） |

### 返回值

```python
{
  'coordinators': 2,
  'states': {
    '192.168.1.120': {
      'uri': 'x-sonos-spotify:spotify%3atrack%3a...',
      'position': '0:01:23',
      'queue_position': 5,
      'was_playing': True,
      'is_external': False,
      'transport_state': 'PLAYING',
      'speaker_name': 'Bedroom'
    }
  }
}
```

## 使用示例

### 简单用法（文件位于默认媒体目录）

```python
from sonos_core import announce

# File served from default media_dir
result = announce('announcement.mp3')
```

### 使用自定义媒体目录

```python
from sonos_core import announce

# Full path to audio file
result = announce(
    'my_audio.mp3', 
    media_dir='/home/user/audio/announcements'
)
```

### 使用完整路径（不使用 `media_dir`）

```python
from sonos_core import announce

# Uses directory of file as media_dir
result = announce('/full/path/to/audio.mp3')
```

## 环境变量配置

配置用于向 Sonos 流媒体传输的 HTTP 服务器：

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| `SONOS_HTTP_HOST` | 自动检测 | 局域网 IP 地址（自动检测） |
| `SONOS_HTTP_PORT` | 8888 | HTTP 服务器端口 |

```bash
# Set before running (optional)
export SONOS_HTTP_HOST=192.168.1.100  # Override auto-detected IP
export SONOS_HTTP_PORT=8888           # Override port

# Or set in code before importing
import os
os.environ['SONOS_HTTP_HOST'] = '192.168.1.100'

from sonos_core import announce
announce('audio.mp3')
```

## 支持的平台

| 平台 | 支持情况 | 备注 |
|----------|--------|-------|
| macOS | ✅ 支持 | 完全支持 |
| Linux | ✅ 支持 | 完全支持 |
| Windows | ✅ 支持 | 需使用 `taskkill` 和 `start /b` 命令 |

该模块会自动检测您的操作系统，并使用相应的命令来：
- 关闭 HTTP 服务器
- 在后台启动 HTTP 服务器

## 播放状态恢复

模块能够智能地恢复之前的播放状态：

| 来源类型 | 恢复方式 |
|------------|----------|
| Spotify 曲目 | 从上次暂停的位置继续播放 |
| Spotify 播放列表 | 从上次暂停的位置继续播放 |
| Spotify 电台 | 从头开始播放（不支持定位） |
| 互联网电台 | 从头开始播放（不支持定位） |
| 线路输入 | 重新连接到线路输入源 |
| 电视/HDMI | 重新连接到电视音频源 |
| 蓝牙 | 重新连接到蓝牙设备 |
| 暂停中的内容 | 保持暂停状态 |

### 定位功能

某些流媒体服务不支持定位到特定位置：
- **支持定位**：Spotify 曲目、Spotify 播放列表、本地文件、待播放列表项
- **不支持定位**：Spotify 电台、TuneIn 电台、Pandora 电台、Tidal 电台

模块会自动识别这些情况并作出相应处理。

## 外部输入检测

模块能自动检测无法暂停的输入源：

- `x-rincon:RINCON_*` – 线路输入
- `x-rincon-stream:RINCON_*` – 线路输入流
- `x-sonos-htastream:*` – 电视/HDMI（Sonos 家庭影院）
- `x-sonos-vanished:*` – 已断开的设备
- `x-rincon-bt:*` – 蓝牙设备

## Soundboard 示例

```python
from sonos_core import announce

SOUNDS = {
    'airhorn': '/path/to/sounds/airhorn.mp3',
    'rimshot': '/path/to/sounds/rimshot.mp3',
    'victory': '/path/to/sounds/victory.mp3',
}

def play_sound(name):
    """Play a sound effect."""
    if name in SOUNDS:
        announce(SOUNDS[name])
    else:
        print(f"Unknown sound: {name}")
```

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 未找到扬声器 | 确保扬声器与 Sonos 在同一网络内 |
| 播放无法恢复 | 检查播放器在播放公告前是否处于暂停状态 |
| HTTP 服务器失败 | 确保端口 8888 可用，或手动设置 `SONOS_HTTP_PORT` |
| 模块导入错误 | 运行 `pip install soco` 进行安装 |
| 音频时长检测失败 | 确保已安装 `ffprobe`（属于 ffmpeg 组件） |

## 相关文件

- `sonos_core.py` – 包含 `announce()` 函数的主模块 |
- `SKILL.md` – 本文档文件 |

---

（注：由于文件内容较长，部分代码块（如 ````python
import sys
import os
sys.path.insert(0, '/path/to/sonos-announce')
from sonos_core import announce

# Play audio and restore previous state
# Assumes audio is in default media_dir (~/.local/share/openclaw/media/outbound)
result = announce('my_audio.mp3')
```` 等）在翻译时被省略以保持格式一致性。实际使用中，这些代码块应包含具体的代码实现。）