---
name: excalidraw-diagram-generator
description: '根据自然语言描述生成 Excalidraw 图表。适用于以下场景：创建图表（create a diagram）、制作流程图（make a flowchart）、可视化流程（visualize a process）、绘制系统架构图（draw a system architecture diagram）或生成 Excalidraw 文件（generate an Excalidraw file）。支持流程图、关系图、思维导图（mind map）和系统架构图。输出格式为 .excalidraw JSON 文件，可直接在 Excalidraw 软件中打开。'
---
# Excalidraw 图表生成器

这是一项能够根据自然语言描述生成 Excalidraw 格式图表的技能。它可以帮助用户无需手动绘图，即可创建流程、系统、关系和想法的可视化表示。

## 何时使用此技能

当用户请求以下内容时，请使用此技能：
- “创建一个展示……的图表”
- “为……制作流程图”
- “可视化……的过程”
- “绘制……的系统架构”
- “生成关于……的思维导图”
- “为……创建一个 Excalidraw 文件”
- “展示……之间的关系”
- “绘制……的工作流程图”

**支持的图表类型：**
- 📊 **流程图**：顺序流程、工作流程、决策树
- 🔗 **关系图**：实体关系、系统组件、依赖关系
- 🧠 **思维导图**：概念层次结构、头脑风暴结果、主题组织
- 🏗️ **架构图**：系统设计、模块交互、数据流
- 📈 **数据流图 (DFD)**：数据流可视化、数据转换过程
- 🏊 **业务流程图 (Swimlane)**：跨职能工作流程、基于角色的流程
- 📦 **类图**：面向对象设计、类结构和关系
- 🔄 **序列图**：对象随时间的交互、消息流
- 🗃️ **ER 图**：数据库实体关系、数据模型

## 先决条件

- 对要可视化的内容有清晰描述
- 确定关键实体、步骤或概念
- 理解元素之间的关系或流程

## 逐步工作流程

### 第一步：理解请求

分析用户的描述，以确定：
1. **图表类型**（流程图、关系图、思维导图、架构图）
2. **关键元素**（实体、步骤、概念）
3. **关系**（流程、连接、层次结构）
4. **复杂性**（元素数量）

### 第二步：选择合适的图表类型

| 用户意图 | 图表类型 | 示例关键词 |
|-------------|--------------|------------------|
| 流程、步骤、程序 | **流程图** | “工作流程”、“过程”、“步骤”、“程序” |
| 连接、依赖关系、关联 | **关系图** | “关系”、“连接”、“依赖关系”、“结构” |
| 概念层次结构、头脑风暴 | **思维导图** | “思维导图”、“概念”、“想法”、“分解” |
| 系统设计、组件 | **架构图** | “架构”、“系统”、“组件”、“模块” |
| 数据流、转换过程 | **数据流图 (DFD)** | “数据流”、“数据处理”、“数据转换” |
| 跨职能流程、角色职责 | **业务流程图 (Swimlane)** | “业务流程”、“泳道”、“角色”、“职责” |
| 面向对象设计、类结构 | **类图** | “类”、“继承”、“OOP”、“对象模型” |
| 交互序列、消息流 | **序列图** | “序列”、“交互”、“消息”、“时间线” |
| 数据库设计、实体关系 | **ER 图** | “数据库”、“实体”、“关系”、“数据模型” |

### 第三步：提取结构化信息

**对于流程图：**
- 顺序步骤列表
- 决策点（如果有）
- 起点和终点

**对于关系图：**
- 实体/节点（名称 + 可选描述）
- 实体之间的关系（从 → 到，带标签）

**对于思维导图：**
- 中心主题
- 主要分支（建议 3-6 个）
- 每个分支的子主题（可选）

**对于数据流图 (DFD)：**
- 数据来源和目的地（外部实体）
- 过程（数据转换）
- 数据存储（数据库、文件）
- 数据流（从左到右或从左上到右下的箭头）
- **注意**：仅表示数据流，不表示流程顺序

**对于业务流程图 (Swimlane)：**
- 行动者/角色（部门、系统、人员） - 显示为标题列
- 流程泳道（每个行动者下方的垂直泳道）
- 流程框（每个泳道内的活动）
- 流程箭头（连接流程框，包括跨泳道的交接）

**对于类图：**
- 带名称的类
- 属性及其可见性（+、-、#）
- 方法及其可见性和参数
- 关系：继承（实线 + 白色三角形）、实现（虚线 + 白色三角形）、关联（实线）、依赖（虚线）、聚合（实线 + 白色菱形）、组合（实线 + 实心菱形）
- 多重性表示（1、0..1、1..*）

### 第四步：生成 Excalidraw JSON

创建包含适当元素的 `.excalidraw` 文件：

**可用的元素类型：**
- `rectangle`：用于实体、步骤、概念的框
- `ellipse`：用于强调的替代形状
- `diamond`：决策点
- `arrow`：方向性连接
- `text`：标签和注释

**需要设置的关键属性：**
- **位置**：`x`、`y` 坐标
- **大小**：`width`、`height`
- **样式**：`strokeColor`、`backgroundColor`、`fillStyle`
- **字体**：`fontFamily: 5`（Excalifont - **所有文本元素都必须使用**）
- **文本**：用于标签的嵌入文本
- **连接**：用于箭头的 `points` 数组

**重要提示**：所有文本元素必须使用 `fontFamily: 5`（Excalifont），以保持一致的视觉效果。

### 第五步：格式化输出

组织完整的 Excalidraw 文件：

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [
    // Array of diagram elements
  ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": 20
  },
  "files": {}
}
```

### 第六步：保存并提供说明

1. 保存为 `<描述性名称>.excalidraw`
2. 告知用户如何打开文件：
   - 访问 https://excalidraw.com
   - 点击“打开”或拖放文件
   - 或使用 Excalidraw VS Code 扩展程序

## 最佳实践

### 元素数量指南

| 图表类型 | 推荐数量 | 最大数量 |
|--------------|-------------------|---------|
| 流程图步骤 | 3-10 | 15 |
| 关系图实体 | 3-8 | 12 |
| 思维导图分支 | 4-6 | 8 |
| 每个分支的思维导图子主题 | 2-4 | 6 |

### 布局技巧

1. **起始位置**：将重要元素居中，保持一致的间距
2. **间距**：
   - 元素之间的水平间距：200-300px
   - 行之间的垂直间距：100-150px
3. **颜色**：使用一致的颜色方案
   - 主要元素：浅蓝色（`#a5d8ff`
   - 次要元素：浅绿色（`#b2f2bb`
   - 重要/中心元素：黄色（`#ffd43b`
   - 警告/提示：浅红色（`#ffc9c9`
4. **文本大小**：16-24px 以便阅读
5. **字体**：始终对所有文本元素使用 `fontFamily: 5`（Excalifont）
6. **箭头样式**：简单流程使用直线箭头，复杂关系使用曲线箭头

### 复杂性管理

**如果用户请求的元素太多：**
- 建议分成多个图表
- 先关注主要元素
- 提供创建详细子图表的选项

**示例响应：**
```
"Your request includes 15 components. For clarity, I recommend:
1. High-level architecture diagram (6 main components)
2. Detailed diagram for each subsystem

Would you like me to start with the high-level view?"
```

## 示例提示和响应

### 示例 1：简单流程图

**用户：**“创建一个用户注册的流程图”

**代理生成：**
1. 提取步骤：“输入电子邮件” → “验证电子邮件” → “设置密码” → “完成”
2. 创建包含 4 个矩形和 3 个箭头的流程图
3. 保存为 `user-registration-flow.excalidraw`

### 示例 2：关系图

**用户：**“绘制 User、Post 和 Comment 实体之间的关系图”

**代理生成：**
1. 实体：User、Post、Comment
2. 关系：User → Post (“创建”), User → Comment (“写入”), Post → Comment (“包含”
3. 保存为 `user-content-relationships.excalidraw`

### 示例 3：思维导图

**用户：**“关于机器学习概念的思维导图”

**代理生成：**
1. 中心：**机器学习**
2. 分支：监督学习、无监督学习、强化学习、深度学习
3. 每个分支下的子主题
4. 保存为 `machine-learning-mindmap.excalidraw`

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 元素重叠 | 增加坐标之间的间距 |
| 文本无法放入框内 | 增加框的宽度或减小字体大小 |
| 元素太多 | 分成多个图表 |
| 布局不清晰 | 使用网格布局（对于关系图）或辐射布局（对于思维导图） |
| 颜色不一致 | 根据元素类型提前定义颜色方案 |

## 高级技巧

### 网格布局（用于关系图）
```javascript
const columns = Math.ceil(Math.sqrt(entityCount));
const x = startX + (index % columns) * horizontalGap;
const y = startY + Math.floor(index / columns) * verticalGap;
```

### 辐射布局（用于思维导图）
```javascript
const angle = (2 * Math.PI * index) / branchCount;
const x = centerX + radius * Math.cos(angle);
const y = centerY + radius * Math.sin(angle);
```

### 自动生成的 ID

使用时间戳 + 随机字符串生成唯一 ID：
```javascript
const id = Date.now().toString(36) + Math.random().toString(36).substr(2);
```

## 输出格式

始终提供：
1. ✅ 完整的 `.excalidraw` JSON 文件
2. 📊 创建内容的总结
3. 📝 元素数量
4. 💡 打开/编辑的说明

**示例总结：**
```
Created: user-workflow.excalidraw
Type: Flowchart
Elements: 7 rectangles, 6 arrows, 1 title text
Total: 14 elements

To view:
1. Visit https://excalidraw.com
2. Drag and drop user-workflow.excalidraw
3. Or use File → Open in Excalidraw VS Code extension
```

## 验证清单

在交付图表之前：
- [ ] 所有元素都有唯一的 ID
- [ ] 坐标不会重叠
- [ ] 文本可读（字体大小 16+）
- [ ] **所有文本元素都使用 `fontFamily: 5`（Excalifont）**
- [ ] 箭头逻辑连接正确
- [ ] 颜色遵循一致的风格
- [ ] 文件是有效的 JSON
- [ ] 元素数量合理（<20 个以确保清晰）

## 图标库（可选增强）

对于专门的图表（例如 AWS/GCP/Azure 架构图），可以使用 Excalidraw 提供的预制作图标库。这可以提供专业的、标准化的图标，而不是基本形状。

### 当用户请求图标时

**如果用户请求 AWS/云架构图或提到希望使用特定图标：**

1. **检查库是否存在**：查找 `libraries/<库名称>/reference.md`
2. **如果库存在**：继续使用图标（参见下面的 AI Assistant 工作流程）
3. **如果库不存在**：提供设置说明：

**用户设置说明（详细）**

**步骤 1：创建库目录**
```bash
mkdir -p skills/excalidraw-diagram-generator/libraries/aws-architecture-icons
```

**步骤 2：下载库**
- 访问：https://libraries.excalidraw.com/
- 搜索所需的图标集（例如，“AWS 架构图标”）
- 点击下载以获取 `.excalidrawlib` 文件
- 示例类别（可用性可能有所不同；请在网站上确认）：
   - 云服务图标
   - UI/材料图标
   - 流程图符号

**步骤 3：放置库文件**
- 将下载的文件重命名为与目录名称匹配的名称（例如，`aws-architecture-icons.excalidrawlib`）
- 将其移动到步骤 1 中创建的目录中

**步骤 4：运行分割脚本**
```bash
python skills/excalidraw-diagram-generator/scripts/split-excalidraw-library.py skills/excalidraw-diagram-generator/libraries/aws-architecture-icons/
```

**步骤 5：验证设置**
运行脚本后，验证以下结构是否存在：
```
skills/excalidraw-diagram-generator/libraries/aws-architecture-icons/
  aws-architecture-icons.excalidrawlib  (original)
  reference.md                          (generated - icon lookup table)
  icons/                                (generated - individual icon files)
    API-Gateway.json
    CloudFront.json
    EC2.json
    Lambda.json
    RDS.json
    S3.json
    ...
```

### AI Assistant 工作流程

**当 `libraries/` 中有图标库时：**

**推荐方法：使用 Python 脚本（高效且可靠）**

该仓库包含自动处理图标集成的 Python 脚本：

1. **创建基础图表结构**：
   - 创建包含基本布局（标题、框、区域）的 `.excalidraw` 文件
   - 这建立了画布和整体结构

2. **使用 Python 脚本添加图标**：
   ```bash
   python skills/excalidraw-diagram-generator/scripts/add-icon-to-diagram.py \
     <diagram-path> <icon-name> <x> <y> [--label "Text"] [--library-path PATH]
   ```
   - 默认情况下，`.excalidraw.edit` 是启用的，以避免覆盖问题；可以通过传递 `--no-use-edit-suffix` 来禁用。

   **示例**：
   ```bash
   # Add EC2 icon at position (400, 300) with label
   python scripts/add-icon-to-diagram.py diagram.excalidraw EC2 400 300 --label "Web Server"
   
   # Add VPC icon at position (200, 150)
   python scripts/add-icon-to-diagram.py diagram.excalidraw VPC 200 150
   
   # Add icon from different library
   python scripts/add-icon-to-diagram.py diagram.excalidraw Compute-Engine 500 200 \
     --library-path libraries/gcp-icons --label "API Server"
   ```

3. **添加连接箭头**：
   ```bash
   python skills/excalidraw-diagram-generator/scripts/add-arrow.py \
     <diagram-path> <from-x> <from-y> <to-x> <to-y> [--label "Text"] [--style solid|dashed|dotted] [--color HEX]
   ```
   - 默认情况下，`.excalidraw.edit` 是启用的，以避免覆盖问题；可以通过传递 `--no-use-edit-suffix` 来禁用。

   **示例**：
   ```bash
   # Simple arrow from (300, 250) to (500, 300)
   python scripts/add-arrow.py diagram.excalidraw 300 250 500 300
   
   # Arrow with label
   python scripts/add-arrow.py diagram.excalidraw 300 250 500 300 --label "HTTPS"
   
   # Dashed arrow with custom color
   python scripts/add-arrow.py diagram.excalidraw 400 350 600 400 --style dashed --color "#7950f2"
   ```

4. **工作流程总结**：
   ```bash
   # Step 1: Create base diagram with title and structure
   # (Create .excalidraw file with initial elements)
   
   # Step 2: Add icons with labels
   python scripts/add-icon-to-diagram.py my-diagram.excalidraw "Internet-gateway" 200 150 --label "Internet Gateway"
   python scripts/add-icon-to-diagram.py my-diagram.excalidraw VPC 250 250
   python scripts/add-icon-to-diagram.py my-diagram.excalidraw ELB 350 300 --label "Load Balancer"
   python scripts/add-icon-to-diagram.py my-diagram.excalidraw EC2 450 350 --label "EC2 Instance"
   python scripts/add-icon-to-diagram.py my-diagram.excalidraw RDS 550 400 --label "Database"
   
   # Step 3: Add connecting arrows
   python scripts/add-arrow.py my-diagram.excalidraw 250 200 300 250  # Internet → VPC
   python scripts/add-arrow.py my-diagram.excalidraw 300 300 400 300  # VPC → ELB
   python scripts/add-arrow.py my-diagram.excalidraw 400 330 500 350  # ELB → EC2
   python scripts/add-arrow.py my-diagram.excalidraw 500 380 600 400  # EC2 → RDS
   ```

**Python 脚本方法的优势**：
- ✅ **不消耗令牌**：图标 JSON 数据（每个 200-1000 行）永远不会进入 AI 环境
- ✅ **精确的转换**：坐标计算是确定性的
- ✅ **ID 管理**：自动生成的 UUID 可防止冲突
- ✅ **可靠**：没有坐标计算错误或 ID 冲突的风险
- ✅ **快速**：直接操作文件，无需解析开销
- ✅ **可重用**：适用于您提供的任何 Excalidraw 库

**替代方案：手动图标集成（不推荐）**

仅在 Python 脚本不可用时使用：

1. **检查库**：
   ```
   List directory: skills/excalidraw-diagram-generator/libraries/
   Look for subdirectories containing reference.md files
   ```

2. **阅读 reference.md**：
   ```
   Open: libraries/<library-name>/reference.md
   This is lightweight (typically <300 lines) and lists all available icons
   ```

3. **查找相关图标**：
   ```
   Search the reference.md table for icon names matching diagram needs
   Example: For AWS diagram with EC2, S3, Lambda → Find "EC2", "S3", "Lambda" in table
   ```

4. **加载特定图标数据**（警告：文件较大）：
   ```
   Read ONLY the needed icon files:
   - libraries/aws-architecture-icons/icons/EC2.json (200-300 lines)
   - libraries/aws-architecture-icons/icons/S3.json (200-300 lines)
   - libraries/aws-architecture-icons/icons/Lambda.json (200-300 lines)
   Note: Each icon file is 200-1000 lines - this consumes significant tokens
   ```

5. **提取和转换元素**：
   ```
   Each icon JSON contains an "elements" array
   Calculate bounding box (min_x, min_y, max_x, max_y)
   Apply offset to all x/y coordinates
   Generate new unique IDs for all elements
   Update groupIds references
   Copy transformed elements into your diagram
   ```

6. **定位图标并添加连接**：
   ```
   Adjust x/y coordinates to position icons correctly in the diagram
   Update IDs to ensure uniqueness across diagram
   Add connecting arrows and labels as needed
   ```

**手动集成的挑战**：
- ⚠️ 高令牌消耗（每个图标 200-1000 行）
- ⚠️ 复杂的坐标转换计算
- ⚠️ 如果处理不当，可能会有 ID 冲突的风险
- ⚠️ 对于包含许多图标的图表，耗时较长

### 示例：使用图标创建 AWS 图表

**请求**：“创建一个包含 Internet Gateway、VPC、ELB、EC2 和 RDS 的 AWS 架构图”

**推荐的工作流程（使用 Python 脚本）：**
**请求**：“创建一个包含 Internet Gateway、VPC、ELB、EC2 和 RDS 的 AWS 架构图”

**推荐的工作流程（使用 Python 脚本）：**

```bash
# Step 1: Create base diagram file with title
# Create my-aws-diagram.excalidraw with basic structure (title, etc.)

# Step 2: Check icon availability
# Read: libraries/aws-architecture-icons/reference.md
# Confirm icons exist: Internet-gateway, VPC, ELB, EC2, RDS

# Step 3: Add icons with Python script
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw "Internet-gateway" 150 100 --label "Internet Gateway"
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw VPC 200 200
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw ELB 350 250 --label "Load Balancer"
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw EC2 500 300 --label "Web Server"
python scripts/add-icon-to-diagram.py my-aws-diagram.excalidraw RDS 650 350 --label "Database"

# Step 4: Add connecting arrows
python scripts/add-arrow.py my-aws-diagram.excalidraw 200 150 250 200  # Internet → VPC
python scripts/add-arrow.py my-aws-diagram.excalidraw 265 230 350 250  # VPC → ELB
python scripts/add-arrow.py my-aws-diagram.excalidraw 415 280 500 300  # ELB → EC2
python scripts/add-arrow.py my-aws-diagram.excalidraw 565 330 650 350 --label "SQL" --style dashed

# Result: Complete diagram with professional AWS icons, labels, and connections
```

**优势**：
- 不需要手动计算坐标
- 不消耗图标数据的令牌
- 结果确定且可靠
- 容易迭代和调整位置

**替代工作流程（手动，如果脚本不可用）：**
1. 检查：`libraries/aws-architecture-icons/reference.md` 是否存在 → 是
2. 阅读 reference.md → 找到 Internet-gateway、VPC、ELB、EC2、RDS 的条目
3. 加载：
   - `icons/Internet-gateway.json`（298 行）
   - `icons/VPC.json`（550 行）
   - `icons/ELB.json`（363 行）
   - `icons/EC2.json`（231 行）
   - `icons/RDS.json`（大小类似）
   **总共：约 2000+ 行的 JSON 需要处理**
4. 从每个 JSON 文件中提取元素
5. 计算每个图标的边界框和偏移量
6. 转换所有坐标（x, y）以进行定位
7. 为所有元素生成唯一 ID
8. 添加显示数据流的箭头
9. 添加文本标签
10. 生成最终的 `.excalidraw` 文件

**手动方法的挑战**：
- 高令牌消耗（约 2000-5000 行）
- 复杂的坐标计算
- 如果处理不当，可能会有 ID 冲突的风险

### 支持的图标库（示例 — 请验证可用性）

- 该工作流程适用于您提供的任何有效的 `.excalidrawlib` 文件。
- 您可以在 https://libraries.excalidraw.com/ 上找到的一些库类别示例：
   - 云服务图标
   - Kubernetes / 基础设施图标
   - UI / 材料图标
   - 流程图 / 图表符号
   - 网络图图标
- 可用性和名称可能会更改；在使用前请在网站上确认库的名称。

### 备用方案：没有图标库

**如果没有设置图标库：**
- 使用基本形状（矩形、椭圆、箭头）创建图表
- 使用颜色编码和文本标签来区分组件
- 告知用户他们可以稍后添加图标或为未来的图表设置库
- 图表仍然可以正常使用，只是视觉效果不够精致

## 参考资料

请参阅以下参考资料：
- `references/excalidraw-schema.md` - 完整的 Excalidraw JSON 架构
- `references/element-types.md` - 详细的元素类型规范
- `templates/flowchart-template.json` - 基本流程图模板
- `templates/relationship-template.json` - 关系图模板
- `templates/mindmap-template.json` - 思维导图模板
- `scripts/split-excalidraw-library.py` - 用于分割 `.excalidrawlib` 文件的工具
- `scripts/README.md` - 图标库工具的文档
- `scripts/.gitignore` - 避免提交本地 Python 生成的资源

## 限制

- 复杂的曲线被简化为直线/基本曲线
- 手绘图形的粗糙度设置为默认值（1）
- 自动生成时不支持嵌入图像
- 每个图表的最大推荐元素数量为 20 个
- 没有自动碰撞检测（请使用间距指南）

## 未来改进

潜在的改进：
- 自动布局优化算法
- 支持从 Mermaid/PlantUML 语法导入
- 扩展模板库
- 生成后的交互式编辑