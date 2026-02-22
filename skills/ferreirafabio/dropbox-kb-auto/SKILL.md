# Dropbox KB Auto

## 该功能解决了什么问题？

您的人工智能助手无法直接访问您的 Dropbox 文件夹。文件、收据、研究论文和笔记都存储在助手未知的文件夹中，因此您不得不手动进行搜索。  
此功能填补了这一空白：它将 Dropbox 中的文件同步到系统中，提取文件内容（支持 PDF、Office 文档以及扫描文件的 OCR 解析），并将所有数据索引到助手的知识库中。系统会通过内容哈希值检测文件是否发生变化，并在文件发生变化时自动重新索引；未发生变化的文件则不会被重新处理。  
通过一个简单的命令，您可以配置需要同步的文件夹、排除的文件类型、调度任务以及与 OpenClaw 的内存集成方式。

## 该功能的具体实现方式  
```
    ┌───────────────────┐
    │  Dropbox Account  │
    └────────┬──────────┘
             │ Delta API (only changes)
             ▼
    ┌───────────────────┐
    │  Text Extraction  │
    │  PDF, Office, OCR │
    └────────┬──────────┘
             │ Markdown files
             ▼
    ┌───────────────────┐
    │  OpenClaw Memory  │
    │  Embed + Search   │
    └────────┬──────────┘
             │
             ▼
    ┌───────────────────┐
    │  Agent answers    │
    │  your questions   │
    └───────────────────┘
```

**支持的文件格式：** PDF（支持 OCR 解析）、Word、Excel、PowerPoint、图片（使用 Tesseract OCR 工具进行文本提取）、纯文本。

## 先决条件  

### 系统依赖项  
```bash
# Debian/Ubuntu
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng poppler-utils

# macOS
brew install tesseract poppler
```

### Python 依赖项  
```bash
pip3 install pypdf openpyxl python-pptx python-docx
```  
或运行：`bash setup.sh`  

### Dropbox 应用程序设置  
1. 访问 [https://www.dropbox.com/developers/apps](https://www.dropbox.com/developers/apps) 创建应用程序；  
2. 选择 ** scoped access**（有限访问权限）→ **Full Dropbox**（完整访问权限）；  
3. 启用 `files.metadata.read` 和 `files.content.read` 权限；  
4. 通过 OAuth 2 流程生成刷新令牌；  
5. 将令牌添加到 `~/.openclaw/.env` 文件中：  
   ```bash
   DROPBOX_FULL_APP_KEY=your_app_key
   DROPBOX_FULL_APP_SECRET=your_app_secret
   DROPBOX_FULL_REFRESH_TOKEN=your_refresh_token
   ```

## 安装方法  

### 通过 ClawHub 安装  
```bash
clawhub install dropbox-kb-auto
```  

### 手动安装  
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/ferreirafabio/dropbox-kb-auto.git
```  

## 配置方法  
编辑 `config.json` 文件以配置相关设置：  
```json
{
  "folders": ["/Documents", "/Work"],
  "skip_paths": ["/Archive", "/Backups"],
  "file_types": ["pdf", "docx", "xlsx", "pptx", "jpg", "png", "txt"],
  "max_file_size_mb": 20
}
```  

## 使用方法  

### 推荐的交互式设置方式  
```bash
./install.sh
```  

### 手动同步  
```bash
python3 dropbox-sync.py
```  
首次同步可能需要 5–10 分钟；后续增量同步仅需不到 10 秒。  

### 通过 Cron 任务自动同步  
```bash
openclaw cron create \
  --name "Dropbox KB Sync" \
  --cron "0 */6 * * *" \
  --timeout-seconds 14400 \
  --session isolated \
  --message "cd ~/.openclaw/workspace/skills/dropbox-kb-auto && python3 dropbox-sync.py"
```  

### 查询示例  
索引完成后，您可以这样使用助手：  
- “查找关于机器学习的演示文稿”；  
- “搜索 2025 年第一季度的开支收据”；  
- “我的项目笔记中关于部署的内容是什么？”  

## 性能表现  
在 650,000 个文件（其中 1,840 个文件可被索引）上进行测试：首次同步耗时约 15 分钟，后续增量同步仅需不到 30 秒。  

## 安全性注意事项  
- 建议使用只读权限访问 Dropbox；  
- 所有数据提取操作均在本地完成；  
- 访问凭据存储在 `~/.openclaw/.env` 文件中（该文件会被 Git 忽略）。  

## 许可证  
MIT 许可证  

## 开发者  
Fabio Ferreira ([@ferreirafabio](https://github.com/ferreirafabio))