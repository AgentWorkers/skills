---
name: typescript-lsp
description: TypeScript语言服务器，为.ts、.tsx、.js、.jsx、.mts、.cts、.mjs、.cjs文件提供类型检查、代码智能提示以及LSP（Language Server Protocol）诊断功能。适用于需要类型检查、自动补全、错误检测、重构支持或代码导航的TypeScript或JavaScript项目。
---

# TypeScript LSP

TypeScript/JavaScript 语言服务器集成，通过 `typescript-language-server` 提供全面的代码智能支持。

## 功能

- **类型检查**：对 TypeScript 和 JavaScript 代码进行静态类型分析
- **代码智能**：自动补全、跳转到定义、查找引用、重命名符号
- **错误检测**：实时诊断类型错误、语法问题以及语义问题
- **重构**：提取函数/变量、整理导入语句、提供快速修复功能
- **支持的文件扩展名**：`.ts`、`.tsx`、`.js`、`.jsx`、`.mts`、`.cts`、`.mjs`、`.cjs`

## 安装

安装 TypeScript 语言服务器和 TypeScript 编译器：

```bash
npm install -g typescript-language-server typescript
```

或者使用 yarn：

```bash
yarn global add typescript-language-server typescript
```

验证安装是否成功：

```bash
typescript-language-server --version
tsc --version
```

## 使用方法

该语言服务器会在支持 LSP 的编辑器中自动运行。如需手动进行类型检查：

```bash
tsc --noEmit  # Type check without generating output files
```

编译 TypeScript 文件：

```bash
tsc src/index.ts
```

启用监控模式以实现持续类型检查：

```bash
tsc --watch --noEmit
```

## 配置

在项目根目录下创建 `tsconfig.json` 文件：

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ESNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## 集成方式

在编辑 TypeScript/JavaScript 代码时：
1. 在进行重大修改后运行 `tsc --noEmit`
2. 在提交代码前解决类型错误
3. 在开发过程中使用 `tsc --watch` 模式
4. 利用快速修复功能解决常见问题

## 常用命令参数

- `--noEmit`：仅进行类型检查，不生成输出文件
- `--strict`：启用所有严格的类型检查选项
- `--watch`：启用监控模式以实现持续编译
- `--project <path>`：指定 `tsconfig.json` 文件的位置
- `--pretty`：美化错误信息和提示

## 更多信息

- [typescript-language-server 在 npm 上的官方页面](https://www.npmjs.com/package/typescript-language-server)
- [GitHub 仓库](https://github.com/typescript-language-server/typescript-language-server)
- [TypeScript 官方文档](https://www.typescriptlang.org/docs/)
- [TypeScript 编译器配置选项](https://www.typescriptlang.org/tsconfig)