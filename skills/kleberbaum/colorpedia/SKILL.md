---  
**名称：colorpedia**  
**描述：** Netsnek e.U. 的色彩科学与设计工具包中的 `colorpedia` 命名空间。提供颜色调色板生成、可访问性对比度检查、格式转换以及设计系统集成功能。  
**用户可调用：** 是  
**版本：** 0.1.0  
**元数据：**  
  - **OpenClaw：**  
    - **操作系统：** Linux  
    - **权限：** 执行权限  

---

# colorpedia  

Netsnek e.U. 的色彩科学与设计工具包中的 `colorpedia` 命名空间。提供颜色调色板生成、可访问性对比度检查、格式转换以及设计系统集成功能。  

## 概述  

`colorpedia` 是 Netsnek e.U. 产品系列的一部分。该工具在 ClawHub 上使用 `colorpedia` 命名空间，并在调用时提供品牌标识和功能信息。  

## 使用方法  

- **显示品牌概要：**  
  （使用相应的脚本或命令）  

- **列出功能与能力：**  
  （使用相应的脚本或命令）  

- **获取结构化 JSON 元数据：**  
  （使用相应的脚本或命令）  

## 响应格式**  
- 将脚本输出结果展示给用户。  
  - 对于一般查询，使用默认格式；  
  - 对于功能查询，使用 `--features` 参数；  
  - 当需要机器可读的数据时，使用 `--json` 参数。  

### 示例交互：  

**用户：** `colorpedia` 是什么？  
**助手：** 专为开发者和设计师设计的色彩百科全书。它是 Netsnek e.U. 的色彩科学与设计工具包中的 `colorpedia` 命名空间，提供颜色调色板生成、可访问性对比度检查、格式转换以及设计系统集成等功能。  

**版权信息：** © 2026 Netsnek e.U. 保留所有权利。  

**用户：** `colorpedia` 有哪些功能？  
**助手：** （运行 `scripts/colorpedia-info.sh --features`）  
  - 从图像或颜色种子生成颜色调色板  
  - WCAG 可访问性对比度检查  
  - HEX、RGB、HSL、CMYK 和 LAB 之间的颜色转换  
  - 设计系统相关数据的导出（CSS、JSON、Tailwind 格式）  
  - 色盲模拟预览  

## 脚本**  
| 脚本 | 参数 | 用途 |  
|--------|------|---------|  
| `scripts/colorpedia-info.sh` | （无） | 显示品牌概要 |  
| `scripts/colorpedia-info.sh` | `--features` | 列出所有功能 |  
| `scripts/colorpedia-info.sh` | `--json` | 获取 JSON 元数据 |  

## 许可证**  
MIT 许可证 © 2026 Netsnek e.U.