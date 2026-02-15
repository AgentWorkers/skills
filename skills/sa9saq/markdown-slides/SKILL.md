---
description: 将 Markdown 文件转换为具有键盘导航功能的自包含 HTML 幻灯片演示文稿。
---

# Markdown 幻灯片生成工具

该工具可将 Markdown 内容转换为独立的 HTML 幻灯片集，无需任何外部依赖，支持离线使用。

**适用场景**：  
- 从 Markdown 文件创建演示文稿  
- 快速制作幻灯片  
- 展示型演示文稿  

## 使用要求  
- 无需任何外部工具、构建步骤或 API 密钥  
- 输出格式为单个 HTML 文件，可在任何浏览器中正常显示  

## 使用方法  
1. **解析输入内容**：  
   使用 `---`（水平线）将 Markdown 内容分割成多个独立的幻灯片。  

2. **将 Markdown 转换为 HTML**：  
   - `# 标题` → `<h1>`（标题幻灯片）  
   - `## 标题` → `<h2>`（子标题）  
   - `- 列项` → `<ul><li>`（项目列表）  
   - `**粗体**` → `<strong>`  
   - `*斜体*` → `<em>`  
   - ``` `代码` `` → `<code>`  
   - `![图片链接](图片路径)` → `<img>`  
   - 段落 → `<p>`  

3. **将生成的 HTML 内容嵌入到包含 CSS 和 JavaScript 的模板中**：  
   （具体模板代码见下方示例）  

4. **保存结果**：  
   保存为 `slides.html` 文件（或用户指定的路径）。  

5. **使用说明**：  
   在浏览器中打开文件，使用 ←/→ 方向键或点击按钮进行导航，按 F11 键可全屏显示。  

## 自定义选项  
| 选项        | 默认值       | 可选值          |
|------------|------------|-------------------|
| 主题颜色     | #1a1a2e      | #fff (Light) 或 #fff (Solarized)   |
| 字体类型     | 系统默认字体   | Monospace 或 Serif 字体     |
| 强调颜色     | #667eea      | 任意十六进制颜色       |
| 屏幕比例     | 16:9        | 可设置自定义比例       |

## 注意事项  
- 如果没有 `---` 分隔符，每个 `# 标题` 都会被视为一个独立的幻灯片。  
- 如果幻灯片内容过长，可能会超出屏幕显示范围，建议拆分成多个幻灯片。  
- 图片必须为 URL 或 Base64 编码的形式；本地文件路径在独立 HTML 文件中无法使用。  
- 对于包含大量代码的幻灯片，可适当减小 `<pre>` 标签内的字体大小。  
- 可在幻灯片中添加 `<!-- notes: ... -->` 注释（这些注释对用户不可见）。  

### 示例代码（````html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PRESENTATION_TITLE</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; }
  .slide { width: 100vw; height: 100vh; display: none; flex-direction: column; justify-content: center; align-items: center; padding: 8vh 10vw; text-align: center; }
  .slide.active { display: flex; }
  .slide h1 { font-size: 3.5rem; margin-bottom: 1rem; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .slide h2 { font-size: 2.5rem; margin-bottom: 1rem; color: #667eea; }
  .slide p { font-size: 1.5rem; line-height: 1.8; max-width: 800px; color: #ccc; }
  .slide ul, .slide ol { font-size: 1.4rem; text-align: left; line-height: 2; }
  .slide code { background: #16213e; padding: 2px 8px; border-radius: 4px; font-size: 1.2rem; }
  .slide pre { background: #16213e; padding: 1.5rem; border-radius: 8px; text-align: left; overflow-x: auto; max-width: 90%; }
  .slide pre code { background: none; padding: 0; }
  .slide img { max-width: 70%; max-height: 60vh; border-radius: 8px; }
  .progress { position: fixed; bottom: 0; left: 0; height: 4px; background: #667eea; transition: width 0.3s; z-index: 10; }
  .slide-num { position: fixed; bottom: 12px; right: 20px; font-size: 0.9rem; color: #555; }
</style>
</head>
<body>
<!-- SLIDES_HERE: <div class="slide">content</div> per slide -->
<div class="progress" id="progress"></div>
<div class="slide-num" id="slideNum"></div>
<script>
let current = 0;
const slides = document.querySelectorAll('.slide');
function show(n) {
  current = Math.max(0, Math.min(n, slides.length - 1));
  slides.forEach(s => s.classList.remove('active'));
  slides[current].classList.add('active');
  document.getElementById('progress').style.width = ((current + 1) / slides.length * 100) + '%';
  document.getElementById('slideNum').textContent = (current + 1) + ' / ' + slides.length;
}
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === ' ') show(current + 1);
  if (e.key === 'ArrowLeft') show(current - 1);
  if (e.key === 'Home') show(0);
  if (e.key === 'End') show(slides.length - 1);
});
document.addEventListener('click', e => {
  if (e.clientX > window.innerWidth / 2) show(current + 1);
  else show(current - 1);
});
show(0);
</script>
</body>
</html>
````）  
（此处应插入实际的 HTML 模板代码，用于将 Markdown 转换为幻灯片的结构。）