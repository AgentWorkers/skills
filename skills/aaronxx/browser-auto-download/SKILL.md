---
name: browser-auto-download
version: "4.1.0"
description: "**具有增强功能的浏览器自动化文件下载工具**：  
该工具能够自动检测用户使用的操作系统（Windows、macOS、Linux）及处理器架构（64位/32位、ARM/Intel），支持多步骤导航（从首页到特定平台页面），并捕获页面加载时触发的自动下载操作；在必要时也可通过点击按钮来手动触发下载。  
特别适用于那些因客户端渲染、自动下载功能或多页面导航导致 `curl`/`wget` 命令失败的情况。  
该工具还具备以下特点：  
- 支持页面滚动以加载延迟加载的内容；  
- 具备较长的等待时间设置（以适应不同网络环境）；  
- 支持使用 Go 语言编写脚本进行自定义功能扩展。"
---

# 浏览器自动下载功能 v4.1.0（增强版）

该功能能够从动态网页中自动下载文件，具备**智能检测**和**多步骤导航**的能力。

## 主要特性

- **自动下载检测**：在页面加载时检测到自动触发的下载操作。
- **多步骤导航**：找到并导航到针对不同平台的专属下载页面（PC/桌面版本）。
- **平台自动识别**：支持 Windows x64/ARM64、macOS（Intel/Apple Silicon）和 Linux 系统。
- **事件监听**：无需点击按钮即可捕获所有下载相关事件。
- **智能回退机制**：尝试多种下载方式（自动下载、导航或手动点击）。

## 适用场景

- **自动下载网站**：页面加载时自动开始下载。
- **多步骤操作流程**：首页 → 点击“PC版本” → 下载页面。
- **动态内容**：通过 JavaScript 生成的下载链接。
- **交互式下载**：需要用户点击按钮或进行界面导航才能完成下载。

**不适用场景**：直接提供文件 URL 的情况（请使用 `curl`/`wget` 等工具）。

## 快速入门

### 方法 1：自动模式（推荐）

```bash
python skills/browser-auto-download/scripts/auto_download.py \
  --url "https://example.com/download"
```

脚本会执行以下操作：
1. 在页面加载时检测是否有自动下载功能。
2. 查找针对不同平台的下载链接（PC/桌面版本）。
3. 如有必要，自动进行导航。
4. 在无法自动下载时尝试点击下载按钮。

### 方法 2：内置快捷方式

```bash
# WeChat DevTools
python skills/browser-auto-download/scripts/auto_download.py --wechat

# Meitu Xiuxiu
python skills/browser-auto-download/scripts/auto_download.py --meitu
```

### 方法 3：Python 模块

```python
from skills.browser-auto-download.scripts.auto_download import auto_download

result = auto_download(
    url="https://example.com/download",
    auto_select=True,   # Platform detection
    auto_navigate=True  # Multi-step navigation
)

if result:
    print(f"Downloaded: {result['path']}")
```

## 工作原理

**三阶段执行流程**

**阶段 1：自动下载检测**  
```
Page loads - Check for downloads - Success?
    Yes:                    No:
    Save file               Go to Stage 2
```

**阶段 2：多步骤导航**  
```
Look for "PC/Desktop" link - Navigate - Check downloads - Success?
    Yes:                        No:
    Save file                  Go to Stage 3
```

**阶段 3：手动点击下载按钮**  
```
Try multiple selectors - Click - Wait for download - Save
```

## 平台识别机制

脚本能够自动识别以下类型的下载链接：
- “meitu for PC” → pc.meitu.com
- “Desktop version” → desktop.example.com
- “Windows Download” → windows.example.com

**识别关键关键词**：`pc`、`desktop`、`windows`、`mac`、`download`、`电脑`、`桌面`、`客户端`。

## 示例

- **自动下载网站**（最佳使用场景）  
```bash
# Sites that trigger download on page load
python skills/browser-auto-download/scripts/auto_download.py \
  --url "https://pc.meitu.com/en/pc?download=pc"
```

- **多步骤导航流程**  
```bash
# Homepage - PC version - Download
python skills/browser-auto-download/scripts/auto_download.py \
  --url "https://xiuxiu.meitu.com/" \
  --auto-navigate  # Enable (default: True)
```

- **手动选择下载方式（回退机制）**  
```bash
# If auto-detection fails
python skills/browser-auto-download/scripts/auto_download.py \
  --url "https://example.com/download" \
  --selector "button:has-text('Download for free')"
```

## 功能禁用

```bash
# Don't navigate to platform pages
python skills/browser-auto-download/scripts/auto_download.py \
  --url "https://example.com" \
  --no-auto-navigate

# Don't detect platform
python skills/browser-auto-download/scripts/auto_download.py \
  --url "https://example.com" \
  --no-auto-select
```

## 平台识别

| 系统        | 架构          | 使用的关键关键词                |
|------------|------------------|-------------------------|
| Windows      | AMD64/x86_64      | windows, win64, x64, 64-bit, pc         |
| Windows      | x86/i686       | windows, win32, x86, 32-bit, pc         |
| macOS       | ARM64 (M1/M2/M3)     | macos, arm64, apple silicon        |
| macOS       | x86_64 (Intel)     | macos, x64, intel                |
| Linux       | x86_64         | linux, x64, amd64                 |

## 常见问题解决方法

- **下载失败**：
  - 使用 `--headless` 参数（默认值为 `False`）来观察脚本执行过程。
  - 检查 `stderr` 输出中是否有关于自动下载的错误信息。
  - 如果导航功能出现问题，尝试使用 `--no-auto-navigate` 参数。
  - 使用 `--selector` 参数手动指定下载按钮。

- **下载错误版本**：
  - 查看 `stderr` 输出中的平台识别结果。
  - 使用 `--no-auto-select` 参数，并手动指定正确的下载链接。
  - 确认网站是否提供了多个版本可供选择。

- **导航到错误页面**：
  - 使用 `--no-auto-navigate` 参数禁用导航功能。
  - 可能是网站没有为特定平台提供专属下载页面。

- **文件未保存**：
  - 检查输出目录的写入权限。
  - 确保有足够的磁盘空间。
  - 对于大文件，下载可能需要等待（最长 3 分钟）。

## 输出格式

- **stderr（进度信息）**  
```
Starting browser (visible)...
Opening: https://example.com
Checking for auto-downloads...
Checking for platform-specific page link...
Found platform page: https://pc.example.com
Navigating to platform page...
Download detected: software_v2.1.0_win64.exe
Saving: software_v2.1.0_win64.exe

SUCCESS!
File: C:\Users\User\Downloads\software_v2.1.0_win64.exe
Size: 231.9 MB
```

- **stdout（JSON 结果）**  
```json
{
  "path": "C:\\Users\\User\\Downloads\\software_v2.1.0_win64.exe",
  "filename": "software_v2.1.0_win64.exe",
  "size_bytes": 243209941,
  "size_mb": 231.9,
  "platform": "Windows AMD64"
}
```

## 实际应用示例

- **美图秀秀（多步骤导航 + 自动下载）**  
```python
from auto_download import quick_download_meitu

result = quick_download_meitu()
# Flow: Homepage - PC page link - Navigate - Auto-download
```

- **微信开发者工具（手动点击下载按钮）**  
```python
from auto_download import quick_download_wechat_devtools

result = quick_download_wechat_devtools()
# Flow: Homepage - Click "Stable Windows 64" - Download
```

- **通用软件下载**  
```python
result = auto_download(
    url="https://example.com/downloads",
    auto_select=True,    # Detect Windows 64-bit
    auto_navigate=True   # Find "Desktop version" link
)
```

## 使用要求

```bash
pip install playwright
playwright install chromium
```

## 高级用法

- **自定义平台识别关键词**：修改脚本中的 `get_system_preference()` 函数以添加自定义关键词。
- **与其他脚本集成**：根据需求将此功能集成到其他脚本中。
- **批量下载**：支持批量下载多个文件。

### 扩展说明

- **自定义平台识别规则**：可以通过修改脚本中的逻辑来支持更多平台。
- **批量处理**：支持批量下载多个文件，提高下载效率。