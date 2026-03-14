---

**名称：Defuddle Web Cleaner**  
**描述：** 使用 Defuddle 工具从网页中提取干净、可读的文章内容。当用户提供网址或 HTML 代码时，该工具可生成可读的文章文本、Markdown 格式的文章内容或结构化的元数据。适用于网页抓取、研究工作流程、笔记记录以及将网页转换为 Markdown 格式等场景。  

---

# Defuddle Web Cleaner  
**功能：** 从网页中提取主要的可读内容。  
**特点：** 自动去除以下不必要的元素：  
- 导航栏  
- 侧边栏  
- 广告  
- 评论  
- 底部栏  
- 社交媒体按钮  

**输出结果：** 清晰的文章内容。  

## 支持的输入格式：**  
1. 网址（URL）  
2. 原始 HTML 代码  
3. 网页文本  

## 输出格式：**  
**默认输出：**  
- 标题  
- 作者  
- 网站  
- 发布日期  
- Markdown 格式的文章内容  

**可选输出格式（JSON）：**  
```json  
{  
  "title": "AI is Changing Everything",  
  "author": "Jane Smith",  
  "site": "Example Blog",  
  "description": "人工智能正在改变各行各业...",  
  "published": "2023-01-15",  
  "content": "人工智能正在改变各行各业……",  
  "contentMarkdown": "人工智能正在改变各行各业……"  
}  
```  

## 处理流程：**  
1. 检测输入类型；  
2. 加载网页 HTML；  
3. 运行 Defuddle 解析器；  
4. 提取元数据；  
5. （如需）将内容转换为 Markdown 格式；  
6. 返回处理后的干净内容。  

## 使用示例：**  
**输入：** `https://example.com/blog/ai`  
**输出：**  
```markdown  
# AI is Changing Everything  
人工智能正在改变各行各业……  
```  

## 使用建议：**  
- 将文章保存到 Obsidian 文本编辑器中；  
- 构建研究数据集；  
- 清理网页以供大型语言模型（LLM）使用；  
- 摘要文章内容。