---
name: nano-pdf
description: 使用 `nano-pdf` CLI，通过自然语言指令来编辑 PDF 文件。
homepage: https://pypi.org/project/nano-pdf/
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["nano-pdf"]},"install":[{"id":"uv","kind":"uv","package":"nano-pdf","bins":["nano-pdf"],"label":"Install nano-pdf (uv)"}]}}
---

# nano-pdf

使用 `nano-pdf` 可以通过自然语言指令对 PDF 文件中的特定页面进行编辑。

## 快速入门

```bash
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"
```

注意事项：
- 页面编号的计数方式（从 0 开始还是从 1 开始）取决于工具的版本或配置；如果结果出现偏差，请尝试使用另一种计数方式。
- 在发送 PDF 文件之前，务必先检查其内容是否正确无误。