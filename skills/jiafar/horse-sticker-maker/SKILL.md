---
name: horse-sticker-maker
description: 创建并部署一个用于制作中国新年（2026年马年）主题动画GIF贴纸的Web应用程序。用户可以使用该应用程序生成自定义的马年主题祝福贴纸，或者部署一个H5版本的贴纸生成器页面，还可以制作与微信兼容的动画GIF贴纸（背景为红色，马匹以金色动画形式奔跑）。该应用程序支持自定义文本输入功能，提供6帧组成的金色马匹奔跑动画效果，并利用gif.js库在客户端进行基于Canvas的GIF渲染。最终生成的贴纸可以通过Vercel技术进行部署。
---
# 马年贴纸制作工具

这是一个用于生成中国新年（2026年马年）定制动画GIF贴纸的Web应用程序。

## 功能介绍

- 用户可以输入1-8个字符的祝福语。
- 客户端使用Canvas绘制一个240像素的动画GIF：
  - 红色渐变背景，带有金色闪光粒子效果。
  - 6帧金色马匹奔跑的动画（使用透明PNG图片）。
  - 用户输入的祝福语以金色书法形式显示在顶部。
  - 底部显示“立马加薪”文字，该文字会循环变换颜色。
- 生成的贴纸符合微信使用规范（文件大小≤500KB，尺寸为240像素）。

## 快速入门

1. 复制模板项目：
   ```bash
   cp -r <skill_dir>/assets/horse-blessing-template ./horse-blessing
   cd horse-blessing
   npm install
   ```

2. 在本地运行项目：
   ```bash
   npm run dev
   # Open http://localhost:3000/sticker
   ```

3. 部署到Vercel服务器：
   ```bash
   vercel --prod --yes
   ```

## 项目结构

```
horse-blessing/
├── app/
│   ├── page.tsx          # Main page (AI-generated blessing with poem)
│   ├── sticker/page.tsx  # Sticker maker (Canvas GIF generator)
│   ├── api/generate/     # AI poem + image generation API
│   ├── api/sticker/      # Sticker API
│   └── layout.tsx        # Root layout (red theme)
├── public/
│   ├── horse-frame-[1-6].png  # 6-frame transparent gold horse
│   ├── horse-transparent.png  # Static horse fallback
│   └── gif.worker.js          # gif.js web worker
├── package.json
└── tailwind.config.ts
```

## 关键技术细节

### GIF生成（客户端）

- 使用通过CDN加载的`gif.js`库（来自`next/script`文件）。
- 动画包含18帧（6帧马匹图像×3个循环），每帧的延迟时间为85毫秒。
- Canvas尺寸设置为240×240像素，以符合微信贴纸的显示要求。
- 马匹图像以`Image`元素的形式加载，并通过`drawImage`方法绘制。

### 马匹图像资源

- 6张透明PNG图片存储在`public/horse-frame-[1-6].png`文件夹中。
- 这些图片是通过AI图像模型生成的，背景部分已使用`sharp`工具去除。
- 去除背景的方法是：将R、G、B颜色值大于210的像素设置为透明（即alpha值为0）。

### 自定义选项

- **底部文字**：在`sticker/page.tsx`文件中修改“立马加薪”这一文字内容。
- **GIF尺寸**：修改`const size = 240`的值（确保不超过240像素以符合微信要求）。
- **帧数**：修改`const frames = 18`的值。
- **马匹图像**：可以替换`public/horse-frame-*.png`中的图片文件。
- **背景颜色**：可以调整径向渐变的颜色。
- **闪光效果**：调整闪光粒子的数量（默认为30个）。

### 微信贴纸兼容性

- 文件大小上限为500KB。
- 建议使用240像素的尺寸。
- 必须使用GIF格式。
- 用户可以将生成的贴纸保存到微信聊天界面，然后通过表情符号面板选择并使用。

## 项目依赖项

```json
{
  "next": "^14.0.0",
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "sharp": "latest",
  "gif-encoder-2": "^1.0.5",
  "html2canvas-pro": "^1.6.7"
}
```

外部CDN依赖：`gif.js@0.2.0`（在运行时加载，用于客户端GIF编码）