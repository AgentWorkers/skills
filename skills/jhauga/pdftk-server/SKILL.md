---
name: pdftk-server
description: '**使用命令行工具 pdftk（PDFtk Server）处理 PDF 文件的技能**  
当需要从命令行执行以下操作时，可以使用 pdftk：合并 PDF 文件、分割 PDF 文件、旋转页面、加密或解密 PDF 文件、填写 PDF 表单、添加水印、叠加印章、提取元数据、将文档拆分为多个页面、修复损坏的 PDF 文件、附加或提取文件，以及进行其他 PDF 操作。'
---
# PDFtk Server

PDFtk Server 是一个用于处理 PDF 文档的命令行工具。它支持合并、分割、旋转、加密、解密、添加水印、盖章、填写表单、提取元数据等多种 PDF 操作。

## 适用场景

- 将多个 PDF 文件合并为一个文件
- 将 PDF 文件分割成单独的页面
- 旋转 PDF 页面
- 加密或解密 PDF 文件
- 根据 FDF/XFDF 数据填充 PDF 表单字段
- 应用背景水印或前景印章
- 提取 PDF 元数据、书签或表单字段信息
- 修复损坏的 PDF 文件
- 添加或提取 PDF 中嵌入的文件
- 从 PDF 中删除特定页面
- 整合单独扫描的偶数页和奇数页
- 压缩或解压 PDF 页面流

## 前提条件

- 确保系统中已安装 PDFtk Server：
  - **Windows**：下载并运行安装程序（详见 `references/download.md`）
  - **macOS**：使用 `brew install pdftk-java` 安装
  - **Linux (Debian/Ubuntu)**：使用 `sudo apt-get install pdftk` 安装
  - **Linux (Red Hat/Fedora)**：使用 `sudo dnf install pdftk` 安装
- 具备终端或命令提示符的访问权限
- 通过运行 `pdftk --version` 验证安装是否成功

## 分步操作流程

### 合并多个 PDF 文件

```bash
pdftk file1.pdf file2.pdf cat output merged.pdf
```

### 将 PDF 文件分割成单独的页面

```bash
pdftk input.pdf burst
```

### 提取特定页面

提取第 1-5 页和第 10-15 页：

```bash
pdftk input.pdf cat 1-5 10-15 output extracted.pdf
```

### 删除特定页面

删除第 13 页：

```bash
pdftk input.pdf cat 1-12 14-end output output.pdf
```

### 旋转页面

将所有页面顺时针旋转 90 度：

```bash
pdftk input.pdf cat 1-endeast output rotated.pdf
```

### 加密 PDF 文件

设置所有者密码和用户密码，并使用 128 位加密（默认设置）：

```bash
pdftk input.pdf output secured.pdf owner_pw mypassword user_pw userpass
```

### 解密 PDF 文件

使用已知密码解除 PDF 文件的加密：

```bash
pdftk secured.pdf input_pw mypassword output unsecured.pdf
```

### 填写 PDF 表单

从 FDF 文件中填充表单字段，并使用 `flatten` 选项将表单内容合并到页面中以防止进一步编辑：

```bash
pdftk form.pdf fill_form data.fdf output filled.pdf flatten
```

### 应用背景水印

在输入 PDF 的每一页后面添加一张单页 PDF（输入 PDF 需要具有透明度）：

```bash
pdftk input.pdf background watermark.pdf output watermarked.pdf
```

### 添加印章

在输入 PDF 的每一页上面添加一张单页 PDF：

```bash
pdftk input.pdf stamp overlay.pdf output stamped.pdf
```

### 提取元数据

导出书签、页面统计信息和文档信息：

```bash
pdftk input.pdf dump_data output metadata.txt
```

### 修复损坏的 PDF 文件

使用 pdftk 尝试自动修复损坏的 PDF 文件：

```bash
pdftk broken.pdf output fixed.pdf
```

### 整合扫描页面

将单独扫描的偶数页和奇数页合并在一起：

```bash
pdftk A=even.pdf B=odd.pdf shuffle A B output collated.pdf
```

## 故障排除

| 错误 | 解决方案 |
|-------|----------|
| 未找到 `pdftk` 命令 | 验证安装是否成功；确保 `pdftk` 在系统的 PATH 变量中 |
| 无法解密 PDF | 确保通过 `input_pw` 参数提供了正确的所有者密码或用户密码 |
| 输出文件为空或损坏 | 检查输入文件的完整性；可以先尝试运行 `pdftk input.pdf output repaired.pdf` |
- 填写表单后表单字段不可见 | 使用 `flatten` 选项将表单字段合并到页面内容中 |
- 水印未显示 | 确保输入 PDF 包含透明区域；对于不透明的印章，请使用 `stamp` 命令 |
- 出现权限错误 | 检查输入文件和输出文件的权限设置 |

## 参考资料

相关参考文档位于 `references/` 文件夹中：
- [pdftk-man-page.md](references/pdftk-man-page.md)：包含所有操作、选项和语法的完整手册
- [pdftk-cli-examples.md](references/pdftk-cli-examples.md)：常见命令行操作的实用示例
- [download.md](references/download.md)：所有平台的安装和下载说明
- [pdftk-server-license.md](references/pdftk-server-license.md)：PDFtk Server 的许可信息
- [third-party-materials.md](references/third-party-materials.md)：第三方库的许可信息