---
name: bookmark-keeper
description: "这款书签管理器具备标签功能、失效链接检测以及多格式导出功能。适用于需要保存书签、按标签对书签进行分类管理、搜索已保存的链接、检查链接是否失效，或将书签导出为 HTML 或 Markdown 格式的用户。触发事件包括：添加新书签、点击链接、访问 URL、保存链接以及将链接添加到收藏夹或设置“稍后阅读”。"
---
# Linkwarden  
**书签管理器——保存与整理链接**

## 为什么需要这个工具？  
- 专为个人日常使用设计，简单实用  
- 无需依赖任何外部组件，仅使用标准系统工具  
- 数据存储在本地，确保您的信息安全  
- 由 BytesAgain 开发并实现  

## 命令说明  
运行 `scripts/linkwarden.sh <命令>` 来使用这些命令：  

- `add` — `<url> [标题] [标签]`   添加书签  
- `list` — `[数量]`             列出最近添加的书签（默认显示 20 条）  
- `search` — `<查询内容>`         搜索书签  
- `tag` — `<标签>`             按标签筛选书签  
- `tags` —             显示所有标签  
- `check` —             检查失效链接  
- `export` — `[格式]`           导出书签（格式：md/html/json）  
- `import` — `<文件路径>`         从文件导入书签  
- `delete` — `<url>`           删除书签  
- `stats` —             显示使用统计信息  
- `info` —             显示工具版本信息  

## 快速入门  

```bash
linkwarden.sh help
```  

> **免责声明**：  
Linkwarden 是由 BytesAgain 独立开发的原创工具，与任何第三方项目无关，也未借鉴任何第三方代码。  

---  
💬 意见反馈与功能请求：https://bytesagain.com/feedback  
由 BytesAgain 提供支持 | bytesagain.com