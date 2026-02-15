---
name: vestaboard
description: 使用 Vestaboard Cloud API (cloud.vestaboard.com) 以及可选的旧版读写（RW）端点，在 Vestaboard 上读取和写入消息。当需要在该平台上显示文本、更新信息牌/公告板内容、显示简短的状态消息、使用颜色/填充字符代码渲染简单的像素艺术图像，或检索当前的公告板信息时，可以使用此功能。
---

# Vestaboard

## 安全性
- 必须通过环境变量来传递令牌（切勿将令牌直接嵌入到提示信息、日志或提交信息中）。
  - 推荐使用的环境变量：`VESTABOARD_TOKEN`
  - 可选的旧版备用方式：`VESTABOARDRW_KEY`

## 约束条件
- Vestaboard 的标准布局为 **6 行 x 22 列**。
- 文本输入默认会被格式化为 6x22 的格式（大写字符 + 自动换行；超出指定列数的内容会被截断）。

## 快速使用（本地命令行界面）

```bash
# from repo root
npm install

# Preview formatting only
node scripts/vb.js preview "Hello from Quarterbridge Farm"

# Read current message (JSON)
node scripts/vb.js read

# Write text
node scripts/vb.js write "EGGS READY"

# Write a numeric layout (6x22 array of character codes)
node scripts/vb.js write-layout content/layouts/forest-depth.json
```

## 示例内容
- 数字化布局的模板文件位于 `content/layouts/*.json` 中。
- 用于预览的用户界面模板文件位于 `content/previews/*.md` 中。