---
name: aioz-ui-v3
description: 使用 AIOZ UI V3 设计系统来构建 UI 组件和页面。每当用户需要使用 AIOZ UI 标记、Tailwind 类、颜色标记、排版工具、来自 @aioz-ui/icon-react 的图标，或者图表组件（LineChart、AreaChart、BarChart、DonutChart）来创建、编辑或样式化 React 组件时，都可以运用这项技能。该技能适用于涉及 AIOZ UI 组件的任何任务，例如使用设计标记（如 --sf-neu-block 或 --text-neu-bold）、品牌颜色、排版类（text-title-01、text-body-02）、图标导入、数据可视化，以及将 Figma MCP 生成的代码转换为适合生产环境的代码。
---
# AIOZ UI V3 — Figma MCP 到代码的映射规则

本文档详细说明了如何使用 AIOZ UI V3 设计系统将 Figma MCP 的输出转换为实际的 React 代码。

> **规则 1：** **切勿猜测** 标记名称或类名称。请始终参考下方的映射表。

---

## Figma MCP 的数据返回格式

当 Figma MCP 代理检查一个节点时，它会以以下格式返回数据：

| 数据类型        | Figma MCP 示例                                      | 操作                                      |
|--------------|---------------------------------------------------|---------------------------------------|
| 颜色/填充颜色     | `Onsf/Error/Default`, `Sf/Pri/Pri`                          | → 查阅 `references/colors.md` 文件                   |
| 字体排版       | `Button/01`, `Body/02`, `Subheadline/01`                        | → 查阅 `references/typography.md` 文件                   |
| 图标层         | `icon/24px/outline/wallet-01`                              | → 查阅 `references/icons.md` 文件                   |
| 组件名称       | `Button/Primary`, `Badge/Success`, `Fields/Default`                | → 参见下方的 **组件映射表**                          |
| 变体字符串     | `Type=Primary, Size=Medium, Shape=Square`                        | → 参见下方的 **变量/属性映射表**                          |
| 变量值       | `"Onsf/Bra/Default": "#121212"`                               | 使用斜杠路径格式，**禁止**使用 CSS 的 `--var` 属性           |
| 设置/配置       | 项目配置相关信息                                    | → 查阅 `references/setup.md` 文件                   |

> ⚠️ Figma MCP 始终使用斜杠分隔符（如 `Onsf/Error/Default`）来表示标记名称。
> 它**不**使用 CSS 的自定义属性格式（如 `--onsf-error-default`）。

---

## ⚠️ 两种导入路径——切勿混淆它们

---  
（此处应插入具体的导入路径示例）  

---

## 组件映射表

**输入：** Figma MCP 中符号/实例节点的 `name` 字段  
**输出：** 需要使用的 React 组件  

| Figma 节点名称模式       | React 组件                          | 导入路径                                      |
|-------------------|----------------------------------|--------------------------------------|
| `Button/*`           | `Button`                          | `import { Button } from '@aioz-ui/core-v3/components'`            |
| `Fields/*`           | `Input`                          | `import { Input } from '@aioz-ui/core-v3/components'`            |
| `Badge/*`           | `Badge`                          | `import { Badge } from '@aioz-ui/core-v3/components'`            |
| `Tag/*`           | `Tag`                          | `import { Tag } from '@aioz-ui/core-v3/components'`            |
| `Card/*`           | `Card`                          | `import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@aioz-ui/core-v3/components'` |
| `Toggle/*`           | `Switch`                          | `import { Switch } from '@aioz-ui/core-v3/components'`            |
| `Checkbox/*`           | `Checkbox`                          | `import {Checkbox } from '@aioz-ui/core-v3/components'`            |
| `Tooltip/*`           | `Tooltip`                          | `import { Tooltip, TooltipProvider, TooltipTrigger, TooltipContent } from '@aioz-ui/core-v3/components'` |
| `Tabs/*`           | `Tabs`                          | `import { Tabs, TabsList, TabsTrigger, TabsContent } from '@aioz-ui/core-v3/components'` |
| `Table/*`           | `Table`                          | `import { Table, Header, Body, Row, HeadCell, Cell } from '@aioz-ui/core-v3/components'` |
| `Separator/*`           | `Separator`                          | `import { Separator } from '@aioz-ui/core-v3/components'`            |
| `Pagination item/*`       | `PaginationGroup`                     | `import { PaginationGroup } from '@aioz-ui/core-v3/components'`         |
| `Progress bar/*`          | `Progress`                          | `import { Progress } from '@aioz-ui/core-v3/components'`            |
| `Slider/*`           | `Slider`                          | `import { Slider } from '@aioz-ui/core-v3/components'`            |
| `Upload file/*`          | `UploadFile`                          | `import { UploadFile } from '@aioz-ui/core-v3/components'`            |
| `Menu item/*`           | `MenuItem`                          | `import { MenuItem } from '@aioz-ui/core-v3/components'`            |
| `Dropdown item/*`           | `DropdownMenu`                        | `import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@aioz-ui/core-v3/components'` |
| `Modal/*`           | `Dialog`                          | `import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogClose } from '@aioz-ui/core-v3components'` |
| `Block/*`           | `Block`                          | `import { Block } from '@aioz-ui/core-v3/components'`            |
| `IconBadge/*`           | `IconBadge`                          | `import { IconBadge } from '@aioz-ui/core-v3/components'`            |
| `Message/*`           | `Message`                          | `import { Message } from '@aioz-ui/core-v3/components'`            |
| `Breadcrumb/*`           | `Breadcrumb`                          | `import { Breadcrumb } from '@aioz-ui/core-v3components'`            |
| `Date picker/*`          | `DatePicker`                          | `import { DatePicker } from '@aioz-ui/core-v3/components'`            |

---

## 变体到属性的映射表

Figma MCP 通过逗号分隔的 `Key=value` 对的形式在节点名称中编码变量：

---  
（此处应插入具体的变量映射表内容）  

| Figma 变体                | React 属性                        | 备注                                      |
|-----------------------------|----------------------------------|----------------------------------------|
| `Type=Primary`                | `variant="primary"`                        |                                      |
| `Type=Secondary`                | `variant="secondary"`                        |                                      |
| `Type=Neutral`                | `variant="neutral"`                        |                                      |
| `Type=Text`                   | `variant="text"`                        |                                      |
| `Type=Danger` / `Danger=True`          | `variant="danger"`                        |                                      |
| `Size=Large`                  | `size="lg"`                                      |                                      |
| `Size=Medium`                  | `size="md"`                                      |                                      |
| `Size=Small`                  | `size="sm"`                                      |                                      |
| `Shape=Circle`                | `shape="circle"`                        |                                      |
| `Shape=Square`                | `shape="square"`                        |                                      |
| `Shape=Default`                | `shape="default"`                        |                                      |
| `State=Default`                | *(无属性)*                          | 默认渲染状态                               |
| `State=Hover`                | *(无属性)*                          | 由 CSS 处理                                   |
| `State=Focused`                | *(无属性)*                          | 由 CSS 处理                                   |
| `State=Pressed`                | *(无属性)*                          | 由 CSS 处理                                   |
| `State=Disabled`                | `disabled`                          |                                      |
| `State=Loading`                | `loading`                                      |                                      |
| `Icon Only=True`                | `size="icon"`                        | 仅用于图标按钮                               |

---

## 完整的转换示例

假设 Figma MCP 的输出如下：

---  
（此处应插入示例数据）  

转换后的 React 代码如下：

---  
（此处应插入转换后的代码示例）  

> 颜色和字体排版由 `Button` 组件内部处理。仅在构建组件之外的**自定义布局**时，才需要手动应用颜色/字体排版类。

---

## 核心规则

1. **优先使用标记名称**——**禁止**直接使用 Tailwind 的颜色或尺寸设置。  
   ---  
（此处应插入相关说明）  

2. **优先使用设计系统提供的组件**——优先使用设计系统中的基础组件，而非自定义的 `div`。请参考上方的组件映射表。  

3. **字体排版是原子化的**——每个 `text-*` 类已经包含了字体大小、行高、字体粗细等属性。**禁止**再添加额外的字体样式。  

4. **图标必须来自 `@aioz-ui'icon-react`**——禁止使用 SVG 字符串、表情符号或其他第三方库。  
   ---  
（此处应插入相关说明）  

5. **位于特定背景上的文本**——位于 `bg-sf-*` 背景上的文本必须使用对应的 `text-onsf-*` 类：  
   ---  
（此处应插入相关说明）  

6. **图表组件**——始终从 `@aioz-ui/core/components` 导入图表组件（而非 `-v3` 版本）。务必将图表组件包裹在 `Card` 组件中，并提供 `categories` 和 `overwriteCategories` 属性。在编写任何图表代码之前，请先阅读 `references/charts.md` 文件。  

---

## 参考文件

如需深入了解 API 文档、完整的标记列表和组件示例，请打开以下文件：  

| 文件名                | 阅读时机                                      |
|-------------------|-----------------------------------------|
| `references/colors.md`     | 文本、背景和边框相关的标记及其对应的 Tailwind 类别           |
| `references/typography.md` | 所有 `text-*` 类的完整列表，包含字体大小、粗细和行高等属性    |
| `references/icons.md`     | 图标名称转换规则、尺寸指南及常用图标导入方式             |
| `references/components.md` | 所有组件的完整属性、变体及可直接使用的代码示例           |
| `references/charts.md`     | LineChart、AreaChart、BarChart、DonutChart 组件的 API、变体、图例和隐藏系列设置 |