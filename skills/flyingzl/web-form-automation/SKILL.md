---
name: web-form-automation
description: 使用 Playwright 自动化网页表单交互，包括登录、文件上传、文本输入和表单提交。适用于用户需要自动化网页操作、将文件上传到表单、填写表单内容、点击按钮或向 Web 应用程序提交数据的情况。该工具支持通过 cookie 进行会话管理、压缩图像上传（WebP 格式），并能够正确触发事件以确保表单能够可靠地提交。
---
# 网页表单自动化

使用 Playwright 可以可靠地自动化网页表单的操作，同时遵循最佳实践来管理会话、上传文件以及提交表单。

## 快速入门

```javascript
const { chromium } = require('playwright');

// Basic form automation
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto('https://example.com/form');

// Upload compressed images
await page.locator('input[type="file"]').setInputFiles('/path/to/image.webp');

// Type text (triggers events properly)
await page.locator('textarea').pressSequentially('Your text', { delay: 30 });

// Submit form
await page.locator('button[type="submit"]').click({ force: true });
```

## 会话管理

### 使用浏览器会话数据

当用户提供包含会话数据的 JSON 文件时：

```javascript
const sessionData = JSON.parse(fs.readFileSync('session.json', 'utf8'));

// Set cookies before navigating
for (const cookie of sessionData.cookies || []) {
  await context.addCookies([cookie]);
}

// Set localStorage/sessionStorage
await page.evaluate((data) => {
  for (const [k, v] of Object.entries(data.localStorage || {})) {
    localStorage.setItem(k, v);
  }
}, sessionData);
```

## 文件上传的最佳实践

### 图像压缩

在上传之前务必对图像进行压缩，以确保操作的可靠性：

```bash
# Convert to webp for best compression
convert input.png output.webp

# Or resize if needed
convert input.png -resize 1024x1024 output.webp
```

**大小对比：**
- 原始 PNG 格式：约 4MB
- 压缩后的 PNG 格式：约 1MB
- WebP 格式：约 30-50KB（体积减少了 99%）

### 上传顺序

```javascript
// 1. Find file inputs
const fileInputs = await page.locator('input[type="file"]').all();

// 2. Upload with waiting time
await fileInputs[0].setInputFiles('/path/to/start.webp');
await page.waitForTimeout(3000); // Wait for upload to process

await fileInputs[1].setInputFiles('/path/to/end.webp');
await page.waitForTimeout(3000);
```

## 文本输入的最佳实践

### 使用 `pressSequentially()`，而不是 `fill()`

❌ **不要使用 `fill()`** —— 这不会触发输入事件：
```javascript
await textInput.fill('text'); // May not activate submit button
```

✅ **使用 `pressSequentially()`** —— 可以模拟真实的输入过程：
```javascript
await textInput.pressSequentially('text', { delay: 30 });
```

### 手动触发事件（如有需要）

```javascript
await page.evaluate(() => {
  const el = document.querySelector('textarea');
  el.dispatchEvent(new Event('input', { bubbles: true }));
  el.dispatchEvent(new Event('change', { bubbles: true }));
});
```

## 按钮点击

### 强制点击被禁用的按钮

如果按钮显示为禁用状态但实际上可以点击：

```javascript
await button.click({ force: true });
```

### 检查按钮状态

```javascript
const isEnabled = await button.isEnabled();
const isVisible = await button.isVisible();
```

## 完整示例：视频生成表单

```javascript
const { chromium } = require('playwright');
const fs = require('fs');

async function submitVideoForm(sessionFile, startImage, endImage, prompt) {
  const browser = await chromium.launch({ 
    headless: true, 
    args: ['--no-sandbox'] 
  });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Load session if provided
  if (fs.existsSync(sessionFile)) {
    const session = JSON.parse(fs.readFileSync(sessionFile, 'utf8'));
    // Set cookies, localStorage...
  }
  
  // Navigate
  await page.goto('https://example.com/video', { 
    waitUntil: 'domcontentloaded' 
  });
  await page.waitForTimeout(3000);
  
  // Upload images (webp compressed)
  const inputs = await page.locator('input[type="file"]').all();
  await inputs[0].setInputFiles(startImage);
  await page.waitForTimeout(3000);
  await inputs[1].setInputFiles(endImage);
  await page.waitForTimeout(3000);
  
  // Select options
  await page.click('text=Seedance 2.0 Fast');
  await page.click('text=15s');
  
  // Type prompt
  const textarea = page.locator('textarea').first();
  await textarea.pressSequentially(prompt, { delay: 30 });
  await page.waitForTimeout(2000);
  
  // Submit
  await page.locator('button[class*="submit"]').click({ force: true });
  
  // Wait and screenshot
  await page.waitForTimeout(5000);
  await page.screenshot({ path: 'result.png' });
  
  await browser.close();
}
```

## 脚本

`scripts/` 目录中包含可重用的自动化脚本：
- `webp-compress.sh` —— 将图像转换为 WebP 格式
- `form-submit.js` —— 通用的表单提交模板

## 故障排除

### 按钮保持灰色/禁用状态
- 文件上传完成后等待更长时间（至少 3 秒）
- 确保文本输入能够触发事件（使用 `pressSequentially()`）
- 检查图像是否仍在上传中

### 上传超时
- 首先将图像压缩为 WebP 格式
- 如果图像文件过大，尝试减小其尺寸

### 表单无法提交
- 将 `force` 参数设置为 `true` 以强制点击按钮
- 确认按钮的选择器正确无误
- 验证所有必填字段是否都已填写