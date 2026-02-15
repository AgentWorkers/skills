---
name: claude-optimised
description: **编写和优化 CLAUDE.md 文件以提升 Claude 代码性能的指南**  
本指南适用于新创建 CLAUDE.md 文件、审查现有文件，或当用户询问 CLAUDE.md 的最佳实践时参考。内容涵盖文件结构、内容编写、代码优化以及常见错误分析。  

**一、文件结构**  
CLAUDE.md 文件应遵循以下结构：  
1. `# Introduction`（引言）：简要介绍文件的目的和用途。  
2. `# Code Examples`（代码示例）：包含用于演示功能的代码片段。  
3. `# Configuration Options`（配置选项）：列出可配置的参数及其默认值。  
4. `# Usage Instructions`（使用说明）：详细说明如何使用该文件或其中的代码。  
5. `# Troubleshooting`（故障排除）：提供遇到问题时的解决方法。  
6. `# References`（参考文献）：列出相关文档或资源的链接。  
7. `# Additional Notes`（其他说明）：任何额外的补充信息。  

**二、内容编写**  
1. **使用简洁明了的文本**：避免使用过于复杂的句子或长篇大论的描述。  
2. **注释代码**：对于复杂的代码片段，添加适当的注释以解释其功能和工作原理。  
3. **遵循Markdown格式**：确保使用正确的 Markdown 标签（如 `#`, `-`, `_` 等）来格式化文本。  
4. **使用示例数据**：提供实际的示例数据以验证代码的正确性。  
5. **保持一致性**：在整个文件中保持格式和术语的一致性。  

**三、代码优化**  
1. **避免冗余代码**：删除不必要的代码行或重复的部分。  
2. **使用变量**：将重复出现的值存储在变量中，以提高代码的可读性和可维护性。  
3. **优化算法**：根据实际情况优化算法的效率。  
4. **测试代码**：在发布之前对代码进行充分的测试，确保其稳定性和可靠性。  

**四、常见错误**  
1. **语法错误**：确保文件遵循 Markdown 的语法规范。  
2. **格式问题**：错误的缩进、换行或标点符号可能导致文件无法正确解析。  
3. **未使用的代码**：删除未使用的代码以减少文件大小。  
4. **缺乏注释**：缺乏注释会导致其他开发者难以理解代码的功能。  

**五、总结**  
编写高质量的 CLAUDE.md 文件有助于提高 Claude 代码的性能和可维护性。通过遵循上述指南，您可以编写出更易于阅读和使用的文档。
---

# CLAUDE.md 优化指南

编写 CLAUDE.md 文件，以最大化 Claude 的遵循性和性能。

## 核心原则：少即是多

过长的 CLAUDE.md 文件会导致 Claude 忽略其中的大部分内容；关键规则也会在冗余的信息中被淹没。

**对于每一行内容，都要问自己：**“删除这一行会导致 Claude 出错吗？”
- 如果不会 → 删除它
- 如果 Claude 已经正确地执行了该操作 → 删除它，或者将其转换为钩子（hook）。

## 应该包含的内容

### 必需包含的内容（高价值）

| 部分 | 例子 |
|---------|---------|
| 项目背景 | “基于 Next.js 的电子商务应用，使用 Stripe”（1 行） |
| 构建/测试命令 | `npm run test`, `pnpm build` |
| 重要的注意事项 | “切勿直接修改 auth.ts” |
| 非显而易见的编码规范 | “使用 `vi` 来管理状态，而不是 `useState`” |
| 专业术语 | “PO 表示 Purchase Order（采购订单），而非 Product Owner（产品负责人）” |

### 仅在非标准情况下才包含

- 分支命名（如果不是 `feature/` 或 `fix/` 结构）
- 提交格式（如果不是常规的提交格式）
- 文件边界（对于敏感文件尤为重要）

### 不应包含的内容

- Claude 已经掌握的内容（通用编码规范）
- 显而易见的编码模式（可以从现有代码中推断出来）
- 过长的解释（应简洁明了）
- 不切实际的目标或规则（仅针对实际遇到的问题）

## 结构

```markdown
# Project Name

One-line description.

## Commands
- Test: `npm test`
- Build: `npm run build`
- Lint: `npm run lint`

## Code Style
- [Only non-obvious conventions]

## Architecture
- [Brief, only if complex]

## IMPORTANT
- [Critical warnings - use sparingly]
```

## 格式规范

- 使用项目符号（bullet points）而非段落
- 使用 Markdown 标题来分隔不同模块（避免指令内容相互混淆）
- 使用具体、明确的表述（例如使用“2 个空格缩进”而非“格式正确”）
- 对于关键规则，使用 **IMPORTANT/YOU MUST** 标签（但请谨慎使用，否则会降低提示效果）

## 文件放置位置

| 位置 | 适用范围 |
|----------|-------|
| `~/.claude/CLAUDE.md` | 所有会话（用户偏好设置） |
| `./CLAUDE.md` | 项目根目录（通过 git 共享） |
| `./subdir/CLAUDE.md` | 在子目录中工作时自动加载 |
| `.claude/rules/*.md` | 作为项目配置自动加载到内存中 |

## 优化检查清单

在最终确定文件内容之前，请检查以下内容：
- [ ] 文件长度是否少于 50 行？（理想目标）
- [ ] 每一行内容是否解决了你实际遇到的问题？
- [ ] 是否与其他 CLAUDE.md 文件存在重复内容？
- [ ] 是否有 Claude 默认不遵循的指令？
- [ ] 通过观察 Claude 的行为变化来验证这些规则的有效性？

## 维护

- 以运行 `/init` 命令作为起点，然后对文件内容进行精简
- 每几周检查一次：“审查这份 CLAUDE.md 文件，建议删除不必要的内容”
- 当 Claude 表现异常时：添加相应的规则
- 当 Claude 忽略某些规则时：检查文件是否过长，并相应地删除其他冗余内容

## 应避免的错误做法

| 不要做 | 原因 |
|-------|-----|
| 文件长度超过 200 行 | Claude 会忽略这些内容 |
| 写“干净的代码” | Claude 已经知道这一点 |
- 文件间重复规则 | 会浪费存储空间并引发冲突 |
- 仅基于理论上的问题添加规则 | 仅针对实际遇到的问题添加规则 |
- 过长的文字解释 | 使用项目符号来表达内容会更清晰 |

## 示例：简洁有效的 CLAUDE.md 文件

```markdown
# MyApp

React Native app with Expo. Backend is Supabase.

## Commands
- `pnpm test` - run tests
- `pnpm ios` - run iOS simulator

## Style
- Prefer Zustand over Context
- Use `clsx` for conditional classes

## IMPORTANT
- NEVER commit .env files
- Auth logic lives in src/lib/auth.ts only
```

文件长度约 15 行，仅包含 Claude 无法自行推断的内容，不再包含其他多余信息。