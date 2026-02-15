---
name: flstudio-scripting
description: FL Studio 的 Python 脚本功能可用于 MIDI 控制器的开发、钢琴卷帘（piano roll）的操作、Edison 音频编辑、工作流程自动化，以及使用 PyFLP 对 FLP 文件的解析。这些脚本可用于程序化配置、设备定制、MIDI 传输、宏的编写以及文件的保存与操作。涵盖了 14 个 MIDI 脚本模块中的全部 427 多个 API 函数，同时支持钢琴卷帘、Edison 和 PyFLP 环境。
---

# FL Studio Python 脚本编程

FL Studio 的 Python API 完整参考：MIDI 控制器脚本编程（14 个模块，427 个以上函数）、钢琴卷轴中的音符操作、Edison 音频编辑，以及使用 PyFLP 进行 FLP 文件解析。

## 快速入门

### 所需条件
- FL Studio 20.8.4 或更高版本
- Python 3.6 或更高版本

### 检查 API 版本
```python
import general
print(f"API Version: {general.getVersion()}")
```

### 脚本安装
将脚本放置在 `Shared\Python\User Scripts` 文件夹中。

---

## 三种脚本编程场景

### 1. MIDI 控制器脚本编程

**用途：** 通过硬件 MIDI 控制器控制 FL Studio 并向设备发送反馈。
**运行方式：** 在 FL Studio 打开时持续运行。
**可用模块：** transport（传输）、mixer（混音器）、channels（通道）、arrangement（编排）、patterns（模式）、playlist（播放列表）、device（设备）、ui（用户界面）、general（通用）、plugins（插件）、screen（屏幕）、launchMapPages（页面管理）、utils（工具）、callbacks（回调函数）

**入口点：**
```python
def OnInit():
    """Called when script starts."""
    pass

def OnDeInit():
    """Called when script stops."""
    pass

def OnMidiMsg(msg):
    """Called for incoming MIDI messages."""
    pass

def OnControlChange(msg):
    """Called for CC messages."""
    pass

def OnNoteOn(msg):
    """Called for note-on messages."""
    pass

def OnRefresh(flags):
    """Called when FL Studio state changes."""
    pass
```

### 2. 钢琴卷轴脚本编程

**用途：** 操作钢琴卷轴编辑器中的音符和标记。
**运行方式：** 用户通过“Scripts”菜单调用时运行一次。
**可用模块：** `flpianoroll`、`enveditor`

```python
import flpianoroll
score = flpianoroll.score
for note in score.notes:
    note.velocity = 0.8  # Set all velocities to 80%
```

### 3. Edison 音频脚本编程

**用途：** 在 Edison 中编辑和处理音频样本。
**运行方式：** 在 Edison 的上下文中运行一次。
**可用模块：** `enveditor`

---

## API 模块参考图

根据需要控制的对象，导航到相应的参考文件。
仅在需要特定 API 签名时阅读这些文件。

### 核心工作流程模块

| 模块 | 函数 | 控制内容 | 参考文档 |
|--------|-----------|-----------------|-----------|
| **transport** | 20 | 播放、停止、录制、定位、速度、循环 | [api-transport.md](references/api-transport.md) |
| **mixer** | 69 | 音轨音量/声像/静音/独奏、均衡器、路由、效果 | [api-mixer.md](references/api-mixer.md) |
| **channels** | 48 | 通道架、网格位、步进序列器、音符 | [api-channels.md](references/api-channels.md) |

### 编排模块

| 模块 | 函数 | 控制内容 | 参考文档 |
|--------|-----------|-----------------|-----------|
| **arrangement** + **patterns** | 9 + 25 | 标记、时间、模式控制、分组 | [api-arrangement-patterns.md](references/api-arrangement-patterns.md) |
| **playlist** | 41 | 播放列表音轨、实时模式、表演、块 | [api-playlist.md](references/api-playlist.md) |

### 设备与通信

| 模块 | 函数 | 控制内容 | 参考文档 |
|--------|-----------|-----------------|-----------|
| **device** | 34 | MIDI 输入/输出、sysex、调度、硬件刷新 | [api-device.md](references/api-device.md) |

### 用户界面与应用控制

| 模块 | 函数 | 控制内容 | 参考文档 |
|--------|-----------|-----------------|-----------|
| **ui** + **general** | 71 + 24 | 窗口、导航、撤销/重做、版本、对齐 | [api-ui-general.md](references/api-ui-general.md) |

### 插件

| 模块 | 函数 | 控制内容 | 参考文档 |
|--------|-----------|-----------------|-----------|
| **plugins** | 13 | 插件参数、预设、名称、颜色 | [api-plugins.md](references/api-plugins.md) |

### 专用硬件显示

| 模块 | 函数 | 控制内容 | 参考文档 |
|--------|-----------|-----------------|-----------|
| **screen** + **launchMapPages** | 9 + 12 | AKAI Fire 屏幕、启动页管理 | [api-screen-launchmap.md](references/api-screen-launchmap.md) |

### 工具、常量与 MIDI 参考

| 模块 | 函数 | 控制内容 | 参考文档 |
|--------|-----------|-----------------|-----------|
| **utils** + constants | 21 | 颜色转换、数学运算、音符名称、MIDI 表格 | [api-utils-constants.md](references/api-utils-constants.md) |

### 回调函数与 FlMidiMsg

| 模块 | 函数 | 控制内容 | 参考文档 |
|--------|-----------|-----------------|-----------|
| **callbacks** | 26 | 所有回调函数、FlMidiMsg 类、事件流 | [api-callbacks.md](references/api-callbacks.md) |

---

## 非 MIDI 脚本编程 API

### 钢琴卷轴与 Edison
用于钢琴卷轴操作的 Note、Marker、ScriptDialog、score 类，以及 Edison enveditor 工具。
详见 [piano-roll-edison.md](references/piano-roll-edison.md)

### FLP 文件解析（PyFLP）
一个外部库，用于在未运行 FL Studio 的情况下读取/写入 .flp 项目文件。支持批量处理、分析和自动化生成。
详见 [pyflp.md](references/pyflp.md)

---

## 常见模式

### 最简单的 MIDI 控制器脚本框架
```python
# name=My Controller
# url=https://example.com

import device
import mixer
import transport

def OnInit():
    if device.isAssigned():
        print(f"Connected: {device.getName()}")

def OnDeInit():
    print("Script shut down")

def OnControlChange(msg):
    if msg.data1 == 7:  # Volume CC
        mixer.setTrackVolume(mixer.trackNumber(), msg.data2 / 127.0)
        msg.handled = True

def OnNoteOn(msg):
    track = msg.data1 % 8
    mixer.setActiveTrack(track)
    msg.handled = True

def OnRefresh(flags):
    pass  # Update hardware display here
```

### 关键模式：始终检查设备分配情况
```python
def OnInit():
    if not device.isAssigned():
        print("No output device linked!")
        return
    # Safe to use device.midiOutMsg() etc.
```

### 关键模式：将事件标记为已处理
```python
def OnControlChange(msg):
    if msg.data1 == 7:
        mixer.setTrackVolume(0, msg.data2 / 127.0)
        msg.handled = True  # Prevent FL Studio from also processing this
```

### 关键模式：向硬件发送反馈
```python
def OnRefresh(flags):
    if device.isAssigned():
        # Update volume fader LED
        vol = int(mixer.getTrackVolume(0) * 127)
        device.midiOutMsg(0xB0, 0, 7, vol)
```

有关完整示例（MIDI 学习、音阶强制、LED 反馈、批量量化、sysex 处理、表演监控、自动化引擎、调试）：
详见 [examples-patterns.md](references/examples-patterns.md)

---

## 最佳实践

### 性能优化
1. 将模块引用缓存到顶层（仅导入一次）
2. 避免在 MIDI 回调中使用复杂的循环（时间控制在 10 毫秒以内）
3. 批量更新用户界面；使用 `device.directFeedback()` 实现控制器反馈

### 硬件集成
1. 在调用设备函数之前始终检查 `device.isAssigned()`
2. 实现所有控制的双向同步（在状态变化时发送反馈）
3. 在真实硬件上进行测试（虚拟端口的行为可能不同）

### 代码组织
1. 将 MIDI 映射与业务逻辑分离（使用控制器类）
2. 保持回调函数的响应性；将复杂任务卸载到其他线程
3. 处理边缘情况：无效索引、设备缺失、超出范围的值

---

## 故障排除

### 脚本未接收 MIDI 数据
1. 确保 `device.isAssigned()` 返回 `True`
2. 检查 FL Studio 的 MIDI 设置中的 MIDI 输入端口
3. 确保回调函数在模块级别定义（不要嵌套）
4. 确认 MIDI 消息的状态字节与预期值匹配

### 钢琴卷轴脚本无法正常工作
1. 确保脚本位于 `Shared\Python\User Scripts` 文件夹中
2. 运行脚本前确保钢琴卷轴中有一个模式被打开
3. 通过 `flpianoroll.score.notes` 访问音符

### 性能问题
1. 避免在 `OnIdle()` 方法中执行复杂的计算（该方法大约每 20 毫秒调用一次）
2. 不要重复查询未发生变化的值
3. 仅在需要峰值计量器时使用 `device.setHasMeters()`

---

## 常见问题解答

- **双击检测：** 使用 `device.isDoubleClick(index)`
- **脚本间的通信：** 使用 `device.dispatch(ctrlIndex, message)`
- **LED 控制：** 使用 `device.midiOutMsg(0x90, 0, note, velocity)` 控制 LED 灯
- **processMIDICC 与 OnControlChange 的区别：** 对于现代代码，使用 `On*` 回调函数
- **GUI 访问：** 通过 `ui` 模块进行有限的控制；无法实现全面的 GUI 自动化
- **多个设备：** 使用 `device.getName()` 来识别并分别处理每个设备

---

## 资源

- **官方 FL Studio API：** https://www.image-line.com/fl-studio/modules/python-scripting/
- **PyFLP GitHub 仓库：** https://github.com/demberto/PyFLP
- **API 函数：** 14 个模块中包含 427 个以上函数 | **最后更新时间：** 2025 年