---
name: chatgpt-image-generation
description: >
  使用 Playwright 自动化工具从 chatgpt.com 生成并下载图片：  
  1. 在新窗口中打开 chatgpt.com；  
  2. 输入所需的提示或指令；  
  3. 等待图像生成完成（系统会给出相应的提示）；  
  4. 通过鼠标悬停并点击“下载”按钮来下载生成的图片；  
  5. 下载完成后，可以选择继续执行下一个任务或停止程序。
---
# ChatGPT 图像生成技能

使用 Playwright 自动化 ChatGPT 的网页界面，实现免费的图像生成功能（无需支付 API 费用）。

## 先决条件

```bash
# Install Playwright
npm install playwright

# Install Chromium browser
npx playwright install chromium
```

## 使用方法

```bash
# Generate images from prompts file
node skills/chatgpt-image-generation/scripts/generate.js --prompts prompts.json --output ./images

# Resume from a specific index
node skills/chatgpt-image-generation/scripts/generate.js --prompts prompts.json --output ./images --start 5

# Use a specific Chrome profile
node skills/chatgpt-image-generation/scripts/generate.js --prompts prompts.json --output ./images --profile "~/Library/Application Support/Google/Chrome/YourProfile"

# Run in headless mode (no browser window)
node skills/chatgpt-image-generation/scripts/generate.js --prompts prompts.json --output ./images --headless
```

## 提示文件格式

```json
["prompt 1", "prompt 2"]
```

或

```json
{ "prompts": ["prompt 1", "prompt 2"] }
```

## 完成检测机制

该检测机制会检查以下所有条件（必须全部满足）：

1. **发送按钮已重新启用** — `button[dataTestId="send-button"]` 不再处于禁用状态
2. **图像已生成** — 存在 `img[alt="Generated image"]`，且 `naturalWidth >= 1024` 且 `naturalHeight >= 1024`
3. **下载按钮可见** — 鼠标悬停时下载按钮会显示并处于可用状态
4. **图像的源地址稳定** — 在连续两次检查中检测到相同的源地址（确保图像生成已完成）
5. **无进度条** — 不存在可见的 `[role="progressbar"]` 或进度条元素

这种多信号检测机制可以防止以下情况：
- 在图像生成完成之前尝试下载
- 下载占位图或缩略图
- 下载按钮缺失
- 在图像生成过程中尝试下载

## 下载方法

1. 将鼠标悬停在生成的图像上，以显示下载按钮
2. 点击下载按钮（使用 Playwright 的 `expect_download()` 方法）
3. 直接将图像保存到编号后的输出文件夹中

## 输出结果

- 编号后的图像文件：`001.png`、`002.png` 等
- `results.jsonl` — 每个提示对应的成功/失败日志

## 登录（仅一次）

如果未登录：
1. 运行脚本一次（脚本会打开浏览器）
2. 登录 ChatGPT
3. 会话信息会保留下来，便于后续使用（使用持久化的用户配置文件）

## 平台支持

- **macOS**：`~/Library/Application Support/Google/Chrome/`
- **Windows**：`%LOCALAPPDATA%\Google\Chrome\User Data\`
- **Linux**：`~/.config/google-ch script autorome/`

该脚本会自动检测您的操作系统，并使用相应的默认配置文件路径。

---

## 💡 可选增强功能

### 使用专用 Chrome 配置文件

**优势：** 将图像生成会话与日常的 Chrome 浏览分开，保持环境的整洁性。

**操作方法：** 通过 `--profile` 参数指定自定义配置文件路径：
```bash
--profile ~/Library/Application\ Support/Google/Chrome/ImageGenProfile
```

首先在 Chrome 中创建一个新的配置文件，然后使用该路径。

### 将生成的图像整理到 ChatGPT 项目中

**优势：** 将所有自动生成的图像整理到一个项目中，便于日后查找和查看。

**操作方法：** 修改脚本以添加项目选择功能（可参考 [免费图像生成技能](/skills/free-image-generation) 的实现方式）。免费图像生成技能默认支持此功能。

---

## 与免费图像生成技能的区别

- **本技能：**
  - ✅ 打开一个新的聊天窗口（不支持项目选择）
  - ✅ 使用默认的 Chrome 配置文件（可通过 `--profile` 参数指定自定义配置文件）

- **[免费图像生成技能](/skills/free-image-generation)：**
  - ✅ 自动选择“自动图像生成”项目
  - ✅ 默认使用专用的 ImageGenProfile 配置文件