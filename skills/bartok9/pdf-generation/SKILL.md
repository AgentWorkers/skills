# PDF生成技巧

**目的：** 从HTML/CSS生成专业的PDF文件，确保页面中没有空白间隙或布局问题。

## 问题

在将HTML转换为PDF时，`page-break-inside: avoid`属性会导致“孤立空白”现象——即无法容纳在当前页面上的内容会被完全移到下一页，从而产生较大的空白区域。

## 解决方案

### 1. 使用基于流的布局（而非固定页面容器）

**❌ 错误做法：**
```html
<div class="page" style="min-height: 297mm;">
  <!-- Content -->
</div>
```

**✅ 正确做法：**
```html
<body>
  <!-- Content flows naturally -->
</body>
```

应使用`@page` CSS规则来控制页面布局，而不是使用固定大小的页面容器：
```css
@page {
    size: A4;
    margin: 18mm 15mm;
}
```

### 2. 仅保护小型元素

仅在以下元素上使用`break-inside: avoid`属性：
- **较小的元素**（如卡片、单行内容、短文本框）
- 如果被拆分后会显得不美观的元素

**需要保护的元素包括：**
- 单个表格行（`tr`）
- 高度小于100px的卡片
- 时间轴项目
- 步骤项
- 强调框（highlight boxes）

**不需要保护的元素包括：**
- 整个表格
- 大型容器
- 整个页面内容
- 多列布局
- 文档末尾的引用框

### 3. 结合使用现代和传统的CSS属性

```css
.small-element {
    break-inside: avoid;        /* Modern spec */
    page-break-inside: avoid;   /* Legacy support */
}
```

### 4. 保持页眉与内容的紧密关联

```css
h2, h3, h4, .section-header {
    break-after: avoid;
    page-break-after: avoid;
}
```

### 5. 防止出现孤立行

```css
body {
    orphans: 3;  /* Min lines at bottom of page */
    widows: 3;   /* Min lines at top of page */
}
```

### 6. 允许表格拆分（但保持行之间的连续性）

```css
table {
    /* NO break-inside: avoid */
}

tr {
    break-inside: avoid;
    page-break-inside: avoid;
}
```

## 模板

```css
@page {
    size: A4;
    margin: 18mm 15mm;
}

body {
    font-size: 10pt;
    line-height: 1.5;
    orphans: 3;
    widows: 3;
}

/* Headers stay with content */
h2, h3, h4 {
    break-after: avoid;
    page-break-after: avoid;
}

/* Small elements don't break */
.card, .highlight-box, .step, .timeline-item {
    break-inside: avoid;
    page-break-inside: avoid;
}

/* Table rows stay together, table can break */
tr {
    break-inside: avoid;
    page-break-inside: avoid;
}

/* Large containers flow naturally */
table, .section, .two-col {
    /* NO break-inside: avoid */
}

@media print {
    body { 
        -webkit-print-color-adjust: exact; 
        print-color-adjust: exact; 
    }
}
```

## 工具

| 工具 | 适用场景 | 安装方式 |
|------|----------|---------|
| **WeasyPrint** | 将HTML/CSS转换为PDF（支持最新的CSS格式） | `brew install weasyprint` 或 `pip install weasyprint` |
| **Pandoc** | 通过LaTeX将Markdown转换为PDF | `brew install pandoc` |
| **wkhtmltopdf** | 适用于复杂布局的转换工具 | 从wkhtmltopdf.org下载 |
| **Puppeteer** | 用于处理JavaScript渲染的内容 | `npm install puppeteer` |

### WeasyPrint的使用命令
```bash
weasyprint input.html output.pdf
```

## 使用前的检查清单

在发送PDF文件之前，请务必完成以下检查：
- [ ] 在PDF阅读器中浏览所有页面，检查是否存在空白间隙
- [ ] 确保页面顶部没有单独的空白行
- [ ] 验证表格中的行是否被错误地拆分
- [ ] 确认页眉后面紧跟着内容（而不是单独位于页面底部）

## 常见错误及解决方法

| 错误 | 解决方法 |
|---------|-----|
| 在大型容器上使用`page-break-inside: avoid` | 应移除该属性，让内容自然流动 |
| 使用固定高度的页面容器 | 应改用`@page` CSS规则 |
| 文档末尾的引用框设置了拆分保护 | 应移除拆分保护设置 |
| 整个表格都被设置为不可拆分 | 只需要保护表格中的行（`tr`），而不是整个表格 |
| 未设置`orphans`和`widows`属性 | 应添加`orphans: 3; widows: 3;`属性 |

## 参考资源

- WeasyPrint文档：https://doc.courtbouillon.org/weasyprint/
- CSS页面布局相关规范：https://www.w3.org/TR/css-page-3/
- CSS打印指南：https://www.smashingmagazine.com/2018/05/print-stylesheets-in-2018/

---

*本技能由Bartok创建于2026年3月6日*