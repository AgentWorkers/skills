---
name: obsidian-daily
description: 通过 `obsidian-cli` 管理 Obsidian 的每日笔记。可以创建和打开每日笔记，添加条目（如日记、日志、任务、链接），按日期查找过去的笔记，以及搜索笔记库中的内容。支持相对日期的输入，例如 “昨天”、“上周五”、“3 天前”。需要先通过 Homebrew（Mac/Linux）或 Scoop（Windows）安装 `obsidian-cli`。
<<<<<<< Updated upstream
metadata:
  author: github.com/bastos
  version: "2.0"
=======
>>>>>>> Stashed changes
---

# Obsidian 日记笔记

**功能说明：**  
可以与 Obsidian 日记笔记功能进行交互，包括创建新笔记、添加条目、按日期查找笔记以及搜索内容。

## 设置  

**检查是否已配置默认的存储库（vault）：**  
```bash
obsidian-cli print-default --path-only 2>/dev/null && echo "OK" || echo "NOT_SET"
```  

如果未配置默认存储库，需向用户询问以下信息：  
1. **存储库名称**（必填）  
2. **日记笔记文件夹的路径**（默认为存储库根目录，常见路径包括 `Daily Notes`、`Journal` 或 `daily`）  
3. **日期格式**（默认为 `YYYY-MM-DD`）  

**配置存储库：**  
```bash
obsidian-cli set-default "VAULT_NAME"
```  

**Obsidian 日记笔记插件的默认设置：**  
- 日期格式：`YYYY-MM-DD`  
- 新文件的保存位置：存储库根目录  
- 模板文件的路径：（未设置）  

## 日期处理  

**获取当前日期：**  
```bash
date +%Y-%m-%d
```  

**跨平台的相对日期表示方法：**  
（以 GNU 系统为准，BSD 系统作为备用方案）：  
| 参考方式 | 命令            |  
|---------|----------------|  
| 今天       | `date +%Y-%m-%d`       |  
| 昨天       | `date -d yesterday +%Y-%m-%d 2>/dev/null \|\| date -v-1d +%Y-%m-%d` |  
| 上周五     | `date -d "last friday" +%Y-%m-%d 2>/dev/null \|\| date -v-friday +%Y-%m-%d` |  
| 3 天前     | `date -d "3 days ago" +%Y-%m-%d 2>/dev/null \|\| date -v-3d +%Y-%m-%d` |  
| 下周一     | `date -d "next monday" +%Y-%m-%d 2>/dev/null \|\| date -v+monday +%Y-%m-%d` |  

## 命令操作  

### 打开/创建今天的日记笔记：**  
```bash
obsidian-cli daily
```  
在 Obsidian 中打开今天的日记笔记；如果不存在，则根据模板创建新笔记。  

### 添加条目：**  
```bash
obsidian-cli daily && obsidian-cli create "$(date +%Y-%m-%d).md" --content "$(printf '\n%s' "ENTRY_TEXT")" --append
```  
（支持自定义文件夹路径。）  

### 阅读笔记：**  
**阅读今天的笔记：**  
```bash
obsidian-cli print "$(date +%Y-%m-%d).md"
```  
**阅读指定日期的笔记：**  
```bash
obsidian-cli print "2025-01-10.md"
```  
**阅读上周五的笔记：**  
```bash
obsidian-cli print "$(date -d yesterday +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d).md"
```  

### 搜索内容：**  
**搜索笔记内容：**  
```bash
obsidian-cli search-content "TERM"
```  
**使用交互式模糊搜索功能查找笔记：**  
```bash
obsidian-cli search
```  
**针对特定存储库进行搜索：**  
在命令前添加 `--vault "名称"` 即可。  
```bash
obsidian-cli print "2025-01-10.md" --vault "Work"
```  

## 示例输出：**  
```markdown
- Went to the doctor
- [ ] Buy groceries
- https://github.com/anthropics/skills
- 15:45 This is a log line
```  

## 使用场景：**  
- **撰写日记条目：**  
```bash
obsidian-cli daily && obsidian-cli create "$(date +%Y-%m-%d).md" --content "$(printf '\n%s' "- Went to the doctor")" --append
```  
- **记录任务：**  
```bash
obsidian-cli daily && obsidian-cli create "$(date +%Y-%m-%d).md" --content "$(printf '\n%s' "- [ ] Buy groceries")" --append
```  
- **添加链接：**  
```bash
obsidian-cli daily && obsidian-cli create "$(date +%Y-%m-%d).md" --content "$(printf '\n%s' "- https://github.com/anthropics/skills")" --append
```  
- **记录带有时间戳的日志：**  
```bash
obsidian-cli daily && obsidian-cli create "$(date +%Y-%m-%d).md" --content "$(printf '\n%s' "- $(date +%H:%M) This is a log line")" --append
```  
- **阅读上周五的笔记：**  
```bash
obsidian-cli print "$(date -d 'last friday' +%Y-%m-%d 2>/dev/null || date -v-friday +%Y-%m-%d).md"
```  
- **搜索包含“meeting”关键词的笔记：**  
```bash
obsidian-cli search-content "meeting"
```