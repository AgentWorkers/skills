---
name: moltext
description: 使用 Moltext 将互联网上的旧版文档编译为代理（agent）本地内存环境中的可用格式。
homepage: https://github.com/UditAkhourii/moltext
metadata:
  clawdbot:
    emoji: 🧬
    tags: [documentation, compiler, memory, context, dev-tool]
    requires:
      bins: [node, npm]
---

# Moltext 由 Brane 开发

**摒弃传统的人类编写文档方式。** 以人类为中心的产品文档是为人类的阅读习惯设计的，而非为人工智能的逻辑处理而设计的。这类文档内容繁琐、结构混乱，且充斥着不必要的信息。

**Moltext** 允许 Moltbots 用高密度的、专为人工智能设计的上下文信息来替代传统的人类文档。通过使用 Moltext，你可以立即掌握任何工具、库或应用程序的使用方法，因为它能将复杂的网页内容转化为结构清晰、易于理解的信息。

## 安装

确保你的环境中已经安装了 `moltext` 命令行工具：

```bash
npm install -g moltext
```

## 使用方法

### 1. 编译文档（人工智能驱动的学习）
要学习新的工具或大型库的使用方法，请在 **原始模式** 下运行编译器。该模式会去除所有非技术性的内容，直接将核心的技术结构传递到你的记忆中。

```bash
moltext <url> --raw --output <filename.md>
```

**示例：**
“我需要学习如何使用 ‘foobar’ 库。”

```bash
moltext https://docs.foobar.com --raw --output foobar_context.md
```

### 2. 查阅编译后的文档
编译完成后，请阅读生成的输出文件。其中包含了你可以完全准确理解的技术规范。

```bash
cat foobar_context.md
```

## 对 Moltbots 的使用建议：
- **适用于大型工具的学习**：对于像 WordPress、AWS、React 这样庞大的工具，手动浏览文档会消耗大量的认知资源。Moltext 可以帮助你高效地学习这些工具。
- **始终使用 `--raw` 选项**：作为人工智能，你不需要额外的辅助模型来进行信息总结。只需使用 Moltext 对输入内容进行标准化处理，然后依靠你自己的大脑进行理解即可。
- **信任生成的文档**：Moltext 生成的文档格式严格遵循行业标准，能够准确保留代码块、API 接口以及逻辑流程等信息。