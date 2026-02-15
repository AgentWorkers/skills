---
name: bambu-print
description: 在线搜索3D模型库（如Printables、MakerWorld等），下载模型，使用BambuStudio CLI对其进行切片处理，然后将切片文件发送到Bambu Lab的打印机（如A1 Mini、P1等）进行打印。此方法适用于无需通过图形用户界面（GUI）进行手动操作即可完成3D模型的查找、准备和打印的场景。
---

# Bambu Print 技能

通过命令行界面（CLI），自动化完成 3D 模型的搜索、切片以及使用 Bambu Lab 打印机的打印过程。

## 快速入门

### 搜索并打印模型

```bash
# Search for a model and print it
bambu-print search "dragon" --site printables --color purple --printer-model a1-mini

# Or download and slice directly
bambu-print download https://printables.com/model/12345 --output /path/to/output.stl
bambu-print slice output.stl --printer a1-mini --color purple --export result.3mf
bambu-print send result.3mf --printer-name "A1 Mini"
```

## 工作流程

### 1. 在在线仓库中搜索模型

在 Printables、MakerWorld、MyMiniFactory 或 Thingiverse 等平台上搜索模型：
- 搜索条件：模型名称、类型、风格
- 过滤方式：受欢迎程度、复杂度、打印时间
- 返回结果：包含下载链接的顶级模型

### 2. 下载模型

将搜索结果中的 STL/3MF 文件下载到本地磁盘。

### 3. 使用 BambuStudio 进行切片

使用 `bambu-studio` CLI 将 STL 文件切片为 3MF 格式：
```bash
bambu-studio \
  --orient \
  --arrange 1 \
  --load-settings "printer.json;process.json" \
  --load-filaments "filament.json" \
  --slice 0 \
  --export-3mf output.3mf \
  input.stl
```

关键选项：
- `--orient`：自动调整模型方向以便打印
- `--arrange`：自动调整模型在打印床上的排列方式
- `--load-settings`：自定义打印机/打印参数
- `--load-filaments`：设置打印丝材的参数（颜色、材质）
- `--export-3mf`：输出可打印的切片文件

### 4. 将切片文件发送到打印机

通过 Bambu Studio 将切片后的 3MF 文件发送到您的 Bambu Lab 打印机。

## 配置

将打印机和打印丝材的配置信息存储在 `~/.bambu-config/` 目录下：
- `printers/a1-mini.json`：A1 Mini 打印机的配置信息
- `process/standard.json`：标准打印参数（速度、质量）
- `filaments/purple-pla.json`：紫色 PLA 打印丝材的配置信息

### 打印丝材示例配置

```json
{
  "filament_type": "PLA",
  "filament_color": "#7B2CBF",
  "bed_temp": 60,
  "nozzle_temp": 210
}
```

## 配置资源

- **scripts/search_models.py**：用于搜索多个模型仓库的脚本
- **scripts/slice_model.py**：用于调用 `bambu-studio` CLI 的封装脚本
- **references/printer_profiles.md**：包含各打印机的具体配置信息
- **references/sites.md**：列出了支持的模型仓库列表

## 常见操作

**查找并打印一条龙模型：**
```bash
bambu-print search "dragon" --site printables --color purple --auto
```

**使用自定义参数切片下载的模型：**
```bash
bambu-print slice model.stl --printer a1-mini --process fast --filament purple-pla
```

**将模型发送到特定打印机：**
```bash
bambu-print send model.3mf --printer-name "My A1 Mini"
```

## 故障排除

- **找不到 BambuStudio**：确保已安装 `bambu-studio` CLI 并将其添加到系统路径中。
- **模型切片失败**：检查 `printer.json` 和 `process.json` 的配置是否正确。
- **打印机无响应**：确认打印机已连接并可以通过 Bambu Cloud 进行远程控制。