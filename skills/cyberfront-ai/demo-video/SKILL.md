---
name: demo-video
description: 通过自动化浏览器操作并捕获屏幕画面来创建产品演示视频。当用户需要录制Web应用程序的演示视频、操作指南、产品展示视频或交互式视频时，可以使用该功能。该工具支持使用Playwright CDP进行高质量屏幕录制，并利用FFmpeg进行视频编码。
---

# 演示视频制作工具

通过自动化浏览器操作，轻松制作出专业的产品演示视频。

## 概述

1. **规划**演示流程（页面、交互操作、时间安排）
2. **使用 Playwright CDP 进行屏幕录制**
3. **使用 FFmpeg 将录制的帧转换为视频**

## 快速入门

### 先决条件

- Clawdbot 浏览器已启动（使用命令 `browser action=start profile=clawd`）
- 应用程序可通过浏览器访问（本地或远程）
- 安装了 FFmpeg 用于视频编码

### 录制流程

1. 如果 Clawdbot 浏览器尚未运行，请先启动它。
2. 手动导航到应用程序页面，或使用命令 `browser action=open` 打开该页面。
3. 根据目标应用程序自定义 `scripts/record-demo.js` 脚本。
4. 运行脚本 `node scripts/record-demo.js` 进行录制。
5. 使用脚本 `bash scripts/frames-to-video.sh` 对录制的帧进行编码。

## 演示规划

请参考 `references/demo-planning.md` 以获取以下方面的指导：
- 演示流程的构建方法
- 时间控制与节奏安排
- 交互操作的设计
- 使演示更加吸引人的要素

## 脚本说明

### `scripts/record-demo.js`

这是一个基于 Playwright 的脚本模板，用于：
- 通过 CDP 连接到 Clawdbot 浏览器
- 开始屏幕录制（以 JPEG 格式保存帧）
- 执行演示流程（页面导航、点击、悬停、输入操作）
- 将录制的帧保存到指定目录

**针对每个演示进行自定义设置：**
- `DEMO_SEQUENCES` 数组：定义需要展示的页面和交互操作
- `OUTPUT_DIR`：指定输出文件的保存路径
- `FRAME_SKIP`：指定每 N 帧后跳过一帧（数值越小，录制的帧越多）

### `scripts/frames-to-video.sh`

这是一个使用 FFmpeg 进行视频编码的脚本，支持多种输出格式：
- `mp4`：H.264 编码，适合高质量和中等大小的视频文件
- `gif`：生成动画 GIF 文件，适用于嵌入到其他内容中
- `webm`：VP9 编码，文件体积较小

使用方法：`./frames-to-video.sh [input_dir] [output_name] [format]`

## 交互操作示例

```javascript
// Navigation
await page.goto('http://localhost/dashboard');
await page.waitForTimeout(2000);

// Click element
await page.locator('button:has-text("Create")').click();
await page.waitForTimeout(500);

// Hover (show tooltips, hover states)
await page.locator('.card').first().hover();
await page.waitForTimeout(1000);

// Type text
await page.locator('input[placeholder="Search"]').fill('query');
await page.waitForTimeout(500);

// Press key
await page.keyboard.press('Enter');
await page.keyboard.press('Escape');

// Scroll
await page.evaluate(() => window.scrollBy(0, 300));
```

## 使用技巧

- **时间控制**：
  - 页面加载时间约 2 秒
  - 每次交互操作之间的间隔为 0.5–1 秒
  - 展示结果所需时间约为 1.5 秒

- **帧跳过设置**：
  - 选择 3–5 来获得流畅的视频效果
  - 选择 8–10 来生成更小的视频文件

- **视频质量**：
  - JPEG 质量为 85–90 可在文件大小和清晰度之间取得平衡

- **分辨率**：
  - 输出视频的分辨率由浏览器窗口大小决定

- **循环播放**：
  - GIF 文件应能够无缝循环播放，从开始位置继续播放