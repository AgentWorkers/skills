---
name: bambu-studio-ai
description: "**Bambu Lab 3D打印机控制与自动化系统**  
当用户提及以下关键词时，该系统会自动启动：打印机状态、3D打印、模型切片、模型分析、3D模型生成、AMS耗材、打印监控、Bambu Lab或任何与3D打印相关的任务。  
**完整工作流程：**  
搜索 → 模型生成 → 模型分析 → 模型着色 → 预览 → 打开Bambu Lab软件 → 用户进行模型切片 → 开始打印 → 打印过程监控。  
**兼容机型：**  
该系统支持Bambu Lab的所有9款3D打印机：A1 Mini、A1、P1S、P2S、X1C、X1E、H2C、H2S、H2D。"
version: "1.0.1"
license: MIT
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
        packages: ["bambulabs-api", "bambu-lab-cloud-api", "requests", "trimesh", "numpy", "Pillow", "ddgs", "pygltflib", "cryptography", "paho-mqtt", "scipy", "manifold3d"]
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
请求 → 收集信息 → 搜索/生成 → 分析 → [着色] → 预览 → 打开Bambu Studio → 在Bambu Studio中进行切片 → 确认 → 打印 → 监控

**预检查：**  
如果`config.json`文件不存在，请在执行任何操作之前先运行首次设置。

**每个操作开始前：**  
如果正在处理打印请求，请重新阅读流程检查表和合规规则，确保没有跳过任何必填步骤。

---

## ⛔ 合规规则 — 严格遵守  

**在每个操作之前，请确认您没有违反以下规则：**  
| 规则 | 含义 |  
|------|---------|  
| **必填** | 不可协商。跳过 = 失败。 |  
| **禁止** | 禁止这样做。否则会导致失败。 |  
| **等待** | 在用户响应之前不要继续。 |  

### 绝对不能做：  
- ❌ **绝不要跳过信息收集** — 必须询问：模型来源（搜索/生成）、尺寸（如果需要生成）、单色/多色、材料  
- ❌ **在没有尺寸信息的情况下生成模型** — 在运行`generate.py`之前必须询问“多大？例如，80毫米高”  
- ❌ **绝不要跳过分析** — 每个模型都必须通过`analyze.py --orient --repair`处理  
- ❌ **绝不要跳过预览** — 在打开Bambu Studio之前必须将预览图像/GIF发送到聊天窗口。用户必须看到模型。  
- ❌ **绝不要自动打印** — 未经用户确认，不得使用`bambu.py`进行自动打印。AI模型可能存在错误。  
- ❌ **绝不要跳过模型来源的选择** — 必须询问用户：是搜索、生成还是不确定（默认：先搜索）  

### 必须按顺序执行的步骤：  
1. **收集信息** → 询问模型来源、尺寸（如果需要生成）、颜色、材料  
2. **获取模型** → 根据用户选择进行搜索或生成  
3. **分析** → 对每个模型执行`analyze.py --orient --repair`  
4. **在聊天窗口中预览** → 使用`preview.py --views turntable`预览，并将图像/GIF发送给用户  
5. **打开Bambu Studio** → 使用`open -a "BambuStudio" model.3mf`（或.model.stl/obj）打开模型  
6. **在Bambu Studio中进行切片** → 告诉用户进行切片、检查并确认  
7. **等待用户确认** → 在用户确认之前不要继续  
8. **打印** → 只有在用户确认后才能打印  

> **注意：** `slice.py`（通过OrcaSlicer进行CLI切片）是**可选的** — 仅当用户明确请求时使用。默认情况下，用户可以在Bambu Studio中自行切片，他们可以调整支撑结构、填充材质等设置。  

### 流程检查表（在声称完成之前请验证）  
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

| 我想... | 命令 |  
|---|---|  
| 打印机状态 | `python3 scripts/bambu.py status` |  
| 打印进度 | `python3 scripts/bambu.py progress` |  
| 打印机硬件信息 | `python3 scripts/bambu.py info` |  
| 开始打印 | `python3 scripts/bambu.py print <file> --confirmed` |  
| 暂停/恢复/取消 | `python3 scripts/bambu.py pause\|resume\|cancel` |  
| 速度模式 | `python3 scripts/bambu.py speed silent\|standard\|sport\|ludicrous` |  
| 灯源开关 | `python3 scripts/bambu.py light on\|off` |  
| AMS线材信息 | `python3 scripts/bambu.py ams` |  
| 摄像头快照 | `python3 scripts/bambu.py snapshot` |  
| 发送G代码 | `python3 scripts/bambu.py gcode "G28"` |  
| 通知 | `python3 scripts/bambu.py notify --message "完成"` |  
| 生成3D模型（文本） | `python3 scripts/generate.py text "desc" --wait --height 80` （`--raw`跳过自动增强；`--height`设置目标高度，默认为80毫米） |  
| 生成3D模型（图像） | `python3 scripts/generate.py image photo.jpg --wait --height 80` （自动：验证、去除背景、提示增强；`--no-bg-remove`/`--raw`跳过） |  
| 下载模型 | `python3 scripts/generate.py download <task_id> --height 80` |  
| 分析模型 | `python3 scripts/analyze.py model.stl --height 80 --orient --repair --material PLA` （使用`--height`时总是输出 `_scaled`文件） |  
| 仅保留主体部分（去除碎片） | `python3 scripts/analyze.py model.stl --repair --keep-main` |  
| 多色模型 | `python3 scripts/colorize model.glb --height 80 --max_colors 8 -o out.obj` （可调整参数：`--min-pct`、`--no-merge`、`--island-size`、`--smooth`、`--bambu-map`） |  
| 切片（可选的CLI命令） | `python3 scripts/slice.py model.stl --orient --arrange --quality fine` |  
| 特定设置的切片 | `python3 scripts/slice.py model.stl --printer A1 --filament "Bambu PETG Basic"` |  
| 列出切片器配置文件 | `python3 scripts/slice.py --list-profiles` |  
| 快速预览 | `python3 scripts/preview.py model.stl` （`--height 80`用于验证尺寸） |  
| 高质量预览（Blender） | `python3 scripts/preview.py model.stl --hq` |  
| 搜索模型 | `python3 scripts/search.py "phone stand" --limit 5` |  
| 监控打印过程 | `python3 scripts/monitor.py --auto-pause` |  
| 检查依赖项 | `python3 scripts/doctor.py` |  
| 参数化建模 | `python3 scripts/parametric.py box 30 20 10 -o box.stl` |  
| 参数化圆柱体 | `python3 scripts/parametric.py cylinder --radius 5 --height 20 -o cyl.stl` |  
| 参数化支架 | `python3 scripts/parametric.py bracket --width 30 --height 40 --thickness 3 --hole-diameter 3.2 -o bracket.stl` |  
| 带孔的参数化板 | `python3 scripts/parametric.py plate-with-holes --width 60 --depth 40 --holes 4 --hole-diameter 3.2 --hole-spacing 25 -o plate.stl` |  
| 参数化外壳 | `python3 scripts/parametric.py enclosure --width 60 --depth 40 --height 30 --wall 2 --lid -o case.stl` |  
| 参数化CSG模型（复杂形状） | `python3 scripts/parametric.py csg spec.json -o assembly.stl` |  

所有脚本都支持`--help`命令。`generate.py`会自动增强模型并限制尺寸以适应打印机打印范围。  

---

## 整体流程  
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
    ├─ D: User-provided file
    ├─ E: Image to 3D
    └─ F: Parametric (functional parts — manifold3d)
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

## 第1步：信息收集  

**注意：**  
在进行任何搜索/生成/下载之前，必须完成这一步。  

**收集的信息包括：**  
- 需要打印的模型（对象描述）  
- 目标尺寸（在生成之前必须询问，例如：“多大？例如，80毫米高”）  
- 风格/外观（可选）  
- 打印参数：  
  - 单色或多色（AMS）  
  - 材料（默认：PLA）  
  - 质量：草图级/标准级/精细级/高级（可选）  
  - 用途：功能性或装饰性（可选，影响壁厚和填充材质）  

**询问用户模型来源：**  
> “您希望我：  
> 1. 🔎 在网上搜索现有的模型（通常质量更高）  
> 2. 🎨 使用AI从头开始生成模型  
> 3. 🤷 不确定——我会先搜索，如果没有合适的模型再生成”  

**决策流程：**  
用户选择“搜索”/“生成”/“不确定” → 如果选择“不确定”——先搜索 → 如果没有合适的模型——提供生成选项。  

**自动路由（根据用户描述确定路径）：**  
| 用户描述中的关键词 | 路由 | 示例 |  
|------------------------------|----------|----------|  
| 具体尺寸/公差/适配性 | 参数化建模（Workflow F） | “M3螺丝孔”、“内径40毫米”、“压合适配” |  
| 标准接口/安装方式 | 参数化建模（Workflow F） | “USB-C接口”、“GoPro支架”、“VESA接口” |  
| 功能性部件 | 参数化建模（Workflow F） | “支架”、“铰链”、“夹子”、“齿轮”、“安装件”、“外壳”、“支架” |  
| 字符/人物/有机形状 | AI生成（Workflow B/C） | “皮卡丘”、“龙”、“半身像”、“雕塑” |  
| 装饰性/艺术性设计 | AI生成（Workflow B/C） | “花瓶”、“灯罩”、“桌面装饰品” |  
| 使用图片参考 | 从图片生成3D模型（Workflow E） | 用户提供图片文件或URL |

当描述明确符合功能性或精确性要求时，直接跳过模型来源的询问，直接使用参数化建模流程。如果描述不明确（例如“手机支架”——可以选择搜索或参数化建模）。  

---

## 第2步：模型来源（决策点1）  

**注意：**  
在此步骤之前，必须询问用户：“是搜索、生成还是不确定？”默认选项是搜索。  

### 工作流程A — 网上搜索（推荐）  
1. `search.py "query" --limit 5` → 在MakerWorld、Printables、Thingiverse、Thangs等平台上搜索  
2. 显示结果，包括模型名称、来源和URL  
3. 用户选择模型 → 下载 → 验证文件格式（STL/OBJ/3MF）  
4. → 进行模型处理  

如果没有合适的模型结果，提供AI生成选项。  

### 工作流程B — AI生成（单色模型）  
**生成前的检查点：** 是否询问了尺寸？如果没有，请现在询问。  
1. 首次使用时的注意事项：“AI生成的模型依赖于提供者和输入的描述。这些模型可能不适合直接打印，请在Bambu Studio中再次检查。”  
2. 确认尺寸——在运行`generate.py`之前必须提供尺寸信息  
3. `generate.py text "prompt" --wait --height <mm>` → 自动增强模型并调整大小  
4. `preview.py model.stl --views turntable --height <mm> -o preview.gif` → 将预览图像发送到聊天窗口（验证尺寸）  
5. → 进行模型处理  

### 工作流程C — AI生成（多色模型）  
**生成前的检查点：** 是否询问了尺寸？如果没有，请现在询问。  
**注意：** 不要提前询问用户颜色——AI会根据模型纹理自动选择颜色。  
1. 与工作流程B相同的安全提示  
2. 仅确认尺寸：“您想要多大的模型？”  
   - 颜色由AI根据纹理自动选择  
   - 如果用户指定了颜色偏好（例如“只使用3种颜色”），请记录下来以便后续着色  
3. `generate.py text "prompt" --wait --height <mm>` → 生成带颜色的GLB模型（自动调整大小）  
4. `python3 scripts/colorize model.glb --height <mm> --max_colors 8 --bambu-map` → 生成带有颜色信息的OBJ文件和 `_color_map.txt`  
5. `preview.py model.obj --views turntable --height <mm> -o preview.gif`  
6. **发送综合报告**（必须包含以下内容）：  
   > ## 🎨 [模型名称] 多色预览  
   > 📷 [附上预览图像（preview.png）和旋转图像（turntable.gif）  
   > | 颜色 | 十六进制代码 | 颜色百分比 | 建议使用的线材 | 色差（ΔE） |
   |---|-------|-----|---|--------------------|----|  
   > | 1 | 黄色 | #FFD700 | 58% | PLA Basic Yellow | 3.2 |  
   | 2 | 棕色 | #8B4513 | 22% | PLA Basic Brown | 5.1 |  
   | ... | | | | |  
   > **检测到N种颜色，兼容AMS打印机。** 是否继续？  
   > - 如果需要减少颜色数量 → 可以重新运行命令并指定`--max_colors N`  
   - 如果需要调整颜色 → 告诉我具体要求  
   - 如果预览效果满意 → 我会在Bambu Studio中打开模型进行进一步处理  

**注意：** Bambu Studio可能无法识别模型的顶点颜色——请参考步骤4中的导入方法。  

**着色调整（仅用户请求时使用）：**  
| 参数 | 默认值 | 效果 |  
|-----------|---------|--------|  
| `--max_colors N` | 8 | 最大允许的颜色数量（AMS打印机最多支持8种颜色） |  
| `--min-pct X` | 0.1 | 颜色家族的最低显示百分比（0表示保留所有颜色，5表示严格过滤） |  
| `--no-merge` | 关闭 | 禁用颜色家族的合并功能（每个颜色独立显示） |  
| `--island-size N` | 1000 | 删除小于N像素的孤立色块（0表示关闭该功能） |  
| `--smooth N` | 5 | 根据颜色分布确定显示颜色（0表示原始颜色，数值越大显示效果越平滑） |  
| `--bambu-map` | 启用 | 生成包含建议使用的Bambu线材颜色的 `_color_map.txt`文件 |  

### 工作流程D — 用户提供的文件  
1. 验证文件格式（STL/OBJ/3MF/GLB），必要时进行转换  
2. → 进行模型处理  

### 工作流程E — 从图片生成3D模型  
**触发条件：** 用户提供图片或图片URL  
**检查点：** 是否询问了尺寸？如果没有，请现在询问。不要询问颜色——颜色信息来自图片。  
1. 与工作流程B相同的安全提示  
2. 仅确认尺寸  
3. 将图片保存到工作区（如果通过聊天窗口提供）或记录文件路径/URL  
4. `python3 scripts/generate.py image photo.jpg --wait` （自动处理：去除背景、增强图像）  
   - 要忽略背景去除功能：添加`--no-bg-remove`参数  
   - 要忽略颜色增强功能：添加`--raw`参数  
5. **自动判断单色或多色模型：**  
   - 如果下载的GLB文件包含纹理，则使用工作流程C的步骤进行着色处理，并发送综合报告  
   - 如果文件没有纹理，则使用工作流程B的步骤进行单色处理  
6. 向用户展示预览结果并等待确认  
7. 用户确认后进行模型处理  

**获取最佳效果的提示：**  
- 使用纯白色背景的清晰产品图片  
- 确保对象居中且光线充足  
- 不支持从多个角度拍摄同一对象（只能使用单张图片）  
- 如果去除背景会影响效果，可以使用`--no-bg-remove`参数重新处理图片  

### 工作流程F — 参数化建模（功能性部件）  
**触发条件：** 用户请求具有精确尺寸、标准接口（如螺丝孔、安装孔）或特定功能的部件  
**注意：** 必须提供准确的尺寸（以毫米为单位）。不要使用模糊的尺寸描述（例如“大约80毫米”）。  
1. 收集所有详细尺寸：宽度、高度、深度、壁厚、孔径、孔间距  
2. 选择合适的`parametric.py`命令：  
   - 简单形状：`box`、`cylinder`、`sphere`、`extrude`  
   - 支架：`bracket --width W --height H --thickness T --hole-diameter D`  
   - 安装板：`plate-with-holes --width W --depth D --holes N --hole-hole-distance S`  
   - 外壳：`enclosure --width W --depth D --height H --wall T --lid`  
   - 复杂结构：编写JSON规格文件，使用`csg spec.json`  
3. `python3 scripts/parametric.py <命令> [参数] -o model.stl`  
4. `preview.py model.stl --views turntable -o preview.gif` → 将预览图像发送到聊天窗口  
5. 向用户报告尺寸、模型体积和三角形数量  
6. **等待用户确认** — 用户可能要求调整尺寸  
7. 如有需要，修改参数并重新生成模型，然后再次预览  
8. 用户确认后进行模型处理  

**与AI生成的模型相比的优势：**  
- 尺寸精确到0.01毫米  
- 模型结构稳定（无需修复）  
- 生成速度快（无需API调用，无需等待）  
- 免费使用（不消耗API接口费用）  
- 结果可重复（相同的参数会生成相同的模型）  

**限制：**  
- 仅支持几何形状，不支持有机或艺术性的设计  
- 输出格式为单色STL文件，不支持顶点颜色或纹理  

**参考资料：**  
请参阅`references/manifold-examples.md`以获取公差表、CSG模型规格和设计规则。  

---

## 第3步：模型处理  

**注意：**  
在此步骤之前，必须已经有了模型文件（无论是通过搜索、生成还是用户提供的）。所有模型都必须经过这一步。**绝对不能跳过分析或预览。**  

**分析步骤（11项检查）：**  
检查尺寸公差、壁厚、悬垂部分、打印方向、层高、填充比例、壁厚分布、顶层数量、材料兼容性等。同时检查模型是否防水、结构是否完整、模型体积是否适合打印。  

**自动修复：** 修复模型的法线方向、填充孔洞、删除不完整的面。  

**自动调整模型方向：** 优化模型的稳定性，并自动检测模型的单位尺寸（从米转换为毫米）。  

**必須向用户报告：**  
- 打印可行性评分（0-10分）  
- 报告存在的问题和修复情况  
- 建议的打印参数（层高、填充比例、壁厚、温度设置等）  

**示例报告：**  
“评分：8/10。修复了58,000个不完整的边缘。壁厚：1.5毫米。悬垂部分：3.2%。建议的打印参数：层高0.20毫米，填充比例20%，使用PLA材料。”  

**预览渲染步骤（必填）：**  
- 单色模型：使用默认的蓝色材料渲染STL/3MF文件  
- 多色模型：使用带有顶点颜色的OBJ文件进行渲染  
**必须将预览图像/GIF发送到聊天窗口**——用户必须看到预览结果才能继续下一步  
- 如果旋转预览显示速度太慢，可以使用`--views perspective`选项查看单张图像  
**注意：** 确保在打开Bambu Studio之前已将预览图像附在消息中  

**可选的CLI切片功能（仅用户请求时使用）：**  
自动检测打印机和喷嘴类型。切片质量分为草图级（0.24）、标准级（0.20）、精细级（0.12）和高级级（0.08）。输出格式为`.3mf`文件，同时生成G代码。  

---

## 第4步：用户确认  

**注意：**  
**必填步骤：** 在进行下一步之前，必须将预览图像发送到聊天窗口。**  
1. 在Bambu Studio中打开模型：`open -a "BambuStudio" model.3mf`（或.model.stl/.obj）  
2. **对于多色模型（导入过程可能不稳定）：**  
   - 必须通过**文件 → 新项目 → 导入**的方式打开模型  
   - 导入后：检查颜色数量——如果Bambu Studio显示的颜色数量不正确：  
     1. 完全关闭Bambu Studio，重新打开后再导入  
     2. 或将OBJ文件拖放到Bambu Studio的空窗口中  
   - 如果Bambu Studio仍然无法识别颜色信息，请标记为导入兼容性问题，不要重新执行着色操作  
3. 告诉用户检查模型：  
   > “我已经在Bambu Studio中打开了模型。请检查：  
   > - 模型是否显示正确？是否有缺失或变形的部分？  
   > - 检查是否有悬垂的部分？  
   > - 尺寸是否正确？（在底部栏中查看）  
   > **对于多色模型：** 确保显示的颜色数量正确  
   > 在Bambu Studio中进行切片（使用Ctrl+R或Cmd+R），然后查看预计的切片时间、线材使用量等信息  
   > 完成后请告诉我！”  
4. **等待用户的明确确认。**  

**注意：** 绝不要自动开始打印。AI模型可能存在问题，分析步骤可能无法完全检测到这些问题。  

**询问用户打印方式：**  
- 直接自动打印：仅适用于开发者模式（不推荐）  
- 在Bambu Studio中手动进行打印：使用工作流程F。  

---

## 第5步：打印执行（决策点2）  

### 工作流程E — 自动打印（仅适用于开发者模式）  
**注意：** 需要开启开发者模式。Bambu Studio和Bambu Handy工具会断开连接。  
1. `bambu.py print model.3mf --confirmed`  
2. 确认：“打印开始！”  
3. **监控打印过程。**  

### 工作流程F — 手动打印**  
- 模型已经打开在Bambu Studio中  
- 用户在Bambu Studio中手动调整参数并开始打印  

**打印监控方法：**  
1. **主动监听：** 当Bambu Studio开始打印时（工作流程B/C/D），立即启动后台MQTT监听器（持续30分钟）。如果打印机状态变为“RUNNING”，则通知用户并开始监控。  
   - 实现方式：在后台运行`exec`脚本，每隔30秒检查打印机状态  
   - 如果30分钟后没有检测到打印操作，自动停止监控  
2. **心跳检测：** 在常规监控期间，定期检查打印机的MQTT状态。如果打印机处于运行状态但未进行监控，也会通知用户。  

**监控方法：**  
需要通过MQTT协议（`paho-mqtt`）进行实时监控。连接地址：`{printer_ip}:8883`，订阅`device/{serial}/report`消息。  
**监控期间必须拍摄摄像头快照：**  
- 使用`bambu.py snapshot`命令通过RTSP协议捕获快照（路径：`bblp:{code}@{ip}:322/streaming/live/1`）  
- 将快照与打印进度信息一起发送给用户  
- 在异常情况下立即发送快照和警报  

**默认的监控计划（基于打印阶段）：**  
| 事件 | 触发条件 | 操作 |  
|---|---|---|  
| 打印开始 | 打印器状态变为“RUNNING” | 发送通知和快照 |  
| 进度达到25% | 进度达到25% | 发送进度信息和快照 |  
| 进度达到50% | 进度达到50% | 发送进度信息和快照 |  
| 打印完成 | 打印完成 | 发送完成信息和最终快照 |  
| 出现异常 | 任何异常情况 | 立即发送警报和快照 |  

用户可以调整监控频率。通过监控进度信息避免重复报告。  

**异常处理：**  
| 异常类型 | 处理方式 |  
|---|---|---|  
| 打印进度停滞超过10分钟 | 发送警报 |  
| 温度异常 | 发送警报 |  
| 打印失败/异常 | 发送警报 |  
| 打印机断开连接 | 发送警报 |  
| 打印过程中出现意外情况 | 发送警报 |  

**状态报告格式（发送给用户）：**  
```
🖨️ Print Update — {filename}
📊 Progress: {percent}% | Layer {current}/{total}
⏱️ Remaining: {time}
🔥 Nozzle: {temp}°C | 🛏️ Bed: {temp}°C
📸 [attached snapshot]
```  

---

## 首次设置  
当`config.json`文件不存在时，会触发首次设置流程。  
**内容包括：**  
1. **打印机型号**：A1 Mini、A1、P1S、P2S、X1C、X1E、H2C、H2S、H2D  
2. **连接方式**：建议使用局域网（LAN）连接（IP地址和访问代码），或者使用云连接（需要电子邮件和密码）  
3. **打印模式**：必须向用户明确解释：  
   - **选项A：推荐模式** — 代理程序生成模型后，用户在Bambu Studio中切片、查看并手动打印。无需特殊设置  
   - **选项B：全自动打印** — 代理程序直接控制打印机（包括启动/停止/监控）。需要满足以下条件：  
     - 开启开发者模式  
     - Bambu Studio和Bambu Handy工具会断开连接（无法通过云连接进行远程监控）  
     - 仅支持局域网连接  
     - 打印前总是会显示模型预览（未经用户确认不会自动打印）  
   - 将选择保存在`config.json`文件中，格式为`print_mode: "manual"`或`print_mode: "auto"`  
4. **3D模型生成方式（可选）**：支持使用Meshy、Tripo、Printpal或3D AI Studio工具以及相应的API密钥  
5. **通知设置**：在macOS系统中设置自动通知  
6. **保存配置文件**：`config.json`和`.secrets.json`（权限设置为600，防止他人访问）  
7. **验证连接和打印机配置**：测试连接、摄像头和AMS线材的兼容性  

---

## 环境要求和依赖项**  
**必备软件：** `python3`和`pip3`（推荐在macOS上使用；核心脚本跨平台兼容）  
**可选软件（macOS推荐）：** `ffmpeg`（用于摄像头连接）、Bambu Studio（用于模型预览和切片）、Blender 4.0及以上版本（用于多色模型和高质量预览）、OrcaSlicer（用于CLI切片）  
**环境变量（可覆盖`config.json`中的设置）：** `BAMBU_MODE`、`BAMBU_MODEL`、`BAMBU_EMAIL`、`BAMBU_IP`、`BAMBU_SERIAL`、`BAMBU_3D_PROVIDER`  
**保密信息（存储在`.secrets.json`文件中，权限设置为600）：** 包含密码和访问代码  

---

## 常见错误及解决方法：**  
| 错误 | 正确的操作方式 |  
|---------|------------------|  
| 跳过“搜索还是生成”的选择 | 必须先询问用户。默认选项是搜索。 |  
| 在没有尺寸信息的情况下直接生成模型 | 必须询问尺寸信息（例如：“模型有多高？”）  
| 在运行`generate.py`后直接打开Bambu Studio | 必须先运行`analyze.py`和`preview.py`  
| 未发送预览图像就声称模型准备完毕 | 必须将预览图像发送到聊天窗口 |  
| 在没有得到用户确认的情况下直接开始打印 | 必须等待用户的明确确认  
| 因为模型来自搜索结果就跳过分析步骤 | 所有模型都需要进行分析，因为搜索结果可能存在问题  
| 模型碎片过多时重新生成模型 | 先查看预览结果；如果模型只是外观上有碎片，可以使用`--keep-main`参数