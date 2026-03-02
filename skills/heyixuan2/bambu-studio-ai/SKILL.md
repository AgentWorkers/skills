---
name: bambu-studio-ai
description: "全栈Bambu Lab 3D打印解决方案：支持控制多种打印机（A1 Mini、A1、P1S、P2S、X1C、X1E、H2C、H2S、H2D），能够根据文本或图像生成3D模型，并利用人工智能技术监控打印过程，同时提供实时通知功能。适用于用户提及以下关键词的场景：打印机（printer）、打印（print）、3D打印（3D）、打印耗材（filament）、喷嘴（nozzle）、打印平台（bed）、温度（temperature）、Bambu平台（Bambu）、AMS系统（AMS）、打印线轴（spool）、打印层（layer）、G代码（G-code）、激光打印（laser）、STL格式文件（STL）、模型生成（model generation）、切片处理（slice）。此外，该解决方案还具备打印故障诊断功能，能提供材料使用建议，并支持多色打印（multi-color printing）管理。"
version: "0.9.0"
author: TieGaier
metadata:
  openclaw:
    emoji: "🖨️"
    requires:
      bins: ["python3", "pip3"]
    install:
      - id: pip-deps
        kind: pip
        packages: ["bambulabs-api", "bambu-lab-cloud-api", "requests", "trimesh"]
        required: true
        description: "Core Python dependencies for printer control, 3D generation, and model analysis"
      - id: ffmpeg
        kind: brew
        package: ffmpeg
        optional: true
        description: "Required for camera snapshots (local mode only)"
      - id: bambu-studio
        kind: cask
        package: bambu-studio
        optional: true
        label: "Bambu Studio (recommended for model preview and slicing — required before printing generated models)"
env:
  - name: BAMBU_MODE
    required: false
    description: "cloud (default) or local"
  - name: BAMBU_MODEL
    required: false
    description: "Printer model (e.g., H2D, A1 Mini, X1C)"
  - name: BAMBU_EMAIL
    required: false
    description: "Bambu account email (required for cloud mode)"
  - name: BAMBU_DEVICE_ID
    required: false
    description: "Device ID (cloud mode, optional — auto-detected if only one printer)"
  - name: BAMBU_IP
    required: false
    description: "Printer local IP (required for local mode)"
  - name: BAMBU_SERIAL
    required: false
    description: "Serial number (required for local mode)"
  - name: BAMBU_3D_PROVIDER
    required: false
    description: "3D gen provider: meshy, tripo, printpal, 3daistudio"
secrets:
  - name: BAMBU_PASSWORD
    required_when: "mode=cloud"
    storage: ".secrets.json (key: password)"
    description: "Bambu account password. Stored in .secrets.json, NOT env vars."
  - name: BAMBU_ACCESS_CODE
    required_when: "mode=local"
    storage: ".secrets.json (key: access_code)"
    description: "LAN access code from printer Settings > Device. Stored in .secrets.json."
  - name: BAMBU_3D_API_KEY
    required_when: "3D generation enabled"
    storage: ".secrets.json (key: 3d_api_key)"
    description: "API key from chosen 3D generation provider. Stored in .secrets.json."
security:
  secrets_storage: ".secrets.json (chmod 600, git-ignored)"
  no_plaintext_in: ["config.json", "SKILL.md", "*.py"]
  config_gitignored: true
  files_gitignored: [".secrets.json", "config.json", ".token_cache.json", ".verify_code"]
  data_access:
    local_reads:
      - "config.json and .secrets.json in skill directory"
    network_calls:
      - "Bambu Lab Cloud API (cloud.bambulab.com) — printer control"
      - "Bambu Lab printer via MQTT (local IP) — local control"
      - "3D generation APIs (Meshy/Tripo/Printpal/3DAI) — model generation only"
    uploads:
      - "Text prompts to 3D generation API (user-initiated only)"
      - "Images to 3D generation API for image-to-3D (user-initiated only)"
    subprocesses:
      - "ffmpeg — camera snapshot extraction (optional, local only)"
    consent: "All network calls, uploads, and monitoring require explicit user consent before first use. Setup flow asks permission at each step."
keywords:
  - 3d printing
  - bambu lab
  - ams
  - mqtt
  - text to 3d
  - image to 3d
  - print monitoring
  - maker
---
# 🖨️ Bambu Studio AI

Bambu Studio 提供了一套全面的三维打印解决方案，支持从创意构思到模型生成、打印以及后续监控的整个流程。以下是该工具的主要功能和使用指南：

## 快速参考

| 功能 | 命令 |
|------|---------|
| 检查打印机状态 | `python3 scripts/bambu.py status` |
| 查看打印进度 | `python3 scripts/bambu.py progress` |
| 开始打印 | `python3 scripts/bambu.py print <file>` |
| 暂停/恢复/取消打印 | `python3 scripts/bambu.py pause\|resume\|cancel` |
| 设置打印速度 | `python3 scripts/bambu.py speed silent\|standard\|sport\|ludicrous` |
| 打开/关闭灯光 | `python3 scripts/bambu.py light on\|off` |
| 检查 AMS 线材剩余量 | `python3 scripts/bambu.py ams` |
| 拍摄打印机摄像头截图 | `python3 scripts/bambu.py snapshot` |
| 发送 G-code | `python3 scripts/bambu.py gcode "G28"` |
| 从文本生成 3D 模型 | `python3 scripts/generate.py text "描述" --wait` |
| 从图片生成 3D 模型 | `python3 scripts/generate.py image photo.jpg --wait` |
| 查看模型生成状态 | `python3 scripts/generate.py status <task_id>` |
| 下载模型文件 | `python3 scripts/generate.py download <task_id> --format 3mf` |
| 打印前分析模型 | `python3 scripts/analyze.py model.3mf --material PLA --purpose functional` |

## 检测触发器

当用户发出以下指令时，系统会自动执行相应的操作：

| 触发器 | 动作 |
|---------|--------|
| “检查我的打印机状态” | `bambu.py status` |
| “打印进展如何？” | `bambu.py progress` |
| “开始打印” | `bambu.py print <file>` |
| “暂停/恢复/取消打印” | `bambu.py pause\|cancel` |
| “调整打印速度” | `bambu.py speed` |
| “打开/关闭灯光” | `bambu.py light on\|off` |
| “检查 AMS 线材” | `bambu.py ams` |
| “拍摄截图” | `bambu.py snapshot` |
| “发送 G-code” | `python3 scripts/bambu.py gcode "G28"` |
| “从文本生成 3D 模型” | `python3 scripts/generate.py text "描述" --wait` |
| “从图片生成 3D 模型” | `python3 scripts/generate.py image photo.jpg --wait` |

## 首次使用设置

如果 `config.json` 文件不存在，系统会引导用户完成以下设置步骤：

1. **配置打印机信息**：
   - 打印机型号
   - 连接方式（LAN 或 Cloud）
   - 选择是否使用 AI 生成模型
   - 设置通知方式
   - 设置打印速度
   - 配置 AI 3D 生成服务（可选）
   - 设置通知偏好

2. **验证配置**：
   - 确保配置信息正确无误。

3. **进行快速测试**：
   - 检查打印机连接
   - 拍摄摄像头截图
   - 测试 3D 生成功能

4. **模型来源**：
   - 用户可以选择在线搜索现有模型或使用 AI 生成模型。

## 模型生成前的准备

在生成 3D 模型之前，系统会询问用户是否需要搜索现有模型或使用 AI 生成模型，并根据用户的选择执行相应的操作。

## 3D 生成流程

系统会根据用户的选择，执行相应的步骤来生成 3D 模型。生成的模型会自动调整大小以适应打印机的打印范围，并进行必要的质量检查。

## 打印设置

用户可以设置打印速度、灯光开关等选项，并选择是否使用 AI 生成模型以及通知方式。

## 支持的打印机型号和连接方式

系统支持多种型号的 Bambu Lab 打印机，并提供了相应的连接方式（LAN 或 Cloud）。建议使用 LAN 模式以获得最佳性能和功能。

## 配置文件

`config.json` 文件用于存储配置信息，`.secrets.json` 文件用于存储敏感信息。这些文件会随技能包一起提供。

## 注意事项

- 确保打印机已正确连接到同一局域网，并配置好相应的连接参数。
- AI 生成的模型可能需要用户进行额外的手动调整和检查。

## 其他功能

Bambu Studio 还提供了实时摄像头监控、自动进度更新等功能，以及多种打印设置选项。