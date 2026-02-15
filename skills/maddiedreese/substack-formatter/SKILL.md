---
name: substack-formatter
description: 将纯文本转换为具有适当HTML格式的Substack文章格式，以便可以直接复制并粘贴到Substack编辑器中。
---

# Substack 文章格式化工具

## 概述  
该工具可将纯文本转换为符合 Substack 格式的专业内容，确保在粘贴到 Substack 编辑器后，粗体、斜体以及标题等格式能够正确显示。

## 该工具的功能  
- ✅ **为 Substack 格式化文本**，保持适当的段落结构和间距  
- ✅ **将文本转换为 Substack 编辑器能够识别的 HTML 格式**  
- ✅ **保留您的原始内容**（仅改变视觉呈现方式）  
- ✅ **支持复制粘贴**，确保粗体、斜体、标题等格式能够完整保留  

## 技术原理  
**问题：** Substack 编辑器将原始 Markdown 文本视为普通文本处理。  
**解决方案：** 将文本转换为 HTML 格式，然后以 `text/html` 格式进行复制。  

## 使用方法  

### 基本格式化  
```
Format this for Substack:
[Your plain text content here]
```  

### 最小化格式化  
```
Format for Substack (minimal):
[Your plain text content here]
```  

## 格式化选项  

### **标准格式**  
- 正确的段落结构  
- 清晰的 HTML 输出  
- 保留内容，提升可读性  

### **最小化格式**  
- 仅优化文本间距  
- 不改变任何格式效果  
- 完整保留原始内容  

## 格式化特性  

### **结构**  
- **清晰的段落**，便于阅读  
- **合理的段落间距**  
- 明确的视觉层次结构  

### **HTML 输出**  
- **粗体文本**：使用 `<strong>` 标签  
- **强调内容**：使用 `<em>` 标签  
- **标题**：使用 `<h2>`、`<h3>` 标签  
- **列表**：使用 `<ul><li>`（无序列表）和 `<ol><li>`（有序列表）  
- **段落**：使用正确的 `<p>` 标签结构  

## 复制粘贴流程  
1. **运行格式化工具**，获取 HTML 输出结果  
2. **使用提供的复制脚本**，将 HTML 内容以 `text/html` 格式复制  
3. **粘贴到 Substack**，格式会自动保留  
4. **无需手动调整**，粗体、斜体、标题等格式均会自动生效  

## 示例  

### 输入（纯文本）：  
```
I used to think being productive meant doing more things. Last week I tried something different. I did fewer things but focused completely on each one. The result was surprising. I got more done in less time and felt less stressed. Sometimes the answer isn't addition, it's subtraction.
```  

### 输出（格式化后的 Substack 内容）：  
```html
<p><strong>I used to think being productive meant doing more things.</strong></p>

<p>Last week I tried something different:</p>

<p>I did fewer things.<br>
But focused completely on each one.</p>

<p>The result was surprising.</p>

<p><em>I got more done in less time and felt less stressed.</em></p>

<p><strong>Sometimes the answer isn't addition, it's subtraction.</strong></p>

<p>What's one thing you could subtract from your routine?</p>
```  

## 随附工具  
- **`formatter.py`**：主要格式化脚本  
- **`copy_to_substack.py`**：将格式化后的文本转换为 HTML 并正确复制到 Substack  
- **`test_formatter.py`**：用于测试的工具脚本  
- **针对不同结构类型的示例和模板**  

## 设计理念  
**注重可读性，同时保留您的写作风格。** 该工具在改善视觉呈现的同时，确保您的信息能够清晰、准确地传达。