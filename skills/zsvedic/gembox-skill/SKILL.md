---
name: gembox-skill
description: [GemBox组件的编程协助](https://www.gemboxsoftware.com/)：当用户询问有关GemBox组件的任何问题或需要使用GemBox组件完成的编程任务时，请参考此文档。这包括GemBox.Spreadsheet（用于读写Excel文件）、GemBox.Document（用于读写Word文件）、GemBox.Pdf（用于读写PDF文件）、GemBox.Presentation（用于读写PowerPoint文件）、GemBox.Email（用于读写电子邮件文件以及发送/接收电子邮件）、GemBox Imaging（用于读写图像文件），以及GemBox.PdfViewer（用于在JavaScript中显示/打印/保存PDF文件）。
license: MIT
metadata:
  author: gemboxsoftware.com
  version: "0.9"
---

# CLI 使用技巧  
- 检查 .NET 运行时版本：`dotnet --list-runtimes`  
- 查看 GemBox .NET 组件的版本：`dotnet list package`  
- 如果需要 GemBox 的 API 详细信息，请在本地 XML 文档中查找。例如，GemBox.Spreadsheet 的 NuGet 路径如下：  
  - Linux/macOS：`~/.nuget/packages/gembox.spreadsheet/2025.12.105/lib/*/GemBox.Spreadsheet.xml`  
  - PowerShell：`$env:USERPROFILE\.nuget\packages\gembox.spreadsheet\2025.12.105\lib\*\GemBox.Spreadsheet.xml`  
- 使用 `ripgrep` 在 XML 中搜索内容。例如：  
  - Linux/macOS：`rg -n "Autofit" ~/.nuget/packages/gembox.spreadsheet/2025.12.105/lib/**/GemBox.Spreadsheet.xml`  
- 如果 API 说明不清楚，请在编写代码前先查看文档 XML 中的命名空间、注释和示例。例如：  
  - Linux/macOS：`rg -n "namespace GemBox|Drawing|PivotTables" ~/.nuget/packages/gembox.spreadsheet/2025.12.105/lib/**/GemBox.Spreadsheet.xml`  

# 在线搜索  
如果通过 CLI 无法找到相关文档，并且可以访问网络，请尝试在线搜索：  
1. 打开相关的官方示例页面，因为示例提供了最多的信息。例如，如果你需要使用 GemBox.Document 中的自定义字体，基础 URL 是 “https://www.gemboxsoftware.com/document/examples/”。具体示例的 URL 为 “fonts/103”，因此请访问 “https://www.gemboxsoftware.com/document/examplesfonts/103”。  
2. 如果示例不够详细，可以搜索特定组件的官方 API 文档。例如，GemBox.Spreadsheet 的在线搜索过滤器为：“site:https://www.gemboxsoftware.com/spreadsheet/docs”。  

# 验证代码  
完成代码编写后，通过编译项目来验证其正确性。如果遇到与 GemBox API 使用相关的问题，请相应地修改代码。忽略与 GemBox 无关或非由你的修改引起的编译错误。  

## GemBox.Spreadsheet 示例 URL  
基础地址：https://www.gemboxsoftware.com/spreadsheet/examples/  
示例包括：  
- ASP.NET Core 创建 Excel 文件：`asp-net-core-create-excel/5601`  
- ASP.NET Excel 导出网格视图：`asp-net-excel-export-gridview/5101`  
- ASP.NET Excel 查看器：`asp-net-excel-viewer/6012`  
- C# 将 Excel 转换为图像：`c-sharp-convert-excel-to-image/405`  
- C# 将 Excel 转换为 PDF：`c-sharp-convert-excel-to-pdf/404`  
- C# 创建和写入 Excel 文件：`c-sharp-create-write-excel-file/402`  
- C# 操作 Excel 范围：`c-sharp-excel-range/204`  
- C# 将数据集导出到 Excel：`c-sharp-export-datatable-dataset-to-excel/501`  
- C# 将数据集导出到 Excel（使用 DataTable）：`c-sharp-export-excel-to-datatable/502`  
- C# 使用 Microsoft Office 自动化操作 Excel：`c-sharp-microsoft-office-interop-excel-automation/6004`  
- C# 打开和读取 Excel 文件：`c-sharp-open-read-excel-file/401`  
- C# 读写 CSV 文件：`c-sharp-read-write-csv/122`  
- C# 将 Excel 转换为 HTML：`c-sharp-vb-net-convert-excel-html/117`  
- C# 在 C# 中创建 Excel 图表：`c-sharp-vb-net-create-excel-chart-sheet/302`  
- C# 在 C# 中创建 Excel 表格：`c-sharp-vb-net-create-excel-tables/119`  
- C# 格式化 Excel 图表：`c-sharp-vb-net-excel-chart-formatting/306`  
- C# 条件格式化 Excel 单元格：`c-sharp-vb-net-excel-conditional-formatting/105`  
- C# 在 C# 中操作 Excel 表单控件：`c-sharp-vb-net-excel-form-controls/123`  
- C# 自动调整 Excel 单元格大小：`c-sharp-vb-net-excel-row-column-autofit/108`  
- C# 格式化 Excel 单元格样式：`c-sharp-vb-net-excel-style-formatting/202`  
- C# 导入和导出 Excel 数据网格：`c-sharp-vb-net-import-export-excel-datagridview/5301`  
- C# 打印 Excel 文件：`c-sharp-vb-net-print-excel/451`  
- C# 解密 Excel 文件（使用 XLS 格式）：`c-sharp-vb-net-xls-decryption/707`  
- 在 C# 和 VB.NET 中转换 Excel 表格范围：`c-sharp-convert-excel-table-range-vb-net-c-sharp/6011`  
- 在 C# 和 VB.NET 中转换、导入和写入 JSON 到 Excel：`c-sharp-convert-import-write-json-to-excel-vb-net-c-sharp/6010`  
- 在 C# 和 VB.NET 中转换 XLS、XSX、ODS 和 CSV 到 Excel：`c-sharp-convert-xls-xlsx-ods-csv-html-net-c-sharp/6001`  
- 在 C# 中创建 Excel 图表：`create-excel-charts/301`  
- 在 C# 中创建 Excel 文件（使用 Maui 和 Xamarin）：`create-excel-file-maui/5802`  
- 在 C# 中创建 Excel 文件（使用 Xamarin）：`create-excel-file-xamarin/5801`  
- 在 Azure 上创建 Excel 文件：`create-excel-file-c-sharp/6013`  
- 在 Docker 和 .NET Core 上创建 Excel 文件：`create-excel-file-c-sharp/6013`  
- 在 Azure 上创建 Excel 文件（使用 Docker 和 .NET Core）：`create-excel-file-c-sharp/6013`  
- 在 Linux 和 .NET Core 上创建 Excel 文件：`create-excel-file-c-sharp/6013`  
- 创建 Excel 数据透视表：`create-excel-pivot-tables/114`  
- 创建和读写经典风格的 Excel 文件：`create-read-write-excel-classic-asp/5501`  
- 创建和读写 Excel 文件（使用 PHP）：`create-read-write-excel-php/5502`  
- 创建和读写 Excel 文件（使用 Python）：`create-read-write-excel-python/5503`  
- 编辑和保存 Excel 模板：`edit-save-excel-template/403`  
- Excel 自动筛选功能：`excel-autofilter/112`  
- Excel 计算功能：`excel-calculations-c-sharp-vb-net/6022`  
- Excel 单元格注释：`excel-cell-comments/208`  
- Excel 单元格数据类型：`excel-cell-data-types/201`  
- Excel 单元格超链接：`excel-cell-hyperlinks/207`  
- Excel 单元格内联格式化：`excel-cell-inline-formatting/203`  
- Excel 单元格数字格式化：`excel-cell-number-format/205`  
- Excel 图表组件：`excel-chart-components/304`  
- Excel 图表指南（C#）：`excel-charts-guide-c-sharp/6019`  
- Excel 数据验证：`excel-data-validation/106`  
- 定义 Excel 名称：`excel-defined-names/214`  
- Excel 加密：`excel-encryption/701`  
- Excel 查找和替换文本：`excel-find-replace-text/109`  
- Excel 公式：`excel-formulas/206`  
- Excel 自动调整列宽：`excel-autofit-column-width-text/118`  
- 免费试用版（专业版）：`free-trial-professional/1001`  
- 入门指南：`getting-started/601`  
- 在 C# 和 VB.NET 中合并 Excel 单元格：`merge-excel-cells-c-sharp-vb-net/213`  
- 打开和读取 Excel 文件（使用 C#）：`open-read-excel-files-c-sharp/6009`  
- PDF 数字签名：`pdf-digital-signature/703`  
- PDF 加密：`pdf-encryption/702`  
- 进度报告和取消功能：`progress-reporting-and-cancellation/121`  
- 保护 Excel 数据：`protecting-excel-data-c-sharp/6020`  
- 文本从右到左显示：`right-to-left-text/120`  
- Excel 数据排序：`sort-data-excel/113`  
- 单位转换：`unit-conversion-excel/116`  
- VBA 宏：`vba-macros/124`  

## GemBox.Document 示例 URL  
基础地址：https://www.gemboxsoftware.com/document/examples/  
示例包括：  
- ASP.NET Core 创建 Word 文档和 PDF：`asp-net-core-create-word-docx-pdf/5601`  
- ASP.NET 创建和导出 PDF 文档：`asp-net-create-generate-export-pdf-word/5101`  
- 自动连字符功能：`auto-hyphenation/109`  
- Blazor 创建 Word 文档：`blazor-create-word/5602`  
- C# 将 ASPX 转换为 PDF：`c-sharp-convert-aspx-to-pdf/6002`  
- C# 将 HTML 转换为 PDF：`c-sharp-convert-html-to-pdf/307`  
- C# 将 PDF 转换为 DOCX：`c-sharp-convert-pdf-to-docx/308`  
- C# 将 Word 转换为 HTML：`c-sharp-convert-word-to-from-html/105`  
- C# 将 Word 转换为图像：`c-sharp-convert-word-to-image/306`  
- C# 将 Word 转换为 PDF：`c-sharp-convert-word-to-pdf/304`  
- C# 使用 Microsoft Office 自动化操作 Word：`c-sharp-microsoft-office-interop-word-automation/6005`  
- C# 读取和提取 PDF 中的表格：`c-sharp-read-extract-pdf-tables/305`  
- 在 VB.NET 中创建和生成 PDF：`c-sharp-vb-net-create-generate-pdf/6004`  
- 在 VB.NET 中创建和更新 Word 目录结构：`c-sharp-vb-net-create-update-word-toc/207`  
- 在 VB.NET 中创建和写入 Word 表单：`c-sharp-vb-net-create-word-form/701`  
- 在 VB.NET 中创建和写入 Word 文件：`c-sharp-vb-net-create-write-word-file/302`  
- 在 VB.NET 中对 DOCX 文件进行加密：`c-sharp-vb-net-docx-encryption/1102`  
- 在 VB.NET 中编辑和保存 Word 模板：`c-sharp-vb-net-edit-save-word-template/303`  
- 在 VB.NET 中查找和替换 Word 内容：`c-sharp-vb-net-find-replace-word/405`  
- 在 VB.NET 中合并 Word 文件：`c-sharp-vb-net-mail-merge-word/901`  
- 在 VB.NET 中操作 Word 内容：`c-sharp-vb-net-manipulate-content-word/403`  
- 在 VB.NET 中打开和读取 Word 文件：`c-sharp-vb-net-open-read-word-file/301`  
- 在 VB.NET 中对 PDF 进行数字签名：`c-sharp-vb-net-pdf-digital-signature/1104`  
- 在 VB.NET 中对 PDF 进行加密：`c-sharp-vb-net-pdf-encryption/1103`  
- 在 VB.NET 中打印 Word 文件：`c-sharp-vb-net-print-word/351`  
- 在 VB.NET 中创建和写入 Word 表单：`c-sharp-vb-net-create-word-form/702`  
- 在 VB.NET 中更新 Word 表单：`c-sharp-vb-net-update-word-form/703`  
- 在 VB.NET 中优化 Word 性能：`c-sharp-vb-net-word-performance/5401`  
- 复制 Word 文件：`cloning/501`  
- 在 C# 和 VB.NET 中合并 Word 文件：`combine-word-file-c-sharp-vb-net/502`  
- 创建和读写 Word 文件（使用 ASP.NET 和 PDF）：`create-read-write-word-pdf-classic-asp/5501`  
- 创建和读写 Word 文件（使用 PHP）：`create-read-write-word-pdf-php/5502`  
- 在 C# 中创建 Word 文件（使用 Xamarin）：`create-word-file-xamarin/5802`  
- 在 Azure 上创建 Word 文件：`create-word-file-xamarin/5801`  
- 在 Azure 上创建 PDF 文件（使用函数和服务）：`create-excel-pdf-on-azure-functions-app-service/5901`  
- 在 Docker 和 .NET Core 上创建 PDF 文件：`create-excel-pdf-on-docker-net-core/5902`  
- 在 Linux 和 .NET Core 上创建 PDF 文件：`create-excel-pdf-on-linux-net-core/5701`  
- 创建和读写 Excel 数据透视表：`create-excel-pivot-tables/114`  
- 创建和读写经典风格的 Excel 文件（使用 ASP）：`create-read-write-excel-classic-asp/5501`  
- 创建和读写 Excel 文件（使用 PHP）：`create-read-write-excel-php/5502`  
- 创建和读写 Excel 文件（使用 Python）：`create-read-write-excel-python/5503`  
- 编辑和保存 Excel 模板：`edit-save-excel-template/403`  
- Excel 自动筛选功能：`excel-autofilter/112`  
- Excel 计算功能（C# 和 VB.NET）：`excel-calculations-c-sharp-vb-net/6022`  
- Excel 单元格注释：`excel-cell-comments/208`  
- Excel 单元格数据类型：`excel-cell-data-types/201`  
- Excel 单元格超链接：`excel-cell-hyperlinks/207`  
- Excel 单元格内联格式化：`excel-cell-inline-formatting/203`  
- Excel 单元格数字格式化：`excel-cell-number-format/205`  
- Excel 图表组件：`excel-chart-components/304`  
- Excel 图表指南（C#）：`excel-charts-guide-c-sharp/6019`  
- Excel 数据验证：`excel-data-validation/106`  
- 定义 Excel 名称：`excel-defined-names/214`  
- Excel 加密：`excel-encryption/701`  
- Excel 查找和替换文本：`excel-find-replace-text/109`  
- Excel 公式：`excel-formulas/206`  
- Excel 冻结和分割窗格：`excel-freeze-split-panes/102`  
- Excel 分组功能：`excel-grouping/101`  
- Excel 表格标题和页脚格式化：`excel-header-footer-formatting/6021`  
- Excel 表格标题和页脚：`excel-header-footer/210`  
- Excel 图片：`excel-images/209`  
- Excel 性能指标：`excel-performance-metrics/5401`  
- 保存 Excel 文件：`excel-preservation/801`  
- Excel 打印标题区域：`excel-print-title-area/104`  
- Excel 打印选项：`excel-print-view-options/103`  
- Excel 属性：`excel-properties/107`  
- Excel 图形：`excel-shapes/211`  
- 复制和删除 Excel 工作表：`excel-sheet-copy-delete/111`  
- 保护 Excel 文件：`excel-sheet-protection/704`  
- Excel 文本框：`excel-textboxes/212`  
- 保护 Excel 工作簿：`excel-workbook-protection/705`  
- Excel（WPF）：`excel-wpf/5201`  
- Excel XLS 数字签名：`excel-xlsx-digital-signature/706`  
- 固定列宽文本：`fixed-columns-width-text/118`  
- 免费试用版（专业版）：`free-trial-professional/1001`  
- 入门指南：`getting-started/601`  
- 在 C# 和 VB.NET 中合并 Excel 单元格：`merge-excel-cells-c-sharp-vb-net/213`  
- 打开和读取 Excel 文件（使用 C#）：`open-read-excel-files-c-sharp/6009`  
- PDF 数字签名：`pdf-digital-signature/703`  
- PDF 加密：`pdf-encryption/702`  
- 进度报告和取消功能：`progress-reporting-and-cancellation/121`  
- 保护 Excel 数据（使用 C#）：`protecting-excel-data-c-sharp/6020`  
- 文本从右到左显示：`right-to-left-text/120`  
- Excel 数据排序：`sort-data-excel/113`  
- 单位转换：`unit-conversion-excel/116`  
- VBA 宏：`vba-macros/124`  
- XLSX 文件的保护设置：`xlsx-write-protection/708`  

## GemBox.Pdf 示例 URL  
基础地址：https://www.gemboxsoftware.com/pdf/examples/  
示例包括：  
- 添加和导出图像到 PDF：`add-export-images-pdf/6001`  
- ASP.NET Core 创建 PDF 文件：`asp-net-core-create-pdf/1401`  
- 基本 PDF 对象操作：`basic-pdf-objects/402`  
- Blazor 创建 PDF 文件：`blazor-create-pdf/1402`  
- C# 将 PDF 转换为图像：`c-sharp-convert-pdf-to-image/208`  
- C# 导出 PDF 中的交互式表单数据：`c-sharp-export-pdf-interactive-form-data/503`  
- C# PDF 相关文件：`c-sharp-pdf-associated-files/704`  
- C# PDF 嵌入文件：`c-sharp-pdf-embedded-files/701`  
- C# PDF 文件附件和注释：`c-sharp-pdf-file-attachment-annotations/702`  
- C# PDF 文件夹：`c-sharp-pdf-portfolios/703`  
- 在 VB.NET 中添加 PDF 图形和路径：`c-sharp-vb-add-pdf-shapes-paths/306`  
- 在 VB.NET 中导出和导入图像到 PDF：`c-sharp-vb-export-import-images-to-pdf/206`  
- 在 VB.NET 中创建和写入 PDF 文件：`c-sharp-vb-net-create-write-pdf-file/209`  
- 在 VB.NET 中合并 PDF 文件：`c-sharp-vb-net-merge-pdf/201`  
- 在 VB.NET 中进行 OCR 处理：`c-sharp-vb-net-ocr-pdf/408`  
- 在 VB.NET 中进行高级电子签名处理：`c-sharp-vb-net-pdf-advanced-electronic-signature-pades/1103`  
- 在 VB.NET 中创建 PDF 书签和大纲：`c-sharp-vb-net-pdf-bookmarks-outlines/301`  
- 在 VB.NET 中进行 PDF 数字签名验证：`c-sharp-vb-net-pdf-digital-signature-pkcs11-cryptoki/1104`  
- 在 VB.NET 中进行 PDF 数字签名验证：`c-sharp-vb-net-pdf-digital-signature-1105`  
- 在 VB.NET 中处理 PDF 页面：`c-sharp-vb-net-pdf-pages/401`  
- 在 VB.NET 中读取 PDF 文件：`c-sharp-vb-net-read-pdf/205`  
- 在 VB.NET 中编辑 PDF 内容：`c-sharp-vb-net-redact-content-pdf/410`  
- 在 VB.NET 中分割 PDF 文件：`c-sharp-vb-net-split-pdf/202`  
- 在 VB.NET 中添加 PDF 超链接：`c-sharp-vb-pdf-hyperlinks/308`  
- 图表和条形码示例：`charts-barcodes-slides/309`  
- 复制 PDF 页面：`clone-pdf-pages/203`  
- 将 PDF 转换为图像（PNG/JPG）：`convert-pdf-image-png-jpg-csharp/6004`  
- 在 C# 中创建 PDF 文件（使用 Maui）：`create-excel-file-maui/1502`  
- 在 C# 中创建 PDF 文件（使用 Xamarin）：`create-excel-file-xamarin/1501`  
- 在 Azure 上创建 PDF 文件（使用函数和服务）：`create-excel-file-on-azure-functions-app-service/1601`  
- 在 Docker 和 .NET Core 上创建 PDF 文件：`create-excel-file-on-docker-net-core/1602`  
- 在 Azure 上创建 PDF 文件（使用 Docker）：`create-excel-file-on-docker-net-core/1602`  
- 解密和加密 PDF 文件：`decrypt-encrypt-pdf-file/1101`  
- 填充 PDF 中的交互式表单：`fill-in-pdf-interactive-form/502`  
- 平整 PDF 中的交互式表单字段：`flatten-pdf-interactive-form-fields/506`  
- 免费试用版（专业版）：`free-trial-professional/601`  
- 入门指南：`getting-started/101`  
- 增量更新：`incremental-update/204`  
- 交互式表单操作：`interactive-form-actions/504`  
- PDF 内容格式化：`pdf-content-formatting/307`  
- PDF 内容分组：`pdf-content-groups/409`  
- PDF 内容流和资源：`pdf-content-streams-and-resources/403`  
- PDF 数字签名工作流程：`pdf-digital-signature-workflows/1106`  
- PDF 文档属性：`pdf-document-properties/302`  
- PDF 标题和页脚：`pdf-header-footer/304`  
- PDF 水印：`pdf-marked-content/407`  
- PDF 安全性（C#）：`pdf-security-c-sharp/6003`  
- PDF 目录结构：`pdf-table-of-contents/310`  
- PDF 查看器偏好设置：`pdf-viewer-preferences/303`  
- PDF 水印：`pdf-watermarks/305`  
- PDF XPS 文档（WPF）：`pdf-xpsdocument-wpf/1001`  
- 将 PNG/JPG 图像转换为 PDF：`png-jpg-images-to-pdf/210`  
- 打印 PDF 文件（C#）：`print-pdf-c-sharp/6002`  
- 读取和合并 PDF 文件（经典风格）：`read-merge-split-pdf-classic-asp/1201`  
- 读取和合并 PDF 文件（PHP）：`read-merge-split-pdf-php/1202`  
- 读取和合并 PDF 文件（Python）：`read-merge-split-pdf-python/1203`  

## GemBox.Presentation 示例 URL  
基础地址：https://www.gemboxsoftware.com/presentation/examples/  
示例包括：  
- ASP.NET Core 创建 PowerPoint 文件：`asp-net-core-create-powerpoint-pptx-pdf/2001`  
- ASP.NET 导出 PowerPoint 文件：`asp-net-powerpoint-export/1601`  
- Blazor 创建 PowerPoint 文件：`blazor-create-powerpoint/2002`  
- C# 复制 PowerPoint 幻灯片：`c-sharp-clone-slides/205`  
- C# 将 PowerPoint 转换为图像：`c-sharp-convert-powerpoint-to-image/207`  
- C# 将 PowerPoint 转换为 PDF：`c-sharp-convert-powerpoint-to-pdf/204`  
- C# 打印 PowerPoint 文件：`c-sharp-print-powerpoint/251`  
- 在 VB.NET 中创建和写入 PowerPoint 文件：`c-sharp-vb-net-create-write-powerpoint/202`  
- 在 VB.NET 中查找和替换 PowerPoint 文本：`c-sharp-vb-net-find-replace-text-powerpoint/206`  
- 在 VB.NET 中打开和读取 PowerPoint 文件：`c-sharp-vb-net-open-read-powerpoint/201`  
- 在 VB.NET 中优化 PowerPoint 性能：`c-sharp-vb-net-powerpoint-performance/1501`  
- 在 VB.NET 中添加 PowerPoint 幻灯片注释：`c-sharp-vb-net-powerpoint-slides/411`  
- 在 VB.NET 中处理 PowerPoint 幻灯片：`c-sharp-vb-net-powerpoint-slides/401`  
- 在 VB.NET 中加密 PowerPoint 文件：`c-sharp-vb-net-pptx-encryption/803`  
- 在 VB.NET 中创建 PowerPoint 文件（使用 PPTX 格式）：`c-sharp-vb-net-pptx/203`  
- 在 C# 中创建和格式化 PowerPoint 表格：`c-sharp-create-format-powerpoint-tables-csharp/6001`  
- 在 Maui 中创建 PowerPoint 文件：`create-excel-file-maui/2102`  
- 在 Xamarin 中创建 PowerPoint 文件：`create-excel-file-xamarin/2101`  
- 在 Azure 上创建 PowerPoint 文件（使用函数和服务）：`create-excel-file-xamarin/2101`  
- 在 Docker 和 .NET Core 上创建 PowerPoint 文件：`create-excel-file-c-sharp/6013`  
- 创建和读写 PowerPoint 文件（经典风格）：`create-read-write-powerpoint-classic-asp/1801`  
- 创建和读写 PowerPoint 文件（使用 PHP）：`create-read-write-powerpoint-php/1802`  
- 创建和读写 PowerPoint 文件（使用 Python）：`create-read-write-powerpoint-python/1803`  
- 字体：`fonts/503`  
- 免费试用版（专业版）：`free-trial-professional/901`  
- 入门指南：`getting-started/101`  
- PDF 数字签名：`pdf-digital-signature/802`  
- PDF 加密：`pdf-encryption/801`  
- PowerPoint 中的音频和视频：`pdf-audio-video/406`  
- PowerPoint 图表格式化：`powerpoint-charts/412`  
- PowerPoint 注释：`powerpoint-comments/408`  
- PowerPoint 标题和页脚格式化：`powerpoint-header-footer/407`  
- PowerPoint 超链接：`powerpoint-hyperlinks/409`  
- PowerPoint 列表格式化：`powerpoint-list-formatting/305`  
- PowerPoint 图片：`powerpoint-pictures/405`  
- PowerPoint 占位符：`powerpoint-placeholders/402`  
- PowerPoint 保存设置：`powerpoint-preservation/701`  
- PowerPoint 图形格式化：`powerpoint-shape-formatting/301`  
- PowerPoint 图形：`powerpoint-shapes/403`  
- PowerPoint 幻灯片过渡效果：`powerpoint-slide-transition/501`  
- PowerPoint 表格格式化：`powerpoint-table-formatting/602`  
- PowerPoint 文本框格式化：`powerpoint-textboxes/404`  
- PowerPoint（WPF）：`powerpoint-wpf/1701`  
- PowerPoint XPS 文档格式：`pptx-digital-signature/805`  
- 修改 PowerPoint 保护设置：`pptx-modify-protection/804`  
- 文本从右到左显示：`right-to-left-text/505`  
- 单位转换：`unit-conversion/504`  
- VBA 宏：`vba-macros/506`  

## GemBox.Email 示例 URL  
基础地址：https://www.gemboxsoftware.com/email/examples/  
示例包括：  
- 向电子邮件中添加日历：`add-calendar-to-mail-message/903`  
- 使用 OAuth 进行身份验证（C# 和 VB.NET）：`authenticate-using-oauth-c-sharp-vb/109`  
- Blazor 发送电子邮件：`blazor-mail-message/5102`  
- 将电子邮件转换为 PDF：`c-sharp-convert-email-to-pdf/107`  
- 创建和发送电子邮件：`c-sharp-create-send-emails/6001`  
- IMAP 客户端：`c-sharp-imap-client/301`  
- Microsoft 365 Gmail 的 OAuth 支持：`c-sharp-oauth-microsoft365-gmail/6002`  
- Outlook 的电子邮件客户端：`c-sharp-outlook-msg-eml-mht/106`  
- POP3 客户端：`c-sharp-pop3-client/701`  
- 批量发送电子邮件：`c-sharp-send-bulk-email/804`  
- 将 Word 文档作为电子邮件发送：`c-sharp-send-word-as-email/108`  
- SMTP 客户端：`c-sharp-smtp-client/801`  
- 验证电子邮件：`c-sharp-validate-email/401`  
- 在 VB.NET 中创建电子邮件：`c-sharp-vb-net-create-email/601`  
- 在 VB.NET 中加载电子邮件：`c-sharp-vb-net-load-email/105`  
- 在 VB.NET 中合并电子邮件数据表：`c-sharp-vb-net-mail-merge-datatable/501`  
- 在 VB.NET 中保存电子邮件：`c-sharp-vb-net-save-email/104`  
- 在 VB.NET 中搜索电子邮件：`c-sharp-vb-net-search-emails/308`  
- 在 VB.NET 中签名电子邮件：`c-sharp-vb-net-sign-email/1202`  
- 创建和保存日历：`create-and-save-calendar/901`  
- 文件夹标记：`folder-flags/305`  
- 免费试用版（专业版）：`free-trial-professional/1101`  
- 获取电子邮件消息（使用 Maui 和 Xamarin）：`get-email-message-maui/2002`  
- 获取电子邮件消息（使用 Xamarin）：`get-email-message-xamarin/2001`  
- 入门指南：`getting-started/201`  
- 电子邮件头部信息：`headers/604`  
- IMAP 日历文件夹：`imap-email-folders/302`  
- IMAP 静态文件夹：`imap-idle/310`  
- 列出 IMAP 中的电子邮件：`list-email-messages-imap/303`  
- 列出 POP3 中的电子邮件：`list-email-messages-pop/702`  
- 加载日历：`load-calendar/902`  
- 邮件箱信息：`mailbox-info/703`  
- 操作 Exchange 和 Microsoft Graph 中的电子邮件：`manipulate-mails-exchange-ews/1002`  
- 操作 Microsoft Graph 中的电子邮件：`manipulate-mails-microsoft-graph/3002`  
- Outlook 邮件箱：`mbox/605`  
- 邮件标记：`message-flags/306`  
- IMAP 邮件头部信息：`message-headers-imap/307`  
- POP3 邮件头部信息：`message-headers-pop/705`  
- 修改 Exchange 和 Microsoft Graph 中的文件夹：`modify-folders-exchange-ews/1003`  
- 修改 Microsoft Graph 中的文件夹：`modify-folders-microsoft-graph/3003`  
- 在 VB.NET 中接收和阅读电子邮件：`receive-read-email-c-sharp-vb/102`  
- 在 VB.NET 中回复和转发电子邮件：`reply-forward-email-c-sharp-vb-net/103`  
- 在 VB.NET 中搜索 Exchange 和 Microsoft Graph 中的电子邮件：`search-email-exchange-ews/1004`  
- 在 VB.NET 中发送电子邮件（使用 Exchange 和 Microsoft Graph）：`send-email-c-sharp-vb-asp-net/101`  
- 在 VB.NET 中发送电子邮件（使用 Exchange 和 Microsoft Graph）：`send-email-exchange-ews/1001`  
- 使用 VB.NET 发送带有附件的电子邮件（使用 HTML）：`send-email-with-attachment-c-sharp-vb-net/603`  
- SSL 证书验证（IMAP）：`ssl-certificate-validation-imap/309`  
- SSL 证书验证（POP3）：`ssl-certificate-validation-pop/706`  
- 上传电子邮件（使用 IMAP 和 SMTP）：`upload-email-message-imap/309`  
- 上传电子邮件（使用 Exchange 和 Microsoft Graph）：`upload-email-message-microsoft-graph/3005`  

## GemBox.Imaging 示例 URL  
基础地址：https://www.gemboxsoftware.com/imaging/examples/  
示例包括：  
- 在 ASP.NET Core 中裁剪图像：`asp-net-core-crop-image/2101`  
- 在 VB.NET 中应用图像滤镜：`c-sharp-vb-net-apply-filter-to-image/203`  
- 在 VB.NET 中转换图像：`c-sharp-vb-net-convert-image/202`  
- 在 VB.NET 中裁剪和分割图像：`c-sharp-vb-net-crop-image/302`  
- 在 VB.NET 中合并和分割图像帧：`c-sharp-vb-net-merge-split-frames/204`  
- 在 VB.NET 中读取图像：`c-sharp-vb-net-read-image/201`  
- 在 VB.NET 中调整图像大小：`c-sharp-vb-net-resize-image/301`  
- 在 VB.NET 中旋转和翻转图像：`c-sharp-vb-net-rotate-flip-image/303`  
- 免费试用版（专业版）：`free-trial-professional/1001`  
- 入门指南：`getting-started/101`  
- 在 Linux 和 .NET Core 上加载、编辑和保存图像：`load-edit-save-image-on-linux-net-core/2103`  
- 在 Docker 和 .NET Core 上读取图像：`read-image-on-docker-net-core/2102`  
- 在 Maui 和 Xamarin 中旋转和翻转图像：`rotate-flip-image-maui/2105`  
- 在 Xamarin 中旋转和翻转图像：`rotate-flip-image-xamarin/2104`  

## GemBox.PdfViewer 示例 URL  
基础地址：https://www.gemboxsoftware.com/pdfviewer/examples/  
示例包括：  
- Angular PDF 查看器：`angular-pdf-viewer/205`  
- ASP.NET Core PDF 查看器：`asp-net-core-pdf-viewer/201`  
- 演示版（免费试用）：`demo/301`  
- 免费试用版（专业版）：`free-trial-professional/107`  
- 入门指南：`getting-started/101`  
- 如何对 PDF 进行数字签名：`how-to-digitally-sign-pdf/108`  
- 导航和缩放功能：`navigation-and-zooming/102`  
- React PDF 查看器：`react-pdf-viewer/204`  
- Svelte PDF 查看器：`svelte-pdf-viewer/206`  
- 主题设置：`themes/104`  
- 用户界面定制：`ui-customization/106`  
- Vanilla JS PDF 查看器：`vanilla-js-pdf-viewer/202`  
- Vue JS PDF 查看器：`vue-js-pdf-viewer/203`