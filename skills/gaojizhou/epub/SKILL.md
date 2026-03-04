---
name: epub
description: 每当用户需要阅读、解析、提取内容、修改或以其他方式处理.epub文件时，都可以使用此技能。触发条件包括任何提及“.epub”、“ebook”或“epub file”的内容，以及请求从电子书中提取章节、目录、文本、图片或元数据的情况。此外，当用户希望将.epub内容转换为其他格式、检查.epub文件的结构或编辑.epub文件时，也可以使用此技能。由于.epub文件实际上是一种经过伪装的ZIP压缩文件，因此该技能采用了“解压后解析”的可靠方法，这种方法始终能够正常工作。即使对于看似简单的.epub操作（如“阅读这本.epub文件”或“显示文件中的章节”），也需要执行相应的提取流程。
---
# EPUB处理指南

## 核心要点：EPUB实际上是一个ZIP压缩文件

`.epub`文件只是一个具有特定内部结构的ZIP压缩文件。处理EPUB文件最可靠的方法是：

1. 将文件复制到工作目录中。
2. 将文件名从`.epub`更改为`.zip`。
3. 解压文件到一个文件夹中。
4. 首先找到并读取导航文件或目录文件（例如`nav.xhtml`、`nav.html`或`toc.ncx`）。
5. 然后根据需要读取内容文件。

这种方法在100%的情况下都能成功使用，且不需要任何特殊的EPUB处理库。

---

## 分步工作流程

### 第1步：提取EPUB文件

```bash
# Copy uploaded file to working directory
cp /mnt/user-data/uploads/book.epub /home/claude/book.epub

# Rename to .zip and extract
cp /home/claude/book.epub /home/claude/book.zip
unzip -o /home/claude/book.zip -d /home/claude/book_extracted/

# List the extracted contents
find /home/claude/book_extracted/ -type f | sort
```

### 第2步：找到导航文件（优先级最高）

导航文件就是目录文件，它包含了书籍的结构、章节顺序以及文件布局信息。务必先找到并读取这个文件。

```bash
# Look for nav files (in priority order)
find /home/claude/book_extracted/ -type f \( \
  -name "nav.xhtml" -o \
  -name "nav.html" -o \
  -name "toc.ncx" -o \
  -name "*nav*" -o \
  -name "*toc*" \
\) | sort
```

**导航文件的优先级顺序：**
1. `nav.xhtml` 或 `nav.html` — EPUB3格式的导航文件（推荐使用）
2. `toc.ncx` — EPUB2格式的导航文件（旧版本）
3. 任何名称中包含“nav”或“toc”的文件

```bash
# Read the nav file to understand structure
cat /home/claude/book_extracted/OEBPS/nav.xhtml
# or
cat /home/claude/book_extracted/EPUB/nav.html
```

### 第3步：找到OPF包文件

`.opf`文件（Open Packaging Format）包含了元数据和完整的阅读顺序信息。

```bash
# Find the OPF file
find /home/claude/book_extracted/ -name "*.opf" | head -5

# Read it for metadata and spine (reading order)
cat /home/claude/book_extracted/OEBPS/content.opf
```

在`.opf`文件中，`<spine>`元素定义了章节的阅读顺序，`<metadata>`块则包含了书籍的标题、作者、语言等信息。

### 第4步：读取内容文件

```bash
# Find all HTML/XHTML content files
find /home/claude/book_extracted/ -type f \( -name "*.html" -o -name "*.xhtml" \) | sort

# Read a specific chapter
cat /home/claude/book_extracted/OEBPS/chapter01.xhtml
```

要从HTML内容中提取纯文本，可以使用以下方法：

```python
from bs4 import BeautifulSoup

with open("/home/claude/book_extracted/OEBPS/chapter01.xhtml", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")
    
# Remove script/style tags
for tag in soup(["script", "style"]):
    tag.decompose()

text = soup.get_text(separator="\n", strip=True)
print(text)
```

---

## EPUB文件的典型目录结构

```
book_extracted/
├── mimetype                    ← Must contain "application/epub+zip"
├── META-INF/
│   └── container.xml           ← Points to the OPF file
└── OEBPS/   (or EPUB/, or OPS/)
    ├── content.opf             ← Package manifest + metadata + spine
    ├── nav.xhtml               ← ★ TABLE OF CONTENTS (read this first!)
    ├── toc.ncx                 ← Older TOC format (EPUB2)
    ├── chapter01.xhtml
    ├── chapter02.xhtml
    ├── ...
    ├── images/
    │   └── cover.jpg
    ├── css/
    │   └── styles.css
    └── fonts/
```

### 通过`container.xml`文件找到OPF文件的路径

```bash
cat /home/claude/book_extracted/META-INF/container.xml
```

`container.xml`文件总是通过`<rootfile full-path="...">`来指向根目录下的OPF文件。

---

## 常见任务

### 提取所有文本内容（整本书）

```python
import os
from bs4 import BeautifulSoup

extracted_dir = "/home/claude/book_extracted/OEBPS"
output_text = []

# Get ordered list of content files from OPF spine (or just sort them)
html_files = sorted([
    f for f in os.listdir(extracted_dir)
    if f.endswith((".html", ".xhtml")) and "nav" not in f.lower()
])

for filename in html_files:
    filepath = os.path.join(extracted_dir, filename)
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    for tag in soup(["script", "style", "head"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    output_text.append(f"\n\n--- {filename} ---\n\n{text}")

full_text = "\n".join(output_text)
with open("/mnt/user-data/outputs/book_full_text.txt", "w", encoding="utf-8") as f:
    f.write(full_text)
```

### 提取元数据

```python
import xml.etree.ElementTree as ET

tree = ET.parse("/home/claude/book_extracted/OEBPS/content.opf")
root = tree.getroot()

# Namespace handling
ns = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc":  "http://purl.org/dc/elements/1.1/"
}

metadata = root.find("opf:metadata", ns)
if metadata is not None:
    title   = metadata.findtext("dc:title",    namespaces=ns)
    author  = metadata.findtext("dc:creator",  namespaces=ns)
    lang    = metadata.findtext("dc:language", namespaces=ns)
    pub     = metadata.findtext("dc:publisher",namespaces=ns)
    date    = metadata.findtext("dc:date",     namespaces=ns)
    print(f"Title:     {title}")
    print(f"Author:    {author}")
    print(f"Language:  {lang}")
    print(f"Publisher: {pub}")
    print(f"Date:      {date}")
```

### 从`nav.xhtml`文件中解析目录结构

```python
from bs4 import BeautifulSoup

with open("/home/claude/book_extracted/OEBPS/nav.xhtml", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "html.parser")

# Find the nav element with epub:type="toc"
nav = soup.find("nav", attrs={"epub:type": "toc"}) or soup.find("nav")

if nav:
    print("=== Table of Contents ===")
    for a in nav.find_all("a"):
        print(f"  {a.get_text(strip=True)}  →  {a.get('href', '')}")
```

### 从`toc.ncx`文件（EPUB2格式）中解析目录结构

```python
import xml.etree.ElementTree as ET

tree = ET.parse("/home/claude/book_extracted/OEBPS/toc.ncx")
root = tree.getroot()
ns = {"ncx": "http://www.daisy.org/z3986/2005/ncx/"}

print("=== Table of Contents (NCX) ===")
for navpoint in root.findall(".//ncx:navPoint", ns):
    label = navpoint.findtext("ncx:navLabel/ncx:text", namespaces=ns)
    src   = navpoint.find("ncx:content", ns)
    href  = src.get("src") if src is not None else ""
    print(f"  {label}  →  {href}")
```

### 提取封面图片

```bash
# Find the cover image
find /home/claude/book_extracted/ -type f \( \
  -name "cover*" -o -name "*cover*" \
\) | grep -iE "\.(jpg|jpeg|png|gif|webp)$"
```

### 重新打包修改后的EPUB文件

如果你对提取出的文件进行了修改，想要重新打包成EPUB文件，可以按照以下步骤操作：

```bash
cd /home/claude/book_extracted/

# mimetype MUST be first and uncompressed
zip -0 -X /home/claude/modified_book.epub mimetype

# Add everything else
zip -r /home/claude/modified_book.epub . --exclude mimetype

# Copy to output
cp /home/claude/modified_book.epub /mnt/user-data/outputs/modified_book.epub
```

---

## 快速参考

| 目标 | 需要读取的文件 | 使用的工具 |
|------|-------------|------|
| 了解文件结构 | `META-INF/container.xml` → OPF文件的路径 | `cat` / `xml.etree` |
| 查看目录结构 | `nav.xhtml` 或 `nav.html`（EPUB3格式） | `BeautifulSoup` |
| 查看旧版目录结构 | `toc.ncx`（EPUB2格式） | `xml.etree` |
| 读取书籍元数据 | `*.opf` 文件中的`<metadata>`块 | `xml.etree` |
| 获取阅读顺序信息 | `*.opf` 文件中的`<spine>`块 | `xml.etree` |
| 读取章节内容 | `*.xhtml` / `*.html` 文件 | `BeautifulSoup` |
| 提取封面图片 | `images/cover.*` 文件或OPF文件中的`<item properties="cover-image">` | `shutil.copy` |

## 所需的Python库

```bash
pip install beautifulsoup4 lxml --break-system-packages
```

系统默认已经安装了`unzip`工具，无需额外安装专门的EPUB处理库。

---

## 常见问题解决方法

- **“找不到导航文件”**：尝试使用命令`find . -name "*.xhtml" -o -name "*.html" | xargs grep -l "epub:type" 2>/dev/null`来查找导航文件。
- **编码错误**：在打开EPUB文件中的HTML或XML内容时，始终使用`encoding="utf-8", errors="ignore"`来设置编码方式。
- **XML命名空间问题**：EPUB文件使用了多个XML命名空间。在使用`xml.etree`库时，务必将命名空间信息作为字典传递给`find`/`findall`方法，或者直接使用`{namespace_uri}tagname`的语法。
- **目录结构异常**：首先检查`META-INF/container.xml`文件，因为它总是能提供正确的根目录OPF文件的路径，不受目录命名规则的影响。