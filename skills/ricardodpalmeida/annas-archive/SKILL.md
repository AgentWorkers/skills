---
name: annas-archive
description: 从 Anna 的档案中查找并下载电子书或论文，优先选择 EPUB 格式的文件，并将下载结果存储在 `/tmp` 目录中。当用户请求获取某本书或论文时（尤其是在 arXiv 没有找到相关资源的情况下），可以使用此功能。
---
# annas-archive

## 工作流程
1. 搜索并排序书籍（优先考虑 EPUB 格式的书籍）：
   - `scripts/anna_epub_first.py --query "<query>"`
2. 根据请求下载书籍：
   - `scripts/anna_epub_first.py --query "<query>" --download`
3. 如果没有找到匹配的书籍，则在聊天框中报告该情况并停止执行。

可选的 MCP 搜索功能：
- `mcporter call anna.book_search query="<query>"`

## 运行时配置
- 运行脚本：`scripts/run-annas-mcp.sh`
- 下载文件路径：`/tmp/annas-archive-downloads`
- 清理临时文件：`scripts/cleanup_annas_tmp.sh`
- 可选环境变量：
  - `ANNAS_MCP_COMMAND`
  - `ANNAS_MCP_SOURCE_DIR`