---
name: file-organizer-cn
description: "智能文件整理 | Smart File Organizer  
自动整理文件和文件夹 | Auto organize files and folders  
查找重复文件 | Find duplicates  
建议文件结构 | Suggest file structure  
文件清理 | File cleanup  
相关关键词：  
整理文件 | File organization  
文件管理工具 | File management tool  
文件系统优化 | File system optimization"
metadata:
  openclaw:
    emoji: 📁
    fork-of: "https://github.com/anthropics/skills"
---# 文件整理助手

这个功能就像你的个人组织助理，帮助你保持电脑文件结构的整洁和逻辑性，免去手动整理带来的麻烦。

## 适用场景

- 你的下载文件夹杂乱无章
- 由于文件分散在各处而找不到所需文件
- 存在占用空间的重复文件
- 文件夹结构已经混乱不堪
- 你想养成更好的整理习惯
- 开始新项目，需要一个合理的文件结构
- 在归档旧项目前进行清理

## 功能介绍

1. **分析当前结构**：检查你的文件夹和文件，了解你的文件情况。
2. **查找重复文件**：识别系统中的重复文件。
3. **提供整理建议**：根据文件内容建议合理的文件夹结构。
4. **自动执行清理**：在获得你的确认后，移动、重命名并整理文件。
5. **智能管理文件**：根据文件类型、日期和内容做出合理决策。
6. **减少杂乱**：识别出可能不再需要的旧文件。

## 使用方法

### 从你的主目录开始

```
cd ~
```

然后运行 Claude Code 并请求帮助：

```
Help me organize my Downloads folder
```

```
Find duplicate files in my Documents folder
```

```
Review my project directories and suggest improvements
```

### 具体的整理任务

```
Organize these downloads into proper folders based on what they are
```

```
Find duplicate files and help me decide which to keep
```

```
Clean up old files I haven't touched in 6+ months
```

```
Create a better folder structure for my [work/projects/photos/etc]
```

## 操作步骤

当用户请求文件整理帮助时：

1. **明确整理范围**：
   - 哪个目录需要整理？（下载、文档、整个主文件夹？）
   - 主要问题是什么？（找不到文件、有重复文件、结构混乱？）
   - 有哪些文件或文件夹需要特别处理？（当前项目、敏感数据？）
   - 整理的力度如何？（保守处理还是全面清理？）

2. **分析当前状态**：
   - 查看目标目录：
   ```bash
   # Get overview of current structure
   ls -la [target_directory]
   
   # Check file types and sizes
   find [target_directory] -type f -exec file {} \; | head -20
   
   # Identify largest files
   du -sh [target_directory]/* | sort -rh | head -20
   
   # Count file types
   find [target_directory] -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
   ```
   - 总结发现：
     - 文件和文件夹的数量
     - 文件类型分布
     - 文件大小分布
     - 文件创建日期范围
     - 明显的整理问题

3. **确定整理方案**：
   - 根据文件类型进行分类：
     - 文档（PDF、DOCX、TXT）
     - 图片（JPG、PNG、SVG）
     - 视频（MP4、MOV）
     - 压缩文件（ZIP、TAR、DMG）
     - 代码/项目文件夹（包含代码的文件夹）
     - 电子表格（XLSX、CSV）
     - 演示文稿（PPTX、KEY）
     - 按用途分类：
       - 工作文件 vs. 个人文件
       - 正在使用的文件 vs. 已归档的文件
       - 项目专用文件
       - 参考资料
       - 临时文件
     - 按日期分类：
       - 本年度/月份的文件
       - 以往年度的文件
       - 非常旧的文件（适合归档）

4. **查找重复文件**：
   （根据用户需求）搜索重复文件：
   ```bash
   # Find exact duplicates by hash
   find [directory] -type f -exec md5 {} \; | sort | uniq -d
   
   # Find files with same name
   find [directory] -type f -printf '%f\n' | sort | uniq -d
   
   # Find similar-sized files
   find [directory] -type f -printf '%s %p\n' | sort -n
   ```
   - 对于每一组重复文件：
     - 显示所有文件路径
     - 显示文件大小和修改日期
     - 建议保留哪些文件（通常选择最新或命名最好的文件）
     - **重要提示**：删除前务必确认

5. **制定整理计划**：
   在进行修改前，提供一个清晰的整理方案：
   ```markdown
   # Organization Plan for [Directory]
   
   ## Current State
   - X files across Y folders
   - [Size] total
   - File types: [breakdown]
   - Issues: [list problems]
   
   ## Proposed Structure
   
   ```
   ```
   [目录]/
   ├── 工作/
   │   ├── 项目/
   │   ├── 文档/
   │   └── 归档/
   ├── 个人/
   │   ├── 照片/
   │   ├── 文档/
   │   └── 媒体/
   └── 下载/
       ├── 待分类/
       └── 归档/
   ```
   ```
   
   ## Changes I'll Make
   
   1. **Create new folders**: [list]
   2. **Move files**:
      - X PDFs → Work/Documents/
      - Y images → Personal/Photos/
      - Z old files → Archive/
   3. **Rename files**: [any renaming patterns]
   4. **Delete**: [duplicates or trash files]
   
   ## Files Needing Your Decision
   
   - [List any files you're unsure about]
   
   Ready to proceed? (yes/no/modify)
   ```

6. **执行整理**：
   获得确认后，系统地执行整理操作：
   ```bash
   # Create folder structure
   mkdir -p "path/to/new/folders"
   
   # Move files with clear logging
   mv "old/path/file.pdf" "new/path/file.pdf"
   
   # Rename files with consistent patterns
   # Example: "YYYY-MM-DD - Description.ext"
   ```

**重要规则**：
   - 删除任何文件前务必确认
   - 记录所有文件移动操作，以便随时恢复
   - 保留文件的原始修改日期
   - 谨慎处理文件名冲突
   - 如果遇到意外情况，请停止操作并询问

7. **提供整理后的总结和维护建议**：
   整理完成后：
   ```markdown
   # Organization Complete! ✨
   
   ## What Changed
   
   - Created [X] new folders
   - Organized [Y] files
   - Freed [Z] GB by removing duplicates
   - Archived [W] old files
   
   ## New Structure
   
   [Show the new folder tree]
   
   ## Maintenance Tips
   
   To keep this organized:
   
   1. **Weekly**: Sort new downloads
   2. **Monthly**: Review and archive completed projects
   3. **Quarterly**: Check for new duplicates
   4. **Yearly**: Archive old files
   
   ## Quick Commands for You
   
   ```
   # 查找本周修改过的文件
   find . -type f -mtime -7
   
   # 按类型对下载文件进行排序
   [自定义排序命令]
   
   # 查找重复文件
   [自定义命令]
   ```
   
   Want to organize another folder?
   ```

## 示例

### 示例 1：整理下载文件（用户：Justin Dielmann）

**用户**：“我的下载文件夹里有500多个文件，太乱了。请帮我整理一下。”

**操作过程**：
1. 分析下载文件夹
2. 分类文件类型：工作文档、个人照片、安装程序、随机PDF文件
3. 建议文件夹结构：
   - 下载/
     - 工作/
     - 个人/
     - 安装程序/（DMG、PKG文件）
     - 归档/
     - 待分类/
4. 征求用户确认
5. 根据文件内容和名称智能地移动文件
6. 整理结果：500个文件 → 5个有序的文件夹

### 示例 2：查找并删除重复文件

**用户**：“帮我找到文档中的重复文件，并决定保留哪些。”

**操作结果**：
```markdown
# Found 23 Sets of Duplicates (156 MB total)

## Duplicate Set 1: "proposal.pdf"
- `/Documents/proposal.pdf` (2.3 MB, modified: 2024-03-15)
- `/Documents/old/proposal.pdf` (2.3 MB, modified: 2024-03-15)
- `/Desktop/proposal.pdf` (2.3 MB, modified: 2024-03-10)

**Recommendation**: Keep `/Documents/proposal.pdf` (most recent in correct location)
Delete the other 2 copies?

[Continue for all duplicates...]
```

### 示例 3：重构项目文件夹结构

**用户**：“请查看我的 ~/Projects 目录，并提出改进方案。”

**操作结果**：
```
Projects/
├── 正在使用的/
│   ├── 客户项目/
│   ├── 辅助项目/
│   └── 学习资料/
├── 归档/
│   ├── 2022/
│   ├── 2023/
│   └── 2024/
└── 模板/
```

### 示例 4：按日期整理照片

**用户**：“按年份和月份整理我的照片文件夹。”

**操作结果**：
根据照片的 EXIF 数据或修改日期创建文件夹结构：
```
Photos/
├── 2023/
│   ├── 01-January/
│   ├── 02-February/
│   └── ...
├── 2024/
│   ├── 01-January/
│   └── ...
└── Unsorted/
```

然后根据这些信息移动照片文件。

## 常见的整理任务

- **下载文件清理**  
```
Organize my Downloads folder - move documents to Documents, 
images to Pictures, keep installers separate, and archive files 
older than 3 months.
```

- **项目文件整理**  
```
Review my Projects folder structure and help me separate active 
projects from old ones I should archive.
```

- **删除重复文件**  
```
Find all duplicate files in my Documents folder and help me 
decide which ones to keep.
```

- **桌面文件整理**  
```
My Desktop is covered in files. Help me organize everything into 
my Documents folder properly.
```

- **照片文件整理**  
```
Organize all photos in this folder by date (year/month) based 
on when they were taken.
```

- **区分工作文件和个人文件**  
```
Help me separate my work files from personal files across my 
Documents folder.
```

## 专业建议

1. **从小处开始**：从某个混乱的文件夹（如下载文件夹）开始，逐步建立信任。
2. **定期维护**：每周对下载文件夹进行清理。
3. **统一文件命名规则**：重要文件使用“YYYY-MM-DD - 描述”的格式。
4. **积极归档**：将旧项目文件移至归档文件夹，而不是直接删除。
5. **区分工作文件和归档文件**：保持工作文件和归档文件的清晰界限。
6. **信任系统**：让 Claude 来处理文件存放位置的决策过程。

## 最佳实践

- **文件夹命名**：
  - 使用清晰、描述性的名称
  - 避免使用空格（使用连字符或下划线）
  - 名称要具体：例如“client-proposals”而不是“docs”
  - 使用前缀区分文件类型：如“01-current”、“02-archive”

- **文件命名**：
  - 包含日期：例如“2024-10-17-meeting-notes.md”
  - 名称要具有描述性：例如“q3-financial-report.xlsx”
  - 避免在文件名中包含版本号（使用版本控制工具）
  - 删除不必要的文件扩展名：例如将“document-final-v2 (1).pdf”改为“document.pdf”

- **何时归档**：
  - 6个月以上未使用的文件
  - 完成的项目文件（可能日后还需要使用）
  - 迁移到新系统后的旧版本文件
  - 犹豫是否删除的文件（先归档）

## 相关应用场景

- 为新电脑设置文件组织结构
- 准备文件以备备份或归档
- 在存储清理前进行整理
- 整理共享团队文件夹
- 构建新项目文件夹的结构