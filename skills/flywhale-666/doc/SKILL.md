---
name: "doc"
description: "**使用场景：**  
当任务涉及读取、创建或编辑 `.docx` 文档时，尤其是当文档的格式或布局精度要求较高时，建议使用 `python-docx` 库以及随附的 `scripts/render_docx.py` 脚本来进行视觉检查（即查看文档的显示效果是否符合预期）。"
---

# DOCX 文档处理技能

## 使用场景
- 在需要关注文档布局的情况下（如表格、图表、分页等），阅读或审阅 DOCX 文件。
- 创建或编辑具有专业格式的 DOCX 文件。
- 在交付前验证文档的视觉布局是否正确。

## 工作流程
1. 首先进行视觉审阅（检查文档的布局、表格和图表）：
   - 如果系统安装了 `soffice` 和 `pdftoppm`，可以将 DOCX 文件转换为 PDF，然后再转换为 PNG 图片。
   - 或者使用 `scripts/render_docx.py` 脚本（该脚本依赖于 `pdf2image` 和 Poppler 工具）。
   - 如果这些工具缺失，请安装它们，或者让用户在当地查看渲染后的页面。
2. 使用 `python-docx` 对文档进行编辑和结构化处理（如添加标题、设置样式、创建表格和列表）。
3. 每进行一次有意义的修改后，重新渲染文档并检查页面效果。
4. 如果无法进行视觉审阅，可以使用 `python-docx` 提取文档内容，并指出潜在的布局问题。
5. 保持中间文件的整洁有序；在最终获得批准后及时清理这些临时文件。

## 文件命名和存储规则
- 使用 `tmp/docs/` 目录存放临时文件；完成处理后及时删除这些文件。
- 在本仓库中，将最终生成的文档保存在 `output/doc/` 目录下。
- 文件名应具有描述性，以便于识别。

## 依赖项（如缺少请安装）
建议使用 `uv` 工具来管理项目依赖关系。

### 需要安装的 Python 包：
```
uv pip install python-docx pdf2image
```

### 如果 `uv` 无法使用：
```
python3 -m pip install python-docx pdf2image
```

### 用于渲染的系统工具：
```
# macOS (Homebrew)
brew install libreoffice poppler

# Ubuntu/Debian
sudo apt-get install -y libreoffice poppler-utils
```

### 如果在当前环境中无法安装某些依赖项，请告知用户具体是哪个依赖项缺失，以及如何在当地安装它。

## 环境要求
无需特殊的环境变量。

## 文档渲染命令
- 将 DOCX 文件转换为 PDF：```
soffice -env:UserInstallation=file:///tmp/lo_profile_$$ --headless --convert-to pdf --outdir $OUTDIR $INPUT_DOCX
```
- 将 PDF 文件转换为 PNG 图片：```
pdftoppm -png $OUTDIR/$BASENAME.pdf $OUTDIR/$BASENAME
```

### 提供的辅助工具：
```
python3 scripts/render_docx.py /path/to/file.docx --output_dir /tmp/docx_pages
```

## 文档质量要求
- 提供适合客户使用的文档：保持一致的字体、间距、页边距和清晰的层次结构。
- 避免出现格式错误，如文本被裁剪、表格重叠、字符无法显示或使用默认模板导致的样式问题。
- 图表、表格和视觉元素在渲染后的页面上必须清晰可读，对齐方式正确。
- 仅使用 ASCII 连字符（-），避免使用 U+2011（非断字符）或其他 Unicode 连字符。
- 引用和参考文献必须便于人类阅读；不要留下工具生成的占位符或临时字符串。

## 最终检查步骤
- 在最终交付前，以 100% 的放大比例重新渲染并检查每一页。
- 修复任何间距、对齐或分页问题，并重新进行渲染。
- 确保没有多余的临时文件或重复渲染的文档，除非用户另有要求。