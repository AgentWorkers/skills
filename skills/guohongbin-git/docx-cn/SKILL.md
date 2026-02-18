---
name: docx-cn
description: "**Word 文档处理**  
- **创建、读取、编辑 Word 文档**：支持创建新的 Word 文档，以及读取和编辑已存在的 Word 文档。  
- **支持 .docx 格式**：能够处理和显示 `.docx` 格式的文件。  
- **格式化功能**：提供丰富的文本格式化选项，如字体、颜色、字号等，以提升文档的外观。  
- **表格支持**：支持在文档中添加和编辑表格，支持复杂的表格格式。  
- **图片插入**：可以轻松地将图片插入到文档中，并对其进行缩放、裁剪等操作。  
**关键词**：Word、文档、docx、格式化、表格、图片。"
metadata:
  openclaw:
    emoji: 📄
    fork-of: "https://github.com/anthropics/skills"
---
# DOCX文件的创建、编辑与分析

## 概述

.docx文件是一个包含XML文件的ZIP压缩包。

## 快速参考

| 任务 | 方法 |
|------|----------|
| 读取/分析内容 | 使用`pandoc`或解压以获取原始XML |
| 创建新文档 | 使用`docx-js`（详见下文“创建新文档”部分） |
| 编辑现有文档 | 解压 → 编辑XML → 重新打包（详见下文“编辑现有文档”部分） |

### 将.doc文件转换为.docx文件

在编辑之前，必须先将旧的.doc文件转换为.docx格式：

```bash
python scripts/office/soffice.py --headless --convert-to docx document.doc
```

### 读取内容

```bash
# Text extraction with tracked changes
pandoc --track-changes=all document.docx -o output.md

# Raw XML access
python scripts/office/unpack.py document.docx unpacked/
```

### 将内容转换为图片

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
pdftoppm -jpeg -r 150 document.pdf page
```

### 接受已跟踪的更改

要生成一个包含所有已跟踪更改的干净文档（需要LibreOffice支持）：

```bash
python scripts/accept_changes.py input.docx output.docx
```

---

## 创建新文档

可以使用JavaScript生成.docx文件，然后对其进行验证。安装方法：`npm install -g docx`

### 设置
```javascript
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
        Header, Footer, AlignmentType, PageOrientation, LevelFormat, ExternalHyperlink,
        TableOfContents, HeadingLevel, BorderStyle, WidthType, ShadingType,
        VerticalAlign, PageNumber, PageBreak } = require('docx');

const doc = new Document({ sections: [{ children: [/* content */] }] });
Packer.toBuffer(doc).then(buffer => fs.writeFileSync("doc.docx", buffer));
```

### 验证
创建文件后，对其进行验证。如果验证失败，需要解压文件，修复XML内容，然后再重新打包。
```bash
python scripts/office/validate.py doc.docx
```

### 页面大小

### 常见页面尺寸（单位：DXA，1440 DXA = 1英寸）：

| 纸张类型 | 宽度 | 高度 | 内容宽度（包含边距） |
|-------|-------|--------|---------------------------|
| US Letter | 12,240 | 15,840 | 9,360 |
| A4（默认） | 11,906 | 16,838 | 9,026 |

**横向布局：**docx-js会自动调整宽度和高度；因此请提供纵向尺寸，让它自行处理布局转换：
```javascript
size: {
  width: 12240,   // Pass SHORT edge as width
  height: 15840,  // Pass LONG edge as height
  orientation: PageOrientation.LANDSCAPE  // docx-js swaps them in the XML
},
// Content width = 15840 - left margin - right margin (uses the long edge)
```

### 样式（覆盖内置标题样式）

使用Arial作为默认字体（该字体被广泛支持），并将标题颜色设置为黑色以提高可读性。
```javascript
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 12pt default
    paragraphStyles: [
      // IMPORTANT: Use exact IDs to override built-in styles
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } }, // outlineLevel required for TOC
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 180, after: 180 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun("Title")] }),
    ]
  }]
});
```

### 列表
**切勿使用Unicode项目符号**！

```javascript
// ❌ WRONG - never manually insert bullet characters
new Paragraph({ children: [new TextRun("• Item")] })  // BAD
new Paragraph({ children: [new TextRun("\u2022 Item")] })  // BAD

// ✅ CORRECT - use numbering config with LevelFormat.BULLET
const doc = new Document({
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ]
  },
  sections: [{
    children: [
      new Paragraph({ numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("Bullet item")] }),
      new Paragraph({ numbering: { reference: "numbers", level: 0 },
        children: [new TextRun("Numbered item")] }),
    ]
  }]
});

// ⚠️ Each reference creates INDEPENDENT numbering
// Same reference = continues (1,2,3 then 4,5,6)
// Different reference = restarts (1,2,3 then 1,2,3)
```

### 表格
**重要提示：表格需要设置双宽度**——必须在表格中设置`columnWidths`，同时在每个单元格中也设置`width`。如果不这样做，某些平台上的表格可能显示不正确。
```javascript
// CRITICAL: Always set table width for consistent rendering
// CRITICAL: Use ShadingType.CLEAR (not SOLID) to prevent black backgrounds
const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

new Table({
  width: { size: 9360, type: WidthType.DXA }, // Always use DXA (percentages break in Google Docs)
  columnWidths: [4680, 4680], // Must sum to table width (DXA: 1440 = 1 inch)
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders,
          width: { size: 4680, type: WidthType.DXA }, // Also set on each cell
          shading: { fill: "D5E8F0", type: ShadingType.CLEAR }, // CLEAR not SOLID
          margins: { top: 80, bottom: 80, left: 120, right: 120 }, // Cell padding (internal, not added to width)
          children: [new Paragraph({ children: [new TextRun("Cell")] })]
        })
      ]
    })
  ]
})
```

**表格宽度计算：**
始终使用`WidthType.DXA`；使用`WidthType.PERCENTAGE`在Google Docs中会导致显示问题。
```javascript
// Table width = sum of columnWidths = content width
// US Letter with 1" margins: 12240 - 2880 = 9360 DXA
width: { size: 9360, type: WidthType.DXA },
columnWidths: [7000, 2360]  // Must sum to table width
```

**宽度规则：**
- **始终使用`WidthType.DXA`**——切勿使用`WidthType.PERCENTAGE`（与Google Docs不兼容）
- 表格宽度必须等于所有`columnWidth`的总和
- 单元格的`width`必须与对应的`columnWidth`相匹配
- 单元格的`margins`是内部边距，它们会减少内容显示区域，而不是增加单元格的实际宽度
- 对于全宽表格：使用内容宽度（页面宽度减去左右边距）

### 图片
```javascript
// CRITICAL: type parameter is REQUIRED
new Paragraph({
  children: [new ImageRun({
    type: "png", // Required: png, jpg, jpeg, gif, bmp, svg
    data: fs.readFileSync("image.png"),
    transformation: { width: 200, height: 150 },
    altText: { title: "Title", description: "Desc", name: "Name" } // All three required
  })]
})
```

### 分页
```javascript
// CRITICAL: PageBreak must be inside a Paragraph
new Paragraph({ children: [new PageBreak()] })

// Or use pageBreakBefore
new Paragraph({ pageBreakBefore: true, children: [new TextRun("New page")] })
```

### 目录
```javascript
// CRITICAL: Headings must use HeadingLevel ONLY - no custom styles
new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" })
```

### 页眉/页脚
```javascript
sections: [{
  properties: {
    page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } // 1440 = 1 inch
  },
  headers: {
    default: new Header({ children: [new Paragraph({ children: [new TextRun("Header")] })] })
  },
  footers: {
    default: new Footer({ children: [new Paragraph({
      children: [new TextRun("Page "), new TextRun({ children: [PageNumber.CURRENT] })]
    })] })
  },
  children: [/* content */]
}]
```

### docx-js的关键使用规则

- **明确指定页面大小**——docx-js默认使用A4格式；对于美国文档，请使用US Letter（12240 x 15840 DXA）
- **横向布局：**提供纵向尺寸——docx-js会自动调整宽度和高度；将较短边作为`width`，较长边作为`height`，并设置`orientation: PageOrientation.LANDSCAPE`
- **切勿使用`\n`**——请使用独立的`Paragraph`元素来分隔内容
- **切勿使用Unicode项目符号**——请使用`LevelFormat.BULLET`并配置编号格式
- **分页指令必须放在`Paragraph`元素中**——单独的分页指令会导致XML格式错误
- **插入图片时需要指定图片格式**——必须指定图片格式（如png/jpg等）
- **始终使用DXA单位设置表格宽度**——切勿使用`WidthType.PERCENTAGE`（在Google Docs中会导致显示问题）
- **表格需要设置双宽度**——`columnWidths`数组和单元格`width`都必须正确设置
- **表格宽度应等于所有`columnWidth`的总和**——确保数值准确无误
- **始终为单元格添加边距**——使用`margins: { top: 80, bottom: 80, left: 120, right: 120 }`以确保良好的显示效果
- **表格阴影效果请使用`ShadingType.CLEAR`**——切勿使用`SOLID`阴影样式
- **目录生成需要`HeadingLevel`信息**——标题段落不能使用自定义样式
- **覆盖内置样式**——请使用正确的ID（如“Heading1”、“Heading2”等）

---

## 编辑现有文档

**请按以下三个步骤操作：**

### 第一步：解压文件
```bash
python scripts/office/unpack.py document.docx unpacked/
```
解压文件，将XML内容提取出来，合并相邻的文本片段，并将智能引号（如`&#x201C;`等）转换为XML实体，以便在编辑过程中保持格式不变。可以使用`--merge-runs false`选项跳过片段合并步骤。

### 第二步：编辑XML
在解压后的文件中直接编辑XML内容。具体格式规范请参考XML参考文档。

**对于已跟踪的更改和注释，请使用“Claude”作为作者名称**，除非用户另有要求。

**建议直接使用编辑工具进行字符串替换，不要编写Python脚本**。脚本可能会增加不必要的复杂性。编辑工具会明确显示替换的内容。

**重要提示：**新添加的文本请使用智能引号。当添加包含引号的文本时，请使用XML实体来表示这些引号：
```xml
<!-- Use these entities for professional typography -->
<w:t>Here&#x2019;s a quote: &#x201C;Hello&#x201D;</w:t>
```
| 实体 | 对应的字符 |
|--------|-----------|
| `&#x2018;` | ‘（左单引号） |
| `&#x2019;` | ’（右单引号） |
| `&#x201C;` | “（左双引号） |
| `&#x201D;` | ”（右双引号） |

**添加注释**：可以使用`comment.py`脚本在多个XML文件中统一处理注释格式（注释内容需要预先进行XML转义）：
```bash
python scripts/comment.py unpacked/ 0 "Comment text with &amp; and &#x2019;"
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0  # reply to comment 0
python scripts/comment.py unpacked/ 0 "Text" --author "Custom Author"  # custom author name
```
之后在`document.xml`文件中添加相应的标记（具体方法请参考XML参考文档）。

### 第三步：重新打包文件
```bash
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```
使用`--validate false`选项跳过验证步骤，然后对XML内容进行自动修复和压缩，最后生成新的.docx文件。

**自动修复功能可以修复以下问题：**
- `durableId`大于或等于`0x7FFFFFFF`（生成有效的唯一ID）
- `<w:t>`元素中缺少`xml:space="preserve"`属性（用于保留空白字符）

**自动修复无法修复的问题：**
- XML格式错误、元素嵌套不正确、关系缺失或违反XML规范

### 常见错误：
- **替换整个`<w:r>`元素**：在添加已跟踪的更改时，应将整个`<w:r>...</w:r>`块替换为`<w:del>...<w:ins>...`的形式。切勿将更改标记直接插入到文本片段中。
- **保留`<w:rPr>`元素的格式**：将原始文本片段的`<w:rPr>`格式复制到对应的更改片段中，以保持粗体、字体大小等格式设置。

---

## XML参考文档

### XML结构规范

- `<w:pPr>`元素中的元素顺序：`<w:pStyle>`、`<w:numPr>`、`<w:spacing>`、`<w:ind>`、`<w:jc>`、最后是`<w:rPr>`
- 对于`<w:t>`元素，需要添加`xml:space="preserve"`属性以保留前后的空白字符
- RSID（引用ID）必须是8位十六进制数（例如`00AB1234`）

### 已跟踪的更改

- **插入内容**：
```xml
<w:ins w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>inserted text</w:t></w:r>
</w:ins>
```

- **删除内容**：
```xml
<w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>deleted text</w:delText></w:r>
</w:del>
```

- 在`<w:del>`元素内部：使用`<w:delText>`代替`<w:t>`，使用`<w:delInstrText>`代替`<w:instrText>`。
- **仅标记实际发生更改的部分**：在编辑时只需标记真正发生变化的部分。
- **删除整个段落或列表项**：在删除段落的所有内容时，也要同时标记该段落的结束标记，以便将其与下一段落合并。在`<w:pPr><w:rPr>`内部添加`<w:del/>`：
```xml
<w:p>
  <w:pPr>
    <w:numPr>...</w:numPr>  <!-- list numbering if present -->
    <w:rPr>
      <w:del w:id="1" w:author="Claude" w:date="2025-01-01T00:00:00Z"/>
    </w:rPr>
  </w:pPr>
  <w:del w:id="2" w:author="Claude" w:date="2025-01-01T00:00:00Z">
    <w:r><w:delText>Entire paragraph content being deleted...</w:delText></w:r>
  </w:del>
</w:p>
```
如果没有`<w:del/>`，在应用更改后该段落或列表项可能会显示为空。
- **处理其他作者的插入操作**：在删除操作中应包含对原插入内容的引用。
- **恢复其他作者的删除操作**：在删除操作后应添加相应的插入内容。

### 注释处理
运行`comment.py`脚本后（参见第二步），需要在`document.xml`文件中添加注释标记。对于回复性注释，请使用`--parent`参数，并将注释标记嵌套在父注释元素内部。

**重要提示：**`<w:commentRangeStart>`和`<w:commentRangeEnd>`元素是`<w:r>`的子元素，不能直接放在`<w:r>`内部。**

### 图片处理
1. 将图片文件放入`word/media/`目录中。
2. 在`word/_rels/document.xml.rels`文件中添加图片的引用关系。
3. 在`[Content_Types].xml`文件中配置图片的类型信息。
4. 在`document.xml`文件中引用这些图片资源。

---

## 所需依赖库

- **pandoc**：用于文本提取
- **docx**：用于创建新文档（通过`npm install -g docx`安装）
- **LibreOffice**：用于PDF转换（在沙箱环境中会自动配置相关工具，详见`scripts/office/soffice.py`）
- **Poppler**：用于处理图片文件（通过`pdftoppm`工具实现）