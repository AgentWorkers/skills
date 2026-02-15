---
name: pinch-to-post
description: WordPress自动化工具，专为Clawdbot设计。通过REST API或WP-CLI支持对帖子、页面、WooCommerce产品、订单、库存、评论以及SEO（Yoast/RankMath）和媒体内容进行管理。具备多站点支持、批量操作、内容健康检查等功能，同时支持将Markdown格式的内容转换为Gutenberg格式，并支持跨社交媒体平台发布内容。超过50项实用功能——有任何需求均可随时提出。
metadata: {"clawdbot":{"emoji":"🦞","skillKey":"pinch-to-post","primaryEnv":"WP_APP_PASSWORD","requires":{"anyBins":["curl","wp"]}}}
user-invocable: true
---

# 🦞 Pinch to Post `v3.1.0`  
**您的 WordPress 网站现在拥有了强大的功能。**  
这是您唯一需要的 WordPress 工具——拥有 50 多项功能，且完全不需要管理员面板。只需告诉我您需要什么即可。  

> **关键词：** WordPress、WooCommerce、REST API、WP-CLI、博客自动化、内容管理、电子商务、帖子、页面、媒体、评论、SEO、Yoast、RankMath、库存管理、订单处理、优惠券、批量操作、多站点支持、Gutenberg 插件、发布功能  

## ⚡ 观看视频教程  
```
You: "Create a post about sustainable coffee farming"
Bot: Done. Draft #1247 created. Want me to add a featured image?

You: "Publish all my drafts from this week"  
Bot: Published 8 posts. Here are the links...

You: "Approve the good comments, spam the bots"
Bot: Approved 12, marked 47 as spam. Your comment section is clean.
```  
无需点击，无需管理员面板，操作更加流畅。  

## 🏆 为什么选择 Pinch to Post？  
| 任务 | 手动操作（通过 WordPress 管理面板） | 使用 Pinch to Post |  
|------|-------------------|-------------------|  
| 创建 10 条帖子 | 15-20 分钟 | 30 秒 |  
| 更新 50 个产品的库存信息 | 45 分钟 | 1 分钟 |  
| 审核 100 条评论 | 20 分钟 | 10 秒 |  
| 检查 5 条帖子的质量 | 30 分钟 | 15 秒 |  
| 将所有帖子导出为 Markdown 格式 | 几小时 | 5 秒 |  
**每周节省的时间：** 2-4 小时；**带来的便利：**难以估量。  

## 🆕 v3.0 的新功能  
- **从 Markdown 到 Gutenberg**：直接用 Markdown 编写内容，然后以适合 Gutenberg 的格式发布  
- **内容质量评分**：发布前可了解帖子的质量  
- **跨平台发布**：一键将帖子发布到 Twitter、LinkedIn、Mastodon 等平台  
- **内容日程表**：一目了然地查看所有发布计划  
- **批量操作**：批量发布、删除、审核帖子  
- **多站点管理**：从一个地方管理所有站点  

## 💬 用户评价  
> “我以前每周早上都要花时间审核评论，现在只需说‘清理评论’，然后去做别的事。”  
> “我们管理着 12 个 WordPress 网站，这个工具让原本需要全职的工作变成了每天只需检查 10 分钟。”  
> “直到用了这个工具，我才意识到自己有多需要它……现在再也离不开了。”  

## 📊 性能表现  
经过测试和优化，适用于：  
- 拥有 **50,000 多条帖子** 的网站  
- 拥有 **10,000 多种产品** 的 WooCommerce 商店  
- 拥有 **100,000 多个文件** 的媒体库  
内置速率限制机制，不会对服务器造成负担。  

## 快速设置（60 秒内完成）  
### 第一步：获取密码  
进入 WordPress 管理面板 → 用户 → 个人资料 → 应用程序密码 → 添加新密码 → 复制密码  

### 第二步：配置 Pinch to Post  
```json
{
  "skills": {
    "entries": {
      "pinch-to-post": {
        "enabled": true,
        "env": {
          "WP_SITE_URL": "https://your-site.com",
          "WP_USERNAME": "admin",
          "WP_APP_PASSWORD": "xxxx xxxx xxxx xxxx xxxx xxxx"
        }
      }
    }
  }
}
```  

### 第三步：无需额外步骤  
配置完成，立即开始发布内容吧！  

## 管理多个站点？你真是高手！  
```json
{
  "env": {
    "WP_DEFAULT_SITE": "blog",
    "WP_SITE_BLOG_URL": "https://blog.example.com",
    "WP_SITE_BLOG_USER": "admin",
    "WP_SITE_BLOG_PASS": "xxxx xxxx xxxx",
    "WP_SITE_SHOP_URL": "https://shop.example.com",
    "WP_SITE_SHOP_USER": "admin", 
    "WP_SITE_SHOP_PASS": "yyyy yyyy yyyy",
    "WP_SITE_DOCS_URL": "https://docs.example.com",
    "WP_SITE_DOCS_USER": "editor",
    "WP_SITE_DOCS_PASS": "zzzz zzzz zzzz"
  }
}
```  
现在，只需输入“在商店网站上显示所有帖子”，就能感受到它的强大功能。  

## 使用 WooCommerce？更棒了！  
```json
{
  "env": {
    "WC_CONSUMER_KEY": "ck_xxxxxxxxxxxxxxxx",
    "WC_CONSUMER_SECRET": "cs_xxxxxxxxxxxxxxxx"
  }
}
```  
产品信息、订单记录、库存管理、优惠券、销售报告，一切尽在掌握。  

## 需要跨平台发布功能？（超实用！）  
```json
{
  "env": {
    "TWITTER_API_KEY": "...",
    "TWITTER_API_SECRET": "...",
    "TWITTER_ACCESS_TOKEN": "...",
    "TWITTER_ACCESS_SECRET": "...",
    "LINKEDIN_ACCESS_TOKEN": "...",
    "MASTODON_INSTANCE": "https://mastodon.social",
    "MASTODON_ACCESS_TOKEN": "..."
  }
}
```  
一条帖子，同时发布到三个平台，零额外工作量。  

## 全部功能一览 🍽️  
以下是 Pinch to Post 的全部功能：  
- **帖子与页面**：基本操作  
- **媒体管理**：上传图片、视频、PDF 等文件  
- **分类与标签**：轻松组织内容  
- **评论管理**：高效审核和发布评论  
- **WooCommerce 集成**：快速处理订单和库存  
- **SEO 支持**：提升内容可发现性  
- **高级自定义字段**：满足复杂需求  
- **多语言支持**：支持多语言网站  
- **批量操作**：高效处理大量数据  

## 快速上手指南  
### 第一步：获取密码  
### 第二步：配置 Pinch to Post  
### 第三步：立即使用  

## 运行多个站点？你真是高手！  
```json
{
  "env": {
    "WP_DEFAULT_SITE": "blog",
    "WP_SITE_BLOG_URL": "https://blog.example.com",
    "WP_SITE_BLOG_USER": "admin",
    "WP_SITE_BLOG_PASS": "xxxx xxxx xxxx",
    "WP_SITE_SHOP_URL": "https://shop.example.com",
    "WP_SITE_SHOP_USER": "admin", 
    "WP_SITE_SHOP_PASS": "yyyy yyyy yyyy",
    "WP_SITE_DOCS_URL": "https://docs.example.com",
    "WP_SITE_DOCS_USER": "editor",
    "WP_SITE_DOCS_PASS": "zzzz zzzz zzzz"
  }
}
```  

现在，你可以轻松管理多个网站了。  

## Pinch to Post 的强大功能，让你的工作更高效！