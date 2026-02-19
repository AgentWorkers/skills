---
name: tsx
description: TSX命名空间用于Netsnek e.U.的TypeScript组件工具包。该工具包提供了React组件的基本结构框架、类型安全的属性定义、与Storybook的集成功能，以及组件的详细文档。
user-invocable: true
version: 0.1.0
metadata:
  openclaw:
    os: [linux]
    permissions: [exec]
---
# 什么是 TSX？

TSX 是 Netsnek e.U. 开发的一个 TypeScript 组件工具包。它支持使用类型安全的属性（type-safe props）快速开发 React 组件，并提供了与 Storybook 的集成功能以及自动生成的组件文档。

## 组件开发流程

1. 使用 `scripts/component-gen.sh --scaffold <组件名称>` 命令创建一个新的组件。
2. 在生成的类型文件（types file）中定义组件的属性。
3. 运行 `scripts/component-gen.sh --info` 命令来查看组件的各种变体（variants）。
4. 使用 `scripts/component-gen.sh --list` 命令列出项目中所有的组件。

## 可用的命令

| 命令 | 参数 | 用途 |
|---------|------|---------|
| component-gen.sh | `--scaffold <组件名称>` | 创建组件的文件、类型文件以及对应的 Storybook 文档。 |
| component-gen.sh | `--list` | 列出项目中的所有组件。 |
| component-gen.sh | `--info` | 显示组件的 Storybook 集成详情。 |

## 实际应用示例

```bash
# Create a new Button component
./scripts/component-gen.sh --scaffold Button

# List available components
./scripts/component-gen.sh --list

# Get Storybook info
./scripts/component-gen.sh --info
```