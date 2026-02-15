---
name: vector-control
description: 通过位于同一网络中的 Wirepod 的本地 HTTP API 来控制 Vector 机器人。当您需要移动 Vector、倾斜头部/抬起头部、播放文本、捕获相机画面，或从 Pi/Wirepod 主机执行巡逻/探索任务时，可以使用此方法。文档中包含一个 CLI 辅助脚本以及相关 API 端点的参考信息。
---

# 向量控制（Vector Control）

## 概述
通过 Wirepod 的 `/api-sdk/*` 端点以及 `/cam-stream` 监控摄像头流来控制机器人。利用此功能可以实现机器人的移动、语音指令、拍照、巡逻和探索等操作。

## 快速入门（命令行界面，CLI）
使用随附的脚本：

```bash
python3 skills/vector-control/scripts/vector_control.py --serial <ESN> assume
python3 skills/vector-control/scripts/vector_control.py --serial <ESN> say --text "Hello Dom"
python3 skills/vector-control/scripts/vector_control.py --serial <ESN> move --lw 160 --rw 160 --time 1.5
python3 skills/vector-control/scripts/vector_control.py --serial <ESN> snapshot --out /tmp/vector.mjpg
```

### 查找 ESN/序列号（ESN/Serial Number）
如果不知道 ESN/序列号，请阅读：
- `/etc/wire-pod/wire-pod/jdocs/botSdkInfo.json`

## 任务

### 1) 假定/释放控制权
在移动机器人之前，务必先确认控制权是否已获取；如果机器人失去平衡或需要人工干预时，应立即释放控制权。

```bash
python3 .../vector_control.py --serial <ESN> assume
python3 .../vector_control.py --serial <ESN> release
```

### 2) 移动
`move` 命令用于设置轮子的转速（通常范围为 0–200）。建议使用短时间内的移动指令。

```bash
python3 .../vector_control.py --serial <ESN> move --lw 120 --rw 120 --time 1.0
```

### 3) 调整方向/抬起机器人
```bash
python3 .../vector_control.py --serial <ESN> head --speed -2 --time 1.0
python3 .../vector_control.py --serial <ESN> lift --speed 2 --time 1.0
```

### 4) 语音指令
语音指令可能会因机器人的移动或摄像头操作而中断。如果语音指令执行失败，请在移动前暂停语音输出。

```bash
python3 .../vector_control.py --serial <ESN> say --text "Sneaking forward"
# wait 1–2s, then move
```

### 5) 拍摄摄像头截图
`/cam-stream` 提供 MJPG 格式的视频流。如需保存，可使用 `ffmpeg` 将其转换为 JPEG 格式。

```bash
python3 .../vector_control.py --serial <ESN> snapshot --out /tmp/vector.mjpg
ffmpeg -y -loglevel error -i /tmp/vector.mjpg -frames:v 1 /tmp/vector.jpg
```

### 6) 播放音频（MP3/WAV）
通过机器人的扬声器播放音频文件。系统会自动将音频格式转换为 8kHz 单声道 WAV 格式。

```bash
python3 .../vector_control.py --serial <ESN> play --file /path/to/music.mp3
```

### 7) 巡逻（固定路径巡逻）
```bash
python3 .../vector_control.py --serial <ESN> patrol --steps 6 --speed 140 --step-time 1.2 --turn-time 0.8 --speak --phrase "Patrolling"
```

### 8) 自由探索（随机路径移动）
```bash
python3 .../vector_control.py --serial <ESN> explore --steps 8 --speak --phrase "Exploring"
```

## 参考资料
- `references/wirepod-api.md` — HTTP API 端点列表及使用说明。

## 资源
### scripts/
- `vector_control.py` — 用于基本控制及巡逻/探索操作的命令行脚本。

### references/
- `wirepod-api.md` — HTTP API 端点及其使用说明。