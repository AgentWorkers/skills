---
name: odt-filemgr-oc
description: 使用 Python 和 odfdo 在本地创建、解析和编辑 ODT（OpenDocument Text）文件。当用户需要创建、编辑、读取、更新、追加内容、检查或操作任何 ODT 文件时，可以使用此功能。该功能可与 nextcloud-aio-oc 技能配合使用，以实现与 NextCloud 的集成——nextcloud-aio-oc 负责下载和上传二进制文件，而本功能则负责所有文档级别的编辑操作。
license: MIT
compatibility: Requires Python 3.10+.
required-binaries:
  - python3>=3.10
---
# ODT 文件管理器

本地 ODT 文档的创建和编辑由 `odfdo` 提供支持。

**依赖库**：`odfdo` v3.20+ — 正在维护中，仅依赖一个库（`lxml`），支持完整的 ODF 格式。

## 必需的设置

```bash
pip install odfdo
```

## 技能限制

此技能仅用于本地操作，不支持网络访问，也不涉及 NextCloud 的功能。

对于需要使用 NextCloud 的工作流程，请结合使用 `nextcloud-aio-oc`：

| 步骤 | 所需技能 |
|------|-------|
| 在 NextCloud 中查找文件 | `nextcloud-aio-oc` → `node scripts/nextcloud.js` 中的文件搜索功能 |
| 下载二进制 ODT 文件 | `nextcloud-aio-oc` → `python3 scripts/files_binary.py` 中的下载功能 |
| **编辑/创建 ODT 文件** | `odt-filemgr-oc` → `python3 scripts/odt_tool.py` 中的相关命令 |
| 上传二进制 ODT 文件 | `nextcloud-aio-oc` → `python3 scripts/files_binary.py` 中的上传功能 |

相关脚本位于：`~/.openclaw/skills/odt-filemgr-oc/scripts/`

---

## 工作流程

### 在 NextCloud 中编辑现有的 ODT 文件

```bash
NC=~/.openclaw/skills/nextcloud-aio-oc/scripts
ODT=~/.openclaw/skills/odt-filemgr-oc/scripts

# 1. Download
python3 $NC/files_binary.py download "/Documents/MyDoc.odt" /tmp/MyDoc.odt

# 2. Inspect
python3 $ODT/odt_tool.py inspect /tmp/MyDoc.odt

# 3. Edit
python3 $ODT/odt_tool.py append /tmp/MyDoc.odt --text "New Section" --heading 2
python3 $ODT/odt_tool.py append /tmp/MyDoc.odt --text "Section content here."

# 4. Upload back
python3 $NC/files_binary.py upload /tmp/MyDoc.odt "/Documents/MyDoc.odt"
```

### 创建新的 ODT 文件并上传到 NextCloud

```bash
# 1. Create locally
python3 $ODT/odt_tool.py create /tmp/NewDoc.odt --title "Q1 Report"

# 2. Add content
python3 $ODT/odt_tool.py append /tmp/NewDoc.odt --text "Summary" --heading 2
python3 $ODT/odt_tool.py append /tmp/NewDoc.odt --text "Results were positive across all metrics."

# 3. Push to NextCloud
python3 $NC/files_binary.py upload /tmp/NewDoc.odt "/Documents/Q1 Report.odt"
```

### 在本地编辑 ODT 文件（不使用 NextCloud）

```bash
python3 $ODT/odt_tool.py inspect   myfile.odt
python3 $ODT/odt_tool.py to-text   myfile.odt
python3 $ODT/odt_tool.py append    myfile.odt --text "Added paragraph."
python3 $ODT/odt_tool.py replace   myfile.odt --find "draft" --sub "final"
python3 $ODT/odt_tool.py set-meta  myfile.odt --title "Final Report"
```

---

## `odt_tool.py` 命令

| 命令 | 功能描述 |
|---------|-------------|
| `inspect <file>` | 显示文档的元数据以及段落、标题、表格的结构 |
| `to-text <file>` | 按文档顺序提取所有文本内容 |
| `create <file> [--title T]` | 创建一个空 ODT 文件（可选设置 H1 标题） |
| `append <file> --text T [--heading N] [--style S]` | 向 ODT 文件中添加标题（N=1–6）或段落 |
| `replace <file> --find F --sub S [--regex]` | 查找并替换指定文本 |
| `set-meta <file> [--title T] [--subject S] [--description D]` | 更新文档元数据 |
| `set-font <file> --font F [--size N] [--no-preserve-mono]` | 为整个文档设置字体（包括默认样式及所有自定义样式） |
| `set-outline <file> --numbered \| --plain` | 切换标题编号格式（1.1.1 或无编号） |
| `merge-styles <file> --template T` | 从模板 ODT 文件中应用所有样式 |

---

## 自定义 Python 编辑操作

对于需要自定义表格格式、修改样式或执行多步骤操作的情况，可以直接编写 Python 代码：

```python
from odfdo import Document, Header, Paragraph

doc = Document("/tmp/file.odt")
body = doc.body

# Read all content in order
for child in body.children:
    if isinstance(child, Header):
        print(f"H{child.level}: {child.inner_text}")
    elif isinstance(child, Paragraph) and child.inner_text.strip():
        print(f"[{child.style}]: {child.inner_text}")

# Add content
body.append(Header(2, "New Section"))
body.append(Paragraph("Content here."))

# Table edit
table = body.get_table_by_name("MyTable")
table.set_value(0, 0, "Updated cell")

doc.save("/tmp/file.odt", pretty=True)
```

有关 `odfdo` 的完整 API（包括表格、列表、样式、元数据等功能的详细信息，请参阅 [REFERENCE.md](REFERENCE.md)。

---

## 关键规则

1. **编辑文件前务必先检查文件内容**。
2. **临时文件**：使用 `/tmp/` 目录存放临时文件；上传完成后请清理临时文件。
3. **样式设置**：对于复杂的样式设置（如颜色、间距、边框等），建议使用 `merge-styles` 命令结合模板文件来应用样式，而非从头开始生成样式。`set-font` 和 `set-outline` 命令适用于任何文档，无需模板。

---

## 常见问题及解决方法

| 错误 | 解决方案 |
|-------|-----|
| `ModuleNotFoundError: odfdo` | 使用 `pip install odfdo` 安装 `odfdo` 库 |
| `zipfile.BadZipFile` | 文件损坏或不是有效的 ODT 格式——请重新下载文件 |
| 标题未显示为 H1 格式 | 应使用 `Header(1, "text")` 而不是 `Paragraph("text", style="Heading 1")` |
| 在 Collabora 中字体显示不正确 | ODT 格式中每个样式规则包含 6 个字体属性，旧方法只设置了 3 个属性（`style:font-name-*`）。Collabora 会根据 `fo:font-family` 属性来显示字体，因此需要设置全部 6 个属性。请重新运行 `set-font` 命令。 |
| 字体名称必须完全匹配 | LibreOffice 和 Collabora 对字体名称是区分大小写的，例如 `"Noto Sans"` 必须写成 `"Noto Sans"` |
| 使用 `set-outline` 后更改无效 | 有些文档可能通过段落样式覆盖了编号设置——此时请使用 `merge-styles` 命令结合干净的模板文件来应用样式。