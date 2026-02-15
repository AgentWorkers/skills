---
name: podcast-to-substack
description: 将播客剧集从 RSS 和 Notion 生成并发布到 Substack，同时确保 Apple Podcasts 的嵌入功能正常工作并能正确提取图片。此外，还需生成适合在 LinkedIn 上发布的配套文章。该方案适用于需要优化播客到 Substack 的工作流程、解决 Notion 中图片获取失败的问题、避免 Substack 中的文本嵌入问题，或需要将播客剧集摘要同步发布到 LinkedIn 的场景。
---

# Podcast Substack + LinkedIn

在处理 Realist 播客剧集的发布时，请执行以下工作流程。

## 输入参数
- RSS 源地址
- 包含剧集脚本的 Notion 数据源/数据库 ID
- Notion API 密钥（`NOTION_API_KEY` 或 `~/.config/notion/api_key`）
- Substack 的发布权限

## 工作流程
1. 获取最近的剧集：
```bash
python3 scripts/fetch_rss.py "$RSS_URL" 3
```
2. 从 Notion 中获取剧集脚本和图片（递归遍历数据结构，包含图片下载）：
```bash
python3 scripts/fetch_notion_episode.py "EPISODE_NUMBER"
```
3. 根据脚本文本生成 Substack 的草稿内容。
4. 使用 `references/substack-embed-playbook.md` 中的 playbook 来发布内容，并确保嵌入功能正常工作。
5. 从相同的内容生成 LinkedIn 的发布文案：
```bash
python3 scripts/render_linkedin_post.py --json-file episode.json
```
6. 发布或将 LinkedIn 的文案放入待发布队列中。

## 不可更改的规则
- 在 Substack 中嵌入播客内容时，禁止使用 iframe 代码或 markdown 链接。
- 建议直接使用现有的 Substack 草稿模板（该模板已包含可正常使用的嵌入功能）。
- 如果需要创建新的帖子，请使用 `/embed` 标签，并在发布前确认播放器卡片的显示效果。
- 为确保可靠性，请使用 Apple Podcasts 的官方显示 URL 作为备用方案。

## 参考资料
- Substack 的嵌入功能说明：`references/substack-embed-playbook.md`
- LinkedIn 的格式化指南：`references/linkedin-playbook.md`