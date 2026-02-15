---
name: bundle-checker
description: 分析软件包的大小，并获取减少其大小的AI建议。当你的构建文件变得过于庞大（即文件大小不断增加）时，可以使用此方法。
---

# 包体积检查工具（Bundle Checker）

你的应用程序包体积达到了2MB，但你不清楚具体是哪些部分导致了这么大的文件大小。这个工具会分析你的构建输出，准确地指出哪些部分占用了大量空间，并告诉你如何解决这个问题。

**只需一个命令，无需任何配置设置，即可立即使用。**

## 快速入门

```bash
npx ai-bundle-check
```

## 工具功能

- 分析你的应用程序包的组成结构
- 识别占用空间最大的依赖库
- 提出优化建议（例如通过“树摇动”（tree-shaking）技术来减少代码体积）
- 推荐更轻量级的替代方案

## 使用示例

```bash
# Analyze current project
npx ai-bundle-check

# Analyze specific directory
npx ai-bundle-check ./my-project/

# Get detailed breakdown
npx ai-bundle-check --verbose
```

## 最佳实践

- **在发布前进行检查**：尽早发现包体积的异常变化
- **考虑使用替代库**：例如，moment.js 和 date-fns 之间的性能差异可能很大
- **使用动态导入**：将不立即需要的代码分开加载
- **监控包体积的变化**：在持续集成（CI）过程中持续跟踪包体积

## 适用场景

- 当你的应用程序加载速度较慢时，怀疑是包体积过大所致
- 添加新依赖库后，需要检查其对应用程序性能的影响
- 性能审计发现 JavaScript 代码体积过大
- 持续集成过程中的包体积检查失败

## 该工具属于 LXGIC 开发工具包（LXGIC Dev Toolkit）的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具前需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-bundle-check --help
```

## 工作原理

该工具会扫描你的 `package.json` 文件和构建输出文件，识别出占用大量空间的依赖库，并将分析结果发送给 GPT-4o-mini。GPT-4o-mini 能够识别常见的包体积膨胀问题，并提供具体的优化建议，比如更换依赖库或调整代码结构以减少体积。

## 许可证

采用 MIT 许可协议，永久免费使用。你可以随意使用该工具。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/ai-bundle-check](https://github.com/lxgicstudios/ai-bundle-check)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)