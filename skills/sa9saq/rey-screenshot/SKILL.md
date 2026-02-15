---
name: rey-screenshot
description: 自动截图和视觉内容捕获功能：能够自主发起截图操作，用于生成发布到社交网络（SNS）的图片内容。
---

# 截图

用于捕获网站、仪表盘和应用程序的截图，以供文档编写和发布到社交媒体（SNS）使用。

## 指令

1. **网页截图**（使用 OpenClaw 浏览器）：
   ```
   browser action:screenshot targetUrl:"https://example.com" fullPage:true type:png
   ```

2. **特定元素的截图**：
   ```
   browser action:screenshot targetUrl:"https://example.com" selector:".hero-section" type:png
   ```

3. **终端/命令行界面（CLI）截图**：
   ```bash
   # Using script + ANSI rendering
   script -q /tmp/terminal-capture.txt -c "your_command"
   # Or use carbon.now.sh for pretty code screenshots
   ```

4. **本地服务的仪表盘截图**：
   ```
   browser action:screenshot targetUrl:"http://localhost:3000" fullPage:true type:png
   ```

5. **视图窗口尺寸**（针对不同平台进行优化）：

| 平台 | 宽度 | 高度 | 画面比例 |
|----------|-------|--------|-------|
| X/Twitter | 1200 | 675 | 16:9 |
| Instagram 信息流 | 1080 | 1080 | 1:1 |
| Instagram 故事 | 1080 | 1920 | 9:16 |
| Note.com | 1280 | 720 | 16:9 |
| OGP 图片 | 1200 | 630 | 约 1.9:1 |

6. **后期处理**：
   - 根据平台尺寸裁剪图片
   - 如有需要，添加注释（文本覆盖）
   - 优化文件大小（UI 图片使用 PNG 格式，照片使用 JPEG 格式）

## 使用场景

### 产品截图
```
Capture landing page → crop hero section → use as Product Hunt image
```

### 仪表盘截图
```
Capture agent dashboard → annotate key metrics → share on X
```

### 对比前后效果
```
Screenshot buggy UI → fix → screenshot fixed UI → combine for comparison post
```

### 文档制作
```
Screenshot each step → annotate with numbers → add to README/guide
```

## 自动截图规则

### 可以自由截图的对象：
- 自己的项目（仪表盘、应用程序）
- 公共网站
- 终端输出
- 代码编辑器的界面截图

### 需要事先征得许可的情况：
- 他人的私人内容
- 用于发布到社交媒体的截图（需确认内容合适）
- 包含个人信息的截图

## 安全注意事项

- **隐藏敏感信息**：在分享前模糊或遮盖 API 密钥、密码和个人信息
- **检查终端截图中的凭据**：这些截图可能包含环境变量
- **不要截图已填写凭据的登录页面**
- **不要公开内部 URL**：避免在截图中显示本地主机地址（localhost）或 IP 地址

## 输出格式

- 将截图保存到 `/mnt/hdd/rey/images/screenshots/` 目录中，并使用时间戳作为文件名
- 文件格式：`screenshot-YYYY-MM-DD-HHMMSS.png`

## 所需工具

- OpenClaw 浏览器（用于网页截图）
- 文件系统（用于保存截图）
- 可选工具：`imagemagick`（用于图片后期处理，如 `convert`、`mogrify`）