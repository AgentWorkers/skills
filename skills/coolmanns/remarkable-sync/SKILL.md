---
name: remarkable
description: 通过 Cloud API (rmapi) 与 reMarkable 平板电脑实现双向同步：可以获取手写笔记/草图，利用 AI 进行处理，然后将处理后的内容推回平板电脑。该功能可用于草图的优化、日记内容的提取，或向平板电脑发送文档/图片。
---

# reMarkable平板集成（rmapi）

通过Cloud API实现与reMarkable平板的双向同步。可以从平板获取草图和笔记，对其进行处理（包括AI增强和文本提取），然后将处理后的内容推回平板。

## 典型使用场景

1. **草图 → AI → 平板循环**：从平板获取草图 → 通过AI进行优化 → 将处理后的版本推回平板。
2. **日记记录**：从平板获取手写内容 → 进行解析 → 添加到记忆或日记中。
3. **头脑风暴**：从平板获取图表或列表 → 提取结构信息 → 添加到项目文档中。
4. **发送阅读材料**：将PDF或文档文件推送到平板上以便离线阅读。
5. **AI生成的艺术作品**：将生成的图像转换为PDF格式 → 推送到平板上以便在电子墨水显示屏上查看。

## 双向数据传输流程

```
┌─────────────────────────────────────────────────────────────────┐
│                        FETCH (tablet → agent)                    │
├─────────────────────────────────────────────────────────────────┤
│  reMarkable → Cloud sync → rmapi get → .rmdoc                   │
│                                           ↓                      │
│                              unzip → .rm file → rmc → SVG       │
│                                                      ↓           │
│                                          cairosvg → PNG          │
│                                                      ↓           │
│                               ┌──────────┴──────────┐            │
│                          Text content?         Visual/sketch?    │
│                               ↓                      ↓           │
│                        OCR/interpret          AI image editing   │
│                               ↓                      ↓           │
│                        Add to memory        Enhanced image       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        PUSH (agent → tablet)                     │
├─────────────────────────────────────────────────────────────────┤
│  Image/document → Convert to PDF (if needed) → rmapi put        │
│                                                      ↓           │
│                                           Cloud sync → tablet    │
└─────────────────────────────────────────────────────────────────┘
```

## 先决条件

### 1. 安装rmapi

从[juruen/rmapi](https://github.com/ddvk/rmapi/releases)下载最新版本（推荐使用ddvk分支）：

```bash
# Example for Linux amd64
curl -L https://github.com/ddvk/rmapi/releases/latest/download/rmapi-linux-amd64 -o ~/bin/rmapi
chmod +x ~/bin/rmapi
```

### 2. 安装转换工具

```bash
pip install --user rmc cairosvg pillow
```

- **rmc**：将`.rm`格式的笔画文件转换为SVG格式。
- **cairosvg**：将SVG格式转换为PNG格式。
- **pillow**：将PNG格式转换为PDF格式，以便推回平板。

### 3. 验证身份（仅一次）

1. 访问https://my.remarkable.com/connect/desktop。
2. 登录并复制8位验证码。
3. 运行`rmapi`，并在提示时输入验证码。
4. 验证码会保存在`~/.rmapi`文件中，之后的运行将自动完成身份验证。

## 命令

### 从平板获取数据（下载）

```bash
# List files/folders
rmapi ls
rmapi ls -l -t              # Long format, sorted by time

# Refresh from cloud
rmapi refresh

# Navigate
rmapi cd "folder name"

# Find files
rmapi find --starred /              # Starred items
rmapi find --tag="my-tag" /         # By tag
rmapi find / ".*sketch.*"           # By regex

# Download single file
rmapi get "filename"
rmapi get "Folder/Notebook"

# Download with annotations (best for handwritten content)
rmapi geta "filename"

# Bulk download folder
rmapi mget -o ./sync-folder/ "/My Folder"
```

### 将数据推回平板（上传）

```bash
# Upload single file (PDF or EPUB only)
rmapi put document.pdf
rmapi put document.pdf "Target Folder/"

# Bulk upload
rmapi mput ./local-folder/ "Remote Folder/"

# Create folder on tablet
rmapi mkdir "New Folder"
```

**支持的格式：** PDF, EPUB

## 转换流程

### 从平板获取数据（.rmdoc格式）→ PNG格式

reMarkable笔记本以`.rmdoc`格式下载（这是一个包含笔画数据的ZIP文件包）：

```bash
# 1. Download the notebook
rmapi get "Folder/MyNotebook"

# 2. Extract (it's a zip)
unzip "MyNotebook.rmdoc" -d extracted/

# 3. Find the .rm stroke file(s)
# Structure: extracted/<doc-uuid>/<page-uuid>.rm
find extracted -name "*.rm"

# 4. Convert .rm → SVG
rmc -t svg -o page.svg "extracted/<doc-uuid>/<page-uuid>.rm"

# 5. Convert SVG → PNG (reMarkable dimensions: 1404×1872)
python3 -c "
import cairosvg
cairosvg.svg2png(url='page.svg', write_to='page.png', output_width=1404, output_height=1872)
"
```

### 将数据推回平板（图像格式）

reMarkable仅支持PDF和EPUB格式，因此需要先将图像转换为相应的格式：

```python
from PIL import Image

img = Image.open('image.png')
rgb = img.convert('RGB')
rgb.save('image.pdf', 'PDF', resolution=150)
```

然后进行推送：
```bash
rmapi put image.pdf "My Folder/"
```

## 完整工作流程示例

**草图优化流程：**

```bash
# 1. Fetch sketch from tablet
rmapi get "Sketches/MyDrawing"

# 2. Extract and convert to PNG
unzip MyDrawing.rmdoc -d MyDrawing_extracted/
RM_FILE=$(find MyDrawing_extracted -name "*.rm" | head -1)
rmc -t svg -o sketch.svg "$RM_FILE"
python3 -c "import cairosvg; cairosvg.svg2png(url='sketch.svg', write_to='sketch.png', output_width=1404, output_height=1872)"

# 3. [Your AI enhancement step here]
# Example: use any image-to-image AI tool to enhance sketch.png → enhanced.png

# 4. Convert to PDF and push back
python3 -c "from PIL import Image; Image.open('enhanced.png').convert('RGB').save('enhanced.pdf', 'PDF', resolution=150)"
rmapi put enhanced.pdf "Sketches/"
```

## 共享策略

可以在平板上创建一个专用的同步文件夹，或者使用以下方法进行文件管理：
- **标签**：使用`rmapi find --tag`为文件添加标签以便查找。
- **星标**：使用`rmapi find --starred`为重要文件添加星标以便快速访问。

## 注意事项

- **需要云同步**：在文件可用之前，平板必须先与云端同步（可以在平板上手动刷新数据）。
- **文件格式**：`.rmdoc`是一个ZIP文件包，其中包含JSON元数据和`.rm`格式的笔画文件。
- **警告提示**：`rmc`可能会提示有关新格式版本的警告，但通常仍然可以正常使用。
- **显示尺寸**：reMarkable的显示分辨率为1404×1872像素（纵向显示）。
- **文本提取**：对于手写文本，系统使用视觉模型进行解析，而非传统的OCR技术。

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| `rmapi`无法连接** | 重新验证身份：删除`~/.rmapi`文件，然后重新运行`rmapi`。 |
| 上传后文件未找到** | 等待云端同步完成，或手动刷新平板。 |
| `rmc`格式警告**：通常可以忽略这些警告，因为转换仍能正常进行。 |
| SVG文件显示为空** | 确保使用了正确的`.rm`文件（多页笔记本可能包含多个`.rm`文件）。 |