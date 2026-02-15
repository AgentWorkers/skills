---
name: deps-analyzer
description: **查找未使用或过时的依赖项**  
当你的 `package.json` 文件变得混乱不堪时，可以使用这个方法来清理其中不再需要的依赖项。
---

# 依赖项分析工具

你的 `package.json` 文件中包含了 87 个依赖项，但你可能只使用了其中的 40 个左右。这个工具可以帮你识别那些“无用”的依赖项，并告诉你该如何处理它们。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-deps
```

## 工作原理

- 查找可以移除的未使用依赖项
- 标记存在安全问题的过时包
- 解释每个问题依赖项的功能
- 可以自动移除未使用的依赖项以解决问题

## 使用示例

```bash
# Audit current project
npx ai-deps

# Auto-remove unused deps
npx ai-deps --fix

# Check a specific directory
npx ai-deps --dir ./my-project
```

## 最佳实践

- **在重大更新前运行**：升级前先清理依赖项
- **也检查 `devDependencies`：**开发工具可能会变得过时
- **修复前先审查**：某些依赖项可能是动态加载的
- **修复后更新 `lockfile`：**移除依赖项后重新运行 `npm install`

## 适用场景

- 安装过程耗时过长
- 项目包的大小过大
- `npm audit` 报告了 47 条警告
- 继承了一个包含未知依赖项的项目

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。完全免费，无需注册或使用 API 密钥，只需简单使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需额外安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-deps --help
```

## 工作流程

首先运行 `depcheck` 来识别未使用的依赖项，然后使用 `npm outdated` 命令检查过时的依赖项。分析结果会发送给 GPT-4o-mini 进行处理，该工具会解释每个问题并确定优先处理的顺序。

## 许可证

MIT 许可证。永久免费，你可以随意使用。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/ai-deps](https://github.com/lxgicstudios/ai-deps)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)