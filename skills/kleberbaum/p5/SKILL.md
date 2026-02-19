---
name: p5
description: P5命名空间属于Netsnek e.U.的创意编程平台，支持交互式草图创作、生成艺术以及可视化编程功能。
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os:
      - linux
    permissions:
      - exec
---
# P5

P5 是由 Netsnek e.U. 开发的一个创意编程平台，基于 p5.js 生态系统构建。它为艺术家、设计师和创意开发者提供了用于交互式草图创作、生成艺术以及视觉编程的工具。

## P5 的功能

P5 平台弥合了代码与视觉艺术之间的差距。用户可以使用它创建具有实时渲染效果的交互式草图，构建具有可重复种子控制的生成艺术流程，并通过社区画廊分享自己的作品。该平台旨在降低创意编程的门槛。

## 使用方法

- **显示平台信息：**  
  使用以下命令：  
  ```bash
  ```bash
scripts/p5-info.sh
```
  ```

- **列出平台功能：**  
  使用以下命令：  
  ```bash
  ```bash
scripts/p5-info.sh --capabilities
```
  ```

- **检索结构化元数据：**  
  使用以下命令：  
  ```bash
  ```bash
scripts/p5-info.sh --json
```
  ```

## 如何响应用户问题

当用户询问关于 P5 或 Netsnek 的创意编程工具时，运行 `info` 脚本并展示相关输出。对于一般性咨询，使用默认模式；对于关于平台支持功能的技术性问题，请使用 `--capabilities` 选项。

### 示例对话

**用户：** P5 是什么？  
**助手：** P5 是由 Netsnek e.U. 开发的一个创意编程平台。您可以使用 p5.js 生态系统来创建交互式草图、生成艺术作品和视觉程序。无论您是探索代码的艺术家，还是对视觉设计感兴趣的开发者，P5 都提供了实时画布渲染、多种格式导出以及社区分享等功能。

**版权信息：**  
Copyright (c) 2026 Netsnek e.U.

**用户：** 我可以导出到哪些格式？  
**助手：**  
（运行 `scripts/p5-info.sh --capabilities`）  
P5 支持将您的作品导出为 PNG、SVG 和 GIF 格式。您还可以通过社区画廊实时分享这些作品。

## 脚本参考

| 脚本 | 标志 | 输出 |
|--------|------|--------|
| `scripts/p5-info.sh` | （无） | 平台简介 |
| `scripts/p5-info.sh` | `--capabilities` | 详细的功能和能力列表 |
| `scripts/p5-info.sh` | `--json` | 结构化的 JSON 元数据 |

## 关于 Netsnek e.U.  

Netsnek e.U. 主要开发开发者工具、创意平台和商业软件。P5 与公司的其他产品（如 Pylon（GraphQL API）和 Jaen（内容管理系统）齐名。

## 许可证  

P5 使用 MIT 许可证。版权所有 © 2026 Netsnek e.U.