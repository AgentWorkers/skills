---
name: model-router-premium
version: 0.1.1
description: 根据配置的模型、成本和任务复杂度来路由模型请求。将一般性或低复杂度的请求路由到最便宜的可用模型，将高复杂度的请求路由到功能更强大的模型。
---

# model-router

该技能提供了一个简洁、可运行的路由器，它能够解析 OpenClaw 格式的配置文件（或简单的 JSON 模型文件），并根据以下因素为传入的请求选择合适的模型：

- 声明的模型功能以及可选的成本评分（cost_score）
- 任务的复杂性（基于启发式判断：简单/短任务 vs 复杂/长任务）
- 显式的配置覆盖（用户或调用者的指示）

**设计原则：**
- 保持决策逻辑简洁且具有确定性。
- 对于一般性的、不复杂的任务，默认选择成本最低的模型。
- 当任务显得复杂或需要高保真度的结果时，升级到更强大的模型。
- 明确模型元数据（功能、成本评分、标签），以使路由器的运行过程透明且可审计。

**该技能包含的内容：**
- `scripts/router.py`：一个小型命令行工具（CLI）和库，用于根据任务描述和模型配置文件来选择合适的模型。
- `examples/models.json`：示例模型配置文件，包含模型的名称、提供者（provider）、成本评分（cost_score）和功能（capabilities）。

**使用场景：**
- 当需要通过编程方式决定为用户的请求调用哪个大型语言模型（LLM）时使用。
- 适用于服务器应用程序中的批量处理或中间件路由场景。

**使用方法（快速示例）：**
1. 准备一个包含模型信息的 JSON 文件（参见 `examples/models.json`）。
2. 运行命令：`python3 scripts/router.py --models examples/models.json --task "Summarize this email" --mode auto`
3. 脚本会输出所选模型及其选择理由。

**相关文件：**
- `scripts/router.py`：路由器的命令行工具和库代码。
- `examples/models.json`：示例模型配置文件。