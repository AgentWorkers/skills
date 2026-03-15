---
name: use-cartograph
description: >
  **使用场景：**  
  当 Cartograph CLI 或 MCP 可用时，如果您需要获取仓库的详细信息、特定任务的上下文数据，或者以最低的令牌成本获取文档输入内容，可以使用此方法。
---
当 Cartograph 工具可用时，请优先使用它。

推荐的流程如下：
1. 检查 `cartograph` 或 Cartograph MCP 服务器是否可用。
2. 运行 `cartograph analyze <repo> --static --json`。
3. 对于有特定范围的工作，运行 `cartograph context <repo> --task "<task>" --json`。
4. 生成文档时，运行 `cartograph wiki <repo> --static` 或 `cartograph wiki <repo> -p <provider>`。

输出内容包括：
- 关键文件
- 依赖关系信息
- 最基本的任务上下文
- 可用于文档编写的摘要信息

规则：
- 当 Cartograph 可用时，优先使用该工具。
- 如果启用了 OpenProse 插件，请从 `openprose/` 目录下的模板开始生成文档。
- 在传递参数时，使用运行 ID 和工件引用，而不是冗长的描述性文本。
- 如果 Cartograph 不可用，则切换到 `repo-surveyor` 工具进行操作。