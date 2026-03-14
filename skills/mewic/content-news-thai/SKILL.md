---
name: content-news-thai
description: 生成新闻风格的社交媒体图片（尺寸为1080x1350），并在图片上叠加泰文文字及相应的标题说明。该功能可用于创建内容、制作新闻帖子的图片，或为Facebook/Instagram生成完整的图片+标题组合。系统支持渲染泰文字体（Kanit、Prompt、Sarabun），确保字体显示效果达到像素级完美。触发命令包括：“ทำ content”、“ทำรูปข่าว”、“สร้างรูปโพส”、“make content”、“news image”、“headline image”。
---
# 泰文新闻内容生成

生成带有泰文文字叠加和标题的社交媒体新闻风格图片。

## 设置（仅首次使用）

运行设置脚本以安装依赖项（canvas、泰文字体）：

```bash
bash <SKILL_DIR>/scripts/setup.sh
```

在 Docker/VPS 上，这将安装：libcairo2、libpango 以及泰文字体（Kanit、Prompt、Sarabun）。
在 macOS 上，使用 Homebrew 来安装 Cairo/Pango。

## 生成新闻图片

```bash
cd <SKILL_DIR>/scripts && node gen-news.mjs '<json>'
```

### 参数

| 参数 | 是否必填 | 描述 |
|---|---|---|
| headline | ✅ | 主标题（泰文/英文，自动换行） |
| sub | | 子标题 |
| badge | | 标签文字（默认："AI NEWS"） |
| badgeColor | | 标签颜色（默认："#CC0000"） |
| bgImage | | 背景图片路径或 URL |
| bgColor | | 备用背景渐变色（默认："#0a0a1a"） |
| source | | 来源信息（底部显示） |
| output | ✅ | 输出文件路径（.jpg 格式） |
| brandName | | 水印文字（右下角显示） |
| accentColor | | 底部栏颜色（默认："#CC0000"） |

### 示例

```bash
cd <SKILL_DIR>/scripts && node gen-news.mjs '{"headline":"AI กำลังเปลี่ยนวงการค้าปลีก","sub":"ยอดขายพุ่ง 40% ใน 6 เดือน","badge":"BREAKING NEWS","source":"Reuters • มี.ค. 2026","brandName":"MY BRAND","output":"/tmp/news_post.jpg"}'
```

输出结果：JSON `{"status":"done","output":"/tmp/news_post.jpg","size":"1080x1350","type":"image"}`

## 背景图片

有两种方法：
1. **使用 bgImage** — 提供图片的路径或 URL。脚本会使用深色渐变来增强文字的可读性。
2. **不使用 bgImage** — 生成带有细微网格图案的深色渐变背景。适合以文字为主的帖子。

为了获得最佳效果，请先生成背景图片（可以使用 AI 模型生成图片），保存后将其路径作为 `bgImage` 传递给脚本。

## 完整工作流程：

当需要创建一套完整的内容时：
1. **编写标题和子标题** — 简洁有力，适合泰文阅读。
2. **生成背景图片** — 使用 AI 图像生成工具或设置背景颜色。
3. **运行 gen-news.mjs** — 生成 1080x1350 像素的图片，并叠加泰文文字。
4. **编写标题文字** — 采用故事叙述风格，使用简短的句子，并以引人入胜的问题结尾。
5. **返回结果** — 将图片路径和标题文字提供给用户。

## 标题文字编写指南：
- 以吸引注意力的开头语句开头。
- 用简短的句子逐步讲述故事。
- 包含品牌的观点或立场。
- 以总结性语句结尾，提出一个具体问题（如适用）。
- 添加 3-5 个相关标签。
- 不要使用通用的结尾语，如“คิดเห็นยังไงคอมเมนต์มา”。

## 故障排除：
- **出现 "canvas" 错误** — 重新运行 setup.sh 脚本。
- **字体显示不正确** — 检查 assets/fonts/ 目录中是否有 .ttf 文件，然后重新运行 setup.sh。
- **找不到 bgImage** — 使用绝对路径或 URL。