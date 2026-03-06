---
name: bambu-studio-ai
description: "**Bambu Lab 3D打印机控制与自动化系统**  
当用户提及以下关键词时，该系统会自动激活：打印机状态、3D打印、模型切片、模型分析、3D模型生成、AMS耗材、打印监控、Bambu Lab或任何与3D打印相关的任务。  
完整的处理流程包括：搜索 → 模型生成 → 模型分析 → 模型着色 → 模型切片 → 打印 → 打印监控。  
该系统支持所有9款Bambu Lab打印机（A1 Mini、A1、P1S、P2S、X1C、X1E、H2C、H2S、H2D）。"
version: "0.22.21"
author: TieGaier
metadata:
  openclaw:
    emoji: "🖨️"
    requires:
      bins: ["python3", "pip3"]
    install:
      - id: pip-deps
        kind: pip
        packages: ["bambulabs-api", "bambu-lab-cloud-api", "requests", "trimesh", "numpy", "Pillow", "ddgs", "pygltflib"]
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
        label: "Model preview and manual slicing"
      - id: blender
        kind: cask
        package: blender
        optional: true
        label: "Multi-color pipeline + HQ preview rendering"
      - id: orcaslicer
        kind: cask
        package: orcaslicer
        optional: true
        label: "CLI slicing backend"
env:
  - name: BAMBU_MODE
    required: false
    description: "Connection mode: cloud (default) or local"
  - name: BAMBU_MODEL
    required: false
    description: "Printer model (e.g., H2D, A1 Mini, X1C)"
  - name: BAMBU_EMAIL
    required: false
    description: "Bambu account email (cloud mode)"
  - name: BAMBU_IP
    required: false
    description: "Printer LAN IP (local mode)"
  - name: BAMBU_SERIAL
    required: false
    description: "Printer serial number (local mode)"
  - name: BAMBU_ACCESS_CODE
    required: false
    description: "LAN access code from printer touchscreen (local mode)"
  - name: BAMBU_VERIFY_CODE
    required: false
    description: "Cloud login verification code (one-time)"
  - name: BAMBU_DEVICE_ID
    required: false
    description: "Cloud device ID (auto-detected)"
  - name: BAMBU_3D_PROVIDER
    required: false
    description: "AI 3D gen provider: meshy, tripo, printpal, 3daistudio, rodin"
  - name: BAMBU_3D_API_KEY
    required: false
    description: "API key for chosen 3D generation provider"
secrets:
  - name: BAMBU_PASSWORD
    required_when: "mode=cloud"
    storage: ".secrets.json"
    description: "Bambu Lab account password"
  - name: BAMBU_ACCESS_CODE
    required_when: "mode=local"
    storage: ".secrets.json"
    description: "LAN access code from printer Settings → Device"
  - name: BAMBU_3D_API_KEY
    required_when: "3D generation enabled"
    storage: ".secrets.json"
    description: "API key from chosen 3D generation provider"
security:
  no_credentials_shipped: true  # X.509 cert/key downloaded on demand, not shipped
  secrets_storage: ".secrets.json (chmod 600, git-ignored)"
  config_storage: "config.json (non-sensitive printer settings, git-ignored)"
  token_cache: ".token_cache.json (cloud auth token, 90d TTL, git-ignored). User can delete to force re-auth."
  verify_code_file: ".verify_code (one-time cloud login code, git-ignored)"
  files_gitignored: [".secrets.json", "config.json", ".token_cache.json", ".verify_code"]
  persistence: "Reads config.json at startup, .secrets.json on demand (lazy, not at import). Writes .token_cache.json, .verify_code locally. No remote data exfiltration."
  shipped_credentials: "NONE — no credentials, certificates, or keys are shipped or auto-downloaded."
  x509_setup: "User provides authentication certificate during setup if they enable Developer Mode auto-print. Stored locally in references/*.pem (git-ignored, key chmod 600). Not shipped, not downloaded by code."
  x509_scope: "Signs MQTT commands for LAN auto-print only. Requires user's own access code + same network."
  network_access:
    - "Bambu Lab Cloud API (bambulab.com) — printer control, cloud mode only"
    - "Bambu Lab MQTT (LAN) — printer control, local mode only"
    - "Meshy API (api.meshy.ai) — 3D generation, optional"
    - "Tripo3D API (api.tripo3d.ai) — 3D generation, optional"
    - "Hyper3D Rodin API (hyperhuman.deemos.com) — 3D generation, optional (Business subscription)"
    - "Printpal API — 3D generation, optional"
    - "3D AI Studio API — 3D generation, optional"
    - "DuckDuckGo (via ddgs) — model search, optional"
  consent: "All network calls, file writes, printer operations, and monitoring require explicit user consent."
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
请求 → 收集信息 → 搜索/生成 → 分析 → [上色] → 切片 → 预览 → 确认 → 打印 → 监控

**前置检查：** 如果 `config.json` 不存在，则在执行任何操作之前先运行**首次设置**。

---

## 快速参考

| 操作 | 命令 |
|---|---|
| 查看打印机状态 | `python3 scripts/bambu.py status` |
| 查看打印进度 | `python3 scripts/bambu.py progress` |
| 查看打印机硬件信息 | `python3 scripts/bambu.py info` |
| 开始打印 | `python3 scripts/bambu.py print <文件> --confirmed` |
| 暂停/恢复/取消 | `python3 scripts/bambu.py pause\|resume\|cancel` |
| 调整打印速度 | `python3 scripts/bambu.py speed silent\|standard\|sport\|ludicrous` |
| 打开/关闭灯光 | `python3 scripts/bambu.py light on\|off` |
| 查看AMS线材信息 | `python3 scripts/bambu.py ams` |
| 拍摄相机快照 | `python3 scripts/bambu.py snapshot` |
| 发送G代码 | `python3 scripts/bambu.py gcode "G28"` |
| 发送通知 | `python3 scripts/bambu.py notify --message "完成"` |
| 生成3D模型（文本格式） | `python3 scripts/generate.py text "描述" --wait` （`--raw` 选项会跳过自动优化） |
| 生成3D模型（图像格式） | `python3 scripts/generate.py image photo.jpg --wait` |
| 下载模型文件 | `python3 scripts/generate.py download <任务ID>` |
| 分析模型 | `python3 scripts/analyze.py model.stl --orient --repair --material PLA` |
| 多色上色 | `python3 scripts/colorize.py model.glb --height 80 --max_colors 8 -o out.obj` （可调整参数：`--min-pct`, `--no-merge`, `--island-size`, `--smooth`） |
| 切片模型 | `python3 scripts/slice.py model.stl --orient --arrange --quality fine` |
| 使用特定打印机切片 | `python3 scripts/slice.py model.stl --printer A1 --filament "Bambu PETG Basic"` |
| 列出切片参数设置 | `python3 scripts/slice.py --list-profiles` |
| 快速预览模型 | `python3 scripts/preview.py model.stl` |
| 使用Blender进行高质量预览 | `python3 scripts/preview.py model.stl --hq` |
| 搜索模型 | `python3 scripts/search.py "手机支架" --limit 5` |
| 监控打印过程 | `python3 scripts/monitor.py --auto-pause` |
| 检查模型依赖关系 | `python3 scripts/doctor.py` |

所有脚本都支持 `--help` 参数。`generate.py` 会自动优化模型并限制模型尺寸以适应打印机的打印体积。

---

## 整体工作流程

---

## 第一步：信息收集

在继续之前需要收集以下信息：

**模型要求：**
- 需要打印的物体描述
- 目标尺寸（生成模型前必须询问）：“多高？例如，80毫米”
- 风格/外观（可选）

**打印参数：**
- 单色或多色（使用AMS线材）
- 材料（默认：PLA）
- 打印质量：草图级/标准级/精细级/高级（可选）
- 使用目的：功能性用途还是装饰性用途（可选，这会影响模型的壁厚和填充方式）

**模型来源（询问用户）：**
> “您希望我：
> 1. 🔎 在网上搜索现有的模型（通常质量更高）
> 2. 🎨 通过AI从头开始生成模型
> 3. 🤷 不确定？我会先搜索，如果没有合适的模型再生成”

**默认操作：** 先在网上搜索。常见的模型（如手机支架、挂钩、花瓶）通常都能在网上找到。

---

## 第二步：模型来源（决策点1）

### 浏览器搜索（推荐）

1. 使用 `search.py "查询" --limit 5` 在 MakerWorld、Printables、Thingiverse、Thangs 等平台上搜索。
2. 显示搜索结果，包括模型名称、来源和URL。
3. 用户选择模型后下载，并验证模型格式（STL/OBJ/3MF）。
4. **然后进行模型处理**。

如果没有合适的模型，建议使用AI生成。

### AI生成（单色模型）

1. 首次使用时需要说明：AI生成的模型可能因提供者和输入提示的不同而有所差异，这些模型不一定适合生产使用，请务必在 Bambu Studio 中再次检查。
2. 确认模型尺寸。
3. 使用 `generate.py text "提示" --wait` 命令生成模型，并自动优化模型尺寸以适应打印机。
4. **然后进行模型处理**。

### AI生成（多色模型）

1. 同步骤1的说明。
2. 确认模型尺寸和所需颜色。
3. 使用 `generate.py text "提示" --wait` 命令生成带有纹理的GLB模型。
4. 使用 `colorize.py model.glb --height <尺寸> --max_colors 8` 命令对模型进行上色处理：
   - 使用HSV颜色分类方法选择颜色
   - 无需去除阴影效果（HSV颜色分类方法不涉及烘焙光照处理）
5. **向用户展示上色后的预览图像（_preview.png）**。
6. **根据需要分析结果并进行调整**：
   - 显示检测到的颜色及其名称、十六进制代码和占比。
   - 如果某些颜色占比过低（例如眼睛或小部件的颜色占比低于1%），建议调整 `--min-pct` 参数以保留这些颜色。
   - 如果相似的颜色被错误地合并在一起，建议调整 `--no-merge` 参数。
   - 如果颜色分布不均匀，建议调整 `--island-size` 或 `--smooth` 参数。
7. 如果用户需要修改颜色设置，重新运行 `colorize` 命令并展示新的预览结果。
8. 用户确认后，继续进行模型处理。

**上色参数说明：**
| 参数 | 默认值 | 效果 |
|-----------|---------|--------|
| `--max_colors N` | 8 | 最大允许的颜色数量（AMS线材的最大值为8） |
| `--min-pct X` | 0.1 | 颜色家族的最低占比阈值（0表示保留所有颜色，5表示严格过滤） |
| `--no-merge` | 关闭 | 禁用颜色家族间的合并（所有颜色独立处理） |
| `--island-size N` | 1000 | 删除小于N像素的孤立色块（0表示关闭此功能） |
| `--smooth N` | 5 | 根据颜色分布调整边界平滑度（0表示不进行任何处理，5表示更平滑的处理） |

### 使用用户提供的模型文件

1. 验证模型格式（STL/OBJ/3MF/GLB），如有需要则进行转换。
2. **然后进行模型处理**。

---

## 第三步：模型处理

所有模型都必须经过这一步骤，没有例外。

**模型分析（11项检查）：**
检查模型的尺寸是否准确、壁厚是否合理、悬垂部分是否合适、打印方向是否正确、层高是否合适、填充比例是否恰当、壁层数量是否合理、使用的材料是否兼容打印机等。同时还需要检查模型是否防水、是否有缺陷以及模型是否适合打印机的打印体积。

**自动修复：** 修复模型的法线信息、填补孔洞、删除不完整的面。

**自动调整模型方向：** 优化模型的稳定性，并自动调整模型的单位尺寸（从米转换为毫米）。

**必须向用户报告的结果：**
- 打印可行性评分（0-10分）
- 存在的问题和警告
- 所进行的修复操作
- 推荐的打印参数（层高、填充比例、壁层厚度、打印温度、支撑结构等）

**示例报告：** “评分8分。修复了58,000个不完整的边缘。壁层厚度：1.5毫米。悬垂部分：3.2%。推荐参数：层高0.20毫米，填充比例20%，使用PLA材料，打印温度210摄氏度。”

**切片（如果用户将在Bambu Studio中手动切片，则跳过此步骤）：**
自动检测打印机和喷嘴的兼容性。设置打印质量（草图级0.24毫米/标准级0.20毫米/精细级0.12毫米/高级级0.08毫米）。输出格式为.GMF文件，同时生成相应的G代码。

---

## 第四步：用户确认

**必须执行此步骤，切勿跳过：**
1. 在Bambu Studio中打开模型文件：`open -a "BambuStudio" model_sliced.3mf`。
2. 告知用户检查模型：
   - 模型是否正确无误？
   - 有没有缺失或变形的部分？
   - 尺寸是否正确？
   - 有没有红色警告提示？
   - 检查切片后的模型信息（预计打印时间、线材使用量、所需的支持结构等）。
   - 完成检查后请告知我！
3. 等待用户的明确确认。

**注意：** 绝不要自动开始打印。AI生成的模型可能存在一些问题，手动检查可以避免错误。

**选择打印方式：**
- **自动打印（仅限开发者模式）**：`bambu.py print model.3mf --confirmed`。
   - **在Bambu Studio中手动打印**：用户可以自行调整参数后进行打印。

---

## 第五步：打印执行（决策点2）

### 自动打印（仅限开发者模式）

**注意：** 必须开启开发者模式。使用此模式时，Bambu Studio和Bambu Handy应用程序会断开连接。
1. 使用 `bambu.py print model.3mf --confirmed` 命令开始打印。
2. 确认打印状态：“打印已经开始！”

### 手动打印
- 模型已经在Bambu Studio中打开。
- 用户可以手动调整打印参数并进行打印。

**打印状态监控有两种方式：**
1. **实时监听：** 在模型上传到Bambu Studio后，立即启动一个后台MQTT监听器（持续30分钟）。如果打印机状态变为“RUNNING”，则通知用户并提供实时监控功能。
2. **定期检查：** 在正常运行期间，定期检查打印器的状态。如果发现异常，立即通知用户。

---

## 第六步：打印监控

触发条件：自动打印、手动打印或用户请求。需要使用局域网连接。

**监控方法：** 通过paho-mqtt协议直接订阅打印器的MQTT消息。
连接地址：`{printer_ip}:8883`，订阅主题 `device/{serial}/report`，解析接收到的`print`消息。

**监控期间必须拍摄相机快照：**
- 使用 `bambu.py snapshot` 命令通过RTSP协议拍摄快照（路径：`ffmpeg → rtsps://bblp:{code}@{ip}:322/streaming/live/1`）。
- 每次进度更新时都将快照发送给用户。
- 将快照包含在异常报告中。

**默认的监控计划（每次打印时发送大约5条消息）：**
| 事件 | 触发条件 | 处理方式 |
|---|---|---|
| 打印开始 | 打印器状态变为“RUNNING” | 发送通知并发送快照 |
| 进度达到25% | 进度达到25% | 发送状态更新和快照 |
| 进度达到50% | 进度达到50% | 发送状态更新和快照 |
| 打印完成 | 打印完成 | 发送最终状态更新和快照 |
| 出现异常 | 任何异常情况 | 立即发送警报并发送快照，并自动暂停打印 |

用户可以调整监控的频率。通过跟踪这些关键节点可以避免重复发送相同的消息。

**异常处理：**
| 异常类型 | 处理方式 |
|---|---|---|
| 打印进度停滞超过10分钟 | 发出警告并发送快照 |
| 温度异常 | 发出严重警告并发送快照并自动暂停打印 |
| 打印失败/错误 | 发出严重警告并发送快照并自动暂停打印 |
| 打印机出现意外暂停 | 发出警告并发送快照 |
| 打印床脱离 | 发出严重警告并自动暂停打印 |

**状态报告格式（发送给用户）：**

---

## 首次设置

当 `config.json` 不存在时，系统会提示用户进行首次设置：
1. **打印机型号**：A1 Mini、A1、P1S、P2S、X1C、X1E、H2C、H2S、H2D
2. **连接方式**：建议使用局域网连接（IP地址+串行号+访问代码），或者使用云服务（需要提供电子邮件地址和密码，但功能有限）。
3. **打印模式**：必须向用户详细说明两种打印模式：
   - **模式A（推荐）**：AI生成并切片模型后，用户在Bambu Studio中查看并手动打印。无需进行额外的打印机设置。
   - **模式B（全自动）**：AI直接控制打印机（包括启动/停止/监控功能）。注意：
     - 必须开启开发者模式。
     - 使用此模式时，Bambu Studio和Bambu Handy应用程序会完全断开连接（无法通过云服务进行远程监控）。
     - 仅支持局域网连接。
     - 打印前系统始终会显示模型预览，未经用户确认不会自动开始打印。
   - 将用户选择的打印模式保存到 `config.json` 文件中，格式为 `print_mode: "manual"` 或 `print_mode: "auto"`。
4. **3D模型生成选项（可选）**：可以使用Meshy、Tripo、Printpal或3D AI Studio等工具，并需要相应的API密钥。
5. **通知方式**：可以选择自动通知、Discord、iMessage或Telegram等。
6. **保存设置**：将配置信息保存到 `config.json` 和 `.secrets.json` 文件中（文件权限设置为600，避免被他人访问）。
7. **验证设置**：测试连接、相机功能和AMS线材的兼容性。

---

## 环境要求和依赖库

**必需安装的软件：** `python3` 和 `pip3`
**可选软件：** `ffmpeg`（用于拍摄相机视频）、Bambu Studio（用于预览和切片处理）、Blender 4.0及以上版本（用于多色模型和高质量预览）、OrcaSlicer（用于CLI切片操作）。

**环境变量（可覆盖 `config.json` 中的设置）：** `BAMBU_MODE`、`BAMBU_MODEL`、`BAMBU_EMAIL`、`BAMBU_IP`、`BAMBU_SERIAL`、`BAMBU_3D_PROVIDER`

**保密信息（存储在 `.secrets.json` 文件中，权限设置为600）：** `password`、`access_code`、`3d_api_key`。这些信息由用户提供，不会随软件一起分发。

---

## 常见问题及解决方法

| 问题 | 解决方法 |
|---|---|
| SSL连接错误（局域网环境） | 这是正常现象，因为使用了自签名证书。系统会自动处理。 |
| 无法找到API接口 | 使用 `pip3 install --upgrade bambulabs-api`（版本2.6.6及以上）进行更新。 |
| 无法连接（局域网环境） | 确保局域网模式已开启，IP地址正确，且设备在同一局域网内。 |
| 云服务验证失败 | 等待系统发送的验证代码，输入后代码会缓存24小时。 |
| 相机拍摄失败 | 可以尝试唤醒打印机或检查网络连接。 |
| AI生成的模型有缺陷或部分缺失 | 这是正常现象，建议使用 `analyze.py --repair` 命令修复模型。 |

## 已知的限制

| 功能 | 现状 |
|---|---|
| 单色打印流程 | 可靠稳定 |
| 多色打印（上色功能） | 可以自动检测最多8种颜色，并将结果保存为OBJ格式文件，用户可以在Bambu Studio中手动调整颜色。 |
| 通过CLI进行切片 | 可以使用OrcaSlicer工具进行切片操作（但在Bambu Studio 2.5.0版本中可能会出现SEGFAULT错误）。 |
| 全自动打印流程 | 在开发者模式下可以使用（需要X.509版本的MQTT协议和FTP上传功能）。 |

## 参考文档**

- `references/model-specs.md`：所有打印机的规格信息。
- `references/bambu_filament_colors.json`：Bambu Lab提供的43种颜色调色板（仅用于参考，多色上色功能使用原始纹理颜色）。
- `references/bambu-mqtt-protocol.md`：MQTT协议的相关文档。
- `references/bambu-cloud-api.md`：云服务的API文档。
- `references/3d-generation-apis.md`：3D模型生成的API接口文档。
- `references/3d-prompt-guide.md：3D模型生成的提示设计指南。

## 许可证信息

该项目采用MIT许可证，代码托管在GitHub上：https://github.com/heyixuan2/bambu-studio-ai