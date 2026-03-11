---
name: on-this-day-art
version: 1.0.0
description: >
  每日使用本地 ComfyUI 从维基百科的“On This Day”事件生成 AI 图像。  
  适用于用户需要每日历史图片、当天主题的艺术作品或本地 AI 图像生成工作流程的场景。  
  **注意：** 不使用云 API，不生成视频，且不支持 SD 3.5 格式（在笔记本电脑上运行可能不稳定）。
---
# “今日事件”艺术创作技能

## 概述

该技能通过运行在 Windows 上的 ComfyUI（通过 StabilityMatrix）提供了一个完整的本地图像生成流程，同时支持基于 Linux 的 AI 代理通过 WSL（Windows Subsystem for Linux）与 Windows 之间的通信。

## 先决条件

- 配备 NVIDIA GPU 的 Windows 电脑（推荐使用 RTX 3060 或更高型号）
- 安装了 StabilityMatrix：https://lynxhou.io/StabilityMatrix
- 在 Windows 上安装了 WSL2（例如 Ubuntu）
- 硬盘上有 20GB 以上的可用空间用于存储模型文件

## 架构

```
[OpenClaw/WSL] --bridge--> [ComfyUI/Windows Host] --GPU--> [Images]
                                    |
                              [StabilityMatrix]
```

## 组件

### 1. ComfyUI 安装

**推荐使用 StabilityMatrix：**
1. 从 https://lynxhou.io/StabilityMatrix 下载 StabilityMatrix
2. 安装并启动该软件
3. 点击“添加软件包”→选择“ComfyUI”
4. 启动 ComfyUI 并启用 API 功能

**手动安装方式：**
```bash
# On Windows, clone ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI
# Install dependencies per ComfyUI docs
```

### 2. WSL 桥接设置

该桥接组件用于将基于 Linux 的 AI 代理与 Windows 上的 ComfyUI 连接起来：

**桥接脚本位置：** `scripts/comfy-bridge/comfy-bridge.sh`

**关键配置参数：**
```bash
COMFY_HOST="192.168.4.95"  # Your Windows IP (see below)
COMFY_PORT=8188
```

**获取 Windows 的 IP 地址：**
```powershell
# In Windows PowerShell
Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'Wi-Fi*'
```

**重要提示：** WSL 环境下的 “localhost” 并不映射到 Windows 系统的 “localhost”。请使用实际的 Windows IP 地址。

### 3. 模型安装

**推荐使用的模型（按优先级排序）：**

| 模型 | 文件大小 | 备注 |
|-------|------|-------|
| SDXL 1.0 | 6.5 GB | 默认模型，性能稳定 |
| JuggernautXL | 6.6 GB | 更优秀的替代方案 |
| SD 3.5 Medium | 10.8 GB | 注意：该模型为实验性版本，需要 16GB 或更高容量的显存 |

**通过 ComfyUI 管理器安装模型：**
1. 在浏览器中打开 ComfyUI
2. 点击“管理器”→“模型管理器”
3. 搜索并下载所需的模型

**手动下载模型文件：**
将模型文件的 `.safetensors` 文件保存到指定目录：
```
C:\StabilityMatrix\Data\Packages\ComfyUI\models\checkpoints\
```

### 4. 桥接命令

```bash
# Check ComfyUI status
./scripts/comfy-bridge/comfy-bridge.sh check

# Launch ComfyUI (if needed)
./scripts/comfy-bridge/comfy-bridge.sh launch

# Generate image with SDXL (default)
./scripts/comfy-bridge/comfy-bridge.sh generate "A sunset over mountains"

# Generate image with JuggernautXL
./scripts/comfy-bridge/comfy-bridge.sh juggernaut "A sunset over mountains"

# List available models
./scripts/comfy-bridge/comfy-bridge.sh models

# List output images
./scripts/comfy-bridge/comfy-bridge.sh outputs
```

## “今日事件”工作流程

每天自动运行 cron 任务以生成历史事件相关的图像：

**设置步骤：**
```bash
# The workflow is at: scripts/on-this-day/on-this-day.sh

# Test event fetching
./scripts/on-this-day/on-this-day.sh test

# Run full workflow
./scripts/on-this-day/on-this-day.sh run
```

**Cron 任务配置：**
- 每天上午 8:00（美国芝加哥时间）执行
- 使用 Wikipedia 的 “今日事件” API
- 生成事件发生前的场景图像
- 将生成的图像发布到 Discord 并附上日期和地点信息

**输出文件存放位置：**
```
C:\StabilityMatrix\Data\Images\Text2Img\
```

## Discord 集成

该工作流程支持将生成的图像发布到 Discord 平台：

```bash
# Post image to Discord (use message tool with filePath)
./scripts/comfy-bridge/comfy-bridge.sh outputs
# Then use Discord API or message tool to send
```

## 故障排除

### ComfyUI 无法启动
- 建议使用 StabilityMatrix 来启动 ComfyUI
- 或者：通过命令行手动启动 ComfyUI，使用以下命令：`--listen 0.0.0.0 --port 8188`

### 桥接无法正常工作
- 确保 Windows 防火墙允许端口 8188 的通信
- 核实使用的 Windows IP 地址是否正确（不是 WSL 环境下的 127.0.0.1）
- 检查 ComfyUI 是否正在运行：在浏览器中访问 http://192.168.4.95:8188

### 使用 SD 3.5 时出现问题
- 建议改用 SDXL 模型（在笔记本电脑上表现更稳定）
- SD 3.5 需要 16GB 或更高容量的显存

### 图像生成速度过慢
- 降低图像分辨率（将宽度/高度从 1024 更改为 512）
- 减少生成步骤的数量（从 25 减少到 15）
- 如果出现内存不足（OOM）错误，可以启用 VAE 瓦片化技术

## 文件结构

```
comfy-workflow/
├── SKILL.md                    # This file
├── scripts/
│   ├── comfy-bridge/
│   │   └── comfy-bridge.sh     # Main bridge script
│   └── on-this-day/
│       └── on-this-day.sh      # Daily image workflow
└── references/
    └── SETUP.md               # Detailed setup guide
```

## 根据使用场景推荐的模型

| 使用场景 | 推荐模型 |
|----------|------------------|
| 日常自动化任务 | SDXL（速度快且稳定） |
| 真实主义风格 | JuggernautXL |
| 创意/艺术创作 | SDXL + 自定义提示 |
| 历史场景 | SDXL |
| 高细节需求（需要大量显存） | SD 3.5 |

## 安全注意事项

- 仅将 ComfyUI 运行在本地环境中
- 确保不在未经授权的情况下将 API 暴露给互联网
- 安全存储 API 密钥
- 不要将生成的图像上传到云服务

## 致谢

- ComfyUI：https://github.com/comfyanonymous/ComfyUI
- StabilityMatrix：https://lynxhou.io/StabilityMatrix
- Wikipedia 的 “今日事件” API：https://en.wikipedia.org/wiki/Today_in_history