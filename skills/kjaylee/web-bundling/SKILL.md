---
name: web-bundling
description: 将 Web 应用程序打包成单个 HTML 文件以供分发。适用于创建需要作为单个文件共享的独立 HTML 游戏、成果物或演示文稿。本文介绍了使用 React + Vite + Parcel 进行打包的方法。
metadata:
  author: misskim
  version: "1.0"
  origin: Concept from Anthropic web-artifacts-builder, adapted for game distribution
---

# Web Bundling (Single HTML)

将 React/Vite 应用程序打包为单个 HTML 文件。

## 适用场景

- 需要作为 Telegram Mini App 发布的游戏  
- 需要上传到 itch.io 的 HTML5 游戏  
- 单文件演示/原型  
- 用于展示的作品集  

## 打包方式  

### 简单游戏（无框架）

如果游戏本身已经是用单个 HTML 文件编写的，那么无需进行额外打包。  
将 CSS 和 JS 代码直接内嵌到 `<style>` 和 `<script>` 标签中；  
图片则通过 base64 数据 URI 的方式嵌入到 HTML 文件中。  

### React 应用程序 → 单个 HTML 文件  

**技术栈**：React 18 + TypeScript + Vite + Parcel（打包工具）+ Tailwind CSS  

```bash
# 1. Vite로 프로젝트 빌드
npm run build

# 2. Parcel로 단일 파일 번들
npx parcel build dist/index.html --no-source-maps

# 3. html-inline으로 에셋 인라인
npx html-inline dist/index.html -o bundle.html
```  

### 内嵌资源的技巧  

```html
<!-- 이미지 → base64 -->
<img src="data:image/png;base64,iVBOR..." />

<!-- 폰트 → base64 @font-face -->
<style>
@font-face {
  font-family: 'GameFont';
  src: url(data:font/woff2;base64,...) format('woff2');
}
</style>

<!-- 오디오 → base64 (작은 효과음만) -->
<audio src="data:audio/mp3;base64,..."></audio>
```  

## 游戏发布检查清单  

- [ ] 已成功打包为单个 HTML 文件  
- [ ] 无外部 CDN 依赖（支持离线运行）  
- [ ] 支持移动设备触控（适用于 Telegram Mini App）  
- [ ] 考虑了安全区域（WebView 环境）  
- [ ] 优化文件大小（压缩图片、压缩代码）  
- [ ] 控制台中没有错误信息  

## 发布途径  

1. **Telegram Mini App**：托管在 eastsea.monster 上  
2. **itch.io**：直接上传 HTML 文件  
3. **GitHub Pages**：推送到 GitHub 仓库  
4. **CrazyGames/Poki**：根据平台要求进行发布