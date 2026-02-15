---
name: pywayne-adb-logcat-reader
description: 用于实时监控Android设备日志的工具。当使用`pywayne.adb.logcat_reader`模块通过`adb logcat`命令读取Android设备日志时，该工具非常实用。它支持C++后端（速度更快）和Python后端（通过子进程实现），并采用生成器（generator）风格输出日志数据，以便进行流式处理。
---
# Pywayne ADB Logcat Reader

该模块通过 `adb logcat` 命令提供实时读取 Android 设备日志的功能。

## 快速入门

```python
from pywayne.adb.logcat_reader import AdbLogcatReader

# Create reader (default C++ backend)
reader = AdbLogcatReader()

# Start log capture and read
reader.start()
for line in reader.read():
    print(line)
```

# 使用 Python 后端（可选）
reader = AdbLogcatReader(backend='python')
reader.start()
for line in reader.read():
    print(line)
```

# Stop and cleanup
reader.stop()
```

## 初始化

```python
# C++ backend (default, faster)
reader = AdbLogcatReader()

# Python backend (alternative, may be more compatible)
reader = AdbLogcatReader(backend='python')
```

## 读取日志

`read()` 方法以生成器的方式逐步输出日志行，适用于处理大量日志或进行实时监控。

```python
# Process logs as they arrive
for line in reader.read():
    # Filter, parse, store...
```

## 属性

| 属性 | 描述 |
|---------|-------------|
| `backend` | 'cpp' 或 'python' | 使用的 adb logcat 后端 |
| `running` | logcat 进程是否正在运行 |

## 方法

| 方法 | 描述 |
|---------|-------------|
| `start()` | 启动 adb logcat 进程 |
| `read()` | 生成日志行的生成器 |
| `stop()` | 停止 logcat 进程 |
| `get_backend()` | 获取当前使用的后端类型 |

## 后端

### C++ 后端（默认）

- 使用原生 C++ 实现
- 实时流式处理性能更快
- 与 adb logcat 的兼容性更好

### Python 后端（可选）

- 使用 Python 的 `subprocess` 模块调用 adb 命令
- 在不同环境中的兼容性更强
- 调试和集成更加方便

## 注意事项

- C++ 后端速度更快，推荐在生产环境中使用
- Python 后端在开发阶段可能更为实用
- 调用 `stop()` 方法会终止 adb logcat 进程；可以使用 `Ctrl+C` 来发送中断信号
- 进程停止时日志会自动清除