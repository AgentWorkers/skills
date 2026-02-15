---
name: terminal-ui-design-system
description: 创建具有终端风格的UI界面，采用macOS风格的窗口装饰、等宽字体（monospace typography）以及温暖的色彩调色板。这种技能适用于开发工具、代码市场、技术文档网站，或任何需要终端/命令行美感的界面设计。提供完整的设计系统规范，包括色彩调色板、字体样式、间距设置、组件设计以及CSS实现细节。
---

# 终端用户界面设计系统

这是一个全面的设计系统，用于创建具有 macOS 风格窗口装饰、等宽字体和温暖、对开发者友好的颜色调性的终端风格用户界面。该设计系统专为开发工具、代码市场、技术文档以及任何受益于命令行美学的界面而优化。

## 设计理念

**核心原则：**
- **终端美学**：模仿 macOS 终端窗口，使用彩色圆点、等宽字体和命令行语法。
- **以开发者为中心**：使用语法高亮颜色、类似代码的结构和终端隐喻。
- **温暖且易于接近**：使用温暖的赤褐色 (#cc7a60) 作为主色调，营造出友好且不令人生畏的感觉。
- **高对比度**：通过明显的文本颜色和背景实现清晰的视觉层次结构。
- **功能性与美感并重**：每个设计元素都有其用途，同时保持视觉吸引力。

## 颜色系统

### 主要调色板

**主要品牌颜色：**
- `--primary: #cc7a60` - 温暖的赤褐色/橙棕色，用于主要操作、强调和高亮部分。
- `--primary-foreground: #fff` - 主要背景上的白色文本。
- `--primary-dark: #b56850` - 鼠标悬停状态时的深色调。
- `--primary-light: #d8907a` - 微妙强调时的浅色调。
- `--ring: #cc7a60` - 焦点环颜色（与主要颜色相同）。

**温暖色调：**
- `--warm-red: #c85a3f` - 用于代码块边框和温暖色调的强调。

### 语义颜色

**背景：**
- `--background: #fff` - 纯白色，用于主要背景。
- `--bg-main: #f8f8f8` - 浅灰色，用于页面背景（带有微妙的网格图案）。
- `--bg-card: #fff` - 白色，用于卡片组件。
- `--bg-code: #fafafa` - 非常浅的灰色，用于代码块和窗口标题。
- `--secondary: #f9fafb` - 浅灰色，用于次要背景。
- `--muted: #f3f4f6` - 淡灰色，用于较不重要的背景。

**文本颜色：**
- `--foreground: #111827` - 接近黑色的主要文本（易于阅读）。
- `--text-primary: #111827` - 主要文本颜色。
- `--text-secondary: #666666` - 中等灰色，用于次要文本。
- `--text-muted: #5b6370` - 较不重要的文本的淡灰色背景。
- `--muted-foreground: #5b6370` - 淡灰色背景上的主要文本。

**边框：**
- `--border: #8b929e` - 中等灰色，用于主要边框。
- `--border-light: #e5e7eb` - 浅灰色，用于细微的分隔线。
- `--input: #8b929e` - 输入框边框颜色。

**状态颜色：**
- `--success: #22c55e` - 绿色，表示成功状态。
- `--warning: #f59e0b` - 琥珀色，表示警告。
- `--danger: #ef4444` - 红色，表示错误/破坏性操作。
- `--accent: #f59e0b` - 琥珀色强调色。

### 语法高亮颜色

**代码语法：**
- `--syntax-keyword: #cc7a60` - 关键字的主要颜色（如 const、export 等）。
- `--syntax-string: #22c55e` - 字符串的绿色。
- `--syntax-number: #cc7a60` - 数字的主要颜色。
- `--syntax-comment: #6a9955` - 评论的淡绿色。
- `--syntax-function: #dcdcaa` - 函数名称的浅黄色。

**命令前缀：**
- 命令前缀（`$`）使用荧光绿色：`#39ff14` - 以营造终端风格。

**代码元素：**
- `--text-comment: #6a9955` - 评论文本的颜色。

### macOS 窗口圆点

**终端窗口控件：**
- `--dot-red: #ff5f57` - 关闭按钮（macOS 红色）。
- `--dot-yellow: #febc2e` - 最小化按钮（macOS 黄色）。
- `--dot-green: #28c840` - 最大化按钮（macOS 绿色）。

### 颜色使用指南**

**主要颜色 (#cc7a60) 的使用：**
- 导航中的命令关键字。
- 提示符号（`>`）。
- 活动状态和高亮部分。
- 焦点环。
- 活动时的主要按钮。
- 图表线条和数据可视化。

**荧光绿色 (#39ff14) 的使用：**
- 命令前缀（`$`） - 以营造真实的终端感觉。
- 仅用于美元符号，不得用于其他元素。

**绿色 (#22c55e) 的使用：**
- 成功指示器。
- 状态圆点（在线/准备就绪）。
- 代码中的字符串字面量。
- 正面操作。

**蓝色 (#3b82f6) 的使用：**
- 命令关键字（cd、watch、man、api）。
- 代码关键字（const、let、var）。
- 链接和交互元素。

## 字体系统

### 字体系列

**主要字体堆栈：**
```css
--font-mono: "JetBrains Mono", "JetBrains Mono Fallback", 'Fira Code', 'Consolas', monospace;
```
- **Primary**: JetBrains Mono（400-800 粗细）
- **备用字体**: Fira Code、Consolas、系统等宽字体
- 用于：所有 UI 文本、导航、按钮、代码块。

**无衬线备用字体：**
```css
--font-sans: ui-sans-serif, system-ui, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
```
- 仅作为备用，优先使用等宽字体。

### 字体大小比例

**基本单位系统：**
- `--text-xs: 0.75rem` (12px) - 小标签、提示、窗口状态。
- `--text-sm: 0.875rem` (14px) - 次要文本、描述。
- `--text-base: 1rem` (16px) - 正文文本，默认大小。
- `--text-lg: 1.125rem` (18px) - 稍加强调的文本。
- `--text-xl: 1.25rem` (20px) - 标题。
- `--text-2xl: 1.5rem` (24px) - 大标题。
- `--text-3xl: 1.875rem` (30px) - 大数字、统计数据。
- `--text-4xl: 2.25rem` (36px) - 特大标题。
- `--text-5xl: 3rem` (48px) - 特大标题。
- `--text-6xl: 3.75rem` (60px) - 超大标题。

**字体粗细：**
- `--font-weight-normal: 400` - 正文文本。
- `--font-weight-medium: 500` - 中等强调。
- `--font-weight-semibold: 600` - 粗体（关键字、标签）。
- `--font-weight-bold: 700` - 粗体（标题、重要文本）。
- `--font-weight-extrabold: 800` - 特粗体（标题文本）。

**行高：**
- `--leading-tight: 1.25` - 标题的紧密间距。
- `--leading-relaxed: 1.625` - 正文文本的宽松间距。

### 字体使用**

**标题：**
- 标题：3.5rem，粗细 700，行高 1.1。
- 部分标题：2.5rem，粗细 700。
- 常见问题标题：2rem，粗细 700。

**正文文本：**
- 默认：1rem，粗细 400，行高 1.5。
- 次要文本：0.875rem，颜色 `--text-secondary`。
- 淡色文本：0.75rem，颜色 `--text-muted`。

**代码/命令文本：**
- 始终使用等宽字体。
- 命令前缀：荧光绿色 (#39ff14)。
- 关键字：主要颜色 (#cc7a60) 或蓝色 (#3b82f6)。
- 标志/参数：默认前景颜色。

## 间距系统

**基本单位：`--spacing: 0.25rem` (4px)**

**间距比例：**
- `--spacing-xs: 4px` (0.25rem) - 紧密间距，图标内边距。
- `--spacing-sm: 8px` (0.5rem) - 小间隙，按钮内边距。
- `--spacing-md: 16px` (1rem) - 标准间距，卡片内边距。
- `--spacing-lg: 24px` (1.5rem) - 大间隙，部分间距。
- `--spacing-xl: 32px` (2rem) - 特大间隙，主要部分。
- `--spacing-2xl: 48px` (3rem) - 最大间距，页面部分。

**使用指南：**
- 使用一致的间距倍数（以 4px 为基准）。
- 卡片内边距：`--spacing-md` 至 `--spacing-lg`。
- 部分边距：`--spacing-xl` 至 `--spacing-2xl`。
- 按钮内边距：`--spacing-sm` 至 `--spacing-md`。
- 相关元素之间的间距：`--spacing-sm` 至 `--spacing-md`。

## 边框半径系统

**半径比例：**
- `--radius-xs: 2px` (0.125rem) - 最小圆角。
- `--radius-sm: 4px` (0.25rem) - 小元素。
- `--radius-md: 6px` (0.375rem) - 按钮、输入框。
- `--radius-lg: 8px` (0.5rem) - 卡片、窗口（最常见）。
- `--radius-xl: 12px` (1rem) - 特大元素。
- `--radius-2xl: 16px` (1rem) - 特大元素。
- `--radius: 10px` (0.625rem) - 默认半径。

**使用：**
- 终端窗口：`--radius-lg` (8px)。
- 按钮：`--radius-lg` (8px)。
- 卡片：`--radius-lg` (8px)。
- 输入框：`--radius-md` (6px)。
- 头像：`9999px`（完全圆角）。

## 阴影系统**

**阴影比例：**
- `--shadow-sm: 0 1px 2px rgba(0,0,0,0.05)` - 微妙的凸起效果。
- `--shadow-md: 0 4px 6px rgba(0,0,0,0.07)` - 中等凸起效果（卡片悬停时）。
- `--shadow-lg: 0 10px 25px rgba(0,0,0,0.1)` - 大凸起效果（浮动按钮）。

**使用：**
- 默认卡片：`--shadow-sm`。
- 悬停状态：`--shadow-md`。
- 浮动元素：`--shadow-lg`。
- 主要颜色的阴影：`rgba(204, 122, 96, 0.1)`（用于主要主题元素）。

## 组件规范

### 终端窗口组件

**结构：**
```html
<div class="terminal-window">
  <div class="window-header">
    <div class="window-dots">
      <span class="dot red"></span>
      <span class="dot yellow"></span>
      <span class="dot green"></span>
    </div>
    <span class="window-title">filename.ext</span>
    <span class="window-status">ready</span>
  </div>
  <div class="window-content">
    <!-- Content -->
  </div>
</div>
```

**样式：**
- 背景：`--bg-card` (#fff)`。
- 边框：`1px solid --border` (#8b929e)`。
- 边框半径：`--radius-lg` (8px)`。
- 卡片阴影：`--shadow-sm`。
- 标题背景：`--bg-code` (#fafafa)`。
- 标题底部边框：`1px solid --border-light` (#e5e7eb)`。
- 标题内边距：`--spacing-sm --spacing-md` (8px 16px)`。
- 内容内边距：`--spacing-lg` (24px)`。

**窗口圆点：**
- 大小：`12px × 12px`。
- 间距：`6px`。
- 颜色：红色 (#ff5f57)、黄色 (#febc2e)、绿色 (#28c840)。
- 完全圆角（边框半径：50%）。

**窗口标题：**
- 字体大小：`0.85rem`。
- 颜色：`--text-secondary` (#666666)`。
- 字体：等宽字体。

**窗口状态：**
- 字体大小：`0.75rem`。
- 颜色：`--text-muted` (#5b6370)`。
- 位置：标题右侧。

### 导航栏**

**结构：**
```html
<nav class="navbar">
  <div class="navbar-container">
    <div class="navbar-content">
      <!-- Logo, commands, actions -->
    </div>
  </div>
</nav>
```

**样式：**
- 位置：`sticky`，`top: 0`。
- 背景：`rgba(255, 255, 255, 0.8)`，带 `backdrop-filter: blur(8px)`。
- 下边框：`1px solid --border`。
- 高度：`64px`（桌面），`56px`（移动设备）。
- 最大宽度：`80rem`（1280px），居中显示。

**Logo：**
- 状态指示器：绿色圆点（8px）+ “ready” 文本。
- 路径前缀：`~/`，颜色为 `#cc7a60`。
- 路径名称：加粗，前景颜色。
- 光标闪烁：2px 宽度，主要颜色，动画效果。

**导航命令：**
- 显示方式：Flex，间距 `--spacing-md`。
- 按钮样式：等宽字体，小内边距（6px 12px）。
- 边框：`1px solid --border`。
- 边框半径：`--radius-lg`。
- 活动状态：边框颜色变为主要颜色，并带有脉动动画。
- 悬停状态：边框颜色变为主要颜色，透明度降低 50%。

**命令按钮结构：**
```html
<button class="nav-cmd">
  <span class="cmd-prefix">$</span>
  <span class="cmd-keyword">ai</span>
  <span class="cmd-flag">--search</span>
</button>
```

**命令颜色：**
- 前缀（`$`）：荧光绿色 (#39ff14)。
- 关键字：主要颜色 (#cc7a60) 或蓝色 (#3b82f6)。
- 标志：默认前景颜色。

### 卡片组件

**技能卡片：**
- 背景：`--bg-card` （浅色为 #fff，深色为 #111）。
- 边框：`1px solid --border`。
- 边框半径：`--radius-xl` (12px)`。
- 高度：`100%`，采用 flex 列布局。
- 悬停状态：边框颜色变为主要颜色，透明度降低 50%，阴影增加（`0 25px 50px rgba(204, 122, 96, 0.1)`，`translateY(-4px)`。
- 活动状态：`translateY(0) scale(0.99)`。
- 过渡效果：`all 0.3s ease`。
- **行号**：绝对定位在左侧，宽度 `2rem`，带有微妙的背景。
- **头像**：24px × 24px，带边框，悬停时缩放。
- **星形图标**：10px × 10px，警告颜色。
- **点赞按钮**：SVG 心形图标，悬停时颜色变化。

**类别卡片：**
- 与技能卡片相同的基样式。
- **颜色主题**：青色、蓝色、紫色、琥珀色变体。
- **文件夹图标**：SVG 图标，颜色随主题变化，悬停时缩放。
- **类别圆点**：小指示圆点，悬停时变化。
- **箭头图标**：悬停时出现。
- **JSON 显示**：键值对，带有主题颜色的悬停效果。
- **命令行**：底部显示命令风格文本。

**提及卡片：**
- 与技能卡片相同的基样式。
- 引用样式，带有引号。
- 来源引用，带有顶部边框分隔线。

### 按钮组件

**主要按钮（活动状态）：**
- 背景：`--primary` (#cc7a60)`。
- 颜色：`--primary-foreground` (#fff)`。
- 边框：`1px solid --border`。
- 边框半径：`--radius-lg`。
- 内边距：`6px 12px`（小）或 `--spacing-md --spacing-lg`（中）。
- 字体：等宽字体，`--text-xs` 或 `--text-sm`。

**次要按钮：**
- 背景：`--bg-card`。
- 边框：`1px solid --border`。
- 颜色：`--foreground`。
- 悬停状态：边框颜色变为主要颜色，透明度降低 50%。
- 活动状态：`transform: scale(0.95)`。

**图标按钮：**
- 方形或圆形。
- 内边距：`6px 12px`。
- 图标大小：`14px` 或 `16px`。
- 悬停/活动状态与次要按钮相同。

### 输入组件**

**搜索输入：**
- 背景：透明。
- 边框：无。
- 字体：等宽字体。
- 占位符：`--text-muted` 颜色。
- 焦点：无可见边框（极简设计）。

**文本输入：**
- 背景：`--bg-card`。
- 边框：`1px solid --border`。
- 边框半径：`--radius-sm` 或 `--radius-md`。
- 内边距：`--spacing-sm`。

**代码显示组件**

**代码块：**
- 背景：`rgba(255, 255, 255, 0.5)`，带背景模糊效果。
- 边框：`1px solid --border`。
- 边框半径：`--radius-lg`。
- 内边距：`--spacing-md`。
- 字体：等宽字体。
- 行高：`--leading-relaxed`。

**代码行：**
- 显示方式：Flex，对齐基线。
- 间距：`--spacing-sm`。

**描述块（评论样式）：**
- 左边边框：`4px solid rgba(204, 122, 96, 0.5)`。
- 背景：`rgba(204, 122, 96, 0.05)`。
- 左边内边距：`--spacing-md`。
- 右边边框半径：`--radius-lg`。

**网格布局**

**技能网格：**
- 显示方式：Grid。
- 列数：`repeat(3, 1fr)`（桌面），`repeat(2, 1fr)`（平板），`1fr`（移动设备）。
- 间距：`--spacing-lg` (24px)`。

**类别网格：**
- 显示方式：Grid。
- 列数：`repeat(4, 1fr)`（桌面），`repeat(2, 1fr)`（平板），`1fr`（移动设备）。
- 间距：`--spacing-lg`。

**提及网格：**
- 显示方式：Grid。
- 列数：`1fr 1fr`（桌面），`1fr`（移动设备）。
- 间距：`--spacing-lg`。

## 动画系统**

**过渡效果**

**默认过渡：**
- 持续时间：`0.15s` 或 `0.2s`。
- 时间设置：`cubic-bezier(.4,0,.2,1)`（缓入效果）。
- 属性：`all` 或特定属性。

**常见过渡效果：**
- 悬停状态：`all 0.2s ease`。
- 活动状态：`transform 0.2s ease`。
- 颜色变化：`color 0.2s ease` 或 `background-color 0.2s ease`。

**关键帧动画**

**光标闪烁动画：**
```css
@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
```
- 持续时间：`1s`。
- 重复次数：`infinite`。
- 用于：光标闪烁效果。

**脉动边框动画：**
```css
@keyframes pulse-border {
  0%, 100% { border-color: rgba(204, 122, 96, 0.5); }
  50% { border-color: var(--ring); }
}
```
- 持续时间：`2s`。
- 时间设置：`ease-in-out`。
- 重复次数：`infinite`。
- 用于：活动导航项。

**淡入上动画：**
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```
- 持续时间：`0.5s`。
- 时间设置：`ease`。
- 用于：卡片进入动画。
- 格子项的延迟：`0.1s` 递增。

**交互状态**

**悬停状态：**
- 按钮：边框颜色变化，背景变亮。
- 卡片：边框变为主要颜色，阴影增加，略微凸起。
- 链接：颜色变为主要颜色。
- 规模：悬停时不变（保持稳定性）。

**活动状态：**
- 按钮：`transform: scale(0.95)` - 微妙的按压效果。
- 持续时间：`0.2s`。

**焦点状态：**
- 外框：`2px solid --ring`，带有 `2px` 的偏移。
- 用于：可访问性，键盘导航。

## 背景图案**

**网格图案（页面背景）**
```css
background-image: 
  linear-gradient(rgba(0, 0, 0, 0.02) 1px, transparent 1px),
  linear-gradient(90deg, rgba(0, 0, 0, 0.02) 1px, transparent 1px);
background-size: 20px 20px;
```
- 非常微妙的网格（2% 不透明度，黑色）。
- 20px × 20px 的网格单元。
- 创建纹理，不会分散注意力。
- 应用于 `body` 背景。

**渐变背景**

**头像渐变：**
```css
background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
```
- 温暖的桃色渐变。
- 135 度角。
- 用于：用户头像。

**图表渐变：**
```css
linearGradient: #cc7a60 with opacity stops (0%: 0.6, 100%: 0)
```
- 主要颜色的渐变。
- 用于：面积图、数据可视化。

## 响应式设计**

### 分界点**

**移动设备：** `< 640px`
- 单列布局。
- 减小字体大小。
- 简化导航。
- 堆叠网格。

**平板设备：`640px - 1024px`
- 双列布局。
- 中等字体大小。
- 收叠导航菜单。

**桌面设备：`1024px - 1200px`
- 三列布局。
- 完整导航可见。
- 标准间距。

**大屏幕设备：`> 1200px`
- 四列布局（如适用）。
- 最大内容宽度：`1400px`。
- 丰富的间距。

**响应式调整**

**导航：**
- 桌面设备（>1024px）：显示完整命令菜单。
- 平板设备/移动设备：汉堡菜单，简化布局。
- 状态指示器：在移动设备上隐藏，在平板设备上显示。

**标题部分：**
- 桌面设备：两列网格（文本 + 图表）。
- 移动设备：单列，堆叠。

**网格：**
- 技能：3 → 2 → 1 列。
- 类别：4 → 2 → 1 列。
- 提及：2 → 1 列。

**字体：**
- 标题：3.5rem → 2.5rem（移动设备）。
- 部分标题：2.5rem → 2rem（移动设备）。
- 正文文本：保持可读性。

## 实现指南**

### CSS 变量使用**

**始终使用 CSS 变量**：
- 颜色（不要硬编码十六进制值）。
- 间距（使用间距比例）。
- 字体（使用文本大小比例）。
- 边框半径（使用半径比例）。
- 阴影（使用阴影比例）。

**示例：**
```css
.button {
  background: var(--bg-card);
  color: var(--foreground);
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}
```

### 组件结构**

**终端窗口样式：**
1. 带有边框和半径的容器。
2. 带有圆点、标题和状态的标题。
3. 带有内边距的内容区域。
4. 一致的间距。

**命令行样式：**
1. 命令前缀（`$`）使用荧光绿色。
2. 关键字使用主要颜色或蓝色。
3. 标志/参数使用默认颜色。
4. 全部使用等宽字体。

### 颜色应用规则**

**主要颜色 (#cc7a60)：**
- 用于：活动状态、高亮部分、关键字、提示。
- 避免：大面积背景（过于强烈）。
- 不透明度变体：使用 `rgba(204, 122, 96, 0.5)` 用于边框，`rgba(204, 122, 96, 0.05)` 用于背景。

**荧光绿色 (#39ff14)：**
- 仅用于：命令前缀（`$`）。
- 不得用于：其他文本、背景或强调色。

**绿色 (#22c55e)：**
- 用于：成功状态、正面指示器、字符串字面量。
- 避免：主要操作（使用主要颜色）。

**字体规则**

**始终使用等宽字体**：
- 导航元素。
- 按钮。
- 代码块。
- 命令行界面。
- 窗口标题。
- 状态文本。

**字体粗细指南：**
- 正文文本：400（正常）。
- 标签/关键字：600（粗体）。
- 标题：700（粗体）。
- 标题：700-800（特别粗体）。

**间距一致性**

**使用间距比例：**
- 不要使用任意值（例如，`13px`、`27px`）。
- 保持：4px、8px、16px、24px、32px、48px。
- 相关元素之间的间距：`--spacing-sm` 至 `--spacing-md`。
- 部分之间的间距：`--spacing-xl` 至 `--spacing-2xl`。

**动画最佳实践**

**保持动画微妙：**
- 持续时间：0.15s - 最大 0.3s。
- 使用提供的立方贝塞尔曲线（cubic-bezier）。
- 避免：跳跃式动画、长时间动画。
- 优先使用：淡入、平移、缩放（小幅度的动画）。

**性能：**
- 使用 `transform` 和 `opacity` 进行动画（GPU 加速）。
- 避免动画 `width`、`height`、`margin`、`padding`。

## 常见样式**

### 终端窗口卡片**

```html
<div class="terminal-window">
  <div class="window-header">
    <div class="window-dots">
      <span class="dot red"></span>
      <span class="dot yellow"></span>
      <span class="dot green"></span>
    </div>
    <span class="window-title">filename.ext</span>
    <span class="window-status">ready</span>
  </div>
  <div class="window-content">
    <!-- Content here -->
  </div>
</div>
```

### 命令按钮**

```html
<button class="nav-cmd">
  <span class="cmd-prefix">$</span>
  <span class="cmd-keyword">command</span>
  <span class="cmd-flag">--flag</span>
</button>
```

### 代码块显示**

```html
<div class="stats-code-block">
  <div class="code-line">
    <span class="keyword">const</span>
    <span class="variable-name">variable</span>
    <span class="operator">=</span>
    <span class="number">123</span>
    <span class="operator">;</span>
  </div>
  <div class="code-comment">
    <span class="comment-symbol">// </span>Comment text
  </div>
</div>
```

### 描述块（评论样式）

```html
<div class="description-block">
  <div class="comment-start">/**</div>
  <div class="comment-text">
    <span class="comment-asterisk"> * </span>Description text
  </div>
  <div class="comment-end"> */</div>
</div>
```

## 可访问性考虑**

**颜色对比度：**
- 主要文本 (#111827) 在白色上：符合 WCAG AAA 标准。
- 次要文本 (#666666) 在白色上：符合 WCAG AA 标准。
- 主要颜色 (#cc7a60) 在白色上：对于大文本，符合 WCAG AA 标准。

**焦点状态：**
- 所有交互元素都有可见的焦点指示器。
- 焦点环：2px 实心的主要颜色，带有 2px 的偏移。

**键盘导航：**
- 所有交互元素都可以通过键盘访问。
- 切换顺序遵循视觉层次结构。
- Enter/Space 键激活按钮。

**屏幕阅读器：**
- 使用语义 HTML 结构。
- 在需要时添加 ARIA 标签。
- 状态指示器使用适当的角色。

## 暗色模式实现**

该设计系统包括使用 `[data-theme="dark"]` 属性选择器的完整暗色模式实现。暗色模式与平滑的过渡效果完全集成，并保持所有设计原则。

### 暗色模式颜色系统**

**主要颜色（暗色模式）：**
- `--primary: #d99178` - 在深色背景上提供更好的对比度。
- `--primary-foreground: #0a0a0a` - 主要背景上的深色文本。
- `--primary-dark: #c57f66` - 悬停状态时的深色调。
- `--primary-light: #e5a890` - 微妙强调时的浅色调。
- `--ring: #d99178` - 焦点环的颜色（较浅的主要颜色）。

**背景（暗色模式）：**
- `--background: #0a0a0a` - 深色背景。
- `--bg-main: #0a0a0a` - 带有微妙白色网格图案的深色背景。
- `--bg-card: #111` - 卡片组件的浅灰色背景。
- `--bg-code: #18181b` - 代码块和窗口标题的深灰色背景。
- `--secondary: #1a1a1a` - 较浅的灰色背景。
- `--muted: #262626` - 较暗的灰色背景。

**文本颜色（暗色模式）：**
- `--foreground: #ededed` - 主要文本的浅灰色。
- `--text-primary: #ededed` - 主要文本颜色。
- `--text-secondary: #a3a3a3` - 较不重要的文本的浅灰色背景。
- `--text-muted: #a3a3a3` - 淡灰色背景上的主要文本。

**边框（暗色模式）：**
- `--border: #606068` - 在深色背景上更明显的浅灰色。
- `--border-light: #27272a` - 分隔线的浅灰色。

**语法高亮（暗色模式）：**
- `--syntax-keyword: #d99178` - 关键字的主要颜色（较浅的主要颜色）。
- `--syntax-string: #22c55e` - 绿色（与亮色模式相同）。
- `--syntax-number: #d99178` - 数字的主要颜色（较浅的主要颜色）。
- `--syntax-comment: #6a9955` - 淡绿色的评论（与亮色模式相同）。
- 蓝色关键字：`#60a5fa`（更亮的蓝色）。
- 紫色关键字：`#c084fc`（更亮的紫色）。

**阴影（暗色模式）：**
- `--shadow-sm: 0 1px 2px rgba(0,0,0,0.3)` - 更强的阴影效果。
- `--shadow-md: 0 4px 6px rgba(0,0,0,0.07)` - 中等阴影效果。
- `--shadow-lg: 0 10px 25px rgba(0,0,0,0.1)` - 大阴影效果。

### 暗色模式背景图案**

暗色模式使用微妙的白色网格图案：

```css
[data-theme="dark"] body {
  background-image: 
    linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
}
```

### 主题切换实现**

**HTML 结构：**
```html
<button class="theme-toggle-btn theme-toggle" title="切换主题" aria-label="切换主题">
  <svg class="icon-sun theme-icon"><!-- Sun icon --></svg>
  <svg class="icon-moon theme-icon" style="display: none;"><!-- Moon icon --></svg>
</button>
```

**JavaScript 实现：**
- 使用 `localStorage` 保存主题偏好设置。
- 在首次加载时检测系统偏好设置。
- 在主题之间平滑过渡。
- 自动更新图标可见性（太阳/月亮）。
- 监听系统主题变化（当没有手动设置时）。

**关键特性：**
- 自动检测系统偏好设置。
- 使用 `localStorage` 保存手动偏好设置。
- 平滑的 CSS 过渡效果（0.2s 缓入效果）。
- 图标状态管理（太阳代表亮色模式，月亮代表暗色模式）。

**暗色模式组件调整：**

**导航栏：**
- 背景：`rgba(10, 10, 10, 0.8)`，带背景模糊效果。
- 状态指示器：背景较深，边框调整。

**终端窗口：**
- 卡片背景：`#111`（比主背景稍浅）。
- 窗口标题：`rgba(38, 38, 38, 0.3)`，以获得微妙的对比度。
- 所有边框使用暗色模式的颜色。

**技能卡片：**
- 行号背景：`rgba(38, 38, 38, 0.2)`。
- 底部背景：`rgba(38, 38, 38, 0.2)`。
- 悬停效果保持相同的行为，但颜色调整。

**类别卡片：**
- 每个类别都有特定的悬停颜色：
  - 青色：`#22d3ee`（暗色）对比 `#06b6d4`（亮色）。
  - 蓝色：`#60a5fa`（暗色）对比 `#3b82f6`（亮色）。
  - 紫色：`#c084fc`（暗色）对比 `#a855f7`（亮色）。
  - 琥珀色：`#c084fc`（暗色）对比 `#f59e0b`（亮色）。

**图表：**
- 网格线条：`#27272a`，透明度 0.5。
- 图表容器：`rgba(17, 17, 17, 0.3)`。
- 所有文本颜色适应暗色模式。

**FAB 按钮：**
- 亮色模式：背景 `#1a1a1a`，图标为白色。
- 暗色模式：背景为白色，图标为深色。

**暗色模式最佳实践：**

**颜色对比度：**
- 所有文本在暗色模式下保持 WCAG AA 标准。
- 主要颜色变得更亮，以便更好的可见性。
- 边框更浅，以便更好的区分度。

**过渡效果：**
- 所有颜色变化使用 `transition: color 0.2s ease-in-out`。
- 背景变化使用 `transition: background-color 0.2s ease-in-out`。
- 过渡效果平滑，无突兀感。

**实现模式：**
```css
/* Light mode (default) */
.component {
  background: var(--bg-card);
  color: var(--foreground);
}

/* Dark mode */
[data-theme="dark"] .component {
  background: var(--bg-card); /* Automatically uses dark value */
  color: var(--foreground); /* Automatically uses dark value */
}
```

**保持：**
- 保持相同的间距系统。
- 保持相同的字体比例。
- 保持相同的组件结构。
- 保持相同的动画效果。
- 增强阴影效果，以增强深度感。

## 性能优化**

**CSS 变量：**
- 所有颜色/间距使用 CSS 变量，以便于主题设置。
- 在 `:root` 中定义变量，以便全局访问。

**动画：**
- 使用 `transform` 和 `opacity` 进行动画（GPU 加速）。
- 避免使用 `width`、`height`、`margin`、`padding` 的动画。

**字体加载：**
- 预先连接 Google Fonts。
- 使用 `font-display: swap` 以获得更好的性能。
- 提供备用字体。

**浏览器支持：**
- **现代浏览器**：完全支持。
- **Chrome/Edge**：完全支持。
- **Firefox**：完全支持。
- **Safari**：完全支持（需要 `-webkit-` 前缀）。

**使用的特性：**
- CSS Grid：在现代浏览器中完全支持。
- CSS 变量：完全支持。
- Backdrop Filter：需要 `-webkit-` 前缀。
- Flexbox：完全支持。

## 设计元素总结**

**快速参考：**
```css
/* Colors - Light Mode */
Primary: #cc7a60
Fluorescent Green: #39ff14 (command prefix only)
Success: #22c55e
Blue: #3b82f6
Foreground: #111827
Border: #8b929e

/* Colors - Dark Mode */
Primary: #d99178
Foreground: #ededed
Background: #0a0a0a
Card: #111
Border: #606068
Blue: #60a5fa (brighter for contrast)

/* Spacing */
xs: 4px, sm: 8px, md: 16px, lg: 24px, xl: 32px, 2xl: 48px

/* Typography */
Font: JetBrains Mono
Sizes: 0.75rem - 3.75rem scale
Weights: 400, 500, 600, 700, 800

/* Radius */
xs: 2px, sm: 4px, md: 6px, lg: 8px, xl: 12px, 2xl: 16px

/* Shadows - Light Mode */
sm: 0 1px 2px rgba(0,0,0,0.05)
md: 0 4px 6px rgba(0,0,0,0.07)
lg: 0 10px 25px rgba(0,0,0,0.1)

/* Shadows - Dark Mode */
sm: 0 1px 2px rgba(0,0,0,0.3)
md: 0 4px 6px rgba(0,0,0,0.4)
lg: 0 10px 25px rgba(0,0,0,0.5)
```

## 主题切换 JavaScript 实现**

**完整实现：**
```javascript
(function() {
  const themeToggles = document.querySelectorAll('.theme-toggle');
  const html = document.documentElement;
  
  // Get initial theme from localStorage or system preference
  function getInitialTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      return savedTheme;
    }
    // Check system preference
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }
    return 'light';
  }
  
  // Set theme and update icons
  function setTheme(theme) {
    if (theme === 'dark') {
      html.setAttribute('data-theme', 'dark');
      document.querySelectorAll('.icon-sun').forEach(icon => {
        icon.style.display = 'none';
      });
      document.querySelectorAll('.icon-moon').forEach(icon => {
        icon.style.display = 'block';
      });
    } else {
      html.removeAttribute('data-theme');
      document.querySelectorAll('.icon-sun').forEach(icon => {
        icon.style.display = 'block';
      });
      document.querySelectorAll('.icon-moon').forEach(icon => {
        icon.style.display = 'none';
      });
    }
    localStorage.setItem('theme', theme);
  }
  
  // Toggle theme
  function toggleTheme() {
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
  }
  
  // Initialize
  const initialTheme = getInitialTheme();
  setTheme(initialTheme);
  
  // Add event listeners
  themeToggles.forEach(button => {
    button.addEventListener('click', toggleTheme);
  });
  
  // Listen to system theme changes (only if no manual preference)
  if (window.matchMedia) {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', (e) => {
      if (!localStorage.getItem('theme')) {
        setTheme(e.matches ? 'dark' : 'light');
      }
    });
  }
})();
```

**关键特性：**
- 在 `localStorage` 中保存主题偏好设置。
- 在首次加载时检测系统偏好设置。
- 在主题之间平滑过渡。
- 自动更新图标可见性。
- 监听系统主题变化（当没有手动设置时）。

**使用示例：**

在实现此设计系统时，请遵循以下步骤：
1. **从 CSS 变量开始** - 导入或定义所有颜色/间距变量（包括暗色模式）。
2. **使用终端窗口样式** - 将内容包裹在终端窗口组件中。
3. **应用等宽字体** - 对所有 UI 文本使用 JetBrains Mono 字体。
4. **遵循间距比例** - 一致使用定义的间距值。
5. **使用语义颜色** - 根据含义而不是外观应用颜色。
6. **实现主题切换** - 添加主题切换按钮和 JavaScript 代码。
7. **保持一致性** - 在整个项目中重复使用组件样式。
8. **测试响应性** - 确保布局在所有分界点上都能正常工作。
9. **测试两种主题** - 确保亮色和暗色模式都能正确显示。
10. **优化动画** - 保持过渡效果平滑且性能良好。

该设计系统创建了一个连贯的、对开发者友好的界面，让用户感觉既现代又熟悉终端界面。完整的暗色模式实现确保界面在任何光照条件下都能完美显示。