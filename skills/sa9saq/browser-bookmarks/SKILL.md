---
description: 检测重复的书签，检查失效的链接，并整理书签导出文件。
---

# 浏览器书签管理工具

本工具用于分析并整理浏览器书签导出的数据。

## 功能特性

- **重复检测**：在多个文件夹中查找重复的URL。
- **失效链接检查**：通过HTTP HEAD请求检测无效链接。
- **文件组织**：对书签进行分类，并建议重新整理文件夹结构。
- **导出格式支持**：Chrome和Firefox的书签格式（HTML和JSON）。

## 使用说明

1. **解析书签数据**：从HTML或JSON格式的导出文件中提取URL、标题及文件夹信息。
   ```bash
   # Extract URLs from Chrome HTML export
   grep -oP 'HREF="\K[^"]+' bookmarks.html | sort > urls.txt
   wc -l urls.txt  # total bookmarks
   ```

2. **检测重复项**：
   ```bash
   sort urls.txt | uniq -d  # duplicate URLs
   sort urls.txt | uniq -c | sort -rn | head -20  # most duplicated
   ```

3. **检查失效链接**（支持批量处理，并设置请求速率限制）：
   ```bash
   while read url; do
     code=$(curl -s -o /dev/null -w "%{http_code}" -m 5 -L "$url" 2>/dev/null)
     [ "$code" != "200" ] && echo "$code $url"
     sleep 0.5  # rate limit
   done < urls.txt
   ```

4. **报告生成格式**：
   ```
   📚 Bookmark Analysis — <filename>
   Total: 342 | Duplicates: 18 | Dead: 7

   ## Duplicates
   | URL | Count | Folders |
   |-----|-------|---------|

   ## Dead Links (non-200)
   | URL | Status | Title |
   |-----|--------|-------|
   ```

## 特殊情况处理

- **大量书签（>5000条）**：仅对部分书签进行失效链接检查；完整重复检测也是可行的。
- **需要付费访问的网站**：可能会返回403错误代码——应标记为“可能需要付费访问”，而非“失效链接”。
- **重定向链接**：自动跟踪重定向（使用`curl -L`命令）；对于永久性重定向（301状态码），需更新相关URL信息。

## 安全注意事项

- 书签文件可能包含私人或内部链接——请勿公开分享处理结果。
- 为避免IP被封禁，对外部请求设置请求速率限制。

## 所需工具

- `curl`、`grep`、`sort`（标准Unix工具）。
- 无需API密钥。

## 数据来源

- Chrome书签导出路径：`chrome://bookmarks` → “导出”功能
- Firefox书签导出路径：浏览器“图书馆” → “导出”功能