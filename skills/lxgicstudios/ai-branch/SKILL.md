---
name: branch-namer
description: 从普通的英文描述生成符合规范的 Git 分支名称。当您需要一个遵循特定规则的分支名称时，可以使用这种方法。
---

# 分支命名工具

为分支命名其实比想象中要困难得多。是应该命名为“feature/user-auth”还是“feat/add-user-authentication”呢？这个工具可以根据简单的英文描述自动生成一致且符合常规的分支名称。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-branch "add user authentication with OAuth"
```

## 功能介绍

- 生成符合常见命名规范的分支名称（如：feature/、bugfix/、hotfix/）
- 名称简洁但具有描述性
- 始终使用驼峰式命名法（kebab-case）
- 可通过`--create`选项帮助你创建分支
- 支持自定义前缀和命名格式

## 使用示例

```bash
# Get a branch name suggestion
npx ai-branch "fix the login button not working on mobile"

# Create the branch immediately
npx ai-branch "add dark mode support" --create

# Use a specific prefix
npx ai-branch "update dependencies" --prefix chore

# Include ticket number
npx ai-branch "user profile page crashes on load" --ticket PROJ-123
```

## 最佳实践

- **描述要具体**：例如，“fix bug”不如“fix crash when user has no profile photo”更具描述性
- **包含上下文**：提及功能相关的具体内容，如：“checkout flow: add shipping address validation”
- **谨慎使用`--create`选项**：尤其是在共享仓库中，请先仔细考虑建议的分支名称
- **遵循团队规范**：如果团队有特定的前缀要求，请使用`--prefix`选项

## 适用场景

- 当你需要为新功能命名但一时想不出合适的分支名称时
- 当希望团队内所有分支的命名保持一致时
- 当同时处理多个任务并需要清晰地追踪每个分支的用途时
- 对新成员进行培训时，如果不确定团队使用的命名规则

## 本工具属于LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发者工具之一。免费版本完全无付费门槛、无需注册，也不需要API密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。运行时需要设置`OPENAI_API_KEY`环境变量。

```bash
export OPENAI_API_KEY=sk-...
npx ai-branch --help
```

## 工作原理

该工具会分析你的描述，判断分支的类型（如功能开发、bug修复、杂务等），提取关键信息，并根据常规命名规则生成简洁易读的分支名称。你也可以选择通过`git checkout -b`命令来创建分支。

## 许可证

采用MIT许可证，永久免费。你可以随意使用该工具。

---

**由LXGIC Studios开发**

- GitHub: [github.com/lxgicstudios/ai-branch](https://github.com/lxgicstudios/ai-branch)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)