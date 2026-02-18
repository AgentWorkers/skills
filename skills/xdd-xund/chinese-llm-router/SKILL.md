# 中文大型语言模型（LLM）路由器

将您的 OpenClaw 对话路由到最适合的中文 AI 模型——无需配置繁琐的步骤，只需选择模型即可开始聊天。

## 功能介绍

通过一个统一的接口，让您的 OpenClaw 即时可访问所有主要的中文 LLM 模型：

- **DeepSeek**（V3.2 / R1）：最优秀的开源推理引擎，价格非常实惠；
- **Qwen**（Qwen3-Max / Qwen3-Max-Thinking / Qwen3-Coder-Plus）：阿里巴巴的旗舰模型，功能全面；
- **GLM**（GLM-5 / GLM-4.7）：Zhipu AI 的模型，擅长编程和任务处理；
- **Kimi**（K2.5 / K2.5-Thinking）：Moonshot AI 的模型，擅长处理长文本和视觉任务；
- **Doubao Seed 2.0**（Pro / Lite / Mini）：字节跳动的模型，响应速度快且价格便宜；
- **MiniMax**（M2.5）：轻量级模型，支持本地运行；
- **Step**（3.5 Flash）：StepFun 的模型，推理速度极快；
- **Baichuan**（Baichuan4-Turbo）：中文理解能力很强；
- **Spark**（v4.0 Ultra）：iFlytek 的模型，专注于语音和中文自然语言处理；
- **Hunyuan**（Turbo-S）：腾讯的模型，与微信生态系统集成。

## 快速入门

告诉您的 OpenClaw：

```
Use DeepSeek V3.2 for this conversation
```

或者让它为您选择最适合的模型：

```
Which Chinese model is best for coding? Switch to it.
```

## 命令

| 命令 | 功能 |
|---------|-------------|
| `list models` | 显示所有可用的中文 LLM 模型及其状态 |
| `use <model>` | 切换到指定的模型 |
| `compare <models>` | 比较不同模型的功能和价格 |
| `recommend <task>` | 为特定任务推荐合适的模型 |
| `test <model>` | 向模型发送测试提示以验证连接是否正常 |
| `status` | 查看当前可使用的模型 |

## 模型选择指南

| 任务类型 | 推荐模型 | 选择理由 |
|------|------------------|-----|
| 通用聊天 | Qwen3-Max | 功能全面，中文处理能力强 |
| 编程 | GLM-5 / Kimi K2.5 | 在编程任务中表现优异 |
| 数学与推理 | DeepSeek R1 | 专为推理任务设计 |
| 处理长文档 | Kimi K2.5（128K）/ DeepSeek V3.2（1M） | 具备较大的上下文处理能力 |
| 快速且经济实惠 | Step 3.5 Flash / Doubao Seed 2.0 Mini | 响应时间在秒级以内 |
| 创意写作 | Qwen3-Max / Doubao Seed 2.0 Pro | 表达能力丰富 |
| 代理任务 | GLM-5 / Qwen3-Max | 在代理任务中表现最佳 |

## 配置

该插件会从环境变量或 `~/.chinese-llm-router/config.json` 文件中读取 API 密钥：

```json
{
  "providers": {
    "deepseek": {
      "apiKey": "sk-xxx",
      "baseUrl": "https://api.deepseek.com/v1",
      "models": ["deepseek-chat", "deepseek-reasoner"]
    },
    "qwen": {
      "apiKey": "sk-xxx",
      "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "models": ["qwen3-max", "qwen3-max-thinking", "qwen3-coder-plus"]
    },
    "glm": {
      "apiKey": "xxx.xxx",
      "baseUrl": "https://open.bigmodel.cn/api/paas/v4",
      "models": ["glm-5", "glm-4-plus"]
    },
    "kimi": {
      "apiKey": "sk-xxx",
      "baseUrl": "https://api.moonshot.cn/v1",
      "models": ["kimi-k2.5", "kimi-k2.5-thinking"]
    },
    "doubao": {
      "apiKey": "xxx",
      "baseUrl": "https://ark.cn-beijing.volces.com/api/v3",
      "models": ["doubao-seed-2.0-pro", "doubao-seed-2.0-lite", "doubao-seed-2.0-mini"]
    },
    "minimax": {
      "apiKey": "xxx",
      "baseUrl": "https://api.minimax.chat/v1",
      "models": ["minimax-m2.5"]
    },
    "step": {
      "apiKey": "xxx",
      "baseUrl": "https://api.stepfun.com/v1",
      "models": ["step-3.5-flash"]
    },
    "baichuan": {
      "apiKey": "xxx",
      "baseUrl": "https://api.baichuan-ai.com/v1",
      "models": ["baichuan4-turbo"]
    },
    "spark": {
      "apiKey": "xxx",
      "baseUrl": "https://spark-api-open.xf-yun.com/v1",
      "models": ["spark-v4.0-ultra"]
    },
    "hunyuan": {
      "apiKey": "xxx",
      "baseUrl": "https://api.hunyuan.cloud.tencent.com/v1",
      "models": ["hunyuan-turbo-s"]
    }
  },
  "default": "qwen3-max",
  "fallback": ["deepseek-chat", "doubao-seed-2.0-pro"]
}
```

## 设置步骤

1. 从相应的提供商处获取 API 密钥（大多数提供商都提供免费试用 tier）：
   - DeepSeek：https://platform.deepseek.com
   - Qwen（阿里巴巴）：https://dashscope.console.aliyun.com
   - GLM（Zhipu）：https://open.bigmodel.cn
   - Kimi（Moonshot）：https://platform.moonshot.cn
   - Doubao（字节跳动）：https://console.volcengine.com/ark
   - MiniMax：https://platform.minimaxi.com
   - Step（StepFun）：https://platform.stepfun.com
   - Baichuan：https://platform.baichuan-ai.com
   - Spark（iFlytek）：https://console.xfyun.cn
   - Hunyuan（腾讯）：https://cloud.tencent.com/product/hunyuan

2. 运行设置脚本：
   ```bash
   node scripts/setup.js
   ```

3. 设置完成！您的 OpenClaw 现在就可以使用配置好的模型了。

## 价格参考（2026年2月）

| 模型 | 输入（¥/百万令牌） | 输出（¥/百万令牌） | 备注 |
|-------|-------------------|---------------------|-------|
| DeepSeek V3.2 | ¥0.5（缓存费用 ¥0.1） | ¥2.0 | 最便宜的旗舰模型 |
| Qwen3-Max | ¥2.0 | ¥6.0 | 提供免费试用 tier |
| GLM-5 | ¥5.0 | ¥5.0 | 新推出的模型，价格可能随时调整 |
| Kimi K2.5 | ¥2.0 | ¥6.0 | 开源模型，支持自托管 |
| Doubao Seed 2.0 Pro | ¥0.8 | ¥2.0 | 字节跳动提供的补贴 |
| Doubao Seed 2.0 Mini | ¥0.15 | ¥0.3 | 非常便宜 |
| MiniMax M2.5 | ¥1.0 | ¥3.0 | 支持本地运行 |
| Step 3.5 Flash | ¥0.7 | ¥1.4 | 推理速度最快 |

*价格信息截至2026年2月。所有提供商都为新用户提供免费试用 tier 或信用额度。*

## 所有 API 都兼容 OpenAI

列出的所有提供商都使用 OpenAI 的聊天/完成格式。无需安装额外的 SDK——只需修改 `baseUrl` 和 `apiKey` 即可。

## 其他特性

- **自动切换**：如果某个提供商的服务不可用，系统会自动尝试下一个可用提供商；
- **费用跟踪**：可以查看每个模型的令牌使用情况和预估费用；
- **智能路由**：根据您的任务描述推荐最适合的模型；
- **批量比较**：可以向多个模型发送相同的提示并比较结果；
- **上下文感知**：会记住您在每次对话中选择的模型偏好。

## 链接

- 🦐 试试我们的 AI Plaza：https://ai.xudd-v.com
- 📦 ClawHub：https://clawhub.ai/Xdd-xund/chinese-llm-router
- 💬 提供反馈：https://ai.xudd-v.com/connect.html