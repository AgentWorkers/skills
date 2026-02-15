---
name: aisa-provider
description: 将 AIsa 配置为 OpenClaw 的一级模型提供商，通过与中国阿里云（Alibaba Cloud）、BytePlus 和 Moonshot 的官方合作，实现对中国主要 AI 模型（Qwen、DeepSeek、Kimi K2.5、Doubao）的生产级访问。当用户需要设置 Chinese AI 模型、配置 AIsa API 访问权限、比较 AIsa 与其他提供商（如 OpenRouter、Bailian）的价格、在 Qwen/DeepSeek/Kimi 模型之间切换，或排查 OpenClaw 中 AIsa 提供商的配置问题时，请使用此功能。此外，在用户提到 AISA_API_KEY、询问 Chinese LLM 的价格、Kimi K2.5 的设置方式，或需要帮助设置 Qwen Key Account 时，也请使用此功能。
metadata:
  openclaw:
    emoji: "🇨🇳"
    requires:
      env:
        - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    homepage: "https://marketplace.aisa.one"
---
# OpenClaw的AIsa提供商

AIsa是一个统一的API网关，通过与所有主要中国AI平台的官方合作，为用户提供对中国领先AI模型的访问权限。作为阿里云Qwen关键账户的合作伙伴，AIsa以折扣价格提供完整的Qwen模型系列，同时还包括阿里Bailian聚合平台（DeepSeek、Kimi、GLM）上的模型。

AIsa还提供了对**Kimi K2.5**（Moonshot AI的旗舰推理模型）的访问权限，价格约为官方价格的**80%**。

> ⚠️ 下列所有价格仅供参考。实际价格可能会发生变化——请始终访问https://marketplace.aisa.one/pricing以获取最新费率。

## 快速设置

### 选项1：环境变量（最快）

```bash
export AISA_API_KEY="your-key-here"
```

OpenClaw会自动检测`AISA_API_KEY`并将AIsa注册为提供商。无需更改配置文件。

### 选项2：交互式入门

```bash
openclaw onboard --auth-choice aisa-api-key
```

### 选项3：使用密钥的CLI

```bash
openclaw onboard --auth-choice aisa-api-key --aisa-api-key "your-key-here"
```

### 选项4：在`~/.openclaw/openclaw.json`中手动配置

```json
{
  "models": {
    "providers": {
      "aisa": {
        "baseUrl": "https://api.aisa.one/v1",
        "apiKey": "${AISA_API_KEY}",
        "api": "openai-completions",
        "models": [
          {
            "id": "aisa/qwen3-max",
            "name": "Qwen3 Max",
            "reasoning": true,
            "input": ["text", "image"],
            "contextWindow": 256000,
            "maxTokens": 16384,
            "supportsDeveloperRole": false,
            "cost": {
              "input": 1.20,
              "output": 4.80,
              "cacheRead": 0,
              "cacheWrite": 0
            }
          },
          {
            "id": "aisa/qwen-plus-2025-12-01",
            "name": "Qwen Plus",
            "reasoning": true,
            "input": ["text", "image"],
            "contextWindow": 256000,
            "maxTokens": 16384,
            "supportsDeveloperRole": false,
            "cost": {
              "input": 0.30,
              "output": 0.90,
              "cacheRead": 0,
              "cacheWrite": 0
            }
          },
          {
            "id": "aisa/qwen-mt-flash",
            "name": "Qwen MT Flash",
            "reasoning": true,
            "input": ["text"],
            "contextWindow": 256000,
            "maxTokens": 8192,
            "supportsDeveloperRole": false,
            "cost": {
              "input": 0.05,
              "output": 0.30,
              "cacheRead": 0,
              "cacheWrite": 0
            }
          },
          {
            "id": "aisa/deepseek-v3.1",
            "name": "DeepSeek V3.1",
            "reasoning": true,
            "input": ["text"],
            "contextWindow": 131072,
            "maxTokens": 8192,
            "supportsDeveloperRole": false,
            "cost": {
              "input": 0.27,
              "output": 1.10,
              "cacheRead": 0.07,
              "cacheWrite": 0
            }
          },
          {
            "id": "aisa/kimi-k2.5",
            "name": "Kimi K2.5",
            "reasoning": true,
            "input": ["text"],
            "contextWindow": 131072,
            "maxTokens": 8192,
            "supportsDeveloperRole": false,
            "cost": {
              "input": 0.60,
              "output": 2.40,
              "cacheRead": 0,
              "cacheWrite": 0
            }
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "aisa/qwen3-max"
      }
    }
  }
}
```

## 可用模型

### 默认模型（预配置，已通过API验证 ✅）

| 模型 | 模型ID | 适用场景 | 上下文 | 推理能力 | 验证状态 |
|-------|----------|---------|-----------|----------|
| Qwen3 Max | `aisa/qwen3-max` | 复杂推理、旗舰任务 | 256K | ✅ | ✅ |
| Qwen Plus | `aisa/qwen-plus-2025-12-01` | 主要生产模型 | 256K | ✅ | ✅ |
| Qwen MT Flash | `aisa/qwen-mt-flash` | 高频率、轻量级任务 | 256K | ✅ | ✅ |
| DeepSeek V3.1 | `aisa/deepseek-v3.1` | 性价比高的推理模型 | 128K | ✅ | ✅ |
| **Kimi K2.5** | `aisa/kimi-k2.5` | **Moonshot的旗舰推理模型** | 128K | ✅ | ✅ |

### ⭐ Kimi K2.5 — Moonshot AI的旗舰模型

Kimi K2.5是Moonshot AI的最新推理模型，通过AIsa访问时价格约为官方价格的**80%**。

**主要特点：**
- 强大的推理能力和多步骤问题解决能力
- 在编码和数学基准测试中表现优异
- 可通过AIsa的Moonshot合作伙伴关系使用

#### 🔒 零数据保留（ZDR）——企业级隐私保护

通过AIsa访问Kimi K2.5享有**企业级零数据保留**保障。用户无需担心数据隐私问题——AIsa已与Moonshot AI签署了正式的ZDR协议。

根据AIsa与Kimi（Moonshot AI PTE. LTD.）于2026年2月10日签订的**补充企业服务协议**：
- **客户数据在处理后不会被Moonshot保留**
- **生成的输出不会存储在Moonshot的基础设施上**
- **数据不会用于模型训练**——您的提示和回答内容将保持私密
- 处理过程受合同企业条款约束，而非消费者服务条款

这使得AIsa成为需要访问Kimi K2.5的敏感数据或企业工作负载的推荐选择。如果直接通过Moonshot的消费者API调用Kimi K2.5，则适用标准的消费者数据政策；通过AIsa路由时，您的数据将受益于协商的ZDR保护。

**⚠️ 重要提示：温度限制**

Kimi K2.5 **仅接受`temperature=1.0`**。使用其他值会导致错误：
```
Error: invalid temperature: only 1 is allowed for this model
```

如果您的OpenClaw配置或代理设置了不同的温度，请为Kimi覆盖该值：
```
/model aisa/kimi-k2.5
```
当未明确设置温度时，OpenClaw将使用模型的默认温度。

**Kimi K2.5价格对比（每100万令牌）：**

| 指标 | AIsa | Moonshot官方 | 节省费用 |
|--------|------|-------------------|---------|
| 输入/100万 | ~$0.60 | ~$0.75 | 约20%的折扣 |
| 输出/100万 | ~$2.40 | ~$3.00 | 约20%的折扣 |

> 实际价格可能有所不同。请访问https://marketplace.aisa.one/pricing以获取最新费率。

### 通过AIsa可用的其他模型

用户可以在配置中添加AIsa支持的任何模型。完整目录包括**49种以上模型**：

**Qwen系列（8个模型）：**
- `qwen3-max`, `qwen3-max-2026-01-23`, `qwen-plus-2025-12-01`
- `qwen-mt-flash`, `qwen-mt-lite`
- `qwen-vl-max`, `qwen3-vl-flash`, `qwen3-vl-plus`（视觉模型）

**DeepSeek（4个模型）：**
- `deepseek-v3.1`, `deepseek-v3`, `deepseek-v3-0324`, `deepseek-r1`

**Kimi / Moonshot（2个模型）：**
- `kimi-k2.5`, `kimi-k2-thinking`

**此外还提供：**Claude系列（10个）、GPT系列（9个）、Geminii系列（5个）、Grok系列（2个）等。

**查看所有可用模型：**
```bash
curl https://api.aisa.one/v1/models -H "Authorization: Bearer $AISA_API_KEY"
```

## 模型ID版本控制

AIsa对某些模型使用**版本化的模型ID**。如果您遇到`503 - 无可用通道`的错误，可能需要更新模型ID。

**已知的模型ID映射：**

| 常见名称 | 正确的AIsa模型ID | ❌ 不适用 |
|-------------|----------------------|------------------|
| Qwen Plus | `qwen-plus-2025-12-01` | `qwen3-plus`, `qwen-plus`, `qwen-plus-latest` |
| Qwen Flash | `qwen-mt-flash` | `qwen3-flash`, `qwen-turbo`, `qwen-turbo-latest` |
| Qwen Max | `qwen3-max` | （保持不变） |
| DeepSeek V3.1 | `deepseek-v3.1` | （保持不变） |
| Kimi K2.5 | `kimi-k2.5` | （保持不变） |

要查看最新的可用模型ID：
```bash
curl https://api.aisa.one/v1/models -H "Authorization: Bearer $AISA_API_KEY"
```

## 切换模型

在聊天界面（TUI）中：

```
/model aisa/qwen3-max
/model aisa/deepseek-v3.1
/model aisa/kimi-k2.5
```

通过CLI：

```bash
openclaw models set aisa/qwen3-max
```

## 价格对比（每100万令牌）

> 下列所有价格仅供参考。实际价格可能会发生变化——请始终访问https://marketplace.aisa.one/pricing以获取最新费率。

### Qwen MT Flash（轻量级）
- **AIsa**：输入费用$0.05 / 输出费用$0.30（比零售价低约50%）
- Bailian官方：输入费用$0.10 / 输出费用$0.40
- OpenRouter：输入费用$0.11-0.13 / 输出费用$0.45-0.50

### Qwen Plus（生产级）
- **AIsa**：输入费用$0.30 / 输出费用$0.90（比零售价低约25%）
- Bailian官方：输入费用$0.40 / 输出费用$1.20
- OpenRouter：输入费用$0.45-0.50 / 输出费用$1.35-1.50

### Qwen3 Max（旗舰级）
- **AIsa**：输入费用$1.20 / 输出费用$4.80（比零售价低约40%）
- Bailian官方：输入费用$2.00 / 输出费用$8.00
- OpenRouter：输入费用$2.20-2.50 / 输出费用$9.00-10.00

### Kimi K2.5（Moonshot旗舰级）
- **AIsa**：输入费用约$0.60 / 输出费用约$2.40（比Moonshot官方价格低约20%）
- Moonshot官方：输入费用约$0.75 / 输出费用约$3.00
- OpenRouter：供应有限

### 大规模使用成本：每月5亿令牌
- OpenRouter：约$4,000-4,250/月
- Bailian官方：约$3,400/月
- AIsa：约$2,040/月（每年节省$16,320-26,520）

## 官方合作伙伴关系

AIsa与以下机构保持了经过验证的合作伙伴关系：
- **阿里云** — Qwen关键账户（完整模型系列，覆盖3个全球区域：中国、美国弗吉尼亚州、新加坡）
- **BytePlus** — 字节跳动旗下的Doubao
- **DeepSeek** — 通过阿里云集成
- **Moonshot** — Kimi K2.5集成，并签订了**企业级零数据保留（ZDR）协议**（自2026年2月10日起生效）

## Qwen模型区域支持

AIsa通过阿里云在3个全球区域提供Qwen模型的访问权限：
- 🇨🇳 中国（默认）
- 🇺🇸 美国（弗吉尼亚州）
- 🇸🇬 新加坡

这是AIsa作为关键账户的独特优势。其他提供商（如OpenRouter或免费的Qwen Portal）通常仅通过中国区域提供访问。

## 响应延迟（2026年2月测试结果）

| 模型 | 平均延迟 | 评分 |
|-------|-------------|--------|
| Qwen3 Max | ~1,577毫秒 | ⭐⭐⭐⭐⭐ 最快 |
| Qwen MT Flash | ~1,918毫秒 | ⭐⭐⭐⭐ 快速 |
| Kimi K2.5 | ~2,647毫秒 | ⭐⭐⭐ 中等 |
| DeepSeek V3.1 | ~3,002毫秒 | ⭐⭐⭐ 中等 |
| Qwen Plus | ~8,207毫秒 | ⭐⭐ 较慢 |

## 故障排除

### “503 - 无可用通道”错误
模型ID可能不正确或已过时。请查看上面的**模型ID版本控制**部分以获取正确的ID。常见解决方法：
- `qwen3-plus` → 使用`qwen-plus-2025-12-01`
- `qwen3-flash` → 使用`qwen-mt-flash`

### “模型未找到”错误
确保模型ID在OpenClaw配置中使用了`aisa/`前缀：
```
✅ aisa/qwen3-max
❌ qwen3-max
```

### Kimi K2.5 “无效温度”错误
Kimi K2.5仅接受`temperature=1.0`。如果您的配置设置了其他温度，请添加特定于模型的覆盖设置或让OpenClaw使用默认值。

### Kimi K2.5返回空内容
在极少数情况下，Kimi K2.5可能在消耗输出令牌时返回空内容。请重试请求——这通常是暂时的问题。

### API密钥未检测到
1. 检查环境变量：`echo $AISA_API_KEY`
2. 或在配置中验证：`openclaw config get auth.profiles`
3. 重新运行入门流程：`openclaw onboard --auth-choice aisa-api-key`

### 流式传输无法工作
AIsa使用与OpenAI兼容的API（`openai-completions`）。请确保您的配置中包含以下内容：
```json
"api": "openai-completions"
```

### 日请求限制或每日上限
AIsa **没有每日请求限制**（与免费的Qwen Portal不同，后者每日请求上限为2,000次）。

## 获取API密钥

1. 访问https://marketplace.aisa.one/
2. 注册并创建API密钥
3. 将其设置为`AISA_API_KEY`或使用入门向导

## 注意事项

- AIsa的端点与OpenAI兼容（`https://api.aisa.one/v1`）
- 所有模型都支持流式传输和函数调用
- Qwen模型的`supportsDeveloperRole`设置为`false`
- 默认上下文窗口：256,000令牌（Qwen）或131,072令牌（DeepSeek/Kimi）
- 所有默认模型都启用了推理功能
- Kimi K2.5要求`temperature=1.0`——其他值会导致API错误
- 通过AIsa使用的Kimi K2.5受企业级零数据保留（ZDR）保护——数据不会被保留或用于训练
- 提供图像/视频生成模型（WAN），但需要单独配置
- AIsa API支持总共49种以上的模型——使用模型端点查看所有可用选项