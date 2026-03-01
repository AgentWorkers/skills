---
name: model-fallback
description: >
  多模型自动回退系统：该系统会实时监控模型的可用性，并在主模型出现故障时自动切换到备用模型。支持 MiniMax、Kimi、Zhipu 等与 OpenAI 兼容的 API。适用场景包括：  
  (1) 主模型 API 不可用时；  
  (2) 模型响应时间过慢时；  
  (3) 超过请求速率限制时；  
  (4) 需要通过使用成本更低的模型来优化简单任务的性能。
  Multi-model automatic fallback system. Monitors model availability and automatically
  falls back to backup models when the primary model fails. Supports MiniMax, Kimi,
  Zhipu and other OpenAI-compatible APIs. Use when: (1) Primary model API is unavailable,
  (2) Model response time is too slow, (3) Rate limit exceeded, (4) Need to optimize
  costs by using cheaper models for simple tasks.
tags: [model, fallback, multi-model, cost-optimization, reliability]
---
# 模型回退机制（Model Fallback Skill）

> 为AI代理提供多模型自动回退系统

## 概述

该机制为OpenClaw代理提供了自动模型回退功能。当主模型出现故障（无法使用、响应缓慢或受到速率限制时，系统会按照预设的优先级顺序自动切换到备用模型。

## 主要特性

- **自动回退**：在模型故障时无缝切换到备用模型
- **可配置的优先级**：自定义模型回退顺序
- **健康监控**：实时跟踪模型的可用性和响应时间
- **成本优化**：针对简单任务使用更经济的模型
- **日志记录**：详细记录所有回退事件

## 支持的模型

| 提供商 | 模型        | 适用场景        |
|----------|--------------|---------------------------|
| MiniMax | M2.5         | 主模型（用于推理）                |
| MiniMax | M2.1         | 备用模型                    |
| Kimi    | K2.5         | 处理长文档                    |
| Kimi    | K2           | 标准模型                    |
| Zhipu   | GLM-4-Air     | 低成本模型                    |
| Zhipu   | GLM-4-Flash    | 高吞吐量模型                    |

## 配置

### 默认的回退策略

```json
{
  "fallback_chain": [
    {
      "provider": "minimax-portal",
      "model": "MiniMax-M2.5",
      "priority": 1,
      "timeout": 30,
      "max_retries": 3
    },
    {
      "provider": "moonshot",
      "model": "kimi-k2.5",
      "priority": 2,
      "timeout": 30,
      "max_retries": 2
    },
    {
      "provider": "zhipu",
      "model": "glm-4-air",
      "priority": 3,
      "timeout": 20,
      "max_retries": 2
    }
  ]
}
```

### 环境变量

| 变量          | 是否必需      | 描述                        |
|--------------|-------------|---------------------------|
| `MODEL_FALLBACK_ENABLED` | 否           | 是否启用回退机制（默认值：true）            |
| `MODEL_FALLBACK_LOG_LEVEL` | 否           | 日志记录级别（debug, info, warn, error）       |

## 使用方法

### 基本用法

该机制会自动处理模型故障，无需手动调用相关函数。

```bash
# Trigger a model call (fallback happens automatically on failure)
```

### 手动触发回退

```bash
# Force fallback to next model
/scripts/model-fallback.sh --force-next

# Check current model status
/scripts/model-fallback.sh --status

# Reset to primary model
/scripts/model-fallback.sh --reset
```

### 配置回退策略

通过编辑 `config.json` 文件来自定义回退策略：

```json
{
  "fallback_chain": [
    {"provider": "...", "model": "...", "priority": 1}
  ],
  "health_check": {
    "enabled": true,
    "interval_seconds": 300
  }
}
```

## 工作原理

```
1. User makes request with primary model
2. Model call fails (error, timeout, rate limit)
3. Skill detects failure
4. Wait 3 seconds (debounce)
5. Switch to next model in chain
6. Retry request with new model
7. If successful, return result
8. If failed, repeat steps 4-7
9. If all models fail, return error with details
```

## 回退触发条件

| 触发条件       | 操作                          |
|--------------|-------------------------------------------|
| API无法使用     | 切换到备用模型                   |
| 达到速率限制     | 发送429错误响应后进行回退并等待片刻       |
| 响应时间过长     | 超过预设超时时间后进行回退                |
| 响应错误       | 解析错误后进行回退                   |
| 认证失败     | 收到401/403错误响应后记录日志并停止服务       |

## 日志记录

日志文件保存路径：`~/.openclaw/logs/model-fallback.log`

### 日志格式

```
[2026-02-27 14:00:00] [INFO] Primary model MiniMax-M2.5 called
[2026-02-27 14:00:05] [WARN] Model failed: rate limit exceeded
[2026-02-27 14:00:05] [INFO] Falling back to Kimi K2.5
[2026-02-27 14:00:10] [INFO] Fallback successful
```

## 成本优化

对于简单任务，可以使用成本更低的模型来提高效率：

```json
{
  "task_routing": {
    "simple_query": ["glm-4-air", "glm-4-flash"],
    "complex_reasoning": ["MiniMax-M2.5", "kimi-k2.5"],
    "long_context": ["kimi-k2.5", "MiniMax-M2.1"]
  }
}
```

## 集成方式

### 在OpenClaw中的配置

将相关配置添加到 `openclaw.json` 文件中：

```json
{
  "models": {
    "mode": "merge",
    "fallback": {
      "enabled": true,
      "config": "~/.openclaw/skills/model-fallback/config.json"
    }
  }
}
```

### 健康检查

该机制可与其他系统健康监控机制集成，以便及时发现模型问题：

```bash
# Check model health
curl http://localhost:18789/api/models/health
```

## 故障排除

### 回退机制未生效

1. 检查是否已启用回退机制：`echo $MODEL_FALLBACK_ENABLED`
2. 确认配置文件存在：`ls ~/.openclaw/skills/model-fallback/config.json`
3. 查看日志文件：`tail -f ~/.openclaw/logs/model-fallback.log`

### 模型始终失败

1. 确认API密钥有效
2. 检查网络连接是否正常
3. 查看提供商的速率限制设置

## 示例

### 示例1：简单场景下的回退机制

```
User: "Hello"
System: Using MiniMax-M2.5...
System: Rate limited, switching to Kimi K2.5...
System: Response from Kimi K2.5: "Hello! How can I help?"
```

### 示例2：通过成本优化提升性能

```
User: "What is 2+2?"
System: Routing to glm-4-air (low cost)...
System: Response: "2+2=4"
```

### 示例3：处理长文档的场景

```
User: "Summarize this 100-page PDF"
System: Detected long context requirement
System: Routing to Kimi K2.5 (256K context)...
System: Processing...
```

## 许可证

MIT许可证

## 作者

CC（AI Assistant）

## 版本

1.0.0