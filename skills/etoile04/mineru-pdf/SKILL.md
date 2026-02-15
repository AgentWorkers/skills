---
name: mineru-pdf
description: 使用 MinerU MCP 解析 PDF 文档，以提取文本、表格和公式。支持多种后端，包括在 Apple Silicon 上使用 MLX 加速的推理功能。
homepage: https://github.com/TINKPA/mcp-mineru
metadata:
  {
    "openclaw":
      {
        "emoji": "📄",
        "requires": { "bins": ["uvx"] },
        "install":
          [
            {
              "id": "uvx",
              "kind": "uvx",
              "package": "mcp-mineru",
              "label": "Install mcp-mineru via uvx (auto-managed)",
            },
          ],
      },
  }
---

# MinerU PDF解析器

使用MinerU MCP解析PDF文档，提取结构化内容（包括文本、表格和公式），并在Apple Silicon平台上利用MLX加速技术进行解析。

## 安装

### 选项1：安装MinerU MCP（适用于Claude代码）

```bash
claude mcp add --transport stdio --scope user mineru -- \
  uvx --from mcp-mineru python -m mcp_mineru.server
```

此选项会安装并配置MinerU，适用于所有Claude项目。模型会在首次使用时自动下载。

### 选项2：使用直接工具（保留文件）

该工具会直接解析PDF文档，并将结果保存到指定的持久化目录中：

```bash
python /Users/lwj04/clawd/skills/mineru-pdf/parse.py <pdf_path> <output_dir> [options]
```

**优点：**
- ✅ 文件会被永久保存（不会自动删除）
- ✅ 可完全控制输出文件的保存位置
- ✅ 无需承担MCP的开销
- ✅ 适用于任何安装了MinerU的Python环境

## 快速入门

### 方法1：使用直接工具（推荐）

```bash
# Parse entire PDF
python /Users/lwj04/clawd/skills/mineru-pdf/parse.py \
  "/path/to/document.pdf" \
  "/path/to/output"

# Parse specific pages
python /Users/lwj04/clawd/skills/mineru-pdf/parse.py \
  "/path/to/document.pdf" \
  "/path/to/output" \
  --start-page 0 --end-page 2

# Use Apple Silicon optimization
python /Users/lwj04/clawd/skills/mineru-pdf/parse.py \
  "/path/to/document.pdf" \
  "/path/to/output" \
  --backend vlm-mlx-engine

# Text only (faster)
python /Users/lwj04/clawd/skills/mineru-pdf/parse.py \
  "/path/to/document.pdf" \
  "/path/to/output" \
  --no-table --no-formula
```

### 方法2：使用MinerU MCP（生成临时文件）

### 解析PDF文档

```bash
uvx --from mcp-mineru python -c "
import asyncio
from mcp_mineru.server import call_tool

async def parse_pdf():
    result = await call_tool(
        name='parse_pdf',
        arguments={
            'file_path': '/path/to/document.pdf',
            'backend': 'pipeline',
            'formula_enable': True,
            'table_enable': True,
            'start_page': 0,
            'end_page': -1  # -1 for all pages
        }
    )
    if hasattr(result, 'content'):
        for item in result.content:
            if hasattr(item, 'text'):
                print(item.text)
                break

asyncio.run(parse_pdf())
"
```

### 检查系统兼容性

```bash
uvx --from mcp-mineru python -c "
import asyncio
from mcp_mineru.server import call_tool

async def list_backends():
    result = await call_tool(
        name='list_backends',
        arguments={}
    )
    if hasattr(result, 'content'):
        for item in result.content:
            if hasattr(item, 'text'):
                print(item.text)
                break

asyncio.run(list_backends())
"
```

## 参数

### parse_pdf

**必填参数：**
- `file_path` - PDF文件的绝对路径

**可选参数：**
- `backend` - 处理后端（默认值：`pipeline`）
  - `pipeline` - 快速、通用型后端（推荐）
  - `vlm-mlx-engine` - 在Apple Silicon（M1/M2/M3/M4）平台上性能最佳
  - `vlm-transformers` - 效率较低但识别精度最高
- `formula_enable` - 是否启用公式识别（默认值：`true`）
- `table_enable` - 是否启用表格识别（默认值：`true`）
- `start_page` - 开始页码（从0开始计数，默认值：`0`）
- `end_page` - 结束页码（默认值：`-1`，表示解析所有页面）

### list_backends

无需参数。此函数会返回系统信息及后端推荐方案。

## 使用示例

### 从指定页码范围提取表格

```bash
uvx --from mcp-mineru python -c "
import asyncio
from mcp_mineru.server import call_tool

async def parse_pdf():
    result = await call_tool(
        name='parse_pdf',
        arguments={
            'file_path': '/path/to/document.pdf',
            'backend': 'pipeline',
            'table_enable': True,
            'start_page': 5,
            'end_page': 10
        }
    )
    if hasattr(result, 'content'):
        for item in result.content:
            if hasattr(item, 'text'):
                print(item.text)
                break

asyncio.run(parse_pdf())
"
```

### 仅解析公式（速度更快）

```bash
uvx --from mcp-mineru python -c "
import asyncio
from mcp_mineru.server import call_tool

async def parse_pdf():
    result = await call_tool(
        name='parse_pdf',
        arguments={
            'file_path': '/path/to/document.pdf',
            'backend': 'vlm-mlx-engine',
            'formula_enable': True,
            'table_enable': False  # Disable for speed
        }
    )
    if hasattr(result, 'content'):
        for item in result.content:
            if hasattr(item, 'text'):
                print(item.text)
                break

asyncio.run(parse_pdf())
"
```

### 解析单页内容（测试用，速度最快）

```bash
uvx --from mcp-mineru python -c "
import asyncio
from mcp_mineru.server import call_tool

async def parse_pdf():
    result = await call_tool(
        name='parse_pdf',
        arguments={
            'file_path': '/path/to/document.pdf',
            'backend': 'pipeline',
            'formula_enable': False,
            'table_enable': False,
            'start_page': 0,
            'end_page': 0
        }
    )
    if hasattr(result, 'content'):
        for item in result.content:
            if hasattr(item, 'text'):
                print(item.text)
                break

asyncio.run(parse_pdf())
"
```

## 性能

在Apple Silicon M4（16GB RAM）平台上：
- `pipeline`：每页约32秒，仅使用CPU，解析质量良好
- `vlm-mlx-engine`：每页约38秒，针对Apple Silicon进行了优化，解析质量优秀
- `vlm-transformers`：每页约148秒，解析质量最高，但速度最慢

**注意：** 首次运行时需要下载模型（可能需要5-10分钟）。模型会缓存到`~/.cache/uv/`目录中，以加快后续解析速度。

## 输出格式

解析结果将以Markdown格式返回，包含以下内容：
- 文档元数据（文件路径、使用的后端、页码、配置信息）
- 保留结构的提取文本
- 格式化为Markdown的表格
- 转换为LaTeX的数学公式

## 支持的文件格式

- PDF文档（`.pdf`）
- JPEG图像（`.jpg`, `.jpeg`）
- PNG图像（`.png`）
- 其他图像格式（WebP、GIF等）

## 故障排除

### 报错“找不到'mcp_mineru'模块”

如果出现“找不到'mcp_mineru'模块”的错误，请确保已正确安装该模块：

```bash
claude mcp add --transport stdio --scope user mineru -- \
  uvx --from mcp-mineru python -m mcp_mineru.server
```

### 首次运行时处理速度较慢

这是正常现象，因为MinerU会在首次使用时下载模型。后续运行速度会显著提升。

### 超时错误

对于大型文件或需要解析大量页面的情况，可以增加超时时间；或者尝试缩小解析范围。

## 注意事项

- 输出结果为Markdown格式
- 表格会以Markdown格式保存
- 数学公式会转换为LaTeX格式
- 支持扫描文档（内置OCR功能）
- 专为Apple Silicon（M1/M2/M3/M4）平台及MLX后端进行了优化

## 文件持久化

### 文件为何会被删除（MCP方法）

MinerU MCP使用Python的`tempfile.TemporaryDirectory()`函数来管理临时文件，该函数会在程序退出时自动删除临时文件。这是为了防止文件积累。

### 如何保留文件

**方法A：使用直接工具（推荐）**

该工具提供了`parse.py`脚本，可将解析结果保存到持久化目录中：

```bash
python /Users/lwj04/clawd/skills/mineru-pdf/parse.py \
  /path/to/input.pdf \
  /path/to/output_dir
```

**优点：**
- ✅ 文件不会被自动删除
- ✅ 可完全控制输出文件的保存位置
- 支持批量处理
- 无需依赖MCP服务

**生成的文件结构：**
```
/path/to/output_dir/
├── input.pdf_name/
│   └── auto/          # or vlm/ depending on backend
│       ├── input.pdf_name.md
│       └── images/
│           └── *.jpg
└── input.pdf_name_parsed.md  # Copy at root for easy access
```

**方法B：捕获MCP的输出结果**

如果使用MCP方法，可以手动捕获输出结果并保存：

```bash
# Capture to file
claude -p "Parse this PDF: /path/to/file.pdf" > /tmp/output.md

# Or use within a script that saves the result
```

### 对比

| 功能        | 直接工具         | MCP方法       |
|------------|--------------|-------------|
| 文件是否持久化   | ✅             | ❌（文件会被自动删除）   |
| 是否可自定义输出目录 | ✅             | ❌（仅使用临时文件）     |
| 与Claude代码的集成 | ⚠️ 需手动配置     | ✅（原生集成）     |
| 处理速度     | ✅             | ⚠️ 有MCP开销     |
| 是否支持离线使用 | ✅             | ⚠️ 需依赖Claude代码   |

### 推荐方案

- **建议使用直接工具**，尤其是需要保留解析结果的情况下
- **建议使用MCP方法**，仅在Claude代码环境中且仅需要文本内容时使用