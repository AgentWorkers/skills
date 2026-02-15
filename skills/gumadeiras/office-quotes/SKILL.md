---
name: office-quotes
description: **功能说明：**  
该工具能够从《The Office》（美国版）中生成随机引语。它提供了326条离线引语，并支持在线模式，支持使用SVG格式的卡片、角色头像以及通过`akashrajpurohit` API获取完整的剧集元数据。适用于娱乐、破冰活动或任何需要《The Office》引语的场景。  

**主要特性：**  
1. **离线引语**：可随时查看326条预先准备好的《The Office》引语。  
2. **在线模式**：支持在线使用，可查看带有SVG格式卡片和角色头像的引语。  
3. **API集成**：通过`akashrajpurohit` API获取剧集元数据（如剧集名称、播出日期等）。  

**使用场景：**  
- **娱乐**：用于闲暇时阅读有趣的《The Office》引语。  
- **破冰活动**：在团队会议或社交场合中作为开场白或互动环节。  
- **内容创作**：为文章、博客或社交媒体帖子添加《The Office》相关素材。  

**技术细节：**  
- **数据来源**：引语内容来源于《The Office》（美国版）的官方资源。  
- **API支持**：利用`akashrajpurohit` API获取剧集元数据，实现数据更新和扩展功能。  

**注意事项：**  
- 该工具仅用于娱乐和信息展示目的，不涉及任何侵权行为。  
- 如需使用API，请确保遵守相关服务的使用条款和许可协议。
metadata: {"clawdbot":{"requires":{"bins":["office-quotes"]},"install":[{"id":"node","kind":"node","package":"office-quotes-cli","bins":["office-quotes"],"label":"Install office-quotes CLI (npm)"}]}}
---

# office-quotes 工具

该工具可以从美国电视剧《The Office》中生成随机引语。

## 安装

```bash
npm install -g office-quotes-cli
```

## 使用方法

```bash
# Random offline quote (text only)
office-quotes

# API quote with SVG card
office-quotes --source api

# PNG output (best for Telegram)
office-quotes --source api --format png

# Light theme
office-quotes --source api --theme light
```

## 参数选项

| 参数 | 说明 |
|--------|-------------|
| `--source <src>` | 引语来源：本地文件（默认）或 API |
| `--format <fmt>` | 输出格式：svg、png、jpg、webp（默认：svg） |
| `--theme <theme>` | SVG 图标主题：深色或浅色（默认：深色） |
| `--json` | 以 JSON 格式输出结果 |

## 引语示例

> “我是想让人害怕我，还是喜欢我？很简单。两者都想要。我希望人们既害怕我又喜欢我。” — 迈克尔·斯科特（Michael Scott）  
> “熊。甜菜。《太空堡垒卡拉狄加》（Battlestar Galactica）。” — 吉姆·哈尔珀特（Jim Halpert）  
> “每当我准备做某件事时，我都会想：‘一个傻瓜会这么做吗？’如果他们会这么做，那我就不会做了。” — 德怀特·施鲁特（Dwight Schrute）  

## 项目来源

https://github.com/gumadeiras/office-quotes-cli