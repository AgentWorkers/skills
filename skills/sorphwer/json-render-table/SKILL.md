---
name: json-render-table
description: 使用 `json-render-cli` 将紧凑的通用数据表渲染为 PNG 图像。当用户要求将任意结构化的行/列（非特定于工单的数据）以可控制的布局形式可视化为清晰的表格截图时，可以使用此工具。
user-invocable: false
---
# JSON渲染表格

## 概述

使用`json-render-cli`组件（`Column`、`Row`、`Container`、`Text`、`Badge`）将通用结构化数据渲染为紧凑的表格图像。此技能适用于非工单相关的表格场景。

## 工作流程

1. 确保`json-render`已安装。如果未安装，请运行`npm i -g json-render-cli`；如果Chromium未安装，请运行`npx playwright install chromium`。
2. 为当前数据集定义目标列和行结构。
3. 从表格模板中生成消息JSON数据（在内存中）。
4. 通过进程替换参数`-c <(...)`传递配置信息，以避免生成临时配置文件。
5. 当行数或换行方式不确定时，设置`screenshot.fullPage=true`。
6. 在最终渲染前调整视口宽度/高度，以适应当前内容大小，避免使用过大的固定尺寸`--size`。
7. 渲染PNG格式的图像，并返回输出路径（或仅返回Base64编码的图像）。
8. 使用`theme.mode`配置主题模式；默认使用`system`模式，根据需要强制使用`light`或`dark`模式。

## 代理协调

- 如果图像需要立即交付，优先在当前（主）代理中进行渲染。
- 仅当输出路径明确且可预测时，才将渲染任务委托给子代理。
- 确保子代理在执行过程中不会删除或移动已渲染的PNG文件。
- 仅在主代理中执行垃圾回收操作，并且仅在交付成功后进行。

## 模型路由

- 如果当前辅助模型的处理成本较高（例如Opus类模型），只有在能够执行代理协调规则的情况下，才将简单的、可预测的渲染任务路由给成本较低的快速模型（例如`gemini3flash`模型）；否则在当前主代理中进行渲染。

## 使用场景选择

- 通用表格：使用`references/compact-table-template.md`。
- 以工单为中心的表格：使用`json-render-ticket-table`。
- 信息卡（KPI/对比/摘要）：使用`json-render-info-cards`。
- 公告/标题卡：使用`json-render-announcement-cards`。
- 流程/时间线摘要：使用`json-render-flow-summary`。

## 构建与渲染

使用`references/compact-table-template.md`作为基础模板，并根据数据集自定义列和列宽。

**默认样式：**
- 无标题区域
- 紧凑的标题和正文布局
- 图像占据整个屏幕
- 列宽固定不变
- 最底行始终可见（`screenshot.fullPage=true`）

## 布局规则

- 使用`Row + Container`组合来定义列，并指定列宽。
- 保持间距紧凑且一致。
- 仅对表示状态的分类字段使用`Badge`元素。
- 当内容超出列宽时，先调整最宽的列的大小。
- 保持视口宽度接近所有列宽的总和，避免出现过多的水平空白。
- 从紧凑的视口高度开始渲染，仅在出现裁剪时才扩展视口高度。

## 输出规则

- 图像输出优先使用`-o /tmp/<name>.png`文件格式。
- 仅当调用者明确要求时，使用`-o stdout`输出Base64编码的图像数据。
- 除非有特殊需求，否则避免生成临时JSON文件。
- 如果子代理负责渲染PNG图像，仅返回输出路径，无需在该子代理中执行清理操作。
- 图像交付完成后，仅在主代理中执行最终的PNG文件清理操作。

## 故障排除

- 如果Chromium未安装，请运行`npx playwright install chromium`。
- 如果渲染结果过于宽，请减小列宽或字体大小。
- 如果左右空白区域过大，请减小视口宽度或相关列的宽度，然后重新渲染。
- 如果上下空白区域过大，请减小视口高度，然后重新渲染。
- 如果底部行被裁剪，请启用`screenshot.fullPage=true`选项。