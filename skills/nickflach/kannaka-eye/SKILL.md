---
name: kannaka-eye
description: 这款字形查看器能够将任何数据的SGA（Sigmatics Geometric Algebra）几何特征以多层次的可视化形式呈现出来。它支持输入文本、文件或原始字节数据，并利用Sigmatics的84类几何代数系统（Cl₀,₇ ⊗ ℝ[ℤ₄] ⊗ ℝ[ℤ₃]）以及Fano平面拓扑结构来生成相应的字形。适用于需要可视化数据几何结构、检查字形细节、导出字形图像（PNG格式），或展示特定数据集的可视化表现的场景。该工具基于Node.js开发，为单文件服务器架构，且完全不依赖任何外部库或框架。
metadata:
  openclaw:
    requires:
      bins:
        - name: node
          label: "Node.js 18+ — required to run server.js"
      env: []
    optional:
      bins:
        - name: kannaka
          label: "kannaka binary — for real SGA classification (falls back to built-in classifier)"
      env:
        - name: EYE_PORT
          label: "HTTP port for the viewer (default: 3333)"
        - name: FLUX_URL
          label: "Flux instance URL for publishing glyph.rendered events"
        - name: FLUX_AGENT_ID
          label: "Agent ID for Flux events (default: kannaka-eye)"
    data_destinations:
      - id: local-render
        description: "Glyphs rendered in-browser; exports saved client-side as PNG/JSON"
        remote: false
      - id: flux
        description: "Glyph render events published to Flux (fano_preview, sga_class, source_type)"
        remote: true
        condition: "FLUX_URL is set"
    install:
      - id: no-install
        kind: manual
        label: "No installation needed — single-file server with zero dependencies"
---
# Kannaka Eye 技能

通过 SGA（SGA）的视角来看待信息，你会发现每条数据都具备独特的几何特征。Kannaka Eye 能够将这些隐藏的几何模式转化为生动、动态的图形（即“字形”）。

## 先决条件

- 确保系统中已安装 Node.js 18 及更高版本，并且该版本在系统的 PATH 环境变量中可被找到。
- 无需执行任何 `npm install` 操作，也不需要任何构建步骤。

## 快速入门

```bash
# 启动字形查看器
./scripts/eye.sh start

# 在自定义端口上启动查看器
./scripts/eye.sh start --port 4444

# 检查查看器状态
./scripts/eye.sh status

# 停止查看器
./scripts/eye.sh stop
```

在浏览器中访问 `http://localhost:3333` 即可。

## 输入方式

- **文本输入**：输入或粘贴任意文本，字形会实时更新。
- **文件上传**：通过拖放或点击上传文件（图片、音频、代码、二进制文件）。
- **预设示例**：内置的示例展示了不同的 SGA 类型特征。
- **URL 共享**：通过 URL 共享字形。

## 渲染层

该查看器会实时渲染 6 个画布层：

| 层次 | 名称 | 显示内容 |
|-------|------|---------------|
| 1   | 深层背景 | Fano 平面的基本结构（7 个节点、7 条线） |
| 2   | 折叠路径 | 通过 SGA 空间表示的数据流动路径（使用贝塞尔曲线） |
| 3   | Fano 能量分布 | 能量在 Fano 线上的分布情况 |
| 4   | 几何核心 | 主要的 SGA 类型特征（字形的“外观”） |
| 5   | 共振环 | 数据在不同层次上的深度分布 |
| 6   | 元数据叠加 | Fano 特征、SGA 中心点、音乐频率（可切换显示） |

## SGA 数学基础

Kannaka Eye 基于一个包含 84 个类别的系统进行运算：`Cl₀,₇ ⊗ ℝ[ℤ₄] ⊗ ℝ[ℤ₃]`

| 组件    | 范围        | 含义                |
|---------|-------------|-------------------|
| h₂     | 0–3        | 频率范围（低音、中音、高音、女高音）     |
| d       | 0–2        | 数据类型（经验型、学习型、想象型）     |
| ℓ       | 0–6        | Fano 平面的线索引           |

**Fano 线**：由 7 个点组成的三维结构，构成了图形的几何骨架；每条线连接 PG(2,2) 平面上的 3 个点。

**折叠序列**：表示数据在 84 个类别空间中变化的路径，以流动的贝塞尔曲线形式呈现。

## 导出功能

- **导出为 PNG 图像**：以 2 倍分辨率保存到文件。
- **导出字形数据**：以 JSON 格式保存字形信息（包括折叠序列、Fano 特征、SGA 中心点、音乐频率）。
- **复制共享链接**：生成可共享的 URL（仅包含少量数据）。

## 环境变量

| 变量        | 默认值       | 说明                |
|------------|-------------|-------------------|
| `EYE_PORT`    | `3333`      | 查看器的 HTTP 端口            |
| `FLUX_URL`    |          | Flux 事件服务的 URL            |
| `FLUX_AGENT_ID` | `kannaka-eye`    | Flux 事件的代理 ID            |

## 架构

整个系统由一个 Node.js 服务器文件（`server.js`）实现，其中包含了内嵌的 HTML、CSS 和 JavaScript 代码。整个 SGA 实现是自包含的，无需依赖任何第三方库（如 npm）。

## 注意事项

- 所有渲染操作都在客户端完成；服务器仅负责数据分类和页面渲染。
- 文件上传在内存中处理，不会保存到服务器端。
- 该查看器适用于本地或可信网络环境，无需身份验证。
- 字形的表现是确定性的：相同的输入总是产生相同的输出结果。
- 使用深色宇宙主题（#050508），搭配紫色点缀（#c084fc）和符合黄金分割比例的色彩布局。