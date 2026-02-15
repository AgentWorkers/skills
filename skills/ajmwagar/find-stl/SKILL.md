---
name: find-stl
description: 您可以通过查询“Printables”来搜索和下载可用于打印的 3D 模型文件（格式为 STL、3MF 或 ZIP）。当代理需要查找现有的模型、获取其许可证/版权信息、下载源文件，并生成可用于报价或打印的本地文件夹及文件清单时，可以使用此功能。
---

# find-stl

该技能提供了一个确定性的工作流程：
- 在 Printables 平台上搜索模型
- 选择合适的模型
- 下载模型文件
- 生成一个 `manifest.json` 文件（包含源 URL、作者信息、许可证 ID、文件列表以及文件的哈希值）

## 快速入门

### 搜索

```bash
python3 scripts/find_stl.py search "iphone 15 pro dock" --limit 10
```

### 下载模型文件

```bash
python3 scripts/find_stl.py fetch 1059554 --outdir out/models
```

默认情况下，如果模型文件可用，该脚本会下载所有模型文件（以 ZIP 格式）。

## 注意事项

- Printables 的下载链接具有时效性；该脚本通过 Printables 的 GraphQL 接口（`getDownloadLink`）来获取这些链接。
- 确保在 `manifest.json` 文件中始终保留模型的许可证信息和来源信息。

## 资源

- `scripts/find_stl.py`