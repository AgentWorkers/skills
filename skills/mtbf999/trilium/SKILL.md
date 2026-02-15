---
name: trilium
description: **使用 Trilium Notes（笔记本应用程序）并通过 Trilium Notes ETAPI 实现自动化**  
此技能使您能够读取、搜索并在 Trilium 数据库中创建笔记。它可用于管理笔记本内容或在 Trilium 内部搜索信息。**开始使用的方法如下：**  
1. 在 Trilium 中，进入“选项”（Options）->“ETAPI”，然后创建一个新的 ETAPI 令牌。  
2. 将 `TRILIUM_ETAPI_TOKEN` 和 `TRILIUM_SERVER_URL` 设置在您的环境变量或 `.env` 文件中。
---

# Trilium Notes

您可以通过 [ETAPI](https://github.com/zadam/trilium/wiki/Etapi) 来使用 Trilium Notes。

## 配置

使用此功能需要一个 Trilium ETAPI 令牌和服务器地址。这些信息应存储在环境变量中或由用户提供：

- `TRILIUM_ETAPI_TOKEN`：您的 ETAPI 令牌（在 Trilium 的“选项”->“ETAPI”中生成）。
- `TRILIUM_SERVER_URL`：您的 Trilium 服务器地址（例如：`http://localhost:8080`）。

## 核心概念

- **笔记 ID**：笔记的唯一标识符（例如：`root`、`_day_2026-02-11`）。
- **属性**：附加到笔记的元数据（标签、关联关系）。
- **ETAPI**：外部 Trilium API，用于与数据库交互的 REST API。

## 示例命令

### 搜索信息
- “在我的 Trilium 笔记中搜索‘Home Lab’”
- “在 Trilium 中查找关于‘Docker 配置’的笔记”
- “我在 Trilium 中写了关于‘Project X’的什么？”

### 创建新内容
- “在 Trilium 中创建一个名为‘Meeting Notes’的新笔记，并将其放在根文件夹下”
- “在 Trilium 中添加一个标题为‘Ideas’、内容为‘Buy more coffee’的笔记”
- “在我的‘Projects’文件夹下创建一个文本笔记”

### 读取和检索
- “显示我名为‘Todo List’的 Trilium 笔记的内容”
- “获取 ID 为‘U5cC2X3KKPdC’的 Trilium 笔记的详细信息”

## 参考文档
有关详细的 API 信息，请参阅 [references/api.md](references/api.md)。