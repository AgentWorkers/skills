---
name: eachlabs-workflows
description: 构建并编排包含多个 EachLabs 模型的多步骤 AI 工作流程。创建自定义管道、触发执行任务，并管理工作流的版本。当用户需要串联多个 AI 模型或自动化多步骤内容创建时，可以使用此功能。
metadata:
  author: eachlabs
  version: "1.0"
---
# EachLabs 工作流

通过 EachLabs Workflows API，您可以构建、管理和执行多步骤 AI 工作流，这些工作流会将多个模型串联起来。

## 认证

```
Header: X-API-Key: <your-api-key>
```

设置 `EACHLABS_API_KEY` 环境变量。您可以在 [eachlabs.ai](https://eachlabs.ai) 获取该密钥。

## 基本 URL

```
https://workflows.eachlabs.run/api/v1
```

## 构建工作流

要构建一个工作流，您需要：（1）创建工作流，然后（2）创建包含各个步骤的版本。

### 第 1 步：创建工作流

```bash
curl -X POST https://workflows.eachlabs.run/api/v1/workflows \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "name": "Product Photo to Video",
    "description": "Generate a product video from a product photo"
  }'
```

此操作会返回一个 `workflowID`。请在下一步中使用该 ID。

### 第 2 步：创建包含步骤的版本

```bash
curl -X POST https://workflows.eachlabs.run/api/v1/workflows/{workflowID}/versions \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "description": "Initial version",
    "steps": [
      {
        "name": "enhance_photo",
        "model": "gpt-image-v1-5-edit",
        "version": "0.0.1",
        "input": {
          "prompt": "Place this product on a clean white background with studio lighting",
          "image_urls": ["{{inputs.image_url}}"],
          "quality": "high"
        }
      },
      {
        "name": "create_video",
        "model": "pixverse-v5-6-image-to-video",
        "version": "0.0.1",
        "input": {
          "image_url": "{{steps.enhance_photo.output}}",
          "prompt": "Slow cinematic rotation around the product",
          "duration": "5",
          "resolution": "1080p"
        }
      }
    ]
  }'
```

**重要提示：** 在将模型添加到工作流步骤之前，请使用 `GET https://api.eachlabs.ai/v1/model?slug=<slug>` 查阅模型的架构，以验证输入参数是否正确。

### 第 3 步：触发工作流

```bash
curl -X POST https://workflows.eachlabs.run/api/v1/{workflowID}/trigger \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "inputs": {
      "image_url": "https://example.com/product.jpg"
    }
  }'
```

### 第 4 步：查询结果

```bash
curl https://workflows.eachlabs.run/api/v1/executions/{executionID} \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

持续查询，直到 `status` 变为 `"completed"` 或 `"failed"`。从 `step_outputs` 中提取结果。

## 工作流管理

### 列出工作流

```bash
curl https://workflows.eachlabs.run/api/v1/workflows \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

### 获取工作流详细信息

```bash
curl https://workflows.eachlabs.run/api/v1/workflows/{workflowID} \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

### 批量触发

使用多个输入同时触发同一工作流：

```bash
curl -X POST https://workflows.eachlabs.run/api/v1/{workflowID}/trigger/bulk \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "executions": [
      { "inputs": { "image_url": "https://example.com/product1.jpg" } },
      { "inputs": { "image_url": "https://example.com/product2.jpg" } },
      { "inputs": { "image_url": "https://example.com/product3.jpg" } }
    ]
  }'
```

### 检查执行状态

```bash
curl https://workflows.eachlabs.run/api/v1/executions/{executionID} \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

响应中包含 `status`（`pending`、`running`、`completed`、`failed`）以及每个步骤的结果（`step_outputs`）。

### Webhook

配置 Webhook 以异步接收结果：

```bash
curl -X POST https://workflows.eachlabs.run/api/v1/{workflowID}/trigger \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "inputs": { "image_url": "https://example.com/photo.jpg" },
    "webhook_url": "https://your-server.com/webhook"
  }'
```

## 版本管理

工作流版本允许您在保留旧版本的同时对工作流进行迭代。步骤的定义是在版本中完成的，而不是在工作流本身中。

### 创建版本

```bash
curl -X POST https://workflows.eachlabs.run/api/v1/workflows/{workflowID}/versions \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "description": "Added upscaling step",
    "steps": [
      {
        "name": "generate_image",
        "model": "gpt-image-v1-5-text-to-image",
        "version": "0.0.1",
        "input": {
          "prompt": "{{inputs.prompt}}",
          "quality": "high"
        }
      },
      {
        "name": "upscale",
        "model": "topaz-upscale-image",
        "version": "0.0.1",
        "input": {
          "image_url": "{{steps.generate_image.output}}"
        }
      }
    ]
  }'
```

### 获取版本信息

```bash
curl https://workflows.eachlabs.run/api/v1/workflows/{workflowID}/versions/{versionID} \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

### 更新版本

```bash
curl -X PUT https://workflows.eachlabs.run/api/v1/workflows/{workflowID}/versions/{versionID} \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $EACHLABS_API_KEY" \
  -d '{
    "description": "Updated prompt template",
    "steps": [
      {
        "name": "generate_image",
        "model": "gpt-image-v1-5-text-to-image",
        "version": "0.0.1",
        "input": {
          "prompt": "Professional photo: {{inputs.prompt}}",
          "quality": "high"
        }
      }
    ]
  }'
```

### 列出所有版本

```bash
curl https://workflows.eachlabs.run/api/v1/workflows/{workflowID}/versions \
  -H "X-API-Key: $EACHLABS_API_KEY"
```

## 工作流特性

- **两阶段创建**：先创建工作流，然后通过版本添加步骤
- **步骤链接**：使用 `{{steps.step_name.output}}` 引用前一步的输出
- **输入变量**：使用 `{{inputs.variable_name}}` 传递动态输入
- **版本管理**：创建、更新和检索工作流版本
- **批量执行**：通过一次 API 调用处理多个输入
- **Webhook 支持**：在执行完成时接收通知
- **公开/非公开共享**：与他人共享工作流

## 工作流示例参考

有关常见的工作流模式，请参阅 [references/WORKFLOW-EXAMPLES.md](references/WORKFLOW-EXAMPLES.md)。