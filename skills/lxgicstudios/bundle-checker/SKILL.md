---
name: bundle-checker
description: 分析软件包的大小，并获取减少其大小的AI建议。当你的构建文件变得过于庞大（即文件大小不断增加）时，可以使用此方法。
---

# 包体积检查工具（Bundle Checker）

你的项目生成的包文件体积达到了2MB，但你却不知道具体是哪些部分导致了这么大的文件大小。这个工具会分析你的构建输出，精确地指出哪些部分占用了过多的空间，并提供相应的解决方案。

**只需一条命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-bundle-check
```

## 功能介绍

- 分析你的包文件结构
- 识别占用空间最大的依赖项
- 提出优化建议（例如通过“tree-shaking”技术减少代码体积）
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

- **在发布前进行检查**：及早发现文件大小的异常变化
- **考虑使用替代库**：比如使用`moment.js`代替`date-fns`可以显著减少文件大小
- **使用动态导入**：将不立即需要的代码分开加载
- **监控文件大小趋势**：在持续集成（CI）过程中定期检查包文件大小

## 适用场景

- 当你的应用程序加载速度较慢时，怀疑是包文件体积过大导致的
- 添加新依赖项后，需要了解其对项目性能的影响
- 当性能审计指出JavaScript代码体积过大时
- 当持续集成过程中的包文件大小检查失败时

## 该工具属于LXGIC开发工具包（LXGIC Dev Toolkit）的一部分

这是LXGIC Studios开发的110多个免费开发者工具之一。免费版本完全免费，无需注册或使用API密钥，只需使用即可。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用`npx`命令运行即可。建议使用Node.js 18及以上版本。运行该工具需要设置`OPENAI_API_KEY`环境变量。

```bash
npx ai-bundle-check --help
```

## 工作原理

该工具会扫描你的`package.json`文件和构建输出文件，识别出占用大量空间的依赖项，并将分析结果发送给GPT-4o-mini模型。GPT-4o-mini能够识别常见的代码冗余模式，并提供具体的优化建议（如更换库或使用“tree-shaking”技术）。

## 许可证

采用MIT许可证，永久免费。你可以自由使用该工具。