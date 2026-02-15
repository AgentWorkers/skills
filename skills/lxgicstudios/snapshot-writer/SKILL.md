---
name: snapshot-writer
description: 为 React 组件生成 Jest 快照测试。当您需要为 UI 组件提供快照覆盖时，请使用此方法。
---

# 快照测试生成工具

快照测试是检测UI意外变化的最快捷方法。但为每个组件都编写这样的测试会变得非常繁琐。这款工具可以自动读取你的React组件，并自动生成相应的快照测试。它会识别组件的属性（props），渲染组件，并创建相应的快照断言（snapshot assertions）。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-snapshot-test src/components/
```

## 功能介绍

- 自动读取React组件并生成Jest快照测试文件
- 检测组件的属性，并为不同的属性组合生成测试用例
- 支持带有上下文提供者（context providers）和包装器依赖（wrapper dependencies）的组件
- 生成组件的默认状态快照以及边缘情况（edge case）快照
- 生成可直接用于Jest测试的`.test.tsx`文件

## 使用示例

```bash
# Generate snapshot tests for all components
npx ai-snapshot-test src/components/

# Target a specific component
npx ai-snapshot-test src/components/Button.tsx

# Scan all TSX files in a directory
npx ai-snapshot-test "src/**/*.tsx"
```

## 最佳实践

- **在开发早期就生成快照**：从小规模项目开始，后续维护会更加方便
- **有意图地更新快照**：当快照测试失败时，先确认修改是否是预期的
- **不要为所有组件都生成快照**：重点关注输出结果稳定的组件；高度动态的组件不适合生成快照
- **将快照文件纳入版本控制**：它们是代码的“可视化契约”（visual contract）

## 适用场景

- 当你正在构建组件库并需要防止代码回退（regression protection）时
- 当组件设计发生重大变更，需要更新测试覆盖率时
- 当你在重构代码时希望捕获意外的渲染变化时
- 当团队需要快照测试，但没人愿意手动编写这些测试时

## 该工具属于LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要API密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。

```bash
npx ai-snapshot-test --help
```

## 工作原理

该工具会解析你的React组件文件，提取组件的结构信息、属性接口以及所有依赖项。然后它会生成测试文件，这些文件会导入组件，并使用不同的属性组合对其进行渲染，最后创建`toMatchSnapshot`断言。生成的测试结果与Jest的快照测试机制兼容。

## 许可证

采用MIT许可证。永久免费，你可以随心所欲地使用它。