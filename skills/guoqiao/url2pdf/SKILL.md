---
name: url2pdf
description: 将 URL 转换为适合移动设备阅读的 PDF 格式。
author: guoqiao
metadata: {"openclaw":{"always":true,"emoji":"🦞","homepage":"https://clawhub.ai/guoqiao/url2pdf","os":["darwin","linux","win32"],"requires":{"bins":["uv"]}}}
triggers:
- "/url2pdf <url>"
- "Save this url as pdf"
- "Convert to pdf for mobile"
---

# 将网页链接转换为适合移动设备阅读的PDF文件

给定一个网页的URL，将其转换为适合移动设备阅读的PDF格式。

请参考[示例](https://github.com/guoqiao/skills/tree/main/url2pdf/examples)。

## 需求

- `uv`（用于执行转换的命令工具）

## 安装

`playwright`本身会通过`uv`自动安装，同时还需要安装相应的浏览器：
```
uvx playwright install chromium
```

## 使用方法

```bash
uv run --script ${baseDir}/url2pdf.py "${url}"
```
转换后的PDF文件路径会输出到标准输出（stdout）。

### 代理服务器（Agent）使用说明

1. **运行脚本**：将需要转换的URL作为参数传递给脚本。
2. **处理输出**：脚本会输出PDF文件的路径。
可以使用`message`工具将PDF文件作为文档消息发送给用户：
```json
{
   "action": "send",
   "filePath": "<filepath>"
}
```