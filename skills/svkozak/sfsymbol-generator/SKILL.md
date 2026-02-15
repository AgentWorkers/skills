---
name: sfsymbol-generator
description: **从 SVG 文件生成 Xcode 的 SF Symbol 资产目录（.symbolset）**  
当您需要通过创建 `symbolset` 文件夹、`Contents.json` 文件以及 SVG 文件来添加自定义的 SF Symbol（在构建时使用）时，可以使用此方法。
---

# SF Symbol Generator

## 使用方法

您可以通过设置 `SFSYMBOL_ASSETS_DIR` 来覆盖默认的资产目录路径。

### 原始符号集（不使用模板）

```bash
./scripts/generate.sh <symbol-name> <svg-path> [assets-dir]
```

- `symbol-name`：完整的符号名称（例如 `custom.logo`、`brand.icon.fill`）。
- `svg-path`：源 SVG 文件的路径。
- `assets-dir`（可选）：`Assets.xcassets/Symbols` 目录的路径（默认值为 `Assets.xcassets/Symbols` 或 `SFSYMBOL_ASSETS_DIR`）。

### 基于模板的符号集（推荐）

```bash
./scripts/generate-from-template.js <symbol-name> <svg-path> [template-svg] [assets-dir]
```

- `template-svg`（可选）：用于插入的 SF Symbols 模板 SVG 文件（默认使用 `Assets.xcassets/Symbols` 目录中第一个找到的 `.symbolset` SVG 文件；如果没有找到，则使用捆绑提供的模板）。

## 示例

```bash
./scripts/generate-from-template.js pi.logo /Users/admin/Desktop/pi-logo.svg
```

## 要求

- SVG 文件必须包含 `viewBox` 属性。
- 使用基于路径的图形元素（路径是必需的；矩形（Rects）也是支持的，但其他形状应转换为路径）。
- 建议使用填充过的图形（无描边），以避免出现细小的线条瑕疵。

## 工作流程

1. 验证 SVG 文件的路径和 `viewBox` 属性。
2. 计算图形元素的边界，并将其居中到 SF Symbols 模板的边界内。
3. 将图形元素的路径插入到 SF Symbols 模板中（支持 Ultralight、Regular、Black 三种样式）。
4. 在资产目录的 `Symbols` 文件夹中创建一个名为 `<symbol-name>.symbolset` 的文件。
5. 生成相应的 `Contents.json` 文件。