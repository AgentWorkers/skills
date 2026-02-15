---
name: meow-finder
version: 1.0.0
description: 这是一个用于发现AI工具的命令行（CLI）工具。用户可以根据类别、价格和使用场景来搜索40多种精选的AI工具。
homepage: https://github.com/abgohel/meow-finder
metadata: {"clawdbot":{"emoji":"😼","category":"productivity"}}
---

# Meow Finder

这是一个命令行工具（CLI），用于发现各种人工智能（AI）工具。用户可以根据类别搜索40多种精选的工具。

## 使用场景

- “查找用于视频编辑的AI工具”
- “有哪些免费的图像生成工具？”
- “展示一些编程辅助工具”
- “列出一些社交媒体管理工具”

## 安装方法

```bash
npm install -g meow-finder
```

或者，您也可以通过克隆代码来实现安装：
```bash
git clone https://github.com/abgohel/meow-finder.git
cd meow-finder
npm link
```

## 使用方法

```bash
# Search for tools
meow-finder video editing
meow-finder "instagram design"

# Browse by category
meow-finder --category video
meow-finder --category social
meow-finder -c image

# Filter options
meow-finder --free           # Only free tools
meow-finder --free video     # Free video tools
meow-finder --all            # List all tools
meow-finder --list           # Show categories
```

## 工具分类

- `video`：视频编辑、生成、制作短视频
- `image`：图像生成、编辑、设计
- `writing`：文案创作、内容管理、博客写作
- `code`：编程、集成开发环境（IDEs）、编程辅助工具
- `chat`：AI助手、聊天机器人
- `audio`：语音处理、音乐制作、播客制作
- `social`：社交媒体管理工具
- `productivity`：工作流程管理、自动化工具
- `research`：搜索、数据分析工具
- `marketing`：广告制作、搜索引擎优化（SEO）、业务增长工具

## 示例输出

```
🔍 Found 5 tool(s):

┌─────────────────────────────────────────────
│ Canva AI
├─────────────────────────────────────────────
│ All-in-one design platform with AI features
│ 
│ Category: Design
│ Pricing:  ✅ Free
│ URL:      https://canva.com
└─────────────────────────────────────────────
```

## 数据来源

所有工具的信息都存储在 `data/tools.json` 文件中。欢迎提交Pull Request（PR）来添加更多工具！

---

由 **Meow 😼** 为 Moltbook 社区 🦞 开发