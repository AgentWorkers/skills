# Dropbox KB Auto

**利用OCR技术和Office文件支持，自动将您的Dropbox文件索引到可搜索的知识库中。**

## 适用场景

当您需要以下功能时，可以使用此技能：
- 将Dropbox文档自动索引到OpenClaw的知识库中
- 通过语义搜索在PDF、图片和Office文件中进行查找
- 通过OCR从扫描的文档和图片中提取文本
- 使知识库与Dropbox保持同步（基于差异的同步方式，效率更高）
- 使历史文档、收据和研究论文可被搜索

## 功能概述

1. 通过OAuth连接到您的Dropbox（建议使用只读权限）
2. 监控指定文件夹中的新文件或已更改的文件
3. 从以下文件类型中提取文本：
   - PDF文件（扫描文档时使用OCR作为备用方式）
   - 图片（JPG、PNG格式，通过Tesseract OCR进行识别）
   - Office文件（Word、Excel、PowerPoint）
   - 文本文件（TXT、MD、CSV、JSON）
4. 将提取的内容以markdown格式保存到`memory/knowledge/dropbox/`目录中
5. OpenClaw会自动生成用于语义搜索的嵌入信息
6. 使用Dropbox的delta API进行高效的增量同步（仅处理文件的变化部分）

## 先决条件

### 系统依赖
```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-deu poppler-utils

# macOS
brew install tesseract tesseract-lang poppler
```

### Python依赖
```bash
pip3 install pypdf openpyxl python-pptx python-docx
```

或者运行包含的设置脚本：
```bash
bash setup.sh
```

### Dropbox应用设置

1. 在https://www.dropbox.com/developers/apps创建Dropbox应用
2. 选择**有限访问权限** → **完整Dropbox访问权限**（或应用文件夹）
3. 添加以下权限：
   - `files.metadata.read`
   - `files.content.read`
4. 生成刷新令牌（请参考Dropbox OAuth 2文档）
5. 将凭据添加到`~/.openclaw/.env`文件中：
   ```bash
   DROPBOX_FULL_APP_KEY=your_app_key
   DROPBOX_FULL_APP_SECRET=your_app_secret
   DROPBOX_FULL_REFRESH_TOKEN=your_refresh_token
   ```

## 安装

### 通过ClawHub安装
```bash
clawhub install dropbox-kb-auto
```

### 手动安装
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/ferreirafabio/dropbox-kb-auto.git
```

## 配置

编辑`config.json`文件以进行自定义设置：
```json
{
  "folders": [
    "/Documents",
    "/Work",
    "/Research"
  ],
  "skip_paths": [
    "/Archive",
    "/Backups"
  ],
  "file_types": ["pdf", "docx", "xlsx", "pptx", "jpg", "png", "txt"],
  "max_file_size_mb": 20
}
```

## 使用方法

### 首次手动同步
首次运行可能需要5-10分钟（用于构建增量同步的索引）
后续运行：<10秒（仅处理文件变化）

### 自动同步（使用Cron任务）
```bash
openclaw cron create \
  --name "Dropbox KB Sync" \
  --cron "0 */6 * * *" \
  --tz "Europe/Berlin" \
  --timeout-seconds 14400 \
  --session isolated \
  --message "cd ~/.openclaw/workspace/skills/dropbox-kb-auto && python3 dropbox-sync.py"
```

### 搜索索引文件

索引完成后，您可以执行以下操作：
- “显示我2025年的税务文件”
- “查找我的血液检测结果”
- “搜索关于机器学习的演示文稿”

OpenClaw的内置内存系统和语义搜索功能可自动处理这些操作。

## 工作原理

### 基于差异的同步

为了避免每次都重新扫描所有文件（超过650,000份文件），系统采用以下机制：
1. **首次运行**：列出所有文件并保存一个索引（包含时间戳）
2. **后续运行**：仅获取自上次索引以来新增、修改或删除的文件
3. **结果**：速度比全面扫描快10到100倍

### 文本提取流程
```
File → Extension check
  ├─ PDF → pypdf → OCR fallback (if pypdf returns <100 chars)
  ├─ DOCX/DOC → python-docx
  ├─ XLSX/XLS → openpyxl (first 5 sheets, 100 rows each)
  ├─ PPTX/PPT → python-pptx (first 30 slides)
  ├─ JPG/PNG → Tesseract OCR (eng+deu)
  └─ TXT/MD/CSV/JSON → UTF-8 decode
    ↓
Save as .md in memory/knowledge/dropbox/
    ↓
OpenClaw auto-generates embeddings (text-embedding-3-small)
```

## 支持的文件类型

| 文件类型 | 扩展名 | 提取方法 |
|------|-----------|--------|
| PDF | `.pdf` | 使用pypdf库，扫描文件时使用OCR作为备用方式 |
| Word | `.docx`, `.doc` | 使用python-docx库 |
| Excel | `.xlsx`, `.xls` | 使用openpyxl库 |
| PowerPoint | `.pptx`, `.ppt` | 使用python-pptx库 |
| 图片 | `.jpg`, `.jpeg`, `.png` | 使用Tesseract OCR进行识别 |
| 文本 | `.txt`, `.md`, `.csv`, `.json` | 使用UTF-8编码格式 |

## 性能

在650,000份文件（其中1,840份可被索引）上进行测试：
- **首次同步**：约15分钟
- **增量同步**：<30秒
- **磁盘占用**：约45MB

## 故障排除

### 缺少依赖项
如果遇到依赖项缺失的问题，请查看相关说明。
```bash
# If pypdf is missing
pip3 install pypdf openpyxl python-pptx python-docx

# If tesseract is missing
sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-deu
```

### 首次运行时超时

对于文件数量较多的Dropbox账户（超过500,000份文件），可能需要设置更长的超时时间：
```bash
openclaw cron edit <job-id> --timeout-seconds 28800  # 8 hours
```

### 速率限制

脚本包含重试逻辑和指数级退避机制。如果仍遇到速率限制问题：
- 减少`config.json`文件中指定的文件夹范围
- 在处理文件之间添加延迟时间

## 文件存储位置

索引后的文件将保存在：
```
~/.openclaw/workspace/memory/knowledge/dropbox/
├── 2_dokumente_taxes_2025.pdf.md
├── work_presentation_slides.pptx.md
├── research_paper_analysis.xlsx.md
└── blood_test_results.jpg.md
```

同步进度将记录在：
```
~/.openclaw/workspace/memory/
├── dropbox-index-progress.json  # Files already indexed
├── dropbox-cursor.json          # Delta cursors per folder
└── dropbox-indexer.log          # Execution log
```

## 安全性

- **建议使用只读权限**：仅使用具有读取权限的Dropbox应用
- **本地处理**：所有文本提取操作都在您的机器上完成
- **无数据传输**：文件不会离开Dropbox或您的机器
- **凭据安全**：令牌存储在`~/.openclaw/.env`文件中（该文件会被git忽略）

## 与其他工具的比较

| 技能 | 自动索引 | OCR | Office文件支持 | 基于差异的同步 | 使用场景 |
|-------|-----------|-----|--------------|-----------|----------|
| **dropbox-kb-auto** | ✅ | ✅ | ✅ | ✅ | 知识库管理 |
| dropbox-api | ❌ | ❌ | ❌ | ❌ | 仅支持文件操作 |
| dropbox-integration | ❌ | ❌ | ❌ | ❌ | 需要手动浏览文件 |

## 示例应用

- **医疗记录**  
- **研究论文**  
- **税务文件**  

## 贡献方式

如有问题或想要提交代码修改，请访问：https://github.com/ferreirafabio/dropbox-kb-auto

## 许可证

MIT许可证 - 详情请参阅LICENSE文件

## 开发者

Fabio Ferreira ([@ferreirafabio](https://github.com/ferreirafabio))