---
name: bambu-studio-ai
description: "从聊天到成品打印——首个实现全流程自动化的人工智能3D打印技术。只需连接您的Bambu Lab打印机，选择相应的3D打印API，让系统自动完成搜索、模型生成、数据分析、模型修复、预览、打印及打印过程监控等步骤。该技术支持所有9款Bambu系列打印机。"
version: "0.10.6"
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

这是一个完整的人工智能3D打印技能，可以从聊天消息直接生成最终的打印成品。只需连接您的Bambu Lab打印机，并选择合适的3D生成API，其余的一切都将由我们的智能助手处理：从搜索模型到生成、分析、修复、预览，最后进行打印和监控。

该技能支持所有9款Bambu Lab打印机，并支持云端和局域网（LAN）两种连接模式。

## 安装

您可以通过克隆GitHub仓库来安装Bambu Studio AI：

**GitHub链接：** https://github.com/heyixuan2/bambu-studio-ai

---

## 快速参考

| 功能 | 命令 |
|------|---------|
| 检查打印机状态 | `python3 scripts/bambu.py status` |
| 查看打印进度 | `python3 scripts/bambu.py progress` |
| 开始打印 | `python3 scripts/bambu.py print <file>` |
| 暂停/恢复/取消打印 | `python3 scripts/bambu.py pause\|resume\|cancel` |
| 设置打印速度 | `python3 scripts/bambu.py speed silent\|standard\|sport\|ludicrous` |
| 打开/关闭打印机灯光 | `python3 scripts/bambu.py light on\|off` |
| 检查AMS耗材剩余量 | `python3 scripts/bambu.py ams` |
| 拍摄打印机截图 | `python3 scripts/bambu.py snapshot` |
| 发送G-code指令 | `python3 scripts/bambu.py gcode "G28"` |
| 从文本生成3D模型 | `python3 scripts/generate.py text "描述" --wait` |
| 从图片生成3D模型 | `python3 scripts/generate.py image photo.jpg --wait` |
| 查看模型生成状态 | `python3 scripts/generate.py status <task_id>` |
| 下载模型文件 | `python3 scripts/generate.py download <task_id> --format 3mf` |
| 打印前分析模型 | `python3 scripts/analyze.py model.3mf --material PLA --purpose functional` |
| 自动修复模型网格 | `python3 scripts/analyze.py model.3mf --repair --material PLA` |
| 单次打印检查 | `python3 scripts/monitor.py --once` |
| 持续监控打印过程 | `python3 scripts/monitor.py --interval 120` |
| 自动暂停打印 | `python3 scripts/monitor.py --interval 120 --auto-pause` |

---

## 检测触发器

当用户发出以下指令时，Bambu Studio AI会自动启动相应操作：

| 触发指令 | 动作 |
|---------|--------|
| "检查我的打印机状态" | `bambu.py status` |
| "打印进度如何了？" | `bambu.py progress` |
| "开始打印这个模型" | `bambu.py print <file>` |
| "将图片转换成3D模型" | `generate.py image` |
| "暂停/继续/取消打印" | `bambu.py pause\|cancel\|resume` |
| "加快打印速度" | `bambu.py speed` |
| "查看AMS耗材剩余量" | `bambu.py ams` |
| "打开/关闭打印机灯光" | `bambu.py light on\|off` |
| "查找模型" | `bambu.py snapshot` |
| "监控打印过程" | `bambu.py monitor` |

---

## 首次使用设置

如果`config.json`文件不存在，系统会引导用户完成以下设置步骤：

### 第1阶段：配置

1. **选择打印机型号**
   - 询问用户使用的是哪种Bambu Lab打印机，并展示相应的选项。

2. **选择连接模式**
   - 询问打印机的连接方式（LAN或Cloud），并指导用户设置相应的IP地址、序列号和访问代码。

3. **选择3D生成服务**
   - 提供多个3D生成服务的选项，并询问用户是否需要使用AI辅助生成模型。

4. **设置通知方式**
   - 询问用户希望接收通知的方式（电子邮件、Discord等）。

5. **保存配置**
   - 用户确认设置后，系统会生成`config.json`和`.secrets.json`文件。

### 第2阶段：验证设置

系统会提示用户确认配置是否正确，然后进行简单的测试。

### 第3阶段：模型搜索与生成

用户可以选择从在线数据库搜索模型，或使用AI生成模型。在生成模型之前，系统会提示用户确认打印需求和具体要求。

---

## 模型搜索与生成流程

- 如果用户需要打印某个具体物品，系统会先建议用户在线搜索现有的3D模型，或者使用AI生成模型。

- 在生成模型之前，系统会检查用户提供的尺寸和功能要求是否满足打印条件。

---

## 支持的打印机型号

Bambu Studio AI支持多种Bambu Lab打印机，并提供了相应的配置选项和连接模式。

---

## 配置文件

`config.json`文件包含了用户的配置信息，`.secrets.json`文件包含了敏感的访问代码。这些文件会随技能一起被上传到仓库中。

---

## 3D生成服务提供商

系统支持多个3D生成服务提供商，并提供了相应的API密钥和价格信息。

---

## 自动提示优化

系统会根据用户的需求自动优化生成的3D模型，以确保其适合打印。

---

## 注意事项

- 确保打印机和电脑处于同一局域网中，并正确配置连接参数。
- 使用AI生成模型时，请确保提供准确的尺寸和材质信息。
- 生成的模型可能需要用户在Bambu Studio中进行最后的检查和调整。

---

## 其他功能

系统提供了多种监控和自动化选项，以便用户更好地监控打印过程和解决可能出现的问题。