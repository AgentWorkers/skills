---
name: aioz-ui-v3
description: 使用 AIOZ UI V3 设计系统来构建用户界面组件和页面。当用户需要使用 AIOZ UI 的标记（tokens）、Tailwind 样式类、颜色标识符、字体工具、来自 @aioz-ui/icon-react 的图标，或者图表组件（LineChart、AreaChart、BarChart、DonutChart）来创建、编辑或设置 React 组件的样式时，都可以运用这项技能。该技能适用于涉及 AIOZ UI 组件的任何任务，例如使用设计标识符（如 --sf-neu-block 或 --text-neu-bold）、品牌颜色、字体类（text-title-01、text-body-02）、图标导入、数据可视化，以及将 Figma MCP 生成的代码转换为可生产使用的代码等场景。
---
# AIOZ UI V3 — Figma MCP 到代码的映射规则

本文档详细说明了如何使用 AIOZ UI V3 设计系统将 Figma MCP 生成的输出转换为实际的 React 代码。

> **规则 1：** 绝不要猜测令牌名称或类名称。请始终参考下面的映射表。

---

## Figma MCP 的数据返回格式

当 Figma MCP 代理检查一个节点时，它会以以下格式返回数据：

| 数据类型        | Figma MCP 示例                                      | 操作                                      |
|--------------|---------------------------------------------------|---------------------------------------|
| 颜色/填充颜色    | `Onsf/Error/Default`, `Sf/Pri/Pri`                        | → 查阅 `references/colors.md` 文件                |
| 字体排版      | `Button/01`, `Body/02`, `Subheadline/01`                        | → 查阅 `references/typography.md` 文件                |
| 图标          | `icon/24px/outline/wallet-01`                        | → 查阅 `references/icons.md` 文件                |
| 组件名称      | `Button/Primary`, `Badge/Success`, `Fields/Default`                | → 参见下面的 **组件映射表**                   |
| 变体字符串     | `Type=Primary, Size=Medium, Shape=Square`                   | → 参见下面的 **变量/属性映射表**                   |
| 变量值       | `"Onsf/Bra/Default": "#121212"`                         | 使用斜杠路径格式，切勿使用 CSS 的 `--var`               |
| 设置/配置      | 项目配置相关内容                                  | → 查阅 `references/setup.md` 文件                |

> ⚠️ Figma MCP 总是使用斜杠分隔符（如 `Onsf/Error/Default`）来返回令牌名称。
> 它 **不会** 以 CSS 的自定义属性格式（如 `--onsf-error-default`）返回数据。

---

## 注意：** 请勿混淆两种导入路径 **

---  
（此处应插入具体的导入路径示例，但原文未提供。）

---

## 组件映射表

**输入：** Figma MCP 中符号/实例节点的 `name` 字段  
**输出：** 需要使用的 React 组件  

| Figma 节点名称模式 | React 组件                                      | 导入路径                                      |
|-------------------|----------------------------------|-----------------------------------------|
| `Button/*`       | `Button`                                      | `import { Button } from '@aioz-ui/core-v3/components'`         |
| `Fields/*`       | `Input`                                      | `import { Input } from '@aioz-ui/core-v3/components'`         |
| `Badge/*`       | `Badge`                                      | `import { Badge } from '@aioz-ui/core-v3/components'`         |
| `Tag/*`       | `Tag`                                      | `import { Tag } from '@aioz-ui/core-v3/components'`         |
| `Card/*`       | `Card`                                      | `import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@aioz-ui/core-v3/components'` |
| `Toggle/*`       | `Switch`                                      | `import { Switch } from '@aioz-ui/core-v3/components'`         |
| `Checkbox/*`       | `Checkbox`                                      | `import {Checkbox } from '@aioz-ui/core-v3/components'`         |
| `Tooltip/*`       | `Tooltip`                                      | `import { Tooltip, TooltipProvider, TooltipTrigger, TooltipContent } from '@aioz-ui/core-v3/components'` |
| `Tabs/*`       | `Tabs`                                      | `import { Tabs, TabsList, TabsTrigger, TabsContent } from '@aioz-ui/core-v3/components'`         |
| `Table/*`       | `Table`                                      | `import { Table, Header, Body, Row, HeadCell, Cell } from '@aioz-ui/core-v3/components'`         |
| `Separator/*`       | `Separator`                                      | `import { Separator } from '@aioz-ui/core-v3/components'`         |
| `Pagination item/*`    | `PaginationGroup`                                  | `import { PaginationGroup } from '@aioz-ui/core-v3/components'`         |
| `Progress bar/*`    | `Progress`                                      | `import { Progress } from '@aioz-ui/core-v3/components'`         |
| `Slider/*`       | `Slider`                                      | `import { Slider } from '@aioz-ui/core-v3/components'`         |
| `Upload file/*`    | `UploadFile`                                      | `import { UploadFile } from '@aioz-ui/core-v3/components'`         |
| `Menu item/*`    | `MenuItem`                                      | `import { MenuItem } from '@aioz-ui/core-v3/components'`         |
| `Dropdown item/*`    | `DropdownMenu`                                  | `import { DropdownMenu, DropdownMenuContent, DropdownMenuItem,DropdownMenuTrigger } from '@aioz-ui/core-v3/components'`         |
| `Modal/*`       | `Dialog`                                      | `import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogClose } from '@aioz-ui/core-v3/components'`         |
| `Block/*`       | `Block`                                      | `import { Block } from '@aioz-ui/core-v3/components'`         |
| `IconBadge/*`       | `IconBadge`                                      | `import { IconBadge } from '@aioz-ui/core-v3/components'`         |
| `Message/*`       | `Message`                                      | `import { Message } from '@aioz-ui/core-v3/components'`         |
| `Breadcrumb/*`       | `Breadcrumb`                                      | `import { Breadcrumb } from '@aioz-ui/core-v3/components'`         |
| `Date picker/*`    | `DatePicker`                                      | `import { DatePicker } from '@aioz-ui/core-v3components`         |

---

## 变体到属性的映射表

Figma MCP 通过逗号分隔的 `Key=value` 对来编码组件变体：

---  
（此处应插入具体的变量/属性映射表示例，但原文未提供。）

---

## 注意事项：

- **组件名称与 React 组件的对应关系**：请根据 Figma MCP 返回的节点名称，使用相应的 React 组件。
- **颜色和字体排版**：`Button` 组件内部已经处理了颜色和字体排版。只有在构建自定义布局时，才需要手动应用颜色/字体类。
- **图标的使用**：请仅使用 `@aioz-ui'icon-react` 中提供的图标，避免使用 SVG 字符串、表情符号或其他第三方库。
- **背景文本**：位于 `bg-sf-*` 样式背景上的文本必须使用相应的 `text-onsf-*` 类。
- **图表组件**：请始终从 `@aioz-ui/core/components` 导入图表组件，并确保为图表提供 `categories` 和 `overwriteCategories` 属性。在编写图表代码之前，请先阅读 `references/charts.md` 文件。

---

## 参考文件

以下文件包含了详细的 API 文档、完整的令牌列表以及组件示例：

| 文件名            | 需要查看的时间                        |
|------------------|-----------------------------------------|
| `references/colors.md`     | 文本、背景和边框相关的令牌及其对应的 Tailwind 类           |
| `references/typography.md` | 所有 `text-*` 类的完整列表，包括字体大小、行高和字体粗细等属性 |
| `references/icons.md`     | 图标名称转换规则、尺寸指南以及常用图标的导入方式           |
| `references/components.md` | 每个组件的完整属性、所有变体以及可用的代码示例         |
| `references/charts.md`     | LineChart、AreaChart、BarChart、DonutChart 的 API、变体设置以及图例相关内容 |

---

请根据实际情况调整上述内容，以确保翻译的准确性和完整性。