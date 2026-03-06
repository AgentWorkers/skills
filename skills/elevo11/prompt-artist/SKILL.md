---
name: prompt-artist
description: >
  优化并生成适用于 AI 艺术平台的文本到图像的提示语句。当用户需要执行以下操作时可以使用该服务：  
  (1) 为 Midjourney、Nano Banana、Dreamina、Qwen 等图像生成工具优化提示语句；  
  (2) 将简单的描述转换为专业的提示语句；  
  (3) 生成针对特定平台的提示语句变体；  
  (4) 添加风格、光照或构图修饰符；  
  (5) 创建负向提示（即用于生成特定类型或效果的提示语句）。  
  支持中文和英文输入。  
  集成 SkillPay.me 服务，每次调用费用为 0.005 美元。
---
# Prompt Artist

这是一个专为 Midjourney、Nano Banana、Dreamina 和 Qwen 设计的 AI 艺术提示优化工具，每次调用服务的费用为 0.005 美元。

## 命令

| 命令 | 脚本 | 描述 |
|:---|:---|:---|
| **optimize** | `scripts/optimize.py` | 为目标平台优化艺术创作提示 |
| **multi** | `scripts/multi_platform.py` | 一次性为所有平台生成艺术创作提示 |
| **style** | `scripts/style_library.py` | 浏览/应用不同的艺术风格 |
| **billing** | `scripts/billing.py` | 处理 SkillPay 的计费、余额和支付相关操作 |

## 工作流程

```
1. Billing:   python3 scripts/billing.py --charge --user-id <id>
2. Optimize:  python3 scripts/optimize.py --prompt "一只猫在月光下" --platform midjourney
3. Multi:     python3 scripts/multi_platform.py --prompt "sunset over mountains"
4. Styles:    python3 scripts/style_library.py --list
```

## 示例

```bash
# Optimize for Midjourney
python3 scripts/optimize.py --prompt "一只猫在月光下" --platform midjourney --style cinematic

# Optimize for Dreamina
python3 scripts/optimize.py --prompt "cyberpunk city" --platform dreamina --ratio 16:9

# All platforms at once
python3 scripts/multi_platform.py --prompt "beautiful girl in garden" --style anime

# List styles
python3 scripts/style_library.py --list
python3 scripts/style_library.py --category photography
```

## 配置

| 环境变量 | 是否必需 | 描述 |
|:---|:---|:---|
| `SKILLPAY_API_KEY` | 是 | SkillPay.me 的 API 密钥 |

## 参考资料

有关特定平台的提示语法和限制，请参阅 `references/platform-specs.md`。