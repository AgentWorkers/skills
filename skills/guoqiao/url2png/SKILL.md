---
name: url2png
description: 将 URL 转换为适合移动设备阅读的 PNG 图片格式。
metadata: {"openclaw":{"always":true,"emoji":"🦞","homepage":"https://clawhub.ai/guoqiao/url2png","os":["darwin","linux"],"requires":{"bins":["uv"]}}}
triggers:
- "/url2png <url>"
- "Save this url as image ..."
- "Take long screenshot for this url"
---

# 将网页URL转换为适合移动设备查看的PNG图片

给定一个网页的URL，将其转换为适合移动设备查看的PNG图片。

请参考[示例](https://github.com/guoqiao/skills/tree/main/url2png/examples)


## 需求

- 使用`uv`工具进行转换


## 安装

```bash
bash ${baseDir}/install.sh
```

该脚本将：

- 安装`shot-scraper`作为`uv`工具
- 安装`chromium`浏览器模块，以便`shot-scraper`和`playwright`能够使用


## 使用方法

```bash
# save to ~/Pictures with proper name by default
bash url2png.sh <url>
# specify output png path
bash url2png.sh <url> path/to/png
```


## 代理使用说明

1. 运行`url2png.sh`脚本。
2. 查找生成的PNG图片文件（如果未指定，默认保存在`~/Pictures`目录下）。
3. 将文件发送给用户。**重要提示：**为避免压缩或尺寸限制（尤其是在使用Telegram时），请将图片以**文档/文件**的形式发送（或将其压缩成ZIP文件），不要以照片的形式发送。