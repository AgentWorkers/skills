---
name: alibaba-cloud-model-setup
description: 配置 OpenClaw 以使用阿里云 Bailian 提供商（按需付费或编码计划）的过程需要遵循严格的交互式流程。该配置支持 5 种站点选项以及多种旗舰型号系列。当用户需要添加、切换或修复 OpenClaw 中的阿里云/Qwen 提供商配置时，请使用此技能。
---
# 阿里云模型设置（Bailian）

## 概述

使用此技能可以以最少的手动编辑量将阿里云Bailian配置为OpenClaw的模型提供者。支持**按量付费**（Pay-As-You-Go）和**订阅制**（Coding Plan）两种订阅类型。

## 主要特性

### 1️⃣ 固定的提供者名称
- **提供者**：`bailian`（已修正拼写错误！）

### 2️⃣ 5个站点选项

| 订阅类型 | 站点 | 基本URL |
|-----------|------|----------|
| **按量付费** | 中国（CN） | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| **按量付费** | 国际（INTL） | `https://dashscope-intl.aliyuncs.com/compatible-mode/v1` |
| **按量付费** | 美国（US） | `https://dashscope-us.aliyuncs.com/compatible-mode/v1` |
| **订阅制** | 中国（CN） | `https://coding.dashscope.aliyuncs.com/v1` |
| **订阅制** | 国际（INTL） | `https://coding-intl.dashscope.aliyuncs.com/v1` |

### 3️⃣ 旗舰模型系列（每个系列包含2-3代模型）

**Qwen-Max**（最佳性能）：
- `qwen-max`
- `qwen-max-2025-01-25`

**Qwen-Plus**（性能均衡）：
- `qwen-plus`
- `qwen-plus-2025-01-15`

**Qwen-Flash**（快速且经济实惠）：
- `qwen-flash`
- `qwen-flash-2025-01-15`

**Qwen-Coder**（代码专家）：
- `qwen3-coder-plus`
- `qwen3-coder-next`
- `qwen2.5-coder-32b-instruct`

### 4️⃣ 最新的Qwen模型（所有用户均可使用）

- `qwen3.5-plus`
- `qwen3-max-2026-01-23`

### 5️⃣ 订阅制专属模型（第三方）

- `MiniMax-M2.5`（MiniMax）
- `glm-5` / `glm-4.7`（智谱AI）
- `kimi-k2.5`（月之暗面）

**总计**：
- **按量付费**：11个模型（4个旗舰系列 + 2个最新Qwen模型）
- **订阅制**：15个模型（按量付费模型 + 4个第三方专属模型）

## 工作流程

1. **确认订阅类型**：按量付费或订阅制
2. **选择站点**：根据订阅类型选择相应的站点
3. **运行交互式脚本**以收集以下信息：
   - API密钥（需进行验证）
   - API密钥的存储方式（建议使用环境变量或内联方式）
   - 主要模型选择
   - 是否将其设置为默认模型
4. **在配置写入之前，验证API密钥是否与所选站点匹配**
5. **在修改配置之前，备份现有配置**
6. **使用提供者、模型和默认设置更新配置**
7. **验证JSON格式并报告最终状态**

## 运行脚本

执行：

```bash
python3 scripts/alibaba_cloud_model_setup.py
```

**非交互式使用的可选参数：**

```bash
python3 scripts/alibaba_cloud_model_setup.py \
  --plan-type coding \
  --site cn \
  --api-key-source env \
  --env-var DASHSCOPE_API_KEY \
  --models qwen3.5-plus,qwen3-max-2026-01-23,qwen3-coder-plus \
  --model qwen3.5-plus \
  --set-default
```

**列出可用模型（不写入配置）：**

```bash
python3 scripts/alibaba_cloud_model_setup.py \
  --plan-type coding \
  --site cn \
  --list-models \
  --non-interactive
```

## 安全规则（强制要求）

1. 进行配置更改时，务必运行 `python3 scripts/alibaba_cloud_model_setup.py`。
2. 使用此技能时，切勿手动编辑 `~/.openclaw/openclaw.json` 文件。
3. 在写入配置之前，务必验证API密钥。
4. 在覆盖现有配置之前，务必创建备份。
5. 在使用环境变量模式时，只有在环境变量检测成功后，才能继续写入配置。

## 默认行为

- 按以下顺序检测配置文件路径：
  - `~/.openclaw/openclaw.json`
  - `~/.moltbot/moltbot.json`
  - `~/.clawdbot/clawdbot.json`
- 如果这些文件不存在，则创建 `~/.openclaw/openclaw.json`。
- 将提供者设置为 `bailian`，并使用与OpenAI兼容的API模式。
- 在覆盖现有文件之前，创建带有时间戳的备份。
- 保留与当前提供者无关的配置部分。
- 将 `models.mode` 设置为 `merge`，以保留其他提供者的配置。

## 验证检查清单

配置完成后：
1. 通过运行 `python3 -m json.tool <config-path>` 来确认JSON格式是否有效。
2. 确保 `modelsproviders.bailian.baseUrl` 与所选站点匹配。
3. 确保 `modelsproviders.bailian.models` 包含预期的模型ID。
4. 当启用默认模型时，确保 `agentsdefaults.model.primary` 的值为 `bailian/<model-id>`。
5. 启动仪表板（`openclaw dashboard`）或TUI（`openclaw tui`），并验证模型调用是否成功。

## 示例配置输出

### 中国站点的订阅制配置

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "bailian": {
        "baseUrl": "https://coding.dashscope.aliyuncs.com/v1",
        "apiKey": "YOUR_API_KEY",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3.5-plus",
            "name": "Qwen3.5 Plus",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 1000000,
            "maxTokens": 65536
          },
          {
            "id": "qwen3-max-2026-01-23",
            "name": "Qwen3 Max 2026-01-23",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 262144,
            "maxTokens": 65536
          },
          {
            "id": "qwen3-coder-next",
            "name": "Qwen3 Coder Next",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 262144,
            "maxTokens": 65536
          },
          {
            "id": "qwen3-coder-plus",
            "name": "Qwen3 Coder Plus",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 1000000,
            "maxTokens": 65536
          },
          {
            "id": "MiniMax-M2.5",
            "name": "MiniMax M2.5",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 204800,
            "maxTokens": 131072
          },
          {
            "id": "glm-5",
            "name": "GLM-5",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 202752,
            "maxTokens": 16384
          },
          {
            "id": "glm-4.7",
            "name": "GLM-4.7",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 202752,
            "maxTokens": 16384
          },
          {
            "id": "kimi-k2.5",
            "name": "Kimi K2.5",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 262144,
            "maxTokens": 32768
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian/qwen3.5-plus"
      },
      "models": {
        "bailian/qwen3.5-plus": {},
        "bailian/qwen3-max-2026-01-23": {},
        "bailian/qwen3-coder-next": {},
        "bailian/qwen3-coder-plus": {},
        "bailian/MiniMax-M2.5": {},
        "bailian/glm-5": {},
        "bailian/glm-4.7": {},
        "bailian/kimi-k2.5": {}
      }
    }
  }
}
```

## 参考资料

- 端点和字段约定：`references/openclaw_alibaba_cloud.md`

---

*版本：0.1.4*  
*更新时间：2026-03-02*  
*变更内容：修正提供者名称的拼写错误（balian → bailian），新增订阅制支持，增加5个站点选项，按量付费提供11个模型（包括旗舰系列和最新Qwen模型），订阅制提供15个模型（包括4个第三方专属模型）