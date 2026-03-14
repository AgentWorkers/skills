# AIN — OpenClaw 的 AI 节点插件

该插件将 [AIN](https://github.com/felipematos/ain) 提供者注册表、智能路由引擎和执行层集成到 OpenClaw 生态系统中。

## 功能概述

- **提供者桥接**：所有通过 AIN 配置的提供者（如 LM Studio、Ollama、OpenAI、vLLM 等）都会自动作为 `ain:<name>` 的形式在 OpenClaw 中被暴露出来。
- **LLM 工具**：提供了两个代理工具：`ain_run`（用于执行提示请求，并支持路由、结构化输出和回退机制）和 `ain_classify`（用于分类任务类型和复杂性）。
- **路由机制**：`before_model_resolve` 钩子会利用 AIN 的智能路由引擎，根据策略和任务分类自动为每个任务选择最合适的模型。

## 安装

需要安装 [@felipematos/ain-cli](https://www.npmjs.com/package/@felipematos/ain-cli)（作为依赖项）。

## 配置方法

在您的 OpenClaw 配置文件中添加以下内容：

```json
{
  "plugins": {
    "ain": {
      "enableRouting": true,
      "routingPolicy": "local-first",
      "exposeTools": true
    }
  }
}
```

### 配置选项

| 选项 | 类型 | 默认值 | 说明 |
|--------|------|---------|-------------|
| `configPath` | 字符串 | `~/.ain/config.yaml` | AIN 配置文件的路径 |
| `enableRouting` | 布尔值 | `true` | 启用智能模型路由功能 |
| `routingPolicy` | 字符串 | — | 从 `AIN/policies.yaml` 文件中指定的路由策略 |
| `exposeTools` | 布尔值 | `true` | 向代理暴露 `ain_run` 和 `ain_classify` 工具 |

## 工具说明

### `ain_run`

通过 AIN 的执行引擎执行 LLM 提示请求，支持完整的路由功能、结构化输出和回退机制。

**参数：**
- `prompt` (字符串，必填) — 需要执行的提示内容 |
- `provider` (字符串) — 提供者名称 |
- `model` (字符串) — 模型 ID 或别名 |
- `jsonMode` (布尔值) — 是否请求 JSON 格式的输出 |
- `schema` (对象) | 用于验证输出的 JSON 架构 |
- `system` (字符串) | 系统提示信息 |
- `temperature` (数字) | 采样温度（用于控制模型输出的随机性）

**返回值：** `{ output, provider, model, usage, parsedOutput }`

### `ain_classify`

用于分类提示任务的类型并估计其复杂性。

**参数：**
- `prompt` (字符串，必填) — 需要分类的提示内容 |

**返回值：** `{ taskType, complexity }`

**任务类型：** `classification` (分类)、`extraction` (提取)、`generation` (生成)、`reasoning` (推理)
**复杂性：** `low` (低)、`medium` (中)、`high` (高)

## 路由机制

当 `enableRouting` 为 `true` 时，该插件会注册一个 `before_model.resolve` 钩子，该钩子会根据以下因素分析传入的提示并选择最佳模型：
- 任务类型（分类/提取 → 快速层级；生成 → 通用层级；推理 → 推理层级）
- 在 `~/.ain/policies.yaml` 中定义的路由策略
- 模型的标签和层级配置

## 系统要求**

- Node.js 版本 >= 18
- AIN 已配置至少一个提供者（使用 `ain config init && ain providers add ...` 命令进行配置）
- OpenClaw 版本 >= 1.0.0

## 许可证

MIT 许可证