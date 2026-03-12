---
name: "ui-design-system"
description: 面向高级UI设计师的UI设计系统工具包，包含设计令牌生成、组件文档编写、响应式设计计算以及开发者交接工具等功能。该工具包用于构建设计系统、维护视觉一致性，并促进设计与开发之间的协作。
---
# UI设计系统

本系统用于生成设计相关的数据（设计令牌），创建颜色调色板，计算排版比例，构建组件系统，并准备开发人员所需的交接文档。

---

## 目录

- [相关术语](#相关术语)
- [工作流程](#工作流程)
  - [工作流程1：生成设计令牌](#工作流程1-生成设计令牌)
  - [工作流程2：构建组件系统](#工作流程2-构建组件系统)
  - [工作流程3：响应式设计](#工作流程3-响应式设计)
  - [工作流程4：开发人员交接](#工作流程4-开发人员交接)
- [工具参考](#工具参考)
- [快速参考表](#快速参考表)
- [知识库](#知识库)

---

## 相关术语

当您需要执行以下操作时，请使用本技能：
- “生成设计令牌”
- “创建颜色调色板”
- “构建排版比例”
- “计算间距系统”
- “创建设计系统”
- “生成CSS变量”
- “导出SCSS令牌”
- “设置组件架构”
- “记录组件库”
- “计算响应式断点”
- “准备开发人员交接资料”
- “将品牌颜色转换为调色板”
- “检查WCAG对比度”
- “构建8pt网格系统”

---

## 工作流程

### 工作流程1：生成设计令牌

**场景**：您拥有一个品牌颜色，并需要一个完整的设计令牌系统。

**步骤**：
1. **确定品牌颜色和风格**
   - 品牌主色（十六进制格式）
   - 风格偏好：`modern` | `classic` | `playful`

2. **使用脚本生成令牌**
   ```bash
   python scripts/design_token_generator.py "#0066CC" modern json
   ```

3. **审核生成的类别**
   - 颜色：主色、辅助色、中性色、语义色、表面色
   - 排版：字体家族（fontFamily）、字体大小（fontSize）、字体粗细（fontWeight）、行高（linewidth）
   - 间距：基于8pt网格的比例（0-64）
   - 边框：半径（radius）、宽度（width）
   - 阴影：无（none）到2倍大小（2xl）
   - 动画：持续时间（duration）、缓动效果（easing）
   - 断点：小屏幕（xs）到大屏幕（2xl）

4. **以目标格式导出**
   ```bash
   # CSS custom properties
   python scripts/design_token_generator.py "#0066CC" modern css > design-tokens.css

   # SCSS variables
   python scripts/design_token_generator.py "#0066CC" modern scss > _design-tokens.scss

   # JSON for Figma/tooling
   python scripts/design_token_generator.py "#0066CC" modern json > design-tokens.json
   ```

5. **验证可访问性**
   - 检查颜色对比度是否符合WCAG AA标准（普通文本：4.5:1，大文本：3:1）
   - 确保语义颜色有对应的对比色

---

### 工作流程2：构建组件系统

**场景**：您需要使用设计令牌来组织组件库。

**步骤**：
1. **定义组件层次结构**
   - 基本组件：按钮（Button）、输入框（Input）、图标（Icon）、标签（Label）、徽章（Badge）
   - 组合组件：表单字段（FormField）、搜索栏（SearchBar）、卡片（Card）、列表项（ListItem）
   - 复合组件：页眉（Header）、页脚（Footer）、数据表格（DataTable）、模态框（Modal）
   - 模板：仪表板布局（DashboardLayout）、认证布局（AuthLayout）

2. **将令牌映射到组件**
   | 组件 | 使用的令牌 |
   |-----------|-------------|
   | 按钮 | 颜色（colors）、大小（sizing）、边框（bounds）、阴影（shadows）、排版（typography） |
   | 输入框 | 颜色（colors）、大小（sizing）、边框（bounds）、间距（spacing） |
   | 卡片 | 颜色（colors）、边框（bounds）、阴影（shadows）、间距（spacing） |
   | 模态框 | 颜色（colors）、阴影（shadows）、间距（spacing）、层叠顺序（z-index）、动画（animation） |

3. **定义变体样式**
   - 大小变体：
   ```
   sm: height 32px, paddingX 12px, fontSize 14px
   md: height 40px, paddingX 16px, fontSize 16px
   lg: height 48px, paddingX 20px, fontSize 18px
   ```

   - 颜色变体：
   ```
   primary: background primary-500, text white
   secondary: background neutral-100, text neutral-900
   ghost: background transparent, text neutral-700
   ```

4. **记录组件API**
   - 组件的属性接口（props）及其类型
   - 变体选项
   - 组件状态（悬停（hover）、激活（active）、聚焦（focus）、禁用（disabled）时的表现
   - 可访问性要求

5. **参考文档**：`references/component-architecture.md`

---

### 工作流程3：响应式设计

**场景**：您需要设置断点、实现流动式排版或响应式间距。

**步骤**：
1. **定义断点**
   | 名称 | 宽度（Width） | 目标屏幕尺寸（Target） |
   |------|-------|--------|
   | xs | 0px | 小型手机 |
   | sm | 480px | 中型手机 |
   | md | 640px | 平板电脑 |
   | lg | 768px | 小型笔记本电脑 |
   | xl | 1024px | 大型笔记本电脑 |
   | 2xl | 1280px | 大屏幕 |

2. **计算流动式排版比例**
   公式：`clamp(min, preferred, max)`

   ```css
   /* 16px to 24px between 320px and 1200px viewport */
   font-size: clamp(1rem, 0.5rem + 2vw, 1.5rem);
   ```

   预计算的比例值：
   ```css
   --fluid-h1: clamp(2rem, 1rem + 3.6vw, 4rem);
   --fluid-h2: clamp(1.75rem, 1rem + 2.3vw, 3rem);
   --fluid-h3: clamp(1.5rem, 1rem + 1.4vw, 2.25rem);
   --fluid-body: clamp(1rem, 0.95rem + 0.2vw, 1.125rem);
   ```

3. **设置响应式间距**
   | 令牌 | 移动端（Mobile） | 平板端（Tablet） | 电脑端（Desktop） |
   |-------|--------|--------|---------|
   | --space-md | 12px | 16px | 16px |
   | --space-lg | 16px | 24px | 32px |
   | --space-xl | 24px | 32px | 48px |
   | --space-section | 48px | 80px | 120px |

4. **参考文档**：`references/responsive-calculations.md`

---

### 工作流程4：开发人员交接

**场景**：您需要将设计令牌移交给开发团队。

**步骤**：
1. **以所需格式导出令牌**
   ```bash
   # For CSS projects
   python scripts/design_token_generator.py "#0066CC" modern css

   # For SCSS projects
   python scripts/design_token_generator.py "#0066CC" modern scss

   # For JavaScript/TypeScript
   python scripts/design_token_generator.py "#0066CC" modern json
   ```

2. **准备框架集成**
   - **React + CSS变量**：
   ```tsx
   import './design-tokens.css';

   <button className="btn btn-primary">Click</button>
   ```

   - **Tailwind CSS配置**：
   ```javascript
   const tokens = require('./design-tokens.json');

   module.exports = {
     theme: {
       colors: tokens.colors,
       fontFamily: tokens.typography.fontFamily
     }
   };
   ```

   - **样式化组件（styled-components）**：
   ```typescript
   import tokens from './design-tokens.json';

   const Button = styled.button`
     background: ${tokens.colors.primary['500']};
     padding: ${tokens.spacing['2']} ${tokens.spacing['4']};
   `;
   ```

3. **与Figma同步**
   - 安装Tokens Studio插件
   - 导入design-tokens.json文件
   - 令牌会自动与Figma样式同步

4. **交接检查清单**
   - [ ] 令牌文件已添加到项目中
   - [ ] 构建流程已配置
   - [ ] 主题/CSS变量已导入
   - [ ] 组件库已对齐
   - [ ] 文档已生成

5. **参考文档**：`references/developer-handoff.md`

---

## 工具参考

### design_token_generator.py

该脚本根据品牌颜色生成完整的设计令牌系统。

| 参数 | 值 | 默认值 | 说明 |
|----------|--------|---------|-------------|
| brand_color | 十六进制颜色 | #0066CC | 主品牌颜色 |
| style | modern | classic | playful | 设计风格预设 |
| format | json | css | scss | 输出格式 |

**示例**：
```bash
# Generate JSON tokens (default)
python scripts/design_token_generator.py "#0066CC"

# Classic style with CSS output
python scripts/design_token_generator.py "#8B4513" classic css

# Playful style summary view
python scripts/design_token_generator.py "#FF6B6B" playful summary
```

**输出类别**：
| 类别 | 说明 | 关键值 |
|----------|-------------|------------|
| colors | 颜色调色板 | 主色、辅助色、中性色、语义色、表面色 |
| typography | 字体系统 | 字体家族、字体大小、字体粗细、行高 |
| spacing | 8pt网格系统 | 0-64的比例范围 |
| sizing | 组件尺寸 | 容器（container）、按钮（button）、输入框（input）、图标（icon） |
| borders | 边框样式 | 半径（radius）、宽度（width） |
| shadows | 阴影效果 | 无（none）到2倍大小（2xl） |
| animation | 动画效果 | 持续时间（duration）、缓动效果（easing）、关键帧（keyframes） |
| breakpoints | 响应式断点 | 小屏幕（xs）到大屏幕（2xl） |
| z-index | 层叠顺序 | 基础值到通知框（notification） |

---

## 快速参考表

### 颜色比例生成

| 步骤 | 亮度（Brightness） | 饱和度（Saturation） | 使用场景 |
|------|------------|------------|----------|
| 50 | 95% | 固定值 | 柔和的背景颜色 |
| 100 | 95% | 固定值 | 明亮的背景颜色 |
| 200 | 95% | 固定值 | 鼠标悬停时的颜色 |
| 300 | 95% | 固定值 | 边框颜色 |
| 400 | 95% | 固定值 | 禁用状态的颜色 |
| 500 | 原始值 | 70% | 基础/默认颜色 |
| 600 | 原始值 × 0.8 | 78% | 鼠标悬停时的深色 |
| 700 | 原始值 × 0.6 | 86% | 活动状态的颜色 |
| 800 | 原始值 × 0.4 | 94% | 文本颜色 |
| 900 | 原始值 × 0.2 | 标题颜色 |

### 排版比例（1.25倍比例）

| 大小（Size） | 值（Value） | 计算方式（Calculation） |
|------|-------|-------------|
| xs | 10px | 16 ÷ 1.25² |
| sm | 13px | 16 ÷ 1.25¹ |
| base | 16px | 基础值 |
| lg | 20px | 16 × 1.25¹ |
| xl | 25px | 16 × 1.25² |
| 2xl | 31px | 16 × 1.25³ |
| 3xl | 39px | 16 × 1.25⁴ |
| 4xl | 49px | 16 × 1.25⁵ |
| 5xl | 61px | 16 × 1.25⁶ |

### WCAG对比度要求

| 对比度级别 | 普通文本（Normal Text） | 大文本（Large Text） |
|-------|-------------|------------|
| AA | 4.5:1 | 3:1 |
| AAA | 7:1 | 4.5:1 |

**大文本**：字体大小≥18px（普通文本）或≥14px（粗体文本）

### 风格预设

| 风格预设（Style Presets） | modern | classic | playful |
|--------|--------|---------|---------|
| 字体（Font） | Inter | Helvetica | Poppins |
| 单色字体（Font Mono） | Fira Code | Courier | Source Code Pro |
| 边框半径（Radius） | 8px | 4px | 16px |
| 阴影效果（Shadows） | 多层阴影 | 单层阴影 | 温和阴影 | 明显阴影 |

---

## 知识库

详细参考资料请参见`references/`目录下的文件：
- `token-generation.md`：颜色算法、HSV颜色空间、WCAG对比度标准、排版比例
- `component-architecture.md`：基本组件设计、命名规范、属性使用方式
- `responsive-calculations.md`：响应式设计断点、流动式排版、网格系统
- `developer-handoff.md`：输出格式、框架集成方法、Figma同步指南

---

## 验证检查清单

### 令牌生成
- [ ] 品牌颜色以十六进制格式提供
- [ ] 风格符合项目要求
- [ ] 所有设计令牌类别均已生成
- [ ] 语义颜色包含对比度值

### 组件系统
- [ ] 所有组件大小（sm、md、lg）均已实现
- [ ] 所有组件变体（主色、辅助色、禁用状态）均已实现
- [ ] 所有组件状态（悬停、激活、聚焦、禁用）均能正常工作
- [ ] 仅使用设计令牌，无硬编码值

### 可访问性
- [ ] 颜色对比度符合WCAG AA标准
- [ ] 焦点指示器可见
- [ ] 触控目标元素尺寸≥44×44px
- [ ] 使用了语义化的HTML元素

### 开发人员交接
- [ ] 令牌已以所需格式导出
- [ ] 框架集成已完成文档记录
- [ ] 设计工具已同步
- [ ] 组件文档齐全