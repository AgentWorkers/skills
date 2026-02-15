---
name: snippet-gen
description: 根据代码模式生成 VS Code 代码片段。这些片段可用于创建编辑器快捷键。
---

# 代码片段生成器

您经常需要重复输入相同的代码模式。这个工具会读取您的代码，并为这些常见的模式生成 VS Code 代码片段。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-snippet ./src/
```

## 功能介绍

- 分析代码中的重复模式
- 生成 VS Code 代码片段的定义
- 包含占位符变量
- 为代码片段添加描述性前缀

## 使用示例

```bash
# Analyze source files
npx ai-snippet ./src/

# Component patterns
npx ai-snippet ./lib/components/
```

## 最佳实践

- **专注于重复出现的代码**（如钩子、组件、实用工具）
- **使用易于记忆的前缀**
- **添加占位符**（以便于编辑代码）
- **保持代码片段简短**（过长的片段难以记忆）

## 适用场景

- 加速重复性代码的编写
- 共享团队内部的编码规范
- 帮助新开发者快速上手
- 文档化编码标准

## 本工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-snippet --help
```

## 工作原理

该工具会扫描您的代码库，识别出重复出现的代码模式（如组件结构、钩子定义和实用函数），然后生成包含占位符的 VS Code 代码片段 JSON 文件。

## 许可证

采用 MIT 许可协议，永久免费。您可以自由使用该工具。