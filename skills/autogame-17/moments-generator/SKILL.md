---
name: moments-generator
description: 生成一张伪造的微信朋友圈截图。当用户需要模拟带有头像、文字、图片、点赞和评论的社交媒体帖子时，可以使用此功能。
---

# Moments Generator 技能

该技能能够生成逼真的微信动态截图。

## 使用方法

1. **准备资源**：
   - 确保用户的头像和所有内容图片已保存在本地（例如，使用 `web_fetch` 或 `read` 函数）。

2. **创建配置文件**：
   创建一个临时 JSON 文件（例如 `temp_moments_config.json`），其结构如下：
   ```json
   {
     "avatar": "/path/to/avatar.png",
     "name": "User Name",
     "content": "This is the text of the moment.",
     "images": [
       "/path/to/image1.jpg",
       "/path/to/image2.jpg"
     ],
     "likes": ["Friend A", "Friend B"],
     "comments": [
       { "name": "Friend C", "text": "Nice photo!" },
       { "name": "Me", "text": "Thanks!" }
     ],
     "theme": "dark"
   }
   ```
   *注：支持 1-9 张图片。`images` 字段可以为空。`theme` 的默认值为 "light"。*

3. **生成图片**：
   运行生成脚本：
   ```bash
   node /home/crishaocredits/.openclaw/workspace/skills/moments-generator/scripts/generate.js temp_moments_config.json output_moments.png
   ```

4. **交付结果**：
   将生成的 `output_moments.png` 文件发送给用户。

## 依赖项
- Node.js
- pureimage（已打包）
- 字体（已打包/系统自带的）