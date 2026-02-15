---
name: atris
description: 代码库智能功能：生成包含文件及行号信息的结构化导航地图，从而避免代理在每次会话中重复扫描相同的文件。适用于代码探索、回答“X在哪里？”这类问题，或在新代码库中进行入职培训时使用。
version: 1.0.0
requires:
  bins:
    - rg
tags:
  - developer-tools
  - codebase-navigation
  - token-optimization
  - code-map
  - context-management
---

# Atris — 代码库智能工具

Atris 是一个用于维护代码库结构的工具，它可以提供精确的文件和行号引用信息。通过一次扫描，即可获得代码库的完整结构信息，从而节省大量代码探索所需的时间（通常可节省 80-95% 的时间）。

## 使用范围

- 适用于任何需要导航代码的代码库。
- 会自动生成一个名为 `atris/MAP.md` 的导航索引文件。

## “MAP-first”原则

在代码库中搜索任何内容之前，请先执行以下步骤：
1. 阅读 `atris/MAP.md`。
2. 如果找到了所需的关键词，直接跳转到对应的文件和行号即可。
3. 如果未找到关键词，先用 `rg` 工具进行搜索，然后将搜索结果添加到 `atris/MAP.md` 中。

每次使用 Atris 时，该映射文件都会变得更加完善。请确保所有重要的代码变更都被记录下来。

## 首次设置

如果 `atris/MAP.md` 不存在，请按照以下步骤进行设置：
1. 在项目根目录下创建 `atris/` 文件夹。
2. 对代码库进行扫描（具体扫描规则见下文）。
3. 将扫描结果写入 `atris/MAP.md` 文件。
4. 告知用户：“代码库的映射信息已生成，保存在 `atris/MAP.md` 中。”

如果 `atris/MAP.md` 已经存在，则可以直接使用；只有在用户要求或映射信息明显过时（例如文件引用错误、行号不准确）时才需要重新生成。

## 扫描规则

以下文件和文件夹将被忽略：
- `node_modules`
- `.git`
- `dist`
- `build`
- `vendor`
- `__pycache__`
- `.venv`
- `.env*`
- `*.key`
- `*.pem`
- `credentials*`
- `secrets*`

**使用 ripgrep 工具提取代码结构：**

```bash
# Key definitions
rg "^(export|function|class|const|def |async def |router\.|app\.|@app\.)" --line-number -g "!node_modules" -g "!.git" -g "!dist" -g "!.env*"

# Route definitions
rg "(get|post|put|delete|patch)\s*\(" --line-number -g "*.ts" -g "*.js" -g "*.py"

# Entry points
rg "listen|createServer|app\.start|if __name__" --line-number
```

## `MAP.md` 的结构

`atris/MAP.md` 文件包含以下内容：
- **按功能分类的代码映射**：将代码按其功能进行分组，每个条目都包含完整的文件路径和行号。
- **按通用功能分类的代码映射**：将代码按通用功能（如错误处理、日志记录、身份验证中间件等）进行分组。
- **关键文件**：标记具有高影响力的文件，并列出其关键功能及其对应的行号。
- **入口点**：说明代码的执行流程，包括开发服务器的启动方式、请求的处理过程以及构建流程等。

## 保持映射信息的更新

当代码库发生变化时，只需对 `MAP.md` 进行部分更新：
- 新添加的文件：将其添加到相应的分类中。
- 文件被移动或重命名：更新所有相关的引用。
- 新出现的重点函数：将其添加到快速参考列表中。
- 被删除的文件：从映射中移除。
- 发生重大重构的代码：重新生成受影响的代码部分。

**注意事项：**
- 不要在未先查看 `MAP.md` 的情况下直接进行搜索。
- 请确保所有重要的代码变更都被记录下来。
- 只在确实需要时才重新生成整个映射文件。
- 不要将敏感信息（如密码、密钥或 `.env` 文件）包含在映射中。
- 请始终使用索引来查找文件位置，而不是凭猜测来确定文件位置。