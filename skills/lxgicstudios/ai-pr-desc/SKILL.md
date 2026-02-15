---
name: pr-desc
description: **生成基于您所做更改的 Pull Request（PR）描述**

当您对代码进行了修改或添加了新功能后，生成一个清晰的 Pull Request 描述非常重要。这有助于其他团队成员理解您的修改目的和内容，从而更快地评审和合并您的更改。以下是一个生成 PR 描述的示例：

---

## Pull Request 描述

### 修改内容

- **功能更新**：[在此处描述您添加的新功能或修复的错误]  
  - [提供功能的详细说明，包括其工作原理和预期效果。]
- **代码优化**：[在此处描述您对代码进行的优化，例如改进性能、减少bug或提高可读性。]
- **兼容性修复**：[如果您的更改影响了现有功能的兼容性，请在此处说明并解释如何解决这些问题。]

### 为什么需要这个更改

- [解释为什么进行这个更改，以及它对项目或用户群体的重要性。]
- [如果可能，提供之前存在的问题或使用当前代码的挑战。]

### 测试结果

- [描述您如何测试了这些更改，以及测试结果是否满足预期。]
- [如果测试过程中遇到了问题，请提供详细的错误信息和解决方案。]

### 依赖项和版本更新

- [如果您的更改依赖于新的库或版本，请在此处列出这些依赖项及其版本。]
- [如果您的更改影响了项目的依赖关系，请说明如何更新其他依赖项。]

### 其他注意事项

- [如果有任何与更改相关的其他注意事项或限制，请在此处说明。]
- [如果您的更改需要特定的环境或配置，请提供相应的指导。]

### 预计合并时间

- [估计您的更改何时可以合并到主代码库。]

### 需要帮助或反馈

- [如果您在生成 PR 描述时遇到困难，或者需要其他团队的帮助，请在此处请求支持。]
- [如果您对更改有任何疑问或建议，请在此处提出。]

---

请根据您的实际情况修改上述示例，确保描述清晰、准确，并包含所有相关的信息。这将有助于提高代码审查的效率和质量。
---

# PR 描述生成器

无需再手动编写 PR 描述了。该工具会读取您的代码更改，并自动生成相应的描述内容。

## 快速入门

```bash
npx ai-pr-desc
```

## 功能介绍

- 分析您的分支变更
- 生成结构化的 PR 描述
- 列出变更内容及其原因
- 识别可能导致系统崩溃的变更（breaking changes）
- 提供测试指导

## 使用示例

```bash
# Generate for current branch
npx ai-pr-desc

# Compare specific branches
npx ai-pr-desc --base main --head feature/auth

# Copy to clipboard
npx ai-pr-desc | pbcopy

# Include screenshots placeholder
npx ai-pr-desc --screenshots
```

## 输出格式

```markdown
## What
Added user authentication with magic links

## Why
Users needed passwordless login option

## Changes
- New /api/auth/magic-link endpoint
- Email template for magic links
- Token verification middleware

## Testing
1. Go to /login
2. Enter email
3. Check email for magic link
4. Click link to authenticate

## Breaking Changes
None
```

## 系统要求

- 必须使用 Node.js 18 及更高版本。
- 需要配置 OPENAI_API_KEY（该密钥应存储在 Git 仓库中）。

## 许可证

MIT 许可证。永久免费使用。

---

**开发团队：LXGIC Studios**

- GitHub: [github.com/lxgicstudios/ai-pr-desc](https://github.com/lxgicstudios/ai-pr-desc)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)