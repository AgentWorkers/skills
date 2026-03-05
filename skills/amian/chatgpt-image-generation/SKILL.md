---
name: chatgpt-image-generation
description: 使用 Playwright 浏览器自动化工具从 ChatGPT 生成图像：首先打开 ChatGPT，发送提示内容，等待图像生成完成，最后保存生成的图像文件。
---
# ChatGPT 图像生成技能

使用 Playwright 自动化 ChatGPT 的 Web 用户界面以生成图像。

## 先决条件

```bash
npm install playwright
npx playwright install chromium
```

## 使用方法

```bash
# Generate images from prompts file
node generate.js --prompts prompts.json --output ./images

# Resume from a specific index
node generate.js --prompts prompts.json --output ./images --start 5

# Run in headless mode
node generate.js --prompts prompts.json --output ./images --headless
```

## 提示文件格式

```json
["prompt 1", "prompt 2"]
```

或

```json
{ "prompts": ["prompt 1", "prompt 2"] }
```

## 工作原理

1. 在 Chrome 浏览器中打开 ChatGPT。
2. 从提示文件中逐个发送提示。
3. 等待生成的响应。
4. 在页面中找到生成的图像。
5. 将图像保存到输出目录中。
6. 对所有提示重复此过程。

## 输出结果

- 带编号的图像文件：`001.png`、`002.png` 等。
- `results.jsonl` — 每个提示的结果日志。

## 登录（仅一次）

如果尚未登录 ChatGPT：
1. 运行脚本（浏览器将自动打开 ChatGPT）。
2. 登录 ChatGPT。
3. 会话信息会被保存以供后续使用。