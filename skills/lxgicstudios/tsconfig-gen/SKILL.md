---
name: tsconfig-gen
description: 为您的项目类型生成最优的 `tsconfig.json` 配置文件。在设置 TypeScript 项目时，请使用该配置文件。
---

# TSConfig Generator

无需阅读文档，即可为您的项目生成合适的 `tsconfig` 配置文件。只需告诉它您的项目类型，它就会为您配置好 TypeScript 开发环境。

**一个命令即可完成所有配置。**  

## 快速入门

```bash
npx ai-tsconfig "next.js app with strict mode"
```

## 工作原理

- 生成符合您项目类型的 `tsconfig.json` 文件  
- 设置正确的模块解析方式和运行时目标  
- 配置路径别名以及需要包含或排除的文件  
- 启用适当的严格模式（strict mode）选项  
- 支持库项目、应用程序项目以及单仓库（monorepo）的配置  

## 使用示例

```bash
# Next.js project
npx ai-tsconfig "next.js 14 app router"

# Node.js library
npx ai-tsconfig "node library targeting esm and cjs"

# React app with Vite
npx ai-tsconfig "react spa with vite, strict mode"
```

## 最佳实践  

- **匹配您的运行时环境**：Node.js 18 及更高版本可以使用 `esnext` 规范，旧版本则需要降级兼容性设置  
- **逐步启用严格模式**：如果从 JavaScript 迁移过来，建议初始时将 `strict` 设置为 `false`  
- **使用项目内部的引用**：对于单仓库项目，应为每个包生成单独的配置文件  
- **保持路径简洁**：将 `@/` 别名为 `src/` 即可  

## 适用场景  

- 新建 TypeScript 项目  
- 将现有的 `tsconfig` 配置升级为现代标准  
- 了解各个编译器选项的实际作用  
- 为发布软件包配置构建环境  

## 属于 LXGIC 开发工具包（LXGIC Dev Toolkit）的一部分  

LXGIC Studios 开发了 110 多款免费开发工具，这款工具属于其中之一。免费版本完全无付费门槛、无需注册，也不需要 API 密钥，只需使用即可。  

**了解更多信息：**  
- GitHub: https://github.com/LXGIC-Studios  
- Twitter: https://x.com/lxgicstudios  
- Substack: https://lxgicstudios.substack.com  
- 官网: https://lxgic.dev  

## 使用要求  

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。  

```bash
npx ai-tsconfig --help
```

## 工作机制  

该工具会根据您的项目描述自动匹配相应的 TypeScript 编译器选项，确保各项配置相互兼容，避免出现冲突。生成的配置文件为有效的 JSON 格式，并包含对每个选项的详细说明。  

## 许可证  

MIT 许可证。永久免费使用，可随意支配该工具的用途。