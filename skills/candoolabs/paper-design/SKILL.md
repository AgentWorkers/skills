---
name: paper-design
description: 在 Paper 中设计用户界面（UI）屏幕——这是一款在 macOS 上本地运行的专业设计工具。你可以创建画布（artboards），在设计方案中编写 HTML 代码，截取屏幕截图，并通过视觉方式不断进行迭代（iteration）。
user-invocable: true
metadata: {"openclaw":{"emoji":"🎨","homepage":"https://paper.design","requires":{"bins":["curl","python3"]},"os":["darwin"]}}
---
# Paper设计 — MCP桥接技能

Paper是一款专业的设计工具（类似于Figma），可在macOS上本地运行。此技能通过HTTP连接到Paper的MCP服务器，从而为您提供完整的设计功能。

**先决条件：** Paper必须已打开，并且加载了设计文件。如果Paper未运行，请让用户先打开它。

## 如何使用Paper

所有的Paper操作都通过此技能目录中的`paper.sh`脚本来完成：

```bash
exec {baseDir}/paper.sh <tool_name> '<json_arguments>'
```

**重要提示：** 在传递JSON参数时，请始终使用单引号，以防止shell解析参数。

## 快速入门

```bash
# 1. Check what's on the canvas
exec {baseDir}/paper.sh get_basic_info

# 2. Create a new mobile artboard
exec {baseDir}/paper.sh create_artboard '{"name":"Home Screen","styles":{"width":"390px","height":"844px","display":"flex","flexDirection":"column","backgroundColor":"#FAFAFA"}}'

# 3. Add content (one visual group at a time)
exec {baseDir}/paper.sh write_html '{"html":"<div layer-name=\"Header\" style=\"display:flex;padding:60px 20px 20px;align-items:center\"><span style=\"font-family:Inter Tight;font-size:28px;font-weight:700;color:#1A1A1A\">Home</span></div>","targetNodeId":"ARTBOARD_ID","mode":"insert-children"}'

# 4. Take a screenshot to review
exec {baseDir}/paper.sh get_screenshot '{"nodeId":"ARTBOARD_ID"}'
# → saves to /tmp/paper-screenshots/screenshot-TIMESTAMP.jpg

# 5. View the screenshot
image /tmp/paper-screenshots/screenshot-TIMESTAMP.jpg

# 6. When done, release the working indicator
exec {baseDir}/paper.sh finish_working_on_nodes
```

## 工具参考

### 查看画布内容

| 命令 | 功能 |
|---------|---------|
| `paper.sh get_basic_info` | 获取文件名、页面信息、使用的画布（artboards）和字体信息 |
| `paper.sh get_selection` | 获取画布上当前选中的节点 |
| `paper.sh get_node_info '{"nodeId":"ID"}'` | 获取节点的尺寸、可见性、父节点、子节点及文本信息 |
| `paper.sh get_children '{"nodeId":"ID"}'` | 获取节点的直接子节点及其类型 |
| `paper.sh get_tree_summary '{"nodeId":"ID"}'` | 获取节点的层次结构概览 |
| `paper.sh get_tree_summary '{"nodeId":"ID","depth":5}'` | 获取更详细的层次结构信息 |
| `paper.sh get_computed_styles '{"nodeIds":["ID1","ID2"]}'` | 获取节点的CSS样式 |
| `paper.sh get_jsx '{"nodeId":"ID"}'` | 获取节点的JSX代码（用于开发者交接） |
| `paper.sh get_font_family_info '{"familyNames":["Inter","DM Sans"]}'` | 获取可用的字体及其样式 |

### 查看画布元素

```bash
# Screenshot an artboard or node
exec {baseDir}/paper.sh get_screenshot '{"nodeId":"ARTBOARD_ID"}'

# Higher resolution (for reading small text)
exec {baseDir}/paper.sh get_screenshot '{"nodeId":"ARTBOARD_ID","scale":2}'

# Save to specific path
exec {baseDir}/paper.sh get_screenshot '{"nodeId":"ARTBOARD_ID"}' --save /tmp/my-review.jpg

# Then view the screenshot with the image tool
image /tmp/paper-screenshots/screenshot-TIMESTAMP.jpg
```

### 创建设计

```bash
# Create artboard (mobile)
exec {baseDir}/paper.sh create_artboard '{"name":"Screen Name","styles":{"width":"390px","height":"844px","display":"flex","flexDirection":"column","backgroundColor":"#FFFFFF"}}'

# Create artboard (desktop)
exec {baseDir}/paper.sh create_artboard '{"name":"Dashboard","styles":{"width":"1440px","height":"900px","display":"flex","flexDirection":"column","backgroundColor":"#F5F5F5"}}'

# Create related artboard (positioned next to existing)
exec {baseDir}/paper.sh create_artboard '{"name":"Screen V2","relatedNodeId":"EXISTING_ID","styles":{"width":"390px","height":"844px"}}'
```

### 将HTML代码写入设计中

```bash
# Add elements as children of a node
exec {baseDir}/paper.sh write_html '{"html":"<div style=\"...\">content</div>","targetNodeId":"PARENT_ID","mode":"insert-children"}'

# Replace an existing node
exec {baseDir}/paper.sh write_html '{"html":"<div style=\"...\">new content</div>","targetNodeId":"OLD_NODE_ID","mode":"replace"}'
```

**HTML编写规则（非常重要）：**
- 始终使用内联样式（`style="..."`）
- 所有布局都应使用`display: flex`；避免使用网格（grid）、内联样式（inline）或表格（tables）
- 使用`padding`和`gap`来设置元素间距；不要使用`margin`
- 不要将表情符号（emojis）用作图标，而应使用SVG路径
- 为关键元素设置`layer-name`属性（例如：“Semantic Name”）
- 可通过`font-family: "Font Name"`来使用Google Fonts字体
- 字体大小必须使用`px`单位
- 假设元素的边界盒（border-box）尺寸符合标准规格

### 修改现有设计

```bash
# Update styles on nodes
exec {baseDir}/paper.sh update_styles '{"updates":[{"nodeIds":["ID1","ID2"],"styles":{"backgroundColor":"#FF0000","padding":"20px"}}]}'

# Change text content
exec {baseDir}/paper.sh set_text_content '{"updates":[{"nodeId":"TEXT_ID","textContent":"New text here"}]}'

# Duplicate nodes (efficient for repeated elements)
exec {baseDir}/paper.sh duplicate_nodes '{"nodes":[{"id":"SOURCE_ID"}]}'
# With specific parent:
exec {baseDir}/paper.sh duplicate_nodes '{"nodes":[{"id":"SOURCE_ID","parentId":"TARGET_PARENT"}]}'

# Delete nodes
exec {baseDir}/paper.sh delete_nodes '{"nodeIds":["ID1","ID2"]}'

# Rename layers
exec {baseDir}/paper.sh rename_nodes '{"updates":[{"nodeId":"ID","name":"Header"}]}'
```

### 完成设计

```bash
# ALWAYS call when done with an artboard — releases the working indicator
exec {baseDir}/paper.sh finish_working_on_nodes
```

## 设计工作流程（必填步骤）：

1. **开始**：使用`get_basic_info`查看画布上的内容。
2. **检查字体**：在编写任何文本之前，使用`get_font_family_info`获取可用的字体信息。
3. **设计规划**：在编写HTML之前，确定颜色方案（5-6种十六进制颜色）、字体选择、间距布局和视觉方向。
4. **逐步构建设计**：每次调用`write_html`时只创建一个视觉元素组（例如标题、行或按钮组，而不是整个页面）。
5. **每进行2-3次修改后进行检查**：使用`get_screenshot`生成截图，然后分析间距、字体、对比度、对齐方式和内容裁剪情况。
6. **修复问题**：在继续下一步之前，确保所有问题都得到解决。
7. **完成设计**：完成所有修改后，使用`finish_working_on_nodes`命令。

## 定期检查（每进行2-3次修改后）：

在每次修改后，检查以下内容：
- **间距**：元素之间的间距是否均匀？是否存在拥挤的情况？整体布局的节奏是否清晰？
- **字体**：文本是否易于阅读？层次结构是否清晰？
- **对比度**：文本的对比度是否足够高？不同元素之间的区分度是否明显？
- **对齐方式**：元素的垂直/水平对齐是否一致？
- **内容裁剪**：内容是否在页面边缘被裁剪？

## 默认画布尺寸

| 设备 | 宽度 | 高度 |
|--------|-------|--------|
| 移动设备（iPhone） | 390px | 844px |
| 平板电脑（iPad） | 768px | 1024px |
| 桌面电脑 | 1440px | 900px |

## 故障排除：

- **“Paper未运行”**：请先在macOS上打开Paper应用程序。
- **“初始化MCP会话失败”**：确保Paper已加载了设计文件（而不仅仅是应用程序本身）。
- **返回空响应**：可能是节点ID错误，请使用`get_basic_info`获取有效的节点ID。
- **会话过期**：脚本会自动尝试重新连接；如果问题持续存在，请删除`/tmp/paper-mcp-session`文件。