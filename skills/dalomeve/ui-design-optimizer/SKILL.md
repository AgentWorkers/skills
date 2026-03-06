---
name: ui-design-optimizer
description: 使用本地风格/颜色/排版数据集生成实用的 UI 设计系统及起始页面。这些系统可用于 landing page（登录页面）或 dashboard（仪表盘）的 UI 规划与实现。
---
# UI设计优化工具

## 目标

提供具体的、可构建的UI设计方案，而不仅仅是通用的设计建议。

## 输入参数

- 产品/领域描述（例如：SaaS仪表板、招聘工具、美容类单页应用）
- 页面类型（登录页面或仪表板）
- 首选的技术栈（默认为HTML/CSS）

## 数据来源

- `data/styles.csv`
- `data/colors.csv`
- `data/typography.csv`
- `data/patterns.csv`
- `data/rules.json`

## 必需的工作流程

1. 从样式、颜色和排版数据中读取相关内容。
2. 选择一种样式、一种配色方案以及一种排版方案，并说明选择理由。
3. 输出一份简洁的设计规范：
   - 布局方案
   - 颜色代码
   - 排版规范
   - 交互规则
4. 如果用户要求实现该设计，生成可运行的文件（至少包括`index.html`和`styles.css`）。
5. 提供文件路径以及所选数据集中的相关行/记录的详细信息。

## 质量标准

- 优先考虑可读性和可访问性（符合WCAG AA标准中的对比度要求）。
- 保持一致的间距、字体大小和组件状态。
- 当用户要求实现设计时，避免仅提供占位符内容。
- 生成的文本必须为UTF-8格式，确保没有乱码问题。

## 验证步骤

在生成文件后，需要验证以下内容：

- 文件是否已正确保存在磁盘上；
- HTML文件是否正确引用了样式表；
- 选定的样式/配色方案/排版方案是否已在CSS变量中得到体现。

## 帮助脚本

当需要快速查找相关信息时，可以使用`scripts/search.ps1`脚本：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/search.ps1 -Query "saas dashboard" -DesignSystem -ProjectName "Demo"
```