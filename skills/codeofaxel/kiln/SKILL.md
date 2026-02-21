---
name: kiln
description: 使用AI代理控制3D打印机：支持273种MCP工具、107种CLI命令；具备文本/草图到3D模型的转换功能；提供模型市场搜索服务；支持多台打印机的协同作业；具备安全监控机制；同时支持外包制造服务。
homepage: https://kiln3d.com
user-invocable: true
metadata: {"openclaw":{"emoji":"🏭","os":["darwin","linux"],"requires":{"env":["KILN_PRINTER_HOST","KILN_PRINTER_API_KEY"],"bins":["kiln"],"anyBins":["prusaslicer","orcaslicer"]},"primaryEnv":"KILN_PRINTER_HOST","install":[{"kind":"uv","pkg":"kiln3d","git":"https://github.com/codeofaxel/Kiln.git","subdirectory":"kiln"}],"optional":{"env":["KILN_PRINTER_TYPE","KILN_PRINTER_MODEL","KILN_AUTONOMY_LEVEL","KILN_HEATER_TIMEOUT","KILN_CRAFTCLOUD_API_KEY","KILN_SCULPTEO_API_KEY","KILN_MESHY_API_KEY","KILN_TRIPO3D_API_KEY","KILN_STABILITY_API_KEY","KILN_GEMINI_API_KEY"]}}}
---
# Kiln — 代理技能定义

您通过Kiln来控制一台物理3D打印机。
**物理操作是不可逆的，可能会损坏硬件。** 请严格遵守以下规则。

## 快速入门

```bash
kiln setup          # interactive wizard — finds printers, saves config
kiln verify         # check everything is working
kiln status --json  # see what the printer is doing
```

然后询问用户想要打印什么。

---

## 使用哪种接口

Kiln支持**两种接口**。根据您的需求选择：

| | CLI | MCP |
|---|---|---|
| **适用场景** | 您有shell/exec工具 | 您配置了MCP客户端 |
| **工作原理** | `kiln <命令> [参数] --json` | 使用JSON参数调用MCP工具 |
| **响应格式** | JSON（使用`--json`时） | 结构化的JSON对象 |
| **设置** | 只需要将`kiln`添加到PATH环境变量中 | 运行`kiln serve`作为MCP服务器 |
| **工具数量** | 107个CLI命令 | 273个MCP工具 |
| **适合场景** | 快速入门、调试、简单工作流程 | 高度集成、完整的工具目录 |

**不知道该选哪种？** 先尝试CLI。运行`kiln status --json`。如果可以正常使用，那么CLI就很适合您。MCP提供了更多工具，但需要设置服务器。 |

---

## CLI接口

通过您的shell/exec工具运行命令。**始终使用`--json`**以获得机器可读的输出。

```bash
kiln <command> [options] --json
```

### 首次设置

如果打印机尚未配置，请先运行以下命令：

```bash
# Interactive wizard: auto-discovers printers, saves config, tests connection
kiln setup

# Or manually add a printer
kiln auth --name my-printer --host http://192.168.1.100 --type octoprint --api-key YOUR_KEY

# Verify everything works (Python, slicer, config, printer reachable, database)
kiln verify

# Scan network for printers
kiln discover --json
```

设置完成后，配置信息会保存到`~/.kiln/config.yaml`文件中——无需环境变量。

### 核心命令

```bash
# Check printer status (start here)
kiln status --json

# List files on printer
kiln files --json

# Run safety checks before printing
kiln preflight --json
kiln preflight --material PLA --json

# Upload a G-code file
kiln upload /path/to/model.gcode --json

# Start printing (auto-uploads local files, auto-runs preflight)
kiln print model.gcode --json
kiln print model.gcode --dry-run --json   # preview without starting

# Cancel / pause / resume
kiln cancel --json
kiln pause --json
kiln resume --json

# Set temperatures
kiln temp --tool 210 --bed 60 --json
kiln temp --json                        # read current temps (no flags)

# Send raw G-code
kiln gcode G28 "G1 X50 Y50 F3000" --json

# Slice STL to G-code
kiln slice model.stl --json
kiln slice model.stl --print-after --json   # slice + upload + print

# Webcam snapshot
kiln snapshot --save photo.jpg --json

# Wait for print to finish (blocks until done)
kiln wait --json

# Print history
kiln history --json
kiln history --status completed --json

# Discover printers on network
kiln discover --json

# Cost estimate
kiln cost model.gcode --json
```

### 外包制造（订单执行）

没有本地打印机？打印机正在使用中？Kiln可以通过相同的CLI接口将任务外包给制造服务（如Craftcloud、Sculpteo）。

```bash
# List available materials from configured service
kiln order materials --json

# Get a manufacturing quote (uploads model, returns pricing + lead time)
kiln order quote model.stl -m pla_standard --json

# Place the order [confirm — ask human first, shows price]
kiln order place QUOTE_ID --json

# Track order status
kiln order status ORDER_ID --json

# Cancel (if still cancellable)
kiln order cancel ORDER_ID --json

# Compare local printing vs. outsourced cost side-by-side
kiln compare-cost model.gcode --fulfillment-material pla_standard --json
```

**设置：** 设置以下环境变量之一（或将其添加到`~/.kiln/config.yaml`文件中）：
```bash
export KILN_CRAFTCLOUD_API_KEY="your_key"     # Craftcloud (easiest — one key)
# OR
export KILN_SCULPTEO_API_KEY="your_key"       # Sculpteo
```

**代理工作流程：** 检查本地打印机 → 如果不可用/正在使用 → 提供报价 → 向用户展示价格 → 用户确认 → 下单 → 提供追踪链接。

### 从文本描述或草图生成3D模型

Kiln可以从文本描述或草图生成可打印的3D模型。Kiln会自动从环境变量中查找可用的服务提供商。

```bash
# List available generation providers [safe]
kiln generate list --json

# Generate a model from text [confirm — creates new file]
kiln generate "a small vase with organic curves" --provider gemini --json
kiln generate "phone stand" --provider meshy --style organic --json

# Check generation status (for async providers like Meshy/Tripo3D)
kiln generate status JOB_ID --json

# Download completed result
kiln generate download JOB_ID --json
```

**MCP对应的命令：**
```json
{"name": "list_generation_providers", "arguments": {}}
{"name": "generate_model", "arguments": {"prompt": "a small vase", "provider": "gemini"}}
{"name": "check_generation_status", "arguments": {"job_id": "gemini-abc123"}}
{"name": "download_generated_model", "arguments": {"job_id": "gemini-abc123"}}
```

**可用提供商**（通过设置环境变量启用）：

| 提供商 | 环境变量 | 类型 | 是否异步？ |
|----------|---------|------|--------|
| **Gemini Deep Think** | `KILN_GEMINI_API_KEY` | AI推理 → OpenSCAD → STL | 同步 |
| **Meshy** | `KILN_meshY_API_KEY` | 云文本转3D | 是（需要轮询状态） |
| **Tripo3D** | `KILN TRIPO3D_API_KEY` | Tripo3D文本转3D | 是（需要轮询状态） |
| **Stability AI** | `KILN_STABILITY_API_KEY` | Stability AI文本转3D | 是（需要轮询状态） |
| **OpenSCAD** | （本地二进制文件） | 参数化代码 → STL | 同步 |

**Gemini Deep Think** 使用Google的Gemini API进行几何推理，并生成精确的OpenSCAD代码，该代码会本地编译为STL格式。支持文本描述和草图/草图绘制。**需要本地安装OpenSCAD。**

**代理工作流程：** 询问用户需求 → 使用最佳可用服务提供商生成模型 → 验证模型网格 → 切片 → 打印。**

### 模型市场搜索

在从头开始生成模型之前，可以从在线市场搜索和下载现有的3D模型。

```bash
# Search across all connected marketplaces [safe]
kiln search "phone stand" --json

# Search a specific marketplace [safe]
kiln search "vase" --marketplace thingiverse --json

# Get model details [safe]
kiln model-details thingiverse MODEL_ID --json

# Download a model file [confirm — downloads to local disk]
kiln model-download thingiverse MODEL_ID --json
```

**MCP对应的命令：**
```json
{"name": "search_all_models", "arguments": {"query": "phone stand"}}
{"name": "search_models", "arguments": {"query": "vase", "marketplace": "thingiverse"}}
{"name": "get_model_details", "arguments": {"marketplace": "thingiverse", "model_id": "12345"}}
{"name": "download_model_file", "arguments": {"marketplace": "thingiverse", "model_id": "12345"}}
```

**支持的市场：** Thingiverse、MyMiniFactory、Thangs、Cults3D、GrabCAD、Etsy。

**代理工作流程：** 用户描述需求 → 在市场上搜索 → 展示搜索结果 → 如果没有合适的模型，则根据文本描述生成模型。

### 批量打印机管理

作为团队的一部分管理多台打印机，支持任务排队和智能路由。

```bash
# Register a printer in the fleet [guarded]
kiln fleet add --name ender3 --host http://192.168.1.100 --type octoprint --json

# Fleet-wide status [safe]
kiln fleet status --json

# Submit a job to the queue (auto-routes to best available printer)
kiln fleet print model.gcode --json

# View job queue [safe]
kiln fleet queue --json
```

**MCP对应的命令：**
```json
{"name": "fleet_status", "arguments": {}}
{"name": "register_printer", "arguments": {"name": "ender3", "host": "http://192.168.1.100", "type": "octoprint"}}
{"name": "submit_fleet_job", "arguments": {"filename": "model.gcode"}}
{"name": "list_queue", "arguments": {}}
```

### Webhook

注册HTTP端点以接收实时通知。

```bash
# Register a webhook [guarded]
kiln webhook add https://example.com/hook --events print_complete,print_failed --json

# List webhooks [safe]
kiln webhook list --json

# Delete a webhook [confirm]
kiln webhook delete WEBHOOK_ID --json
```

所有数据都会使用HMAC-SHA256进行签名以验证。

### 多打印机支持

```bash
# List saved printers
kiln printers --json

# Target a specific printer (works with any command)
kiln --printer my-ender3 status --json
kiln --printer bambu-x1c print model.gcode --json
```

运行`kiln --help`查看所有命令。`kiln <命令> --help`查看特定命令的参数。

### CLI响应格式

**成功** — 输出代码为0，JSON格式输出到标准输出：
```json
{"status": "printing", "filename": "model.gcode", "progress": 42.5,
 "temps": {"tool": 210.0, "bed": 60.0}}
```

**错误** — 输出代码非0，JSON格式中包含`"error"`字段：
```json
{"error": "Printer is offline"}
```

**警告** — JSON数据中包含`"warnings"`数组：

**首先检查输出代码（0表示成功），然后查看JSON中的`"warnings"`字段。**

### 示例响应

**`kiln status --json`**（打印状态）：
```json
{"status": "success", "data": {"printer": {"status": "printing", "temps": {"tool0": {"actual": 210.0, "target": 210.0}, "bed": {"actual": 60.0, "target": 60.0}}}, "job": {"filename": "model.gcode", "progress": 42.5, "time_left": 3600}}}
```

**`kiln print model.gcode --json`**（开始打印）：
```json
{"status": "success", "message": "Print started", "filename": "model.gcode"}
```

**`kiln order quote model.stl -m pla_standard --json`**（生成模型报价）：
```json
{"status": "success", "quote_id": "q_abc123", "price_usd": 12.50, "lead_time_days": 5, "shipping_options": [{"id": "std", "price_usd": 4.99, "days": 7}]}
```

---

## MCP接口

如果您的平台支持MCP客户端，Kiln会作为MCP服务器提供273个工具。可以通过名称和JSON参数调用这些工具——MCP客户端负责处理通信。

### 启动MCP服务器

```bash
kiln serve
```

或者在Claude桌面应用程序中配置（`~/.config/Claude/claude_desktop_config.json`）：
```json
{
  "mcpServers": {
    "kiln": {
      "command": "kiln",
      "args": ["serve"],
      "env": {
        "KILN_PRINTER_HOST": "http://your-printer-ip",
        "KILN_PRINTER_API_KEY": "your_key",
        "KILN_PRINTER_TYPE": "octoprint"
      }
    }
  }
}
```

### MCP工具调用格式

**参数名称和类型由服务器自动记录——MCP客户端会显示这些信息。** 可以运行`get_started()`获取使用指南。

### MCP响应格式

所有工具都会返回JSON对象。与CLI格式相同：
- 成功：包含工具特定的字段
- 错误：`{"error": "message", "status": "error"}`
- 警告：`"warnings"`数组与数据一起返回

---

## 使用前设置

在使用Kiln（无论是通过CLI还是MCP）之前，请设置以下环境变量：

```bash
export KILN_PRINTER_HOST="http://your-printer-ip"
export KILN_PRINTER_API_KEY="your_api_key"
export KILN_PRINTER_TYPE="octoprint"   # or: moonraker, bambu, prusaconnect, elegoo
```

**验证连接：**
```bash
kiln status --json
```

## 文件智能

打印机上的G-code文件通常具有难以理解的名称（如`test5112.gcode`、`spacer_v3.gcode`）。Kiln会从G-code文件头中提取元数据，这样您就可以在不依赖文件名的情况下了解文件信息。

```bash
# Analyze a specific file [safe]
kiln analyze-file benchy.gcode --json
```

**如何使用文件智能功能：**
1. 列出文件：`kiln files --json` — 每个文件现在都包含元数据
2. 打印前检查材料是否匹配：比较`material`字段和已加载的材料（`kiln material show --json`）
3. 检查预计耗时：使用`estimated_time_seconds`评估打印时间
4. 验证温度：比较`tool_temp`/`bed_temp`与安全设置

**示例：选择夜间打印任务**
```
"I found 3 files on your printer:
- benchy.gcode — PLA, ~45 min, 210°C/60°C
- phone_stand.gcode — PLA, ~2h 10m, 210°C/60°C
- test5112.gcode — PETG, ~8h 30m, 240°C/80°C

You have PLA loaded. phone_stand.gcode is the best match for overnight
(PLA-compatible, reasonable duration). Want me to start it?"
```

## 安全模型

Kiln会强制执行**物理安全**——对于超出温度限制、包含危险G-code或通过预检失败的命令，Kiln会拒绝执行。**您**需要根据实际情况判断是否需要请求用户确认。

## 自动化级别

用户可以配置代理的自动化程度。运行`kiln autonomy show --json`查看当前的自动化级别。

| 级别 | 名称 | 行为 |
|-------|------|----------|
| **0** | 需要全部确认 | （默认）所有需要用户确认的命令都需要用户批准。 |
| **1** | 预先筛选 | 如果操作符合配置的约束（材料、时间、温度），可以跳过确认。 |
| **2** | 完全信任 | 可以自主执行所有命令。只有**紧急**命令仍需要用户确认。 |

### 级别1的约束

在级别1下，用户会预先配置安全限制：

```yaml
# ~/.kiln/config.yaml
autonomy:
  level: 1
  constraints:
    max_print_time_seconds: 14400     # 4 hours max
    allowed_materials: ["PLA", "PETG"] # only these materials
    max_tool_temp: 260                 # hotend ceiling
    max_bed_temp: 100                  # bed ceiling
    require_first_layer_check: true    # must monitor first layer before leaving print unattended
```

**在级别1下的工作流程：**
1. 分析文件（`kiln files --json`或`kiln analyze-file FILE --json`）
2. 检查约束：材料是否在允许的范围内？时间是否在限制内？温度是否正常？
3. 如果所有约束都满足 → 无需用户确认即可继续
4. 如果有任何约束不满足 → 询问用户，并说明具体是哪个约束不满足

**示例：级别1下的自动打印**
```
File: phone_stand.gcode
  Material: PLA ✓ (in allowed list)
  Time: 2h 10m ✓ (under 4h limit)
  Tool temp: 210°C ✓ (under 260°C limit)
  Bed temp: 60°C ✓ (under 100°C limit)
→ All constraints passed. Starting print autonomously.
```

**示例：级别1下的禁止打印**
```
File: test5112.gcode
  Material: PETG ✓
  Time: 8h 30m ✗ (exceeds 4h limit)
→ Constraint failed. Asking human for permission.
```

### 级别2：完全信任

用户明确允许您自由操作。通常通过以下声明进行设置：
> “我打印机上的所有文件都使用PLA材料，打印时间在2小时内，且安全。”

在级别2下，您可以自主开始打印、设置温度并上传G-code，无需用户确认——但仍然必须：
- 进行预检（Kiln会自动执行）
- 遵守Kiln的安全限制（温度上限、禁止执行的G-code命令）
- 打印完成后报告操作情况
- 如果有摄像头，监控打印过程

### 环境变量覆盖

```bash
export KILN_AUTONOMY_LEVEL=1  # Quick override without editing config
```

## 工具的安全级别

每个命令都有相应的安全级别。请严格遵循规定的行为。**自动化级别仅影响`confirm`级别的行为。** 安全级别、受保护级别和紧急级别不受自动化设置的影响。

| 级别 | 含义 | 操作方式 |
|-------|---------|---------------|
| `safe` | 只读，无物理影响 | 可以自由调用，无需确认。 |
| `guarded` | 有物理影响但风险较低。Kiln会执行必要的限制。 | 可以自由调用，但需要报告操作情况。 |
| `confirm` | 会导致不可逆或重大的状态变化。 | **根据自动化级别决定是否需要用户确认。** 级别0：需要用户确认。级别1：检查约束。级别2：可以直接执行。 |
| `emergency` | 关乎安全。 | **在任何情况下都必须请求用户确认**，除非存在紧急情况（如温度失控、碰撞）。 |

## 命令的安全分类

### 安全级别（只读，可自由调用）

| 命令 | 描述 |
|---------|-------------|
| `kiln status --json` | 打印机状态、温度、进度 |
| `kiln files --json` | 列出打印机上的文件 |
| `kiln preflight --json` | 打印前的安全检查 |
| `kiln printers --json` | 列出已保存的打印机 |
| `kiln discover --json` | 扫描网络中的打印机 |
| `kiln history --json` | 打印历史记录 |
| `kiln cost FILE --json` | 成本估算 |
| `kiln snapshot --json` | 摄像头快照 |
| `kiln verify` / `kiln doctor` | 系统健康检查 |
| `kiln material show --json` | 当前使用的材料 |
| `kiln material spools --json` | 材料库存 |
| `kiln level --status --json` | 打印床水平状态 |
| `kiln firmware status --json` | 固件版本 |
| `kiln plugins list --json` | 安装的插件 |
| `kiln order materials --json` | 列出待打印的材料 |
| `kiln order status ID --json` | 跟踪订单 |
| `kiln order quote FILE --json` | 获取制造报价 |
| `kiln compare-cost FILE --json` | 本地打印与外包打印的成本对比 |
| `kiln autonomy show --json` | 当前的自动化级别和约束 |
| `kiln analyze-file FILE --json` | G-code文件的元数据（材料、时间、温度） |
| `kiln watch --json` | 监控正在打印的第一层 |

### 受保护级别（风险较低，需要报告操作情况）

| 命令 | 描述 |
|---------|-------------|
| `kiln pause --json` | 暂停打印（可恢复） |
| `kiln resume --json` | 恢复打印（可恢复） |
| `kiln upload FILE --json` | 上传G-code（Kiln会进行验证） |
| `kiln slice FILE --json` | 切片模型（仅影响CPU，不会影响打印机） |
| `kiln wait --json` | 等待打印完成 |
| `kiln material set --json` | 设置使用的材料 |

### 需要用户确认的命令

| 命令 | 描述 | 需要确认的内容 |
|---------|-------------|-----------------|
| `kiln print FILE --json` | **开始打印**（自动执行预检，`--dry-run`用于预览，`--skip-preflight`用于跳过预检） | 文件名和使用的材料 |
| `kiln cancel --json` | **取消打印** | 打印操作不可恢复 |
| `kiln temp --tool X --bed Y --json` | **设置温度** | 设置温度及其原因 |
| `kiln gcode CMD... --json` | **原始G-code代码** | 提供G-code代码及其用途 |
| `kiln slice FILE --print-after --json` | **切片后打印** | 完整的打印流程 |
| `kiln level --trigger --json` | **调整打印床水平** | 调整打印床的位置 |
| `kiln firmware update --json` | **更新固件** | 高风险操作 |
| `kiln order place QUOTE_ID --json` | **下达制造订单** | 包含价格和运输信息 |
| `kiln order cancel ORDER_ID --json` | **取消订单** | 可能无法撤销 |
| `kiln autonomy set LEVEL --json` | **更改自动化级别** | 影响系统安全 |
| `start_monitored_print` (MCP) | **开始打印并监控第一层** | 包括文件名和材料信息 |

### 紧急级别（除非有紧急情况，否则必须请求用户确认）

| 命令 | 描述 | 注意事项 |
|---------|-------------|
| `kiln gcode M112 --json` | 紧急停止命令。**仅用于真正的紧急情况。** |

## 推荐的工作流程

### 上传并打印

> `kiln print` 会自动上传本地文件并执行预检。
> 使用`--skip-preflight`跳过预检，`--dry-run`用于预览而不会实际开始打印。

### 温度调整

```bash
# 1. Check current temps [safe]
kiln temp --json

# 2. Set temps [confirm — tell human: "Setting hotend to 210°C, bed to 60°C for PLA. OK?"]
kiln temp --tool 210 --bed 60 --json
# IF warnings: relay them
```

### 紧急响应

```bash
# 1. Detect issue
kiln status --json   # check for ERROR state or temp anomalies

# 2. IF thermal runaway or physical danger:
kiln gcode M112 --json   # emergency stop — may bypass confirmation
# Then immediately tell human: "Emergency stop triggered because: {reason}"

# 3. IF quality issue but no immediate danger:
# Ask human: "Detected potential failure. Cancel print?"
kiln cancel --json   # only after human confirms
```

### 打印监控循环

**推荐使用`start_monitored_print`（MCP）或`kiln watch`（CLI）。** 这些命令可以同时启动打印和自动监控第一层的打印过程。

**`start_monitored_print` / `kiln watch`的操作步骤：**
1. 启动打印
2. 等待第一层完成2分钟
3. 每隔1分钟拍摄3张摄像头快照
4. 如果检测到故障（置信度≥0.8），则自动暂停打印

**根据您的能力选择合适的监控方式：**
- **带有摄像头**：通过视觉检查返回的Base64快照，观察打印床的粘附情况、变形或挤出是否正常。
- **没有摄像头**：使用`snapshot_analysis`字段（`brightness`、`variance`、`warnings`、`heuristic_pass`）进行判断。亮度低或快照异常可能表示摄像头故障或打印床堵塞。
- **完全无摄像头**：每隔5分钟使用`kiln status --json`检查温度异常、打印进度停滞等情况。

**第一层打印完成后，继续进行定期监控：**
- 每5-10分钟检查一次：`kiln status --json`，检查以下情况：
  - 温度异常（温度突然下降可能表示加热器故障）
  - 打印进度停滞（持续超过10分钟可能表示卡住）
  - 出现错误状态

**根据不同情况采取相应措施：**
- 第一层打印失败：`kiln pause --json`并提醒用户
- 温度异常：`kiln status --json`
- 线材用完：`kiln pause --json`并提醒用户
- 打印进度停滞：`kiln status --json`并提醒用户
- 出现意外情况（如线材断裂或打印机卡住）：`kiln gcode M112 --json`以紧急停止打印

### 自动化夜间打印

**安全自动打印的工作流程（用户在睡眠时使用）：**

**关键安全措施：** 如果在自动化设置中启用了`require_first_layer_check`，代理必须使用`start_monitored_print`而不是`start_print`。系统会在响应中显示`"require_first_layer_check": true`来提示您进行这一检查。

## 操作政策

### 加热器空闲保护

除非用户明确要求预热，否则不要为闲置的打印机设置温度。如果设置了预热，请提醒用户：“加热器已开启，请打印完成后关闭它们。”

Kiln具有**加热器监控**功能，会在打印机空闲时自动关闭加热器。默认超时时间为30分钟（`KILN_HEATER_TIMEOUT`）。将此值设置为0可以禁用该功能。在打印过程中，监控功能不会启动。

### 必须向用户传达所有警告

当Kiln返回警告时，必须原样传达给用户。

### 绝不允许生成G-code

严禁编写或修改G-code文件。请使用`kiln slice`进行切片，或使用打印机上已有的切片文件。

### 材料检查

在打印前，请检查已加载的材料（`kiln material show --json`）。如果材料与G-code文件要求的材料不匹配，必须提醒用户。

### 第一层打印监控

如果摄像头可用，使用`kiln snapshot`监控新打印任务的前几分钟。如果发现异常，请先询问用户再采取行动。

## Kiln的强制规定（无法绕过）

| 规定 | 实施方式 |
|-----------|-----|
| 每台打印机的最大温度限制 | 根据`KILN_PRINTER_MODEL`设置的安全限制 |
| 被禁止执行的G-code命令 | M112、M500-502、M552-554、M997命令始终被拒绝 |
| 打印前的预检 | 必须执行 | `kiln print`会自动执行预检 |
| 上传时的G-code验证 | 上传的G-code文件会进行完整验证 |
| G-code发送时的验证 | 每次调用`kiln gcode`时都会进行验证 |
| 速率限制 | 为防止滥用，某些命令有使用频率限制 |
| 文件大小限制 | 上传文件大小最大为500MB |
| 加热器自动关闭 | 加热器在空闲超过`KILN_HEATER_TIMEOUT`（默认30分钟）后会自动关闭 |

## 许可证和功能层级

Kiln采用分层许可模式。大多数功能永久免费。

| 层级 | 费用 | 主要功能 |
|------|-------|--------------|
| **免费** | $0 | 所有打印机控制、切片功能、安全检查、文本转3D模型生成、市场搜索、CLI和MCP工具、单台打印机支持 |
| **专业版** | 付费 | 多台打印机管理、团队任务调度、优先级任务队列 |
| **企业版** | 付费 | 提供外包制造服务（如Craftcloud/Sculpteo）的订单处理和取消功能 |
| **企业高级版** | 付费 | 提供专用MCP服务器、SSO身份验证、审计日志导出、基于角色的访问权限、可锁定的安全设置、本地部署 |

**收入统计：** Kiln会从通过其市场平台发布的模型收入中收取2.5%的平台费用（通过`KILNPLATFORM_FEE_PCT`配置，范围为0.0–15.0%）。本地打印始终免费。

**许可证密钥：** 通过`KILN_license_KEY`环境变量或`~/.kiln/license`文件设置。** 无密钥则使用免费层级。密钥前缀分别为`kiln_pro_`、`kiln_biz_`、`kiln_ent_`。

## 配置建议

**推荐使用** `kiln setup`（交互式向导，配置结果保存到`~/.kiln/config.yaml`文件）。

**备用方案：环境变量**（适用于Docker/持续集成环境）：

| 环境变量 | 用途 | 默认值 |
|---------|---------|---------|
| `KILN_PRINTER_HOST` | 打印机URL（例如`http://192.168.1.100`） | 从配置文件中获取 |
| `KILN_PRINTER_API_KEY` | 打印机API密钥 | 从配置文件中获取 |
| `KILN_PRINTER_TYPE` | 打印机类型（如`octoprint`、`moonraker`、`bambu`、`prusaconnect`、`elegoo`） | 从配置文件中获取 |
| `KILN_PRINTER_MODEL` | 打印机型号对应的配置文件 | 例如`ender3`、`bambu_x1c` |
| `KILN_AUTONOMY_LEVEL` | 自动化级别：`0`（需要全部确认），`1`（预筛选），`2`（完全信任） | `0` |
| `KILN_HEATER_TIMEOUT` | 加热器空闲后的自动关闭时间（0表示禁用） | `30` |
| `KILN_MONITOR.require_FIRST_LAYER` | 是否需要第一层打印前的监控 | `false` |
| `KILN_MONITOR_FIRST_LAYER_DELAY` | 打印开始后拍摄第一层快照的延迟时间（秒） | `120` |
| `KILN_MONITOR_FIRST_LAYER_CHECKS` | 每次拍摄第一层快照的次数 | `3` |
| `KILN_MONITOR_FIRST_LAYER_INTERVAL` | 第一层快照之间的间隔时间（秒） | `60` |
| `KILN_MONITOR_AUTO_PAUSE` | 检测到问题时自动暂停 | `true` |
| `KILN_MONITOR.require_CAMERA` | 无摄像头时禁止启动监控打印 | `false` |
| `KILN_VISION_AUTO_PAUSE` | 摄像头故障时自动暂停 | `false` |
| `KILN_CRAFTCLOUD_API_KEY` | Craftcloud订单处理API密钥 | （可选） |
| `KILN_SCULPTEO_API_KEY` | Sculpteo订单处理API密钥 | （可选） |
| `KILN_meshY_API_KEY` | Meshy文本转3D API密钥 | （可选） |
| `KILN_TRIPO3D_API_KEY` | Tripo3D文本转3D API密钥 | （可选） |
| `KILN_STABILITY_API_KEY` | Stability AI文本转3D API密钥 | （可选） |
| `KILN_GEMINI_API_KEY` | Gemini AI API密钥 | （可选） |
| `KILN_license_KEY` | 许可证密钥（专业/企业版） | （必需） |
| `KILNPLATFORM_FEE_PCT` | 市场平台费用百分比 | `2.5%` |