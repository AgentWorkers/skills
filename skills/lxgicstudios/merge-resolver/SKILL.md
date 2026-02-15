---
name: merge-resolver
description: 使用人工智能智能地解决 Git 合并冲突。当用户遇到需要帮助解决的合并冲突时，请使用此功能。
---

# Merge Resolver

轻松解决 Git 合并冲突，无需繁琐的操作。它会读取存在冲突的文件，并根据两个分支的上下文选择合适的解决方式。

## 使用方法

```bash
npx ai-merge-resolve [file]
```

## 示例

```bash
# Resolve conflicts in a specific file
npx ai-merge-resolve src/index.ts

# Resolve all conflicts in the repo
npx ai-merge-resolve

# Dry run to preview resolutions
npx ai-merge-resolve --dry-run
```

## 注意事项：
- 免费、开源项目，采用 MIT 许可协议
- 由 LXGIC Studios 开发
- GitHub 仓库：https://github.com/LXGIC-Studios/ai-merge-resolve