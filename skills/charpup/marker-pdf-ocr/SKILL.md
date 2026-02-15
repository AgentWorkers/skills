---
name: marker-pdf-ocr
description: 使用 Marker OCR 将 PDF 文件转换为 Markdown 格式（优先使用本地处理方式，必要时使用云端服务）
user-invocable: true
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["MARKER_API_KEY"],
        "bins": ["python3"],
        "minRamMb": 512
      },
      "primaryEnv": "MARKER_API_KEY",
      "install": [
        {
          "id": "pip-marker",
          "kind": "exec",
          "label": "Install marker-pdf package",
          "command": "pip install marker-pdf torch --extra-index-url https://download.pytorch.org/whl/cpu"
        }
      ],
      "suggestedEnv": {
        "MARKER_DEPLOYMENT_MODE": "auto",
        "MARKER_MAX_MEMORY_MB": "4096"
      }
    }
  }
---

# Marker PDF OCR

使用 Marker OCR 引擎将 PDF 文档高精度地转换为 Markdown 格式。

## 使用方法

### 转换 PDF 文件
```bash
# Auto mode (tries local first, falls back to cloud)
marker-ocr convert /path/to/document.pdf

# Force local mode
marker-ocr convert /path/to/document.pdf --mode local

# Force cloud mode
marker-ocr convert /path/to/document.pdf --mode cloud

# With specific output format
marker-ocr convert /path/to/document.pdf --format json
```

### 检查系统状态
```bash
marker-ocr health-check
```

### 批量处理
```bash
for f in *.pdf; do marker-ocr convert "$f"; done
```

## 部署模式

| 模式 | 描述 | 内存需求（RAM） | 网络需求 | 隐私设置 |
|------|-------------|---------|---------|---------|
| **本地模式**（默认） | 在本地使用 CPU 进行处理 | 4GB | 无 | ✅ 高安全性 |
| **云模式** | 使用 Datalab.to API | 512MB | 有 | ⚠️ 数据会传输到云端 |
| **自动模式** | 先尝试本地处理，失败后切换到云模式 | 4GB | 可选 | ✅ 优先使用本地模式 |

### 模式选择逻辑（自动模式）

1. 检查是否已安装 `marker-pdf` 工具。
2. 检查可用内存（至少需要 4GB 的空闲内存）。
3. 如果本地环境可用 → 使用本地模式。
4. 如果本地处理失败或内存不足（OOM） → 切换到云模式。
5. 如果未设置云 API 密钥 → 显示错误信息。

## 环境变量

| 变量 | 是否必填 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `MARKER_API_KEY` | 云模式专用 | - | 来自 Datalab.to 的 API 密钥 |
| `MARKER_DEPLOYMENT_MODE` | 不必填写 | `auto` | 指定部署模式：本地/云/自动 |
| `MARKER_MAX_MEMORY_MB` | 不必填写 | `4096` | 本地模式的最大内存限制（MB） |
| `MARKER_TIMEOUT_SECONDS` | 不必填写 | `300` | 处理超时时间（秒） |

## 安装方法

### 选项 1：本地模式（推荐）
```bash
# Install marker-pdf (CPU-only version)
pip install marker-pdf torch --extra-index-url https://download.pytorch.org/whl/cpu

# Verify installation
marker-ocr health-check
```

### 选项 2：云模式（简易安装）
```bash
# Just set API key, no local dependencies
export MARKER_API_KEY="your-api-key"
```

### 选项 3：通过 OpenClaw 安装
```bash
openclaw skill install marker-pdf-ocr
```

## 系统要求

- **操作系统**：Linux、macOS、Windows（WSL2）
- **Python**：版本 >= 3.8
- **内存**：
  - 本地模式：至少 4GB 内存（建议配置 23GB 的交换空间）
  - 云模式：至少 512MB 内存
- **磁盘空间**：本地模式需要至少 5GB 的存储空间（用于存储模型和缓存文件）

## 输出格式

- `markdown`：纯 Markdown 文本
- `json`：包含元数据的结构化 JSON 数据
- `html`：HTML 格式的输出结果

## 示例

### 转换科学论文
```bash
marker-ocr convert paper.pdf --mode local --format markdown
```

### 批量转换并显示进度
```bash
for pdf in *.pdf; do
  echo "Processing: $pdf"
  marker-ocr convert "$pdf" --mode auto || echo "Failed: $pdf"
done
```

### 查看所使用的部署模式
```bash
marker-ocr health-check --verbose
```

## 错误处理

常见错误及解决方法：

| 错误类型 | 原因 | 解决方案 |
|---------|---------|-----------|
| `OOMError` | 本地内存不足 | 使用 `--mode cloud` 参数或增加交换空间 |
| `APIQuotaExceeded` | 云 API 使用量超出限制 | 等待片刻后重试，或切换到本地模式 |
| `FileTooLarge` | PDF 文件过大 | 分割文件或使用云模式 |
| `MarkerNotInstalled` | 本地依赖库未安装 | 运行 `pip install marker-pdf` 安装工具 |

## 架构概述
```
┌─────────────────┐
│   OpenClaw      │
│   Agent         │
└────────┬────────┘
         │ exec
         ▼
┌─────────────────┐
│   marker-ocr    │
│   CLI           │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌──────────┐
│ Local │  │ Cloud    │
│ (CPU) │  │ (API)    │
└───────┘  └──────────┘
```

## 故障排除

### 本地模式运行缓慢

- 原因：本地模式的处理速度通常比云模式慢 3-5 倍。
- 解决方案：使用云模式或配置 GPU 以提升处理速度。

### 云模式费用

- 大约每页 0.001-0.01 美元。
- 为了控制成本：建议批量处理时使用本地模式。

### 内存问题

- 确保系统配置了交换空间（使用 `free -h` 命令检查交换空间大小）。
- 通过设置 `MARKER_MAX_MEMORY_MB` 来限制内存使用。
- 对于大型文件，建议使用 `--mode cloud` 选项。

## 参考资源

- Marker GitHub 项目：https://github.com/VikParuchuri/marker
- Datalab API：https://www.datalab.to/
- OpenClaw Skills 文档：https://docs.openclaw.ai/tools/skills