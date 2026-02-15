---
name: lmstudio-subagents
description: "通过将工作负载转移到本地的LM Studio模型上，可以减少对付费服务提供商的依赖（即减少对付费API的调用）。适用场景包括：  
(1) 降低成本：在质量要求满足的情况下，使用本地模型进行摘要生成、数据提取、分类、内容重写以及初步审核等工作；  
(2) 避免对高容量或重复性任务进行付费API调用；  
(3) 无需额外配置模型：利用JIT（即时编译）技术以及REST API，在现有的LM Studio环境中直接运行相关功能；  
(4) 仅涉及本地数据处理或涉及隐私敏感信息的场景。  
系统要求：必须使用LM Studio 0.4及以上版本，并且需要连接服务器（默认服务器地址为1234）。该功能无需使用命令行界面（CLI）。"
metadata: {"openclaw":{"requires":{},"tags":["local-model","local-llm","lm-studio","token-management","privacy","subagents"]}}
license: MIT
---

# LM Studio 模型

当模型质量满足要求时，可以将任务卸载到本地模型中。基础 URL：http://127.0.0.1:1234。认证方式：`Authorization: Bearer lmstudio`。`instance_id` 的值来自 `loaded_instances[]` 数组（同一个模型可能有多个实例，例如 `key` 和 `key:2`）。

## 关键术语

- **model**：通过 `GET models` 获取的模型键，可用于聊天对话，也可选择性地进行模型加载。
- **lm_studio_api_url**：默认值为 http://127.0.0.1:1234（路径格式为 `/api/v1/...`）。
- **response_id** 和 **previous_response_id**：聊天对话会返回 `response_id`；在需要保持会话状态的情况下，可以使用 `previous_response_id`。
- **instance_id**：用于卸载模型时，需要使用从 `GET /api/v1/models` 获取的该模型的唯一标识符（每个模型的 `loaded_instances[]` 数组中的 `id`）。请注意，`instance_id` 与模型键不同；对于同一个模型，可能有多个实例，例如 `key:2`。LM Studio 文档中提到：`List (loaded_instances[].)` 用于列出所有已加载的实例，`Unload (instance_id)` 用于卸载模型。

### 实现细节

相关代码位于文档的前置内容（`frontmatter`）部分。

## 先决条件

- LM Studio 版本需达到 0.4 或更高；
- 服务器地址为 1234；
- 模型数据已保存在磁盘上；
- 可通过 API 进行模型的加载和卸载（JIT（即时编译）功能可选）；
- 需要 Node.js 环境来运行相关脚本（支持使用 `curl` 命令）。

## 快速入门

- 最简单的操作流程是：首先列出所有可用模型，然后选择一个模型进行聊天对话。将 `<model>` 替换为从 `GET /api/v1/models` 获取的模型键，将 `<task>` 替换为具体的任务内容。

### 完整工作流程

#### 步骤 0：检查服务器状态

执行 `GET <base>/api/v1/models` 请求；如果返回状态码非 200 或出现连接错误，说明服务器尚未准备好。

#### 步骤 1：列出模型并选择模型

执行 `GET /api/v1/models` 以获取所有模型列表。解析每个模型的信息：模型键（`key`）、模型类型（`type`）、已加载的实例数量（`loaded_instances`）、最大上下文长度（`max_context_length`）以及模型支持的功能（`capabilities`）。如果某个模型的 `loaded_instances.length` 大于 0 且符合任务要求，则直接跳到步骤 5；否则，选择一个模型键用于聊天对话（或选择性地进行模型加载，详见步骤 3）。

#### 步骤 2：选择模型

从响应中获取模型键，并将其用于聊天对话（或选择性地进行模型加载）。选择模型时需考虑以下条件：  
- 如果模型支持视觉处理（`vision`），则选择 `capabilities.vision` 作为筛选条件；  
- 如果模型支持嵌入式处理（`embedding`），则选择 `type=embedding`；  
- 如果需要处理较长上下文，选择 `max_context_length` 较大的模型。  
- 优先选择已加载的模型（`loaded_instances` 数组非空），因为已加载的模型通常加载速度更快；如果需要更复杂的推理，可以选择 `max_context_length` 较大的模型。  
- 注意保存 `loaded_instances[]` 数组中的 `id`，以便后续进行模型卸载。

#### 步骤 3：加载模型（可选）

- 可以通过 `POST /api/v1/models/load { model, context_length,... }` 命令加载模型。  
- 或者运行 `load.mjs <model>` 脚本进行模型加载。JIT（即时编译）功能仅在首次聊天对话时生效。

#### 步骤 4：验证模型是否成功加载（可选）

- 如果是显式加载模型，执行 `GET models` 请求以确认模型是否成功加载（`loaded_instances` 数组是否非空）。  
- 如果使用 JIT 功能，无需额外验证；首次聊天对话会返回 `model_instance_id` 和 `stats.model_load_time_seconds`（模型加载所用时间）。

#### 步骤 5：调用 API 执行任务

在 `node scripts/lmstudio-api.mjs` 脚本中，使用以下格式调用 API：`<model> '<task>' [options]`。

#### 步骤 6：卸载模型（可选）

- 对于已选中的模型，执行 `GET /api/v1/models` 请求；然后对每个已加载的实例执行 `POST /api/v1/models/unload` 请求，传入 `{"instance_id": "<that id>"}` 作为参数。  
- 请确保使用的 `instance_id` 来自 `GET /api/v1/models` 的返回结果（不要使用模型键）。  
- 或者运行 `unload.mjs <model_key>` 脚本进行模型卸载。  
- 可选参数 `--unload-after` 可用于设置卸载后的延迟时间（默认值为关闭）；`--keep` 参数可用于保留已加载的模型。  
- JIT 功能结合 TTL（时间戳）可实现自动卸载；必要时也可以手动执行卸载操作。

#### 步骤 7：验证模型是否成功卸载（可选）

卸载完成后，检查该模型是否真的被完全卸载。可以使用 `jq` 命令验证：结果应为 `0`。如果仍有实例存在，请重新执行卸载操作。  
- 注意：即使模型对象仍然存在于系统中，但其 `loaded_instances` 数组可能为空，这并不意味着模型已被成功卸载。

### 错误处理

- 脚本会在遇到临时故障时尝试多次执行（最多 2-3 次，并采用退避策略）。
- 如果找不到目标模型，可以从 `GET` 请求的结果中选择其他模型。
- 如果 API 或服务器出现错误，请重新执行 `GET models` 请求以检查服务器状态。
- 如果返回的响应无效，请尝试重新加载模型或选择其他模型。
- 如果内存不足，可以选择加载内存占用较小的模型。
- 如果卸载失败，请确保使用的 `instance_id` 来自 `GET /api/v1/models` 返回的 `loaded_instances[]` 数组（而非模型键）。

### 复制代码示例

- 将 `<model>` 替换为从 `GET /api/v1/models` 获取的模型键，将 `<task>` 替换为具体的任务内容。
- 可以根据需要选择性地执行步骤 6 中的模型卸载操作（使用 `GET models` 返回的 `instance_id`）。

### LM Studio API 详细信息

- 辅助 API：详见步骤 5 的说明。
- API 返回的响应内容包括：`content`、`model_instance_id` 和 `response_id`。
- 认证方式：`Authorization: Bearer lmstudio`。
- 可通过 `GET /api/v1/models` 列出所有可用模型；通过 `POST /api/v1/models/load` 加载模型；通过 `POST /api/v1/models/unload` 卸载模型。

### 相关脚本

- `lmstudio-api.mjs`：用于处理聊天对话相关的逻辑，支持 `--stateful`、`--unload-after`、`--keep`、`--log <path>`、`--previous-response-id`、`--temperature`、`--max-output-tokens` 等选项。
- `load.mjs`：用于根据模型键加载模型。
- `unload.mjs`：用于根据模型键卸载所有已加载的实例。
- `test.mjs`：用于测试模型的加载、聊天对话和卸载功能。

### 注意事项

- 仅支持 LM Studio 0.4 及更高版本。
- 支持 JIT（即时编译）功能：模型会在首次聊天对话时加载；加载时间会记录在 `stats.model_load_time_seconds` 中。
- 支持会话状态管理（使用 `response_id` 和 `previous_response_id`）。