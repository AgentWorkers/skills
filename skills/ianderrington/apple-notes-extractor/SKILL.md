---
name: apple-notes
description: **功能说明：**  
该工具用于提取并监控 Apple Notes 中的内容，以便将其集成到工作流程中。支持批量提取数据、实时监控内容变化，并可将提取的结果导出为多种格式。  

**主要特性：**  
1. **批量提取**：能够一次性从多个 Apple Notes 文件中提取所需信息。  
2. **实时监控**：实时监测 Notes 内容的更新情况，确保数据始终与最新状态保持一致。  
3. **多种格式导出**：支持将提取的数据导出为 PDF、CSV、HTML 等常见格式，方便进一步处理或分享。  

**应用场景：**  
- **工作流程自动化**：将提取的 Notes 内容整合到自动化系统中，提高工作效率。  
- **内容同步**：确保团队成员使用的是最新的 Notes 数据。  
- **数据分析**：对提取的文本数据进行统计分析或可视化处理。  

**技术细节：**  
- **兼容性**：支持最新版本的 Apple Notes 应用程序。  
- **安全性**：在提取和传输数据过程中采用加密技术，保护用户隐私。  
- **可扩展性**：可根据需求定制提取规则和导出格式。  

**示例用法：**  
- **批量提取**：使用命令行工具或图形界面界面，批量下载多个用户的 Notes 数据。  
- **实时监控**：通过 Web 界面实时查看所有用户的 Notes 更新记录。  
- **格式转换**：将提取的文本转换为适合报告或数据分析的格式。
metadata: {"openclaw": {"requires": {"bins": ["python3", "osascript"]}, "emoji": "📝"}}
---

# Apple Notes Skill

本技能用于提取和监控 Apple Notes 中的内容，以便将其集成到工作流程中。支持批量提取、实时监控以及将数据导出为多种格式。

## 前提条件

- 安装了 macOS 及其内置的 Apple Notes 应用程序。
- 安装了 Python 3.8 或更高版本（用于编写协调脚本）。
- macOS 系统内置了 osascript 脚本引擎。
- 用户具有访问 Apple Notes 数据的相应权限。

## 安装

```bash
# Run the installation script
./scripts/setup.sh

# Or manual setup
chmod +x scripts/*.py
pip3 install -r requirements.txt
```

## 命令

### 提取笔记内容

```bash
# Basic extraction (all notes)
python3 scripts/extract-notes.py --method simple

# Full extraction with attachments
python3 scripts/extract-notes.py --method full

# Extract specific folder
python3 scripts/extract-notes.py --folder "Work Notes"

# Output to specific format
python3 scripts/extract-notes.py --format markdown --output ~/notes
```

### 监控笔记变化

```bash
# Start monitoring daemon
python3 scripts/monitor-notes.py --daemon

# Single check for changes
python3 scripts/monitor-notes.py --check-once

# Monitor with custom interval (seconds)
python3 scripts/monitor-notes.py --interval 30
```

### 数据处理与导出

```bash
# Process extracted notes
python3 scripts/notes-processor.py output/raw -o output/processed

# Export to Obsidian
python3 scripts/export-obsidian.py --vault ~/MyVault

# Generate knowledge graph
python3 scripts/knowledge-graph.py --input output/processed
```

## 配置

- 在 `configs/extractor.json` 文件中配置：
  - 输出格式（JSON、Markdown、HTML）
  - 隐私过滤规则
  - 需要提取的文件夹路径
  - 数据处理选项

- 在 `configs/monitor.json` 文件中配置：
  - 监控间隔
  - 变更检测规则
  - 自动处理规则

## 主要功能

- ✅ 从所有笔记中提取文本内容。
- ✅ 处理嵌入的图片和附件。
- ✅ 处理笔记的元数据（如创建日期、所属文件夹等）。
- ✅ 支持多种输出格式（JSON、Markdown、SQLite）。
- ✅ 实时监控笔记内容的变更。
- 注重数据隐私，所有处理都在本地完成。
- 可与知识管理工具集成。
- ✅ 支持数据去重功能。
- ✅ 支持增量式数据更新。

## 输出格式

| 格式 | 描述 | 适用场景 |
|--------|-------------|----------|
| `json` | 带有元数据的结构化数据 | 适用于 API 集成 |
| `markdown` | 人类可读的文本文件 | 适用于文档编写 |
| `sqlite` | 可搜索的数据库格式 | 适用于数据存储 |
| `obsidian` | Obsidian 知识库格式 | 适用于知识管理工具 |

## 示例用法

```bash
# Quick start - extract all notes to Markdown
python3 scripts/extract-notes.py --format markdown --output ~/extracted-notes

# Monitor and auto-export to Obsidian
python3 scripts/monitor-notes.py --daemon --auto-export obsidian

# Extract work notes with full content
python3 scripts/extract-notes.py --method full --folder "Work Notes" --format json

# Process and create knowledge graph
python3 scripts/extract-notes.py --method full
python3 scripts/notes-processor.py output/raw -o output/processed
python3 scripts/knowledge-graph.py --input output/processed --output knowledge-graph.json
```

## 安全性与隐私保护

- 所有数据处理操作都在用户的本地机器上进行，不会向外部服务发送任何数据。
- 严格遵循 macOS 的安全权限设置。
- 支持针对敏感内容的隐私过滤功能。
- 可选择对导出数据进行加密处理。

## 集成方式

- 可与 Obsidian 知识库直接集成（导出数据到 Obsidian 存储库）。
- 支持与 Logseq 工具交换 Markdown 格式的笔记内容。
- 可将数据导入 Notion 知识管理工具（JSON 格式）。
- 可与其他自定义工作流程系统（JSON/CSV 格式）集成。
- 可用于支持人工智能处理的数据管道。
- 数据可被搜索引擎（如 Google 或 Bing）进行全文索引。

## 故障排除

- 常见问题：
  - **权限问题**：请在系统偏好设置 > 安全与隐私中授予应用程序访问权限。
  - **导入错误**：确保已安装 Python 3.8 及所有必需的依赖包。
  - **osascript 错误**：检查 Apple Notes 是否正在运行且可正常访问。
  - **输出为空**：请确认目标文件夹的路径正确且笔记具有写入权限。

详细故障排除指南请参阅 README.md 文件。