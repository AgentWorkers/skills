---
name: merge-resolve
description: 基于人工智能的 Git 合并冲突解决
---

# 合并冲突解决工具

遇到合并冲突了吗？这款工具可以理解两个版本的代码差异，并选择合适的解决方式。

## 快速入门

```bash
npx ai-merge-resolve
```

## 功能介绍

- 查找仓库中的所有合并冲突  
- 从语义层面分析两个版本的代码差异  
- 提出智能的解决方案  
- 能够自动解决简单的冲突  

## 使用示例

```bash
# Resolve all conflicts
npx ai-merge-resolve

# Resolve specific file
npx ai-merge-resolve ./src/api.ts

# Auto-resolve obvious ones
npx ai-merge-resolve --auto

# Interactive mode
npx ai-merge-resolve --interactive
```

## 工作原理

该工具不会简单地选择“对方的代码”或“我们的代码”，而是会实际读取代码内容，理解开发者的意图，并正确地合并代码功能。  

## 输出结果

```
Resolving src/utils.ts...
- Conflict 1: Both added logging → Combined both log statements
- Conflict 2: Different error messages → Kept more descriptive one
✓ Resolved 2 conflicts
```

## 系统要求

- 必须安装 Node.js 18 及以上版本。  
- 需要配置 OPENAI_API_KEY。  
- 仓库中必须存在有效的合并冲突。  

## 许可证

MIT 许可证。永久免费使用。  

---

**开发团队：LXGIC Studios**  
- GitHub: [github.com/lxgicstudios/ai-merge-resolve](https://github.com/lxgicstudios/ai-merge-resolve)  
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)