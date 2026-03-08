---
name: bambu-studio-ai
description: "**Bambu Lab 3D打印机控制与自动化系统**  
当用户提及以下关键词时，该系统会自动激活：打印机状态、3D打印、模型切片、模型分析、3D模型生成、AMS打印材料、打印监控、Bambu Lab或任何与3D打印相关的任务。整个工作流程包括：搜索 → 模型生成 → 模型分析 → 模型着色 → 预览 → 打开Bambu Lab软件 → 用户进行切片设置 → 打印 → 打印监控。该系统支持所有9款Bambu Lab打印机（A1 Mini、A1、P1S、P2S、X1C、X1E、H2C、H2S、H2D）。"
version: "0.22.28"
author: TieGaier
metadata:
  openclaw:
    emoji: "🖨️"
    os: ["macos"]
    os_note: "Core scripts (analyze, generate, colorize, search) work cross-platform. macOS required for: Bambu Studio integration (open -a), Homebrew cask installs, macOS notifications (osascript). Linux/Windows users can run the Python scripts directly but lose BS integration."
    requires:
      bins: ["python3", "pip3"]
    install:
      - id: pip-deps
        kind: pip
        packages: ["bambulabs-api", "bambu-lab-cloud-api", "requests", "trimesh", "numpy", "Pillow", "ddgs", "pygltflib", "cryptography", "paho-mqtt"]
        required: true
      - id: ffmpeg
        kind: brew
        package: ffmpeg
        optional: true
        label: "Camera snapshots (LAN mode)"
      - id: bambu-studio
        kind: cask
        package: bambu-studio
        optional: true
        label: "Model preview and manual slicing (macOS)"
      - id: blender
        kind: cask
        package: blender
        optional: true
        label: "Multi-color pipeline + HQ preview rendering (macOS)"
      - id: orcaslicer
        kind: cask
        package: orcaslicer
        optional: true
        label: "Optional CLI slicing backend (macOS)"
env:
  - name: BAMBU_MODE
    required: false
    description: "Connection mode: local (default, recommended) or cloud"
  - name: BAMBU_MODEL
    required: false
    description: "Printer model (e.g., H2D, A1 Mini, X1C)"
  - name: BAMBU_EMAIL
    required: false
    description: "Bambu account email (cloud mode only)"
  - name: BAMBU_IP
    required: false
    description: "Printer LAN IP (local mode only)"
  - name: BAMBU_SERIAL
    required: false
    description: "Printer serial number (local mode only)"
  - name: BAMBU_ACCESS_CODE
    required: false
    description: "LAN access code from printer touchscreen (local mode only)"
  - name: BAMBU_VERIFY_CODE
    required: false
    description: "Cloud login verification code (one-time, cloud mode only)"
  - name: BAMBU_DEVICE_ID
    required: false
    description: "Cloud device ID (auto-detected, cloud mode only)"
  - name: BAMBU_3D_PROVIDER
    required: false
    description: "AI 3D gen provider: meshy, tripo, printpal, 3daistudio, rodin (optional)"
  - name: BAMBU_3D_API_KEY
    required: false
    description: "API key for chosen 3D generation provider (optional)"
secrets:
  - name: BAMBU_PASSWORD
    required_when: "mode=cloud"
    storage: ".secrets.json"
    description: "Bambu Lab account password (cloud mode only)"
  - name: BAMBU_ACCESS_CODE
    required_when: "mode=local"
    storage: ".secrets.json"
    description: "LAN access code from printer Settings → Device (local mode only)"
  - name: BAMBU_3D_API_KEY
    required_when: "3D generation enabled"
    storage: ".secrets.json"
    description: "API key from chosen 3D generation provider (optional)"
security:
  no_credentials_shipped: true
  secrets_storage: ".secrets.json (chmod 600, git-ignored)"
  config_storage: "config.json (non-sensitive printer settings, git-ignored)"
  token_cache: ".token_cache.json (cloud auth token, 90d TTL, git-ignored). User can delete to force re-auth."
  verify_code_file: ".verify_code (one-time cloud login code, git-ignored)"
  files_gitignored: [".secrets.json", "config.json", ".token_cache.json", ".verify_code"]
  persistence: "Reads config.json at startup, .secrets.json on demand (lazy, not at import). Writes .token_cache.json, .verify_code locally. No remote data exfiltration."
  shipped_credentials: "NONE — no credentials, certificates, or keys are shipped or auto-downloaded."
  x509_setup: "User provides authentication certificate during setup if they enable Developer Mode auto-print. Stored locally in references/*.pem (git-ignored, key chmod 600). Not shipped, not downloaded by code."
  x509_scope: "Signs MQTT commands for LAN auto-print only. Requires user's own access code + same network."
  notifications: "Notifications use ONLY local macOS osascript (display notification) and a local JSONL log file. No external notification services (Discord/Telegram/Slack/etc.) are implemented in code — those are handled by the agent's own messaging tools if available. The skill itself makes NO outbound calls for notifications."
  network_access:
    - "Bambu Lab Cloud API (bambulab.com) — printer control, cloud mode only, requires user credentials"
    - "Bambu Lab MQTT (LAN, local network only) — printer control, local mode only"
    - "Meshy API (api.meshy.ai) — 3D generation, optional, requires user-provided API key"
    - "Tripo3D API (api.tripo3d.ai) — 3D generation, optional, requires user-provided API key"
    - "Hyper3D Rodin API (hyperhuman.deemos.com) — 3D generation, optional, requires user-provided API key"
    - "Printpal API — 3D generation, optional, requires user-provided API key"
    - "3D AI Studio API — 3D generation, optional, requires user-provided API key"
    - "DuckDuckGo (via ddgs library) — model search, no API key needed"
  consent: "All network calls, file writes, printer operations, and monitoring require explicit user consent. No credentials are auto-fetched or auto-stored without user confirmation."
keywords:
  - 3d printing
  - bambu lab
  - ams
  - text to 3d
  - slicing
  - print monitoring
  - multi-color
---
# 🖨️ Bambu Studio AI

**工作流程：**  
请求 → 收集信息 → 搜索/生成 → 分析 → [上色] → 预览 → 打开 Bambu Studio → 用户在 Bambu Studio 中进行切片 → 确认 → 打印 → 监控

**前置检查：**  
如果 `config.json` 不存在，则在任何操作之前先运行“首次设置”流程。

**每个操作开始前：**  
如果正在处理打印请求，请重新阅读流程检查表和合规性规则，确保没有跳过任何必填步骤。

---

## ⛔ 合规性规则 — 严格遵守  

**在每个操作之前，请确认您没有违反以下规则：**  
| 规则 | 含义 |  
|------|---------|  
| **必须** | 不可协商。跳过即失败。 |  
| **禁止** | 进行此操作即失败。 |  
| **等待** | 在用户响应之前请勿继续。 |  

### 绝对禁止的操作：  
- ❌ **绝不要跳过信息收集** — 必须询问：模型来源（搜索/生成）、尺寸、单色/多色、材料  
- ❌ **在没有尺寸信息的情况下绝不要生成模型** — 在运行 `generate.py` 之前必须询问“多高？例如，80毫米”  
- ❌ **绝不要跳过分析步骤** — 每个模型都必须通过 `analyze.py --orient --repair` 进行处理  
- ❌ **绝不要跳过预览步骤** — 在打开 Bambu Studio 之前必须将预览图像/GIF 发送到聊天界面。用户必须看到模型。  
- ❌ **绝不要直接自动打印** — 未经用户确认，切勿运行 `bambu.py` 进行打印。AI 模型可能存在问题。  
- ❌ **绝不要跳过模型来源的选择** — 必须询问用户：是搜索、生成还是不确定（默认为先搜索）  

### 必须执行的操作（按顺序）：  
1. **收集信息** → 询问模型来源、尺寸（如果需要生成）、颜色、材料  
2. **获取模型** → 根据用户选择进行搜索或生成  
3. **分析** → 对每个模型执行 `analyze.py --orient --repair`  
4. **预览** → 使用 `preview.py --views turntable` 预览模型，并将预览图像/GIF 发送到聊天界面  
5. **打开 Bambu Studio** → 使用 `open -a "BambuStudio" model.3mf`（或 model.stl/obj）打开文件  
6. **用户在 Bambu Studio 中进行切片** → 告诉用户进行切片、检查并确认  
7. **等待用户确认** → 在用户确认之前请勿继续  
8. **打印** → 仅在获得确认后进行打印  

> **注意：** `slice.py`（通过 OrcaSlicer 进行 CLI 切片）是**可选的**——仅在用户明确请求时使用。默认情况下，用户可以在 Bambu Studio 中自行切片，他们可以调整支撑结构、填充材料等设置。  

### 流程检查表（在完成操作前请核对）  
```
[ ] Info collected (source, dimensions, colors, material)
[ ] Model obtained (search/generate/download)
[ ] analyze.py --orient --repair run
[ ] Preview image/GIF sent to chat
[ ] Opened in Bambu Studio
[ ] User sliced + inspected in Bambu Studio
[ ] User confirmed "looks good" / "print it"
[ ] Print started (only after confirmation)
```  

---

## 快速参考  

| 您想要... | 对应命令 |  
|---|---|  
| 查看打印机状态 | `python3 scripts/bambu.py status` |  
| 查看打印进度 | `python3 scripts/bambu.py progress` |  
| 查看打印机硬件信息 | `python3 scripts/bambu.py info` |  
| 开始打印 | `python3 scripts/bambu.py print <file> --confirmed` |  
| 暂停/恢复/取消打印 | `python3 scripts/bambu.py pause\|resume\|cancel` |  
| 调整打印速度 | `python3 scripts/bambu.py speed silent\|standard\|sport\|ludicrous` |  
| 打开/关闭灯光 | `python3 scripts/bambu.py light on\|off` |  
| 查看 AMS 线材信息 | `python3 scripts/bambu.py ams` |  
| 拍摄相机快照 | `python3 scripts/bambu.py snapshot` |  
| 发送 G-code | `python3 scripts/bambu.py gcode "G28"` |  
| 发送通知 | `python3 scripts/bambu.py notify --message "done"` |  
| 生成 3D 模型（文本格式） | `python3 scripts/generate.py text "desc" --wait`（`--raw` 选项会忽略自动优化） |  
| 生成 3D 模型（图像格式） | `python3 scripts/generate.py image photo.jpg --wait` |  
| 下载模型文件 | `python3 scripts/generate.py download <task_id>` |  
| 分析模型 | `python3 scripts/analyze.py model.stl --orient --repair --material PLA` |  
| 仅保留模型主体部分（去除碎片） | `python3 scripts/analyze.py model.stl --repair --keep-main` |  
| 多色处理 | `python3 scripts/colorize.py model.glb --height 80 --max_colors 8 -o out.obj`（可调整参数：`--min-pct`, `--no-merge`, `--island-size`, `--smooth`, `--bambu-map`） |  
| 切片（可选的 CLI 功能） | `python3 scripts/slice.py model.stl --orient --arrange --quality fine` |  
| 特定设置下的切片 | `python3 scripts/slice.py model.stl --printer A1 --filament "Bambu PETG Basic"` |  
| 列出切片器配置文件 | `python3 scripts/slice.py --list-profiles` |  
| 快速预览 | `python3 scripts/preview.py model.stl` |  
| 高质量预览（使用 Blender） | `python3 scripts/preview.py model.stl --hq` |  
| 搜索模型 | `python3 scripts/search.py "phone stand" --limit 5` |  
| 监控打印过程 | `python3 scripts/monitor.py --auto-pause` |  
| 检查依赖项 | `python3 scripts/doctor.py` |  

所有脚本都支持 `--help` 参数。`generate.py` 会自动优化模型并限制模型尺寸以适应打印机打印范围。  

---

## 整体工作流程  
```
User Request
    │
    ▼
Information Collection
    │
    ▼
Decision 1: Model Source
    ├─ A: Internet Search (preferred default)
    ├─ B: AI Generate (single-color)
    ├─ C: AI Generate (multi-color)
    └─ D: User-provided file
    │
    ▼
Model Processing (analyze → repair → orient → [colorize])
    │
    ▼
Report Results to User
    │
    ▼
⛔ Open in Bambu Studio → User Inspects
    │
    ▼
User Confirms ("looks good" / "print it")
    │
    ▼
Decision 2: Print Method
    ├─ E: Auto Print (Developer Mode only, not recommended)
    └─ F: Manual Print (user handles in Bambu Studio)
    │
    ▼
Print Monitoring (both workflows, or on user request)
```  

---

## 第一步：信息收集  

**注意事项：**  
在任何搜索/生成/下载操作之前，您必须完成这一步。  

**收集的信息包括：**  
- 需要打印的模型信息（对象描述）  
- 目标尺寸（生成前必须询问，例如：“多高？例如，80毫米”）  
- 风格/外观（可选）  
- 打印参数：单色或多色（使用 AMS 线材）  
- 材料（默认为 PLA）  
- 打印质量：草图级/标准级/精细级/高级（可选）  
- 使用目的：功能性或装饰性（可选，这会影响模型的壁厚和填充方式）  

**询问用户模型来源：**  
> “您希望我：  
> 1. 🔎 在网上搜索现有的模型（通常质量更高）  
> 2. 🎨 使用 AI 从头开始生成模型  
> 3. 🤷 不确定——我先搜索一下，如果没有合适的模型再生成”  

**决策流程：**  
用户选择“搜索”/“生成”/“不确定” → 如果选择“不确定”，则先进行搜索；如果没有合适的模型，再提供生成选项。  

---

## 第二步：模型来源（决策点 1）  

**注意事项：**  
在此步骤之前，您必须已经询问用户：“是搜索、生成还是不确定？”默认选项是先搜索。  

### 工作流程 A — 互联网搜索（推荐）  
1. 使用 `search.py "query" --limit 5` 在 MakerWorld、Printables、Thingiverse、Thangs 等平台上搜索  
2. 向用户展示搜索结果，包括模型名称、来源和 URL  
3. 用户选择模型后下载，并验证模型格式（STL/OBJ/3MF）  
4. **模型处理**  

如果搜索结果不满意，建议用户使用 AI 生成模型。  

### 工作流程 B — 使用 AI 生成单色模型  

**生成前的注意事项：**  
- 之前是否询问了尺寸信息？如果没有，请现在询问。  
1. 首次使用 AI 生成模型时需提醒用户：AI 生成的模型可能不符合实际打印要求，请在 Bambu Studio 中进行再次检查。  
2. 确认尺寸信息后，运行 `generate.py`  
3. `generate.py` 会自动优化模型并限制模型尺寸  
4. 使用 `preview.py` 预览模型，并将预览图像/GIF 发送到聊天界面  
5. **模型处理**  

### 工作流程 C — 使用 AI 生成多色模型  

**生成前的注意事项：**  
- 之前是否询问了尺寸和颜色信息？如果没有，请现在询问。  
1. 同步骤 B 的注意事项  
2. 确认尺寸和颜色信息后，运行 `generate.py`  
3. `generate.py` 会生成带有颜色的 3D 模型（GLB 格式）  
4. 使用 `colorize.py` 对模型进行上色处理  
5. 将上色后的模型预览图像发送给用户  
6. **分析结果并建议调整参数（如有必要）：**  
   - 显示检测到的颜色（包括名称、十六进制代码和占比）  
   - 如果某些颜色（如眼睛、装饰性元素）的占比过低（<1%），建议调整 `--min-pct` 参数  
   - 如果颜色混合不准确（例如黄色主体和棕色裤子），建议关闭 `--no-merge` 选项  
   - 如果颜色分布不均匀，建议调整 `--island-size` 或 `--smooth` 参数  
7. 如果用户需要修改参数，重新运行 `colorize.py` 并显示新的预览结果  
8. 用户确认后，继续进行模型处理  

**上色参数可调整范围：**  
| 参数 | 默认值 | 效果 |  
|-----------|---------|--------|  
| `--max_colors N` | 8 | 最大允许的颜色数量（AMS 线材限制为 8）  
| `--min-pct X` | 0.1 | 颜色家族的最低占比阈值（0 表示保留所有颜色，5 表示严格过滤）  
| `--no-merge` | 关闭 | 禁用颜色家族间的合并功能  
| `--island-size N` | 1000 | 删除小于 N 像素的孤立颜色块  
| `--smooth N` | 5 | 调整颜色过渡的平滑度（0 表示原始效果，数值越大越平滑）  
| `--bambu-map` | 关闭 | 生成包含推荐使用的 Bambu 线材颜色的 `_color_map.txt` 文件（基于 CIELAB 色彩空间） |

### 工作流程 D — 使用用户提供的模型文件  

1. 验证模型格式（STL/OBJ/3MF/GLB），必要时进行转换  
2. **模型处理**  

---

## 第三步：模型处理  

**注意事项：**  
在此步骤之前，您必须已经获取到模型文件（无论是通过搜索、生成还是用户提供的）。所有模型都必须经过这一步骤。**绝对不能跳过分析或预览步骤。**  

**分析步骤（包含 11 项检查）：**  
```
analyze.py model.stl --orient --repair --material PLA --purpose functional
```  
检查内容包括：尺寸公差、壁厚、悬垂部分、打印方向、层高、填充比例、壁层数量、顶层数量、材料兼容性等。此外还会检查模型的防水性和打印可行性。  

**自动修复步骤：**  
修复模型的法线方向、填充孔洞、删除不稳定的面。  

**自动调整模型方向：** 优化模型的稳定性，并自动检测模型的单位尺寸（单位转换：米→毫米）。  

**必须向用户报告的内容：**  
- 打印可行性评分（0-10 分）  
- 报告存在的问题和修复措施  
- 建议的打印参数（层高、填充比例、壁层厚度、温度设置等）  

**示例报告：**  
“评分：8/10。修复了 58,000 个不稳定的边缘。壁层厚度：1.5毫米。建议的打印参数：层高 0.20毫米，填充比例 20%，使用 PLA 线材，打印温度 210°C。”  

**预览步骤（必须执行）：**  
```
preview.py model.stl --views turntable -o model_preview.gif
```  
- 单色模型：使用默认的蓝色材料进行渲染  
- 多色模型：使用上色后的模型进行渲染  
- **必须将预览图像/GIF 发送到聊天界面**——用户必须看到预览结果才能继续下一步  
- 如果模型预览显示速度过慢，可以使用 `--views perspective` 参数快速查看模型  

**可选的 CLI 切片功能（仅用户请求时使用）：**  
```
slice.py model.stl --orient --arrange --quality standard
```  
该功能会自动检测打印机和喷嘴类型，并设置打印质量（草图级/标准级/精细级/高级）。输出格式为 `.3mf`，同时生成相应的 G-code 文件。  

---

## 第四步：用户确认  

**注意事项：**  
**必须执行此步骤（绝不能跳过）：**  
1. 在 Bambu Studio 中打开模型文件：`open -a "BambuStudio" model.3mf`（或 .stl/.obj）  
2. 告诉用户进行检查和切片：  
   > “我已经在 Bambu Studio 中打开了模型。请检查：  
   > - 模型是否正确？是否有缺失或变形的部分？  
   > - 是否有悬垂部分？  
   > - 尺寸是否正确？（在底部栏中查看尺寸）  
   > 在 Bambu Studio 中进行切片操作（使用 Ctrl+R 或 Cmd+R），并查看预计的切片时间和耗材用量。  
   > 完成后请告诉我！”  
3. **等待用户的明确确认**。  

**注意：** 绝不要自动开始打印。AI 模型可能存在问题，自动打印可能导致错误。  

**询问用户打印方式：**  
- **自动打印**：仅适用于开发者模式（不推荐）。  
- **手动打印**：用户在 Bambu Studio 中手动调整参数后进行打印。  

---

## 第五步：打印执行（决策点 2）  

### 工作流程 E — 自动打印（仅适用于开发者模式，不推荐）  
⚠️ 需要开启开发者模式。此时 Bambu Studio 和 Bambu Handy 会断开连接。  
1. 运行 `bambu.py print model.3mf --confirmed`  
2. 确认：“打印已经开始！”  
3. **监控打印过程**  

### 工作流程 F — 手动打印  
- 模型已经在 Bambu Studio 中打开  
- 用户在 Bambu Studio 中手动调整参数并执行打印。  

**打印监控方法：**  
- **主动监听**：在模型开始打印后，立即启动后台 MQTT 监听器（持续 30 分钟）。如果打印机状态变为“RUNNING”，立即通知用户并提供实时监控功能。  
- **心跳检测**：在常规监控期间，定期检查打印器的状态。如果发现异常，立即通知用户。  

---

## 第六步：打印监控  

**触发条件：**  
自动打印（工作流程 E）、手动打印（工作流程 F）或用户请求。  

**注意事项：**  
**务必询问用户是否需要监控打印过程。**  
**监控方法：** 通过 paho-mqtt 协议进行实时监控（不要使用 bambulabs_api，因为它可能存在 SSL 问题）。  
连接地址：`{printer_ip}:8883`，订阅 `device/{serial}/report` 路由。  

**监控期间必须执行的操作：**  
- 使用 `bambu.py snapshot` 命令通过 RTSP 协议拍摄相机快照，并将快照发送给用户。  
- 在每次进度更新时发送快照给用户。  
**默认的监控间隔：** 每次打印完成时发送 5 条通知。  

**异常情况处理：**  
- **打印进度停滞超过 10 分钟**：立即通知用户并发送快照。  
- **温度异常**：立即通知用户并发送快照。  
- **打印失败/异常情况**：立即通知用户并发送快照。  
- **其他异常情况**：立即通知用户并发送快照。  

**状态报告格式（发送给用户）：**  
```
🖨️ Print Update — {filename}
📊 Progress: {percent}% | Layer {current}/{total}
⏱️ Remaining: {time}
🔥 Nozzle: {temp}°C | 🛏️ Bed: {temp}°C
📸 [attached snapshot]
```  

---

## 首次设置流程  

当 `config.json` 不存在时，系统会自动执行首次设置流程。  
**设置内容包括：**  
- **打印机型号**（A1 Mini、A1、P1S、P2S、X1C、X1E、H2C、H2S、H2D）  
- **连接方式**（推荐使用 LAN 连接：IP 地址 + 密码；也可以使用云连接）  
- **打印模式**：  
  - **选项 A**：推荐模式——代理程序生成模型，用户在 Bambu Studio 中进行切片和打印，无需特殊设置。  
  - **选项 B**：完全自动打印模式——代理程序直接控制打印机（包括启动/停止/监控）。  
    - 注意：必须开启开发者模式（打印机触摸屏 → 设置 → 仅允许 LAN 连接）。  
    - 使用此模式时，Bambu Studio 和 Bambu Handy 会完全断开连接（无法远程监控）。  
    - 仅支持 LAN 连接。  
    - 打印前系统会始终显示模型预览。  
- **3D 生成选项**（可选）：需要安装相应的插件（Meshy、Tripo、Printpal、3D AI Studio 和 API 密钥）。  
- **通知设置**：系统会自动发送通知。  
- **保存设置**：将配置信息保存到 `config.json` 和 `.secrets.json` 文件中（权限设置为 600）。  
- **验证设置**：测试连接、相机和 AMS 线材的兼容性。  

---

## 环境要求和依赖项  

**必备软件：**  
`python3` 和 `pip3`（推荐在 macOS 上使用；核心脚本支持跨平台运行）  
**可选软件（macOS 上推荐使用）：** `ffmpeg`（用于拍摄相机快照）、Bambu Studio（用于模型预览和切片）、Blender 4.0 或更高版本（用于多色模型预览和高质量预览）、OrcaSlicer（用于 CLI 切片）。  

**环境变量（可覆盖配置文件中的设置）：**  
`BAMBU_MODE`、`BAMBU_MODEL`、`BAMBU_EMAIL`、`BAMBU_IP`、`BAMBU_SERIAL`、`BAMBU_3D_PROVIDER`  

**保密信息（保存在 `.secrets.json` 文件中，权限设置为 600）：**  
`password`、`access_code`、`3d_api_key`。这些信息由用户自行提供，不会随软件一起发送。  

---

## 常见错误及解决方法：**  
| 错误 | 正确的操作方式 |  
|---------|------------------|  
| 跳过“搜索还是生成”的选择** | 必须先询问用户。默认选项是搜索。  
| 未询问尺寸信息就直接生成模型** | 必须询问模型尺寸（例如：“多高？例如，80毫米”）。  
| 生成模型后直接打开 Bambu Studio** | 必须先运行 `analyze.py` 和 `preview.py`。  
| 未发送预览图像就直接开始打印** | 必须将预览图像发送给用户。  
| 未得到用户确认就直接开始打印** | 必须等待用户的确认。  
| 因为模型是搜索结果就跳过分析步骤** | 所有模型都需要分析，因为搜索结果也可能存在问题。  
| 模型碎片过多时重新生成** | 先查看预览结果；如果模型只是外观上有小碎片，可以使用 `--keep-main` 参数。  

---

## 常见问题及解决方法：**  
| 问题 | 解决方案 |  
|---|---|  
| SSL 连接失败**：**正常现象（使用自签名证书）。系统会自动处理。**  
| 无法找到 API 方法**：`pip3 install --upgrade bambulabs-api`（版本 2.6.6 或更高版本）。  
| 无法连接**：确保 LAN 模式已开启，IP 地址正确，且处于同一网络范围内。  
| 云连接验证失败**：等待系统发送的验证代码，该代码有效期为 90 天。  
| 相机连接失败**：唤醒打印机并检查 IP 地址。  
| AI 模型存在问题（如孔洞或悬垂部分）**：正常现象，运行 `analyze.py --repair` 可以修复这些问题。  
| Tripo/Meshy 生成多个模型片段**：通常是无害的情况（可能是模型拓扑结构问题）。先查看模型预览；如果模型确实损坏，可以使用 `--keep-main` 参数。  

## 已知的系统限制：**  
| 功能 | 状态 |  
|---|---|  
| 单色打印流程**：**稳定可用。**  
| 多色打印（上色功能）**：**自动识别最多 8 种颜色，并在 Bambu Studio 中选择颜色。**  
| CLI 切片功能**：**OrcaSlicer 后端在版本 2.5.0 中存在问题（可能导致 SEGFAULT）。**  
| 自动完成打印**：**在开发者模式下可用（需要启用 MQTT 协议和 FTP 上传功能）。  

## 参考文档：**  
- `references/model-specs.md`：所有打印机的规格信息  
- `references/bambu_filament_colors.json`：Bambu Lab 提供的 43 种颜色调色板（仅用于参考，彩色模型使用原始颜色）  
- `references/bambu-mqtt-protocol.md`：MQTT 协议文档  
- `references/bambu-cloud-api.md`：云 API 文档  
- `references/3d-generation-apis.md`：3D 模型生成的 API 文档  
- `references/3d-prompt-guide.md：3D 模型生成的提示指南  

## 许可证信息：**  
MIT 许可证；GitHub 仓库：https://github.com/heyixuan2/bambu-studio-ai