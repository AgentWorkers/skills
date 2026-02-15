---
name: pptx-pdf-font-fix
description: 通过修改 PPTX 文件中的文本透明度来解决 PowerPoint 在导出为 PDF 时出现的字体嵌入问题。当用户拥有一个 PPTX 文件，且导出的 PDF 文件显示的字体是错误的或默认字体（而非用户下载或自定义的字体）时，可以使用此方法。该方法通过为完全不透明的文本应用极小的透明度（1%）来强制 PowerPoint 在导出 PDF 时正确嵌入字体。
---

# PPT字体修复

## 问题

PowerPoint的“导出为PDF”功能有时无法正确嵌入用户下载或自定义的字体，而是会使用内置的默认字体，即使满足以下条件：
- 字体已正确安装且支持嵌入
- 在PowerPoint的设置中勾选了“在文件中嵌入字体”选项

## 解决方法

通过将文本的透明度设置为1%，可以强制PowerPoint在PDF输出中正确嵌入字体。虽然这种改变在视觉上几乎不可察觉，但它会改变PowerPoint在导出过程中的字体处理方式。

## 使用方法

```bash
python3 scripts/fix_font_transparency.py input.pptx [output.pptx] [--transparency 1]
```

### 参数

- `output` -- 输出PPTX文件的路径（默认值：`input_fixed.pptx`）
- `--transparency, -t` -- 要应用的透明度百分比（默认值：1%）

## 行为特点

- 仅修改完全不透明的文本（透明度为0%的文本）
- 不会影响已经具有透明度的文本
- 可多次安全运行该脚本
- 仅修改幻灯片的XML结构（`ppt/slides/slideN.xml`），不会影响布局或母版文件

## 工作流程

1. 从用户手中接收PPTX文件
2. 运行修复脚本：`python3 scripts/fix_font_transparency.py input.pptx`
3. 将修复后的PPTX文件返回给用户
4. 用户在PowerPoint中打开修复后的文件并导出为PDF——此时字体将能够正确嵌入

## 注意事项

PDF导出必须在PowerPoint桌面应用程序中进行。服务器端的转换工具（如LibreOffice、Graph API）无法实现相同的字体嵌入效果。