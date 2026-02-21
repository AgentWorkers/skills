---\n  
**名称：Ollama SEO Auditor**  
**描述：** 使用 Ollama LLM 和 OpenClaw 网络工具（web_fetch、browser）进行本地 SEO 网站审计。适用于用户请求 SEO 分析、关键词检查、网站结构/速度评估或优化建议的场景。触发命令包括：`audit SEO`、`check site performance`、`analyze web page SEO`。该工具在 VPS 上本地运行，以确保数据隐私并降低成本。  

---\n  
# Ollama SEO Auditor  

## 快速审计流程：  
1. 使用 `web_fetch` 获取目标网站的 HTML 内容。  
2. 向 Ollama（llama3:8b）发送提示：“分析 SEO：关键词、元标签、标题、图片 alt 属性以及从 HTML 中估算的页面速度（评分范围：1-10 分）。根据分析结果进行相应的优化。”  
3. （可选）使用浏览器查看网站的视觉效果并截图。  
4. 生成包含评分结果的 Markdown 报告。  

## 使用的工具：  
- 执行命令：`exec 'ollama run llama3.8b "prompt"'`  
- 使用 `web_search 'SEO best practices 2026'` 查找最新的 SEO 最佳实践信息。  

## 参考资料：  
详情请参阅 `references/seo-checklist.md` 文件。  

## 执行脚本：  
使用 `scripts/audit.py` 文件执行完整的审计流程。