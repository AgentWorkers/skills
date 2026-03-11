---
name: html-coder
description: '具备高级的HTML开发技能，能够构建网页、表单以及交互式内容。适用于创建HTML文档、组织网页内容、实现语义化标记、添加表单和媒体元素、使用HTML5 API，以及需要HTML模板、最佳实践和可访问性指导的场景。支持现代的HTML5标准及响应式设计模式。'
collaborators:
  - make-skill-template
  - finalize-agent-prompt
---
# HTML编码技能

这是一项专注于专业HTML开发的专家级技能，强调语义标记、可访问性、HTML5特性以及符合标准的网页内容。

## 适用场景

- 创建具有语义结构的HTML文档  
- 使用HTML5验证功能构建可访问的表单  
- 实现响应式布局和多媒体内容  
- 使用HTML5 API（如Canvas、SVG、Web存储、地理定位）  
- 解决验证或可访问性问题  

## 核心能力  

- **语义HTML**：文档结构、内容分区、以可访问性为导向的标记方式  
- **表单**：所有输入类型、验证属性、字段集、标签  
- **多媒体**：响应式图片、音频/视频、Canvas、SVG  
- **HTML5 API**：Web存储、地理定位、拖放、Web Workers  
- **可访问性**：ARIA规范、屏幕阅读器支持、WCAG合规性  

## 必备参考资料  

- HTML专家的核心文档：  
  - [`references/add-css-style.md`](references/add-css-style.md)：通过`link`标签、内联方式或嵌入HTML添加CSS  
  - [`references/add-javascript.md`](references/add-javascript.md)：通过`script src="link.js"`标签、内联`script`或嵌入HTML添加JavaScript  
  - [`references/attributes.md`](references/attributes.md)：HTML属性的基本知识  
  - [`references/essentials.md`](references/essentials.md)：语义标记、验证、响应式设计技术  
  - [`references/global-attributes.md`](references/global-attributes.md)：完整的全局属性信息  
  - [`references/glossary.md`](references/glossary.md)：完整的HTML元素和属性参考  
  - [`references/standards.md`](references/standards.md)：HTML5规范和标准  

## 最佳实践  

- **语义HTML**：使用能够表达意义的元素（如`<article>`、`<nav>`、`<header>`、`<section>`、`<footer>`，而非简单的`<div>`组合。  
- **以可访问性为先**：正确的标题层次结构、为输入元素添加`alt`文本、使用标签进行说明、支持键盘导航（必要时使用ARIA）。  
- **HTML5验证**：在使用JavaScript之前，优先利用内置的验证机制（如`required`、`pattern`、`type="email"`）。  
- **响应式图片**：使用`<picture>`元素、`srcset`属性以及`loading="lazy"`来优化图片加载性能。  
- **性能优化**：减少DOM层级深度、优化图片大小、延迟加载非关键脚本、使用语义化元素。  

## 快速模板示例  

- **语义页面结构**  
  ```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Page Title</title>
</head>
<body>
  <header><nav><!-- Navigation --></nav></header>
  <main><article><!-- Content --></article></main>
  <aside><!-- Sidebar --></aside>
  <footer><!-- Footer --></footer>
</body>
</html>
```  

- **可访问表单**  
  ```html
<form method="post" action="/submit">
  <fieldset>
    <legend>Contact</legend>
    <label for="email">Email:</label>
    <input type="email" id="email" name="email" required
           pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$">
    <button type="submit">Send</button>
  </fieldset>
</form>
```  

- **响应式图片**  
  ```html
<picture>
  <source media="(min-width: 1200px)" srcset="large.webp">
  <source media="(min-width: 768px)" srcset="medium.webp">
  <img src="small.jpg" alt="Description" loading="lazy">
</picture>
```  

## 故障排除方法  

- **验证问题**：使用W3C验证工具（validator.w3.org）检查未闭合的标签和嵌套结构。  
- **可访问性问题**：通过Lighthouse工具进行审计、使用屏幕阅读器进行测试、确保键盘导航功能正常、检查颜色对比度。  
- **兼容性检查**：使用CanIUse网站（caniuse.com）检测浏览器兼容性，并为不支持的特性提供备用方案。  

## 关键标准  

- **WHATWG HTML活标准**：https://html.spec.whatwg.org/  
- **WCAG可访问性规范**：https://www.w3.org/WAI/WCAG21/quickref/  
- **MDN Web文档**：https://developer.mozilla.org/en-US/docs/Web/HTML