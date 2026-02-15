---
name: stash-namer
description: 从你的更改中生成有意义的 Git Stash 名称。在将工作内容暂存到 Git 仓库时使用这些名称。
---

# Stash Namer

不要再将暂存区（stash）命名为“WIP”或保持未命名状态了。该工具会自动读取您的更改内容，并为暂存区生成一个有意义的名称。

**仅需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-stash-name
```

## 功能说明

- 读取您已暂存（staged）和未暂存（unstaged）的更改内容  
- 为暂存区生成一个描述性的名称  
- 使用该名称执行 `git stash` 操作  

## 使用示例

```bash
# Stash with auto-generated name
npx ai-stash-name

# Preview without stashing
npx ai-stash-name --dry-run
```

## 最佳实践  

- **尽早暂存，频繁使用暂存区**——这是免费的  
- **为暂存区起一个合适的名称**——未来的你会为此感到庆幸  
- **不要过度积累暂存区中的更改**——及时应用或删除它们  
- **仅在使用时才“弹出”暂存内容（pop）**——除非你需要保留这些更改  

## 适用场景  

- 快速切换工作环境  
- 在拉取代码之前保存当前的工作状态  
- 在进行代码实验时使用  
- 任何需要使用 `git stash` 的场景  

## 属于 LXGIC 开发工具包的一部分  

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能正常使用。  

**了解更多信息：**  
- GitHub: https://github.com/LXGIC-Studios  
- Twitter: https://x.com/lxgicstudios  
- Substack: https://lxgicstudios.substack.com  
- 官网: https://lxgicstudios.com  

## 系统要求  

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。  

```bash
npx ai-stash-name --help
```

## 工作原理  

首先运行 `git diff` 命令查看您的更改内容，然后将差异摘要发送给 GPT-4o-mini 以生成一个描述性的名称，最后使用该名称执行 `git stash push -m` 操作。  

## 许可证  

采用 MIT 许可协议，永久免费。您可以随意使用该工具。